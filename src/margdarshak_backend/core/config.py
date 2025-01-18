from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "MargDarshak Backend"
    DEBUG_MODE: bool = True
    API_V1_STR: str = "/api"
    
    # Langflow settings
    LANGFLOW_API_URL: str = "http://localhost:7860"
    LANGFLOW_API_KEY: Optional[str] = None
    LANGFLOW_ID: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings() 