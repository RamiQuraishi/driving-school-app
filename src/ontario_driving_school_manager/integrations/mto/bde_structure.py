"""
BDE Structure Module

This module defines the structure and requirements for BDE (Beginner Driver Education)
data exchange with the MTO. It includes data models and validation rules.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import re

logger = logging.getLogger(__name__)

@dataclass
class BDEInstructor:
    """BDE instructor information."""
    instructor_number: str
    first_name: str
    last_name: str
    license_number: str
    license_expiry: datetime
    certification_date: datetime
    certification_expiry: datetime
    status: str = "ACTIVE"

@dataclass
class BDEStudent:
    """BDE student information."""
    student_number: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    address: str
    city: str
    province: str
    postal_code: str
    phone: str
    email: Optional[str] = None
    license_number: Optional[str] = None
    license_expiry: Optional[datetime] = None

@dataclass
class BDECourse:
    """BDE course information."""
    course_number: str
    start_date: datetime
    end_date: datetime
    instructor: BDEInstructor
    students: List[BDEStudent] = field(default_factory=list)
    status: str = "ACTIVE"
    completion_date: Optional[datetime] = None

@dataclass
class BDELesson:
    """BDE lesson information."""
    lesson_number: int
    course: BDECourse
    student: BDEStudent
    instructor: BDEInstructor
    date: datetime
    start_time: datetime
    end_time: datetime
    lesson_type: str  # CLASSROOM, IN_CAR, SIMULATOR
    status: str = "COMPLETED"
    notes: Optional[str] = None

class BDEStructure:
    """BDE structure manager."""
    
    def __init__(self):
        """Initialize BDE structure manager."""
        self.required_fields = {
            "instructor": [
                "instructor_number",
                "first_name",
                "last_name",
                "license_number",
                "license_expiry",
                "certification_date",
                "certification_expiry"
            ],
            "student": [
                "student_number",
                "first_name",
                "last_name",
                "date_of_birth",
                "address",
                "city",
                "province",
                "postal_code",
                "phone"
            ],
            "course": [
                "course_number",
                "start_date",
                "end_date",
                "instructor",
                "students"
            ],
            "lesson": [
                "lesson_number",
                "course",
                "student",
                "instructor",
                "date",
                "start_time",
                "end_time",
                "lesson_type"
            ]
        }
        
        self.field_validators = {
            "instructor_number": self._validate_instructor_number,
            "license_number": self._validate_license_number,
            "postal_code": self._validate_postal_code,
            "phone": self._validate_phone,
            "email": self._validate_email
        }
    
    def validate_instructor(self, instructor: BDEInstructor) -> List[str]:
        """Validate instructor data.
        
        Args:
            instructor: Instructor data
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Check required fields
        for field in self.required_fields["instructor"]:
            if not getattr(instructor, field, None):
                errors.append(f"Missing required field: {field}")
        
        # Validate fields
        for field, validator in self.field_validators.items():
            if hasattr(instructor, field):
                value = getattr(instructor, field)
                if not validator(value):
                    errors.append(f"Invalid {field}: {value}")
        
        return errors
    
    def validate_student(self, student: BDEStudent) -> List[str]:
        """Validate student data.
        
        Args:
            student: Student data
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Check required fields
        for field in self.required_fields["student"]:
            if not getattr(student, field, None):
                errors.append(f"Missing required field: {field}")
        
        # Validate fields
        for field, validator in self.field_validators.items():
            if hasattr(student, field):
                value = getattr(student, field)
                if not validator(value):
                    errors.append(f"Invalid {field}: {value}")
        
        return errors
    
    def validate_course(self, course: BDECourse) -> List[str]:
        """Validate course data.
        
        Args:
            course: Course data
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Check required fields
        for field in self.required_fields["course"]:
            if not getattr(course, field, None):
                errors.append(f"Missing required field: {field}")
        
        # Validate instructor
        if course.instructor:
            errors.extend(self.validate_instructor(course.instructor))
        
        # Validate students
        if course.students:
            for student in course.students:
                errors.extend(self.validate_student(student))
        
        return errors
    
    def validate_lesson(self, lesson: BDELesson) -> List[str]:
        """Validate lesson data.
        
        Args:
            lesson: Lesson data
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Check required fields
        for field in self.required_fields["lesson"]:
            if not getattr(lesson, field, None):
                errors.append(f"Missing required field: {field}")
        
        # Validate course
        if lesson.course:
            errors.extend(self.validate_course(lesson.course))
        
        # Validate student
        if lesson.student:
            errors.extend(self.validate_student(lesson.student))
        
        # Validate instructor
        if lesson.instructor:
            errors.extend(self.validate_instructor(lesson.instructor))
        
        return errors
    
    def _validate_instructor_number(self, number: str) -> bool:
        """Validate instructor number.
        
        Args:
            number: Instructor number
            
        Returns:
            Whether number is valid
        """
        return bool(re.match(r"^[A-Z]\d{6}$", number))
    
    def _validate_license_number(self, number: str) -> bool:
        """Validate license number.
        
        Args:
            number: License number
            
        Returns:
            Whether number is valid
        """
        return bool(re.match(r"^[A-Z]\d{4}-\d{5}-\d{5}$", number))
    
    def _validate_postal_code(self, code: str) -> bool:
        """Validate postal code.
        
        Args:
            code: Postal code
            
        Returns:
            Whether code is valid
        """
        return bool(re.match(r"^[A-Z]\d[A-Z]\s?\d[A-Z]\d$", code))
    
    def _validate_phone(self, phone: str) -> bool:
        """Validate phone number.
        
        Args:
            phone: Phone number
            
        Returns:
            Whether number is valid
        """
        return bool(re.match(r"^\d{3}[-.]?\d{3}[-.]?\d{4}$", phone))
    
    def _validate_email(self, email: str) -> bool:
        """Validate email address.
        
        Args:
            email: Email address
            
        Returns:
            Whether email is valid
        """
        return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)) 