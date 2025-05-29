"""
Base schema class for Ontario Driving School Manager.
Provides common functionality and validation for all schemas.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, validator
import uuid

class BaseSchema(BaseModel):
    """Base schema with common fields and validation."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    version: int = Field(default=1)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @validator('updated_at')
    def update_timestamp(cls, v, values):
        """Ensure updated_at is always after created_at."""
        if 'created_at' in values and v < values['created_at']:
            raise ValueError('updated_at must be after created_at')
        return v

    class Config:
        """Pydantic model configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            uuid.UUID: str
        }
        validate_assignment = True
        arbitrary_types_allowed = True 