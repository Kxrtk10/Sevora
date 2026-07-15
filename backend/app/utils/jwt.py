from datetime import UTC, datetime, timedelta
from enum import StrEnum
from uuid import UUID

import jwt

from app.core.config import settings

ALGORITHM = "HS256"


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenValidationError(Exception):
    """Raised when a JWT is missing, expired, malformed, or has the wrong type."""


def create_access_token(user_id: UUID, role: str) -> str:
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.jwt_expiry_minutes)
    return _encode_token(
        user_id=user_id,
        role=role,
        token_type=TokenType.ACCESS,
        expires_at=expires_at,
    )


def create_refresh_token(user_id: UUID, role: str) -> str:
    expires_at = datetime.now(UTC) + timedelta(days=settings.refresh_token_expiry_days)
    return _encode_token(
        user_id=user_id,
        role=role,
        token_type=TokenType.REFRESH,
        expires_at=expires_at,
    )


def decode_token(token: str, expected_type: TokenType) -> dict[str, str]:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:
        raise TokenValidationError("Invalid token") from exc

    if payload.get("type") != expected_type.value:
        raise TokenValidationError("Invalid token type")

    subject = payload.get("sub")
    if not subject:
        raise TokenValidationError("Token subject is missing")

    return payload


def _encode_token(user_id: UUID, role: str, token_type: TokenType, expires_at: datetime) -> str:
    issued_at = datetime.now(UTC)
    payload = {
        "sub": str(user_id),
        "role": role,
        "type": token_type.value,
        "iat": issued_at,
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)
