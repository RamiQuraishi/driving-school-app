"""
Offline Sync Service

This module provides the offline sync service for the Ontario Driving School Manager.
It handles data synchronization between offline and online states.

Author: Rami Drive School
Date: 2024
"""

import logging
import json
from typing import Dict, Any, Optional, List, Set
from datetime import datetime
from pathlib import Path

from .base import BaseService
from ..core.metrics import DistributedTracing
from ..core.cache import Cache

logger = logging.getLogger(__name__)

class OfflineSyncService(BaseService[Dict[str, Any]]):
    """Offline sync service."""
    
    def __init__(
        self,
        cache: Optional[Cache] = None,
        tracing: Optional[DistributedTracing] = None,
        sync_dir: Optional[str] = None
    ):
        """Initialize offline sync service.
        
        Args:
            cache: Optional cache instance
            tracing: Optional tracing instance
            sync_dir: Sync directory path
        """
        super().__init__(cache, tracing)
        self.sync_dir = Path(sync_dir) if sync_dir else Path("sync")
        
        # Version tracking
        self.version_file = self.sync_dir / "version.json"
        self.current_version = "1.0.0"
        self.min_version = "1.0.0"
    
    async def initialize(self) -> None:
        """Initialize service."""
        self.log_info("Initializing offline sync service")
        
        # Create sync directory
        try:
            self.sync_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize version file
            if not self.version_file.exists():
                await self._save_version()
        except Exception as e:
            self.log_error("Failed to initialize sync directory", e)
            raise
    
    async def shutdown(self) -> None:
        """Shutdown service."""
        self.log_info("Shutting down offline sync service")
    
    async def _save_version(self) -> None:
        """Save version information."""
        version_data = {
            "version": self.current_version,
            "min_version": self.min_version,
            "last_updated": datetime.now().isoformat()
        }
        
        try:
            with open(self.version_file, "w") as f:
                json.dump(version_data, f, indent=2)
        except Exception as e:
            self.log_error("Failed to save version file", e)
            raise
    
    async def _load_version(self) -> Dict[str, Any]:
        """Load version information.
        
        Returns:
            Version data
        """
        try:
            with open(self.version_file, "r") as f:
                return json.load(f)
        except Exception as e:
            self.log_error("Failed to load version file", e)
            raise
    
    async def check_version_compatibility(self) -> bool:
        """Check version compatibility.
        
        Returns:
            True if compatible, False otherwise
        """
        with self.trace("check_version_compatibility") as span_id:
            try:
                version_data = await self._load_version()
                return version_data["version"] >= self.min_version
            except Exception as e:
                self.log_error("Failed to check version compatibility", e)
                return False
    
    async def sync_data(
        self,
        entity_type: str,
        entity_id: str,
        data: Dict[str, Any]
    ) -> None:
        """Sync entity data.
        
        Args:
            entity_type: Entity type (student, instructor, lesson)
            entity_id: Entity ID
            data: Entity data
        """
        with self.trace("sync_data") as span_id:
            # Validate data
            if not self._validate_sync_data(data):
                raise ValueError("Invalid sync data")
            
            # Generate sync file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{entity_type}_{entity_id}_{timestamp}.json"
            filepath = self.sync_dir / filename
            
            # Write data to file
            try:
                with open(filepath, "w") as f:
                    json.dump(data, f, indent=2)
            except Exception as e:
                self.log_error("Failed to write sync file", e)
                raise
            
            # Cache sync metadata
            metadata = {
                "entity_type": entity_type,
                "entity_id": entity_id,
                "filename": filename,
                "timestamp": timestamp,
                "status": "pending"
            }
            await self.set_cached(f"sync_{entity_id}", metadata)
    
    async def get_pending_syncs(
        self,
        entity_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get pending syncs.
        
        Args:
            entity_type: Optional entity type filter
            
        Returns:
            List of pending sync metadata
        """
        with self.trace("get_pending_syncs") as span_id:
            pending_syncs = []
            
            # Get all sync files
            for filepath in self.sync_dir.glob("*.json"):
                if filepath == self.version_file:
                    continue
                
                # Parse filename
                parts = filepath.stem.split("_")
                if len(parts) < 3:
                    continue
                
                sync_type = parts[0]
                if entity_type and sync_type != entity_type:
                    continue
                
                # Get sync metadata
                entity_id = parts[1]
                metadata = await self.get_cached(f"sync_{entity_id}")
                
                if metadata and metadata["status"] == "pending":
                    pending_syncs.append(metadata)
            
            return pending_syncs
    
    async def mark_sync_complete(
        self,
        entity_id: str,
        success: bool = True
    ) -> None:
        """Mark sync as complete.
        
        Args:
            entity_id: Entity ID
            success: Whether sync was successful
        """
        with self.trace("mark_sync_complete") as span_id:
            # Get sync metadata
            metadata = await self.get_cached(f"sync_{entity_id}")
            
            if metadata:
                # Update status
                metadata["status"] = "completed" if success else "failed"
                metadata["completed_at"] = datetime.now().isoformat()
                
                # Cache updated metadata
                await self.set_cached(f"sync_{entity_id}", metadata)
    
    def _validate_sync_data(self, data: Dict[str, Any]) -> bool:
        """Validate sync data.
        
        Args:
            data: Sync data to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = [
            "id",
            "type",
            "data",
            "version",
            "timestamp"
        ]
        
        return all(field in data for field in required_fields)
    
    async def cleanup_syncs(self, days: int = 7) -> None:
        """Clean up old sync files.
        
        Args:
            days: Number of days to keep syncs
        """
        with self.trace("cleanup_syncs") as span_id:
            try:
                # Get all sync files
                for filepath in self.sync_dir.glob("*.json"):
                    if filepath == self.version_file:
                        continue
                    
                    # Check file age
                    if (datetime.now() - datetime.fromtimestamp(filepath.stat().st_mtime)).days > days:
                        # Delete old file
                        filepath.unlink()
                        
                        # Clear cache
                        entity_id = filepath.stem.split("_")[1]
                        await self.invalidate_cache(f"sync_{entity_id}")
            except Exception as e:
                self.log_error("Failed to cleanup syncs", e)
                raise
    
    async def get_sync_status(
        self,
        entity_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get sync status.
        
        Args:
            entity_id: Entity ID
            
        Returns:
            Sync status or None
        """
        with self.trace("get_sync_status") as span_id:
            # Get from cache
            metadata = await self.get_cached(f"sync_{entity_id}")
            
            if not metadata:
                return None
            
            return {
                "entity_id": entity_id,
                "status": metadata["status"],
                "timestamp": metadata["timestamp"],
                "completed_at": metadata.get("completed_at")
            }