from datetime import time
from uuid import UUID

from app.models.department import Department
from app.models.doctor import Doctor
from app.models.doctor_schedule import DoctorSchedule
from app.models.hospital import Hospital
from app.repositories.hospital_domain import HospitalDomainRepository
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from app.schemas.doctor import (
    DoctorCreate,
    DoctorScheduleCreate,
    DoctorScheduleUpdate,
    DoctorUpdate,
)
from app.schemas.hospital import HospitalCreate, HospitalUpdate


class HospitalDomainError(Exception):
    pass


class NotFoundError(HospitalDomainError):
    pass


class DuplicateDepartmentError(HospitalDomainError):
    pass


class InvalidRelationshipError(HospitalDomainError):
    pass


class DeleteBlockedError(HospitalDomainError):
    pass


class InvalidScheduleError(HospitalDomainError):
    pass


class OverlappingScheduleError(HospitalDomainError):
    pass


class InactiveDoctorScheduleError(HospitalDomainError):
    pass


class HospitalDomainService:
    def __init__(self, repository: HospitalDomainRepository) -> None:
        self.repository = repository

    async def create_hospital(self, payload: HospitalCreate) -> Hospital:
        hospital = Hospital(**payload.model_dump(mode="json"))
        return await self.repository.create(hospital)

    async def get_hospital(self, hospital_id: UUID) -> Hospital:
        hospital = await self.repository.get_hospital(hospital_id)
        if hospital is None:
            raise NotFoundError
        return hospital

    async def list_hospitals(self, *, limit: int = 100, offset: int = 0) -> list[Hospital]:
        return await self.repository.list_hospitals(limit=limit, offset=offset)

    async def update_hospital(self, hospital_id: UUID, payload: HospitalUpdate) -> Hospital:
        hospital = await self.get_hospital(hospital_id)
        for field, value in payload.model_dump(exclude_unset=True, mode="json").items():
            setattr(hospital, field, value)
        return await self.repository.update(hospital)

    async def delete_hospital(self, hospital_id: UUID) -> None:
        hospital = await self.get_hospital(hospital_id)
        if await self.repository.has_departments_or_doctors(hospital_id):
            raise DeleteBlockedError
        await self.repository.delete(hospital)

    async def create_department(self, payload: DepartmentCreate) -> Department:
        await self.get_hospital(payload.hospital_id)
        await self._ensure_unique_department_name(
            hospital_id=payload.hospital_id,
            name=payload.name,
        )
        department = Department(**payload.model_dump())
        return await self.repository.create(department)

    async def get_department(self, department_id: UUID) -> Department:
        department = await self.repository.get_department(department_id)
        if department is None:
            raise NotFoundError
        return department

    async def list_departments(
        self,
        *,
        hospital_id: UUID | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Department]:
        return await self.repository.list_departments(
            hospital_id=hospital_id,
            limit=limit,
            offset=offset,
        )

    async def update_department(
        self,
        department_id: UUID,
        payload: DepartmentUpdate,
    ) -> Department:
        department = await self.get_department(department_id)
        update_data = payload.model_dump(exclude_unset=True)
        candidate_hospital_id = update_data.get("hospital_id", department.hospital_id)
        candidate_name = update_data.get("name", department.name)
        await self.get_hospital(candidate_hospital_id)
        await self._ensure_unique_department_name(
            hospital_id=candidate_hospital_id,
            name=candidate_name,
            exclude_department_id=department.id,
        )
        for field, value in update_data.items():
            setattr(department, field, value)
        return await self.repository.update(department)

    async def delete_department(self, department_id: UUID) -> None:
        department = await self.get_department(department_id)
        if await self.repository.has_doctors(department_id):
            raise DeleteBlockedError
        await self.repository.delete(department)

    async def create_doctor(self, payload: DoctorCreate) -> Doctor:
        await self._validate_doctor_relationship(payload.hospital_id, payload.department_id)
        doctor = Doctor(**payload.model_dump())
        return await self.repository.create(doctor)

    async def get_doctor(self, doctor_id: UUID) -> Doctor:
        doctor = await self.repository.get_doctor(doctor_id)
        if doctor is None:
            raise NotFoundError
        return doctor

    async def list_doctors(
        self,
        *,
        hospital_id: UUID | None = None,
        department_id: UUID | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Doctor]:
        return await self.repository.list_doctors(
            hospital_id=hospital_id,
            department_id=department_id,
            limit=limit,
            offset=offset,
        )

    async def update_doctor(self, doctor_id: UUID, payload: DoctorUpdate) -> Doctor:
        doctor = await self.get_doctor(doctor_id)
        update_data = payload.model_dump(exclude_unset=True)
        candidate_hospital_id = update_data.get("hospital_id", doctor.hospital_id)
        candidate_department_id = update_data.get("department_id", doctor.department_id)
        await self._validate_doctor_relationship(candidate_hospital_id, candidate_department_id)
        for field, value in update_data.items():
            setattr(doctor, field, value)
        return await self.repository.update(doctor)

    async def delete_doctor(self, doctor_id: UUID) -> None:
        doctor = await self.get_doctor(doctor_id)
        await self.repository.delete(doctor)

    async def create_schedule(self, payload: DoctorScheduleCreate) -> DoctorSchedule:
        doctor = await self.get_doctor(payload.doctor_id)
        self._validate_doctor_for_schedule(doctor)
        self._validate_schedule_window(payload.start_time, payload.end_time, payload.slot_duration)
        await self._ensure_schedule_available(
            doctor_id=payload.doctor_id,
            weekday=payload.weekday,
            start_time=payload.start_time,
            end_time=payload.end_time,
        )
        schedule = DoctorSchedule(**payload.model_dump())
        return await self.repository.create(schedule)

    async def get_schedule(self, schedule_id: UUID) -> DoctorSchedule:
        schedule = await self.repository.get_schedule(schedule_id)
        if schedule is None:
            raise NotFoundError
        return schedule

    async def list_schedules(
        self,
        *,
        doctor_id: UUID | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[DoctorSchedule]:
        return await self.repository.list_schedules(
            doctor_id=doctor_id,
            limit=limit,
            offset=offset,
        )

    async def update_schedule(
        self,
        schedule_id: UUID,
        payload: DoctorScheduleUpdate,
    ) -> DoctorSchedule:
        schedule = await self.get_schedule(schedule_id)
        update_data = payload.model_dump(exclude_unset=True)
        candidate_doctor_id = update_data.get("doctor_id", schedule.doctor_id)
        candidate_weekday = update_data.get("weekday", schedule.weekday)
        candidate_start = update_data.get("start_time", schedule.start_time)
        candidate_end = update_data.get("end_time", schedule.end_time)
        candidate_slot_duration = update_data.get("slot_duration", schedule.slot_duration)

        doctor = await self.get_doctor(candidate_doctor_id)
        self._validate_doctor_for_schedule(doctor)
        self._validate_schedule_window(candidate_start, candidate_end, candidate_slot_duration)
        await self._ensure_schedule_available(
            doctor_id=candidate_doctor_id,
            weekday=candidate_weekday,
            start_time=candidate_start,
            end_time=candidate_end,
            exclude_schedule_id=schedule.id,
        )

        for field, value in update_data.items():
            setattr(schedule, field, value)
        return await self.repository.update(schedule)

    async def delete_schedule(self, schedule_id: UUID) -> None:
        schedule = await self.get_schedule(schedule_id)
        await self.repository.delete(schedule)

    async def _validate_doctor_relationship(
        self,
        hospital_id: UUID,
        department_id: UUID,
    ) -> None:
        await self.get_hospital(hospital_id)
        department = await self.get_department(department_id)
        if department.hospital_id != hospital_id:
            raise InvalidRelationshipError

    async def _ensure_unique_department_name(
        self,
        *,
        hospital_id: UUID,
        name: str,
        exclude_department_id: UUID | None = None,
    ) -> None:
        duplicate = await self.repository.get_department_by_hospital_and_name(
            hospital_id=hospital_id,
            name=name,
            exclude_department_id=exclude_department_id,
        )
        if duplicate is not None:
            raise DuplicateDepartmentError

    async def _ensure_schedule_available(
        self,
        *,
        doctor_id: UUID,
        weekday: int,
        start_time: time,
        end_time: time,
        exclude_schedule_id: UUID | None = None,
    ) -> None:
        has_overlap = await self.repository.has_overlapping_schedule(
            doctor_id=doctor_id,
            weekday=weekday,
            start_time=start_time,
            end_time=end_time,
            exclude_schedule_id=exclude_schedule_id,
        )
        if has_overlap:
            raise OverlappingScheduleError

    def _validate_doctor_for_schedule(self, doctor: Doctor) -> None:
        if not doctor.is_active:
            raise InactiveDoctorScheduleError

    def _validate_schedule_window(
        self,
        start_time: time,
        end_time: time,
        slot_duration: int,
    ) -> None:
        if start_time >= end_time:
            raise InvalidScheduleError
        total_minutes = (end_time.hour * 60 + end_time.minute) - (
            start_time.hour * 60 + start_time.minute
        )
        if slot_duration > total_minutes or total_minutes % slot_duration != 0:
            raise InvalidScheduleError
