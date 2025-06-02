"""
Driving Zone Service

This module provides the driving zone service for the Ontario Driving School Manager.
It handles driving zone management and validation.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Dict, Any, Optional, List, Set
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from .base import BaseService
from ..core.metrics import DistributedTracing
from ..core.cache import Cache

logger = logging.getLogger(__name__)

class ZoneType(Enum):
    """Types of driving zones."""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    HIGHWAY = "highway"
    SCHOOL = "school"
    CONSTRUCTION = "construction"

@dataclass
class Zone:
    """Driving zone."""
    id: str
    name: str
    type: ZoneType
    description: str
    restrictions: List[str]
    min_license_level: str
    coordinates: Dict[str, float]
    active: bool = True
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class DrivingZoneService(BaseService[Dict[str, Any]]):
    """Driving zone service."""
    
    def __init__(
        self,
        cache: Optional[Cache] = None,
        tracing: Optional[DistributedTracing] = None
    ):
        """Initialize driving zone service.
        
        Args:
            cache: Optional cache instance
            tracing: Optional tracing instance
        """
        super().__init__(cache, tracing)
        
        # Default zones
        self.default_zones = {
            "residential_1": Zone(
                id="residential_1",
                name="Downtown Residential",
                type=ZoneType.RESIDENTIAL,
                description="Low-traffic residential area",
                restrictions=["30 km/h speed limit", "School zone"],
                min_license_level="G2",
                coordinates={"lat": 43.6532, "lng": -79.3832}
            ),
            "commercial_1": Zone(
                id="commercial_1",
                name="Commercial District",
                type=ZoneType.COMMERCIAL,
                description="High-traffic commercial area",
                restrictions=["50 km/h speed limit", "No parking"],
                min_license_level="G",
                coordinates={"lat": 43.6532, "lng": -79.3832}
            )
        }
    
    async def initialize(self) -> None:
        """Initialize service."""
        self.log_info("Initializing driving zone service")
        
        # Load zones
        try:
            await self._load_zones()
        except Exception as e:
            self.log_error("Failed to load zones", e)
            raise
    
    async def shutdown(self) -> None:
        """Shutdown service."""
        self.log_info("Shutting down driving zone service")
    
    async def _load_zones(self) -> None:
        """Load zones from cache or defaults."""
        with self.trace("load_zones") as span_id:
            # Try to get from cache
            zones = await self.get_cached("driving_zones")
            
            if not zones:
                # Use default zones
                zones = {
                    zone.id: self._zone_to_dict(zone)
                    for zone in self.default_zones.values()
                }
                
                # Cache the zones
                await self.set_cached("driving_zones", zones)
    
    def _zone_to_dict(self, zone: Zone) -> Dict[str, Any]:
        """Convert zone to dictionary.
        
        Args:
            zone: Zone instance
            
        Returns:
            Zone dictionary
        """
        return {
            "id": zone.id,
            "name": zone.name,
            "type": zone.type.value,
            "description": zone.description,
            "restrictions": zone.restrictions,
            "min_license_level": zone.min_license_level,
            "coordinates": zone.coordinates,
            "active": zone.active,
            "created_at": zone.created_at.isoformat(),
            "updated_at": zone.updated_at.isoformat()
        }
    
    def _dict_to_zone(self, data: Dict[str, Any]) -> Zone:
        """Convert dictionary to zone.
        
        Args:
            data: Zone dictionary
            
        Returns:
            Zone instance
        """
        return Zone(
            id=data["id"],
            name=data["name"],
            type=ZoneType(data["type"]),
            description=data["description"],
            restrictions=data["restrictions"],
            min_license_level=data["min_license_level"],
            coordinates=data["coordinates"],
            active=data["active"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
        )
    
    async def get_zone(self, zone_id: str) -> Optional[Zone]:
        """Get zone by ID.
        
        Args:
            zone_id: Zone ID
            
        Returns:
            Zone instance or None
        """
        with self.trace("get_zone") as span_id:
            # Get from cache
            zones = await self.get_cached("driving_zones")
            
            if not zones or zone_id not in zones:
                return None
            
            return self._dict_to_zone(zones[zone_id])
    
    async def get_zones(
        self,
        zone_type: Optional[ZoneType] = None,
        active_only: bool = True
    ) -> List[Zone]:
        """Get zones.
        
        Args:
            zone_type: Optional zone type filter
            active_only: Whether to return only active zones
            
        Returns:
            List of zones
        """
        with self.trace("get_zones") as span_id:
            # Get from cache
            zones = await self.get_cached("driving_zones")
            
            if not zones:
                return []
            
            # Filter zones
            filtered_zones = []
            for zone_data in zones.values():
                zone = self._dict_to_zone(zone_data)
                
                if zone_type and zone.type != zone_type:
                    continue
                
                if active_only and not zone.active:
                    continue
                
                filtered_zones.append(zone)
            
            return filtered_zones
    
    async def create_zone(self, zone: Zone) -> Zone:
        """Create a new zone.
        
        Args:
            zone: Zone to create
            
        Returns:
            Created zone
        """
        with self.trace("create_zone") as span_id:
            # Get current zones
            zones = await self.get_cached("driving_zones") or {}
            
            # Validate zone
            if zone.id in zones:
                raise ValueError(f"Zone {zone.id} already exists")
            
            # Add zone
            zones[zone.id] = self._zone_to_dict(zone)
            
            # Update cache
            await self.set_cached("driving_zones", zones)
            
            return zone
    
    async def update_zone(self, zone: Zone) -> Zone:
        """Update a zone.
        
        Args:
            zone: Zone to update
            
        Returns:
            Updated zone
        """
        with self.trace("update_zone") as span_id:
            # Get current zones
            zones = await self.get_cached("driving_zones")
            
            if not zones or zone.id not in zones:
                raise ValueError(f"Zone {zone.id} not found")
            
            # Update zone
            zones[zone.id] = self._zone_to_dict(zone)
            
            # Update cache
            await self.set_cached("driving_zones", zones)
            
            return zone
    
    async def delete_zone(self, zone_id: str) -> None:
        """Delete a zone.
        
        Args:
            zone_id: Zone ID
        """
        with self.trace("delete_zone") as span_id:
            # Get current zones
            zones = await self.get_cached("driving_zones")
            
            if not zones or zone_id not in zones:
                raise ValueError(f"Zone {zone_id} not found")
            
            # Remove zone
            del zones[zone_id]
            
            # Update cache
            await self.set_cached("driving_zones", zones)
    
    async def validate_zone_for_lesson(
        self,
        zone_id: str,
        student_license: str,
        lesson_type: str
    ) -> List[str]:
        """Validate zone for lesson.
        
        Args:
            zone_id: Zone ID
            student_license: Student license level
            lesson_type: Lesson type
            
        Returns:
            List of validation errors
        """
        with self.trace("validate_zone_for_lesson") as span_id:
            errors = []
            
            # Get zone
            zone = await self.get_zone(zone_id)
            if not zone:
                errors.append(f"Zone {zone_id} not found")
                return errors
            
            # Check if zone is active
            if not zone.active:
                errors.append(f"Zone {zone_id} is not active")
            
            # Check license level
            if student_license < zone.min_license_level:
                errors.append(
                    f"Student license level {student_license} is below required level {zone.min_license_level}"
                )
            
            # Check lesson type restrictions
            if lesson_type == "highway" and zone.type != ZoneType.HIGHWAY:
                errors.append(f"Zone {zone_id} is not suitable for highway lessons")
            
            return errors