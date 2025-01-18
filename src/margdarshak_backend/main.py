from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.margdarshak_backend.core.config import settings
from src.margdarshak_backend.api.routes import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic (if any)
    print("Starting up...")
    yield
    # Shutdown logic (if any)
    print("Shutting down...")

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