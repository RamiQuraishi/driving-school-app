"""
Error tracking service.
"""
import logging
import traceback
from typing import Dict, Any, Optional, List
from datetime import datetime
from ..config.feature_flags import feature_flags

logger = logging.getLogger(__name__)

class ErrorTracker:
    """Error tracking service."""
    
    def __init__(self):
        """Initialize the error tracker."""
        self.config = feature_flags.MONITORING_CONFIG
        self._errors: List[Dict[str, Any]] = []
        self._max_errors = 1000  # Maximum number of errors to keep in memory
    
    def track_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> None:
        """
        Track an error occurrence.
        
        Args:
            error: The exception that occurred
            context: Additional context about the error
        """
        if not self.config['error_tracking']:
            return
            
        error_info = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': type(error).__name__,
            'message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {}
        }
        
        self._errors.append(error_info)
        
        # Trim old errors if we exceed the maximum
        if len(self._errors) > self._max_errors:
            self._errors = self._errors[-self._max_errors:]
        
        # Log the error
        logger.error(
            f"Error tracked: {error_info['type']} - {error_info['message']}",
            extra={'error_info': error_info}
        )
    
    def get_errors(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get tracked errors.
        
        Args:
            limit: Maximum number of errors to return
            
        Returns:
            List of error information dictionaries
        """
        if limit is None:
            return self._errors
        return self._errors[-limit:]
    
    def clear_errors(self) -> None:
        """Clear all tracked errors."""
        self._errors.clear()
        logger.info("Error history cleared") 