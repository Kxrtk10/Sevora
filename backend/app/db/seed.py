from datetime import time
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.department import Department
from app.models.doctor import Doctor
from app.models.doctor_schedule import DoctorSchedule
from app.models.hospital import Hospital

SUNRISE_HOSPITAL_ID = UUID("11111111-1111-4111-8111-111111111111")


async def seed_demo_hospital(session: AsyncSession) -> Hospital:
    existing = await session.execute(
        select(Hospital).where(Hospital.name == "Sunrise Multispeciality Clinic")
    )
    hospital = existing.scalar_one_or_none()
    if hospital is not None:
        return hospital

    hospital = Hospital(
        id=SUNRISE_HOSPITAL_ID,
        name="Sunrise Multispeciality Clinic",
        address="14 Wellness Avenue, Indiranagar",
        city="Bengaluru",
        state="Karnataka",
        country="India",
        postal_code="560038",
        phone="+91-80-4567-2200",
        email="operations@sunriseclinic.example",
        website="https://sunriseclinic.example",
        timezone="Asia/Kolkata",
        is_active=True,
    )
    departments = [
        Department(
            hospital=hospital,
            name="General Medicine",
            description="Primary care and diagnostics",
            is_active=True,
        ),
        Department(
            hospital=hospital,
            name="Orthopedics",
            description="Bone, joint and mobility care",
            is_active=True,
        ),
        Department(
            hospital=hospital,
            name="Dermatology",
            description="Skin, hair and cosmetic dermatology",
            is_active=True,
        ),
        Department(
            hospital=hospital,
            name="Pediatrics",
            description="Child and adolescent healthcare",
            is_active=True,
        ),
    ]
    doctors = [
        _doctor(hospital, departments[0], "Dr. Arjun Mehta", "General Medicine", 14, 800),
        _doctor(hospital, departments[1], "Dr. Priya Rao", "Orthopedics", 11, 1200),
        _doctor(hospital, departments[2], "Dr. Neha Sharma", "Dermatology", 9, 1000),
        _doctor(hospital, departments[3], "Dr. Vikram Gupta", "Pediatrics", 16, 900),
    ]

    for index, doctor in enumerate(doctors):
        start_hour = [9, 10, 11, 9][index]
        for weekday in range(0, 5):
            doctor.schedules.append(
                DoctorSchedule(
                    weekday=weekday,
                    start_time=time(start_hour, 0),
                    end_time=time(start_hour + 4, 0),
                    slot_duration=30,
                    maximum_patients=8,
                    is_available=True,
                )
            )

    session.add(hospital)
    await session.commit()
    await session.refresh(hospital)
    return hospital


def _doctor(
    hospital: Hospital,
    department: Department,
    full_name: str,
    specialization: str,
    years: int,
    fee: int,
) -> Doctor:
    return Doctor(
        hospital=hospital,
        department=department,
        full_name=full_name,
        specialization=specialization,
        qualification="MBBS, MD",
        years_of_experience=years,
        biography=f"{full_name} provides evidence-led {specialization.lower()} care.",
        consultation_duration_minutes=30,
        consultation_fee=Decimal(fee),
        is_active=True,
    )
