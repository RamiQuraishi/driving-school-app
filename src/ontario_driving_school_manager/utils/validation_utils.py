"""
Validation Utilities Module

This module provides data validation functionality.
It includes validation for common data types and formats.

Author: Rami Drive School
Date: 2024
"""

import re
from typing import Dict, Any, Optional, Union, List, Tuple, Callable
from datetime import datetime
import logging
import json
import os
import email.utils
import ipaddress
import uuid

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Validation error."""
    pass

class ValidationManager:
    """Validation manager."""
    
    def __init__(self):
        """Initialize validation manager."""
        # Email pattern
        self.email_pattern = re.compile(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        )
        
        # Phone pattern
        self.phone_pattern = re.compile(
            r"^\+?[1-9]\d{1,14}$"
        )
        
        # URL pattern
        self.url_pattern = re.compile(
            r"^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
        )
        
        # Date pattern
        self.date_pattern = re.compile(
            r"^\d{4}-\d{2}-\d{2}$"
        )
        
        # Time pattern
        self.time_pattern = re.compile(
            r"^\d{2}:\d{2}:\d{2}$"
        )
        
        # DateTime pattern
        self.datetime_pattern = re.compile(
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?$"
        )
        
        # Postal code pattern
        self.postal_code_pattern = re.compile(
            r"^[A-Z]\d[A-Z] \d[A-Z]\d$"
        )
        
        # Credit card pattern
        self.credit_card_pattern = re.compile(
            r"^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9]{2})[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$"
        )
        
        # Password pattern
        self.password_pattern = re.compile(
            r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$"
        )
        
        # Username pattern
        self.username_pattern = re.compile(
            r"^[a-zA-Z0-9_-]{3,16}$"
        )
        
        # File path pattern
        self.file_path_pattern = re.compile(
            r"^[a-zA-Z0-9/\\_.-]+$"
        )
        
        # IP address pattern
        self.ip_pattern = re.compile(
            r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        )
        
        # MAC address pattern
        self.mac_pattern = re.compile(
            r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
        )
        
        # UUID pattern
        self.uuid_pattern = re.compile(
            r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
        )
        
        # Hex color pattern
        self.hex_color_pattern = re.compile(
            r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
        )
        
        # HTML tag pattern
        self.html_tag_pattern = re.compile(
            r"^<([a-z1-6]+)([^<]+)*(?:>(.*)<\/\1>|\s+\/>)$"
        )
        
        # JSON pattern
        self.json_pattern = re.compile(
            r"^\{.*\}$"
        )
        
        # XML pattern
        self.xml_pattern = re.compile(
            r"^<[^>]+>.*<\/[^>]+>$"
        )
        
        # Base64 pattern
        self.base64_pattern = re.compile(
            r"^[A-Za-z0-9+/]+={0,2}$"
        )
        
        # MD5 pattern
        self.md5_pattern = re.compile(
            r"^[a-f0-9]{32}$"
        )
        
        # SHA1 pattern
        self.sha1_pattern = re.compile(
            r"^[a-f0-9]{40}$"
        )
        
        # SHA256 pattern
        self.sha256_pattern = re.compile(
            r"^[a-f0-9]{64}$"
        )
        
        # SHA512 pattern
        self.sha512_pattern = re.compile(
            r"^[a-f0-9]{128}$"
        )
    
    def validate_email(
        self,
        email_str: str
    ) -> bool:
        """Validate email address.
        
        Args:
            email_str: Email address
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check pattern
            if not self.email_pattern.match(email_str):
                return False
            
            # Check format
            email.utils.parseaddr(email_str)
            
            return True
        except Exception:
            return False
    
    def validate_phone(
        self,
        phone_str: str
    ) -> bool:
        """Validate phone number.
        
        Args:
            phone_str: Phone number
            
        Returns:
            True if valid, False otherwise
        """
        return bool(self.phone_pattern.match(phone_str))
    
    def validate_url(
        self,
        url_str: str
    ) -> bool:
        """Validate URL.
        
        Args:
            url_str: URL
            
        Returns:
            True if valid, False otherwise
        """
        return bool(self.url_pattern.match(url_str))
    
    def validate_date(
        self,
        date_str: str
    ) -> bool:
        """Validate date.
        
        Args:
            date_str: Date string
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check pattern
            if not self.date_pattern.match(date_str):
                return False
            
            # Check format
            datetime.strptime(date_str, "%Y-%m-%d")
            
            return True
        except Exception:
            return False
    
    def validate_time(
        self,
        time_str: str
    ) -> bool:
        """Validate time.
        
        Args:
            time_str: Time string
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check pattern
            if not self.time_pattern.match(time_str):
                return False
            
            # Check format
            datetime.strptime(time_str, "%H:%M:%S")
            
            return True
        except Exception:
            return False
    
    def validate_datetime(
        self,
        datetime_str: str
    ) -> bool:
        """Validate datetime.
        
        Args:
            datetime_str: Datetime string
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check pattern
            if not self.datetime_pattern.match(datetime_str):
                return False
            
            # Check format
            datetime.fromisoformat(datetime_str)
            
            return True
        except Exception:
            return False
    
    def validate_postal_code(
        self,
        postal_code: str
    ) -> bool:
        """Validate postal code.
        
        Args:
            postal_code: Postal code
            
        Returns:
            True if valid, False otherwise
        """
        return bool(self.postal_code_pattern.match(postal_code))
    
    def validate_credit_card(
        self,
        credit_card: str
    ) -> bool:
        """Validate credit card number.
        
        Args:
            credit_card: Credit card number
            
        Returns:
            True if valid, False otherwise
        """
        return bool(self.credit_card_pattern.match(credit_card))
    
    def validate_password(
        self,
        password: str
    ) -> bool:
        """Validate password.
        
        Args:
            password: Password
            
        Returns:
            True if valid, False otherwise
        """
        return bool(self.password_pattern.match(password))
    
    def validate_username(
        self,
        username: str
    ) -> bool:
        """Validate username.
        
        Args:
            username: Username
            
        Returns:
            True if valid, False otherwise
        """
        return bool(self.username_pattern.match(username))
    
    def validate_file_path(
        self,
        file_path: str
    ) -> bool:
        """Validate file path.
        
        Args:
            file_path: File path
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check pattern
            if not self.file_path_pattern.match(file_path):
                return False
            
            # Check if file exists
            return os.path.exists(file_path)
        except Exception:
            return False
    
    def validate_ip(
        self,
        ip_str: str
    ) -> bool:
        """Validate IP address.
        
        Args:
            ip_str: IP address
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check pattern
            if not self.ip_pattern.match(ip_str):
                return False
            
            # Check format
            ipaddress.ip_address(ip_str)
            
            return True
        except Exception:
            return False
    
    def validate_mac(
        self,
        mac_str: str
    ) -> bool:
        """Validate MAC address.
        
        Args:
            mac_str: MAC address
            
        Returns:
            True if valid, False otherwise
        """
        return bool(self.mac_pattern.match(mac_str))
    
    def validate_uuid(
        self,
        uuid_str: str
    ) -> bool:
        """Validate UUID.
        
        Args:
            uuid_str: UUID
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check pattern
            if not self.uuid_pattern.match(uuid_str):
                return False
            
            # Check format
            uuid.UUID(uuid_str)
            
            return True
        except Exception:
            return False
    
    def validate_hex_color(
        self,
        hex_color: str
    ) -> bool:
        """Validate hex color.
        
        Args:
            hex_color: Hex color
            
        Returns:
            True if valid, False otherwise
        """
        return bool(self.hex_color_pattern.match(hex_color))
    
    def validate_html_tag(
        self,
        html_tag: str
    ) -> bool:
        """Validate HTML tag.
        
        Args:
            html_tag: HTML tag
            
        Returns:
            True if valid, False otherwise
        """
        return bool(self.html_tag_pattern.match(html_tag))
    
    def validate_json(
        self,
        json_str: str
    ) -> bool:
        """Validate JSON.
        
        Args:
            json_str: JSON string
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check pattern
            if not self.json_pattern.match(json_str):
                return False
            
            # Check format
            json.loads(json_str)
            
            return True
        except Exception:
            return False
    
    def validate_xml(
        self,
        xml_str: str
    ) -> bool:
        """Validate XML.
        
        Args:
            xml_str: XML string
            
        Returns:
            True if valid, False otherwise
        """
        return bool(self.xml_pattern.match(xml_str))
    
    def validate_base64(
        self,
        base64_str: str
    ) -> bool:
        """Validate Base64.
        
        Args:
            base64_str: Base64 string
            
        Returns:
            True if valid, False otherwise
        """
        return bool(self.base64_pattern.match(base64_str))
    
    def validate_md5(
        self,
        md5_str: str
    ) -> bool:
        """Validate MD5.
        
        Args:
            md5_str: MD5 string
            
        Returns:
            True if valid, False otherwise
        """
        return bool(self.md5_pattern.match(md5_str))
    
    def validate_sha1(
        self,
        sha1_str: str
    ) -> bool:
        """Validate SHA1.
        
        Args:
            sha1_str: SHA1 string
            
        Returns:
            True if valid, False otherwise
        """
        return bool(self.sha1_pattern.match(sha1_str))
    
    def validate_sha256(
        self,
        sha256_str: str
    ) -> bool:
        """Validate SHA256.
        
        Args:
            sha256_str: SHA256 string
            
        Returns:
            True if valid, False otherwise
        """
        return bool(self.sha256_pattern.match(sha256_str))
    
    def validate_sha512(
        self,
        sha512_str: str
    ) -> bool:
        """Validate SHA512.
        
        Args:
            sha512_str: SHA512 string
            
        Returns:
            True if valid, False otherwise
        """
        return bool(self.sha512_pattern.match(sha512_str))
    
    def validate_data(
        self,
        data: Dict[str, Any],
        schema: Dict[str, Any]
    ) -> bool:
        """Validate data against schema.
        
        Args:
            data: Data to validate
            schema: Validation schema
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check required fields
            for field, rules in schema.items():
                if rules.get("required", False):
                    if field not in data:
                        return False
            
            # Check field types
            for field, value in data.items():
                if field not in schema:
                    continue
                
                rules = schema[field]
                
                if "type" in rules:
                    if not isinstance(value, rules["type"]):
                        return False
                
                if "min" in rules:
                    if value < rules["min"]:
                        return False
                
                if "max" in rules:
                    if value > rules["max"]:
                        return False
                
                if "min_length" in rules:
                    if len(value) < rules["min_length"]:
                        return False
                
                if "max_length" in rules:
                    if len(value) > rules["max_length"]:
                        return False
                
                if "pattern" in rules:
                    if not re.match(rules["pattern"], value):
                        return False
                
                if "enum" in rules:
                    if value not in rules["enum"]:
                        return False
                
                if "custom" in rules:
                    if not rules["custom"](value):
                        return False
            
            return True
        except Exception:
            return False
    
    def validate_data_with_custom_rules(
        self,
        data: Dict[str, Any],
        rules: Dict[str, Callable[[Any], bool]]
    ) -> bool:
        """Validate data with custom rules.
        
        Args:
            data: Data to validate
            rules: Custom validation rules
            
        Returns:
            True if valid, False otherwise
        """
        try:
            for field, rule in rules.items():
                if field not in data:
                    return False
                
                if not rule(data[field]):
                    return False
            
            return True
        except Exception:
            return False
    
    def validate_data_with_dependencies(
        self,
        data: Dict[str, Any],
        dependencies: Dict[str, List[str]]
    ) -> bool:
        """Validate data with dependencies.
        
        Args:
            data: Data to validate
            dependencies: Field dependencies
            
        Returns:
            True if valid, False otherwise
        """
        try:
            for field, deps in dependencies.items():
                if field in data:
                    for dep in deps:
                        if dep not in data:
                            return False
            
            return True
        except Exception:
            return False
    
    def validate_data_with_conditions(
        self,
        data: Dict[str, Any],
        conditions: List[Tuple[str, str, Any]]
    ) -> bool:
        """Validate data with conditions.
        
        Args:
            data: Data to validate
            conditions: Validation conditions
            
        Returns:
            True if valid, False otherwise
        """
        try:
            for field, operator, value in conditions:
                if field not in data:
                    return False
                
                if operator == "eq":
                    if data[field] != value:
                        return False
                elif operator == "ne":
                    if data[field] == value:
                        return False
                elif operator == "gt":
                    if data[field] <= value:
                        return False
                elif operator == "ge":
                    if data[field] < value:
                        return False
                elif operator == "lt":
                    if data[field] >= value:
                        return False
                elif operator == "le":
                    if data[field] > value:
                        return False
                elif operator == "in":
                    if data[field] not in value:
                        return False
                elif operator == "nin":
                    if data[field] in value:
                        return False
                elif operator == "regex":
                    if not re.match(value, data[field]):
                        return False
                else:
                    return False
            
            return True
        except Exception:
            return False
    
    def validate_data_with_custom_validators(
        self,
        data: Dict[str, Any],
        validators: Dict[str, List[Callable[[Any], bool]]]
    ) -> bool:
        """Validate data with custom validators.
        
        Args:
            data: Data to validate
            validators: Custom validators
            
        Returns:
            True if valid, False otherwise
        """
        try:
            for field, field_validators in validators.items():
                if field not in data:
                    return False
                
                for validator in field_validators:
                    if not validator(data[field]):
                        return False
            
            return True
        except Exception:
            return False
    
    def validate_data_with_error_messages(
        self,
        data: Dict[str, Any],
        schema: Dict[str, Any]
    ) -> Tuple[bool, Dict[str, str]]:
        """Validate data with error messages.
        
        Args:
            data: Data to validate
            schema: Validation schema
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        try:
            error_messages = {}
            
            # Check required fields
            for field, rules in schema.items():
                if rules.get("required", False):
                    if field not in data:
                        error_messages[field] = "Field is required"
            
            # Check field types
            for field, value in data.items():
                if field not in schema:
                    continue
                
                rules = schema[field]
                
                if "type" in rules:
                    if not isinstance(value, rules["type"]):
                        error_messages[field] = f"Invalid type: {type(value)}"
                
                if "min" in rules:
                    if value < rules["min"]:
                        error_messages[field] = f"Value must be >= {rules['min']}"
                
                if "max" in rules:
                    if value > rules["max"]:
                        error_messages[field] = f"Value must be <= {rules['max']}"
                
                if "min_length" in rules:
                    if len(value) < rules["min_length"]:
                        error_messages[field] = f"Length must be >= {rules['min_length']}"
                
                if "max_length" in rules:
                    if len(value) > rules["max_length"]:
                        error_messages[field] = f"Length must be <= {rules['max_length']}"
                
                if "pattern" in rules:
                    if not re.match(rules["pattern"], value):
                        error_messages[field] = "Invalid format"
                
                if "enum" in rules:
                    if value not in rules["enum"]:
                        error_messages[field] = f"Value must be one of {rules['enum']}"
                
                if "custom" in rules:
                    if not rules["custom"](value):
                        error_messages[field] = "Invalid value"
            
            return len(error_messages) == 0, error_messages
        except Exception as e:
            return False, {"error": str(e)}
    
    def validate_data_with_custom_error_messages(
        self,
        data: Dict[str, Any],
        rules: Dict[str, Tuple[Callable[[Any], bool], str]]
    ) -> Tuple[bool, Dict[str, str]]:
        """Validate data with custom error messages.
        
        Args:
            data: Data to validate
            rules: Custom validation rules with error messages
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        try:
            error_messages = {}
            
            for field, (rule, message) in rules.items():
                if field not in data:
                    error_messages[field] = "Field is required"
                    continue
                
                if not rule(data[field]):
                    error_messages[field] = message
            
            return len(error_messages) == 0, error_messages
        except Exception as e:
            return False, {"error": str(e)}
    
    def validate_data_with_dependency_error_messages(
        self,
        data: Dict[str, Any],
        dependencies: Dict[str, List[Tuple[str, str]]]
    ) -> Tuple[bool, Dict[str, str]]:
        """Validate data with dependency error messages.
        
        Args:
            data: Data to validate
            dependencies: Field dependencies with error messages
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        try:
            error_messages = {}
            
            for field, deps in dependencies.items():
                if field in data:
                    for dep, message in deps:
                        if dep not in data:
                            error_messages[field] = message
                            break
            
            return len(error_messages) == 0, error_messages
        except Exception as e:
            return False, {"error": str(e)}
    
    def validate_data_with_condition_error_messages(
        self,
        data: Dict[str, Any],
        conditions: List[Tuple[str, str, Any, str]]
    ) -> Tuple[bool, Dict[str, str]]:
        """Validate data with condition error messages.
        
        Args:
            data: Data to validate
            conditions: Validation conditions with error messages
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        try:
            error_messages = {}
            
            for field, operator, value, message in conditions:
                if field not in data:
                    error_messages[field] = "Field is required"
                    continue
                
                if operator == "eq":
                    if data[field] != value:
                        error_messages[field] = message
                elif operator == "ne":
                    if data[field] == value:
                        error_messages[field] = message
                elif operator == "gt":
                    if data[field] <= value:
                        error_messages[field] = message
                elif operator == "ge":
                    if data[field] < value:
                        error_messages[field] = message
                elif operator == "lt":
                    if data[field] >= value:
                        error_messages[field] = message
                elif operator == "le":
                    if data[field] > value:
                        error_messages[field] = message
                elif operator == "in":
                    if data[field] not in value:
                        error_messages[field] = message
                elif operator == "nin":
                    if data[field] in value:
                        error_messages[field] = message
                elif operator == "regex":
                    if not re.match(value, data[field]):
                        error_messages[field] = message
                else:
                    error_messages[field] = "Invalid operator"
            
            return len(error_messages) == 0, error_messages
        except Exception as e:
            return False, {"error": str(e)}
    
    def validate_data_with_validator_error_messages(
        self,
        data: Dict[str, Any],
        validators: Dict[str, List[Tuple[Callable[[Any], bool], str]]]
    ) -> Tuple[bool, Dict[str, str]]:
        """Validate data with validator error messages.
        
        Args:
            data: Data to validate
            validators: Custom validators with error messages
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        try:
            error_messages = {}
            
            for field, field_validators in validators.items():
                if field not in data:
                    error_messages[field] = "Field is required"
                    continue
                
                for validator, message in field_validators:
                    if not validator(data[field]):
                        error_messages[field] = message
                        break
            
            return len(error_messages) == 0, error_messages
        except Exception as e:
            return False, {"error": str(e)} 