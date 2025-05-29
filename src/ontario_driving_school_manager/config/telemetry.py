"""
Telemetry configuration for Ontario Driving School Manager.
Handles application metrics, monitoring, and analytics.
"""

import logging
from typing import Dict, Any, Optional
from pydantic import BaseSettings, Field
import os

logger = logging.getLogger(__name__)

class TelemetryConfig(BaseSettings):
    """Telemetry configuration settings."""
    
    # General settings
    ENABLED: bool = Field(default=True, env="TELEMETRY_ENABLED")
    ENDPOINT: str = Field(default="https://telemetry.example.com", env="TELEMETRY_ENDPOINT")
    API_KEY: Optional[str] = Field(None, env="TELEMETRY_API_KEY")
    
    # Collection settings
    COLLECTION_INTERVAL: int = Field(default=60, env="TELEMETRY_COLLECTION_INTERVAL")  # seconds
    BATCH_SIZE: int = Field(default=100, env="TELEMETRY_BATCH_SIZE")
    MAX_RETRIES: int = Field(default=3, env="TELEMETRY_MAX_RETRIES")
    
    # Metrics settings
    ENABLE_SYSTEM_METRICS: bool = Field(default=True, env="TELEMETRY_ENABLE_SYSTEM_METRICS")
    ENABLE_PERFORMANCE_METRICS: bool = Field(default=True, env="TELEMETRY_ENABLE_PERFORMANCE_METRICS")
    ENABLE_ERROR_TRACKING: bool = Field(default=True, env="TELEMETRY_ENABLE_ERROR_TRACKING")
    ENABLE_USER_ACTIVITY: bool = Field(default=True, env="TELEMETRY_ENABLE_USER_ACTIVITY")
    
    # Privacy settings
    ANONYMIZE_DATA: bool = Field(default=True, env="TELEMETRY_ANONYMIZE_DATA")
    SAMPLE_RATE: float = Field(default=1.0, env="TELEMETRY_SAMPLE_RATE")  # 0.0 to 1.0
    
    # Storage settings
    LOCAL_STORAGE_ENABLED: bool = Field(default=True, env="TELEMETRY_LOCAL_STORAGE_ENABLED")
    LOCAL_STORAGE_PATH: str = Field(default="telemetry", env="TELEMETRY_LOCAL_STORAGE_PATH")
    MAX_STORAGE_SIZE: int = Field(default=100 * 1024 * 1024, env="TELEMETRY_MAX_STORAGE_SIZE")  # 100MB
    
    # Debug settings
    DEBUG_MODE: bool = Field(default=False, env="TELEMETRY_DEBUG_MODE")
    VERBOSE_LOGGING: bool = Field(default=False, env="TELEMETRY_VERBOSE_LOGGING")
    
    class Config:
        """Pydantic model configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    def is_enabled(self) -> bool:
        """Check if telemetry is enabled."""
        return self.ENABLED and bool(self.ENDPOINT)
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers for telemetry requests."""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "OntarioDrivingSchoolManager/1.0.0"
        }
        if self.API_KEY:
            headers["Authorization"] = f"Bearer {self.API_KEY}"
        return headers
    
    def get_collection_config(self) -> Dict[str, Any]:
        """Get collection configuration."""
        return {
            "interval": self.COLLECTION_INTERVAL,
            "batch_size": self.BATCH_SIZE,
            "max_retries": self.MAX_RETRIES,
            "sample_rate": self.SAMPLE_RATE
        }
    
    def get_metrics_config(self) -> Dict[str, bool]:
        """Get metrics collection configuration."""
        return {
            "system_metrics": self.ENABLE_SYSTEM_METRICS,
            "performance_metrics": self.ENABLE_PERFORMANCE_METRICS,
            "error_tracking": self.ENABLE_ERROR_TRACKING,
            "user_activity": self.ENABLE_USER_ACTIVITY
        }
    
    def get_storage_config(self) -> Dict[str, Any]:
        """Get storage configuration."""
        return {
            "enabled": self.LOCAL_STORAGE_ENABLED,
            "path": self.LOCAL_STORAGE_PATH,
            "max_size": self.MAX_STORAGE_SIZE
        }
    
    def validate_config(self) -> bool:
        """Validate telemetry configuration."""
        try:
            if self.ENABLED and not self.ENDPOINT:
                logger.error("Telemetry endpoint is required when telemetry is enabled")
                return False
            
            if self.SAMPLE_RATE < 0.0 or self.SAMPLE_RATE > 1.0:
                logger.error("Sample rate must be between 0.0 and 1.0")
                return False
            
            if self.COLLECTION_INTERVAL < 1:
                logger.error("Collection interval must be at least 1 second")
                return False
            
            if self.BATCH_SIZE < 1:
                logger.error("Batch size must be at least 1")
                return False
            
            return True
        
        except Exception as e:
            logger.error(f"Error validating telemetry configuration: {str(e)}")
            return False 