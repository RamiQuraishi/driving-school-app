"""
BDE curriculum schema for Ontario Driving School Manager.
Defines the structure for BDE (Beginner Driver Education) curriculum data.
"""

from datetime import datetime
from typing import List, Optional, Dict
from pydantic import Field, validator
from .base import BaseSchema

class BDECurriculumSchema(BaseSchema):
    """Schema for BDE curriculum data."""
    
    curriculum_id: str = Field(..., description="Unique identifier for the curriculum")
    name: str = Field(..., description="Name of the curriculum")
    version: str = Field(..., description="Version of the curriculum")
    effective_date: datetime = Field(..., description="Date when the curriculum becomes effective")
    expiry_date: Optional[datetime] = Field(None, description="Date when the curriculum expires")
    total_hours: float = Field(..., description="Total hours required for the curriculum")
    in_class_hours: float = Field(..., description="Required in-class hours")
    in_car_hours: float = Field(..., description="Required in-car hours")
    modules: List[Dict] = Field(default_factory=list, description="List of curriculum modules")
    requirements: List[str] = Field(default_factory=list, description="List of curriculum requirements")
    status: str = Field(default="active", description="Status of the curriculum")
    
    @validator('total_hours')
    def validate_total_hours(cls, v, values):
        """Validate total hours matches in-class and in-car hours."""
        if 'in_class_hours' in values and 'in_car_hours' in values:
            expected_total = values['in_class_hours'] + values['in_car_hours']
            if abs(v - expected_total) > 0.01:  # Allow for small floating point differences
                raise ValueError(f'Total hours ({v}) must equal in-class hours ({values["in_class_hours"]}) plus in-car hours ({values["in_car_hours"]})')
        return v
    
    @validator('expiry_date')
    def validate_expiry_date(cls, v, values):
        """Validate expiry date is after effective date."""
        if v and 'effective_date' in values and v <= values['effective_date']:
            raise ValueError('Expiry date must be after effective date')
        return v
    
    @validator('status')
    def validate_status(cls, v):
        """Validate curriculum status."""
        valid_statuses = ['active', 'inactive', 'pending', 'expired']
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v
    
    @validator('modules')
    def validate_modules(cls, v):
        """Validate curriculum modules."""
        if not v:
            raise ValueError('At least one module is required')
        
        required_fields = ['name', 'hours', 'type', 'order']
        for module in v:
            missing_fields = [field for field in required_fields if field not in module]
            if missing_fields:
                raise ValueError(f'Module missing required fields: {", ".join(missing_fields)}')
            
            if module['hours'] <= 0:
                raise ValueError(f'Module hours must be greater than 0: {module["name"]}')
            
            if module['type'] not in ['in_class', 'in_car']:
                raise ValueError(f'Invalid module type: {module["type"]}')
        
        return v 