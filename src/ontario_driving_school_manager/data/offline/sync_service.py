"""Data synchronization service."""

import logging
import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import json

from .sqlite_manager import SQLiteManager
from .version_manager import VersionManager
from .conflict_resolver import ConflictResolver

logger = logging.getLogger(__name__)

class SyncService:
    """Handles data synchronization between offline and online databases."""
    
    def __init__(
        self,
        sqlite_manager: SQLiteManager,
        version_manager: VersionManager,
        conflict_resolver: ConflictResolver,
        sync_interval: int = 300,  # 5 minutes
        max_retries: int = 3
    ):
        """Initialize sync service.
        
        Args:
            sqlite_manager: SQLite manager instance
            version_manager: Version manager instance
            conflict_resolver: Conflict resolver instance
            sync_interval: Interval between sync attempts in seconds
            max_retries: Maximum number of retry attempts for failed syncs
        """
        self.sqlite_manager = sqlite_manager
        self.version_manager = version_manager
        self.conflict_resolver = conflict_resolver
        self.sync_interval = sync_interval
        self.max_retries = max_retries
        self._sync_task: Optional[asyncio.Task] = None
        self._is_running = False
    
    async def start(self) -> None:
        """Start the sync service."""
        if self._is_running:
            return
        
        self._is_running = True
        self._sync_task = asyncio.create_task(self._sync_loop())
        logger.info("Sync service started")
    
    async def stop(self) -> None:
        """Stop the sync service."""
        if not self._is_running:
            return
        
        self._is_running = False
        if self._sync_task:
            self._sync_task.cancel()
            try:
                await self._sync_task
            except asyncio.CancelledError:
                pass
        logger.info("Sync service stopped")
    
    async def _sync_loop(self) -> None:
        """Main sync loop."""
        while self._is_running:
            try:
                await self._process_pending_syncs()
                await asyncio.sleep(self.sync_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in sync loop: {e}")
                await asyncio.sleep(self.sync_interval)
    
    async def _process_pending_syncs(self) -> None:
        """Process all pending sync operations."""
        pending_syncs = self.sqlite_manager.get_pending_syncs()
        
        for sync in pending_syncs:
            try:
                await self._process_sync(sync)
            except Exception as e:
                logger.error(f"Error processing sync {sync['id']}: {e}")
                self._handle_sync_error(sync, str(e))
    
    async def _process_sync(self, sync: Dict[str, Any]) -> None:
        """Process a single sync operation.
        
        Args:
            sync: Sync operation data
        """
        table_name = sync["table_name"]
        record_id = sync["record_id"]
        operation = sync["operation"]
        data = json.loads(sync["data"])
        
        # Check for conflicts
        if operation in ["update", "delete"]:
            local_version = self.version_manager.get_local_version(table_name, record_id)
            server_version = await self.version_manager.get_server_version(table_name, record_id)
            
            if server_version > local_version:
                # Resolve conflict
                resolved_data = await self.conflict_resolver.resolve_conflict(
                    table_name,
                    record_id,
                    local_version,
                    server_version,
                    data
                )
                if resolved_data:
                    data = resolved_data
        
        # Perform sync operation
        success = await self._perform_sync_operation(operation, table_name, record_id, data)
        
        if success:
            self.sqlite_manager.update_sync_status(sync["id"], "completed")
            self.version_manager.update_local_version(table_name, record_id)
        else:
            raise Exception("Sync operation failed")
    
    async def _perform_sync_operation(
        self,
        operation: str,
        table_name: str,
        record_id: int,
        data: Dict[str, Any]
    ) -> bool:
        """Perform the actual sync operation.
        
        Args:
            operation: Operation type
            table_name: Name of the table
            record_id: ID of the record
            data: Record data
            
        Returns:
            bool: True if operation was successful
        """
        # TODO: Implement actual API calls here
        # This is a placeholder for the actual implementation
        return True
    
    def _handle_sync_error(self, sync: Dict[str, Any], error: str) -> None:
        """Handle sync operation error.
        
        Args:
            sync: Sync operation data
            error: Error message
        """
        retry_count = sync.get("retry_count", 0) + 1
        
        if retry_count <= self.max_retries:
            self.sqlite_manager.update_sync_status(
                sync["id"],
                "pending",
                f"Retry {retry_count}/{self.max_retries}: {error}"
            )
        else:
            self.sqlite_manager.update_sync_status(
                sync["id"],
                "failed",
                f"Max retries exceeded: {error}"
            ) 