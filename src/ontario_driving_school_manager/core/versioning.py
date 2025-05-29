"""Version control and conflict management for the Ontario Driving School Manager."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declared_attr

from ..core.exceptions import VersionConflictError
from ..core.events import Event, EventBus, EventType

@dataclass
class VersionInfo:
    """Information about a version of an entity."""
    
    version: int
    created_at: datetime
    created_by: UUID
    changes: Dict[str, Any]
    comment: Optional[str] = None

class VersionedMixin:
    """Mixin for adding version control to models."""
    
    @declared_attr
    def version(cls) -> Column:
        """Version number column."""
        return Column(Integer, nullable=False, default=1)
    
    @declared_attr
    def version_created_at(cls) -> Column:
        """Version creation timestamp."""
        return Column(DateTime, nullable=False, default=datetime.utcnow)
    
    @declared_attr
    def version_created_by(cls) -> Column:
        """User who created this version."""
        return Column(String(36), nullable=False)
    
    @declared_attr
    def version_comment(cls) -> Column:
        """Comment for this version."""
        return Column(String(500), nullable=True)

class VersionManager:
    """Manages versioning and conflict resolution for entities."""
    
    def __init__(self, event_bus: EventBus):
        """Initialize the version manager.
        
        Args:
            event_bus: Event bus for publishing version events
        """
        self.event_bus = event_bus
    
    def create_version(
        self,
        entity: Any,
        user_id: UUID,
        changes: Dict[str, Any],
        comment: Optional[str] = None
    ) -> VersionInfo:
        """Create a new version of an entity.
        
        Args:
            entity: The entity to version
            user_id: ID of the user creating the version
            changes: Dictionary of changes made
            comment: Optional comment about the changes
            
        Returns:
            VersionInfo object with version details
        """
        # Increment version number
        entity.version += 1
        entity.version_created_at = datetime.utcnow()
        entity.version_created_by = str(user_id)
        entity.version_comment = comment
        
        # Create version info
        version_info = VersionInfo(
            version=entity.version,
            created_at=entity.version_created_at,
            created_by=user_id,
            changes=changes,
            comment=comment
        )
        
        # Publish version event
        self.event_bus.publish(Event(
            type=EventType.ENTITY_VERSIONED,
            data={
                "entity_id": str(getattr(entity, "id")),
                "entity_type": entity.__class__.__name__,
                "version": version_info
            }
        ))
        
        return version_info
    
    def check_version_conflict(
        self,
        entity: Any,
        expected_version: int
    ) -> None:
        """Check for version conflicts.
        
        Args:
            entity: The entity to check
            expected_version: The version number expected
            
        Raises:
            VersionConflictError: If there is a version conflict
        """
        if entity.version != expected_version:
            raise VersionConflictError(
                f"Version conflict: expected {expected_version}, got {entity.version}",
                current_version=entity.version,
                new_version=expected_version
            )
    
    def get_version_history(
        self,
        entity: Any,
        limit: Optional[int] = None
    ) -> List[VersionInfo]:
        """Get version history for an entity.
        
        Args:
            entity: The entity to get history for
            limit: Optional limit on number of versions to return
            
        Returns:
            List of VersionInfo objects
        """
        # This would typically query a version history table
        # For now, return current version info
        return [VersionInfo(
            version=entity.version,
            created_at=entity.version_created_at,
            created_by=UUID(entity.version_created_by),
            changes={},  # Would need to be populated from history
            comment=entity.version_comment
        )]
    
    def revert_to_version(
        self,
        entity: Any,
        version: int,
        user_id: UUID
    ) -> VersionInfo:
        """Revert an entity to a previous version.
        
        Args:
            entity: The entity to revert
            version: The version to revert to
            user_id: ID of the user performing the revert
            
        Returns:
            VersionInfo for the new version
            
        Raises:
            ValueError: If the version doesn't exist
        """
        # This would typically restore from version history
        # For now, just create a new version
        return self.create_version(
            entity=entity,
            user_id=user_id,
            changes={"reverted_to_version": version},
            comment=f"Reverted to version {version}"
        )
    
    def merge_versions(
        self,
        entity: Any,
        other_version: Any,
        user_id: UUID,
        strategy: str = "manual"
    ) -> VersionInfo:
        """Merge changes from another version.
        
        Args:
            entity: The entity to merge into
            other_version: The version to merge from
            user_id: ID of the user performing the merge
            strategy: Merge strategy to use ("manual", "auto", "theirs", "ours")
            
        Returns:
            VersionInfo for the merged version
            
        Raises:
            ValueError: If the merge strategy is invalid
        """
        if strategy not in ["manual", "auto", "theirs", "ours"]:
            raise ValueError(f"Invalid merge strategy: {strategy}")
        
        # This would typically perform the merge based on strategy
        # For now, just create a new version
        return self.create_version(
            entity=entity,
            user_id=user_id,
            changes={"merged_from_version": other_version.version},
            comment=f"Merged from version {other_version.version} using {strategy} strategy"
        ) 