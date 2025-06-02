"""
Privacy Module

This module provides privacy management functionality for PIPEDA compliance.
It includes consent management, data retention, breach notification,
privacy officer tools, data export, and telemetry consent.

Author: Rami Drive School
Date: 2024
"""

from .consent_manager import ConsentManager
from .data_retention import DataRetentionManager
from .breach_notification import BreachNotificationManager
from .privacy_officer import PrivacyOfficer
from .data_export import DataExportManager
from .telemetry_consent import TelemetryConsentManager

__all__ = [
    "ConsentManager",
    "DataRetentionManager",
    "BreachNotificationManager",
    "PrivacyOfficer",
    "DataExportManager",
    "TelemetryConsentManager"
] 