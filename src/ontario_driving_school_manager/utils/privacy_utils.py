"""
Privacy utilities module providing functions for data anonymization and privacy protection.
This module handles sensitive data masking and privacy-related operations.
"""

import re
from typing import Optional, Union, Dict, Any
import hashlib
import json

class PrivacyUtils:
    """Privacy utilities class."""
    
    @staticmethod
    def mask_email(email: str) -> str:
        """
        Mask an email address for privacy.
        
        Args:
            email: Email address to mask
            
        Returns:
            str: Masked email address
        """
        if not email or '@' not in email:
            return email
            
        username, domain = email.split('@')
        masked_username = username[0] + '*' * (len(username) - 2) + username[-1]
        return f"{masked_username}@{domain}"

    @staticmethod
    def mask_phone(phone: str) -> str:
        """
        Mask a phone number for privacy.
        
        Args:
            phone: Phone number to mask
            
        Returns:
            str: Masked phone number
        """
        if not phone:
            return phone
            
        # Remove non-digit characters
        digits = re.sub(r'\D', '', phone)
        if len(digits) < 10:
            return phone
            
        return f"{digits[:3]}***{digits[-4:]}"

    @staticmethod
    def mask_name(name: str) -> str:
        """
        Mask a person's name for privacy.
        
        Args:
            name: Name to mask
            
        Returns:
            str: Masked name
        """
        if not name:
            return name
            
        parts = name.split()
        if len(parts) == 1:
            return f"{parts[0][0]}***"
            
        return f"{parts[0][0]}*** {parts[-1][0]}***"

    @staticmethod
    def hash_sensitive_data(data: str, salt: Optional[str] = None) -> str:
        """
        Hash sensitive data with optional salt.
        
        Args:
            data: Data to hash
            salt: Optional salt for hashing
            
        Returns:
            str: Hashed data
        """
        if not data:
            return data
            
        to_hash = data
        if salt:
            to_hash = f"{data}{salt}"
            
        return hashlib.sha256(to_hash.encode()).hexdigest()

    @staticmethod
    def anonymize_dict(data: Dict[str, Any], fields_to_mask: list) -> Dict[str, Any]:
        """
        Anonymize specific fields in a dictionary.
        
        Args:
            data: Dictionary containing data to anonymize
            fields_to_mask: List of field names to mask
            
        Returns:
            Dict[str, Any]: Dictionary with masked fields
        """
        result = data.copy()
        
        for field in fields_to_mask:
            if field in result:
                value = result[field]
                if isinstance(value, str):
                    if '@' in value:
                        result[field] = PrivacyUtils.mask_email(value)
                    elif re.match(r'\d', value):
                        result[field] = PrivacyUtils.mask_phone(value)
                    else:
                        result[field] = PrivacyUtils.mask_name(value)
                        
        return result

    @staticmethod
    def is_pii_data(text: str) -> bool:
        """
        Check if text contains personally identifiable information.
        
        Args:
            text: Text to check
            
        Returns:
            bool: True if text contains PII, False otherwise
        """
        # Email pattern
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        # Phone pattern (various formats)
        phone_pattern = r'(\+\d{1,3}[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}'
        
        # Credit card pattern
        cc_pattern = r'\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}'
        
        patterns = [email_pattern, phone_pattern, cc_pattern]
        
        return any(re.search(pattern, text) for pattern in patterns) 