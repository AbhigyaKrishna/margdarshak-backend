from fastapi import APIRouter, HTTPException
from typing import Dict

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}

@router.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Welcome to FastAPI Backend"} 