"""
BDE Processor Module

This module processes BDE (Beginner Driver Education) data for MTO integration.
It includes validation, formatting, and submission functionality.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import re
from .data_formatter import DataFormatter

logger = logging.getLogger(__name__)

class BDEProcessor:
    """BDE processor."""
    
    def __init__(self):
        """Initialize BDE processor."""
        self.formatter = DataFormatter()
    
    def process_instructor(
        self,
        instructor: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process instructor data.
        
        Args:
            instructor: Instructor data
            
        Returns:
            Processed data
        """
        # Validate instructor data
        self._validate_instructor(instructor)
        
        # Format instructor data
        return self.formatter._format_instructor(instructor)
    
    def process_student(
        self,
        student: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process student data.
        
        Args:
            student: Student data
            
        Returns:
            Processed data
        """
        # Validate student data
        self._validate_student(student)
        
        # Format student data
        return self.formatter._format_student(student)
    
    def process_course(
        self,
        course: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process course data.
        
        Args:
            course: Course data
            
        Returns:
            Processed data
        """
        # Validate course data
        self._validate_course(course)
        
        # Format course data
        return self.formatter._format_course(course)
    
    def process_lesson(
        self,
        lesson: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process lesson data.
        
        Args:
            lesson: Lesson data
            
        Returns:
            Processed data
        """
        # Validate lesson data
        self._validate_lesson(lesson)
        
        # Format lesson data
        return self.formatter._format_lesson(lesson)
    
    def process_bde_data(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process BDE data.
        
        Args:
            data: BDE data
            
        Returns:
            Processed data
        """
        # Validate BDE data
        self._validate_bde_data(data)
        
        # Format BDE data
        return self.formatter.format_bde_data(data)
    
    def _validate_instructor(
        self,
        instructor: Dict[str, Any]
    ) -> None:
        """Validate instructor data.
        
        Args:
            instructor: Instructor data
            
        Raises:
            ValueError: If data is invalid
        """
        # Check required fields
        required_fields = [
            "instructor_number",
            "first_name",
            "last_name",
            "license_number",
            "license_expiry",
            "certification_date",
            "certification_expiry"
        ]
        
        for field in required_fields:
            if not instructor.get(field):
                raise ValueError(f"Missing required field: {field}")
        
        # Validate instructor number
        if not re.match(r"^\d{6}$", str(instructor["instructor_number"])):
            raise ValueError("Invalid instructor number")
        
        # Validate license number
        if not re.match(r"^[A-Z]\d{4}-\d{5}-\d{5}$", instructor["license_number"]):
            raise ValueError("Invalid license number")
        
        # Validate dates
        for date_field in ["license_expiry", "certification_date", "certification_expiry"]:
            try:
                datetime.fromisoformat(instructor[date_field])
            except ValueError:
                raise ValueError(f"Invalid date format: {date_field}")
    
    def _validate_student(
        self,
        student: Dict[str, Any]
    ) -> None:
        """Validate student data.
        
        Args:
            student: Student data
            
        Raises:
            ValueError: If data is invalid
        """
        # Check required fields
        required_fields = [
            "student_number",
            "first_name",
            "last_name",
            "date_of_birth",
            "address",
            "city",
            "province",
            "postal_code",
            "phone",
            "email"
        ]
        
        for field in required_fields:
            if not student.get(field):
                raise ValueError(f"Missing required field: {field}")
        
        # Validate student number
        if not re.match(r"^\d{8}$", str(student["student_number"])):
            raise ValueError("Invalid student number")
        
        # Validate date of birth
        try:
            dob = datetime.fromisoformat(student["date_of_birth"])
            if dob > datetime.now():
                raise ValueError("Date of birth cannot be in the future")
        except ValueError:
            raise ValueError("Invalid date of birth format")
        
        # Validate postal code
        if not re.match(r"^[A-Z]\d[A-Z] \d[A-Z]\d$", student["postal_code"]):
            raise ValueError("Invalid postal code")
        
        # Validate phone
        if not re.match(r"^\d{3}-\d{3}-\d{4}$", student["phone"]):
            raise ValueError("Invalid phone number")
        
        # Validate email
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", student["email"]):
            raise ValueError("Invalid email address")
    
    def _validate_course(
        self,
        course: Dict[str, Any]
    ) -> None:
        """Validate course data.
        
        Args:
            course: Course data
            
        Raises:
            ValueError: If data is invalid
        """
        # Check required fields
        required_fields = [
            "course_number",
            "start_date",
            "end_date",
            "instructor",
            "students"
        ]
        
        for field in required_fields:
            if not course.get(field):
                raise ValueError(f"Missing required field: {field}")
        
        # Validate course number
        if not re.match(r"^\d{6}$", str(course["course_number"])):
            raise ValueError("Invalid course number")
        
        # Validate dates
        try:
            start_date = datetime.fromisoformat(course["start_date"])
            end_date = datetime.fromisoformat(course["end_date"])
            
            if start_date >= end_date:
                raise ValueError("Start date must be before end date")
        except ValueError:
            raise ValueError("Invalid date format")
        
        # Validate instructor
        self._validate_instructor(course["instructor"])
        
        # Validate students
        if not isinstance(course["students"], list):
            raise ValueError("Students must be a list")
        
        if not course["students"]:
            raise ValueError("Course must have at least one student")
        
        for student in course["students"]:
            self._validate_student(student)
    
    def _validate_lesson(
        self,
        lesson: Dict[str, Any]
    ) -> None:
        """Validate lesson data.
        
        Args:
            lesson: Lesson data
            
        Raises:
            ValueError: If data is invalid
        """
        # Check required fields
        required_fields = [
            "lesson_number",
            "course",
            "student",
            "instructor",
            "date",
            "start_time",
            "end_time",
            "lesson_type"
        ]
        
        for field in required_fields:
            if not lesson.get(field):
                raise ValueError(f"Missing required field: {field}")
        
        # Validate lesson number
        if not isinstance(lesson["lesson_number"], int):
            raise ValueError("Lesson number must be an integer")
        
        # Validate course
        self._validate_course(lesson["course"])
        
        # Validate student
        self._validate_student(lesson["student"])
        
        # Validate instructor
        self._validate_instructor(lesson["instructor"])
        
        # Validate date
        try:
            datetime.fromisoformat(lesson["date"])
        except ValueError:
            raise ValueError("Invalid date format")
        
        # Validate times
        try:
            start_time = datetime.fromisoformat(lesson["start_time"])
            end_time = datetime.fromisoformat(lesson["end_time"])
            
            if start_time >= end_time:
                raise ValueError("Start time must be before end time")
        except ValueError:
            raise ValueError("Invalid time format")
        
        # Validate lesson type
        valid_types = ["CLASSROOM", "IN_CAR", "SIMULATOR"]
        if lesson["lesson_type"] not in valid_types:
            raise ValueError(f"Invalid lesson type. Must be one of: {valid_types}")
    
    def _validate_bde_data(
        self,
        data: Dict[str, Any]
    ) -> None:
        """Validate BDE data.
        
        Args:
            data: BDE data
            
        Raises:
            ValueError: If data is invalid
        """
        # Check required fields
        required_fields = ["instructor", "students", "courses", "lessons"]
        
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"Missing required field: {field}")
        
        # Validate instructor
        self._validate_instructor(data["instructor"])
        
        # Validate students
        if not isinstance(data["students"], list):
            raise ValueError("Students must be a list")
        
        if not data["students"]:
            raise ValueError("Must have at least one student")
        
        for student in data["students"]:
            self._validate_student(student)
        
        # Validate courses
        if not isinstance(data["courses"], list):
            raise ValueError("Courses must be a list")
        
        if not data["courses"]:
            raise ValueError("Must have at least one course")
        
        for course in data["courses"]:
            self._validate_course(course)
        
        # Validate lessons
        if not isinstance(data["lessons"], list):
            raise ValueError("Lessons must be a list")
        
        if not data["lessons"]:
            raise ValueError("Must have at least one lesson")
        
        for lesson in data["lessons"]:
            self._validate_lesson(lesson) 