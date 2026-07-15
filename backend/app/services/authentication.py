from dataclasses import dataclass
from uuid import UUID

from app.core.config import settings
from app.models.user import User, UserRole
from app.repositories.auth import AuthRepository
from app.utils.jwt import TokenType, TokenValidationError, create_access_token, create_refresh_token
from app.utils.jwt import decode_token as decode_jwt
from app.utils.password import hash_password, verify_password


class DuplicateEmailError(Exception):
    """Raised when attempting to register an email that already exists."""


class InvalidCredentialsError(Exception):
    """Raised when login credentials are incorrect."""


class InvalidRefreshTokenError(Exception):
    """Raised when a refresh token is invalid or references no active user."""


@dataclass(frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str
    expires_in: int


@dataclass(frozen=True)
class AuthenticationResult:
    user: User
    tokens: TokenPair


class AuthService:
    def __init__(self, repository: AuthRepository) -> None:
        self.repository = repository

    async def register_user(
        self,
        *,
        email: str,
        password: str,
        full_name: str,
        role: UserRole,
    ) -> AuthenticationResult:
        existing_user = await self.repository.get_user_by_email(email)
        if existing_user:
            raise DuplicateEmailError

        user = await self.repository.create_user(
            email=email,
            hashed_password=hash_password(password),
            full_name=full_name,
            role=role,
        )
        return AuthenticationResult(user=user, tokens=self._create_token_pair(user))

    async def login_user(self, *, email: str, password: str) -> AuthenticationResult:
        user = await self.repository.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError

        if user.status != "active":
            raise InvalidCredentialsError

        return AuthenticationResult(user=user, tokens=self._create_token_pair(user))

    async def refresh_tokens(self, refresh_token: str) -> TokenPair:
        try:
            payload = decode_jwt(refresh_token, expected_type=TokenType.REFRESH)
            user_id = UUID(payload["sub"])
        except (ValueError, TokenValidationError) as exc:
            raise InvalidRefreshTokenError from exc

        user = await self.repository.get_user_by_id(user_id)
        if not user or user.status != "active":
            raise InvalidRefreshTokenError

        return self._create_token_pair(user)

    def _create_token_pair(self, user: User) -> TokenPair:
        return TokenPair(
            access_token=create_access_token(user.id, str(user.role)),
            refresh_token=create_refresh_token(user.id, str(user.role)),
            expires_in=settings.jwt_expiry_minutes * 60,
        )
