"""
MTO Portal Guide Module

This module provides step-by-step guidance for using the MTO portal.
It includes instructions for data submission, verification, and troubleshooting.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import json

logger = logging.getLogger(__name__)

@dataclass
class PortalStep:
    """Portal step information."""
    step_number: int
    title: str
    description: str
    instructions: List[str]
    requirements: List[str]
    notes: Optional[str] = None
    warnings: Optional[List[str]] = None

class PortalGuide:
    """MTO portal guide."""
    
    def __init__(self):
        """Initialize portal guide."""
        self.steps = {
            "registration": [
                PortalStep(
                    step_number=1,
                    title="Create Account",
                    description="Create a new account on the MTO portal",
                    instructions=[
                        "Visit https://portal.mto.gov.on.ca",
                        "Click 'Register New Account'",
                        "Enter school information",
                        "Upload required documents",
                        "Submit registration"
                    ],
                    requirements=[
                        "Valid business number",
                        "School license",
                        "Insurance certificate",
                        "Instructor certifications"
                    ],
                    notes="Registration may take 2-3 business days to process"
                ),
                PortalStep(
                    step_number=2,
                    title="Verify Email",
                    description="Verify your email address",
                    instructions=[
                        "Check email for verification link",
                        "Click verification link",
                        "Set up security questions",
                        "Create password"
                    ],
                    requirements=[
                        "Valid email address",
                        "Access to email account"
                    ],
                    warnings=[
                        "Verification link expires in 24 hours"
                    ]
                )
            ],
            "instructor_management": [
                PortalStep(
                    step_number=1,
                    title="Add Instructor",
                    description="Add a new instructor to the system",
                    instructions=[
                        "Log in to portal",
                        "Navigate to 'Instructors'",
                        "Click 'Add New Instructor'",
                        "Enter instructor details",
                        "Upload certification",
                        "Submit for approval"
                    ],
                    requirements=[
                        "Instructor number",
                        "Valid license",
                        "Certification documents",
                        "Background check"
                    ],
                    notes="Instructor must be approved before teaching"
                ),
                PortalStep(
                    step_number=2,
                    title="Update Instructor",
                    description="Update instructor information",
                    instructions=[
                        "Select instructor",
                        "Click 'Edit'",
                        "Update information",
                        "Upload new documents",
                        "Save changes"
                    ],
                    requirements=[
                        "Valid instructor number",
                        "Updated documents"
                    ],
                    warnings=[
                        "Changes may require re-approval"
                    ]
                )
            ],
            "student_management": [
                PortalStep(
                    step_number=1,
                    title="Register Student",
                    description="Register a new student",
                    instructions=[
                        "Navigate to 'Students'",
                        "Click 'Add New Student'",
                        "Enter student details",
                        "Upload documents",
                        "Submit registration"
                    ],
                    requirements=[
                        "Student information",
                        "Date of birth",
                        "Address",
                        "Contact details"
                    ],
                    notes="Student must be registered before lessons"
                ),
                PortalStep(
                    step_number=2,
                    title="Update Student",
                    description="Update student information",
                    instructions=[
                        "Select student",
                        "Click 'Edit'",
                        "Update information",
                        "Save changes"
                    ],
                    requirements=[
                        "Valid student number",
                        "Updated information"
                    ]
                )
            ],
            "course_management": [
                PortalStep(
                    step_number=1,
                    title="Create Course",
                    description="Create a new course",
                    instructions=[
                        "Navigate to 'Courses'",
                        "Click 'Add New Course'",
                        "Enter course details",
                        "Select instructor",
                        "Add students",
                        "Submit course"
                    ],
                    requirements=[
                        "Course number",
                        "Start date",
                        "End date",
                        "Instructor",
                        "Students"
                    ],
                    notes="Course must be approved before starting"
                ),
                PortalStep(
                    step_number=2,
                    title="Update Course",
                    description="Update course information",
                    instructions=[
                        "Select course",
                        "Click 'Edit'",
                        "Update information",
                        "Save changes"
                    ],
                    requirements=[
                        "Valid course number",
                        "Updated information"
                    ],
                    warnings=[
                        "Changes may affect student records"
                    ]
                )
            ],
            "lesson_management": [
                PortalStep(
                    step_number=1,
                    title="Record Lesson",
                    description="Record a completed lesson",
                    instructions=[
                        "Navigate to 'Lessons'",
                        "Click 'Add New Lesson'",
                        "Select course",
                        "Select student",
                        "Enter lesson details",
                        "Submit lesson"
                    ],
                    requirements=[
                        "Lesson number",
                        "Course",
                        "Student",
                        "Instructor",
                        "Date and time",
                        "Lesson type"
                    ],
                    notes="Lessons must be recorded within 24 hours"
                ),
                PortalStep(
                    step_number=2,
                    title="Update Lesson",
                    description="Update lesson information",
                    instructions=[
                        "Select lesson",
                        "Click 'Edit'",
                        "Update information",
                        "Save changes"
                    ],
                    requirements=[
                        "Valid lesson number",
                        "Updated information"
                    ],
                    warnings=[
                        "Changes may affect student progress"
                    ]
                )
            ],
            "reporting": [
                PortalStep(
                    step_number=1,
                    title="Generate Report",
                    description="Generate a report",
                    instructions=[
                        "Navigate to 'Reports'",
                        "Select report type",
                        "Set date range",
                        "Select filters",
                        "Generate report"
                    ],
                    requirements=[
                        "Report type",
                        "Date range",
                        "Filters"
                    ],
                    notes="Reports can be exported in various formats"
                ),
                PortalStep(
                    step_number=2,
                    title="Export Report",
                    description="Export report data",
                    instructions=[
                        "Select report",
                        "Click 'Export'",
                        "Choose format",
                        "Download file"
                    ],
                    requirements=[
                        "Generated report",
                        "Export format"
                    ],
                    warnings=[
                        "Large reports may take time to export"
                    ]
                )
            ]
        }
    
    def get_steps(
        self,
        section: str
    ) -> List[PortalStep]:
        """Get steps for section.
        
        Args:
            section: Section name
            
        Returns:
            List of steps
        """
        return self.steps.get(section, [])
    
    def get_all_steps(self) -> Dict[str, List[PortalStep]]:
        """Get all steps.
        
        Returns:
            Dictionary of steps by section
        """
        return self.steps
    
    def get_step(
        self,
        section: str,
        step_number: int
    ) -> Optional[PortalStep]:
        """Get specific step.
        
        Args:
            section: Section name
            step_number: Step number
            
        Returns:
            Step information
        """
        steps = self.get_steps(section)
        return next(
            (step for step in steps if step.step_number == step_number),
            None
        )
    
    def export_guide(
        self,
        format: str = "json"
    ) -> str:
        """Export guide.
        
        Args:
            format: Export format
            
        Returns:
            Guide data
        """
        if format == "json":
            return json.dumps(
                {
                    section: [
                        {
                            "step_number": step.step_number,
                            "title": step.title,
                            "description": step.description,
                            "instructions": step.instructions,
                            "requirements": step.requirements,
                            "notes": step.notes,
                            "warnings": step.warnings
                        }
                        for step in steps
                    ]
                    for section, steps in self.steps.items()
                },
                indent=2
            )
        
        raise ValueError(f"Unsupported format: {format}") 