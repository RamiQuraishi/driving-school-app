"""
Configuration Utilities Module

This module provides configuration management functionality.
It includes loading, saving, and validating configuration.

Author: Rami Drive School
Date: 2024
"""

import json
import os
from typing import Dict, Any, Optional, Union
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ConfigError(Exception):
    """Configuration error."""
    pass

def load_config(
    config_path: str = "config.json",
    default_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Load configuration.
    
    Args:
        config_path: Path to config file
        default_config: Default configuration
        
    Returns:
        Configuration dictionary
        
    Raises:
        ConfigError: If config file is invalid
    """
    default_config = default_config or {
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "driving_school",
            "user": "postgres",
            "password": ""
        },
        "mto": {
            "api_key": "",
            "api_url": "https://api.mto.gov.on.ca",
            "timeout": 30
        },
        "logging": {
            "level": "INFO",
            "dir": "logs",
            "max_size": 10485760,  # 10MB
            "backup_count": 5
        },
        "export": {
            "dir": "exports",
            "formats": ["json", "csv", "excel"],
            "max_size": 104857600  # 100MB
        }
    }
    
    try:
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
            
            # Merge with default config
            merged_config = default_config.copy()
            merged_config.update(config)
            return merged_config
        else:
            # Create default config file
            save_config(default_config, config_path)
            return default_config
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid config file: {str(e)}")
    except Exception as e:
        raise ConfigError(f"Error loading config: {str(e)}")

def save_config(
    config: Dict[str, Any],
    config_path: str = "config.json"
) -> None:
    """Save configuration.
    
    Args:
        config: Configuration dictionary
        config_path: Path to config file
        
    Raises:
        ConfigError: If config cannot be saved
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        raise ConfigError(f"Error saving config: {str(e)}")

def validate_config(
    config: Dict[str, Any],
    required_fields: Optional[Dict[str, Any]] = None
) -> bool:
    """Validate configuration.
    
    Args:
        config: Configuration dictionary
        required_fields: Required fields and their types
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = required_fields or {
        "database": dict,
        "mto": dict,
        "logging": dict,
        "export": dict
    }
    
    try:
        for field, field_type in required_fields.items():
            if field not in config:
                logger.error(f"Missing required field: {field}")
                return False
            
            if not isinstance(config[field], field_type):
                logger.error(
                    f"Invalid type for {field}: "
                    f"expected {field_type.__name__}, "
                    f"got {type(config[field]).__name__}"
                )
                return False
        
        return True
    except Exception as e:
        logger.error(f"Error validating config: {str(e)}")
        return False

def get_config_value(
    config: Dict[str, Any],
    key: str,
    default: Any = None
) -> Any:
    """Get configuration value.
    
    Args:
        config: Configuration dictionary
        key: Key path (dot-separated)
        default: Default value
        
    Returns:
        Configuration value
    """
    try:
        value = config
        for k in key.split("."):
            value = value[k]
        return value
    except (KeyError, TypeError):
        return default

def set_config_value(
    config: Dict[str, Any],
    key: str,
    value: Any
) -> None:
    """Set configuration value.
    
    Args:
        config: Configuration dictionary
        key: Key path (dot-separated)
        value: Value to set
    """
    keys = key.split(".")
    current = config
    
    for k in keys[:-1]:
        if k not in current:
            current[k] = {}
        current = current[k]
    
    current[keys[-1]] = value

def merge_configs(
    base_config: Dict[str, Any],
    override_config: Dict[str, Any]
) -> Dict[str, Any]:
    """Merge configurations.
    
    Args:
        base_config: Base configuration
        override_config: Override configuration
        
    Returns:
        Merged configuration
    """
    merged = base_config.copy()
    
    for key, value in override_config.items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            merged[key] = merge_configs(merged[key], value)
        else:
            merged[key] = value
    
    return merged

def get_env_config() -> Dict[str, Any]:
    """Get configuration from environment variables.
    
    Returns:
        Configuration dictionary
    """
    config = {}
    
    # Database configuration
    if "DB_HOST" in os.environ:
        config["database"] = {
            "host": os.environ["DB_HOST"],
            "port": int(os.environ.get("DB_PORT", "5432")),
            "name": os.environ.get("DB_NAME", "driving_school"),
            "user": os.environ.get("DB_USER", "postgres"),
            "password": os.environ.get("DB_PASSWORD", "")
        }
    
    # MTO configuration
    if "MTO_API_KEY" in os.environ:
        config["mto"] = {
            "api_key": os.environ["MTO_API_KEY"],
            "api_url": os.environ.get(
                "MTO_API_URL",
                "https://api.mto.gov.on.ca"
            ),
            "timeout": int(os.environ.get("MTO_TIMEOUT", "30"))
        }
    
    # Logging configuration
    if "LOG_LEVEL" in os.environ:
        config["logging"] = {
            "level": os.environ["LOG_LEVEL"],
            "dir": os.environ.get("LOG_DIR", "logs"),
            "max_size": int(os.environ.get("LOG_MAX_SIZE", "10485760")),
            "backup_count": int(os.environ.get("LOG_BACKUP_COUNT", "5"))
        }
    
    # Export configuration
    if "EXPORT_DIR" in os.environ:
        config["export"] = {
            "dir": os.environ["EXPORT_DIR"],
            "formats": os.environ.get(
                "EXPORT_FORMATS",
                "json,csv,excel"
            ).split(","),
            "max_size": int(os.environ.get("EXPORT_MAX_SIZE", "104857600"))
        }
    
    return config 