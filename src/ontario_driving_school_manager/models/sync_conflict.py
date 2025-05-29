"""Sync conflict model for tracking data synchronization conflicts."""

from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.orm import relationship

from .base import BaseModel

class SyncConflict(BaseModel):
    """Sync conflict model.
    
    This model tracks:
    - Data synchronization conflicts
    - Conflict resolution
    - Version tracking
    """
    
    table_name = Column(String(100), nullable=False)
    record_id = Column(Integer, nullable=False)
    local_version = Column(Integer, nullable=False)
    server_version = Column(Integer, nullable=False)
    local_data = Column(JSON, nullable=False)
    server_data = Column(JSON, nullable=False)
    resolved_data = Column(JSON)
    resolution_type = Column(String(50))
    resolved_at = Column(DateTime)
    
    def is_resolved(self) -> bool:
        """Check if conflict is resolved.
        
        Returns:
            bool: True if resolved
        """
        return self.resolved_data is not None and self.resolution_type is not None
    
    def get_conflicting_fields(self) -> Dict[str, tuple[Any, Any]]:
        """Get conflicting fields.
        
        Returns:
            Dict[str, tuple[Any, Any]]: Dictionary of conflicting fields
        """
        conflicts = {}
        for key in set(self.local_data.keys()) | set(self.server_data.keys()):
            local_value = self.local_data.get(key)
            server_value = self.server_data.get(key)
            if local_value != server_value:
                conflicts[key] = (local_value, server_value)
        return conflicts
    
    def resolve(self, resolved_data: Dict[str, Any], resolution_type: str) -> None:
        """Resolve conflict.
        
        Args:
            resolved_data: Resolved data
            resolution_type: Resolution type
        """
        self.resolved_data = resolved_data
        self.resolution_type = resolution_type
        self.resolved_at = datetime.utcnow()
    
    def get_resolution_summary(self) -> str:
        """Get resolution summary.
        
        Returns:
            str: Resolution summary
        """
        if not self.is_resolved():
            return "Conflict not resolved"
        
        return (
            f"Conflict resolved at {self.resolved_at}\n"
            f"Resolution type: {self.resolution_type}\n"
            f"Conflicting fields: {len(self.get_conflicting_fields())}"
        ) 