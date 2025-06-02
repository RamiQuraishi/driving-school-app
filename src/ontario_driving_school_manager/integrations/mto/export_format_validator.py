"""
Export Format Validator Module

This module validates export formats for MTO data exchange.
It includes validation rules and error handling.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime
import re
import json
import csv
import io

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Validation error."""
    pass

@dataclass
class ValidationRule:
    """Validation rule."""
    field: str
    rule_type: str  # REQUIRED, FORMAT, RANGE, ENUM
    description: str
    validator: callable
    error_message: str
    is_critical: bool = True

class ExportFormatValidator:
    """Export format validator."""
    
    def __init__(self):
        """Initialize export format validator."""
        self.rules = {
            "instructor": [
                ValidationRule(
                    field="instructor_number",
                    rule_type="FORMAT",
                    description="Instructor number format",
                    validator=lambda x: bool(re.match(r"^\d{6}$", str(x))),
                    error_message="Instructor number must be 6 digits"
                ),
                ValidationRule(
                    field="license_number",
                    rule_type="FORMAT",
                    description="License number format",
                    validator=lambda x: bool(re.match(r"^[A-Z]\d{4}-\d{5}-\d{5}$", x)),
                    error_message="Invalid license number format"
                ),
                ValidationRule(
                    field="certification_date",
                    rule_type="FORMAT",
                    description="Certification date format",
                    validator=lambda x: bool(re.match(r"^\d{4}-\d{2}-\d{2}$", x)),
                    error_message="Invalid date format"
                )
            ],
            "student": [
                ValidationRule(
                    field="student_number",
                    rule_type="FORMAT",
                    description="Student number format",
                    validator=lambda x: bool(re.match(r"^\d{8}$", str(x))),
                    error_message="Student number must be 8 digits"
                ),
                ValidationRule(
                    field="date_of_birth",
                    rule_type="FORMAT",
                    description="Date of birth format",
                    validator=lambda x: bool(re.match(r"^\d{4}-\d{2}-\d{2}$", x)),
                    error_message="Invalid date format"
                ),
                ValidationRule(
                    field="postal_code",
                    rule_type="FORMAT",
                    description="Postal code format",
                    validator=lambda x: bool(re.match(r"^[A-Z]\d[A-Z] \d[A-Z]\d$", x)),
                    error_message="Invalid postal code format"
                )
            ],
            "course": [
                ValidationRule(
                    field="course_number",
                    rule_type="FORMAT",
                    description="Course number format",
                    validator=lambda x: bool(re.match(r"^\d{6}$", str(x))),
                    error_message="Course number must be 6 digits"
                ),
                ValidationRule(
                    field="start_date",
                    rule_type="FORMAT",
                    description="Start date format",
                    validator=lambda x: bool(re.match(r"^\d{4}-\d{2}-\d{2}$", x)),
                    error_message="Invalid date format"
                ),
                ValidationRule(
                    field="end_date",
                    rule_type="FORMAT",
                    description="End date format",
                    validator=lambda x: bool(re.match(r"^\d{4}-\d{2}-\d{2}$", x)),
                    error_message="Invalid date format"
                )
            ],
            "lesson": [
                ValidationRule(
                    field="lesson_number",
                    rule_type="FORMAT",
                    description="Lesson number format",
                    validator=lambda x: isinstance(x, int),
                    error_message="Lesson number must be an integer"
                ),
                ValidationRule(
                    field="lesson_type",
                    rule_type="ENUM",
                    description="Lesson type",
                    validator=lambda x: x in ["CLASSROOM", "IN_CAR", "SIMULATOR"],
                    error_message="Invalid lesson type"
                ),
                ValidationRule(
                    field="date",
                    rule_type="FORMAT",
                    description="Lesson date format",
                    validator=lambda x: bool(re.match(r"^\d{4}-\d{2}-\d{2}$", x)),
                    error_message="Invalid date format"
                )
            ]
        }
    
    def validate_data(
        self,
        data: Dict[str, Any],
        data_type: str
    ) -> Tuple[bool, List[str]]:
        """Validate data.
        
        Args:
            data: Data to validate
            data_type: Type of data
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        if data_type not in self.rules:
            raise ValueError(f"Unknown data type: {data_type}")
        
        errors = []
        
        # Check required fields
        for rule in self.rules[data_type]:
            if rule.rule_type == "REQUIRED":
                if rule.field not in data:
                    errors.append(f"Missing required field: {rule.field}")
                    if rule.is_critical:
                        return False, errors
        
        # Validate fields
        for rule in self.rules[data_type]:
            if rule.field in data:
                if not rule.validator(data[rule.field]):
                    errors.append(rule.error_message)
                    if rule.is_critical:
                        return False, errors
        
        return len(errors) == 0, errors
    
    def validate_json(
        self,
        json_data: str,
        data_type: str
    ) -> Tuple[bool, List[str]]:
        """Validate JSON data.
        
        Args:
            json_data: JSON data to validate
            data_type: Type of data
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        try:
            data = json.loads(json_data)
            return self.validate_data(data, data_type)
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON: {str(e)}"]
    
    def validate_csv(
        self,
        csv_data: str,
        data_type: str
    ) -> Tuple[bool, List[str]]:
        """Validate CSV data.
        
        Args:
            csv_data: CSV data to validate
            data_type: Type of data
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        try:
            reader = csv.DictReader(io.StringIO(csv_data))
            data = next(reader, None)
            
            if not data:
                return False, ["Empty CSV data"]
            
            return self.validate_data(data, data_type)
        except csv.Error as e:
            return False, [f"Invalid CSV: {str(e)}"]
    
    def validate_batch(
        self,
        data_list: List[Dict[str, Any]],
        data_type: str
    ) -> Tuple[bool, List[str]]:
        """Validate batch of data.
        
        Args:
            data_list: List of data to validate
            data_type: Type of data
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        all_valid = True
        all_errors = []
        
        for i, data in enumerate(data_list):
            is_valid, errors = self.validate_data(data, data_type)
            
            if not is_valid:
                all_valid = False
                all_errors.extend(
                    f"Item {i + 1}: {error}"
                    for error in errors
                )
        
        return all_valid, all_errors
    
    def add_rule(
        self,
        data_type: str,
        rule: ValidationRule
    ) -> None:
        """Add validation rule.
        
        Args:
            data_type: Type of data
            rule: Validation rule
        """
        if data_type not in self.rules:
            self.rules[data_type] = []
        
        self.rules[data_type].append(rule)
    
    def remove_rule(
        self,
        data_type: str,
        field: str
    ) -> None:
        """Remove validation rule.
        
        Args:
            data_type: Type of data
            field: Field name
        """
        if data_type in self.rules:
            self.rules[data_type] = [
                rule for rule in self.rules[data_type]
                if rule.field != field
            ]
    
    def get_rules(
        self,
        data_type: str
    ) -> List[ValidationRule]:
        """Get validation rules.
        
        Args:
            data_type: Type of data
            
        Returns:
            List of validation rules
        """
        return self.rules.get(data_type, [])
    
    def get_all_rules(self) -> Dict[str, List[ValidationRule]]:
        """Get all validation rules.
        
        Returns:
            Dictionary of validation rules by data type
        """
        return self.rules 