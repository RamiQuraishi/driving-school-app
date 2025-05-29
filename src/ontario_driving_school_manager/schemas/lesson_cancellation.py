"""
Lesson cancellation schema for Ontario Driving School Manager.
Defines the structure for lesson cancellation data and validations.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import Field, validator
from .base import BaseSchema

class LessonCancellationSchema(BaseSchema):
    """Schema for lesson cancellation data."""
    
    lesson_id: str = Field(..., description="ID of the cancelled lesson")
    student_id: str = Field(..., description="ID of the student")
    instructor_id: str = Field(..., description="ID of the instructor")
    cancellation_date: datetime = Field(..., description="Date and time of cancellation")
    original_lesson_date: datetime = Field(..., description="Original date and time of the lesson")
    reason: str = Field(..., description="Reason for cancellation")
    cancellation_type: str = Field(..., description="Type of cancellation")
    refund_amount: Optional[float] = Field(None, description="Refund amount if applicable")
    refund_status: Optional[str] = Field(None, description="Status of the refund")
    rescheduled_lesson_id: Optional[str] = Field(None, description="ID of the rescheduled lesson if applicable")
    notes: Optional[str] = Field(None, description="Additional notes about the cancellation")
    affected_parties: List[str] = Field(default_factory=list, description="List of parties affected by the cancellation")
    
    @validator('cancellation_date')
    def validate_cancellation_date(cls, v, values):
        """Validate cancellation date is before original lesson date."""
        if 'original_lesson_date' in values and v >= values['original_lesson_date']:
            raise ValueError('Cancellation date must be before original lesson date')
        return v
    
    @validator('cancellation_type')
    def validate_cancellation_type(cls, v):
        """Validate cancellation type."""
        valid_types = ['student_initiated', 'instructor_initiated', 'school_initiated', 'emergency', 'weather']
        if v not in valid_types:
            raise ValueError(f'Cancellation type must be one of: {", ".join(valid_types)}')
        return v
    
    @validator('refund_status')
    def validate_refund_status(cls, v, values):
        """Validate refund status."""
        if v is not None:
            valid_statuses = ['pending', 'approved', 'processed', 'rejected']
            if v not in valid_statuses:
                raise ValueError(f'Refund status must be one of: {", ".join(valid_statuses)}')
            
            if v in ['approved', 'processed'] and 'refund_amount' not in values:
                raise ValueError('Refund amount is required for approved or processed refunds')
        return v
    
    @validator('refund_amount')
    def validate_refund_amount(cls, v, values):
        """Validate refund amount."""
        if v is not None:
            if v < 0:
                raise ValueError('Refund amount cannot be negative')
            if v > 1000:  # Arbitrary maximum refund amount
                raise ValueError('Refund amount cannot exceed $1000')
        return v
    
    @validator('affected_parties')
    def validate_affected_parties(cls, v):
        """Validate affected parties."""
        valid_parties = ['student', 'instructor', 'school', 'vehicle']
        invalid_parties = [party for party in v if party not in valid_parties]
        if invalid_parties:
            raise ValueError(f'Invalid affected parties: {", ".join(invalid_parties)}')
        return v 