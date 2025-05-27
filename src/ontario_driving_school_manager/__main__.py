"""
Main entry point for the Ontario Driving School Manager.
"""
import uvicorn
from ontario_driving_school_manager.main import app

def main():
    """Run the FastAPI application."""
    uvicorn.run(
        "ontario_driving_school_manager.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main() 