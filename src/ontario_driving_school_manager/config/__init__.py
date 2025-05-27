"""
Configuration package for Ontario Driving School Manager.
"""
from .settings import Settings
from .feature_flags import FeatureFlags
from .telemetry import TelemetryConfig

__all__ = ['Settings', 'FeatureFlags', 'TelemetryConfig'] 