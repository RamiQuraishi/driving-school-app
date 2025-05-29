"""
MTO export schema for Ontario Driving School Manager.
Defines the structure for MTO data exports and validations.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import Field, validator
from .base import BaseSchema

class MTOExportSchema(BaseSchema):
    """Schema for MTO data exports."""
    
    school_id: str = Field(..., description="Unique identifier for the driving school")
    export_date: datetime = Field(default_factory=datetime.utcnow)
    export_type: str = Field(..., description="Type of MTO export (e.g., 'student_records', 'instructor_records')")
    status: str = Field(default="pending", description="Export status (pending, completed, failed)")
    file_path: Optional[str] = Field(None, description="Path to the exported file")
    record_count: Optional[int] = Field(None, description="Number of records in the export")
    error_message: Optional[str] = Field(None, description="Error message if export failed")
    validation_errors: List[str] = Field(default_factory=list, description="List of validation errors")
    
    @validator('export_type')
    def validate_export_type(cls, v):
        """Validate export type."""
        valid_types = ['student_records', 'instructor_records', 'vehicle_records', 'lesson_records']
        if v not in valid_types:
            raise ValueError(f'Export type must be one of: {", ".join(valid_types)}')
        return v
    
    @validator('status')
    def validate_status(cls, v):
        """Validate export status."""
        valid_statuses = ['pending', 'in_progress', 'completed', 'failed']
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v
    
    @validator('record_count')
    def validate_record_count(cls, v, values):
        """Validate record count based on status."""
        if values.get('status') == 'completed' and v is None:
            raise ValueError('Record count is required for completed exports')
        if v is not None and v < 0:
            raise ValueError('Record count cannot be negative')
        return v 