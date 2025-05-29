"""
Circuit breaker configuration for Ontario Driving School Manager.
Handles fault tolerance and service resilience settings.
"""

import logging
from typing import Dict, Any, Optional
from pydantic import BaseSettings, Field
import os

logger = logging.getLogger(__name__)

class CircuitBreakerConfig(BaseSettings):
    """Circuit breaker configuration settings."""
    
    # General settings
    ENABLED: bool = Field(default=True, env="CIRCUIT_BREAKER_ENABLED")
    THRESHOLD: int = Field(default=5, env="CIRCUIT_BREAKER_THRESHOLD")
    TIMEOUT: int = Field(default=60, env="CIRCUIT_BREAKER_TIMEOUT")  # seconds
    HALF_OPEN_TIMEOUT: int = Field(default=30, env="CIRCUIT_BREAKER_HALF_OPEN_TIMEOUT")  # seconds
    
    # Service settings
    SERVICES: Dict[str, Dict[str, Any]] = Field(
        default={
            "database": {
                "enabled": True,
                "threshold": 5,
                "timeout": 60,
                "half_open_timeout": 30
            },
            "api": {
                "enabled": True,
                "threshold": 3,
                "timeout": 30,
                "half_open_timeout": 15
            },
            "cache": {
                "enabled": True,
                "threshold": 5,
                "timeout": 30,
                "half_open_timeout": 15
            }
        },
        env="CIRCUIT_BREAKER_SERVICES"
    )
    
    # Monitoring settings
    ENABLE_METRICS: bool = Field(default=True, env="CIRCUIT_BREAKER_ENABLE_METRICS")
    ENABLE_LOGGING: bool = Field(default=True, env="CIRCUIT_BREAKER_ENABLE_LOGGING")
    LOG_LEVEL: str = Field(default="INFO", env="CIRCUIT_BREAKER_LOG_LEVEL")
    
    # Recovery settings
    AUTO_RECOVERY: bool = Field(default=True, env="CIRCUIT_BREAKER_AUTO_RECOVERY")
    RECOVERY_TIMEOUT: int = Field(default=300, env="CIRCUIT_BREAKER_RECOVERY_TIMEOUT")  # 5 minutes
    MAX_RECOVERY_ATTEMPTS: int = Field(default=3, env="CIRCUIT_BREAKER_MAX_RECOVERY_ATTEMPTS")
    
    # Fallback settings
    ENABLE_FALLBACK: bool = Field(default=True, env="CIRCUIT_BREAKER_ENABLE_FALLBACK")
    FALLBACK_TIMEOUT: int = Field(default=10, env="CIRCUIT_BREAKER_FALLBACK_TIMEOUT")  # seconds
    
    # Debug settings
    DEBUG_MODE: bool = Field(default=False, env="CIRCUIT_BREAKER_DEBUG_MODE")
    VERBOSE_LOGGING: bool = Field(default=False, env="CIRCUIT_BREAKER_VERBOSE_LOGGING")
    
    class Config:
        """Pydantic model configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    def get_service_config(self, service_name: str) -> Dict[str, Any]:
        """Get configuration for a specific service."""
        return self.SERVICES.get(service_name, {})
    
    def is_service_enabled(self, service_name: str) -> bool:
        """Check if circuit breaker is enabled for a service."""
        service_config = self.get_service_config(service_name)
        return self.ENABLED and service_config.get("enabled", False)
    
    def get_service_threshold(self, service_name: str) -> int:
        """Get failure threshold for a service."""
        service_config = self.get_service_config(service_name)
        return service_config.get("threshold", self.THRESHOLD)
    
    def get_service_timeout(self, service_name: str) -> int:
        """Get timeout for a service."""
        service_config = self.get_service_config(service_name)
        return service_config.get("timeout", self.TIMEOUT)
    
    def get_service_half_open_timeout(self, service_name: str) -> int:
        """Get half-open timeout for a service."""
        service_config = self.get_service_config(service_name)
        return service_config.get("half_open_timeout", self.HALF_OPEN_TIMEOUT)
    
    def get_monitoring_config(self) -> Dict[str, Any]:
        """Get monitoring configuration."""
        return {
            "enable_metrics": self.ENABLE_METRICS,
            "enable_logging": self.ENABLE_LOGGING,
            "log_level": self.LOG_LEVEL
        }
    
    def get_recovery_config(self) -> Dict[str, Any]:
        """Get recovery configuration."""
        return {
            "auto_recovery": self.AUTO_RECOVERY,
            "recovery_timeout": self.RECOVERY_TIMEOUT,
            "max_recovery_attempts": self.MAX_RECOVERY_ATTEMPTS
        }
    
    def get_fallback_config(self) -> Dict[str, Any]:
        """Get fallback configuration."""
        return {
            "enable_fallback": self.ENABLE_FALLBACK,
            "fallback_timeout": self.FALLBACK_TIMEOUT
        }
    
    def validate_config(self) -> bool:
        """Validate circuit breaker configuration."""
        try:
            if self.ENABLED:
                if self.THRESHOLD < 1:
                    logger.error("Threshold must be at least 1")
                    return False
                
                if self.TIMEOUT < 1:
                    logger.error("Timeout must be at least 1 second")
                    return False
                
                if self.HALF_OPEN_TIMEOUT < 1:
                    logger.error("Half-open timeout must be at least 1 second")
                    return False
                
                if self.RECOVERY_TIMEOUT < 1:
                    logger.error("Recovery timeout must be at least 1 second")
                    return False
                
                if self.MAX_RECOVERY_ATTEMPTS < 1:
                    logger.error("Max recovery attempts must be at least 1")
                    return False
                
                if self.FALLBACK_TIMEOUT < 1:
                    logger.error("Fallback timeout must be at least 1 second")
                    return False
                
                for service_name, service_config in self.SERVICES.items():
                    if not isinstance(service_config, dict):
                        logger.error(f"Invalid service configuration for {service_name}")
                        return False
                    
                    if "threshold" in service_config and service_config["threshold"] < 1:
                        logger.error(f"Invalid threshold for service {service_name}")
                        return False
                    
                    if "timeout" in service_config and service_config["timeout"] < 1:
                        logger.error(f"Invalid timeout for service {service_name}")
                        return False
                    
                    if "half_open_timeout" in service_config and service_config["half_open_timeout"] < 1:
                        logger.error(f"Invalid half-open timeout for service {service_name}")
                        return False
            
            return True
        
        except Exception as e:
            logger.error(f"Error validating circuit breaker configuration: {str(e)}")
            return False 