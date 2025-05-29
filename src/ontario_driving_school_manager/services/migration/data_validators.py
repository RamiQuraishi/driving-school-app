"""Data validators for ensuring data quality during migration."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from sqlalchemy.orm import Session

from ...models import (
    Student,
    Instructor,
    Vehicle,
    Lesson,
    Payment
)

@dataclass
class ValidationResult:
    """Result of a validation operation."""
    
    is_valid: bool
    errors: List[Dict[str, Any]]
    warnings: List[Dict[str, Any]]
    validated_fields: Set[str]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "validated_fields": list(self.validated_fields),
            "timestamp": self.timestamp.isoformat()
        }

class BaseValidator(ABC):
    """Base class for data validators."""
    
    def __init__(self, session: Session):
        """Initialize validator.
        
        Args:
            session: Database session
        """
        self.session = session
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.validated_fields: Set[str] = set()
    
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate data.
        
        Args:
            data: Data to validate
            
        Returns:
            ValidationResult: Validation result
        """
        pass
    
    def add_error(self, field: str, message: str, value: Any = None) -> None:
        """Add error message.
        
        Args:
            field: Field name
            message: Error message
            value: Field value
        """
        self.errors.append({
            "field": field,
            "message": message,
            "value": value,
            "timestamp": datetime.utcnow()
        })
    
    def add_warning(self, field: str, message: str, value: Any = None) -> None:
        """Add warning message.
        
        Args:
            field: Field name
            message: Warning message
            value: Field value
        """
        self.warnings.append({
            "field": field,
            "message": message,
            "value": value,
            "timestamp": datetime.utcnow()
        })
    
    def mark_validated(self, field: str) -> None:
        """Mark field as validated.
        
        Args:
            field: Field name
        """
        self.validated_fields.add(field)

class StudentValidator(BaseValidator):
    """Validator for student data."""
    
    REQUIRED_FIELDS = {
        "first_name", "last_name", "email", "phone",
        "date_of_birth", "license_number"
    }
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate student data.
        
        Args:
            data: Student data
            
        Returns:
            ValidationResult: Validation result
        """
        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in data:
                self.add_error(field, "Required field missing")
            else:
                self.mark_validated(field)
        
        # Validate email
        if "email" in data:
            if not self._is_valid_email(data["email"]):
                self.add_error("email", "Invalid email format", data["email"])
        
        # Validate phone
        if "phone" in data:
            if not self._is_valid_phone(data["phone"]):
                self.add_error("phone", "Invalid phone format", data["phone"])
        
        # Validate date of birth
        if "date_of_birth" in data:
            if not self._is_valid_date_of_birth(data["date_of_birth"]):
                self.add_error(
                    "date_of_birth",
                    "Invalid date of birth",
                    data["date_of_birth"]
                )
        
        # Validate license number
        if "license_number" in data:
            if not self._is_valid_license(data["license_number"]):
                self.add_error(
                    "license_number",
                    "Invalid license number format",
                    data["license_number"]
                )
        
        return ValidationResult(
            is_valid=len(self.errors) == 0,
            errors=self.errors,
            warnings=self.warnings,
            validated_fields=self.validated_fields,
            timestamp=datetime.utcnow()
        )
    
    def _is_valid_email(self, email: str) -> bool:
        """Check if email is valid.
        
        Args:
            email: Email to check
            
        Returns:
            bool: True if valid
        """
        # Basic email validation
        return "@" in email and "." in email.split("@")[1]
    
    def _is_valid_phone(self, phone: str) -> bool:
        """Check if phone is valid.
        
        Args:
            phone: Phone to check
            
        Returns:
            bool: True if valid
        """
        # Basic phone validation
        return len(phone.replace("-", "").replace(" ", "")) >= 10
    
    def _is_valid_date_of_birth(self, dob: Any) -> bool:
        """Check if date of birth is valid.
        
        Args:
            dob: Date of birth to check
            
        Returns:
            bool: True if valid
        """
        try:
            # Convert to date if string
            if isinstance(dob, str):
                dob = datetime.strptime(dob, "%Y-%m-%d").date()
            
            # Check if date is in the past
            return dob < datetime.now().date()
        except (ValueError, TypeError):
            return False
    
    def _is_valid_license(self, license_number: str) -> bool:
        """Check if license number is valid.
        
        Args:
            license_number: License number to check
            
        Returns:
            bool: True if valid
        """
        # Basic license validation
        return len(license_number) >= 5

class InstructorValidator(BaseValidator):
    """Validator for instructor data."""
    
    REQUIRED_FIELDS = {
        "first_name", "last_name", "email", "phone",
        "license_number", "certification_number"
    }
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate instructor data.
        
        Args:
            data: Instructor data
            
        Returns:
            ValidationResult: Validation result
        """
        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in data:
                self.add_error(field, "Required field missing")
            else:
                self.mark_validated(field)
        
        # Validate email
        if "email" in data:
            if not self._is_valid_email(data["email"]):
                self.add_error("email", "Invalid email format", data["email"])
        
        # Validate phone
        if "phone" in data:
            if not self._is_valid_phone(data["phone"]):
                self.add_error("phone", "Invalid phone format", data["phone"])
        
        # Validate license number
        if "license_number" in data:
            if not self._is_valid_license(data["license_number"]):
                self.add_error(
                    "license_number",
                    "Invalid license number format",
                    data["license_number"]
                )
        
        # Validate certification number
        if "certification_number" in data:
            if not self._is_valid_certification(data["certification_number"]):
                self.add_error(
                    "certification_number",
                    "Invalid certification number format",
                    data["certification_number"]
                )
        
        return ValidationResult(
            is_valid=len(self.errors) == 0,
            errors=self.errors,
            warnings=self.warnings,
            validated_fields=self.validated_fields,
            timestamp=datetime.utcnow()
        )
    
    def _is_valid_email(self, email: str) -> bool:
        """Check if email is valid."""
        return "@" in email and "." in email.split("@")[1]
    
    def _is_valid_phone(self, phone: str) -> bool:
        """Check if phone is valid."""
        return len(phone.replace("-", "").replace(" ", "")) >= 10
    
    def _is_valid_license(self, license_number: str) -> bool:
        """Check if license number is valid."""
        return len(license_number) >= 5
    
    def _is_valid_certification(self, cert_number: str) -> bool:
        """Check if certification number is valid."""
        return len(cert_number) >= 5

class VehicleValidator(BaseValidator):
    """Validator for vehicle data."""
    
    REQUIRED_FIELDS = {
        "make", "model", "year", "license_plate",
        "vin", "inspection_date"
    }
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate vehicle data.
        
        Args:
            data: Vehicle data
            
        Returns:
            ValidationResult: Validation result
        """
        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in data:
                self.add_error(field, "Required field missing")
            else:
                self.mark_validated(field)
        
        # Validate year
        if "year" in data:
            if not self._is_valid_year(data["year"]):
                self.add_error("year", "Invalid year", data["year"])
        
        # Validate license plate
        if "license_plate" in data:
            if not self._is_valid_license_plate(data["license_plate"]):
                self.add_error(
                    "license_plate",
                    "Invalid license plate format",
                    data["license_plate"]
                )
        
        # Validate VIN
        if "vin" in data:
            if not self._is_valid_vin(data["vin"]):
                self.add_error("vin", "Invalid VIN format", data["vin"])
        
        # Validate inspection date
        if "inspection_date" in data:
            if not self._is_valid_inspection_date(data["inspection_date"]):
                self.add_error(
                    "inspection_date",
                    "Invalid inspection date",
                    data["inspection_date"]
                )
        
        return ValidationResult(
            is_valid=len(self.errors) == 0,
            errors=self.errors,
            warnings=self.warnings,
            validated_fields=self.validated_fields,
            timestamp=datetime.utcnow()
        )
    
    def _is_valid_year(self, year: Any) -> bool:
        """Check if year is valid."""
        try:
            year = int(year)
            return 1900 <= year <= datetime.now().year
        except (ValueError, TypeError):
            return False
    
    def _is_valid_license_plate(self, plate: str) -> bool:
        """Check if license plate is valid."""
        return len(plate) >= 2
    
    def _is_valid_vin(self, vin: str) -> bool:
        """Check if VIN is valid."""
        return len(vin) == 17
    
    def _is_valid_inspection_date(self, date: Any) -> bool:
        """Check if inspection date is valid."""
        try:
            if isinstance(date, str):
                date = datetime.strptime(date, "%Y-%m-%d").date()
            return date <= datetime.now().date()
        except (ValueError, TypeError):
            return False 