"""
Error Recovery Patterns

This package provides error recovery patterns for the Ontario Driving School Manager.
It includes circuit breaker, retry policies, and dead letter queue implementations.

Author: Rami Drive School
Date: 2024
"""

from .circuit_breaker import CircuitBreaker
from .retry_policy import RetryPolicy
from .dead_letter_queue import DeadLetterQueue

__all__ = [
    'CircuitBreaker',
    'RetryPolicy',
    'DeadLetterQueue'
] 