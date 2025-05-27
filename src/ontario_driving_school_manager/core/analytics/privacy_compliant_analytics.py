"""
Privacy-compliant analytics service.
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from ..config.feature_flags import feature_flags

logger = logging.getLogger(__name__)

class PrivacyCompliantAnalytics:
    """Privacy-compliant analytics service."""
    
    def __init__(self):
        """Initialize the analytics service."""
        self.config = feature_flags.ANALYTICS_CONFIG
        self._data_retention = timedelta(days=self.config['data_retention_days'])
        self._events: Dict[str, Any] = {}
    
    async def track_event(self, event_name: str, properties: Optional[Dict[str, Any]] = None) -> None:
        """
        Track an analytics event.
        
        Args:
            event_name: Name of the event
            properties: Optional event properties
        """
        if not self.config['enabled']:
            return
            
        try:
            # Anonymize data if needed
            if self.config['privacy_compliant']:
                properties = self._anonymize_data(properties)
            
            # Store event
            self._events[event_name] = {
                'timestamp': datetime.utcnow(),
                'properties': properties or {}
            }
            
            # Clean up old data
            self._cleanup_old_data()
            
        except Exception as e:
            logger.error(f"Error tracking event {event_name}: {str(e)}")
    
    def _anonymize_data(self, data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Anonymize sensitive data.
        
        Args:
            data: Data to anonymize
            
        Returns:
            Anonymized data
        """
        if not data:
            return {}
            
        # Remove or hash sensitive fields
        sensitive_fields = {'email', 'phone', 'address', 'name'}
        return {
            k: '***' if k in sensitive_fields else v
            for k, v in data.items()
        }
    
    def _cleanup_old_data(self) -> None:
        """Clean up data older than retention period."""
        cutoff = datetime.utcnow() - self._data_retention
        self._events = {
            k: v for k, v in self._events.items()
            if v['timestamp'] > cutoff
        } 