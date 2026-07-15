from datetime import date, time
from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.appointment import Appointment, AppointmentStatus
from app.models.department import Department
from app.models.doctor import Doctor
from app.models.doctor_schedule import DoctorSchedule


class AppointmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, appointment: Appointment) -> Appointment:
        self.session.add(appointment)
        await self.session.commit()
        await self.session.refresh(appointment)
        return appointment

    async def get_by_id(self, appointment_id: UUID) -> Appointment | None:
        result = await self.session.execute(
            select(Appointment).where(Appointment.id == appointment_id)
        )
        return result.scalar_one_or_none()

    async def list(
        self,
        *,
        doctor_id: UUID | None = None,
        department_id: UUID | None = None,
        appointment_date: date | None = None,
        status: AppointmentStatus | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Appointment]:
        query: Select[tuple[Appointment]] = select(Appointment).order_by(
            Appointment.appointment_date,
            Appointment.appointment_start_time,
        )
        if doctor_id is not None:
            query = query.where(Appointment.doctor_id == doctor_id)
        if department_id is not None:
            query = query.where(Appointment.department_id == department_id)
        if appointment_date is not None:
            query = query.where(Appointment.appointment_date == appointment_date)
        if status is not None:
            query = query.where(Appointment.status == status)

        result = await self.session.execute(query.limit(limit).offset(offset))
        return list(result.scalars().all())

    async def update(self, appointment: Appointment) -> Appointment:
        await self.session.commit()
        await self.session.refresh(appointment)
        return appointment

    async def get_doctor_by_id(self, doctor_id: UUID) -> Doctor | None:
        result = await self.session.execute(select(Doctor).where(Doctor.id == doctor_id))
        return result.scalar_one_or_none()

    async def get_department_by_id(self, department_id: UUID) -> Department | None:
        result = await self.session.execute(
            select(Department).where(Department.id == department_id)
        )
        return result.scalar_one_or_none()

    async def has_overlapping_appointment(
        self,
        *,
        doctor_id: UUID,
        appointment_date: date,
        start_time: time,
        end_time: time,
        exclude_appointment_id: UUID | None = None,
    ) -> bool:
        query = select(Appointment).where(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == appointment_date,
            Appointment.status.in_(
                [
                    AppointmentStatus.PENDING,
                    AppointmentStatus.CONFIRMED,
                    AppointmentStatus.CHECKED_IN,
                    AppointmentStatus.COMPLETED,
                    AppointmentStatus.NO_SHOW,
                ]
            ),
            Appointment.appointment_start_time < end_time,
            Appointment.appointment_end_time > start_time,
        )
        if exclude_appointment_id is not None:
            query = query.where(Appointment.id != exclude_appointment_id)

        result = await self.session.execute(query.limit(1))
        return result.scalar_one_or_none() is not None

    async def has_matching_available_schedule(
        self,
        *,
        doctor_id: UUID,
        weekday: int,
        start_time: time,
        end_time: time,
    ) -> bool:
        result = await self.session.execute(
            select(DoctorSchedule)
            .where(
                DoctorSchedule.doctor_id == doctor_id,
                DoctorSchedule.weekday == weekday,
                DoctorSchedule.is_available.is_(True),
                DoctorSchedule.start_time <= start_time,
                DoctorSchedule.end_time >= end_time,
            )
            .limit(1)
        )
        return result.scalar_one_or_none() is not None
