from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_ai_concierge_service
from app.schemas.ai_concierge import AIConciergeRequest, AIConciergeResponse
from app.services.ai_concierge import AIConciergeService

router = APIRouter()


@router.post("/message", response_model=AIConciergeResponse)
async def handle_concierge_message(
    payload: AIConciergeRequest,
    service: Annotated[AIConciergeService, Depends(get_ai_concierge_service)],
) -> AIConciergeResponse:
    return await service.handle(payload)
