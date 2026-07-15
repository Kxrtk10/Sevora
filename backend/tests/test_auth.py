import asyncio

from app.db.base import Base
from app.db.session import get_db_session
from app.main import app
from app.models.user import User
from app.utils.jwt import TokenType, decode_token
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


def test_authentication_flow(tmp_path) -> None:
    database_path = tmp_path / "auth-test.db"
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
            registration_payload = {
                "email": "patient@example.com",
                "password": "secure-password",
                "full_name": "Patient One",
                "role": "patient",
            }

            register_response = client.post("/api/v1/auth/register", json=registration_payload)
            assert register_response.status_code == 201

            register_body = register_response.json()
            assert register_body["token_type"] == "bearer"
            assert register_body["access_token"]
            assert register_body["refresh_token"]
            assert register_body["expires_in"] == 900
            assert register_body["user"]["email"] == "patient@example.com"
            assert register_body["user"]["role"] == "patient"

            access_payload = decode_token(register_body["access_token"], TokenType.ACCESS)
            refresh_payload = decode_token(register_body["refresh_token"], TokenType.REFRESH)
            assert access_payload["sub"] == register_body["user"]["id"]
            assert refresh_payload["sub"] == register_body["user"]["id"]

            duplicate_response = client.post("/api/v1/auth/register", json=registration_payload)
            assert duplicate_response.status_code == 409

            short_password_response = client.post(
                "/api/v1/auth/register",
                json={
                    "email": "short@example.com",
                    "password": "short",
                    "full_name": "Short Password",
                    "role": "patient",
                },
            )
            assert short_password_response.status_code == 422

            missing_fields_response = client.post("/api/v1/auth/register", json={})
            assert missing_fields_response.status_code == 422

            login_response = client.post(
                "/api/v1/auth/login",
                json={"email": "patient@example.com", "password": "secure-password"},
            )
            assert login_response.status_code == 200
            assert login_response.json()["access_token"]

            invalid_login_response = client.post(
                "/api/v1/auth/login",
                json={"email": "patient@example.com", "password": "wrong-password"},
            )
            assert invalid_login_response.status_code == 401

            refresh_response = client.post(
                "/api/v1/auth/refresh",
                json={"refresh_token": register_body["refresh_token"]},
            )
            assert refresh_response.status_code == 200
            refresh_body = refresh_response.json()
            assert refresh_body["access_token"]
            assert refresh_body["refresh_token"]
            decode_token(refresh_body["access_token"], TokenType.ACCESS)
            decode_token(refresh_body["refresh_token"], TokenType.REFRESH)
    finally:
        app.dependency_overrides.clear()
        asyncio.run(engine.dispose())


def test_password_is_hashed(tmp_path) -> None:
    database_path = tmp_path / "password-test.db"
    engine = create_async_engine(f"sqlite+aiosqlite:///{database_path}")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def create_schema() -> None:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def override_db_session():
        async with session_factory() as session:
            yield session

    async def get_user() -> User:
        async with session_factory() as session:
            result = await session.execute(select(User).where(User.email == "doctor@example.com"))
            user = result.scalar_one()
            return user

    asyncio.run(create_schema())
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/auth/register",
                json={
                    "email": "doctor@example.com",
                    "password": "another-secure-password",
                    "full_name": "Doctor One",
                    "role": "doctor",
                },
            )
            assert response.status_code == 201

        user = asyncio.run(get_user())
        assert user.hashed_password != "another-secure-password"
        assert user.hashed_password.startswith("$2")
    finally:
        app.dependency_overrides.clear()
        asyncio.run(engine.dispose())
