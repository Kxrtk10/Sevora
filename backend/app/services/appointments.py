from datetime import UTC, date, datetime, time
from uuid import UUID

from app.models.appointment import Appointment, AppointmentStatus
from app.models.doctor import Doctor
from app.repositories.appointment import AppointmentRepository
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


class AppointmentError(Exception):
    pass


class AppointmentNotFoundError(AppointmentError):
    pass


class DoctorNotFoundError(AppointmentError):
    pass


class DepartmentNotFoundError(AppointmentError):
    pass


class InactiveDoctorError(AppointmentError):
    pass


class InvalidAppointmentScheduleError(AppointmentError):
    pass


class DoubleBookingError(AppointmentError):
    pass


class InvalidStatusTransitionError(AppointmentError):
    pass


TERMINAL_STATUSES = {AppointmentStatus.CANCELLED, AppointmentStatus.COMPLETED}
ALLOWED_STATUS_TRANSITIONS = {
    AppointmentStatus.PENDING: {
        AppointmentStatus.CONFIRMED,
        AppointmentStatus.CHECKED_IN,
        AppointmentStatus.CANCELLED,
        AppointmentStatus.NO_SHOW,
    },
    AppointmentStatus.CONFIRMED: {
        AppointmentStatus.CHECKED_IN,
        AppointmentStatus.COMPLETED,
        AppointmentStatus.CANCELLED,
        AppointmentStatus.NO_SHOW,
    },
    AppointmentStatus.CHECKED_IN: {
        AppointmentStatus.COMPLETED,
        AppointmentStatus.CANCELLED,
        AppointmentStatus.NO_SHOW,
    },
    AppointmentStatus.COMPLETED: set(),
    AppointmentStatus.CANCELLED: set(),
    AppointmentStatus.NO_SHOW: {AppointmentStatus.CANCELLED},
}


class AppointmentService:
    def __init__(self, repository: AppointmentRepository) -> None:
        self.repository = repository

    async def create_appointment(self, payload: AppointmentCreate) -> Appointment:
        doctor = await self._get_schedulable_doctor(payload.doctor_id)
        await self._ensure_department_exists(payload.department_id)
        await self._validate_schedule(
            doctor=doctor,
            appointment_date=payload.appointment_date,
            start_time=payload.appointment_start_time,
            end_time=payload.appointment_end_time,
        )
        await self._ensure_slot_available(
            doctor_id=payload.doctor_id,
            appointment_date=payload.appointment_date,
            start_time=payload.appointment_start_time,
            end_time=payload.appointment_end_time,
        )

        appointment = Appointment(**payload.model_dump())
        return await self.repository.create(appointment)

    async def get_appointment(self, appointment_id: UUID) -> Appointment:
        appointment = await self.repository.get_by_id(appointment_id)
        if appointment is None:
            raise AppointmentNotFoundError
        return appointment

    async def list_appointments(
        self,
        *,
        doctor_id: UUID | None = None,
        department_id: UUID | None = None,
        appointment_date: date | None = None,
        status: AppointmentStatus | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Appointment]:
        return await self.repository.list(
            doctor_id=doctor_id,
            department_id=department_id,
            appointment_date=appointment_date,
            status=status,
            limit=limit,
            offset=offset,
        )

    async def update_appointment(
        self,
        appointment_id: UUID,
        payload: AppointmentUpdate,
    ) -> Appointment:
        appointment = await self.get_appointment(appointment_id)
        if appointment.status in TERMINAL_STATUSES:
            raise InvalidStatusTransitionError

        update_data = payload.model_dump(exclude_unset=True)
        candidate_doctor_id = update_data.get("doctor_id", appointment.doctor_id)
        candidate_department_id = update_data.get("department_id", appointment.department_id)
        candidate_date = update_data.get("appointment_date", appointment.appointment_date)
        candidate_start = update_data.get(
            "appointment_start_time",
            appointment.appointment_start_time,
        )
        candidate_end = update_data.get("appointment_end_time", appointment.appointment_end_time)

        doctor = await self._get_schedulable_doctor(candidate_doctor_id)
        await self._ensure_department_exists(candidate_department_id)
        await self._validate_schedule(
            doctor=doctor,
            appointment_date=candidate_date,
            start_time=candidate_start,
            end_time=candidate_end,
        )
        await self._ensure_slot_available(
            doctor_id=candidate_doctor_id,
            appointment_date=candidate_date,
            start_time=candidate_start,
            end_time=candidate_end,
            exclude_appointment_id=appointment.id,
        )

        for field, value in update_data.items():
            setattr(appointment, field, value)

        return await self.repository.update(appointment)

    async def cancel_appointment(self, appointment_id: UUID) -> Appointment:
        return await self.update_appointment_status(
            appointment_id,
            AppointmentStatus.CANCELLED,
        )

    async def update_appointment_status(
        self,
        appointment_id: UUID,
        status: AppointmentStatus,
    ) -> Appointment:
        appointment = await self.get_appointment(appointment_id)
        if appointment.status == status:
            return appointment
        if status not in ALLOWED_STATUS_TRANSITIONS[appointment.status]:
            raise InvalidStatusTransitionError

        appointment.status = status
        return await self.repository.update(appointment)

    async def _get_schedulable_doctor(self, doctor_id: UUID) -> Doctor:
        doctor = await self.repository.get_doctor_by_id(doctor_id)
        if doctor is None:
            raise DoctorNotFoundError
        if not doctor.is_active:
            raise InactiveDoctorError
        return doctor

    async def _ensure_department_exists(self, department_id: UUID) -> None:
        department = await self.repository.get_department_by_id(department_id)
        if department is None:
            raise DepartmentNotFoundError

    async def _ensure_slot_available(
        self,
        *,
        doctor_id: UUID,
        appointment_date: date,
        start_time: time,
        end_time: time,
        exclude_appointment_id: UUID | None = None,
    ) -> None:
        has_overlap = await self.repository.has_overlapping_appointment(
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            start_time=start_time,
            end_time=end_time,
            exclude_appointment_id=exclude_appointment_id,
        )
        if has_overlap:
            raise DoubleBookingError

    async def _validate_schedule(
        self,
        *,
        doctor: Doctor,
        appointment_date: date,
        start_time: time,
        end_time: time,
    ) -> None:
        if start_time >= end_time:
            raise InvalidAppointmentScheduleError

        duration_minutes = self._duration_minutes(start_time, end_time)
        if duration_minutes < 15 or duration_minutes > 240:
            raise InvalidAppointmentScheduleError

        appointment_start = datetime.combine(appointment_date, start_time, tzinfo=UTC)
        if appointment_start <= datetime.now(UTC):
            raise InvalidAppointmentScheduleError

        weekday = appointment_date.weekday()
        has_schedule = await self.repository.has_matching_available_schedule(
            doctor_id=doctor.id,
            weekday=weekday,
            start_time=start_time,
            end_time=end_time,
        )
        if not has_schedule:
            raise InvalidAppointmentScheduleError

    def _duration_minutes(self, start_time: time, end_time: time) -> int:
        start = datetime.combine(date.min, start_time)
        end = datetime.combine(date.min, end_time)
        return int((end - start).total_seconds() // 60)
