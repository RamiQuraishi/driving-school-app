"""
Main Application

This module contains the main application logic for the Ontario Driving School Manager.
It sets up the FastAPI server and initializes core components.

Author: Rami Drive School
Date: 2024
"""

import os
import logging
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .core.analytics import PrivacyCompliantAnalytics, TelemetryService
from .core.monitoring import (
    PerformanceTracker,
    ErrorTracker,
    ConflictTracker,
    BusinessMetrics,
    HealthChecker
)

# Configure logging
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Ontario Driving School Manager",
    description="API for managing driving schools in Ontario",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Electron app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize core components
analytics = None
telemetry = None
performance_tracker = None
error_tracker = None
conflict_tracker = None
business_metrics = None
health_checker = None

def initialize_components(data_dir: Optional[str] = None) -> None:
    """Initialize core components.
    
    Args:
        data_dir: Directory to store data files
    """
    global analytics, telemetry, performance_tracker, error_tracker
    global conflict_tracker, business_metrics, health_checker
    
    # Set up data directory
    if data_dir is None:
        data_dir = os.path.join(os.path.expanduser("~"), ".ontario_driving_school")
    
    os.makedirs(data_dir, exist_ok=True)
    
    # Initialize components
    analytics = PrivacyCompliantAnalytics(
        storage_path=os.path.join(data_dir, "analytics.json")
    )
    
    telemetry = TelemetryService(
        app_version="1.0.0",
        storage_path=os.path.join(data_dir, "telemetry.json")
    )
    
    performance_tracker = PerformanceTracker(
        storage_path=os.path.join(data_dir, "performance.json")
    )
    
    error_tracker = ErrorTracker(
        storage_path=os.path.join(data_dir, "errors.json")
    )
    
    conflict_tracker = ConflictTracker(
        storage_path=os.path.join(data_dir, "conflicts.json")
    )
    
    business_metrics = BusinessMetrics(
        storage_path=os.path.join(data_dir, "metrics.json")
    )
    
    health_checker = HealthChecker(
        storage_path=os.path.join(data_dir, "health.json")
    )

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup."""
    initialize_components()

@app.get("/health")
async def health_check():
    """Check system health."""
    if health_checker is None:
        raise HTTPException(status_code=503, detail="Health checker not initialized")
    
    return health_checker.check_system_health()

def main():
    """Run the application."""
    # Get port from environment or use default
    port = int(os.getenv("PORT", "8000"))
    
    # Run server
    uvicorn.run(
        "ontario_driving_school_manager.main:app",
        host="127.0.0.1",
        port=port,
        reload=True
    )

if __name__ == "__main__":
    main() 