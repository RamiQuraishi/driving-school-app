"""
Main settings configuration for Ontario Driving School Manager.
Handles application-wide settings and environment configuration.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseSettings, Field, validator
import yaml

class Settings(BaseSettings):
    """Application settings configuration."""
    
    # Application
    APP_NAME: str = "Ontario Driving School Manager"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DATABASE_POOL_SIZE: int = Field(default=5, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=10, env="DATABASE_MAX_OVERFLOW")
    
    # API
    API_HOST: str = Field(default="localhost", env="API_HOST")
    API_PORT: int = Field(default=8000, env="API_PORT")
    API_PREFIX: str = Field(default="/api/v1", env="API_PREFIX")
    
    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    
    # File Storage
    UPLOAD_DIR: Path = Field(default=Path("uploads"), env="UPLOAD_DIR")
    MAX_UPLOAD_SIZE: int = Field(default=10 * 1024 * 1024, env="MAX_UPLOAD_SIZE")  # 10MB
    
    # Email
    SMTP_HOST: str = Field(default="smtp.gmail.com", env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USER: str = Field(..., env="SMTP_USER")
    SMTP_PASSWORD: str = Field(..., env="SMTP_PASSWORD")
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    REDIS_PASSWORD: Optional[str] = Field(None, env="REDIS_PASSWORD")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT")
    
    # Feature Flags
    FEATURE_FLAGS_FILE: str = Field(default="feature_flags.yaml", env="FEATURE_FLAGS_FILE")
    
    # Telemetry
    ENABLE_TELEMETRY: bool = Field(default=True, env="ENABLE_TELEMETRY")
    TELEMETRY_ENDPOINT: str = Field(default="https://telemetry.example.com", env="TELEMETRY_ENDPOINT")
    
    # Cache
    CACHE_TYPE: str = Field(default="redis", env="CACHE_TYPE")
    CACHE_TTL: int = Field(default=3600, env="CACHE_TTL")  # 1 hour
    
    # Circuit Breaker
    CIRCUIT_BREAKER_ENABLED: bool = Field(default=True, env="CIRCUIT_BREAKER_ENABLED")
    CIRCUIT_BREAKER_THRESHOLD: int = Field(default=5, env="CIRCUIT_BREAKER_THRESHOLD")
    CIRCUIT_BREAKER_TIMEOUT: int = Field(default=60, env="CIRCUIT_BREAKER_TIMEOUT")  # 60 seconds
    
    class Config:
        """Pydantic model configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    @validator("UPLOAD_DIR")
    def create_upload_dir(cls, v: Path) -> Path:
        """Create upload directory if it doesn't exist."""
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    @validator("ENVIRONMENT")
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        valid_environments = ["development", "testing", "staging", "production"]
        if v not in valid_environments:
            raise ValueError(f"Environment must be one of: {', '.join(valid_environments)}")
        return v
    
    def load_feature_flags(self) -> Dict[str, Any]:
        """Load feature flags from YAML file."""
        flags_path = Path(__file__).parent / self.FEATURE_FLAGS_FILE
        if not flags_path.exists():
            return {}
        
        with open(flags_path, 'r') as f:
            return yaml.safe_load(f)
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT == "development"
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT == "production"
    
    def get_api_url(self) -> str:
        """Get the full API URL."""
        return f"http://{self.API_HOST}:{self.API_PORT}{self.API_PREFIX}" 