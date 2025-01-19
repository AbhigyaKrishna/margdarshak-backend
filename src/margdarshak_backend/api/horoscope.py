from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Literal
from datetime import datetime, time
import logging
import requests
from enum import Enum
from pydantic import BaseModel, Field

from margdarshak_backend.models.user import UserData
from src.margdarshak_backend.core.database import db
from src.margdarshak_backend.core.config import settings

router = APIRouter()

class ZodiacSign(str, Enum):
    ARIES = "Aries"
    TAURUS = "Taurus"
    GEMINI = "Gemini"
    CANCER = "Cancer"
    LEO = "Leo"
    VIRGO = "Virgo"
    LIBRA = "Libra"
    SCORPIO = "Scorpio"
    SAGITTARIUS = "Sagittarius"
    CAPRICORN = "Capricorn"
    AQUARIUS = "Aquarius"
    PISCES = "Pisces"

class Day(str, Enum):
    TODAY = "TODAY"
    TOMORROW = "TOMORROW"
    YESTERDAY = "YESTERDAY"

location = {
    "Delhi": ("28.6139", "77.2090"),
    "Mumbai": ("19.0760", "72.8777"),
    "Kolkata": ("22.5726", "88.3639"),
    "Chennai": ("13.0825", "80.2707"),
    "Bengaluru": ("12.9716", "77.5946")
}

async def get_chart_data(user_id: str, chart_type: Literal["navamsa", "rasi", "d10"]) -> Dict[str, Any]:
    """
    Common function to get chart data from Astrology API.
    
    Args:
        user_id: User's unique identifier
        chart_type: Type of chart to generate ("navamsa", "rasi", or "d10")
    
    Returns:
        dict: Response containing the chart URL
    
    Raises:
        HTTPException: If user not found or invalid location
    """
    try:
        # Get user data from MongoDB
        user_data = await db.get_db()["user_data"].find_one({"user_id": user_id})
        if not user_data:
            raise HTTPException(status_code=404, detail="User data not found")
        
        # Convert user data to model for validation
        user = UserData(**user_data)
        
        # Get location coordinates
        if user.city not in location:
            raise HTTPException(status_code=400, detail="Invalid location")
        latitude, longitude = location[user.city]
        
        # Extract date and time components
        birth_date = user.date_of_birth
        birth_time = user.time_of_birth
        
        # Prepare request data
        chart_data = {
            "year": birth_date.year,
            "month": birth_date.month,
            "date": birth_date.day,
            "hours": birth_time.hour,
            "minutes": birth_time.minute,
            "seconds": birth_time.second,
            "latitude": float(latitude),
            "longitude": float(longitude),
            "timezone": 5.5,  # IST
            "config": {
                "observation_point": "topocentric",
                "ayanamsha": "lahiri"
            }
        }
        
        # Update endpoint mapping
        endpoints = {
            "navamsa": "navamsa-chart-url",
            "rasi": "horoscope-chart-url",
            "d10": "d10-chart-url"
        }
        
        url = f"https://json.freeastrologyapi.com/{endpoints[chart_type]}"
        
        # Call astrology API
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': settings.ASTROLOGY_API_KEY
        }
        
        response = requests.post(
            url,
            headers=headers,
            json=chart_data
        )
        response.raise_for_status()
        return response.json()
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching {chart_type} chart: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching {chart_type} chart: {str(e)}"
        )

@router.post("/navamsa-chart")
async def get_navamsa_chart(user_id: str) -> Dict[str, Any]:
    """
    Get Navamsa chart URL from Astrology API using user's birth data.
    
    Args:
        user_id: User's unique identifier
    
    Returns:
        dict: Response containing the chart URL
    """
    return await get_chart_data(user_id, "navamsa")

@router.post("/rasi-chart")
async def get_rasi_chart(user_id: str) -> Dict[str, Any]:
    """
    Get Rasi (Birth) chart URL from Astrology API using user's birth data.
    
    Args:
        user_id: User's unique identifier
    
    Returns:
        dict: Response containing the chart URL
    """
    return await get_chart_data(user_id, "rasi")

@router.post("/d10-chart")
async def get_d10_chart(user_id: str) -> Dict[str, Any]:
    """
    Get D10 (Dasamsa) chart URL from Astrology API using user's birth data.
    The D10 chart is particularly used for career and profession analysis.
    
    Args:
        user_id: User's unique identifier
    
    Returns:
        dict: Response containing the chart URL
    """
    return await get_chart_data(user_id, "d10")

@router.get("/daily")
async def get_daily_horoscope(
    sign: ZodiacSign,
    day: Day = Day.TODAY
) -> Dict[str, Any]:
    """
    Get daily horoscope for a zodiac sign.
    
    Args:
        sign: Zodiac sign
        day: Day for horoscope (TODAY/TOMORROW/YESTERDAY)
    
    Returns:
        dict: Horoscope data including date and prediction
    """
    try:
        response = requests.get(
            f"https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily",
            params={"sign": sign, "day": day}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching horoscope: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching horoscope: {str(e)}"
        )
    
@router.get("/monthly")
async def get_monthly_horoscope(
    sign: ZodiacSign
) -> Dict[str, Any]:
    """
    Get monthly horoscope for a zodiac sign.
    
    Args:
        sign: Zodiac sign
    
    Returns:
        dict: Horoscope data including date and prediction
    """
    try:
        response = requests.get(
            f"https://horoscope-app-api.vercel.app/api/v1/get-horoscope/monthly",
            params={"sign": sign}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching horoscope: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching horoscope: {str(e)}"
        )

