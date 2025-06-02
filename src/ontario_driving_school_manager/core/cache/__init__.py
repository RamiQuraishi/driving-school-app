"""
Cache Infrastructure

This module provides caching infrastructure for the Ontario Driving School Manager.
It includes Redis and local caching implementations, along with cache invalidation strategies.

Author: Rami Drive School
Date: 2024
"""

from typing import Dict, Any, Optional, Protocol, TypeVar, Generic
from datetime import datetime, timedelta

T = TypeVar('T')

class Cache(Generic[T], Protocol):
    """Cache interface protocol."""
    
    def get(self, key: str) -> Optional[T]:
        """Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        ...
    
    def set(self, key: str, value: T, ttl: Optional[timedelta] = None) -> bool:
        """Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live
            
        Returns:
            True if successful
        """
        ...
    
    def delete(self, key: str) -> bool:
        """Delete value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if successful
        """
        ...
    
    def clear(self) -> bool:
        """Clear all cached values.
        
        Returns:
            True if successful
        """
        ...
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if key exists
        """
        ...

class CacheStats:
    """Cache statistics."""
    
    def __init__(self):
        """Initialize cache statistics."""
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.size = 0
        self.last_updated = datetime.now()
    
    @property
    def hit_rate(self) -> float:
        """Get cache hit rate.
        
        Returns:
            Hit rate as float between 0 and 1
        """
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    def update(self, hit: bool = False, miss: bool = False, eviction: bool = False) -> None:
        """Update statistics.
        
        Args:
            hit: Whether there was a cache hit
            miss: Whether there was a cache miss
            eviction: Whether there was a cache eviction
        """
        if hit:
            self.hits += 1
        if miss:
            self.misses += 1
        if eviction:
            self.evictions += 1
        self.last_updated = datetime.now()

# Export cache implementations
from .redis_cache import RedisCache
from .local_cache import LocalCache
from .cache_invalidation import CacheInvalidator

__all__ = [
    'Cache',
    'CacheStats',
    'RedisCache',
    'LocalCache',
    'CacheInvalidator'
]