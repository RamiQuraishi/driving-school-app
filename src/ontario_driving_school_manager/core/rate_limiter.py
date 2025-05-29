"""
Rate Limiter

This module implements rate limiting for the desktop application to prevent
overloading of resources and ensure fair usage.

Author: Rami Drive School
Date: 2024
"""

import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional

@dataclass
class RateLimitConfig:
    """Rate limit configuration."""
    max_requests: int  # Maximum number of requests
    time_window: float  # Time window in seconds
    burst_size: Optional[int] = None  # Maximum burst size

class RateLimiter:
    """Rate limiter implementation."""
    
    def __init__(
        self,
        config: RateLimitConfig,
        key_prefix: str = "rate_limit"
    ):
        """Initialize rate limiter.
        
        Args:
            config: Rate limit configuration
            key_prefix: Key prefix for rate limit tracking
        """
        self.config = config
        self.key_prefix = key_prefix
        self.requests: Dict[str, list] = {}
    
    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed.
        
        Args:
            key: Rate limit key
            
        Returns:
            bool: True if request is allowed
        """
        full_key = f"{self.key_prefix}:{key}"
        now = time.time()
        
        # Initialize request history if needed
        if full_key not in self.requests:
            self.requests[full_key] = []
        
        # Remove old requests
        self.requests[full_key] = [
            t for t in self.requests[full_key]
            if now - t < self.config.time_window
        ]
        
        # Check burst limit
        if (
            self.config.burst_size
            and len(self.requests[full_key]) >= self.config.burst_size
        ):
            return False
        
        # Check rate limit
        if len(self.requests[full_key]) >= self.config.max_requests:
            return False
        
        # Add request
        self.requests[full_key].append(now)
        return True
    
    def get_remaining_requests(self, key: str) -> int:
        """Get remaining requests.
        
        Args:
            key: Rate limit key
            
        Returns:
            int: Number of remaining requests
        """
        full_key = f"{self.key_prefix}:{key}"
        now = time.time()
        
        if full_key not in self.requests:
            return self.config.max_requests
        
        # Remove old requests
        self.requests[full_key] = [
            t for t in self.requests[full_key]
            if now - t < self.config.time_window
        ]
        
        return max(0, self.config.max_requests - len(self.requests[full_key]))
    
    def get_reset_time(self, key: str) -> datetime:
        """Get rate limit reset time.
        
        Args:
            key: Rate limit key
            
        Returns:
            datetime: Reset time
        """
        full_key = f"{self.key_prefix}:{key}"
        now = time.time()
        
        if full_key not in self.requests or not self.requests[full_key]:
            return datetime.utcnow()
        
        # Get oldest request
        oldest = min(self.requests[full_key])
        
        # Calculate reset time
        reset_time = oldest + self.config.time_window
        
        return datetime.utcnow() + timedelta(seconds=reset_time - now)
    
    def reset(self, key: str) -> None:
        """Reset rate limit for key.
        
        Args:
            key: Rate limit key
        """
        full_key = f"{self.key_prefix}:{key}"
        if full_key in self.requests:
            del self.requests[full_key]
    
    def reset_all(self) -> None:
        """Reset all rate limits."""
        self.requests.clear() 