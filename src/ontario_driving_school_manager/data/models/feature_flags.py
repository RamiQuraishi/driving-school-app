"""Feature flags model for managing feature toggles."""

from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship

from .base import BaseModel

class FeatureFlag(BaseModel):
    """Feature flag model.
    
    This model manages feature toggles for:
    - A/B testing
    - Gradual rollouts
    - Feature deprecation
    - Environment-specific features
    """
    
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255))
    is_enabled = Column(Boolean, nullable=False, default=False)
    enabled_for = Column(JSON)  # List of user IDs or groups
    rollout_percentage = Column(Integer, default=100)  # 0-100
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    metadata = Column(JSON)  # Additional configuration
    
    def is_active(self) -> bool:
        """Check if feature flag is active.
        
        Returns:
            bool: True if active
        """
        if not self.is_enabled:
            return False
        
        now = datetime.utcnow()
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        
        return True
    
    def is_enabled_for_user(self, user_id: int) -> bool:
        """Check if feature is enabled for user.
        
        Args:
            user_id: User ID
            
        Returns:
            bool: True if enabled
        """
        if not self.is_active():
            return False
        
        if not self.enabled_for:
            return True
        
        return user_id in self.enabled_for
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get feature metadata.
        
        Returns:
            Dict[str, Any]: Feature metadata
        """
        return self.metadata or {}
    
    def update_metadata(self, metadata: Dict[str, Any]) -> None:
        """Update feature metadata.
        
        Args:
            metadata: New metadata
        """
        current = self.get_metadata()
        current.update(metadata)
        self.metadata = current 