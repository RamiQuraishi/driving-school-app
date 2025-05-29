"""MTO compliance models for tracking regulatory requirements."""

from datetime import date
from typing import Optional

from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship

from .base import BaseModel

class MTOCompliance(BaseModel):
    """MTO compliance record model.
    
    This model tracks compliance records for:
    - Instructor certifications
    - Vehicle inspections
    - School licensing
    - Other regulatory requirements
    """
    
    record_type = Column(String(50), nullable=False)
    record_date = Column(Date, nullable=False)
    expiry_date = Column(Date)
    status = Column(String(20), nullable=False)
    notes = Column(Text)
    
    # Relationships
    instructor_compliance = relationship("InstructorCompliance", back_populates="compliance")
    vehicle_compliance = relationship("VehicleCompliance", back_populates="compliance")
    school_compliance = relationship("SchoolCompliance", back_populates="compliance")
    
    def is_expired(self) -> bool:
        """Check if compliance record is expired.
        
        Returns:
            bool: True if expired
        """
        if not self.expiry_date:
            return False
        return self.expiry_date < date.today()
    
    def is_valid(self) -> bool:
        """Check if compliance record is valid.
        
        Returns:
            bool: True if valid
        """
        return self.status == "valid" and not self.is_expired()

class InstructorCompliance(BaseModel):
    """Instructor compliance record model."""
    
    instructor_id = Column(Integer, ForeignKey("instructor.id"), nullable=False)
    compliance_id = Column(Integer, ForeignKey("mtocompliance.id"), nullable=False)
    status = Column(String(20), nullable=False)
    verification_date = Column(Date)
    verified_by = Column(Integer, ForeignKey("user.id"))
    notes = Column(Text)
    
    # Relationships
    compliance = relationship("MTOCompliance", back_populates="instructor_compliance")
    instructor = relationship("Instructor")
    verifier = relationship("User")

class VehicleCompliance(BaseModel):
    """Vehicle compliance record model."""
    
    vehicle_id = Column(Integer, ForeignKey("vehicle.id"), nullable=False)
    compliance_id = Column(Integer, ForeignKey("mtocompliance.id"), nullable=False)
    status = Column(String(20), nullable=False)
    verification_date = Column(Date)
    verified_by = Column(Integer, ForeignKey("user.id"))
    notes = Column(Text)
    
    # Relationships
    compliance = relationship("MTOCompliance", back_populates="vehicle_compliance")
    vehicle = relationship("Vehicle")
    verifier = relationship("User")

class SchoolCompliance(BaseModel):
    """School compliance record model."""
    
    compliance_id = Column(Integer, ForeignKey("mtocompliance.id"), nullable=False)
    status = Column(String(20), nullable=False)
    verification_date = Column(Date)
    verified_by = Column(Integer, ForeignKey("user.id"))
    notes = Column(Text)
    
    # Relationships
    compliance = relationship("MTOCompliance", back_populates="school_compliance")
    verifier = relationship("User") 