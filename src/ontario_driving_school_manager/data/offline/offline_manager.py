"""Offline data management coordinator."""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
import asyncio

from .sqlite_manager import SQLiteManager
from .version_manager import VersionManager
from .sync_service import SyncService
from .sync_queue import SyncQueue
from .conflict_resolver import ConflictResolver

logger = logging.getLogger(__name__)

class OfflineManager:
    """Coordinates offline data operations."""
    
    def __init__(
        self,
        db_path: str,
        sync_interval: int = 300,  # 5 minutes
        batch_size: int = 100,
        max_retries: int = 3
    ):
        """Initialize offline manager.
        
        Args:
            db_path: Path to SQLite database
            sync_interval: Sync interval in seconds
            batch_size: Batch size for sync operations
            max_retries: Maximum number of retry attempts
        """
        self.sqlite_manager = SQLiteManager(db_path)
        self.version_manager = VersionManager(self.sqlite_manager)
        self.sync_queue = SyncQueue(
            self.sqlite_manager,
            batch_size=batch_size,
            max_retries=max_retries
        )
        self.conflict_resolver = ConflictResolver(
            self.version_manager,
            self.sqlite_manager
        )
        self.sync_service = SyncService(
            self.sqlite_manager,
            self.version_manager,
            self.sync_queue,
            self.conflict_resolver
        )
        
        self.sync_interval = sync_interval
        self._sync_task: Optional[asyncio.Task] = None
        self._is_running = False
    
    async def start(self) -> None:
        """Start the offline manager."""
        if self._is_running:
            return
        
        self._is_running = True
        await self.sync_service.start()
        self.sync_queue.start_processing()
        
        # Start periodic sync
        self._sync_task = asyncio.create_task(self._periodic_sync())
        logger.info("Offline manager started")
    
    async def stop(self) -> None:
        """Stop the offline manager."""
        if not self._is_running:
            return
        
        self._is_running = False
        if self._sync_task:
            self._sync_task.cancel()
            try:
                await self._sync_task
            except asyncio.CancelledError:
                pass
        
        self.sync_queue.stop_processing()
        await self.sync_service.stop()
        logger.info("Offline manager stopped")
    
    async def _periodic_sync(self) -> None:
        """Run periodic sync."""
        while self._is_running:
            try:
                await self.sync_service.sync_all()
            except Exception as e:
                logger.error(f"Error in periodic sync: {e}")
            
            await asyncio.sleep(self.sync_interval)
    
    async def create_record(
        self,
        table_name: str,
        data: Dict[str, Any]
    ) -> int:
        """Create a new record.
        
        Args:
            table_name: Name of the table
            data: Record data
            
        Returns:
            int: Record ID
        """
        try:
            # Add metadata
            data["created_at"] = datetime.utcnow().isoformat()
            data["updated_at"] = data["created_at"]
            
            # Insert record
            record_id = self.sqlite_manager.insert(table_name, data)
            
            # Track version
            self.version_manager.update_local_version(
                table_name,
                record_id,
                data
            )
            
            # Queue for sync
            await self.sync_queue.enqueue(
                "create",
                table_name,
                record_id,
                data
            )
            
            return record_id
            
        except Exception as e:
            logger.error(f"Error creating record: {e}")
            raise
    
    async def update_record(
        self,
        table_name: str,
        record_id: int,
        data: Dict[str, Any]
    ) -> None:
        """Update an existing record.
        
        Args:
            table_name: Name of the table
            record_id: ID of the record
            data: Updated data
        """
        try:
            # Get current version
            current_version = self.version_manager.get_local_version(
                table_name,
                record_id
            )
            
            # Add metadata
            data["updated_at"] = datetime.utcnow().isoformat()
            
            # Update record
            self.sqlite_manager.update(
                table_name,
                record_id,
                data
            )
            
            # Track version
            self.version_manager.update_local_version(
                table_name,
                record_id,
                data
            )
            
            # Queue for sync
            await self.sync_queue.enqueue(
                "update",
                table_name,
                record_id,
                data,
                current_version
            )
            
        except Exception as e:
            logger.error(f"Error updating record: {e}")
            raise
    
    async def delete_record(
        self,
        table_name: str,
        record_id: int
    ) -> None:
        """Delete a record.
        
        Args:
            table_name: Name of the table
            record_id: ID of the record
        """
        try:
            # Get current version
            current_version = self.version_manager.get_local_version(
                table_name,
                record_id
            )
            
            # Delete record
            self.sqlite_manager.delete(table_name, record_id)
            
            # Queue for sync
            await self.sync_queue.enqueue(
                "delete",
                table_name,
                record_id,
                None,
                current_version
            )
            
        except Exception as e:
            logger.error(f"Error deleting record: {e}")
            raise
    
    def get_record(
        self,
        table_name: str,
        record_id: int
    ) -> Optional[Dict[str, Any]]:
        """Get a record.
        
        Args:
            table_name: Name of the table
            record_id: ID of the record
            
        Returns:
            Optional[Dict[str, Any]]: Record data if found
        """
        try:
            return self.sqlite_manager.get(table_name, record_id)
        except Exception as e:
            logger.error(f"Error getting record: {e}")
            return None
    
    def get_records(
        self,
        table_name: str,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get multiple records.
        
        Args:
            table_name: Name of the table
            filters: Filter conditions
            order_by: Order by clause
            limit: Maximum number of records
            offset: Offset for pagination
            
        Returns:
            List[Dict[str, Any]]: List of records
        """
        try:
            return self.sqlite_manager.get_many(
                table_name,
                filters,
                order_by,
                limit,
                offset
            )
        except Exception as e:
            logger.error(f"Error getting records: {e}")
            return []
    
    async def force_sync(self) -> None:
        """Force immediate synchronization."""
        try:
            await self.sync_service.sync_all()
        except Exception as e:
            logger.error(f"Error in force sync: {e}")
            raise 