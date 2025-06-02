"""
Role schema module defining Pydantic models for role data validation.
This module contains models for role creation, updates, and responses.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum

class Permission(str, Enum):
    """Enum for user permissions."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

class RoleBase(BaseModel):
    """Base role model with common attributes."""
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    permissions: List[Permission] = Field(default_factory=list)
    is_active: bool = True

class RoleCreate(RoleBase):
    """Model for creating a new role."""
    pass

class RoleUpdate(BaseModel):
    """Model for updating role information."""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    permissions: Optional[List[Permission]] = None
    is_active: Optional[bool] = None

class RoleInDB(RoleBase):
    """Model for role data in database."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True

class RoleResponse(RoleBase):
    """Model for role response data."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True

class RoleList(BaseModel):
    """Model for list of roles."""
    roles: List[RoleResponse]
    total: int
    page: int
    size: int 