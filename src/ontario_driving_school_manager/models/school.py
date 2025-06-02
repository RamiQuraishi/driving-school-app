"""
School Model

This module provides the School model for database operations.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base = declarative_base()

class School(Base):
    """School model."""
    
    __tablename__ = "schools"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    license_number = Column(String(50), unique=True, nullable=False)
    address = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    province = Column(String(50), nullable=False)
    postal_code = Column(String(10), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    website = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="school")
    vehicles = relationship("Vehicle", back_populates="school")
    schedules = relationship("Schedule", back_populates="school")
    
    def __init__(
        self,
        name: str,
        license_number: str,
        address: str,
        city: str,
        province: str,
        postal_code: str,
        phone: str,
        email: str,
        website: Optional[str] = None
    ):
        """Initialize school.
        
        Args:
            name: School name
            license_number: License number
            address: Address
            city: City
            province: Province
            postal_code: Postal code
            phone: Phone number
            email: Email
            website: Website
        """
        self.name = name
        self.license_number = license_number
        self.address = address
        self.city = city
        self.province = province
        self.postal_code = postal_code
        self.phone = phone
        self.email = email
        self.website = website
    
    def __repr__(self) -> str:
        """Get string representation.
        
        Returns:
            String representation
        """
        return f"<School {self.name}>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "id": self.id,
            "name": self.name,
            "license_number": self.license_number,
            "address": self.address,
            "city": self.city,
            "province": self.province,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "email": self.email,
            "website": self.website,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    def get_full_address(self) -> str:
        """Get full address.
        
        Returns:
            Full address
        """
        return f"{self.address}, {self.city}, {self.province} {self.postal_code}" 