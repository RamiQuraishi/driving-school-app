"""
Retry Policy with Exponential Backoff

This module implements retry policies with exponential backoff for handling
temporary failures in operations.

Author: Rami Drive School
Date: 2024
"""

import time
import random
from typing import Any, Callable, Optional, Type, Union, Tuple
from dataclasses import dataclass

@dataclass
class RetryConfig:
    """Retry policy configuration."""
    max_attempts: int = 3  # Maximum number of retry attempts
    initial_delay: float = 1.0  # Initial delay in seconds
    max_delay: float = 60.0  # Maximum delay in seconds
    exponential_base: float = 2.0  # Base for exponential backoff
    jitter: bool = True  # Whether to add random jitter
    jitter_factor: float = 0.1  # Jitter factor (0.0 to 1.0)

class RetryPolicy:
    """Retry policy implementation."""
    
    def __init__(
        self,
        config: Optional[RetryConfig] = None,
        retry_on: Optional[Union[Type[Exception], Tuple[Type[Exception], ...]]] = None
    ):
        """Initialize retry policy.
        
        Args:
            config: Retry configuration
            retry_on: Exception type(s) to retry on
        """
        self.config = config or RetryConfig()
        self.retry_on = retry_on or Exception
    
    def execute(
        self,
        func: Callable[..., Any],
        *args,
        **kwargs
    ) -> Any:
        """Execute function with retry policy.
        
        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
            
        Raises:
            Exception: If all retry attempts fail
        """
        last_exception = None
        
        for attempt in range(self.config.max_attempts):
            try:
                return func(*args, **kwargs)
            except self.retry_on as e:
                last_exception = e
                
                if attempt < self.config.max_attempts - 1:
                    delay = self._calculate_delay(attempt)
                    time.sleep(delay)
                else:
                    break
        
        raise last_exception
    
    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay for retry attempt.
        
        Args:
            attempt: Retry attempt number
            
        Returns:
            float: Delay in seconds
        """
        # Calculate exponential delay
        delay = min(
            self.config.initial_delay * (self.config.exponential_base ** attempt),
            self.config.max_delay
        )
        
        # Add jitter if enabled
        if self.config.jitter:
            jitter = delay * self.config.jitter_factor
            delay = delay + random.uniform(-jitter, jitter)
        
        return max(0.0, delay)
    
    def with_config(self, config: RetryConfig) -> 'RetryPolicy':
        """Create new retry policy with configuration.
        
        Args:
            config: Retry configuration
            
        Returns:
            RetryPolicy: New retry policy
        """
        return RetryPolicy(config, self.retry_on)
    
    def with_retry_on(
        self,
        retry_on: Union[Type[Exception], Tuple[Type[Exception], ...]]
    ) -> 'RetryPolicy':
        """Create new retry policy with exception types.
        
        Args:
            retry_on: Exception type(s) to retry on
            
        Returns:
            RetryPolicy: New retry policy
        """
        return RetryPolicy(self.config, retry_on) 