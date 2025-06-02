"""
Role Model

This module defines the Role model for managing user roles.

Author: Rami Drive School
Date: 2024
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, List

from .base import Base

# Association table for role-permission relationship
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True)
)

class Role(Base):
    """Role model."""
    
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    users = relationship("User", back_populates="role")
    
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        is_active: bool = True
    ):
        """Initialize role.
        
        Args:
            name: Role name
            description: Role description
            is_active: Whether role is active
        """
        self.name = name
        self.description = description
        self.is_active = is_active
    
    def __repr__(self) -> str:
        """Get string representation.
        
        Returns:
            String representation
        """
        return f"<Role {self.name}>"
    
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
            "is_active": self.is_active,
            "permissions": [p.to_dict() for p in self.permissions]
        }
    
    def has_permission(self, permission_name: str) -> bool:
        """Check if role has permission.
        
        Args:
            permission_name: Permission name
            
        Returns:
            True if role has permission, False otherwise
        """
        return any(p.name == permission_name for p in self.permissions)
    
    def add_permission(self, permission: "Permission") -> None:
        """Add permission to role.
        
        Args:
            permission: Permission to add
        """
        if permission not in self.permissions:
            self.permissions.append(permission)
    
    def remove_permission(self, permission: "Permission") -> None:
        """Remove permission from role.
        
        Args:
            permission: Permission to remove
        """
        if permission in self.permissions:
            self.permissions.remove(permission) 