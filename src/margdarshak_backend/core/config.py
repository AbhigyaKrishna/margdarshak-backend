from pydantic_settings import BaseSettings
from typing import Optional
from urllib.parse import quote_plus

class Settings(BaseSettings):
    APP_NAME: str = "MargDarshak Backend"
    DEBUG_MODE: bool = True
    API_V1_STR: str = "/api"
    
    # Langflow settings
    LANGFLOW_API_URL: str = "http://localhost:7860"
    LANGFLOW_API_KEY: Optional[str] = None
    LANGFLOW_ID: Optional[str] = None
    
    # MongoDB Atlas settings
    MONGODB_URL: str
    MONGODB_DB_NAME: str
    MONGODB_USERNAME: Optional[str] = None
    MONGODB_PASSWORD: Optional[str] = None

    # Astrology API settings
    ASTROLOGY_API_KEY: Optional[str] = None
    
    @property
    def mongodb_connection_string(self) -> str:
        """Generate MongoDB connection string with proper escaping."""
        if self.MONGODB_USERNAME and self.MONGODB_PASSWORD:
            username = quote_plus(self.MONGODB_USERNAME)
            password = quote_plus(self.MONGODB_PASSWORD)
            return self.MONGODB_URL.replace('<db_username>', username).replace('<db_password>', password)
        return self.MONGODB_URL
    
    class Config:
        env_file = ".env"

settings = Settings() 