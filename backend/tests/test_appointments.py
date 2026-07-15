import asyncio
from collections.abc import Generator
from contextlib import contextmanager
from datetime import UTC, date, datetime, time, timedelta
from typing import Any
from uuid import uuid4

from app.db.base import Base
from app.db.session import get_db_session
from app.main import app
from app.models.department import Department
from app.models.doctor import Doctor
from app.models.doctor_schedule import DoctorSchedule
from app.models.hospital import Hospital
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


@contextmanager
def appointment_client(tmp_path) -> Generator[TestClient, None, None]:
    database_path = tmp_path / "appointment-test.db"
    engine = create_async_engine(f"sqlite+aiosqlite:///{database_path}")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def create_schema() -> None:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def override_db_session():
        async with session_factory() as session:
            yield session

    asyncio.run(create_schema())
    asyncio.run(seed_reference_data(session_factory))
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        asyncio.run(engine.dispose())


async def seed_reference_data(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async with session_factory() as session:
        cardiology = Department(
            id=DEPARTMENT_ID,
            hospital_id=HOSPITAL_ID,
            name="Cardiology",
            description="Heart health",
            is_active=True,
        )
        hospital = Hospital(
            id=HOSPITAL_ID,
            name="Appointment Test Hospital",
            address="1 Test Way",
            city="Bengaluru",
            state="Karnataka",
            country="India",
            postal_code="560001",
            phone="+15555550111",
            email="hospital@example.com",
            website="https://hospital.example.com",
            timezone="Asia/Kolkata",
            is_active=True,
        )
        active_doctor = Doctor(
            id=DOCTOR_ID,
            hospital_id=HOSPITAL_ID,
            department_id=DEPARTMENT_ID,
            full_name="Active Doctor",
            specialization="Cardiology",
            qualification="MBBS, MD",
            years_of_experience=12,
            biography="Cardiology consultant.",
            consultation_duration_minutes=30,
            consultation_fee=1000,
            is_active=True,
        )
        inactive_doctor = Doctor(
            id=INACTIVE_DOCTOR_ID,
            hospital_id=HOSPITAL_ID,
            department_id=DEPARTMENT_ID,
            full_name="Inactive Doctor",
            specialization="Cardiology",
            qualification="MBBS, MD",
            years_of_experience=8,
            biography="Inactive consultant.",
            consultation_duration_minutes=30,
            consultation_fee=1000,
            is_active=False,
        )
        schedule = DoctorSchedule(
            doctor_id=DOCTOR_ID,
            weekday=(datetime.now(UTC).date() + timedelta(days=7)).weekday(),
            start_time=time(9, 0),
            end_time=time(17, 0),
            slot_duration=30,
            maximum_patients=16,
            is_available=True,
        )
        session.add_all([hospital, cardiology, active_doctor, inactive_doctor, schedule])
        await session.commit()


HOSPITAL_ID = uuid4()
DEPARTMENT_ID = uuid4()
DOCTOR_ID = uuid4()
INACTIVE_DOCTOR_ID = uuid4()


def future_date() -> str:
    return (datetime.now(UTC).date() + timedelta(days=7)).isoformat()


def appointment_payload(**overrides: Any) -> dict[str, Any]:
    payload = {
        "patient_name": "Maya Patel",
        "patient_email": "maya@example.com",
        "patient_phone": "+15555550123",
        "reason_for_visit": "Chest discomfort follow-up",
        "doctor_id": str(DOCTOR_ID),
        "department_id": str(DEPARTMENT_ID),
        "appointment_date": future_date(),
        "appointment_start_time": "10:00:00",
        "appointment_end_time": "10:30:00",
        "notes": "Prefers morning calls.",
    }
    payload.update(overrides)
    return payload


def create_appointment(client: TestClient, **overrides: Any) -> dict[str, Any]:
    response = client.post("/api/v1/appointments", json=appointment_payload(**overrides))
    assert response.status_code == 201, response.json()
    return response.json()


def test_create_get_list_update_and_cancel_appointment(tmp_path) -> None:
    with appointment_client(tmp_path) as client:
        created = create_appointment(client)
        assert created["patient_name"] == "Maya Patel"
        assert created["status"] == "pending"
        assert created["doctor_id"] == str(DOCTOR_ID)
        assert created["department_id"] == str(DEPARTMENT_ID)

        get_response = client.get(f"/api/v1/appointments/{created['id']}")
        assert get_response.status_code == 200
        assert get_response.json()["id"] == created["id"]

        list_response = client.get("/api/v1/appointments")
        assert list_response.status_code == 200
        assert len(list_response.json()) == 1

        update_response = client.put(
            f"/api/v1/appointments/{created['id']}",
            json={
                "patient_phone": "+15555550999",
                "appointment_start_time": "11:00:00",
                "appointment_end_time": "11:45:00",
            },
        )
        assert update_response.status_code == 200
        assert update_response.json()["patient_phone"] == "+15555550999"
        assert update_response.json()["appointment_start_time"] == "11:00:00"

        cancel_response = client.delete(f"/api/v1/appointments/{created['id']}")
        assert cancel_response.status_code == 200
        assert cancel_response.json()["status"] == "cancelled"


def test_status_changes_follow_valid_transitions(tmp_path) -> None:
    with appointment_client(tmp_path) as client:
        created = create_appointment(client)

        confirm_response = client.patch(
            f"/api/v1/appointments/{created['id']}/status",
            json={"status": "confirmed"},
        )
        assert confirm_response.status_code == 200
        assert confirm_response.json()["status"] == "confirmed"

        check_in_response = client.patch(
            f"/api/v1/appointments/{created['id']}/status",
            json={"status": "checked_in"},
        )
        assert check_in_response.status_code == 200
        assert check_in_response.json()["status"] == "checked_in"

        complete_response = client.patch(
            f"/api/v1/appointments/{created['id']}/status",
            json={"status": "completed"},
        )
        assert complete_response.status_code == 200
        assert complete_response.json()["status"] == "completed"

        reopen_response = client.patch(
            f"/api/v1/appointments/{created['id']}/status",
            json={"status": "confirmed"},
        )
        assert reopen_response.status_code == 409


def test_double_booking_is_rejected(tmp_path) -> None:
    with appointment_client(tmp_path) as client:
        create_appointment(client)

        overlapping_response = client.post(
            "/api/v1/appointments",
            json=appointment_payload(
                patient_email="second@example.com",
                appointment_start_time="10:15:00",
                appointment_end_time="10:45:00",
            ),
        )
        assert overlapping_response.status_code == 409
        assert "already has an appointment" in overlapping_response.json()["detail"]


def test_cancelled_appointment_releases_slot(tmp_path) -> None:
    with appointment_client(tmp_path) as client:
        created = create_appointment(client)
        cancel_response = client.delete(f"/api/v1/appointments/{created['id']}")
        assert cancel_response.status_code == 200

        replacement_response = client.post(
            "/api/v1/appointments",
            json=appointment_payload(patient_email="replacement@example.com"),
        )
        assert replacement_response.status_code == 201


def test_invalid_doctor_and_inactive_doctor_are_rejected(tmp_path) -> None:
    with appointment_client(tmp_path) as client:
        invalid_response = client.post(
            "/api/v1/appointments",
            json=appointment_payload(doctor_id=str(uuid4())),
        )
        assert invalid_response.status_code == 404

        inactive_response = client.post(
            "/api/v1/appointments",
            json=appointment_payload(doctor_id=str(INACTIVE_DOCTOR_ID)),
        )
        assert inactive_response.status_code == 400
        assert "inactive doctors" in inactive_response.json()["detail"]


def test_invalid_schedule_and_dates_are_rejected(tmp_path) -> None:
    with appointment_client(tmp_path) as client:
        outside_schedule_response = client.post(
            "/api/v1/appointments",
            json=appointment_payload(
                appointment_start_time="08:00:00",
                appointment_end_time="08:30:00",
            ),
        )
        assert outside_schedule_response.status_code == 400

        invalid_duration_response = client.post(
            "/api/v1/appointments",
            json=appointment_payload(
                appointment_start_time="10:00:00",
                appointment_end_time="10:05:00",
            ),
        )
        assert invalid_duration_response.status_code == 400

        past_response = client.post(
            "/api/v1/appointments",
            json=appointment_payload(
                appointment_date=(date.today() - timedelta(days=1)).isoformat()
            ),
        )
        assert past_response.status_code == 400


def test_required_patient_information_is_validated(tmp_path) -> None:
    with appointment_client(tmp_path) as client:
        missing_name_response = client.post(
            "/api/v1/appointments",
            json=appointment_payload(patient_name=""),
        )
        assert missing_name_response.status_code == 422

        invalid_email_response = client.post(
            "/api/v1/appointments",
            json=appointment_payload(patient_email="not-an-email"),
        )
        assert invalid_email_response.status_code == 422
