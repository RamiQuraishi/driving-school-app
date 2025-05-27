"""
Performance tracking service.
"""
import logging
import time
from typing import Dict, Any, Optional, Callable
from functools import wraps
from ..config.feature_flags import feature_flags

logger = logging.getLogger(__name__)

class PerformanceTracker:
    """Performance tracking service."""
    
    def __init__(self):
        """Initialize the performance tracker."""
        self.config = feature_flags.MONITORING_CONFIG
        self._metrics: Dict[str, list] = {}
    
    def track(self, name: str) -> Callable:
        """
        Decorator to track function performance.
        
        Args:
            name: Metric name
            
        Returns:
            Decorated function
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                if not self.config['performance_tracking']:
                    return await func(*args, **kwargs)
                    
                start_time = time.perf_counter()
                try:
                    result = await func(*args, **kwargs)
                    duration = time.perf_counter() - start_time
                    self._record_metric(name, duration)
                    return result
                except Exception as e:
                    duration = time.perf_counter() - start_time
                    self._record_metric(f"{name}_error", duration)
                    raise
            return wrapper
        return decorator
    
    def _record_metric(self, name: str, duration: float) -> None:
        """
        Record a performance metric.
        
        Args:
            name: Metric name
            duration: Duration in seconds
        """
        if name not in self._metrics:
            self._metrics[name] = []
        self._metrics[name].append(duration)
        
        # Log if duration exceeds threshold
        if duration > 1.0:  # 1 second threshold
            logger.warning(f"Slow operation detected: {name} took {duration:.2f}s")
    
    def get_metrics(self) -> Dict[str, Dict[str, float]]:
        """
        Get performance metrics.
        
        Returns:
            Dictionary of metric statistics
        """
        stats = {}
        for name, durations in self._metrics.items():
            if durations:
                stats[name] = {
                    'count': len(durations),
                    'min': min(durations),
                    'max': max(durations),
                    'avg': sum(durations) / len(durations)
                }
        return stats 