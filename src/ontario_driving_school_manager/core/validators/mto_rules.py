"""
MTO Rules Validator

This module provides validation for Ministry of Transportation (MTO) specific rules.
It implements validation for driver's licenses, vehicle registrations, and other MTO requirements.

Author: Rami Drive School
Date: 2024
"""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from . import Validator, ValidationError

class MTORules(Validator[Dict[str, Any]]):
    """MTO rules validator."""
    
    def __init__(self):
        """Initialize MTO rules validator."""
        # License plate format: 4 letters followed by 3 numbers
        self.license_plate_pattern = re.compile(r'^[A-Z]{4}\d{3}$')
        
        # Driver's license format: 15 characters (letters and numbers)
        self.license_number_pattern = re.compile(r'^[A-Z0-9]{15}$')
        
        # Minimum age requirements
        self.min_age_g1 = 16
        self.min_age_g2 = 17
        self.min_age_g = 18
    
    def validate(self, data: Dict[str, Any]) -> List[str]:
        """Validate MTO rules.
        
        Args:
            data: Data to validate
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Validate driver's license
        if 'license' in data:
            errors.extend(self._validate_license(data['license']))
        
        # Validate vehicle registration
        if 'vehicle' in data:
            errors.extend(self._validate_vehicle(data['vehicle']))
        
        # Validate age requirements
        if 'age' in data and 'license_type' in data:
            errors.extend(self._validate_age(data['age'], data['license_type']))
        
        return errors
    
    def _validate_license(self, license_data: Dict[str, Any]) -> List[str]:
        """Validate driver's license.
        
        Args:
            license_data: License data to validate
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Validate license number
        if 'number' not in license_data:
            errors.append("License number is required")
        elif not self.license_number_pattern.match(license_data['number']):
            errors.append("Invalid license number format")
        
        # Validate license type
        if 'type' not in license_data:
            errors.append("License type is required")
        elif license_data['type'] not in ['G1', 'G2', 'G']:
            errors.append("Invalid license type")
        
        # Validate expiry date
        if 'expiry_date' in license_data:
            try:
                expiry = datetime.fromisoformat(license_data['expiry_date'])
                if expiry < datetime.now():
                    errors.append("License has expired")
            except ValueError:
                errors.append("Invalid expiry date format")
        
        return errors
    
    def _validate_vehicle(self, vehicle_data: Dict[str, Any]) -> List[str]:
        """Validate vehicle registration.
        
        Args:
            vehicle_data: Vehicle data to validate
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Validate license plate
        if 'license_plate' not in vehicle_data:
            errors.append("License plate is required")
        elif not self.license_plate_pattern.match(vehicle_data['license_plate']):
            errors.append("Invalid license plate format")
        
        # Validate vehicle type
        if 'type' not in vehicle_data:
            errors.append("Vehicle type is required")
        elif vehicle_data['type'] not in ['car', 'truck', 'van']:
            errors.append("Invalid vehicle type")
        
        # Validate registration expiry
        if 'registration_expiry' in vehicle_data:
            try:
                expiry = datetime.fromisoformat(vehicle_data['registration_expiry'])
                if expiry < datetime.now():
                    errors.append("Vehicle registration has expired")
            except ValueError:
                errors.append("Invalid registration expiry date format")
        
        return errors
    
    def _validate_age(self, age: int, license_type: str) -> List[str]:
        """Validate age requirements.
        
        Args:
            age: Age to validate
            license_type: Type of license
            
        Returns:
            List of validation errors
        """
        errors = []
        
        if license_type == 'G1' and age < self.min_age_g1:
            errors.append(f"Must be at least {self.min_age_g1} years old for G1 license")
        elif license_type == 'G2' and age < self.min_age_g2:
            errors.append(f"Must be at least {self.min_age_g2} years old for G2 license")
        elif license_type == 'G' and age < self.min_age_g:
            errors.append(f"Must be at least {self.min_age_g} years old for G license")
        
        return errors