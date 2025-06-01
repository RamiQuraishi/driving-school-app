"""
Circuit Breaker Test Script

This script tests the circuit breaker pattern implementation with various scenarios.

Author: Rami Drive School
Date: 2024
"""

import time
import pytest
from datetime import datetime
from prototypes.error_recovery_demo.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitState
)

def test_circuit_breaker_initial_state():
    """Test initial circuit breaker state."""
    breaker = CircuitBreaker()
    assert breaker.get_state() == CircuitState.CLOSED
    assert breaker.failure_count == 0
    assert breaker.success_count == 0

def test_circuit_breaker_successful_execution():
    """Test successful function execution."""
    breaker = CircuitBreaker()
    
    def success_func():
        return "success"
    
    result = breaker.execute(success_func)
    assert result == "success"
    assert breaker.get_state() == CircuitState.CLOSED
    assert breaker.failure_count == 0

def test_circuit_breaker_failure_threshold():
    """Test circuit opening after failure threshold."""
    config = CircuitBreakerConfig(failure_threshold=3)
    breaker = CircuitBreaker(config)
    
    def failing_func():
        raise Exception("Test failure")
    
    # Execute failing function multiple times
    for _ in range(3):
        with pytest.raises(Exception):
            breaker.execute(failing_func)
    
    assert breaker.get_state() == CircuitState.OPEN
    assert breaker.failure_count == 3

def test_circuit_breaker_recovery():
    """Test circuit recovery after timeout."""
    config = CircuitBreakerConfig(
        failure_threshold=2,
        reset_timeout=1,
        success_threshold=2
    )
    breaker = CircuitBreaker(config)
    
    def failing_func():
        raise Exception("Test failure")
    
    def success_func():
        return "success"
    
    # Open the circuit
    for _ in range(2):
        with pytest.raises(Exception):
            breaker.execute(failing_func)
    
    assert breaker.get_state() == CircuitState.OPEN
    
    # Wait for recovery timeout
    time.sleep(1.1)
    
    # Test half-open state
    result = breaker.execute(success_func)
    assert result == "success"
    assert breaker.get_state() == CircuitState.HALF_OPEN
    
    # Complete recovery
    result = breaker.execute(success_func)
    assert result == "success"
    assert breaker.get_state() == CircuitState.CLOSED

def test_circuit_breaker_metrics():
    """Test circuit breaker metrics collection."""
    breaker = CircuitBreaker()
    metrics = breaker.get_metrics()
    
    assert "state" in metrics
    assert "failure_count" in metrics
    assert "success_count" in metrics
    assert "last_failure_time" in metrics
    assert "last_state_change" in metrics
    assert "time_in_current_state" in metrics

def test_circuit_breaker_custom_config():
    """Test circuit breaker with custom configuration."""
    config = CircuitBreakerConfig(
        failure_threshold=2,
        reset_timeout=30,
        half_open_timeout=15,
        success_threshold=3
    )
    breaker = CircuitBreaker(config)
    
    assert breaker.config.failure_threshold == 2
    assert breaker.config.reset_timeout == 30
    assert breaker.config.half_open_timeout == 15
    assert breaker.config.success_threshold == 3

if __name__ == "__main__":
    pytest.main([__file__]) 