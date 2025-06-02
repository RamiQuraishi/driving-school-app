"""
Feature Flag Service

This module provides the feature flag service for the Ontario Driving School Manager.
It handles feature toggles and A/B testing.

Author: Rami Drive School
Date: 2024
"""

import logging
import json
from typing import Dict, Any, Optional, List, Set
from datetime import datetime
from pathlib import Path

from .base import BaseService
from ..core.metrics import DistributedTracing
from ..core.cache import Cache

logger = logging.getLogger(__name__)

class FeatureFlagService(BaseService[Dict[str, Any]]):
    """Feature flag service."""
    
    def __init__(
        self,
        cache: Optional[Cache] = None,
        tracing: Optional[DistributedTracing] = None,
        config_dir: Optional[str] = None
    ):
        """Initialize feature flag service.
        
        Args:
            cache: Optional cache instance
            tracing: Optional tracing instance
            config_dir: Config directory path
        """
        super().__init__(cache, tracing)
        self.config_dir = Path(config_dir) if config_dir else Path("config")
        
        # Feature flag configuration
        self.config_file = self.config_dir / "features.json"
        self.default_flags = {
            "enable_offline_mode": True,
            "enable_sync": True,
            "enable_export": True,
            "enable_metrics": True,
            "enable_tracing": True
        }
    
    async def initialize(self) -> None:
        """Initialize service."""
        self.log_info("Initializing feature flag service")
        
        # Create config directory
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize config file
            if not self.config_file.exists():
                await self._save_config()
        except Exception as e:
            self.log_error("Failed to initialize config directory", e)
            raise
    
    async def shutdown(self) -> None:
        """Shutdown service."""
        self.log_info("Shutting down feature flag service")
    
    async def _save_config(self) -> None:
        """Save feature flag configuration."""
        config_data = {
            "flags": self.default_flags,
            "last_updated": datetime.now().isoformat()
        }
        
        try:
            with open(self.config_file, "w") as f:
                json.dump(config_data, f, indent=2)
        except Exception as e:
            self.log_error("Failed to save config file", e)
            raise
    
    async def _load_config(self) -> Dict[str, Any]:
        """Load feature flag configuration.
        
        Returns:
            Config data
        """
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except Exception as e:
            self.log_error("Failed to load config file", e)
            raise
    
    async def is_feature_enabled(
        self,
        feature: str,
        user_id: Optional[str] = None
    ) -> bool:
        """Check if feature is enabled.
        
        Args:
            feature: Feature name
            user_id: Optional user ID for user-specific flags
            
        Returns:
            True if enabled, False otherwise
        """
        with self.trace("check_feature_flag") as span_id:
            try:
                # Try to get from cache
                cache_key = f"feature_{feature}"
                if user_id:
                    cache_key = f"{cache_key}_{user_id}"
                
                flag_value = await self.get_cached(cache_key)
                
                if flag_value is not None:
                    return flag_value
                
                # Load from config
                config = await self._load_config()
                flag_value = config["flags"].get(feature, False)
                
                # Cache the value
                await self.set_cached(cache_key, flag_value)
                
                return flag_value
            except Exception as e:
                self.log_error("Failed to check feature flag", e)
                return False
    
    async def set_feature_flag(
        self,
        feature: str,
        enabled: bool,
        user_id: Optional[str] = None
    ) -> None:
        """Set feature flag.
        
        Args:
            feature: Feature name
            enabled: Whether feature is enabled
            user_id: Optional user ID for user-specific flags
        """
        with self.trace("set_feature_flag") as span_id:
            try:
                # Load current config
                config = await self._load_config()
                
                # Update flag
                if user_id:
                    if "user_flags" not in config:
                        config["user_flags"] = {}
                    if user_id not in config["user_flags"]:
                        config["user_flags"][user_id] = {}
                    config["user_flags"][user_id][feature] = enabled
                else:
                    config["flags"][feature] = enabled
                
                # Save config
                config["last_updated"] = datetime.now().isoformat()
                with open(self.config_file, "w") as f:
                    json.dump(config, f, indent=2)
                
                # Update cache
                cache_key = f"feature_{feature}"
                if user_id:
                    cache_key = f"{cache_key}_{user_id}"
                await self.set_cached(cache_key, enabled)
            except Exception as e:
                self.log_error("Failed to set feature flag", e)
                raise
    
    async def get_all_flags(
        self,
        user_id: Optional[str] = None
    ) -> Dict[str, bool]:
        """Get all feature flags.
        
        Args:
            user_id: Optional user ID for user-specific flags
            
        Returns:
            Dictionary of feature flags
        """
        with self.trace("get_all_flags") as span_id:
            try:
                # Load config
                config = await self._load_config()
                
                # Get global flags
                flags = config["flags"].copy()
                
                # Add user-specific flags
                if user_id and "user_flags" in config:
                    user_flags = config["user_flags"].get(user_id, {})
                    flags.update(user_flags)
                
                return flags
            except Exception as e:
                self.log_error("Failed to get feature flags", e)
                return {}
    
    async def reset_flags(self) -> None:
        """Reset all feature flags to defaults."""
        with self.trace("reset_flags") as span_id:
            try:
                # Save default config
                await self._save_config()
                
                # Clear cache
                if self.cache:
                    await self.cache.clear()
            except Exception as e:
                self.log_error("Failed to reset feature flags", e)
                raise
    
    async def get_flag_history(
        self,
        feature: str,
        user_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get feature flag history.
        
        Args:
            feature: Feature name
            user_id: Optional user ID for user-specific flags
            
        Returns:
            List of flag changes
        """
        with self.trace("get_flag_history") as span_id:
            try:
                # Load config
                config = await self._load_config()
                
                # Get history
                history = []
                if "history" in config:
                    for entry in config["history"]:
                        if entry["feature"] == feature:
                            if user_id and entry.get("user_id") != user_id:
                                continue
                            history.append(entry)
                
                return history
            except Exception as e:
                self.log_error("Failed to get flag history", e)
                return []