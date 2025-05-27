"""
Conflict tracking service for detecting and managing data conflicts.
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from ..config.feature_flags import feature_flags

logger = logging.getLogger(__name__)

class ConflictTracker:
    """Conflict tracking service."""
    
    def __init__(self):
        """Initialize the conflict tracker."""
        self.config = feature_flags.MONITORING_CONFIG
        self._conflicts: List[Dict[str, Any]] = []
        self._max_conflicts = 1000  # Maximum number of conflicts to keep in memory
    
    def track_conflict(
        self,
        conflict_type: str,
        entity_id: str,
        details: Dict[str, Any],
        resolution: Optional[str] = None
    ) -> None:
        """
        Track a data conflict.
        
        Args:
            conflict_type: Type of conflict (e.g., 'schedule_overlap', 'data_mismatch')
            entity_id: ID of the entity involved in the conflict
            details: Additional details about the conflict
            resolution: How the conflict was resolved (if applicable)
        """
        if not self.config['conflict_tracking']:
            return
            
        conflict_info = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': conflict_type,
            'entity_id': entity_id,
            'details': details,
            'resolution': resolution
        }
        
        self._conflicts.append(conflict_info)
        
        # Trim old conflicts if we exceed the maximum
        if len(self._conflicts) > self._max_conflicts:
            self._conflicts = self._conflicts[-self._max_conflicts:]
        
        # Log the conflict
        logger.warning(
            f"Conflict detected: {conflict_type} for entity {entity_id}",
            extra={'conflict_info': conflict_info}
        )
    
    def get_conflicts(
        self,
        conflict_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get tracked conflicts with optional filtering.
        
        Args:
            conflict_type: Filter by conflict type
            entity_id: Filter by entity ID
            limit: Maximum number of conflicts to return
            
        Returns:
            List of conflict information dictionaries
        """
        filtered_conflicts = self._conflicts
        
        if conflict_type:
            filtered_conflicts = [
                c for c in filtered_conflicts
                if c['type'] == conflict_type
            ]
            
        if entity_id:
            filtered_conflicts = [
                c for c in filtered_conflicts
                if c['entity_id'] == entity_id
            ]
            
        if limit is not None:
            filtered_conflicts = filtered_conflicts[-limit:]
            
        return filtered_conflicts
    
    def resolve_conflict(self, conflict_index: int, resolution: str) -> None:
        """
        Mark a conflict as resolved.
        
        Args:
            conflict_index: Index of the conflict in the list
            resolution: How the conflict was resolved
        """
        if 0 <= conflict_index < len(self._conflicts):
            self._conflicts[conflict_index]['resolution'] = resolution
            logger.info(
                f"Conflict resolved: {self._conflicts[conflict_index]['type']}",
                extra={'resolution': resolution}
            )
    
    def clear_conflicts(self) -> None:
        """Clear all tracked conflicts."""
        self._conflicts.clear()
        logger.info("Conflict history cleared") 