from fastapi import APIRouter, HTTPException
from typing import Dict

from src.margdarshak_backend.api.langflow import router as langflow_router
from src.margdarshak_backend.api.user import router as user_router
from src.margdarshak_backend.api.horoscope import router as horoscope_router

router = APIRouter()

# Include Langflow routes
router.include_router(
    langflow_router,
    prefix="/langflow",
    tags=["langflow"]
)

# Include User routes
router.include_router(
    user_router,
    prefix="/user",
    tags=["user"]
)

# Include Horoscope routes
router.include_router(
    horoscope_router,
    prefix="/horoscope",
    tags=["horoscope"]
)

@router.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}

@router.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Welcome to MargDarshak Backend"}