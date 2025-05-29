"""Constants and configuration for the Ontario Driving School Manager."""

from enum import Enum
from typing import Dict, List

# MTO Requirements
MTO_REQUIREMENTS = {
    "instructor": {
        "min_age": 21,
        "min_experience_years": 3,
        "certification_validity_days": 365,
        "background_check_required": True,
        "medical_check_required": True,
        "min_lessons_per_week": 20
    },
    "vehicle": {
        "min_safety_rating": 4,
        "inspection_frequency_days": 180,
        "dual_controls_required": True,
        "min_airbags": 6,
        "gps_tracking_required": True
    },
    "school": {
        "min_instructors": 2,
        "min_vehicles": 2,
        "insurance_coverage_min": 2000000,
        "business_hours_min": 40,
        "student_ratio_max": 20
    }
}

# Driving Zone Types
class DrivingZoneType(Enum):
    """Types of driving zones."""
    
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    HIGHWAY = "highway"
    CITY = "city"
    RESIDENTIAL = "residential"
    SCHOOL = "school"
    PROHIBITED = "prohibited"

DRIVING_ZONE_TYPES = [zone.value for zone in DrivingZoneType]

# Lesson Types
class LessonType(Enum):
    """Types of driving lessons."""
    
    THEORY = "theory"
    PRACTICAL = "practical"
    HIGHWAY = "highway"
    NIGHT = "night"
    PARKING = "parking"
    EMERGENCY = "emergency"
    EVALUATION = "evaluation"

LESSON_TYPES = [lesson.value for lesson in LessonType]

# Payment Statuses
class PaymentStatus(Enum):
    """Payment statuses."""
    
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"
    PARTIAL = "partial"

PAYMENT_STATUSES = [status.value for status in PaymentStatus]

# Vehicle Types
class VehicleType(Enum):
    """Types of vehicles."""
    
    SEDAN = "sedan"
    SUV = "suv"
    HATCHBACK = "hatchback"
    CROSSOVER = "crossover"
    ELECTRIC = "electric"
    HYBRID = "hybrid"

VEHICLE_TYPES = [vehicle.value for vehicle in VehicleType]

# Business Rules
BUSINESS_RULES = {
    "lesson": {
        "min_duration_minutes": 45,
        "max_duration_minutes": 120,
        "min_break_minutes": 15,
        "max_lessons_per_day": 8,
        "cancellation_hours": 24
    },
    "payment": {
        "min_deposit_percent": 20,
        "payment_terms_days": 30,
        "late_fee_percent": 5,
        "refund_days": 7
    },
    "scheduling": {
        "min_notice_hours": 24,
        "max_advance_days": 30,
        "buffer_minutes": 15
    }
}

# System Configuration
SYSTEM_CONFIG = {
    "gps": {
        "tracking_interval_seconds": 30,
        "retention_days": 90,
        "accuracy_meters": 10
    },
    "notifications": {
        "email_enabled": True,
        "sms_enabled": True,
        "push_enabled": True
    },
    "security": {
        "password_min_length": 8,
        "session_timeout_minutes": 30,
        "max_login_attempts": 5
    }
}

# Feature Flags
FEATURE_FLAGS = {
    "gps_tracking": True,
    "online_booking": True,
    "payment_processing": True,
    "student_portal": True,
    "instructor_app": True,
    "analytics": True
}

# Error Messages
ERROR_MESSAGES = {
    "validation": {
        "required_field": "Field {field} is required",
        "invalid_format": "Invalid format for field {field}",
        "invalid_value": "Invalid value for field {field}"
    },
    "business": {
        "insufficient_funds": "Insufficient funds for payment",
        "invalid_schedule": "Invalid schedule configuration",
        "booking_conflict": "Booking conflict detected"
    },
    "system": {
        "database_error": "Database operation failed",
        "network_error": "Network connection failed",
        "permission_denied": "Permission denied"
    }
}

# API Endpoints
API_ENDPOINTS = {
    "students": "/api/v1/students",
    "instructors": "/api/v1/instructors",
    "vehicles": "/api/v1/vehicles",
    "lessons": "/api/v1/lessons",
    "payments": "/api/v1/payments",
    "reports": "/api/v1/reports"
}

# File Paths
FILE_PATHS = {
    "logs": "logs",
    "reports": "reports",
    "exports": "exports",
    "uploads": "uploads",
    "temp": "temp"
}

# Cache Configuration
CACHE_CONFIG = {
    "default_ttl": 3600,
    "max_size": 1000,
    "cleanup_interval": 300
} 