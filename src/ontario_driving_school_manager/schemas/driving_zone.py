"""
Driving zone schema for Ontario Driving School Manager.
Defines the structure for driving zone data and validations.
"""

from datetime import datetime
from typing import List, Optional, Dict
from pydantic import Field, validator
from .base import BaseSchema
import re

class DrivingZoneSchema(BaseSchema):
    """Schema for driving zone data."""
    
    zone_id: str = Field(..., description="Unique identifier for the driving zone")
    name: str = Field(..., description="Name of the driving zone")
    description: Optional[str] = Field(None, description="Description of the driving zone")
    boundaries: Dict[str, List[float]] = Field(..., description="Geographic boundaries of the zone")
    center_point: Dict[str, float] = Field(..., description="Center point of the zone")
    radius_km: float = Field(..., description="Radius of the zone in kilometers")
    status: str = Field(default="active", description="Status of the driving zone")
    restrictions: List[str] = Field(default_factory=list, description="List of driving restrictions")
    available_times: Dict[str, List[str]] = Field(default_factory=dict, description="Available times for lessons")
    instructor_ids: List[str] = Field(default_factory=list, description="List of instructor IDs assigned to this zone")
    
    @validator('boundaries')
    def validate_boundaries(cls, v):
        """Validate zone boundaries."""
        required_keys = ['north', 'south', 'east', 'west']
        missing_keys = [key for key in required_keys if key not in v]
        if missing_keys:
            raise ValueError(f'Missing boundary coordinates: {", ".join(missing_keys)}')
        
        for direction, coords in v.items():
            if not isinstance(coords, list) or len(coords) != 2:
                raise ValueError(f'Invalid coordinates for {direction}')
            if not all(isinstance(coord, (int, float)) for coord in coords):
                raise ValueError(f'Coordinates must be numbers for {direction}')
        
        return v
    
    @validator('center_point')
    def validate_center_point(cls, v):
        """Validate center point coordinates."""
        required_keys = ['latitude', 'longitude']
        missing_keys = [key for key in required_keys if key not in v]
        if missing_keys:
            raise ValueError(f'Missing center point coordinates: {", ".join(missing_keys)}')
        
        if not all(isinstance(v[key], (int, float)) for key in required_keys):
            raise ValueError('Center point coordinates must be numbers')
        
        if not (-90 <= v['latitude'] <= 90):
            raise ValueError('Latitude must be between -90 and 90')
        if not (-180 <= v['longitude'] <= 180):
            raise ValueError('Longitude must be between -180 and 180')
        
        return v
    
    @validator('radius_km')
    def validate_radius(cls, v):
        """Validate zone radius."""
        if v <= 0:
            raise ValueError('Radius must be greater than 0')
        if v > 100:  # Arbitrary maximum radius
            raise ValueError('Radius cannot exceed 100 km')
        return v
    
    @validator('status')
    def validate_status(cls, v):
        """Validate zone status."""
        valid_statuses = ['active', 'inactive', 'maintenance', 'restricted']
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v
    
    @validator('available_times')
    def validate_available_times(cls, v):
        """Validate available times format."""
        valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        
        for day, times in v.items():
            if day.lower() not in valid_days:
                raise ValueError(f'Invalid day: {day}')
            
            if not isinstance(times, list):
                raise ValueError(f'Times must be a list for {day}')
            
            for time_slot in times:
                if not isinstance(time_slot, str):
                    raise ValueError(f'Time slot must be a string for {day}')
                # Basic time format validation (HH:MM-HH:MM)
                if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]-([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', time_slot):
                    raise ValueError(f'Invalid time slot format for {day}: {time_slot}')
        
        return v 