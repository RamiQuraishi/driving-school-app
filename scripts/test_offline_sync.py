#!/usr/bin/env python3
"""
Test script for offline sync functionality.
Tests data synchronization between local SQLite and remote server.
"""

import asyncio
import logging
import os
import sqlite3
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import aiohttp
import pytest
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SyncTestData(BaseModel):
    """Test data model for sync operations."""
    id: str
    content: str
    version: int
    last_modified: datetime
    device_id: str

class OfflineSyncTester:
    """Test class for offline sync functionality."""
    
    def __init__(self, db_path: str, api_url: str):
        self.db_path = db_path
        self.api_url = api_url
        self.conn = None
        self.setup_database()
    
    def setup_database(self):
        """Initialize SQLite database with test tables."""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Create test tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sync_test (
                id TEXT PRIMARY KEY,
                content TEXT,
                version INTEGER,
                last_modified TIMESTAMP,
                device_id TEXT,
                sync_status TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sync_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT,
                timestamp TIMESTAMP,
                status TEXT,
                details TEXT
            )
        """)
        
        self.conn.commit()
    
    async def simulate_offline_changes(self, num_changes: int) -> List[SyncTestData]:
        """Simulate making changes while offline."""
        changes = []
        cursor = self.conn.cursor()
        
        for i in range(num_changes):
            test_data = SyncTestData(
                id=f"test_{i}",
                content=f"Offline content {i}",
                version=1,
                last_modified=datetime.now(),
                device_id="test_device"
            )
            
            cursor.execute("""
                INSERT INTO sync_test (id, content, version, last_modified, device_id, sync_status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                test_data.id,
                test_data.content,
                test_data.version,
                test_data.last_modified.isoformat(),
                test_data.device_id,
                "pending"
            ))
            
            changes.append(test_data)
        
        self.conn.commit()
        return changes
    
    async def test_sync_process(self):
        """Test the complete sync process."""
        try:
            # Simulate offline changes
            changes = await self.simulate_offline_changes(5)
            logger.info(f"Created {len(changes)} offline changes")
            
            # Simulate network reconnection
            await asyncio.sleep(2)
            
            # Attempt sync
            success = await self.perform_sync()
            assert success, "Sync process failed"
            
            # Verify sync results
            verified = await self.verify_sync_results(changes)
            assert verified, "Sync verification failed"
            
            logger.info("Sync test completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Sync test failed: {str(e)}")
            return False
    
    async def perform_sync(self) -> bool:
        """Perform the sync operation."""
        try:
            async with aiohttp.ClientSession() as session:
                # Get pending changes
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM sync_test WHERE sync_status = 'pending'")
                pending_changes = cursor.fetchall()
                
                # Sync each change
                for change in pending_changes:
                    async with session.post(
                        f"{self.api_url}/sync",
                        json={
                            "id": change[0],
                            "content": change[1],
                            "version": change[2],
                            "last_modified": change[3],
                            "device_id": change[4]
                        }
                    ) as response:
                        if response.status == 200:
                            cursor.execute(
                                "UPDATE sync_test SET sync_status = 'synced' WHERE id = ?",
                                (change[0],)
                            )
                            self.conn.commit()
                
                return True
                
        except Exception as e:
            logger.error(f"Sync operation failed: {str(e)}")
            return False
    
    async def verify_sync_results(self, changes: List[SyncTestData]) -> bool:
        """Verify that changes were properly synced."""
        try:
            cursor = self.conn.cursor()
            for change in changes:
                cursor.execute(
                    "SELECT sync_status FROM sync_test WHERE id = ?",
                    (change.id,)
                )
                result = cursor.fetchone()
                if not result or result[0] != "synced":
                    return False
            return True
            
        except Exception as e:
            logger.error(f"Verification failed: {str(e)}")
            return False

@pytest.mark.asyncio
async def test_offline_sync():
    """Main test function."""
    tester = OfflineSyncTester(
        db_path="test_sync.db",
        api_url="http://localhost:8000/api"
    )
    
    success = await tester.test_sync_process()
    assert success, "Offline sync test failed"

if __name__ == "__main__":
    asyncio.run(test_offline_sync()) 