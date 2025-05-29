"""Instructor insurance models for managing insurance policies."""

from datetime import date
from typing import Optional

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel

class InsurancePolicy(BaseModel):
    """Insurance policy model.
    
    This model manages:
    - Insurance policies
    - Policy coverage
    - Policy expiration
    """
    
    policy_number = Column(String(50), nullable=False, unique=True)
    provider = Column(String(100), nullable=False)
    coverage_type = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    coverage_amount = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    vehicle_insurance = relationship("VehicleInsurance", back_populates="policy")
    
    def is_valid(self) -> bool:
        """Check if policy is valid.
        
        Returns:
            bool: True if valid
        """
        if not self.is_active:
            return False
        
        today = date.today()
        return self.start_date <= today <= self.end_date
    
    def days_until_expiry(self) -> int:
        """Get days until policy expiry.
        
        Returns:
            int: Days until expiry
        """
        return (self.end_date - date.today()).days

class VehicleInsurance(BaseModel):
    """Vehicle insurance model."""
    
    vehicle_id = Column(Integer, ForeignKey("vehicle.id"), nullable=False)
    policy_id = Column(Integer, ForeignKey("insurancepolicy.id"), nullable=False)
    
    # Relationships
    vehicle = relationship("Vehicle")
    policy = relationship("InsurancePolicy", back_populates="vehicle_insurance")
    
    def is_valid(self) -> bool:
        """Check if insurance is valid.
        
        Returns:
            bool: True if valid
        """
        return self.policy.is_valid() 