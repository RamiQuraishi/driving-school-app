"""
User schema module defining Pydantic models for user data validation.
This module contains models for user creation, updates, and responses.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    """Base user model with common attributes."""
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """Model for creating a new user."""
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    """Model for updating user information."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)

class UserInDB(UserBase):
    """Model for user data in database."""
    id: int
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True

class UserResponse(UserBase):
    """Model for user response data."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True

class UserList(BaseModel):
    """Model for list of users."""
    users: List[UserResponse]
    total: int
    page: int
    size: int 