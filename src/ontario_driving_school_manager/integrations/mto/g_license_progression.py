"""
G License Progression Module

This module manages G license progression requirements and tracking.
It includes progression rules, validation, and reporting functionality.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)

@dataclass
class GLicenseRequirement:
    """G license requirement."""
    level: str  # G1, G2, G
    requirement_type: str  # WAIT_TIME, LESSONS, TEST
    description: str
    minimum_value: int
    unit: str  # DAYS, HOURS, COUNT
    is_mandatory: bool = True
    notes: Optional[str] = None

@dataclass
class GLicenseProgress:
    """G license progress."""
    student_number: str
    current_level: str
    start_date: datetime
    requirements: List[GLicenseRequirement]
    completed_requirements: Dict[str, Any] = field(default_factory=dict)
    next_test_date: Optional[datetime] = None
    notes: Optional[str] = None

class GLicenseProgression:
    """G license progression manager."""
    
    def __init__(self):
        """Initialize G license progression manager."""
        self.requirements = {
            "G1": [
                GLicenseRequirement(
                    level="G1",
                    requirement_type="WAIT_TIME",
                    description="Minimum time between G1 and G2",
                    minimum_value=365,
                    unit="DAYS",
                    notes="Must be at least 16 years old"
                ),
                GLicenseRequirement(
                    level="G1",
                    requirement_type="LESSONS",
                    description="Minimum in-car lessons",
                    minimum_value=20,
                    unit="HOURS",
                    notes="Must include 10 hours of night driving"
                )
            ],
            "G2": [
                GLicenseRequirement(
                    level="G2",
                    requirement_type="WAIT_TIME",
                    description="Minimum time between G2 and G",
                    minimum_value=365,
                    unit="DAYS"
                ),
                GLicenseRequirement(
                    level="G2",
                    requirement_type="LESSONS",
                    description="Minimum in-car lessons",
                    minimum_value=20,
                    unit="HOURS",
                    notes="Must include 10 hours of night driving"
                )
            ]
        }
    
    def get_requirements(self, level: str) -> List[GLicenseRequirement]:
        """Get requirements for license level.
        
        Args:
            level: License level
            
        Returns:
            List of requirements
        """
        return self.requirements.get(level, [])
    
    def check_progress(
        self,
        progress: GLicenseProgress
    ) -> Dict[str, Any]:
        """Check license progression progress.
        
        Args:
            progress: License progress
            
        Returns:
            Progress status
        """
        status = {
            "student_number": progress.student_number,
            "current_level": progress.current_level,
            "start_date": progress.start_date,
            "requirements": [],
            "is_eligible": True,
            "next_test_date": None,
            "notes": []
        }
        
        # Check each requirement
        for req in progress.requirements:
            req_status = self._check_requirement(req, progress)
            status["requirements"].append(req_status)
            
            if req_status["is_mandatory"] and not req_status["is_met"]:
                status["is_eligible"] = False
                status["notes"].append(req_status["message"])
        
        # Calculate next test date
        if status["is_eligible"]:
            status["next_test_date"] = self._calculate_next_test_date(progress)
        
        return status
    
    def _check_requirement(
        self,
        requirement: GLicenseRequirement,
        progress: GLicenseProgress
    ) -> Dict[str, Any]:
        """Check requirement status.
        
        Args:
            requirement: License requirement
            progress: License progress
            
        Returns:
            Requirement status
        """
        status = {
            "type": requirement.requirement_type,
            "description": requirement.description,
            "is_mandatory": requirement.is_mandatory,
            "is_met": False,
            "message": ""
        }
        
        # Get completed value
        completed = progress.completed_requirements.get(
            requirement.requirement_type,
            0
        )
        
        # Check wait time
        if requirement.requirement_type == "WAIT_TIME":
            elapsed = (datetime.now() - progress.start_date).days
            status["is_met"] = elapsed >= requirement.minimum_value
            status["message"] = (
                f"Wait time requirement met ({elapsed} days)"
                if status["is_met"]
                else f"Need {requirement.minimum_value - elapsed} more days"
            )
        
        # Check lessons
        elif requirement.requirement_type == "LESSONS":
            status["is_met"] = completed >= requirement.minimum_value
            status["message"] = (
                f"Lesson requirement met ({completed} hours)"
                if status["is_met"]
                else f"Need {requirement.minimum_value - completed} more hours"
            )
        
        # Check test
        elif requirement.requirement_type == "TEST":
            status["is_met"] = completed > 0
            status["message"] = (
                "Test requirement met"
                if status["is_met"]
                else "Test not completed"
            )
        
        return status
    
    def _calculate_next_test_date(
        self,
        progress: GLicenseProgress
    ) -> Optional[datetime]:
        """Calculate next test date.
        
        Args:
            progress: License progress
            
        Returns:
            Next test date
        """
        if not progress.is_eligible:
            return None
        
        # Get wait time requirement
        wait_req = next(
            (r for r in progress.requirements if r.requirement_type == "WAIT_TIME"),
            None
        )
        
        if not wait_req:
            return None
        
        # Calculate date
        return progress.start_date + timedelta(days=wait_req.minimum_value)
    
    def validate_license_number(self, number: str) -> bool:
        """Validate license number.
        
        Args:
            number: License number
            
        Returns:
            Whether number is valid
        """
        return bool(re.match(r"^[A-Z]\d{4}-\d{5}-\d{5}$", number))
    
    def format_license_number(self, number: str) -> str:
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