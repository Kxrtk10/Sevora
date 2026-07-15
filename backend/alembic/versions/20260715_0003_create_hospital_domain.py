"""create hospital domain

Revision ID: 20260715_0003
Revises: 20260715_0002
Create Date: 2026-07-15
"""

from collections.abc import Sequence
from uuid import uuid4

import sqlalchemy as sa
from alembic import op

revision: str = "20260715_0003"
down_revision: str | None = "20260715_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SUNRISE_HOSPITAL_ID = "11111111-1111-4111-8111-111111111111"
GENERAL_MEDICINE_ID = "22222222-2222-4222-8222-222222222221"
ORTHOPEDICS_ID = "22222222-2222-4222-8222-222222222222"
DERMATOLOGY_ID = "22222222-2222-4222-8222-222222222223"
PEDIATRICS_ID = "22222222-2222-4222-8222-222222222224"
ARJUN_ID = "33333333-3333-4333-8333-333333333331"
PRIYA_ID = "33333333-3333-4333-8333-333333333332"
NEHA_ID = "33333333-3333-4333-8333-333333333333"
VIKRAM_ID = "33333333-3333-4333-8333-333333333334"


def upgrade() -> None:
    op.create_table(
        "hospitals",
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("address", sa.String(length=500), nullable=False),
        sa.Column("city", sa.String(length=120), nullable=False),
        sa.Column("state", sa.String(length=120), nullable=False),
        sa.Column("country", sa.String(length=120), nullable=False),
        sa.Column("postal_code", sa.String(length=30), nullable=False),
        sa.Column("phone", sa.String(length=40), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("website", sa.String(length=500), nullable=True),
        sa.Column("timezone", sa.String(length=80), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_hospitals_name"), "hospitals", ["name"], unique=True)

    op.add_column("departments", sa.Column("hospital_id", sa.Uuid(), nullable=True))
    op.add_column(
        "departments",
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
    )
    op.create_foreign_key(
        "fk_departments_hospital_id_hospitals",
        "departments",
        "hospitals",
        ["hospital_id"],
        ["id"],
    )
    op.drop_constraint("departments_name_key", "departments", type_="unique")
    op.create_unique_constraint(
        "uq_department_hospital_name",
        "departments",
        ["hospital_id", "name"],
    )

    op.add_column("doctors", sa.Column("hospital_id", sa.Uuid(), nullable=True))
    op.add_column("doctors", sa.Column("full_name", sa.String(length=200), nullable=True))
    op.add_column("doctors", sa.Column("specialization", sa.String(length=160), nullable=True))
    op.add_column("doctors", sa.Column("qualification", sa.String(length=200), nullable=True))
    op.add_column("doctors", sa.Column("years_of_experience", sa.Integer(), nullable=True))
    op.add_column("doctors", sa.Column("biography", sa.Text(), nullable=True))
    op.add_column(
        "doctors",
        sa.Column("consultation_duration_minutes", sa.Integer(), nullable=True),
    )
    op.add_column("doctors", sa.Column("consultation_fee", sa.Numeric(10, 2), nullable=True))
    op.add_column(
        "doctors",
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
    )
    op.create_foreign_key(
        "fk_doctors_hospital_id_hospitals",
        "doctors",
        "hospitals",
        ["hospital_id"],
        ["id"],
    )
    op.alter_column("doctors", "user_id", nullable=True)
    op.alter_column("doctors", "department_id", nullable=False)

    op.create_table(
        "doctor_schedules",
        sa.Column("doctor_id", sa.Uuid(), nullable=False),
        sa.Column("weekday", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("slot_duration", sa.Integer(), nullable=False),
        sa.Column("maximum_patients", sa.Integer(), nullable=False),
        sa.Column("is_available", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["doctor_id"], ["doctors.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "doctor_id",
            "weekday",
            "start_time",
            "end_time",
            name="uq_doctor_schedule_window",
        ),
    )

    _seed_demo_data()


def downgrade() -> None:
    op.drop_table("doctor_schedules")
    op.drop_constraint("fk_doctors_hospital_id_hospitals", "doctors", type_="foreignkey")
    op.drop_column("doctors", "is_active")
    op.drop_column("doctors", "consultation_fee")
    op.drop_column("doctors", "consultation_duration_minutes")
    op.drop_column("doctors", "biography")
    op.drop_column("doctors", "years_of_experience")
    op.drop_column("doctors", "qualification")
    op.drop_column("doctors", "specialization")
    op.drop_column("doctors", "full_name")
    op.drop_column("doctors", "hospital_id")

    op.drop_constraint("uq_department_hospital_name", "departments", type_="unique")
    op.drop_constraint("fk_departments_hospital_id_hospitals", "departments", type_="foreignkey")
    op.create_unique_constraint("departments_name_key", "departments", ["name"])
    op.drop_column("departments", "is_active")
    op.drop_column("departments", "hospital_id")

    op.drop_index(op.f("ix_hospitals_name"), table_name="hospitals")
    op.drop_table("hospitals")


def _seed_demo_data() -> None:
    connection = op.get_bind()
    now = sa.func.now()
    hospitals = sa.table(
        "hospitals",
        sa.column("id"),
        sa.column("name"),
        sa.column("address"),
        sa.column("city"),
        sa.column("state"),
        sa.column("country"),
        sa.column("postal_code"),
        sa.column("phone"),
        sa.column("email"),
        sa.column("website"),
        sa.column("timezone"),
        sa.column("is_active"),
        sa.column("created_at"),
        sa.column("updated_at"),
    )
    departments = sa.table(
        "departments",
        sa.column("id"),
        sa.column("hospital_id"),
        sa.column("name"),
        sa.column("description"),
        sa.column("status"),
        sa.column("is_active"),
        sa.column("created_at"),
        sa.column("updated_at"),
    )
    doctors = sa.table(
        "doctors",
        sa.column("id"),
        sa.column("hospital_id"),
        sa.column("department_id"),
        sa.column("full_name"),
        sa.column("specialization"),
        sa.column("qualification"),
        sa.column("years_of_experience"),
        sa.column("biography"),
        sa.column("consultation_duration_minutes"),
        sa.column("consultation_fee"),
        sa.column("is_active"),
        sa.column("created_at"),
        sa.column("updated_at"),
    )
    schedules = sa.table(
        "doctor_schedules",
        sa.column("id"),
        sa.column("doctor_id"),
        sa.column("weekday"),
        sa.column("start_time"),
        sa.column("end_time"),
        sa.column("slot_duration"),
        sa.column("maximum_patients"),
        sa.column("is_available"),
        sa.column("created_at"),
        sa.column("updated_at"),
    )

    connection.execute(
        hospitals.insert().values(
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
            created_at=now,
            updated_at=now,
        )
    )
    connection.execute(
        departments.insert(),
        [
            _department(GENERAL_MEDICINE_ID, "General Medicine", "Primary care and diagnostics"),
            _department(ORTHOPEDICS_ID, "Orthopedics", "Bone, joint and mobility care"),
            _department(DERMATOLOGY_ID, "Dermatology", "Skin, hair and cosmetic dermatology"),
            _department(PEDIATRICS_ID, "Pediatrics", "Child and adolescent healthcare"),
        ],
    )
    connection.execute(
        doctors.insert(),
        [
            _doctor(ARJUN_ID, GENERAL_MEDICINE_ID, "Dr. Arjun Mehta", "General Medicine", 14, 800),
            _doctor(PRIYA_ID, ORTHOPEDICS_ID, "Dr. Priya Rao", "Orthopedics", 11, 1200),
            _doctor(NEHA_ID, DERMATOLOGY_ID, "Dr. Neha Sharma", "Dermatology", 9, 1000),
            _doctor(VIKRAM_ID, PEDIATRICS_ID, "Dr. Vikram Gupta", "Pediatrics", 16, 900),
        ],
    )
    connection.execute(
        schedules.insert(),
        [_schedule(ARJUN_ID, weekday, "09:00:00", "13:00:00", 30, 8) for weekday in range(0, 5)]
        + [_schedule(PRIYA_ID, weekday, "10:00:00", "15:00:00", 30, 10) for weekday in range(0, 5)]
        + [_schedule(NEHA_ID, weekday, "11:00:00", "16:00:00", 30, 10) for weekday in range(1, 6)]
        + [
            _schedule(VIKRAM_ID, weekday, "09:30:00", "14:30:00", 30, 10) for weekday in range(0, 5)
        ],
    )


def _department(department_id: str, name: str, description: str) -> dict[str, object]:
    return {
        "id": department_id,
        "hospital_id": SUNRISE_HOSPITAL_ID,
        "name": name,
        "description": description,
        "status": "active",
        "is_active": True,
        "created_at": sa.func.now(),
        "updated_at": sa.func.now(),
    }


def _doctor(
    doctor_id: str,
    department_id: str,
    full_name: str,
    specialization: str,
    years: int,
    fee: int,
) -> dict[str, object]:
    return {
        "id": doctor_id,
        "hospital_id": SUNRISE_HOSPITAL_ID,
        "department_id": department_id,
        "full_name": full_name,
        "specialization": specialization,
        "qualification": "MBBS, MD",
        "years_of_experience": years,
        "biography": f"{full_name} provides evidence-led {specialization.lower()} care.",
        "consultation_duration_minutes": 30,
        "consultation_fee": fee,
        "is_active": True,
        "created_at": sa.func.now(),
        "updated_at": sa.func.now(),
    }


def _schedule(
    doctor_id: str,
    weekday: int,
    start_time: str,
    end_time: str,
    slot_duration: int,
    maximum_patients: int,
) -> dict[str, object]:
    return {
        "doctor_id": doctor_id,
        "id": str(uuid4()),
        "weekday": weekday,
        "start_time": start_time,
        "end_time": end_time,
        "slot_duration": slot_duration,
        "maximum_patients": maximum_patients,
        "is_available": True,
        "created_at": sa.func.now(),
        "updated_at": sa.func.now(),
    }
