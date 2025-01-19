from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Literal
from datetime import datetime, time
import logging
import requests
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl
from PIL import Image
import io
from src.margdarshak_backend.core.gemini import model as gemini_model

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

class ChartType(str, Enum):
    D1 = "d1"
    D2 = "d2"
    D3 = "d3"
    D4 = "d4"
    D5 = "d5"
    D6 = "d6"
    D7 = "d7"
    D8 = "d8"
    D9 = "d9"
    D10 = "d10"
    D11 = "d11"
    D12 = "d12"
    D16 = "d16"
    D20 = "d20"
    D24 = "d24"
    D27 = "d27"
    D30 = "d30"
    D40 = "d40"
    D45 = "d45"
    D60 = "d60"

def chart_type_to_endpoint(chart_type: ChartType) -> str:
    if chart_type == ChartType.D1:
        return "horoscope-chart-url"
    elif chart_type == ChartType.D9:
        return "navamsa-chart-url"
    else:
        return f"{chart_type}-chart-url"

async def get_chart_data(user_id: str, chart_type: ChartType) -> Dict[str, Any]:
    """
    Common function to get chart data from Astrology API.
    
    Args:
        user_id: User's unique identifier
        chart_type: Type of chart to generate (ChartType)
    
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
        
        url = f"https://json.freeastrologyapi.com/{chart_type_to_endpoint(chart_type)}"
        
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

class ChartAnalysisRequest(BaseModel):
    image_url: HttpUrl
    chart_type: ChartType

@router.post("/analyze-chart")
async def analyze_chart(request: ChartAnalysisRequest) -> Dict[str, Any]:
    """
    Analyze an astrological chart image using Google's Gemini AI model.
    
    Args:
        request: Contains image URL of the astrological chart
            - image_url: URL of the chart image to analyze
    
    Returns:
        dict: Gemini's analysis of the astrological chart
    """
    try:
        # Download image from URL
        response = requests.get(str(request.image_url))
        response.raise_for_status()
        
        if not response.content:
            raise HTTPException(status_code=400, detail="Empty image content")
            
        # Convert to PIL Image
        img = Image.open(io.BytesIO(response.content))
        
        # Fixed prompt for astrological chart analysis
        prompt = f"You are an expert astrologer. Analyze this {request.chart_type} astrological chart and provide insights about the planetary positions and their significance."
        
        # Generate response from Gemini
        response = gemini_model.generate_content([prompt, img])
        response.resolve()
        
        return {
            "text": response.text
        }
        
    except requests.RequestException as e:
        logging.error(f"Error downloading image: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Error downloading image: {str(e)}"
        )
    except Exception as e:
        logging.error(f"Error analyzing chart: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing chart: {str(e)}"
        )

@router.post("/gem-suggestion")
async def get_gem_suggestion(user_id: str) -> Dict[str, Any]:
    """
    Get gemstone suggestions based on user's birth details from Vedic Rishi API,
    enriched with detailed descriptions from Gemini.
    
    Args:
        user_id: User's unique identifier
    
    Returns:
        dict: Gemstone suggestions with detailed descriptions
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
        
        # Prepare request payload
        payload = {
            "apiName": "basic_gem_suggestion",
            "userData": {
                "nameu": user.name,
                "birth": f"{user.city}, {user.state}",
                "day": birth_date.day,
                "month": birth_date.month,
                "year": birth_date.year,
                "min": birth_time.minute,
                "hour": birth_time.hour,
                "language": "english",
                "gender": user.gender.value,
                "tzone": 5.5,  # IST
                "country": "India",
                "lat": latitude,
                "lon": longitude
            }
        }
        
        # Call Vedic Rishi API
        headers = {
            'Content-Type': 'application/json',
            'Origin': 'https://vedicrishi.in',
            'Referer': 'https://vedicrishi.in/'
        }
        
        response = requests.post(
            'https://workers.vedicrishi.in/vedicrishi',
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        vedic_response = response.json()

        import asyncio
        
        async def get_gem_description(key: str, value: dict) -> None:
            prompt = f"""You are an expert gemologist and astrologer. 
            Provide a detailed description of the {key.lower()} gemstone and its astrological significance: {value["name"]} with semi gem {value["semi_gem"]}.
            Include information about:
            1. Physical properties
            2. Astrological benefits
            3. How to wear them
            4. Best practices for using these gemstones
            Format the response in clear sections."""

            gemini_response = gemini_model.generate_content(prompt)
            gemini_response.resolve()
            value["gem_description"] = gemini_response.text

        # Create tasks for each gem
        tasks = []
        for key, value in vedic_response["response"].items():
            task = asyncio.create_task(get_gem_description(key, value))
            tasks.append(task)
            
        # Wait for all tasks to complete
        await asyncio.gather(*tasks)
            
        return vedic_response
        
    except requests.RequestException as e:
        logging.error(f"Error fetching gem suggestions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching gem suggestions: {str(e)}"
        )
    except Exception as e:
        logging.error(f"Error processing gem suggestions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing gem suggestions: {str(e)}"
        )

