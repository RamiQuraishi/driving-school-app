"""
Shared Types

This package provides shared type definitions for both Python and TypeScript.
It ensures consistent types across the application.

Author: Rami Drive School
Date: 2024
"""

from typing import TypedDict, Optional, List, Dict, Any
from datetime import datetime

class Student(TypedDict):
    """Student type definition."""
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    date_of_birth: datetime
    license_number: Optional[str]
    medical_info: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

class Instructor(TypedDict):
    """Instructor type definition."""
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    license_number: str
    insurance_info: Dict[str, Any]
    availability: List[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

class Lesson(TypedDict):
    """Lesson type definition."""
    id: str
    student_id: str
    instructor_id: str
    start_time: datetime
    end_time: datetime
    status: str
    type: str
    location: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

class Payment(TypedDict):
    """Payment type definition."""
    id: str
    student_id: str
    amount: float
    currency: str
    status: str
    method: str
    reference: Optional[str]
    created_at: datetime
    updated_at: datetime

__all__ = [
    'Student',
    'Instructor',
    'Lesson',
    'Payment'
] 