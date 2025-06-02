"""
Data Formatter Module

This module provides data formatting functionality for MTO data exchange.
It includes formatting for various data types and export formats.

Author: Rami Drive School
Date: 2024
"""

import logging
import json
import csv
from typing import Dict, Any, List, Optional, Union, Iterator
from datetime import datetime
import io
import re

logger = logging.getLogger(__name__)

class DataFormatter:
    """Data formatter."""
    
    def __init__(self):
        """Initialize data formatter."""
        self.date_format = "%Y-%m-%d"
        self.time_format = "%H:%M:%S"
        self.datetime_format = f"{self.date_format} {self.time_format}"
    
    def format_bde_data(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Format BDE data.
        
        Args:
            data: BDE data
            
        Returns:
            Formatted data
        """
        formatted = {}
        
        # Format instructor
        if "instructor" in data:
            formatted["instructor"] = self._format_instructor(data["instructor"])
        
        # Format students
        if "students" in data:
            formatted["students"] = [
                self._format_student(student)
                for student in data["students"]
            ]
        
        # Format courses
        if "courses" in data:
            formatted["courses"] = [
                self._format_course(course)
                for course in data["courses"]
            ]
        
        # Format lessons
        if "lessons" in data:
            formatted["lessons"] = [
                self._format_lesson(lesson)
                for lesson in data["lessons"]
            ]
        
        return formatted
    
    def format_license_data(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Format license data.
        
        Args:
            data: License data
            
        Returns:
            Formatted data
        """
        formatted = {}
        
        # Format student
        if "student" in data:
            formatted["student"] = self._format_student(data["student"])
        
        # Format license
        if "license" in data:
            formatted["license"] = self._format_license(data["license"])
        
        # Format progress
        if "progress" in data:
            formatted["progress"] = self._format_progress(data["progress"])
        
        return formatted
    
    def format_for_json(
        self,
        data: Dict[str, Any]
    ) -> str:
        """Format data for JSON.
        
        Args:
            data: Data to format
            
        Returns:
            JSON string
        """
        return json.dumps(data, indent=2)
    
    def format_for_csv(
        self,
        data: Dict[str, Any]
    ) -> str:
        """Format data for CSV.
        
        Args:
            data: Data to format
            
        Returns:
            CSV string
        """
        if not data:
            return ""
        
        # Flatten nested fields
        flattened = self._flatten_dict(data)
        
        # Write CSV
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=sorted(flattened.keys()))
        writer.writeheader()
        writer.writerow(flattened)
        
        return output.getvalue()
    
    def _format_instructor(
        self,
        instructor: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Format instructor data.
        
        Args:
            instructor: Instructor data
            
        Returns:
            Formatted data
        """
        return {
            "instructor_number": instructor.get("instructor_number", ""),
            "first_name": instructor.get("first_name", ""),
            "last_name": instructor.get("last_name", ""),
            "license_number": self._format_license_number(
                instructor.get("license_number", "")
            ),
            "license_expiry": self._format_date(
                instructor.get("license_expiry")
            ),
            "certification_date": self._format_date(
                instructor.get("certification_date")
            ),
            "certification_expiry": self._format_date(
                instructor.get("certification_expiry")
            ),
            "status": instructor.get("status", "ACTIVE")
        }
    
    def _format_student(
        self,
        student: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Format student data.
        
        Args:
            student: Student data
            
        Returns:
            Formatted data
        """
        return {
            "student_number": student.get("student_number", ""),
            "first_name": student.get("first_name", ""),
            "last_name": student.get("last_name", ""),
            "date_of_birth": self._format_date(
                student.get("date_of_birth")
            ),
            "address": student.get("address", ""),
            "city": student.get("city", ""),
            "province": student.get("province", ""),
            "postal_code": self._format_postal_code(
                student.get("postal_code", "")
            ),
            "phone": self._format_phone(
                student.get("phone", "")
            ),
            "email": student.get("email", ""),
            "license_number": self._format_license_number(
                student.get("license_number", "")
            ),
            "license_expiry": self._format_date(
                student.get("license_expiry")
            )
        }
    
    def _format_course(
        self,
        course: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Format course data.
        
        Args:
            course: Course data
            
        Returns:
            Formatted data
        """
        return {
            "course_number": course.get("course_number", ""),
            "start_date": self._format_date(course.get("start_date")),
            "end_date": self._format_date(course.get("end_date")),
            "instructor": self._format_instructor(course.get("instructor", {})),
            "students": [
                self._format_student(student)
                for student in course.get("students", [])
            ],
            "status": course.get("status", "ACTIVE"),
            "completion_date": self._format_date(
                course.get("completion_date")
            )
        }
    
    def _format_lesson(
        self,
        lesson: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Format lesson data.
        
        Args:
            lesson: Lesson data
            
        Returns:
            Formatted data
        """
        return {
            "lesson_number": lesson.get("lesson_number", 0),
            "course": self._format_course(lesson.get("course", {})),
            "student": self._format_student(lesson.get("student", {})),
            "instructor": self._format_instructor(lesson.get("instructor", {})),
            "date": self._format_date(lesson.get("date")),
            "start_time": self._format_time(lesson.get("start_time")),
            "end_time": self._format_time(lesson.get("end_time")),
            "lesson_type": lesson.get("lesson_type", ""),
            "status": lesson.get("status", "COMPLETED"),
            "notes": lesson.get("notes", "")
        }
    
    def _format_license(
        self,
        license_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Format license data.
        
        Args:
            license_data: License data
            
        Returns:
            Formatted data
        """
        return {
            "license_number": self._format_license_number(
                license_data.get("license_number", "")
            ),
            "level": license_data.get("level", ""),
            "issue_date": self._format_date(
                license_data.get("issue_date")
            ),
            "expiry_date": self._format_date(
                license_data.get("expiry_date")
            ),
            "status": license_data.get("status", "ACTIVE")
        }
    
    def _format_progress(
        self,
        progress: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Format progress data.
        
        Args:
            progress: Progress data
            
        Returns:
            Formatted data
        """
        return {
            "current_level": progress.get("current_level", ""),
            "start_date": self._format_date(progress.get("start_date")),
            "requirements": [
                self._format_requirement(req)
                for req in progress.get("requirements", [])
            ],
            "completed_requirements": progress.get("completed_requirements", {}),
            "next_test_date": self._format_date(
                progress.get("next_test_date")
            ),
            "notes": progress.get("notes", "")
        }
    
    def _format_requirement(
        self,
        requirement: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Format requirement data.
        
        Args:
            requirement: Requirement data
            
        Returns:
            Formatted data
        """
        return {
            "level": requirement.get("level", ""),
            "type": requirement.get("type", ""),
            "description": requirement.get("description", ""),
            "minimum_value": requirement.get("minimum_value", 0),
            "unit": requirement.get("unit", ""),
            "is_mandatory": requirement.get("is_mandatory", True),
            "notes": requirement.get("notes", "")
        }
    
    def _format_date(
        self,
        date: Optional[Union[str, datetime]]
    ) -> str:
        """Format date.
        
        Args:
            date: Date to format
            
        Returns:
            Formatted date string
        """
        if not date:
            return ""
        
        if isinstance(date, str):
            try:
                date = datetime.fromisoformat(date)
            except ValueError:
                return date
        
        if isinstance(date, datetime):
            return date.strftime(self.date_format)
        
        return str(date)
    
    def _format_time(
        self,
        time: Optional[Union[str, datetime]]
    ) -> str:
        """Format time.
        
        Args:
            time: Time to format
            
        Returns:
            Formatted time string
        """
        if not time:
            return ""
        
        if isinstance(time, str):
            try:
                time = datetime.fromisoformat(time)
            except ValueError:
                return time
        
        if isinstance(time, datetime):
            return time.strftime(self.time_format)
        
        return str(time)
    
    def _format_license_number(self, number: str) -> str:
        """Format license number.
        
        Args:
            number: License number
            
        Returns:
            Formatted license number
        """
        # Remove non-alphanumeric characters
        chars = re.sub(r"[^A-Z0-9]", "", number.upper())
        
        # Format as X####-#####-#####
        if len(chars) == 15:
            return f"{chars[0]}{chars[1:5]}-{chars[5:10]}-{chars[10:]}"
        
        return number
    
    def _format_postal_code(self, code: str) -> str:
        """Format postal code.
        
        Args:
            code: Postal code
            
        Returns:
            Formatted postal code
        """
        # Remove spaces and convert to uppercase
        code = code.replace(" ", "").upper()
        
        # Add space in the middle
        if len(code) == 6:
            return f"{code[:3]} {code[3:]}"
        
        return code
    
    def _format_phone(self, phone: str) -> str:
        """Format phone number.
        
        Args:
            phone: Phone number
            
        Returns:
            Formatted phone number
        """
        # Remove non-digit characters
        digits = re.sub(r"\D", "", phone)
        
        # Format as XXX-XXX-XXXX
        if len(digits) == 10:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        
        return phone
    
    def _flatten_dict(
        self,
        data: Dict[str, Any],
        prefix: str = ""
    ) -> Dict[str, Any]:
        """Flatten nested dictionary.
        
        Args:
            data: Dictionary to flatten
            prefix: Key prefix
            
        Returns:
            Flattened dictionary
        """
        flattened = {}
        
        for key, value in data.items():
            new_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                flattened.update(
                    self._flatten_dict(value, new_key)
                )
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        flattened.update(
                            self._flatten_dict(
                                item,
                                f"{new_key}[{i}]"
                            )
                        )
                    else:
                        flattened[f"{new_key}[{i}]"] = item
            else:
                flattened[new_key] = value
        
        return flattened 