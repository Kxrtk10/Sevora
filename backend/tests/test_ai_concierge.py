import asyncio
from collections.abc import Generator
from contextlib import contextmanager

from app.db.base import Base
from app.db.seed import seed_demo_hospital
from app.db.session import get_db_session
from app.main import app
from app.services.intent_router import ConciergeIntent, RuleBasedIntentRouter
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


@contextmanager
def concierge_client(
    tmp_path,
) -> Generator[TestClient, None, None]:
    database_path = tmp_path / "concierge-test.db"
    engine = create_async_engine(f"sqlite+aiosqlite:///{database_path}")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def create_schema_and_seed() -> None:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        async with session_factory() as session:
            await seed_demo_hospital(session)

    async def override_db_session():
        async with session_factory() as session:
            yield session

    asyncio.run(create_schema_and_seed())
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        asyncio.run(engine.dispose())


def test_intent_router_maps_supported_intents() -> None:
    router = RuleBasedIntentRouter()
    assert router.route("I have knee pain") == ConciergeIntent.BOOK_APPOINTMENT
    assert router.route("I want a skin specialist") == ConciergeIntent.FIND_DOCTOR
    assert router.route("Browse departments") == ConciergeIntent.BROWSE_DEPARTMENTS
    assert router.route("I need to cancel my appointment") == ConciergeIntent.CANCEL_APPOINTMENT
    assert router.route("what medication should I take") == ConciergeIntent.MEDICAL_ADVICE
    assert router.route("blue umbrella") == ConciergeIntent.UNKNOWN


def test_knee_pain_recommends_orthopedics_doctors_and_slots(tmp_path) -> None:
    with concierge_client(tmp_path) as client:
        response = client.post("/api/v1/ai-concierge/message", json={"message": "I have knee pain"})
        assert response.status_code == 200
        body = response.json()
        assert body["intent"] == "book_appointment"
        assert body["departments"][0]["name"] == "Orthopedics"
        assert body["doctors"]
        assert body["slots"]


def test_skin_specialist_recommends_dermatology(tmp_path) -> None:
    with concierge_client(tmp_path) as client:
        response = client.post(
            "/api/v1/ai-concierge/message",
            json={"message": "I want a skin specialist"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["intent"] == "find_doctor"
        assert body["departments"][0]["name"] == "Dermatology"
        assert body["doctors"][0]["specialization"] == "Dermatology"


def test_browse_departments_and_hospital_information(tmp_path) -> None:
    with concierge_client(tmp_path) as client:
        departments = client.post(
            "/api/v1/ai-concierge/message",
            json={"message": "Browse departments"},
        )
        hospital = client.post(
            "/api/v1/ai-concierge/message",
            json={"message": "hospital information"},
        )
        assert departments.status_code == 200
        assert len(departments.json()["departments"]) == 4
        assert hospital.status_code == 200
        assert "Sunrise Multispeciality Clinic" in hospital.json()["message"]


def test_concierge_booking_and_cancellation_flow(tmp_path) -> None:
    with concierge_client(tmp_path) as client:
        guidance = client.post(
            "/api/v1/ai-concierge/message",
            json={"message": "I have knee pain"},
        ).json()
        doctor = guidance["doctors"][0]
        department = guidance["departments"][0]
        slot = guidance["slots"][0]

        booking = client.post(
            "/api/v1/ai-concierge/message",
            json={
                "message": "Book this appointment",
                "action": "book_appointment",
                "doctor_id": doctor["id"],
                "department_id": department["id"],
                "patient_name": "Maya Patel",
                "patient_email": "maya@example.com",
                "patient_phone": "+15555550123",
                "reason_for_visit": "Knee pain",
                "appointment_date": slot["appointment_date"],
                "appointment_start_time": slot["start_time"],
                "appointment_end_time": slot["end_time"],
            },
        )
        assert booking.status_code == 200
        appointment = booking.json()["appointment"]
        assert appointment["status"] == "pending"

        cancellation = client.post(
            "/api/v1/ai-concierge/message",
            json={
                "message": "I need to cancel my appointment",
                "appointment_id": appointment["id"],
            },
        )
        assert cancellation.status_code == 200
        assert cancellation.json()["appointment"]["status"] == "cancelled"


def test_concierge_refuses_medical_advice_and_handles_unknown_intents(tmp_path) -> None:
    with concierge_client(tmp_path) as client:
        medical = client.post(
            "/api/v1/ai-concierge/message",
            json={"message": "What medication should I take for my report?"},
        )
        unknown = client.post(
            "/api/v1/ai-concierge/message",
            json={"message": "blue umbrella"},
        )
        assert medical.status_code == 200
        assert medical.json()["intent"] == "medical_advice"
        assert "unable to provide medical advice" in medical.json()["message"]
        assert unknown.status_code == 200
        assert unknown.json()["intent"] == "unknown"
