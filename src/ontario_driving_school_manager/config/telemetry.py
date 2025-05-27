"""
Telemetry configuration.
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class TelemetryConfig(BaseModel):
    """Telemetry configuration."""
    
    # Basic settings
    enabled: bool = True
    anonymous: bool = True
    collection_interval: int = 3600  # 1 hour
    
    # Data collection settings
    collect_usage_stats: bool = True
    collect_performance_metrics: bool = True
    collect_error_reports: bool = True
    
    # Privacy settings
    data_retention_days: int = 30
    anonymize_ip: bool = True
    exclude_pii: bool = True
    
    # Endpoint configuration
    endpoint: str = "https://telemetry.ontariodrivingschool.com"
    api_key: Optional[str] = None
    
    # Advanced settings
    batch_size: int = 100
    max_retries: int = 3
    timeout: int = 30
    
    # Custom dimensions
    custom_dimensions: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        """Pydantic config."""
        env_prefix = "TELEMETRY_"

# Create telemetry config instance
telemetry_config = TelemetryConfig() 