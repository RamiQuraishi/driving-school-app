"""
Feature flags configuration for Ontario Driving School Manager.
Manages feature toggles and experimental features.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import yaml
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class FeatureFlags:
    """Manages feature flags and experimental features."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize feature flags."""
        self.config_file = config_file or "feature_flags.yaml"
        self.flags: Dict[str, Any] = {}
        self.last_updated: Optional[datetime] = None
        self.load_flags()
    
    def load_flags(self) -> None:
        """Load feature flags from YAML file."""
        try:
            config_path = Path(__file__).parent / self.config_file
            if not config_path.exists():
                logger.warning(f"Feature flags file not found: {self.config_file}")
                return
            
            with open(config_path, 'r') as f:
                self.flags = yaml.safe_load(f)
            self.last_updated = datetime.utcnow()
            logger.info("Feature flags loaded successfully")
        
        except Exception as e:
            logger.error(f"Failed to load feature flags: {str(e)}")
            self.flags = {}
    
    def is_enabled(self, feature_name: str) -> bool:
        """Check if a feature is enabled."""
        try:
            feature = self.flags.get(feature_name, {})
            if not feature:
                return False
            
            # Check if feature is enabled
            if not feature.get('enabled', False):
                return False
            
            # Check environment restrictions
            environment = feature.get('environment', [])
            if environment and 'all' not in environment:
                current_env = os.getenv('ENVIRONMENT', 'development')
                if current_env not in environment:
                    return False
            
            # Check date restrictions
            start_date = feature.get('start_date')
            end_date = feature.get('end_date')
            now = datetime.utcnow()
            
            if start_date and datetime.fromisoformat(start_date) > now:
                return False
            
            if end_date and datetime.fromisoformat(end_date) < now:
                return False
            
            return True
        
        except Exception as e:
            logger.error(f"Error checking feature flag {feature_name}: {str(e)}")
            return False
    
    def get_feature_config(self, feature_name: str) -> Dict[str, Any]:
        """Get configuration for a specific feature."""
        return self.flags.get(feature_name, {})
    
    def get_all_features(self) -> Dict[str, Any]:
        """Get all feature flags and their configurations."""
        return self.flags
    
    def get_enabled_features(self) -> Dict[str, Any]:
        """Get all currently enabled features."""
        return {
            name: config
            for name, config in self.flags.items()
            if self.is_enabled(name)
        }
    
    def update_feature(self, feature_name: str, config: Dict[str, Any]) -> bool:
        """Update a feature flag configuration."""
        try:
            self.flags[feature_name] = config
            self._save_flags()
            return True
        
        except Exception as e:
            logger.error(f"Failed to update feature flag {feature_name}: {str(e)}")
            return False
    
    def _save_flags(self) -> None:
        """Save feature flags to YAML file."""
        try:
            config_path = Path(__file__).parent / self.config_file
            with open(config_path, 'w') as f:
                yaml.safe_dump(self.flags, f, default_flow_style=False)
            self.last_updated = datetime.utcnow()
            logger.info("Feature flags saved successfully")
        
        except Exception as e:
            logger.error(f"Failed to save feature flags: {str(e)}")
            raise 