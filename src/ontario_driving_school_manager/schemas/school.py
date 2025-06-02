"""
School schema module defining Pydantic models for school data validation.
This module contains models for school creation, updates, and responses.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class SchoolBase(BaseModel):
    """Base school model with common attributes."""
    name: str = Field(..., min_length=1, max_length=100)
    address: str = Field(..., min_length=1, max_length=200)
    phone: str = Field(..., min_length=10, max_length=15)
    email: str = Field(..., min_length=1, max_length=100)
    is_active: bool = True
    description: Optional[str] = None

class SchoolCreate(SchoolBase):
    """Model for creating a new school."""
    pass

class SchoolUpdate(BaseModel):
    """Model for updating school information."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    address: Optional[str] = Field(None, min_length=1, max_length=200)
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    email: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None
    description: Optional[str] = None

class SchoolInDB(SchoolBase):
    """Model for school data in database."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True

class SchoolResponse(SchoolBase):
    """Model for school response data."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True

class SchoolList(BaseModel):
    """Model for list of schools."""
    schools: List[SchoolResponse]
    total: int
    page: int
    size: int 