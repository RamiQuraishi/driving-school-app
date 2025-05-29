"""Version management for offline data."""

import logging
from typing import Any, Dict, Optional, List
from datetime import datetime
import json

from .sqlite_manager import SQLiteManager

logger = logging.getLogger(__name__)

class VersionManager:
    """Manages version tracking for records."""
    
    def __init__(self, sqlite_manager: SQLiteManager):
        """Initialize version manager.
        
        Args:
            sqlite_manager: SQLite manager instance
        """
        self.sqlite_manager = sqlite_manager
        self._initialize_version_tracking()
    
    def _initialize_version_tracking(self) -> None:
        """Initialize version tracking tables."""
        try:
            self.sqlite_manager._connection.executescript("""
                CREATE TABLE IF NOT EXISTS version_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_name TEXT NOT NULL,
                    record_id INTEGER NOT NULL,
                    version INTEGER NOT NULL,
                    data TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    UNIQUE(table_name, record_id, version)
                );
                
                CREATE INDEX IF NOT EXISTS idx_version_tracking_lookup 
                ON version_tracking(table_name, record_id);
            """)
            
            self.sqlite_manager._connection.commit()
            logger.info("Version tracking initialized")
        except Exception as e:
            logger.error(f"Error initializing version tracking: {e}")
            raise
    
    def get_local_version(self, table_name: str, record_id: int) -> int:
        """Get the local version number for a record.
        
        Args:
            table_name: Name of the table
            record_id: ID of the record
            
        Returns:
            int: Version number
        """
        try:
            cursor = self.sqlite_manager._connection.execute(
                """
                SELECT MAX(version) as version
                FROM version_tracking
                WHERE table_name = ? AND record_id = ?
                """,
                (table_name, record_id)
            )
            row = cursor.fetchone()
            return row["version"] if row and row["version"] is not None else 0
        except Exception as e:
            logger.error(f"Error getting local version: {e}")
            return 0
    
    async def get_server_version(self, table_name: str, record_id: int) -> int:
        """Get the server version number for a record.
        
        Args:
            table_name: Name of the table
            record_id: ID of the record
            
        Returns:
            int: Version number
        """
        # TODO: Implement server version check
        # This is a placeholder for the actual implementation
        return 0
    
    def update_local_version(
        self,
        table_name: str,
        record_id: int,
        data: Optional[Dict[str, Any]] = None
    ) -> int:
        """Update the local version number for a record.
        
        Args:
            table_name: Name of the table
            record_id: ID of the record
            data: Record data to store with version
            
        Returns:
            int: New version number
        """
        try:
            current_version = self.get_local_version(table_name, record_id)
            new_version = current_version + 1
            
            if data is None:
                # Get current data
                cursor = self.sqlite_manager._connection.execute(
                    """
                    SELECT data
                    FROM version_tracking
                    WHERE table_name = ? AND record_id = ? AND version = ?
                    """,
                    (table_name, record_id, current_version)
                )
                row = cursor.fetchone()
                data = json.loads(row["data"]) if row else {}
            
            # Store new version
            self.sqlite_manager._connection.execute(
                """
                INSERT INTO version_tracking
                (table_name, record_id, version, data, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    table_name,
                    record_id,
                    new_version,
                    json.dumps(data),
                    datetime.utcnow().isoformat()
                )
            )
            
            self.sqlite_manager._connection.commit()
            logger.debug(f"Updated version for {table_name}:{record_id} to {new_version}")
            return new_version
            
        except Exception as e:
            logger.error(f"Error updating local version: {e}")
            raise
    
    async def get_server_data(
        self,
        table_name: str,
        record_id: int,
        version: int
    ) -> Optional[Dict[str, Any]]:
        """Get server data for a specific version.
        
        Args:
            table_name: Name of the table
            record_id: ID of the record
            version: Version number
            
        Returns:
            Optional[Dict[str, Any]]: Record data if found
        """
        # TODO: Implement server data retrieval
        # This is a placeholder for the actual implementation
        return None
    
    def get_version_history(
        self,
        table_name: str,
        record_id: int,
        start_version: Optional[int] = None,
        end_version: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get version history for a record.
        
        Args:
            table_name: Name of the table
            record_id: ID of the record
            start_version: Start version number (inclusive)
            end_version: End version number (inclusive)
            
        Returns:
            List[Dict[str, Any]]: List of version records
        """
        try:
            query = """
                SELECT *
                FROM version_tracking
                WHERE table_name = ? AND record_id = ?
            """
            params = [table_name, record_id]
            
            if start_version is not None:
                query += " AND version >= ?"
                params.append(start_version)
            
            if end_version is not None:
                query += " AND version <= ?"
                params.append(end_version)
            
            query += " ORDER BY version"
            
            cursor = self.sqlite_manager._connection.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            logger.error(f"Error getting version history: {e}")
            return []
    
    def cleanup_old_versions(
        self,
        table_name: str,
        record_id: int,
        keep_versions: int = 10
    ) -> None:
        """Clean up old versions of a record.
        
        Args:
            table_name: Name of the table
            record_id: ID of the record
            keep_versions: Number of recent versions to keep
        """
        try:
            self.sqlite_manager._connection.execute(
                """
                DELETE FROM version_tracking
                WHERE table_name = ? AND record_id = ? AND version NOT IN (
                    SELECT version
                    FROM version_tracking
                    WHERE table_name = ? AND record_id = ?
                    ORDER BY version DESC
                    LIMIT ?
                )
                """,
                (table_name, record_id, table_name, record_id, keep_versions)
            )
            
            self.sqlite_manager._connection.commit()
            logger.debug(f"Cleaned up old versions for {table_name}:{record_id}")
            
        except Exception as e:
            logger.error(f"Error cleaning up old versions: {e}")
            raise 