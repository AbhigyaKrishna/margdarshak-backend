from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from datetime import datetime, time
import logging

from src.margdarshak_backend.models.horoscope import UserData
from src.margdarshak_backend.core.database import db

router = APIRouter()

@router.post("/")
async def create_user_data(data: UserData) -> Dict[str, Any]:
    """
    Store user's data.
    
    Args:
        data: User's information including birth details and location
    
    Returns:
        dict: Confirmation message and user_id
    """
    try:
        user_data = data.model_dump()
        result = await db.get_db()["user_data"].insert_one(user_data)
        
        return {
            "message": "User data stored successfully",
            "user_id": str(result.inserted_id)
        }
    except Exception as e:
        logging.error(f"Error storing user data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error storing user data: {str(e)}"
        )

@router.get("/{user_id}")
async def get_user_data(user_id: str) -> UserData:
    """
    Retrieve user's data.
    
    Args:
        user_id: Unique identifier for the user
    
    Returns:
        HoroscopeData: User's information
    """
    try:
        data = await db.get_db()["user_data"].find_one({"user_id": user_id})
        if not data:
            raise HTTPException(status_code=404, detail="User data not found")
        return UserData(**data)
    except Exception as e:
        logging.error(f"Error retrieving user data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving user data: {str(e)}"
        )