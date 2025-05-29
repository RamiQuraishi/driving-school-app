"""Core application services and utilities.

This package provides core functionality for the Ontario Driving School Manager,
including:
- Exception handling
- Event management
- Constants and configuration
- Version control
- MTO compliance utilities
"""

from .exceptions import (
    ODSMError,
    ValidationError,
    DatabaseError,
    MTOComplianceError,
    BusinessRuleError
)
from .events import (
    EventBus,
    EventHandler,
    EventType,
    Event
)
from .constants import (
    MTO_REQUIREMENTS,
    DRIVING_ZONE_TYPES,
    LESSON_TYPES,
    PAYMENT_STATUSES,
    VEHICLE_TYPES
)
from .versioning import (
    VersionManager,
    VersionConflictError,
    VersionInfo
)

__all__ = [
    # Exceptions
    "ODSMError",
    "ValidationError",
    "DatabaseError",
    "MTOComplianceError",
    "BusinessRuleError",
    
    # Events
    "EventBus",
    "EventHandler",
    "EventType",
    "Event",
    
    # Constants
    "MTO_REQUIREMENTS",
    "DRIVING_ZONE_TYPES",
    "LESSON_TYPES",
    "PAYMENT_STATUSES",
    "VEHICLE_TYPES",
    
    # Versioning
    "VersionManager",
    "VersionConflictError",
    "VersionInfo"
] 