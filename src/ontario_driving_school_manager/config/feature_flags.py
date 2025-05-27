"""
Feature flags configuration.
"""
from typing import Dict, Any
from pydantic import BaseModel

class FeatureFlags(BaseModel):
    """Feature flags configuration."""
    
    # Feature flags
    ENABLE_ANALYTICS: bool = True
    ENABLE_TELEMETRY: bool = True
    ENABLE_PERFORMANCE_MONITORING: bool = True
    ENABLE_ERROR_TRACKING: bool = True
    ENABLE_CONFLICT_TRACKING: bool = True
    
    # Feature toggles
    ENABLE_BETA_FEATURES: bool = False
    ENABLE_EXPERIMENTAL_FEATURES: bool = False
    
    # Feature configurations
    ANALYTICS_CONFIG: Dict[str, Any] = {
        "enabled": True,
        "privacy_compliant": True,
        "data_retention_days": 30
    }
    
    TELEMETRY_CONFIG: Dict[str, Any] = {
        "enabled": True,
        "anonymous": True,
        "collection_interval": 3600  # 1 hour
    }
    
    MONITORING_CONFIG: Dict[str, Any] = {
        "enabled": True,
        "performance_tracking": True,
        "error_tracking": True,
        "conflict_tracking": True
    }

# Create feature flags instance
feature_flags = FeatureFlags() 