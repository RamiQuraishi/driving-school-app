"""
Shared Constants

This package provides shared constants for both Python and TypeScript.
It ensures consistent values across the application.

Author: Rami Drive School
Date: 2024
"""

# API Constants
API_BASE_URL = "http://localhost:8000"
API_VERSION = "v1"

# Application Constants
APP_NAME = "Ontario Driving School Manager"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Rami Drive School"

# Feature Flags
FEATURES = {
    "ENABLE_ANALYTICS": True,
    "ENABLE_TELEMETRY": True,
    "ENABLE_SYNC": True,
    "ENABLE_OFFLINE_MODE": True
}

# Validation Constants
MAX_NAME_LENGTH = 100
MAX_EMAIL_LENGTH = 255
MAX_PHONE_LENGTH = 20
MAX_ADDRESS_LENGTH = 200

# Business Rules
MIN_LESSON_DURATION = 30  # minutes
MAX_LESSON_DURATION = 120  # minutes
MIN_STUDENT_AGE = 16
MAX_INSTRUCTOR_STUDENTS = 20

# File Paths
DATA_DIR = ".ontario_driving_school"
LOG_DIR = "logs"
EXPORT_DIR = "exports"
BACKUP_DIR = "backups"

# Time Constants
DEFAULT_TIMEZONE = "America/Toronto"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"

__all__ = [
    'API_BASE_URL',
    'API_VERSION',
    'APP_NAME',
    'APP_VERSION',
    'APP_AUTHOR',
    'FEATURES',
    'MAX_NAME_LENGTH',
    'MAX_EMAIL_LENGTH',
    'MAX_PHONE_LENGTH',
    'MAX_ADDRESS_LENGTH',
    'MIN_LESSON_DURATION',
    'MAX_LESSON_DURATION',
    'MIN_STUDENT_AGE',
    'MAX_INSTRUCTOR_STUDENTS',
    'DATA_DIR',
    'LOG_DIR',
    'EXPORT_DIR',
    'BACKUP_DIR',
    'DEFAULT_TIMEZONE',
    'DATE_FORMAT',
    'TIME_FORMAT',
    'DATETIME_FORMAT'
] 