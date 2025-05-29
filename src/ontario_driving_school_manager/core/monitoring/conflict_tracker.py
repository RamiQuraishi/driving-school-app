"""
Conflict Tracker

This module implements conflict tracking for the Ontario Driving School Manager.
It tracks and analyzes synchronization conflicts between local and remote data.

Author: Rami Drive School
Date: 2024
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ConflictEvent:
    """Conflict event data."""
    entity_type: str
    entity_id: str
    local_version: str
    remote_version: str
    timestamp: datetime
    resolution: Optional[str]
    metadata: Dict[str, Any]

class ConflictTracker:
    """Conflict tracker implementation."""
    
    def __init__(
        self,
        storage_path: str,
        max_conflicts: int = 1000
    ):
        """Initialize conflict tracker.
        
        Args:
            storage_path: Path to store conflict data
            max_conflicts: Maximum number of conflicts to store
        """
        self.storage_path = storage_path
        self.max_conflicts = max_conflicts
        self.conflicts: List[ConflictEvent] = []
    
    def track_conflict(
        self,
        entity_type: str,
        entity_id: str,
        local_version: str,
        remote_version: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Track conflict.
        
        Args:
            entity_type: Type of entity
            entity_id: Entity ID
            local_version: Local version
            remote_version: Remote version
            metadata: Additional metadata
        """
        # Create conflict event
        conflict = ConflictEvent(
            entity_type=entity_type,
            entity_id=entity_id,
            local_version=local_version,
            remote_version=remote_version,
            timestamp=datetime.utcnow(),
            resolution=None,
            metadata=metadata or {}
        )
        
        # Store conflict
        self.conflicts.append(conflict)
        self._save_conflict(conflict)
        
        # Trim conflicts if needed
        if len(self.conflicts) > self.max_conflicts:
            self.conflicts = self.conflicts[-self.max_conflicts:]
    
    def resolve_conflict(
        self,
        entity_type: str,
        entity_id: str,
        resolution: str
    ) -> None:
        """Resolve conflict.
        
        Args:
            entity_type: Type of entity
            entity_id: Entity ID
            resolution: Resolution type
        """
        # Find conflict
        for conflict in self.conflicts:
            if (conflict.entity_type == entity_type and
                conflict.entity_id == entity_id and
                conflict.resolution is None):
                
                # Update resolution
                conflict.resolution = resolution
                self._save_conflict(conflict)
                break
    
    def _save_conflict(self, conflict: ConflictEvent) -> None:
        """Save conflict event.
        
        Args:
            conflict: Conflict event
        """
        # Convert conflict to dict
        conflict_dict = {
            'entity_type': conflict.entity_type,
            'entity_id': conflict.entity_id,
            'local_version': conflict.local_version,
            'remote_version': conflict.remote_version,
            'timestamp': conflict.timestamp.isoformat(),
            'resolution': conflict.resolution,
            'metadata': conflict.metadata
        }
        
        # Save to file
        with open(self.storage_path, 'a') as f:
            f.write(json.dumps(conflict_dict) + '\n')
    
    def get_conflicts(
        self,
        entity_type: Optional[str] = None,
        resolved: Optional[bool] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[ConflictEvent]:
        """Get conflict events.
        
        Args:
            entity_type: Filter by entity type
            resolved: Filter by resolution status
            start_time: Filter by start time
            end_time: Filter by end time
            
        Returns:
            List[ConflictEvent]: Filtered conflicts
        """
        conflicts = self.conflicts
        
        if entity_type:
            conflicts = [c for c in conflicts if c.entity_type == entity_type]
            
        if resolved is not None:
            conflicts = [c for c in conflicts if (c.resolution is not None) == resolved]
            
        if start_time:
            conflicts = [c for c in conflicts if c.timestamp >= start_time]
            
        if end_time:
            conflicts = [c for c in conflicts if c.timestamp <= end_time]
            
        return conflicts
    
    def get_conflict_summary(self) -> Dict[str, Dict[str, int]]:
        """Get conflict summary.
        
        Returns:
            Dict[str, Dict[str, int]]: Conflict counts by type and resolution
        """
        summary = {}
        
        for conflict in self.conflicts:
            if conflict.entity_type not in summary:
                summary[conflict.entity_type] = {
                    'total': 0,
                    'resolved': 0,
                    'unresolved': 0
                }
            
            summary[conflict.entity_type]['total'] += 1
            
            if conflict.resolution:
                summary[conflict.entity_type]['resolved'] += 1
            else:
                summary[conflict.entity_type]['unresolved'] += 1
            
        return summary
    
    def clear_conflicts(self) -> None:
        """Clear all conflicts."""
        self.conflicts.clear() 