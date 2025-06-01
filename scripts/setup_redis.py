"""
Redis Setup Script

This script sets up Redis for caching in the application.
It configures Redis with appropriate settings and creates necessary keys.

Author: Rami Drive School
Date: 2024
"""

import os
import sys
import redis
import logging
from typing import Dict, Any, Optional
from pathlib import Path

# Add src to Python path
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)

from ontario_driving_school_manager.core.cache.redis_cache import RedisCache
from ontario_driving_school_manager.core.cache.cache_invalidation import CacheInvalidator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RedisSetup:
    """Redis setup and configuration."""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None
    ):
        """Initialize Redis setup.
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
            password: Redis password
        """
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.redis_client = None
        self.cache = None
        self.invalidator = None
    
    def connect(self) -> bool:
        """Connect to Redis.
        
        Returns:
            True if connection successful
        """
        try:
            self.redis_client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=True
            )
            self.redis_client.ping()
            logger.info("Successfully connected to Redis")
            return True
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            return False
    
    def setup_cache(self) -> None:
        """Set up Redis cache."""
        if not self.redis_client:
            raise RuntimeError("Redis client not initialized")
        
        self.cache = RedisCache(self.redis_client)
        self.invalidator = CacheInvalidator(self.redis_client)
        
        # Configure cache settings
        self.redis_client.config_set('maxmemory', '512mb')
        self.redis_client.config_set('maxmemory-policy', 'allkeys-lru')
        
        logger.info("Cache setup completed")
    
    def create_indexes(self) -> None:
        """Create Redis indexes for efficient querying."""
        if not self.redis_client:
            raise RuntimeError("Redis client not initialized")
        
        # Create indexes for common queries
        self.redis_client.execute_command(
            'FT.CREATE',
            'idx:students',
            'ON',
            'HASH',
            'PREFIX',
            '1',
            'student:',
            'SCHEMA',
            'first_name', 'TEXT',
            'last_name', 'TEXT',
            'email', 'TEXT',
            'phone', 'TEXT'
        )
        
        self.redis_client.execute_command(
            'FT.CREATE',
            'idx:instructors',
            'ON',
            'HASH',
            'PREFIX',
            '1',
            'instructor:',
            'SCHEMA',
            'first_name', 'TEXT',
            'last_name', 'TEXT',
            'email', 'TEXT',
            'phone', 'TEXT'
        )
        
        logger.info("Indexes created successfully")
    
    def setup_pubsub(self) -> None:
        """Set up Redis pub/sub for cache invalidation."""
        if not self.redis_client:
            raise RuntimeError("Redis client not initialized")
        
        # Create pub/sub channels
        self.redis_client.publish('cache:invalidate', 'setup')
        logger.info("Pub/sub setup completed")
    
    def verify_setup(self) -> Dict[str, Any]:
        """Verify Redis setup.
        
        Returns:
            Dictionary of verification results
        """
        if not self.redis_client:
            raise RuntimeError("Redis client not initialized")
        
        results = {
            "connection": self.redis_client.ping(),
            "memory_usage": self.redis_client.info()['used_memory_human'],
            "maxmemory": self.redis_client.config_get('maxmemory'),
            "maxmemory_policy": self.redis_client.config_get('maxmemory-policy'),
            "indexes": self.redis_client.execute_command('FT._LIST')
        }
        
        logger.info("Setup verification completed")
        return results

def main():
    """Run Redis setup."""
    # Get Redis configuration from environment
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    redis_db = int(os.getenv('REDIS_DB', '0'))
    redis_password = os.getenv('REDIS_PASSWORD')
    
    # Initialize and run setup
    setup = RedisSetup(
        host=redis_host,
        port=redis_port,
        db=redis_db,
        password=redis_password
    )
    
    if not setup.connect():
        sys.exit(1)
    
    try:
        setup.setup_cache()
        setup.create_indexes()
        setup.setup_pubsub()
        
        # Verify setup
        results = setup.verify_setup()
        logger.info("Setup verification results:")
        for key, value in results.items():
            logger.info(f"{key}: {value}")
        
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 