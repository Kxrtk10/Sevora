import asyncio
from collections.abc import Generator
from contextlib import contextmanager
from decimal import Decimal
from typing import Any

from app.db.base import Base
from app.db.seed import seed_demo_hospital
from app.db.session import get_db_session
from app.main import app
from app.models.department import Department
from app.models.doctor import Doctor
from app.models.doctor_schedule import DoctorSchedule
from app.models.hospital import Hospital
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


@contextmanager
def hospital_client(
    tmp_path,
) -> Generator[tuple[TestClient, async_sessionmaker[AsyncSession]], None, None]:
    database_path = tmp_path / "hospital-domain-test.db"
    engine = create_async_engine(f"sqlite+aiosqlite:///{database_path}")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def create_schema() -> None:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def override_db_session():
        async with session_factory() as session:
            yield session

    asyncio.run(create_schema())
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        with TestClient(app) as client:
            yield client, session_factory
    finally:
        app.dependency_overrides.clear()
        asyncio.run(engine.dispose())


def hospital_payload(**overrides: Any) -> dict[str, Any]:
    payload = {
        "name": "Northstar Clinic",
        "address": "12 Care Street",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "postal_code": "400001",
        "phone": "+91-22-5555-0101",
        "email": "ops@northstar.example",
        "website": "https://northstar.example",
        "timezone": "Asia/Kolkata",
        "is_active": True,
    }
    payload.update(overrides)
    return payload


def department_payload(hospital_id: str, **overrides: Any) -> dict[str, Any]:
    payload = {
        "hospital_id": hospital_id,
        "name": "General Medicine",
        "description": "Primary care",
        "is_active": True,
    }
    payload.update(overrides)
    return payload


def doctor_payload(hospital_id: str, department_id: str, **overrides: Any) -> dict[str, Any]:
    payload = {
        "hospital_id": hospital_id,
        "department_id": department_id,
        "full_name": "Dr. Asha Menon",
        "specialization": "General Medicine",
        "qualification": "MBBS, MD",
        "years_of_experience": 13,
        "biography": "Experienced clinician.",
        "consultation_duration_minutes": 30,
        "consultation_fee": "900.00",
        "is_active": True,
    }
    payload.update(overrides)
    return payload


def schedule_payload(doctor_id: str, **overrides: Any) -> dict[str, Any]:
    payload = {
        "doctor_id": doctor_id,
        "weekday": 1,
        "start_time": "09:00:00",
        "end_time": "13:00:00",
        "slot_duration": 30,
        "maximum_patients": 8,
        "is_available": True,
    }
    payload.update(overrides)
    return payload


def create_hospital_tree(
    client: TestClient,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    hospital_response = client.post("/api/v1/hospitals", json=hospital_payload())
    assert hospital_response.status_code == 201, hospital_response.json()
    hospital = hospital_response.json()

    department_response = client.post(
        "/api/v1/departments",
        json=department_payload(hospital["id"]),
    )
    assert department_response.status_code == 201, department_response.json()
    department = department_response.json()

    doctor_response = client.post(
        "/api/v1/doctors",
        json=doctor_payload(hospital["id"], department["id"]),
    )
    assert doctor_response.status_code == 201, doctor_response.json()
    doctor = doctor_response.json()

    return hospital, department, doctor


def test_hospital_department_doctor_and_schedule_crud(tmp_path) -> None:
    with hospital_client(tmp_path) as (client, _):
        hospital, department, doctor = create_hospital_tree(client)

        hospital_update = client.put(
            f"/api/v1/hospitals/{hospital['id']}",
            json={"phone": "+91-22-5555-0202"},
        )
        assert hospital_update.status_code == 200
        assert hospital_update.json()["phone"] == "+91-22-5555-0202"

        department_update = client.put(
            f"/api/v1/departments/{department['id']}",
            json={"description": "Family and internal medicine"},
        )
        assert department_update.status_code == 200
        assert department_update.json()["description"] == "Family and internal medicine"

        doctor_update = client.put(
            f"/api/v1/doctors/{doctor['id']}",
            json={"consultation_fee": "950.00"},
        )
        assert doctor_update.status_code == 200
        assert Decimal(doctor_update.json()["consultation_fee"]) == Decimal("950.00")

        schedule_response = client.post(
            "/api/v1/doctor-schedules",
            json=schedule_payload(doctor["id"]),
        )
        assert schedule_response.status_code == 201
        schedule = schedule_response.json()

        list_response = client.get(f"/api/v1/doctor-schedules?doctor_id={doctor['id']}")
        assert list_response.status_code == 200
        assert len(list_response.json()) == 1

        schedule_update = client.put(
            f"/api/v1/doctor-schedules/{schedule['id']}",
            json={"maximum_patients": 10},
        )
        assert schedule_update.status_code == 200
        assert schedule_update.json()["maximum_patients"] == 10

        delete_schedule = client.delete(f"/api/v1/doctor-schedules/{schedule['id']}")
        assert delete_schedule.status_code == 204


def test_relationship_filters_and_delete_protection(tmp_path) -> None:
    with hospital_client(tmp_path) as (client, _):
        hospital, department, doctor = create_hospital_tree(client)

        hospitals = client.get("/api/v1/hospitals")
        departments = client.get(f"/api/v1/departments?hospital_id={hospital['id']}")
        doctors = client.get(f"/api/v1/doctors?department_id={department['id']}")
        assert hospitals.status_code == 200
        assert departments.status_code == 200
        assert doctors.status_code == 200
        assert departments.json()[0]["hospital_id"] == hospital["id"]
        assert doctors.json()[0]["id"] == doctor["id"]

        blocked_department_delete = client.delete(f"/api/v1/departments/{department['id']}")
        blocked_hospital_delete = client.delete(f"/api/v1/hospitals/{hospital['id']}")
        assert blocked_department_delete.status_code == 409
        assert blocked_hospital_delete.status_code == 409

        delete_doctor = client.delete(f"/api/v1/doctors/{doctor['id']}")
        delete_department = client.delete(f"/api/v1/departments/{department['id']}")
        delete_hospital = client.delete(f"/api/v1/hospitals/{hospital['id']}")
        assert delete_doctor.status_code == 204
        assert delete_department.status_code == 204
        assert delete_hospital.status_code == 204


def test_duplicate_departments_are_rejected_within_same_hospital(tmp_path) -> None:
    with hospital_client(tmp_path) as (client, _):
        hospital_response = client.post("/api/v1/hospitals", json=hospital_payload())
        other_response = client.post(
            "/api/v1/hospitals",
            json=hospital_payload(name="Southstar Clinic", email="south@example.com"),
        )
        assert hospital_response.status_code == 201
        assert other_response.status_code == 201

        first = client.post(
            "/api/v1/departments",
            json=department_payload(hospital_response.json()["id"]),
        )
        duplicate = client.post(
            "/api/v1/departments",
            json=department_payload(hospital_response.json()["id"]),
        )
        same_name_other_hospital = client.post(
            "/api/v1/departments",
            json=department_payload(other_response.json()["id"]),
        )
        assert first.status_code == 201
        assert duplicate.status_code == 409
        assert same_name_other_hospital.status_code == 201


def test_doctor_department_must_belong_to_hospital(tmp_path) -> None:
    with hospital_client(tmp_path) as (client, _):
        hospital = client.post("/api/v1/hospitals", json=hospital_payload()).json()
        other = client.post(
            "/api/v1/hospitals",
            json=hospital_payload(name="East Clinic", email="east@example.com"),
        ).json()
        department = client.post(
            "/api/v1/departments",
            json=department_payload(other["id"]),
        ).json()

        response = client.post(
            "/api/v1/doctors",
            json=doctor_payload(hospital["id"], department["id"]),
        )
        assert response.status_code == 400


def test_schedule_validation_and_overlap_rules(tmp_path) -> None:
    with hospital_client(tmp_path) as (client, _):
        _, _, doctor = create_hospital_tree(client)

        invalid_hours = client.post(
            "/api/v1/doctor-schedules",
            json=schedule_payload(doctor["id"], start_time="13:00:00", end_time="09:00:00"),
        )
        invalid_slot = client.post(
            "/api/v1/doctor-schedules",
            json=schedule_payload(doctor["id"], slot_duration=45),
        )
        assert invalid_hours.status_code == 400
        assert invalid_slot.status_code == 400

        created = client.post("/api/v1/doctor-schedules", json=schedule_payload(doctor["id"]))
        overlap = client.post(
            "/api/v1/doctor-schedules",
            json=schedule_payload(
                doctor["id"],
                start_time="12:00:00",
                end_time="15:00:00",
            ),
        )
        assert created.status_code == 201
        assert overlap.status_code == 409


def test_inactive_doctors_cannot_receive_future_schedules(tmp_path) -> None:
    with hospital_client(tmp_path) as (client, _):
        hospital, department, doctor = create_hospital_tree(client)
        inactive = client.put(f"/api/v1/doctors/{doctor['id']}", json={"is_active": False})
        assert inactive.status_code == 200

        response = client.post(
            "/api/v1/doctor-schedules",
            json=schedule_payload(doctor["id"]),
        )
        assert response.status_code == 400

        active_replacement = client.post(
            "/api/v1/doctors",
            json=doctor_payload(
                hospital["id"],
                department["id"],
                full_name="Dr. Replacement",
                is_active=True,
            ),
        )
        assert active_replacement.status_code == 201


def test_seed_demo_hospital_creates_expected_domain_graph(tmp_path) -> None:
    with hospital_client(tmp_path) as (_, session_factory):

        async def seed_and_count() -> tuple[Hospital, int, int, int]:
            async with session_factory() as session:
                hospital = await seed_demo_hospital(session)
                departments = await session.execute(select(Department))
                doctors = await session.execute(select(Doctor))
                schedules = await session.execute(select(DoctorSchedule))
                return (
                    hospital,
                    len(list(departments.scalars().all())),
                    len(list(doctors.scalars().all())),
                    len(list(schedules.scalars().all())),
                )

        hospital, department_count, doctor_count, schedule_count = asyncio.run(seed_and_count())
        assert hospital.name == "Sunrise Multispeciality Clinic"
        assert department_count == 4
        assert doctor_count == 4
        assert schedule_count == 20
