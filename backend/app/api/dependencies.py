from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.repositories.appointment import AppointmentRepository
from app.repositories.auth import AuthRepository
from app.repositories.hospital_domain import HospitalDomainRepository
from app.services.ai_concierge import AIConciergeService
from app.services.ai_provider import MockAIProvider
from app.services.appointments import AppointmentService
from app.services.authentication import AuthService
from app.services.hospital_domain import HospitalDomainService
from app.services.intent_router import RuleBasedIntentRouter


async def get_auth_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> AsyncGenerator[AuthRepository, None]:
    yield AuthRepository(session)


async def get_auth_service(
    repository: Annotated[AuthRepository, Depends(get_auth_repository)],
) -> AsyncGenerator[AuthService, None]:
    yield AuthService(repository)


async def get_appointment_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> AsyncGenerator[AppointmentRepository, None]:
    yield AppointmentRepository(session)


async def get_appointment_service(
    repository: Annotated[AppointmentRepository, Depends(get_appointment_repository)],
) -> AsyncGenerator[AppointmentService, None]:
    yield AppointmentService(repository)


async def get_hospital_domain_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> AsyncGenerator[HospitalDomainRepository, None]:
    yield HospitalDomainRepository(session)


async def get_hospital_domain_service(
    repository: Annotated[HospitalDomainRepository, Depends(get_hospital_domain_repository)],
) -> AsyncGenerator[HospitalDomainService, None]:
    yield HospitalDomainService(repository)


async def get_ai_concierge_service(
    hospital_service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
    appointment_service: Annotated[AppointmentService, Depends(get_appointment_service)],
) -> AsyncGenerator[AIConciergeService, None]:
    yield AIConciergeService(
        hospital_service=hospital_service,
        appointment_service=appointment_service,
        intent_router=RuleBasedIntentRouter(),
        ai_provider=MockAIProvider(),
    )
