from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.department import Department
from app.models.doctor import Doctor
from app.models.doctor_schedule import DoctorSchedule
from app.models.hospital import Hospital


class HospitalDomainRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, entity):
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def update(self, entity):
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def delete(self, entity) -> None:
        await self.session.delete(entity)
        await self.session.commit()

    async def get_hospital(self, hospital_id: UUID) -> Hospital | None:
        result = await self.session.execute(select(Hospital).where(Hospital.id == hospital_id))
        return result.scalar_one_or_none()

    async def get_hospital_by_name(self, name: str) -> Hospital | None:
        result = await self.session.execute(
            select(Hospital).where(func.lower(Hospital.name) == name.lower())
        )
        return result.scalar_one_or_none()

    async def list_hospitals(self, limit: int, offset: int) -> list[Hospital]:
        result = await self.session.execute(
            select(Hospital).order_by(Hospital.name).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_department(self, department_id: UUID) -> Department | None:
        result = await self.session.execute(
            select(Department).where(Department.id == department_id)
        )
        return result.scalar_one_or_none()

    async def get_department_by_hospital_and_name(
        self,
        *,
        hospital_id: UUID,
        name: str,
        exclude_department_id: UUID | None = None,
    ) -> Department | None:
        query = select(Department).where(
            Department.hospital_id == hospital_id,
            func.lower(Department.name) == name.lower(),
        )
        if exclude_department_id is not None:
            query = query.where(Department.id != exclude_department_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def list_departments(
        self,
        *,
        hospital_id: UUID | None,
        limit: int,
        offset: int,
    ) -> list[Department]:
        query: Select[tuple[Department]] = select(Department).order_by(Department.name)
        if hospital_id is not None:
            query = query.where(Department.hospital_id == hospital_id)
        result = await self.session.execute(query.limit(limit).offset(offset))
        return list(result.scalars().all())

    async def get_doctor(self, doctor_id: UUID) -> Doctor | None:
        result = await self.session.execute(select(Doctor).where(Doctor.id == doctor_id))
        return result.scalar_one_or_none()

    async def list_doctors(
        self,
        *,
        hospital_id: UUID | None,
        department_id: UUID | None,
        limit: int,
        offset: int,
    ) -> list[Doctor]:
        query: Select[tuple[Doctor]] = select(Doctor).order_by(Doctor.full_name)
        if hospital_id is not None:
            query = query.where(Doctor.hospital_id == hospital_id)
        if department_id is not None:
            query = query.where(Doctor.department_id == department_id)
        result = await self.session.execute(query.limit(limit).offset(offset))
        return list(result.scalars().all())

    async def get_schedule(self, schedule_id: UUID) -> DoctorSchedule | None:
        result = await self.session.execute(
            select(DoctorSchedule).where(DoctorSchedule.id == schedule_id)
        )
        return result.scalar_one_or_none()

    async def list_schedules(
        self,
        *,
        doctor_id: UUID | None,
        limit: int,
        offset: int,
    ) -> list[DoctorSchedule]:
        query: Select[tuple[DoctorSchedule]] = select(DoctorSchedule).order_by(
            DoctorSchedule.weekday,
            DoctorSchedule.start_time,
        )
        if doctor_id is not None:
            query = query.where(DoctorSchedule.doctor_id == doctor_id)
        result = await self.session.execute(query.limit(limit).offset(offset))
        return list(result.scalars().all())

    async def has_departments_or_doctors(self, hospital_id: UUID) -> bool:
        departments = await self.session.execute(
            select(Department.id).where(Department.hospital_id == hospital_id).limit(1)
        )
        if departments.scalar_one_or_none() is not None:
            return True
        doctors = await self.session.execute(
            select(Doctor.id).where(Doctor.hospital_id == hospital_id).limit(1)
        )
        return doctors.scalar_one_or_none() is not None

    async def has_doctors(self, department_id: UUID) -> bool:
        result = await self.session.execute(
            select(Doctor.id).where(Doctor.department_id == department_id).limit(1)
        )
        return result.scalar_one_or_none() is not None

    async def has_overlapping_schedule(
        self,
        *,
        doctor_id: UUID,
        weekday: int,
        start_time,
        end_time,
        exclude_schedule_id: UUID | None = None,
    ) -> bool:
        query = select(DoctorSchedule).where(
            DoctorSchedule.doctor_id == doctor_id,
            DoctorSchedule.weekday == weekday,
            DoctorSchedule.start_time < end_time,
            DoctorSchedule.end_time > start_time,
        )
        if exclude_schedule_id is not None:
            query = query.where(DoctorSchedule.id != exclude_schedule_id)
        result = await self.session.execute(query.limit(1))
        return result.scalar_one_or_none() is not None
