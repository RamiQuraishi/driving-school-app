"""
Password policy utility module providing functions for password validation and strength checking.
This module handles password requirements and security checks.
"""

import re
from typing import List, Tuple, Dict
from dataclasses import dataclass
from enum import Enum

class PasswordStrength(Enum):
    """Enum for password strength levels."""
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"
    VERY_STRONG = "very_strong"

@dataclass
class PasswordPolicy:
    """Password policy configuration."""
    min_length: int = 8
    max_length: int = 128
    require_uppercase: bool = True
    require_lowercase: bool = True
    require_digits: bool = True
    require_special: bool = True
    min_special_chars: int = 1
    prevent_common_passwords: bool = True
    prevent_sequential_chars: bool = True
    prevent_repeated_chars: bool = True

class PasswordValidator:
    """Password validation and strength checking."""
    
    def __init__(self, policy: PasswordPolicy = None):
        """
        Initialize the password validator.
        
        Args:
            policy: Optional custom password policy
        """
        self.policy = policy or PasswordPolicy()
        self.common_passwords = self._load_common_passwords()

    def _load_common_passwords(self) -> List[str]:
        """
        Load list of common passwords.
        
        Returns:
            List[str]: List of common passwords
        """
        # This is a small subset of common passwords
        return [
            "password", "123456", "qwerty", "admin", "welcome",
            "letmein", "monkey", "dragon", "baseball", "football"
        ]

    def validate_password(self, password: str) -> Tuple[bool, List[str]]:
        """
        Validate a password against the policy.
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_errors)
        """
        errors = []
        
        # Check length
        if len(password) < self.policy.min_length:
            errors.append(f"Password must be at least {self.policy.min_length} characters long")
        if len(password) > self.policy.max_length:
            errors.append(f"Password must not exceed {self.policy.max_length} characters")

        # Check character requirements
        if self.policy.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        if self.policy.require_lowercase and not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        if self.policy.require_digits and not re.search(r'\d', password):
            errors.append("Password must contain at least one digit")
        if self.policy.require_special:
            special_chars = len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password))
            if special_chars < self.policy.min_special_chars:
                errors.append(f"Password must contain at least {self.policy.min_special_chars} special character(s)")

        # Check for common passwords
        if self.policy.prevent_common_passwords and password.lower() in self.common_passwords:
            errors.append("Password is too common")

        # Check for sequential characters
        if self.policy.prevent_sequential_chars:
            if re.search(r'(?:abc|bcd|cde|def|efg|123|234|345|456|567|678|789)', password.lower()):
                errors.append("Password contains sequential characters")

        # Check for repeated characters
        if self.policy.prevent_repeated_chars:
            if re.search(r'(.)\1{2,}', password):
                errors.append("Password contains too many repeated characters")

        return len(errors) == 0, errors

    def check_password_strength(self, password: str) -> PasswordStrength:
        """
        Check the strength of a password.
        
        Args:
            password: Password to check
            
        Returns:
            PasswordStrength: Password strength level
        """
        score = 0
        
        # Length score
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1

        # Character type score
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'\d', password):
            score += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1

        # Complexity score
        if len(set(password)) > len(password) * 0.7:
            score += 1
        if not re.search(r'(.)\1{2,}', password):
            score += 1

        # Determine strength level
        if score >= 6:
            return PasswordStrength.VERY_STRONG
        elif score >= 4:
            return PasswordStrength.STRONG
        elif score >= 2:
            return PasswordStrength.MEDIUM
        else:
            return PasswordStrength.WEAK

    def get_password_requirements(self) -> Dict[str, str]:
        """
        Get a dictionary of password requirements.
        
        Returns:
            Dict[str, str]: Dictionary of requirements
        """
        return {
            "min_length": f"At least {self.policy.min_length} characters",
            "max_length": f"Maximum {self.policy.max_length} characters",
            "uppercase": "At least one uppercase letter" if self.policy.require_uppercase else None,
            "lowercase": "At least one lowercase letter" if self.policy.require_lowercase else None,
            "digits": "At least one digit" if self.policy.require_digits else None,
            "special": f"At least {self.policy.min_special_chars} special character(s)" if self.policy.require_special else None,
            "common": "Must not be a common password" if self.policy.prevent_common_passwords else None,
            "sequential": "Must not contain sequential characters" if self.policy.prevent_sequential_chars else None,
            "repeated": "Must not contain repeated characters" if self.policy.prevent_repeated_chars else None
        } 