from typing import Protocol

from app.core.security import AuthenticatedPrincipal


class AuthenticationService(Protocol):
    async def authenticate_token(self, token: str) -> AuthenticatedPrincipal:
        """Authenticate a future access token."""
