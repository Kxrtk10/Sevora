from fastapi import APIRouter, status

from app.schemas.auth import AuthArchitectureResponse

router = APIRouter()


@router.get(
    "/architecture",
    response_model=AuthArchitectureResponse,
    status_code=status.HTTP_200_OK,
)
async def authentication_architecture() -> AuthArchitectureResponse:
    return AuthArchitectureResponse(
        status="prepared",
        message=(
            "Authentication boundaries are defined; "
            "login implementation is intentionally deferred."
        ),
    )
