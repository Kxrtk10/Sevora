from datetime import UTC, datetime

from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", checked_at=datetime.now(UTC))
