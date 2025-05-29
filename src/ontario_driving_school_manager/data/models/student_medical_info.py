"""Student medical information models for managing medical records."""

from datetime import date
from typing import Optional

from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel

class MedicalCertificate(BaseModel):
    """Medical certificate model.
    
    This model manages:
    - Medical certificates
    - Certificate expiration
    - Certificate verification
    """
    
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    certificate_number = Column(String(50), nullable=False)
    issue_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)
    issuing_authority = Column(String(100), nullable=False)
    file_path = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    student = relationship("Student")
    
    def is_valid(self) -> bool:
        """Check if certificate is valid.
        
        Returns:
            bool: True if valid
        """
        if not self.is_active:
            return False
        
        today = date.today()
        return self.issue_date <= today <= self.expiry_date
    
    def days_until_expiry(self) -> int:
        """Get days until certificate expiry.
        
        Returns:
            int: Days until expiry
        """
        return (self.expiry_date - date.today()).days

class MedicalCondition(BaseModel):
    """Medical condition model."""
    
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    condition_type = Column(String(50), nullable=False)
    description = Column(Text)
    severity = Column(String(20), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    student = relationship("Student")
    
    def requires_accommodation(self) -> bool:
        """Check if condition requires accommodation.
        
        Returns:
            bool: True if requires accommodation
        """
        return self.severity in ["high", "critical"]
    
    def get_accommodation_notes(self) -> Optional[str]:
        """Get accommodation notes.
        
        Returns:
            Optional[str]: Accommodation notes
        """
        if not self.requires_accommodation():
            return None
        
        return f"Medical condition: {self.condition_type}\nSeverity: {self.severity}\nNotes: {self.description}" 