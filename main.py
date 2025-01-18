import uvicorn
from src.margdarshak_backend.main import app

if __name__ == "__main__":
    uvicorn.run(
        "src.margdarshak_backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        workers=1,    # Number of worker processes
        log_level="info"
    )