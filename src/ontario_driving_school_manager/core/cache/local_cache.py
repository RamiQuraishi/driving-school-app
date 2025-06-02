"""
Local Cache Implementation

This module provides local caching for the Ontario Driving School Manager's Electron app.
It implements the Cache protocol with in-memory storage and persistence.

Author: Rami Drive School
Date: 2024
"""

import json
import logging
import os
from typing import Dict, Any, Optional, TypeVar, Generic, Type
from datetime import datetime, timedelta
from collections import OrderedDict

from . import Cache, CacheStats

logger = logging.getLogger(__name__)

T = TypeVar('T')

class LRUCache(OrderedDict):
    """Least Recently Used (LRU) cache implementation."""
    
    def __init__(self, maxsize: int = 1000):
        """Initialize LRU cache.
        
        Args:
            maxsize: Maximum number of items to cache
        """
        super().__init__()
        self.maxsize = maxsize
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        if key not in self:
            return None
        
        # Move to end (most recently used)
        value = self.pop(key)
        self[key] = value
        return value
    
    def put(self, key: str, value: Any) -> None:
        """Put value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        if key in self:
            self.pop(key)
        elif len(self) >= self.maxsize:
            # Remove least recently used item
            self.popitem(last=False)
        
        self[key] = value

class LocalCache(Cache[T], Generic[T]):
    """Local cache implementation for Electron."""
    
    def __init__(
        self,
        storage_path: str,
        maxsize: int = 1000,
        default_ttl: Optional[timedelta] = None,
        value_type: Optional[Type[T]] = None
    ):
        """Initialize local cache.
        
        Args:
            storage_path: Path to persistent storage
            maxsize: Maximum number of items to cache
            default_ttl: Default time to live for cached values
            value_type: Type of cached values
        """
        self.storage_path = storage_path
        self.cache = LRUCache(maxsize)
        self.default_ttl = default_ttl
        self.value_type = value_type
        self.stats = CacheStats()
        self.expiry_times: Dict[str, datetime] = {}
        
        # Load persistent cache
        self._load()
    
    def get(self, key: str) -> Optional[T]:
        """Get value from local cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        # Check expiry
        if key in self.expiry_times:
            if datetime.now() > self.expiry_times[key]:
                self.delete(key)
                self.stats.update(miss=True)
                return None
        
        # Get value
        value = self.cache.get(key)
        if value is None:
            self.stats.update(miss=True)
            return None
        
        # Deserialize value
        if self.value_type:
            value = self._deserialize(value)
        
        self.stats.update(hit=True)
        return value
    
    def set(self, key: str, value: T, ttl: Optional[timedelta] = None) -> bool:
        """Set value in local cache.
        
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
            
            # Set value
            self.cache.put(key, value)
            
            # Set expiry
            if ttl or self.default_ttl:
                self.expiry_times[key] = datetime.now() + (ttl or self.default_ttl)
            
            # Save to persistent storage
            self._save()
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete value from local cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if successful
        """
        try:
            if key in self.cache:
                del self.cache[key]
            if key in self.expiry_times:
                del self.expiry_times[key]
            
            # Save to persistent storage
            self._save()
            
            return True
            
        except Exception as e:
            logger.error(f"Error deleting key {key}: {e}")
            return False
    
    def clear(self) -> bool:
        """Clear all cached values.
        
        Returns:
            True if successful
        """
        try:
            self.cache.clear()
            self.expiry_times.clear()
            
            # Save to persistent storage
            self._save()
            
            return True
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in local cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if key exists
        """
        if key not in self.cache:
            return False
        
        # Check expiry
        if key in self.expiry_times:
            if datetime.now() > self.expiry_times[key]:
                self.delete(key)
                return False
        
        return True
    
    def _serialize(self, value: T) -> str:
        """Serialize value for storage.
        
        Args:
            value: Value to serialize
            
        Returns:
            Serialized value
        """
        if isinstance(value, (str, int, float, bool)):
            return str(value)
        return json.dumps(value)
    
    def _deserialize(self, value: str) -> T:
        """Deserialize value from storage.
        
        Args:
            value: Value to deserialize
            
        Returns:
            Deserialized value
        """
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    
    def _save(self) -> None:
        """Save cache to persistent storage."""
        try:
            data = {
                'cache': dict(self.cache),
                'expiry_times': {
                    k: v.isoformat()
                    for k, v in self.expiry_times.items()
                }
            }
            
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump(data, f)
                
        except Exception as e:
            logger.error(f"Error saving cache: {e}")
    
    def _load(self) -> None:
        """Load cache from persistent storage."""
        try:
            if not os.path.exists(self.storage_path):
                return
            
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
            
            # Load cache
            self.cache.clear()
            self.cache.update(data['cache'])
            
            # Load expiry times
            self.expiry_times.clear()
            self.expiry_times.update({
                k: datetime.fromisoformat(v)
                for k, v in data['expiry_times'].items()
            })
            
        except Exception as e:
            logger.error(f"Error loading cache: {e}")