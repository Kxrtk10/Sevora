from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_auth_service
from app.schemas.auth import (
    AuthTokenResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.services.authentication import (
    AuthService,
    DuplicateEmailError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    TokenPair,
)

router = APIRouter()


@router.post(
    "/register",
    response_model=AuthTokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    payload: UserRegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> AuthTokenResponse:
    try:
        result = await auth_service.register_user(
            email=payload.email,
            password=payload.password,
            full_name=payload.full_name,
            role=payload.role,
        )
    except DuplicateEmailError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        ) from exc

    return _auth_response(user=UserResponse.model_validate(result.user), tokens=result.tokens)


@router.post("/login", response_model=AuthTokenResponse)
async def login_user(
    payload: UserLoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> AuthTokenResponse:
    try:
        result = await auth_service.login_user(email=payload.email, password=payload.password)
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        ) from exc

    return _auth_response(user=UserResponse.model_validate(result.user), tokens=result.tokens)


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(
    payload: RefreshTokenRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RefreshTokenResponse:
    try:
        tokens = await auth_service.refresh_tokens(payload.refresh_token)
    except InvalidRefreshTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token.",
        ) from exc

    return RefreshTokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        expires_in=tokens.expires_in,
    )


def _auth_response(user: UserResponse, tokens: TokenPair) -> AuthTokenResponse:
    return AuthTokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        expires_in=tokens.expires_in,
        user=user,
    )
