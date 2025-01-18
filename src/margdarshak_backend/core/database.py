from motor.motor_asyncio import AsyncIOMotorClient
from src.margdarshak_backend.core.config import settings
import logging
from urllib.parse import quote_plus

class MongoDB:
    client: AsyncIOMotorClient = None
    
    @classmethod
    async def connect_db(cls):
        """Create database connection to MongoDB Atlas."""
        try:
            # Create MongoDB client with connection pooling and timeouts
            cls.client = AsyncIOMotorClient(
                settings.mongodb_connection_string,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                maxPoolSize=10,
                retryWrites=True
            )
            
            # Verify connection
            await cls.client.admin.command('ping')
            logging.info("Successfully connected to MongoDB Atlas")
            
        except Exception as e:
            logging.error(f"Error connecting to MongoDB Atlas: {str(e)}")
            raise
            
    @classmethod
    async def close_db(cls):
        """Close database connection."""
        try:
            if cls.client is not None:
                cls.client.close()
                logging.info("MongoDB connection closed")
        except Exception as e:
            logging.error(f"Error closing MongoDB connection: {str(e)}")
            
    @classmethod
    def get_db(cls):
        """Get database instance."""
        if not cls.client:
            raise ConnectionError("Database client not initialized")
        return cls.client[settings.MONGODB_DB_NAME]

db = MongoDB() 