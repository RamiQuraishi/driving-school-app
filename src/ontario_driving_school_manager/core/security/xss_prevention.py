"""
XSS Prevention Module

This module provides XSS prevention functionality.
It handles input sanitization and output encoding.

Author: Rami Drive School
Date: 2024
"""

import logging
import re
import html
import json
from typing import Dict, Any, Optional, List, Union, Callable
from dataclasses import dataclass
from enum import Enum
import os
from datetime import datetime
from bleach import clean
from markupsafe import Markup

logger = logging.getLogger(__name__)

class ContentType(Enum):
    """Content type."""
    HTML = "html"
    TEXT = "text"
    JSON = "json"
    URL = "url"
    CSS = "css"
    JAVASCRIPT = "javascript"

@dataclass
class SanitizationRule:
    """Sanitization rule."""
    pattern: str
    replacement: str
    content_type: ContentType
    description: str

class XSSPreventionManager:
    """XSS prevention manager."""
    
    def __init__(self):
        """Initialize XSS prevention manager."""
        # Allowed HTML tags
        self.allowed_tags = [
            "a", "abbr", "acronym", "b", "blockquote", "code",
            "em", "i", "li", "ol", "strong", "ul", "p", "br"
        ]
        
        # Allowed HTML attributes
        self.allowed_attrs = {
            "a": ["href", "title"],
            "abbr": ["title"],
            "acronym": ["title"]
        }
        
        # Allowed CSS properties
        self.allowed_styles = [
            "color", "background-color", "font-size", "font-weight",
            "text-align", "text-decoration", "margin", "padding"
        ]
        
        # Allowed URL schemes
        self.allowed_schemes = ["http", "https", "mailto", "tel"]
    
    def sanitize_input(
        self,
        content: str,
        content_type: str = "text/html"
    ) -> str:
        """Sanitize input content.
        
        Args:
            content: Content to sanitize
            content_type: Content type
            
        Returns:
            Sanitized content
        """
        if not content:
            return ""
        
        if content_type == "text/html":
            # Clean HTML
            return clean(
                content,
                tags=self.allowed_tags,
                attributes=self.allowed_attrs,
                styles=self.allowed_styles,
                protocols=self.allowed_schemes,
                strip=True
            )
        
        if content_type == "text/plain":
            # Escape HTML
            return html.escape(content)
        
        if content_type == "text/markdown":
            # Clean HTML after markdown conversion
            return clean(
                content,
                tags=self.allowed_tags,
                attributes=self.allowed_attrs,
                styles=self.allowed_styles,
                protocols=self.allowed_schemes,
                strip=True
            )
        
        # Default to plain text
        return html.escape(content)
    
    def encode_output(
        self,
        content: str,
        content_type: str = "text/html"
    ) -> str:
        """Encode output content.
        
        Args:
            content: Content to encode
            content_type: Content type
            
        Returns:
            Encoded content
        """
        if not content:
            return ""
        
        if content_type == "text/html":
            # Mark as safe HTML
            return Markup(content)
        
        if content_type == "text/plain":
            # Escape HTML
            return html.escape(content)
        
        if content_type == "text/markdown":
            # Mark as safe HTML after markdown conversion
            return Markup(content)
        
        # Default to plain text
        return html.escape(content)
    
    def sanitize_url(self, url: str) -> Optional[str]:
        """Sanitize URL.
        
        Args:
            url: URL to sanitize
            
        Returns:
            Sanitized URL if valid, None otherwise
        """
        if not url:
            return None
        
        # Remove whitespace
        url = url.strip()
        
        # Check if URL is valid
        if not re.match(
            r"^https?://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(?:/[^\s]*)?$",
            url
        ):
            return None
        
        return url
    
    def sanitize_email(self, email: str) -> Optional[str]:
        """Sanitize email address.
        
        Args:
            email: Email address to sanitize
            
        Returns:
            Sanitized email address if valid, None otherwise
        """
        if not email:
            return None
        
        # Remove whitespace
        email = email.strip()
        
        # Check if email is valid
        if not re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            email
        ):
            return None
        
        return email
    
    def sanitize_phone(self, phone: str) -> Optional[str]:
        """Sanitize phone number.
        
        Args:
            phone: Phone number to sanitize
            
        Returns:
            Sanitized phone number if valid, None otherwise
        """
        if not phone:
            return None
        
        # Remove non-digit characters
        phone = re.sub(r"\D", "", phone)
        
        # Check if phone number is valid
        if not re.match(r"^\d{10}$", phone):
            return None
        
        return phone
    
    def sanitize_postal_code(self, postal_code: str) -> Optional[str]:
        """Sanitize postal code.
        
        Args:
            postal_code: Postal code to sanitize
            
        Returns:
            Sanitized postal code if valid, None otherwise
        """
        if not postal_code:
            return None
        
        # Remove whitespace and convert to uppercase
        postal_code = postal_code.strip().upper()
        
        # Check if postal code is valid
        if not re.match(
            r"^[A-Z]\d[A-Z]\s?\d[A-Z]\d$",
            postal_code
        ):
            return None
        
        return postal_code
    
    def validate_input(
        self,
        content: str,
        content_type: ContentType,
        validation_rules: Optional[List[Callable[[str], bool]]] = None
    ) -> bool:
        """Validate input content.
        
        Args:
            content: Content to validate
            content_type: Content type
            validation_rules: Additional validation rules
            
        Returns:
            True if valid, False otherwise
        """
        # Sanitize content
        sanitized_content = self.sanitize_input(content, content_type.value)
        
        # Check if content was modified
        if sanitized_content != content:
            logger.warning(f"Content was modified during sanitization: {content}")
            return False
        
        # Apply additional validation rules
        if validation_rules:
            for rule in validation_rules:
                if not rule(content):
                    logger.warning(f"Content failed validation rule: {content}")
                    return False
        
        return True
    
    def add_sanitization_rule(
        self,
        pattern: str,
        replacement: str,
        content_type: ContentType,
        description: str
    ) -> None:
        """Add sanitization rule.
        
        Args:
            pattern: Regular expression pattern
            replacement: Replacement string
            content_type: Content type
            description: Rule description
        """
        rule = SanitizationRule(
            pattern=pattern,
            replacement=replacement,
            content_type=content_type,
            description=description
        )
        
        self.sanitization_rules.append(rule)
        
        logger.info(f"Added sanitization rule: {description}")
    
    def remove_sanitization_rule(
        self,
        pattern: str,
        content_type: ContentType
    ) -> None:
        """Remove sanitization rule.
        
        Args:
            pattern: Regular expression pattern
            content_type: Content type
        """
        self.sanitization_rules = [
            rule
            for rule in self.sanitization_rules
            if not (rule.pattern == pattern and rule.content_type == content_type)
        ]
        
        logger.info(f"Removed sanitization rule for pattern: {pattern}")
    
    def get_sanitization_rules(
        self,
        content_type: Optional[ContentType] = None
    ) -> List[SanitizationRule]:
        """Get sanitization rules.
        
        Args:
            content_type: Content type
            
        Returns:
            List of sanitization rules
        """
        if content_type:
            return [
                rule
                for rule in self.sanitization_rules
                if rule.content_type == content_type
            ]
        
        return self.sanitization_rules
    
    def get_sanitization_stats(
        self
    ) -> Dict[str, Any]:
        """Get sanitization statistics.
        
        Returns:
            Sanitization statistics dictionary
        """
        stats = {
            "total_rules": len(self.sanitization_rules),
            "content_types": {
                content_type.value: len([
                    rule
                    for rule in self.sanitization_rules
                    if rule.content_type == content_type
                ])
                for content_type in ContentType
            }
        }
        
        return stats
    
    def export_sanitization_rules(
        self,
        format: str = "json"
    ) -> str:
        """Export sanitization rules.
        
        Args:
            format: Export format
            
        Returns:
            Path to exported file
            
        Raises:
            ValueError: If format is not supported
        """
        if format != "json":
            raise ValueError(f"Unsupported format: {format}")
        
        # Create export directory
        export_dir = "xss_rules"
        os.makedirs(export_dir, exist_ok=True)
        
        # Create export file path
        export_file = os.path.join(
            export_dir,
            f"sanitization_rules_{datetime.now().strftime('%Y%m%d')}.{format}"
        )
        
        # Export rules
        rules_data = [
            {
                "pattern": rule.pattern,
                "replacement": rule.replacement,
                "content_type": rule.content_type.value,
                "description": rule.description
            }
            for rule in self.sanitization_rules
        ]
        
        with open(export_file, "w") as f:
            json.dump(rules_data, f, indent=2)
        
        return export_file 