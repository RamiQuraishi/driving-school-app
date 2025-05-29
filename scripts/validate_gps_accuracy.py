#!/usr/bin/env python3
"""
Test script for validating GPS accuracy in the driving school management system.
Tests GPS data collection, processing, and accuracy metrics.
"""

import asyncio
import logging
import math
import random
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import aiohttp
import numpy as np
import pytest
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GPSDataPoint(BaseModel):
    """Model for GPS data points."""
    timestamp: datetime
    latitude: float
    longitude: float
    accuracy: float
    speed: float
    altitude: float
    heading: float
    satellites: int
    signal_strength: float

class GPSAccuracyTester:
    """Test class for GPS accuracy validation."""
    
    def __init__(self, known_route: List[Tuple[float, float]]):
        self.known_route = known_route
        self.collected_points: List[GPSDataPoint] = []
        self.accuracy_metrics: Dict[str, float] = {}
    
    def simulate_gps_data(self, num_points: int) -> List[GPSDataPoint]:
        """Simulate GPS data collection with controlled accuracy."""
        points = []
        
        for i in range(num_points):
            # Get base coordinates from known route
            base_lat, base_lon = self.known_route[i % len(self.known_route)]
            
            # Add random error based on accuracy level
            accuracy = random.uniform(2.0, 10.0)  # meters
            error_lat = random.gauss(0, accuracy / 111000)  # Convert meters to degrees
            error_lon = random.gauss(0, accuracy / (111000 * math.cos(math.radians(base_lat))))
            
            point = GPSDataPoint(
                timestamp=datetime.now(),
                latitude=base_lat + error_lat,
                longitude=base_lon + error_lon,
                accuracy=accuracy,
                speed=random.uniform(0, 100),
                altitude=random.uniform(0, 100),
                heading=random.uniform(0, 360),
                satellites=random.randint(4, 12),
                signal_strength=random.uniform(-100, -50)
            )
            points.append(point)
        
        return points
    
    def calculate_accuracy_metrics(self, points: List[GPSDataPoint]) -> Dict[str, float]:
        """Calculate various accuracy metrics."""
        metrics = {
            "horizontal_accuracy": np.mean([p.accuracy for p in points]),
            "vertical_accuracy": np.std([p.altitude for p in points]),
            "speed_accuracy": np.std([p.speed for p in points]),
            "signal_quality": np.mean([p.signal_strength for p in points]),
            "satellite_coverage": np.mean([p.satellites for p in points])
        }
        return metrics
    
    def calculate_position_error(self, points: List[GPSDataPoint]) -> float:
        """Calculate position error compared to known route."""
        errors = []
        
        for i, point in enumerate(points):
            known_lat, known_lon = self.known_route[i % len(self.known_route)]
            error = math.sqrt(
                (point.latitude - known_lat) ** 2 +
                (point.longitude - known_lon) ** 2
            ) * 111000  # Convert to meters
            errors.append(error)
        
        return np.mean(errors)
    
    async def test_gps_accuracy(self):
        """Run the complete GPS accuracy test."""
        try:
            # Simulate GPS data collection
            points = self.simulate_gps_data(100)
            logger.info(f"Collected {len(points)} GPS data points")
            
            # Calculate accuracy metrics
            self.accuracy_metrics = self.calculate_accuracy_metrics(points)
            logger.info("Accuracy metrics calculated")
            
            # Calculate position error
            position_error = self.calculate_position_error(points)
            logger.info(f"Average position error: {position_error:.2f} meters")
            
            # Validate results
            assert self.accuracy_metrics["horizontal_accuracy"] < 10.0, "Horizontal accuracy too low"
            assert self.accuracy_metrics["satellite_coverage"] >= 4, "Insufficient satellite coverage"
            assert position_error < 15.0, "Position error too high"
            
            logger.info("GPS accuracy test completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"GPS accuracy test failed: {str(e)}")
            return False

@pytest.mark.asyncio
async def test_gps_accuracy():
    """Main test function."""
    # Define a known test route (latitude, longitude pairs)
    test_route = [
        (43.6532, -79.3832),  # Toronto
        (43.6519, -79.3817),
        (43.6506, -79.3802),
        (43.6493, -79.3787),
        (43.6480, -79.3772)
    ]
    
    tester = GPSAccuracyTester(test_route)
    success = await tester.test_gps_accuracy()
    assert success, "GPS accuracy test failed"

if __name__ == "__main__":
    asyncio.run(test_gps_accuracy()) 