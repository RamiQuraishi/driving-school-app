"""
Performance Tracker

This module implements performance tracking for the Ontario Driving School Manager.
It tracks execution times and resource usage of operations.

Author: Rami Drive School
Date: 2024
"""

import time
import psutil
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass
import json

@dataclass
class PerformanceMetric:
    """Performance metric data."""
    operation: str
    start_time: datetime
    end_time: datetime
    duration: float
    memory_usage: float
    cpu_usage: float
    metadata: Dict[str, Any]

class PerformanceTracker:
    """Performance tracker implementation."""
    
    def __init__(self, storage_path: str):
        """Initialize performance tracker.
        
        Args:
            storage_path: Path to store performance data
        """
        self.storage_path = storage_path
        self.metrics: List[PerformanceMetric] = []
        self.process = psutil.Process()
    
    def track(
        self,
        operation: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Callable:
        """Track performance of operation.
        
        Args:
            operation: Operation name
            metadata: Additional metadata
            
        Returns:
            Callable: Decorator function
        """
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs) -> Any:
                start_time = datetime.utcnow()
                start_memory = self.process.memory_info().rss
                start_cpu = self.process.cpu_percent()
                
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    end_time = datetime.utcnow()
                    end_memory = self.process.memory_info().rss
                    end_cpu = self.process.cpu_percent()
                    
                    # Calculate metrics
                    duration = (end_time - start_time).total_seconds()
                    memory_usage = (end_memory - start_memory) / 1024 / 1024  # MB
                    cpu_usage = end_cpu - start_cpu
                    
                    # Create metric
                    metric = PerformanceMetric(
                        operation=operation,
                        start_time=start_time,
                        end_time=end_time,
                        duration=duration,
                        memory_usage=memory_usage,
                        cpu_usage=cpu_usage,
                        metadata=metadata or {}
                    )
                    
                    # Store metric
                    self.metrics.append(metric)
                    self._save_metric(metric)
            
            return wrapper
        return decorator
    
    def _save_metric(self, metric: PerformanceMetric) -> None:
        """Save performance metric.
        
        Args:
            metric: Performance metric
        """
        # Convert metric to dict
        metric_dict = {
            'operation': metric.operation,
            'start_time': metric.start_time.isoformat(),
            'end_time': metric.end_time.isoformat(),
            'duration': metric.duration,
            'memory_usage': metric.memory_usage,
            'cpu_usage': metric.cpu_usage,
            'metadata': metric.metadata
        }
        
        # Save to file
        with open(self.storage_path, 'a') as f:
            f.write(json.dumps(metric_dict) + '\n')
    
    def get_metrics(
        self,
        operation: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[PerformanceMetric]:
        """Get performance metrics.
        
        Args:
            operation: Filter by operation
            start_time: Filter by start time
            end_time: Filter by end time
            
        Returns:
            List[PerformanceMetric]: Filtered metrics
        """
        metrics = self.metrics
        
        if operation:
            metrics = [m for m in metrics if m.operation == operation]
            
        if start_time:
            metrics = [m for m in metrics if m.start_time >= start_time]
            
        if end_time:
            metrics = [m for m in metrics if m.end_time <= end_time]
            
        return metrics
    
    def get_average_metrics(
        self,
        operation: Optional[str] = None
    ) -> Dict[str, float]:
        """Get average performance metrics.
        
        Args:
            operation: Filter by operation
            
        Returns:
            Dict[str, float]: Average metrics
        """
        metrics = self.get_metrics(operation)
        
        if not metrics:
            return {
                'duration': 0.0,
                'memory_usage': 0.0,
                'cpu_usage': 0.0
            }
        
        return {
            'duration': sum(m.duration for m in metrics) / len(metrics),
            'memory_usage': sum(m.memory_usage for m in metrics) / len(metrics),
            'cpu_usage': sum(m.cpu_usage for m in metrics) / len(metrics)
        }
    
    def clear_metrics(self) -> None:
        """Clear all metrics."""
        self.metrics.clear() 