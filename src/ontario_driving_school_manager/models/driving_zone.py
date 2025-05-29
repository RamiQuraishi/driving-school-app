"""Driving zone models for managing lesson zones."""

from datetime import time
from typing import List, Optional

from sqlalchemy import Column, Integer, String, Boolean, Float, Time, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel

class DrivingZone(BaseModel):
    """Driving zone model.
    
    This model manages:
    - Zone definitions
    - Zone boundaries
    - Zone pricing
    - Zone availability
    """
    
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    boundaries = relationship("ZoneBoundary", back_populates="zone")
    pricing = relationship("ZonePricing", back_populates="zone")
    availability = relationship("ZoneAvailability", back_populates="zone")
    
    def get_boundaries(self) -> List[tuple[float, float]]:
        """Get zone boundaries.
        
        Returns:
            List[tuple[float, float]]: List of (latitude, longitude) points
        """
        return [(b.latitude, b.longitude) for b in sorted(self.boundaries, key=lambda x: x.sequence)]
    
    def get_price(self, lesson_type: str) -> Optional[float]:
        """Get zone price for lesson type.
        
        Args:
            lesson_type: Lesson type
            
        Returns:
            Optional[float]: Price if found
        """
        for price in self.pricing:
            if price.lesson_type == lesson_type and price.is_active:
                return price.price
        return None
    
    def is_available(self, day_of_week: int, time: time) -> bool:
        """Check if zone is available.
        
        Args:
            day_of_week: Day of week (0-6)
            time: Time to check
            
        Returns:
            bool: True if available
        """
        for availability in self.availability:
            if (availability.day_of_week == day_of_week and
                availability.is_active and
                availability.start_time <= time <= availability.end_time):
                return True
        return False

class ZoneBoundary(BaseModel):
    """Zone boundary model."""
    
    zone_id = Column(Integer, ForeignKey("drivingzone.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    sequence = Column(Integer, nullable=False)
    
    # Relationships
    zone = relationship("DrivingZone", back_populates="boundaries")

class ZonePricing(BaseModel):
    """Zone pricing model."""
    
    zone_id = Column(Integer, ForeignKey("drivingzone.id"), nullable=False)
    lesson_type = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    zone = relationship("DrivingZone", back_populates="pricing")

class ZoneAvailability(BaseModel):
    """Zone availability model."""
    
    zone_id = Column(Integer, ForeignKey("drivingzone.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0-6
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    zone = relationship("DrivingZone", back_populates="availability") 