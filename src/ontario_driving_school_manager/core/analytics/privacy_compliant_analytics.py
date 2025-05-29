"""
Privacy-Compliant Analytics

This module implements privacy-compliant analytics for the Ontario Driving School Manager.
It ensures data collection follows privacy regulations and best practices.

Author: Rami Drive School
Date: 2024
"""

import json
import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

@dataclass
class AnalyticsEvent:
    """Analytics event data."""
    event_type: str
    timestamp: datetime
    data: Dict[str, Any]
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class PrivacyCompliantAnalytics:
    """Privacy-compliant analytics implementation."""
    
    def __init__(
        self,
        storage_path: str,
        anonymize_data: bool = True
    ):
        """Initialize analytics.
        
        Args:
            storage_path: Path to store analytics data
            anonymize_data: Whether to anonymize data
        """
        self.storage_path = storage_path
        self.anonymize_data = anonymize_data
        self.events: List[AnalyticsEvent] = []
    
    def track_event(
        self,
        event_type: str,
        data: Dict[str, Any],
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> None:
        """Track analytics event.
        
        Args:
            event_type: Event type
            data: Event data
            user_id: User ID
            session_id: Session ID
        """
        # Create event
        event = AnalyticsEvent(
            event_type=event_type,
            timestamp=datetime.utcnow(),
            data=self._sanitize_data(data),
            user_id=self._anonymize_id(user_id) if self.anonymize_data else user_id,
            session_id=session_id
        )
        
        # Store event
        self.events.append(event)
        self._save_event(event)
    
    def _sanitize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize event data.
        
        Args:
            data: Event data
            
        Returns:
            Dict[str, Any]: Sanitized data
        """
        sanitized = {}
        
        for key, value in data.items():
            # Skip sensitive fields
            if key.lower() in ['password', 'token', 'key', 'secret']:
                continue
                
            # Sanitize values
            if isinstance(value, str):
                # Remove PII
                if '@' in value:  # Email
                    sanitized[key] = '***@***'
                elif len(value) > 10:  # Long strings might be PII
                    sanitized[key] = '***'
                else:
                    sanitized[key] = value
            else:
                sanitized[key] = value
        
        return sanitized
    
    def _anonymize_id(self, id: Optional[str]) -> Optional[str]:
        """Anonymize ID.
        
        Args:
            id: ID to anonymize
            
        Returns:
            Optional[str]: Anonymized ID
        """
        if not id:
            return None
            
        return hashlib.sha256(id.encode()).hexdigest()[:16]
    
    def _save_event(self, event: AnalyticsEvent) -> None:
        """Save event to storage.
        
        Args:
            event: Event to save
        """
        # Convert event to dict
        event_dict = {
            'event_type': event.event_type,
            'timestamp': event.timestamp.isoformat(),
            'data': event.data,
            'user_id': event.user_id,
            'session_id': event.session_id
        }
        
        # Save to file
        with open(self.storage_path, 'a') as f:
            f.write(json.dumps(event_dict) + '\n')
    
    def get_events(
        self,
        event_type: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[AnalyticsEvent]:
        """Get analytics events.
        
        Args:
            event_type: Filter by event type
            start_time: Filter by start time
            end_time: Filter by end time
            
        Returns:
            List[AnalyticsEvent]: Filtered events
        """
        events = self.events
        
        if event_type:
            events = [e for e in events if e.event_type == event_type]
            
        if start_time:
            events = [e for e in events if e.timestamp >= start_time]
            
        if end_time:
            events = [e for e in events if e.timestamp <= end_time]
            
        return events
    
    def clear_events(self) -> None:
        """Clear all events."""
        self.events.clear() 