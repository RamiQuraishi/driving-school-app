"""
Redis Cache Implementation

This module provides Redis-based caching for the Ontario Driving School Manager.
It implements the Cache protocol with Redis-specific optimizations.

Author: Rami Drive School
Date: 2024
"""

import json
import logging
from typing import Dict, Any, Optional, TypeVar, Generic, Type
from datetime import datetime, timedelta
import redis

from . import Cache, CacheStats

logger = logging.getLogger(__name__)

T = TypeVar('T')

class RedisCache(Cache[T], Generic[T]):
    """Redis-based cache implementation."""
    
    def __init__(
        self,
        redis_client: redis.Redis,
        default_ttl: Optional[timedelta] = None,
        value_type: Optional[Type[T]] = None
    ):
        """Initialize Redis cache.
        
        Args:
            redis_client: Redis client instance
            default_ttl: Default time to live for cached values
            value_type: Type of cached values
        """
        self.redis = redis_client
        self.default_ttl = default_ttl
        self.value_type = value_type
        self.stats = CacheStats()
    
    def get(self, key: str) -> Optional[T]:
        """Get value from Redis cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        try:
            value = self.redis.get(key)
            if value is None:
                self.stats.update(miss=True)
                return None
            
            # Deserialize value
            if self.value_type:
                value = self._deserialize(value)
            
            self.stats.update(hit=True)
            return value
            
        except redis.RedisError as e:
            logger.error(f"Redis error getting key {key}: {e}")
            return None
    
    def set(self, key: str, value: T, ttl: Optional[timedelta] = None) -> bool:
        """Set value in Redis cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live
            
        Returns:
            True if successful
        """
        try:
            # Serialize value
            if self.value_type:
                value = self._serialize(value)
            
            # Set value with TTL
            ttl_seconds = int((ttl or self.default_ttl or timedelta()).total_seconds())
            if ttl_seconds > 0:
                self.redis.setex(key, ttl_seconds, value)
            else:
                self.redis.set(key, value)
            
            return True
            
        except redis.RedisError as e:
            logger.error(f"Redis error setting key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete value from Redis cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if successful
        """
        try:
            return bool(self.redis.delete(key))
        except redis.RedisError as e:
            logger.error(f"Redis error deleting key {key}: {e}")
            return False
    
    def clear(self) -> bool:
        """Clear all cached values.
        
        Returns:
            True if successful
        """
        try:
            self.redis.flushdb()
            return True
        except redis.RedisError as e:
            logger.error(f"Redis error clearing cache: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in Redis cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if key exists
        """
        try:
            return bool(self.redis.exists(key))
        except redis.RedisError as e:
            logger.error(f"Redis error checking key {key}: {e}")
            return False
    
    def _serialize(self, value: T) -> str:
        """Serialize value for Redis storage.
        
        Args:
            value: Value to serialize
            
        Returns:
            Serialized value
        """
        if isinstance(value, (str, int, float, bool)):
            return str(value)
        return json.dumps(value)
    
    def _deserialize(self, value: str) -> T:
        """Deserialize value from Redis storage.
        
        Args:
            value: Value to deserialize
            
        Returns:
            Deserialized value
        """
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value