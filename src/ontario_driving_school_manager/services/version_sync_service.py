"""
Version Sync Service

This module provides the version sync service for the Ontario Driving School Manager.
It handles optimistic concurrency control and version synchronization.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Dict, Any, Optional, List, Set, TypeVar, Generic
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from .base import BaseService
from ..core.metrics import DistributedTracing
from ..core.cache import Cache

logger = logging.getLogger(__name__)

T = TypeVar('T')

class VersionStatus(Enum):
    """Version status."""
    ACTIVE = "active"
    STAGED = "staged"
    CONFLICT = "conflict"
    MERGED = "merged"

@dataclass
class Version(Generic[T]):
    """Version record."""
    id: str
    entity_id: str
    entity_type: str
    data: T
    version: int
    status: VersionStatus
    parent_version: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class VersionSyncService(BaseService[Dict[str, Any]]):
    """Version sync service."""
    
    def __init__(
        self,
        cache: Optional[Cache] = None,
        tracing: Optional[DistributedTracing] = None
    ):
        """Initialize version sync service.
        
        Args:
            cache: Optional cache instance
            tracing: Optional tracing instance
        """
        super().__init__(cache, tracing)
        
        # Version conflict resolution strategies
        self.conflict_strategies = {
            "last_write_wins": self._resolve_last_write_wins,
            "manual_resolution": self._resolve_manual,
            "merge": self._resolve_merge
        }
    
    async def initialize(self) -> None:
        """Initialize service."""
        self.log_info("Initializing version sync service")
    
    async def shutdown(self) -> None:
        """Shutdown service."""
        self.log_info("Shutting down version sync service")
    
    def _version_to_dict(self, version: Version) -> Dict[str, Any]:
        """Convert version to dictionary.
        
        Args:
            version: Version instance
            
        Returns:
            Version dictionary
        """
        return {
            "id": version.id,
            "entity_id": version.entity_id,
            "entity_type": version.entity_type,
            "data": version.data,
            "version": version.version,
            "status": version.status.value,
            "parent_version": version.parent_version,
            "created_at": version.created_at.isoformat(),
            "updated_at": version.updated_at.isoformat()
        }
    
    def _dict_to_version(self, data: Dict[str, Any]) -> Version:
        """Convert dictionary to version.
        
        Args:
            data: Version dictionary
            
        Returns:
            Version instance
        """
        return Version(
            id=data["id"],
            entity_id=data["entity_id"],
            entity_type=data["entity_type"],
            data=data["data"],
            version=data["version"],
            status=VersionStatus(data["status"]),
            parent_version=data.get("parent_version"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
        )
    
    async def create_version(
        self,
        entity_id: str,
        entity_type: str,
        data: Any,
        parent_version: Optional[str] = None
    ) -> Version:
        """Create a new version.
        
        Args:
            entity_id: Entity ID
            entity_type: Entity type
            data: Entity data
            parent_version: Optional parent version ID
            
        Returns:
            Created version
        """
        with self.trace("create_version") as span_id:
            # Get current version
            current_version = await self.get_latest_version(entity_id)
            version_number = (current_version.version + 1) if current_version else 1
            
            # Create version
            version = Version(
                id=f"ver_{entity_id}_{version_number}",
                entity_id=entity_id,
                entity_type=entity_type,
                data=data,
                version=version_number,
                status=VersionStatus.STAGED,
                parent_version=parent_version
            )
            
            # Cache version
            await self.set_cached(
                f"version_{version.id}",
                self._version_to_dict(version)
            )
            
            return version
    
    async def get_version(self, version_id: str) -> Optional[Version]:
        """Get version by ID.
        
        Args:
            version_id: Version ID
            
        Returns:
            Version instance or None
        """
        with self.trace("get_version") as span_id:
            # Get from cache
            data = await self.get_cached(f"version_{version_id}")
            
            if not data:
                return None
            
            return self._dict_to_version(data)
    
    async def get_latest_version(
        self,
        entity_id: str,
        status: Optional[VersionStatus] = None
    ) -> Optional[Version]:
        """Get latest version for entity.
        
        Args:
            entity_id: Entity ID
            status: Optional status filter
            
        Returns:
            Latest version or None
        """
        with self.trace("get_latest_version") as span_id:
            # Get from cache
            versions = []
            cache_keys = await self.cache.keys(f"version_*")
            
            for key in cache_keys:
                data = await self.get_cached(key)
                if not data:
                    continue
                
                version = self._dict_to_version(data)
                
                if version.entity_id != entity_id:
                    continue
                
                if status and version.status != status:
                    continue
                
                versions.append(version)
            
            if not versions:
                return None
            
            # Sort by version number
            versions.sort(key=lambda v: v.version, reverse=True)
            return versions[0]
    
    async def update_version(
        self,
        version_id: str,
        data: Any,
        strategy: str = "last_write_wins"
    ) -> Version:
        """Update version.
        
        Args:
            version_id: Version ID
            data: New data
            strategy: Conflict resolution strategy
            
        Returns:
            Updated version
        """
        with self.trace("update_version") as span_id:
            # Get version
            version = await self.get_version(version_id)
            if not version:
                raise ValueError(f"Version {version_id} not found")
            
            # Get latest version
            latest = await self.get_latest_version(version.entity_id)
            
            if latest and latest.version > version.version:
                # Handle conflict
                if strategy not in self.conflict_strategies:
                    raise ValueError(f"Unknown conflict strategy: {strategy}")
                
                resolved_data = await self.conflict_strategies[strategy](
                    version,
                    latest,
                    data
                )
                
                version.data = resolved_data
                version.status = VersionStatus.MERGED
            else:
                version.data = data
            
            version.updated_at = datetime.now()
            
            # Update cache
            await self.set_cached(
                f"version_{version_id}",
                self._version_to_dict(version)
            )
            
            return version
    
    async def _resolve_last_write_wins(
        self,
        current: Version,
        latest: Version,
        new_data: Any
    ) -> Any:
        """Resolve conflict using last-write-wins strategy.
        
        Args:
            current: Current version
            latest: Latest version
            new_data: New data
            
        Returns:
            Resolved data
        """
        return new_data
    
    async def _resolve_manual(
        self,
        current: Version,
        latest: Version,
        new_data: Any
    ) -> Any:
        """Resolve conflict using manual resolution strategy.
        
        Args:
            current: Current version
            latest: Latest version
            new_data: New data
            
        Returns:
            Resolved data
        """
        # Mark as conflict for manual resolution
        current.status = VersionStatus.CONFLICT
        return current.data
    
    async def _resolve_merge(
        self,
        current: Version,
        latest: Version,
        new_data: Any
    ) -> Any:
        """Resolve conflict using merge strategy.
        
        Args:
            current: Current version
            latest: Latest version
            new_data: New data
            
        Returns:
            Resolved data
        """
        # Simple merge strategy - combine unique keys
        if isinstance(new_data, dict) and isinstance(latest.data, dict):
            merged = latest.data.copy()
            merged.update(new_data)
            return merged
        
        # Default to new data if not dictionaries
        return new_data
    
    async def activate_version(self, version_id: str) -> Version:
        """Activate version.
        
        Args:
            version_id: Version ID
            
        Returns:
            Activated version
        """
        with self.trace("activate_version") as span_id:
            # Get version
            version = await self.get_version(version_id)
            if not version:
                raise ValueError(f"Version {version_id} not found")
            
            # Update status
            version.status = VersionStatus.ACTIVE
            version.updated_at = datetime.now()
            
            # Update cache
            await self.set_cached(
                f"version_{version_id}",
                self._version_to_dict(version)
            )
            
            return version
    
    async def get_version_history(
        self,
        entity_id: str,
        include_inactive: bool = False
    ) -> List[Version]:
        """Get version history.
        
        Args:
            entity_id: Entity ID
            include_inactive: Whether to include inactive versions
            
        Returns:
            List of versions
        """
        with self.trace("get_version_history") as span_id:
            # Get from cache
            versions = []
            cache_keys = await self.cache.keys(f"version_*")
            
            for key in cache_keys:
                data = await self.get_cached(key)
                if not data:
                    continue
                
                version = self._dict_to_version(data)
                
                if version.entity_id != entity_id:
                    continue
                
                if not include_inactive and version.status == VersionStatus.STAGED:
                    continue
                
                versions.append(version)
            
            # Sort by version number
            versions.sort(key=lambda v: v.version)
            return versions