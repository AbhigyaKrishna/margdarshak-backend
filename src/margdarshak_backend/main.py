from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from src.margdarshak_backend.core.config import settings
from src.margdarshak_backend.api.routes import router as api_router
from src.margdarshak_backend.core.database import db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    try:
        logging.info("Connecting to MongoDB Atlas...")
        await db.connect_db()
        logging.info("Successfully connected to MongoDB Atlas")
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {str(e)}")
        raise
    yield
    # Shutdown logic
    try:
        logging.info("Closing MongoDB connection...")
        await db.close_db()
        logging.info("MongoDB connection closed")
    except Exception as e:
        logging.error(f"Error closing MongoDB connection: {str(e)}")

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API",
    version="1.0.0",
    lifespan=lifespan,
    debug=settings.DEBUG_MODE,
    openapi_tags=[
        {
            "name": "langflow",
            "description": "AI Flow Operations",
            "externalDocs": {
                "description": "Langflow Documentation",
                "url": "https://docs.langflow.org",
            },
        },
        {
            "name": "health",
            "description": "Health check endpoints",
        },
    ],
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  # Hide schemas section by default
        "displayRequestDuration": True,   # Show request duration
        "filter": True,                   # Enable filtering operations
        "syntaxHighlight.theme": "monokai"
    }
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR) 