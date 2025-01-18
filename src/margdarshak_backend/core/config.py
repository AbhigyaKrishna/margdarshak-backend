from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Backend"
    DEBUG_MODE: bool = True
    API_V1_STR: str = "/api"
    
    # Database settings (example)
    DATABASE_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings() 