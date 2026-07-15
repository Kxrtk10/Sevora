from fastapi import APIRouter

from app.api.v1.endpoints import ai_concierge, appointments, auth, health, hospital_domain

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
api_router.include_router(hospital_domain.router, tags=["hospital-domain"])
api_router.include_router(ai_concierge.router, prefix="/ai-concierge", tags=["ai-concierge"])
