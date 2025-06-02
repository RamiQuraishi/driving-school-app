"""
Permission Model

This module defines the Permission model for managing user permissions.

Author: Rami Drive School
Date: 2024
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, List

from .base import Base

class Permission(Base):
    """Permission model."""
    
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")
    
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        is_active: bool = True
    ):
        """Initialize permission.
        
        Args:
            name: Permission name
            description: Permission description
            is_active: Whether permission is active
        """
        self.name = name
        self.description = description
        self.is_active = is_active
    
    def __repr__(self) -> str:
        """Get string representation.
        
        Returns:
            String representation
        """
        return f"<Permission {self.name}>"
    
    def to_dict(self) -> dict:
        """Convert to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active
        } 