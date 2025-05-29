"""
Error Tracker

This module implements error tracking for the Ontario Driving School Manager.
It tracks and analyzes application errors and exceptions.

Author: Rami Drive School
Date: 2024
"""

import json
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Type
from dataclasses import dataclass

@dataclass
class ErrorEvent:
    """Error event data."""
    error_type: str
    message: str
    timestamp: datetime
    stack_trace: str
    context: Dict[str, Any]
    severity: str

class ErrorTracker:
    """Error tracker implementation."""
    
    def __init__(
        self,
        storage_path: str,
        max_errors: int = 1000
    ):
        """Initialize error tracker.
        
        Args:
            storage_path: Path to store error data
            max_errors: Maximum number of errors to store
        """
        self.storage_path = storage_path
        self.max_errors = max_errors
        self.errors: List[ErrorEvent] = []
    
    def track_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        severity: str = 'error'
    ) -> None:
        """Track error.
        
        Args:
            error: Exception to track
            context: Additional context
            severity: Error severity
        """
        # Create error event
        error_event = ErrorEvent(
            error_type=error.__class__.__name__,
            message=str(error),
            timestamp=datetime.utcnow(),
            stack_trace=traceback.format_exc(),
            context=context or {},
            severity=severity
        )
        
        # Store error
        self.errors.append(error_event)
        self._save_error(error_event)
        
        # Trim errors if needed
        if len(self.errors) > self.max_errors:
            self.errors = self.errors[-self.max_errors:]
    
    def _save_error(self, error: ErrorEvent) -> None:
        """Save error event.
        
        Args:
            error: Error event
        """
        # Convert error to dict
        error_dict = {
            'error_type': error.error_type,
            'message': error.message,
            'timestamp': error.timestamp.isoformat(),
            'stack_trace': error.stack_trace,
            'context': error.context,
            'severity': error.severity
        }
        
        # Save to file
        with open(self.storage_path, 'a') as f:
            f.write(json.dumps(error_dict) + '\n')
    
    def get_errors(
        self,
        error_type: Optional[str] = None,
        severity: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[ErrorEvent]:
        """Get error events.
        
        Args:
            error_type: Filter by error type
            severity: Filter by severity
            start_time: Filter by start time
            end_time: Filter by end time
            
        Returns:
            List[ErrorEvent]: Filtered errors
        """
        errors = self.errors
        
        if error_type:
            errors = [e for e in errors if e.error_type == error_type]
            
        if severity:
            errors = [e for e in errors if e.severity == severity]
            
        if start_time:
            errors = [e for e in errors if e.timestamp >= start_time]
            
        if end_time:
            errors = [e for e in errors if e.timestamp <= end_time]
            
        return errors
    
    def get_error_summary(self) -> Dict[str, int]:
        """Get error summary.
        
        Returns:
            Dict[str, int]: Error counts by type
        """
        summary = {}
        
        for error in self.errors:
            summary[error.error_type] = summary.get(error.error_type, 0) + 1
            
        return summary
    
    def clear_errors(self) -> None:
        """Clear all errors."""
        self.errors.clear() 