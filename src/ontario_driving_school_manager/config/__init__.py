"""
Configuration package for Ontario Driving School Manager.
Provides centralized configuration management and feature flags.
"""

from pathlib import Path
from typing import Dict, Any
import yaml
import logging
import logging.config
from .settings import Settings
from .feature_flags import FeatureFlags
from .telemetry import TelemetryConfig
from .cache import CacheConfig
from .circuit_breaker import CircuitBreakerConfig

# Base paths
CONFIG_DIR = Path(__file__).parent
ROOT_DIR = CONFIG_DIR.parent.parent.parent

def load_yaml_config(config_file: str) -> Dict[str, Any]:
    """Load a YAML configuration file."""
    config_path = CONFIG_DIR / config_file
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def setup_logging():
    """Set up logging configuration."""
    logging_config = load_yaml_config('logging.yaml')
    logging.config.dictConfig(logging_config)

# Initialize configurations
settings = Settings()
feature_flags = FeatureFlags()
telemetry = TelemetryConfig()
cache = CacheConfig()
circuit_breaker = CircuitBreakerConfig()

# Set up logging
setup_logging()

__all__ = [
    'settings',
    'feature_flags',
    'telemetry',
    'cache',
    'circuit_breaker',
    'load_yaml_config',
    'setup_logging'
] 