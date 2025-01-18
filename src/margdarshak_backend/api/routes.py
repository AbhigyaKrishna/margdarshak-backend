from fastapi import APIRouter, HTTPException
from typing import Dict

from langflow import router as langflow_router

router = APIRouter()

# Include Langflow routes
router.include_router(
    langflow_router,
    prefix="/langflow",
    tags=["langflow"]
)

@router.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}

@router.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Welcome to MargDarshak Backend"} 