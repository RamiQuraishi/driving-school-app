"""
User Model

This module provides the User model for database operations.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
import bcrypt

logger = logging.getLogger(__name__)

Base = declarative_base()

class UserRole(enum.Enum):
    """User role."""
    ADMIN = "admin"
    INSTRUCTOR = "instructor"
    STUDENT = "student"

class User(Base):
    """User model."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(100), unique=True)
    reset_token = Column(String(100), unique=True)
    reset_token_expires = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    school_id = Column(Integer, ForeignKey("schools.id"))
    school = relationship("School", back_populates="users")
    
    def __init__(
        self,
        username: str,
        email: str,
        password_hash: str,
        first_name: str,
        last_name: str,
        role: UserRole,
        school_id: Optional[int] = None
    ):
        """Initialize user.
        
        Args:
            username: Username
            email: Email
            password_hash: Password hash
            first_name: First name
            last_name: Last name
            role: User role
            school_id: School ID
        """
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.school_id = school_id
    
    def __repr__(self) -> str:
        """Get string representation.
        
        Returns:
            String representation
        """
        return f"<User {self.username}>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role.value,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "school_id": self.school_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has permission.
        
        Args:
            permission: Permission to check
            
        Returns:
            True if user has permission, False otherwise
        """
        if self.role == UserRole.ADMIN:
            return True
        
        if self.role == UserRole.INSTRUCTOR:
            return permission in [
                "view_students",
                "edit_students",
                "view_schedule",
                "edit_schedule",
                "view_vehicles",
                "edit_vehicles"
            ]
        
        if self.role == UserRole.STUDENT:
            return permission in [
                "view_schedule",
                "view_vehicles"
            ]
        
        return False
    
    def set_password(self, password: str) -> None:
        """Set password.
        
        Args:
            password: Password
        """
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode(), salt).decode()
    
    def check_password(self, password: str) -> bool:
        """Check password.
        
        Args:
            password: Password
            
        Returns:
            True if password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
    
    def get_full_name(self) -> str:
        """Get full name.
        
        Returns:
            Full name
        """
        return f"{self.first_name} {self.last_name}"
    
    def get_full_address(self) -> Optional[str]:
        """Get full address.
        
        Returns:
            Full address if available, None otherwise
        """
        if not all([self.address, self.city, self.province, self.postal_code]):
            return None
        
        return f"{self.address}, {self.city}, {self.province} {self.postal_code}" 