"""
MTO Utilities Module

This module provides utility functions for MTO data handling.
It includes formatting, validation, and conversion functions.

Author: Rami Drive School
Date: 2024
"""

import re
from typing import Optional, Union, Dict, Any
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

def format_license_number(
    license_number: str,
    format_type: str = "standard"
) -> str:
    """Format license number.
    
    Args:
        license_number: License number
        format_type: Format type (standard, compact, display)
        
    Returns:
        Formatted license number
    """
    # Remove any non-alphanumeric characters
    license_number = re.sub(r"[^A-Z0-9]", "", license_number.upper())
    
    if format_type == "standard":
        # Format: A1234-567890-12345
        if len(license_number) == 15:
            return (
                f"{license_number[0]}{license_number[1:5]}-"
                f"{license_number[5:11]}-{license_number[11:]}"
            )
    elif format_type == "compact":
        # Format: A123456789012345
        return license_number
    elif format_type == "display":
        # Format: A 1234 567890 12345
        if len(license_number) == 15:
            return (
                f"{license_number[0]} {license_number[1:5]} "
                f"{license_number[5:11]} {license_number[11:]}"
            )
    
    return license_number

def validate_postal_code(
    postal_code: str,
    strict: bool = True
) -> bool:
    """Validate postal code.
    
    Args:
        postal_code: Postal code
        strict: Whether to use strict validation
        
    Returns:
        True if valid, False otherwise
    """
    if strict:
        # Format: A1A 1A1
        pattern = r"^[A-Z]\d[A-Z] \d[A-Z]\d$"
    else:
        # Format: A1A1A1
        pattern = r"^[A-Z]\d[A-Z]\d[A-Z]\d$"
    
    return bool(re.match(pattern, postal_code.upper()))

def format_postal_code(
    postal_code: str,
    format_type: str = "standard"
) -> str:
    """Format postal code.
    
    Args:
        postal_code: Postal code
        format_type: Format type (standard, compact)
        
    Returns:
        Formatted postal code
    """
    # Remove any non-alphanumeric characters
    postal_code = re.sub(r"[^A-Z0-9]", "", postal_code.upper())
    
    if len(postal_code) != 6:
        return postal_code
    
    if format_type == "standard":
        # Format: A1A 1A1
        return f"{postal_code[0:3]} {postal_code[3:]}"
    elif format_type == "compact":
        # Format: A1A1A1
        return postal_code
    
    return postal_code

def validate_phone_number(
    phone_number: str,
    format_type: str = "standard"
) -> bool:
    """Validate phone number.
    
    Args:
        phone_number: Phone number
        format_type: Format type (standard, compact)
        
    Returns:
        True if valid, False otherwise
    """
    # Remove any non-numeric characters
    phone_number = re.sub(r"[^0-9]", "", phone_number)
    
    if len(phone_number) != 10:
        return False
    
    if format_type == "standard":
        # Format: (123) 456-7890
        pattern = r"^\(\d{3}\) \d{3}-\d{4}$"
    elif format_type == "compact":
        # Format: 1234567890
        pattern = r"^\d{10}$"
    
    return bool(re.match(pattern, phone_number))

def format_phone_number(
    phone_number: str,
    format_type: str = "standard"
) -> str:
    """Format phone number.
    
    Args:
        phone_number: Phone number
        format_type: Format type (standard, compact)
        
    Returns:
        Formatted phone number
    """
    # Remove any non-numeric characters
    phone_number = re.sub(r"[^0-9]", "", phone_number)
    
    if len(phone_number) != 10:
        return phone_number
    
    if format_type == "standard":
        # Format: (123) 456-7890
        return f"({phone_number[0:3]}) {phone_number[3:6]}-{phone_number[6:]}"
    elif format_type == "compact":
        # Format: 1234567890
        return phone_number
    
    return phone_number

def validate_date(
    date_str: str,
    format_type: str = "standard"
) -> bool:
    """Validate date.
    
    Args:
        date_str: Date string
        format_type: Format type (standard, compact)
        
    Returns:
        True if valid, False otherwise
    """
    if format_type == "standard":
        # Format: YYYY-MM-DD
        pattern = r"^\d{4}-\d{2}-\d{2}$"
    elif format_type == "compact":
        # Format: YYYYMMDD
        pattern = r"^\d{8}$"
    
    if not re.match(pattern, date_str):
        return False
    
    try:
        if format_type == "standard":
            datetime.strptime(date_str, "%Y-%m-%d")
        else:
            datetime.strptime(date_str, "%Y%m%d")
        return True
    except ValueError:
        return False

def format_date(
    date_obj: Union[datetime, date],
    format_type: str = "standard"
) -> str:
    """Format date.
    
    Args:
        date_obj: Date object
        format_type: Format type (standard, compact)
        
    Returns:
        Formatted date string
    """
    if format_type == "standard":
        # Format: YYYY-MM-DD
        return date_obj.strftime("%Y-%m-%d")
    elif format_type == "compact":
        # Format: YYYYMMDD
        return date_obj.strftime("%Y%m%d")
    
    return str(date_obj)

def validate_time(
    time_str: str,
    format_type: str = "standard"
) -> bool:
    """Validate time.
    
    Args:
        time_str: Time string
        format_type: Format type (standard, compact)
        
    Returns:
        True if valid, False otherwise
    """
    if format_type == "standard":
        # Format: HH:MM:SS
        pattern = r"^\d{2}:\d{2}:\d{2}$"
    elif format_type == "compact":
        # Format: HHMMSS
        pattern = r"^\d{6}$"
    
    if not re.match(pattern, time_str):
        return False
    
    try:
        if format_type == "standard":
            datetime.strptime(time_str, "%H:%M:%S")
        else:
            datetime.strptime(time_str, "%H%M%S")
        return True
    except ValueError:
        return False

def format_time(
    time_obj: datetime,
    format_type: str = "standard"
) -> str:
    """Format time.
    
    Args:
        time_obj: Time object
        format_type: Format type (standard, compact)
        
    Returns:
        Formatted time string
    """
    if format_type == "standard":
        # Format: HH:MM:SS
        return time_obj.strftime("%H:%M:%S")
    elif format_type == "compact":
        # Format: HHMMSS
        return time_obj.strftime("%H%M%S")
    
    return str(time_obj)

def validate_datetime(
    datetime_str: str,
    format_type: str = "standard"
) -> bool:
    """Validate datetime.
    
    Args:
        datetime_str: Datetime string
        format_type: Format type (standard, compact)
        
    Returns:
        True if valid, False otherwise
    """
    if format_type == "standard":
        # Format: YYYY-MM-DD HH:MM:SS
        pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
    elif format_type == "compact":
        # Format: YYYYMMDDHHMMSS
        pattern = r"^\d{14}$"
    
    if not re.match(pattern, datetime_str):
        return False
    
    try:
        if format_type == "standard":
            datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        else:
            datetime.strptime(datetime_str, "%Y%m%d%H%M%S")
        return True
    except ValueError:
        return False

def format_datetime(
    datetime_obj: datetime,
    format_type: str = "standard"
) -> str:
    """Format datetime.
    
    Args:
        datetime_obj: Datetime object
        format_type: Format type (standard, compact)
        
    Returns:
        Formatted datetime string
    """
    if format_type == "standard":
        # Format: YYYY-MM-DD HH:MM:SS
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    elif format_type == "compact":
        # Format: YYYYMMDDHHMMSS
        return datetime_obj.strftime("%Y%m%d%H%M%S")
    
    return str(datetime_obj)

def validate_currency(
    amount: Union[str, float],
    format_type: str = "standard"
) -> bool:
    """Validate currency amount.
    
    Args:
        amount: Currency amount
        format_type: Format type (standard, compact)
        
    Returns:
        True if valid, False otherwise
    """
    if isinstance(amount, str):
        if format_type == "standard":
            # Format: 1234.56
            pattern = r"^\d+\.\d{2}$"
        elif format_type == "compact":
            # Format: 123456
            pattern = r"^\d+$"
        
        if not re.match(pattern, amount):
            return False
        
        try:
            float(amount)
            return True
        except ValueError:
            return False
    
    return isinstance(amount, (int, float))

def format_currency(
    amount: Union[str, float],
    format_type: str = "standard"
) -> str:
    """Format currency amount.
    
    Args:
        amount: Currency amount
        format_type: Format type (standard, compact)
        
    Returns:
        Formatted currency string
    """
    if isinstance(amount, str):
        try:
            amount = float(amount)
        except ValueError:
            return amount
    
    if format_type == "standard":
        # Format: 1234.56
        return f"{amount:.2f}"
    elif format_type == "compact":
        # Format: 123456
        return f"{int(amount * 100)}"
    
    return str(amount)

def validate_percentage(
    percentage: Union[str, float],
    format_type: str = "standard"
) -> bool:
    """Validate percentage.
    
    Args:
        percentage: Percentage value
        format_type: Format type (standard, compact)
        
    Returns:
        True if valid, False otherwise
    """
    if isinstance(percentage, str):
        if format_type == "standard":
            # Format: 12.34%
            pattern = r"^\d+\.\d{2}%$"
        elif format_type == "compact":
            # Format: 1234
            pattern = r"^\d+$"
        
        if not re.match(pattern, percentage):
            return False
        
        try:
            float(percentage.rstrip("%"))
            return True
        except ValueError:
            return False
    
    return isinstance(percentage, (int, float))

def format_percentage(
    percentage: Union[str, float],
    format_type: str = "standard"
) -> str:
    """Format percentage.
    
    Args:
        percentage: Percentage value
        format_type: Format type (standard, compact)
        
    Returns:
        Formatted percentage string
    """
    if isinstance(percentage, str):
        try:
            percentage = float(percentage.rstrip("%"))
        except ValueError:
            return percentage
    
    if format_type == "standard":
        # Format: 12.34%
        return f"{percentage:.2f}%"
    elif format_type == "compact":
        # Format: 1234
        return f"{int(percentage * 100)}"
    
    return str(percentage) 