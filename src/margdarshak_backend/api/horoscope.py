from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from datetime import datetime, time
import logging
import requests
from enum import Enum

from src.margdarshak_backend.models.horoscope import UserData
from src.margdarshak_backend.core.database import db

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
