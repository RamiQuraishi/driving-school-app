"""
Sync conflict schema for Ontario Driving School Manager.
Defines the structure for handling data synchronization conflicts.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import Field, validator
from .base import BaseSchema

class SyncConflictSchema(BaseSchema):
    """Schema for data synchronization conflicts."""
    
    entity_type: str = Field(..., description="Type of entity in conflict (e.g., 'student', 'instructor')")
    entity_id: str = Field(..., description="ID of the entity in conflict")
    local_version: Dict[str, Any] = Field(..., description="Local version of the data")
    remote_version: Dict[str, Any] = Field(..., description="Remote version of the data")
    conflict_type: str = Field(..., description="Type of conflict (e.g., 'update_conflict', 'delete_conflict')")
    resolution: Optional[str] = Field(None, description="Resolution of the conflict")
    resolved_at: Optional[datetime] = Field(None, description="When the conflict was resolved")
    resolution_notes: Optional[str] = Field(None, description="Notes about the resolution")
    affected_fields: List[str] = Field(default_factory=list, description="Fields affected by the conflict")
    
    @validator('conflict_type')
    def validate_conflict_type(cls, v):
        """Validate conflict type."""
        valid_types = ['update_conflict', 'delete_conflict', 'create_conflict', 'merge_conflict']
        if v not in valid_types:
            raise ValueError(f'Conflict type must be one of: {", ".join(valid_types)}')
        return v
    
    @validator('resolution')
    def validate_resolution(cls, v, values):
        """Validate resolution based on conflict type."""
        if v is not None:
            valid_resolutions = ['use_local', 'use_remote', 'manual_resolution', 'merge']
            if v not in valid_resolutions:
                raise ValueError(f'Resolution must be one of: {", ".join(valid_resolutions)}')
            
            if v == 'manual_resolution' and not values.get('resolution_notes'):
                raise ValueError('Resolution notes are required for manual resolution')
        return v
    
    @validator('resolved_at')
    def validate_resolved_at(cls, v, values):
        """Validate resolved_at timestamp."""
        if v is not None and 'created_at' in values and v < values['created_at']:
            raise ValueError('resolved_at must be after created_at')
        return v
    
    @validator('affected_fields')
    def validate_affected_fields(cls, v, values):
        """Validate affected fields."""
        if not v and values.get('conflict_type') == 'update_conflict':
            raise ValueError('Affected fields are required for update conflicts')
        return v 