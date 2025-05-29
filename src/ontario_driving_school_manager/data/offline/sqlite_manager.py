"""SQLite database manager for offline storage."""

import logging
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class SQLiteManager:
    """Manages SQLite database for offline storage."""
    
    def __init__(self, db_path: str = "offline_data.db"):
        """Initialize SQLite manager.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = Path(db_path)
        self._connection: Optional[sqlite3.Connection] = None
        self._initialize_db()
    
    def _initialize_db(self) -> None:
        """Initialize the SQLite database with required tables."""
        try:
            self._connection = sqlite3.connect(str(self.db_path))
            self._connection.row_factory = sqlite3.Row
            
            # Create tables for offline storage
            self._connection.executescript("""
                CREATE TABLE IF NOT EXISTS offline_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_name TEXT NOT NULL,
                    record_id INTEGER NOT NULL,
                    data TEXT NOT NULL,
                    version INTEGER NOT NULL,
                    sync_status TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    UNIQUE(table_name, record_id)
                );
                
                CREATE TABLE IF NOT EXISTS sync_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation TEXT NOT NULL,
                    table_name TEXT NOT NULL,
                    record_id INTEGER NOT NULL,
                    data TEXT NOT NULL,
                    status TEXT NOT NULL,
                    error TEXT,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL
                );
                
                CREATE INDEX IF NOT EXISTS idx_offline_records_sync 
                ON offline_records(sync_status);
                
                CREATE INDEX IF NOT EXISTS idx_sync_queue_status 
                ON sync_queue(status);
            """)
            
            self._connection.commit()
            logger.info("SQLite database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing SQLite database: {e}")
            raise
    
    def store_record(self, table_name: str, record_id: int, data: Dict[str, Any], version: int) -> None:
        """Store a record in the offline database.
        
        Args:
            table_name: Name of the table
            record_id: ID of the record
            data: Record data as dictionary
            version: Version number of the record
        """
        try:
            now = datetime.utcnow().isoformat()
            self._connection.execute(
                """
                INSERT OR REPLACE INTO offline_records 
                (table_name, record_id, data, version, sync_status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (table_name, record_id, json.dumps(data), version, "pending", now, now)
            )
            self._connection.commit()
            logger.debug(f"Stored record {record_id} from {table_name}")
        except Exception as e:
            logger.error(f"Error storing record: {e}")
            raise
    
    def get_record(self, table_name: str, record_id: int) -> Optional[Dict[str, Any]]:
        """Get a record from the offline database.
        
        Args:
            table_name: Name of the table
            record_id: ID of the record
            
        Returns:
            Optional[Dict[str, Any]]: Record data if found, None otherwise
        """
        try:
            cursor = self._connection.execute(
                "SELECT * FROM offline_records WHERE table_name = ? AND record_id = ?",
                (table_name, record_id)
            )
            row = cursor.fetchone()
            if row:
                return json.loads(row["data"])
            return None
        except Exception as e:
            logger.error(f"Error getting record: {e}")
            raise
    
    def queue_sync(self, operation: str, table_name: str, record_id: int, data: Dict[str, Any]) -> None:
        """Queue a record for synchronization.
        
        Args:
            operation: Operation type (insert, update, delete)
            table_name: Name of the table
            record_id: ID of the record
            data: Record data as dictionary
        """
        try:
            now = datetime.utcnow().isoformat()
            self._connection.execute(
                """
                INSERT INTO sync_queue 
                (operation, table_name, record_id, data, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (operation, table_name, record_id, json.dumps(data), "pending", now, now)
            )
            self._connection.commit()
            logger.debug(f"Queued {operation} for record {record_id} from {table_name}")
        except Exception as e:
            logger.error(f"Error queueing sync: {e}")
            raise
    
    def get_pending_syncs(self) -> List[Dict[str, Any]]:
        """Get all pending sync operations.
        
        Returns:
            List[Dict[str, Any]]: List of pending sync operations
        """
        try:
            cursor = self._connection.execute(
                "SELECT * FROM sync_queue WHERE status = 'pending' ORDER BY created_at"
            )
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting pending syncs: {e}")
            raise
    
    def update_sync_status(self, sync_id: int, status: str, error: Optional[str] = None) -> None:
        """Update the status of a sync operation.
        
        Args:
            sync_id: ID of the sync operation
            status: New status
            error: Error message if any
        """
        try:
            now = datetime.utcnow().isoformat()
            self._connection.execute(
                """
                UPDATE sync_queue 
                SET status = ?, error = ?, updated_at = ?
                WHERE id = ?
                """,
                (status, error, now, sync_id)
            )
            self._connection.commit()
            logger.debug(f"Updated sync {sync_id} status to {status}")
        except Exception as e:
            logger.error(f"Error updating sync status: {e}")
            raise
    
    def close(self) -> None:
        """Close the database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
            logger.info("SQLite database connection closed") 