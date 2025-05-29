"""
Shared Validation

This package provides shared validation rules for both Python and TypeScript.
It ensures consistent validation across the application.

Author: Rami Drive School
Date: 2024
"""

from .student_validation import validate_student
from .instructor_validation import validate_instructor
from .lesson_validation import validate_lesson
from .payment_validation import validate_payment

__all__ = [
    'validate_student',
    'validate_instructor',
    'validate_lesson',
    'validate_payment'
] 