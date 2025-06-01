"""
Cache Performance Test Script

This script tests and validates different caching strategies and their performance.

Author: Rami Drive School
Date: 2024
"""

import time
import random
import pytest
from typing import Dict, Any, List
from datetime import datetime, timedelta

class CacheStrategy:
    """Base class for cache strategies."""
    
    def __init__(self, max_size: int = 1000):
        """Initialize cache strategy.
        
        Args:
            max_size: Maximum number of items in cache
        """
        self.max_size = max_size
        self.cache: Dict[str, Any] = {}
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Any:
        """Get item from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Set item in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        if len(self.cache) >= self.max_size:
            self._evict()
        self.cache[key] = value
    
    def _evict(self) -> None:
        """Evict item from cache."""
        raise NotImplementedError
    
    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics.
        
        Returns:
            Dictionary of cache statistics
        """
        return {
            "hits": self.hits,
            "misses": self.misses,
            "size": len(self.cache),
            "hit_rate": self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0
        }

class LRUCache(CacheStrategy):
    """Least Recently Used cache implementation."""
    
    def __init__(self, max_size: int = 1000):
        """Initialize LRU cache.
        
        Args:
            max_size: Maximum number of items in cache
        """
        super().__init__(max_size)
        self.access_times: Dict[str, datetime] = {}
    
    def get(self, key: str) -> Any:
        """Get item from cache and update access time.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        value = super().get(key)
        if value is not None:
            self.access_times[key] = datetime.now()
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set item in cache and update access time.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        super().set(key, value)
        self.access_times[key] = datetime.now()
    
    def _evict(self) -> None:
        """Evict least recently used item."""
        if not self.access_times:
            return
        
        lru_key = min(self.access_times.items(), key=lambda x: x[1])[0]
        del self.cache[lru_key]
        del self.access_times[lru_key]

class FIFOCache(CacheStrategy):
    """First In First Out cache implementation."""
    
    def __init__(self, max_size: int = 1000):
        """Initialize FIFO cache.
        
        Args:
            max_size: Maximum number of items in cache
        """
        super().__init__(max_size)
        self.insertion_order: List[str] = []
    
    def set(self, key: str, value: Any) -> None:
        """Set item in cache and update insertion order.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        super().set(key, value)
        self.insertion_order.append(key)
    
    def _evict(self) -> None:
        """Evict first inserted item."""
        if not self.insertion_order:
            return
        
        oldest_key = self.insertion_order.pop(0)
        del self.cache[oldest_key]

def generate_test_data(size: int) -> List[tuple]:
    """Generate test data.
    
    Args:
        size: Number of test items to generate
        
    Returns:
        List of (key, value) tuples
    """
    return [(f"key_{i}", f"value_{i}") for i in range(size)]

def test_cache_performance():
    """Test cache performance with different strategies."""
    # Test parameters
    cache_size = 100
    num_operations = 1000
    test_data = generate_test_data(num_operations)
    
    # Initialize caches
    lru_cache = LRUCache(max_size=cache_size)
    fifo_cache = FIFOCache(max_size=cache_size)
    
    # Test write performance
    start_time = time.time()
    for key, value in test_data:
        lru_cache.set(key, value)
    lru_write_time = time.time() - start_time
    
    start_time = time.time()
    for key, value in test_data:
        fifo_cache.set(key, value)
    fifo_write_time = time.time() - start_time
    
    # Test read performance
    start_time = time.time()
    for key, _ in test_data:
        lru_cache.get(key)
    lru_read_time = time.time() - start_time
    
    start_time = time.time()
    for key, _ in test_data:
        fifo_cache.get(key)
    fifo_read_time = time.time() - start_time
    
    # Print results
    print("\nCache Performance Results:")
    print("-------------------------")
    print(f"LRU Cache:")
    print(f"  Write time: {lru_write_time:.4f} seconds")
    print(f"  Read time: {lru_read_time:.4f} seconds")
    print(f"  Hit rate: {lru_cache.get_stats()['hit_rate']:.2%}")
    print(f"\nFIFO Cache:")
    print(f"  Write time: {fifo_write_time:.4f} seconds")
    print(f"  Read time: {fifo_read_time:.4f} seconds")
    print(f"  Hit rate: {fifo_cache.get_stats()['hit_rate']:.2%}")

def test_cache_eviction():
    """Test cache eviction strategies."""
    cache_size = 5
    lru_cache = LRUCache(max_size=cache_size)
    fifo_cache = FIFOCache(max_size=cache_size)
    
    # Fill caches
    for i in range(10):
        lru_cache.set(f"key_{i}", f"value_{i}")
        fifo_cache.set(f"key_{i}", f"value_{i}")
    
    # Verify cache size
    assert len(lru_cache.cache) == cache_size
    assert len(fifo_cache.cache) == cache_size
    
    # Verify eviction
    assert "key_0" not in lru_cache.cache  # Should be evicted
    assert "key_0" not in fifo_cache.cache  # Should be evicted
    assert "key_9" in lru_cache.cache  # Should be kept
    assert "key_9" in fifo_cache.cache  # Should be kept

if __name__ == "__main__":
    test_cache_performance()
    pytest.main([__file__]) 