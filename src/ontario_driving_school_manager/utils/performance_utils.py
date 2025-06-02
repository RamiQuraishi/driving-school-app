"""
Performance Utilities Module

This module provides performance monitoring functionality.
It includes timing, profiling, and resource usage tracking.

Author: Rami Drive School
Date: 2024
"""

import time
import psutil
import logging
from typing import Dict, Any, Optional, Union, Callable
from functools import wraps
from datetime import datetime
import threading
import queue
import json
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Performance monitor."""
    
    def __init__(
        self,
        log_dir: str = "logs",
        log_interval: int = 60,  # seconds
        metrics: Optional[Dict[str, Callable]] = None
    ):
        """Initialize performance monitor.
        
        Args:
            log_dir: Log directory
            log_interval: Log interval in seconds
            metrics: Custom metrics
        """
        self.log_dir = log_dir
        self.log_interval = log_interval
        self.metrics = metrics or {}
        self.running = False
        self.thread = None
        self.queue = queue.Queue()
        
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
    
    def start(self) -> None:
        """Start performance monitoring."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True
        )
        self.thread.start()
    
    def stop(self) -> None:
        """Stop performance monitoring."""
        if not self.running:
            return
        
        self.running = False
        self.queue.put(None)
        self.thread.join()
    
    def _monitor_loop(self) -> None:
        """Monitor loop."""
        while self.running:
            try:
                # Collect metrics
                metrics = self._collect_metrics()
                
                # Log metrics
                self._log_metrics(metrics)
                
                # Wait for next interval
                time.sleep(self.log_interval)
            except Exception as e:
                logger.error(f"Error in monitor loop: {str(e)}")
    
    def _collect_metrics(self) -> Dict[str, Any]:
        """Collect metrics.
        
        Returns:
            Metrics dictionary
        """
        metrics = {
            "timestamp": datetime.utcnow().isoformat(),
            "cpu": {
                "percent": psutil.cpu_percent(interval=1),
                "count": psutil.cpu_count(),
                "frequency": psutil.cpu_freq().current
            },
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent": psutil.virtual_memory().percent
            },
            "disk": {
                "total": psutil.disk_usage("/").total,
                "used": psutil.disk_usage("/").used,
                "free": psutil.disk_usage("/").free,
                "percent": psutil.disk_usage("/").percent
            },
            "network": {
                "bytes_sent": psutil.net_io_counters().bytes_sent,
                "bytes_recv": psutil.net_io_counters().bytes_recv,
                "packets_sent": psutil.net_io_counters().packets_sent,
                "packets_recv": psutil.net_io_counters().packets_recv
            }
        }
        
        # Add custom metrics
        for name, func in self.metrics.items():
            try:
                metrics[name] = func()
            except Exception as e:
                logger.error(f"Error collecting metric {name}: {str(e)}")
        
        return metrics
    
    def _log_metrics(self, metrics: Dict[str, Any]) -> None:
        """Log metrics.
        
        Args:
            metrics: Metrics dictionary
        """
        try:
            # Create log file path
            log_file = os.path.join(
                self.log_dir,
                f"performance_{datetime.now().strftime('%Y%m%d')}.log"
            )
            
            # Write metrics to log file
            with open(log_file, "a") as f:
                f.write(json.dumps(metrics) + "\n")
        except Exception as e:
            logger.error(f"Error logging metrics: {str(e)}")
    
    def add_metric(
        self,
        name: str,
        func: Callable
    ) -> None:
        """Add custom metric.
        
        Args:
            name: Metric name
            func: Metric function
        """
        self.metrics[name] = func
    
    def remove_metric(self, name: str) -> None:
        """Remove custom metric.
        
        Args:
            name: Metric name
        """
        self.metrics.pop(name, None)

def timing_decorator(
    logger: Optional[logging.Logger] = None
) -> Callable:
    """Timing decorator.
    
    Args:
        logger: Logger instance
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            duration = end_time - start_time
            
            if logger:
                logger.info(
                    f"Function {func.__name__} took {duration:.2f} seconds"
                )
            
            return result
        return wrapper
    return decorator

class ResourceMonitor:
    """Resource monitor."""
    
    def __init__(self):
        """Initialize resource monitor."""
        self.start_time = time.time()
        self.start_cpu = psutil.cpu_percent()
        self.start_memory = psutil.virtual_memory().percent
        self.start_disk = psutil.disk_usage("/").percent
    
    def get_usage(self) -> Dict[str, float]:
        """Get resource usage.
        
        Returns:
            Resource usage dictionary
        """
        return {
            "cpu": psutil.cpu_percent() - self.start_cpu,
            "memory": psutil.virtual_memory().percent - self.start_memory,
            "disk": psutil.disk_usage("/").percent - self.start_disk,
            "duration": time.time() - self.start_time
        }

class Profiler:
    """Profiler."""
    
    def __init__(self):
        """Initialize profiler."""
        self.start_time = None
        self.end_time = None
        self.start_cpu = None
        self.end_cpu = None
        self.start_memory = None
        self.end_memory = None
    
    def start(self) -> None:
        """Start profiling."""
        self.start_time = time.time()
        self.start_cpu = psutil.cpu_percent()
        self.start_memory = psutil.virtual_memory().percent
    
    def stop(self) -> Dict[str, float]:
        """Stop profiling.
        
        Returns:
            Profiling results
        """
        self.end_time = time.time()
        self.end_cpu = psutil.cpu_percent()
        self.end_memory = psutil.virtual_memory().percent
        
        return {
            "duration": self.end_time - self.start_time,
            "cpu_usage": self.end_cpu - self.start_cpu,
            "memory_usage": self.end_memory - self.start_memory
        }
    
    def __enter__(self) -> "Profiler":
        """Enter context."""
        self.start()
        return self
    
    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[Exception],
        exc_tb: Optional[Any]
    ) -> None:
        """Exit context."""
        self.stop()

class MemoryTracker:
    """Memory tracker."""
    
    def __init__(self):
        """Initialize memory tracker."""
        self.start_memory = None
        self.end_memory = None
    
    def start(self) -> None:
        """Start tracking."""
        self.start_memory = psutil.Process().memory_info().rss
    
    def stop(self) -> int:
        """Stop tracking.
        
        Returns:
            Memory usage in bytes
        """
        self.end_memory = psutil.Process().memory_info().rss
        return self.end_memory - self.start_memory
    
    def __enter__(self) -> "MemoryTracker":
        """Enter context."""
        self.start()
        return self
    
    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[Exception],
        exc_tb: Optional[Any]
    ) -> None:
        """Exit context."""
        self.stop()

class CPUTracker:
    """CPU tracker."""
    
    def __init__(self):
        """Initialize CPU tracker."""
        self.start_cpu = None
        self.end_cpu = None
    
    def start(self) -> None:
        """Start tracking."""
        self.start_cpu = psutil.cpu_percent()
    
    def stop(self) -> float:
        """Stop tracking.
        
        Returns:
            CPU usage percentage
        """
        self.end_cpu = psutil.cpu_percent()
        return self.end_cpu - self.start_cpu
    
    def __enter__(self) -> "CPUTracker":
        """Enter context."""
        self.start()
        return self
    
    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[Exception],
        exc_tb: Optional[Any]
    ) -> None:
        """Exit context."""
        self.stop()

class DiskTracker:
    """Disk tracker."""
    
    def __init__(self):
        """Initialize disk tracker."""
        self.start_disk = None
        self.end_disk = None
    
    def start(self) -> None:
        """Start tracking."""
        self.start_disk = psutil.disk_usage("/").percent
    
    def stop(self) -> float:
        """Stop tracking.
        
        Returns:
            Disk usage percentage
        """
        self.end_disk = psutil.disk_usage("/").percent
        return self.end_disk - self.start_disk
    
    def __enter__(self) -> "DiskTracker":
        """Enter context."""
        self.start()
        return self
    
    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[Exception],
        exc_tb: Optional[Any]
    ) -> None:
        """Exit context."""
        self.stop()

class NetworkTracker:
    """Network tracker."""
    
    def __init__(self):
        """Initialize network tracker."""
        self.start_io = None
        self.end_io = None
    
    def start(self) -> None:
        """Start tracking."""
        self.start_io = psutil.net_io_counters()
    
    def stop(self) -> Dict[str, int]:
        """Stop tracking.
        
        Returns:
            Network usage dictionary
        """
        self.end_io = psutil.net_io_counters()
        
        return {
            "bytes_sent": self.end_io.bytes_sent - self.start_io.bytes_sent,
            "bytes_recv": self.end_io.bytes_recv - self.start_io.bytes_recv,
            "packets_sent": self.end_io.packets_sent - self.start_io.packets_sent,
            "packets_recv": self.end_io.packets_recv - self.start_io.packets_recv
        }
    
    def __enter__(self) -> "NetworkTracker":
        """Enter context."""
        self.start()
        return self
    
    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[Exception],
        exc_tb: Optional[Any]
    ) -> None:
        """Exit context."""
        self.stop() 