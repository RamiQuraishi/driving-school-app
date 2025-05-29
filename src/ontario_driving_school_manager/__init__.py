"""
Ontario Driving School Manager

A comprehensive management system for driving schools in Ontario.
Provides tools for managing students, instructors, lessons, and MTO compliance.

Author: Rami Drive School
Date: 2024
"""

__version__ = "1.0.0"
__author__ = "Rami Drive School"
__license__ = "Proprietary"

from .core.analytics import PrivacyCompliantAnalytics, TelemetryService
from .core.monitoring import (
    PerformanceTracker,
    ErrorTracker,
    ConflictTracker,
    BusinessMetrics,
    HealthChecker
)

__all__ = [
    'PrivacyCompliantAnalytics',
    'TelemetryService',
    'PerformanceTracker',
    'ErrorTracker',
    'ConflictTracker',
    'BusinessMetrics',
    'HealthChecker'
] 