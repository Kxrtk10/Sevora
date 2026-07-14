from dataclasses import dataclass
from enum import StrEnum


class Role(StrEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    RECEPTION = "reception"
    DOCTOR = "doctor"
    PATIENT = "patient"


@dataclass(frozen=True)
class AuthenticatedPrincipal:
    subject: str
    role: Role
    organization_id: str | None = None


class AuthenticationProvider:
    """Interface for future authentication providers."""

    async def authenticate(self, token: str) -> AuthenticatedPrincipal:
        raise NotImplementedError
