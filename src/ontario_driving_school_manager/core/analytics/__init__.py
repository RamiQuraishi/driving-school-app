"""
Analytics Package

This package provides analytics and telemetry functionality for the Ontario Driving School Manager.
It includes privacy-compliant analytics and anonymous telemetry services.

Author: Rami Drive School
Date: 2024
"""

from .privacy_compliant_analytics import PrivacyCompliantAnalytics
from .telemetry_service import TelemetryService

__all__ = [
    'PrivacyCompliantAnalytics',
    'TelemetryService'
] 