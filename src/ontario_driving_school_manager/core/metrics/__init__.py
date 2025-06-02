"""
Metrics Infrastructure

This module provides metrics infrastructure for the Ontario Driving School Manager.
It includes business KPIs, distributed tracing, and custom metrics collection.

Author: Rami Drive School
Date: 2024
"""

from typing import Dict, Any, Optional, Protocol, TypeVar, Generic, List
from datetime import datetime, timedelta
from enum import Enum, auto

class MetricType(Enum):
    """Types of metrics."""
    COUNTER = auto()
    GAUGE = auto()
    HISTOGRAM = auto()
    SUMMARY = auto()

class MetricLabel(Enum):
    """Standard metric labels."""
    SERVICE = "service"
    OPERATION = "operation"
    STATUS = "status"
    ERROR_TYPE = "error_type"
    VERSION = "version"
    ENVIRONMENT = "environment"

class Metric(Generic[T], Protocol):
    """Metric interface protocol."""
    
    def record(self, value: T, labels: Optional[Dict[str, str]] = None) -> None:
        """Record a metric value.
        
        Args:
            value: Metric value
            labels: Metric labels
        """
        ...
    
    def get(self, labels: Optional[Dict[str, str]] = None) -> T:
        """Get metric value.
        
        Args:
            labels: Metric labels
            
        Returns:
            Metric value
        """
        ...
    
    def reset(self, labels: Optional[Dict[str, str]] = None) -> None:
        """Reset metric value.
        
        Args:
            labels: Metric labels
        """
        ...

class MetricsCollector:
    """Metrics collector."""
    
    def __init__(self):
        """Initialize metrics collector."""
        self.metrics: Dict[str, Metric] = {}
        self.start_time = datetime.now()
    
    def register(self, name: str, metric: Metric) -> None:
        """Register a metric.
        
        Args:
            name: Metric name
            metric: Metric instance
        """
        self.metrics[name] = metric
    
    def unregister(self, name: str) -> None:
        """Unregister a metric.
        
        Args:
            name: Metric name
        """
        if name in self.metrics:
            del self.metrics[name]
    
    def get_metric(self, name: str) -> Optional[Metric]:
        """Get a metric by name.
        
        Args:
            name: Metric name
            
        Returns:
            Metric instance or None if not found
        """
        return self.metrics.get(name)
    
    def collect(self) -> Dict[str, Any]:
        """Collect all metrics.
        
        Returns:
            Dictionary of metric values
        """
        return {
            name: metric.get()
            for name, metric in self.metrics.items()
        }
    
    def reset(self) -> None:
        """Reset all metrics."""
        for metric in self.metrics.values():
            metric.reset()
    
    @property
    def uptime(self) -> timedelta:
        """Get collector uptime.
        
        Returns:
            Uptime as timedelta
        """
        return datetime.now() - self.start_time

# Export metrics implementations
from .business_metrics import BusinessMetrics
from .distributed_tracing import DistributedTracing

__all__ = [
    'MetricType',
    'MetricLabel',
    'Metric',
    'MetricsCollector',
    'BusinessMetrics',
    'DistributedTracing'
]