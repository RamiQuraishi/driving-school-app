"""
Health Checks

This module implements health checks for the Ontario Driving School Manager.
It monitors system health and component status.

Author: Rami Drive School
Date: 2024
"""

import json
import psutil
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

@dataclass
class HealthStatus:
    """Health status data."""
    component: str
    status: str
    timestamp: datetime
    details: Dict[str, Any]

class HealthChecker:
    """Health checker implementation."""
    
    def __init__(
        self,
        storage_path: str,
        check_interval: int = 300  # 5 minutes
    ):
        """Initialize health checker.
        
        Args:
            storage_path: Path to store health data
            check_interval: Check interval in seconds
        """
        self.storage_path = storage_path
        self.check_interval = check_interval
        self.statuses: List[HealthStatus] = []
    
    def check_system_health(self) -> Dict[str, HealthStatus]:
        """Check system health.
        
        Returns:
            Dict[str, HealthStatus]: Health status by component
        """
        statuses = {}
        
        # Check CPU
        statuses['cpu'] = self._check_cpu()
        
        # Check memory
        statuses['memory'] = self._check_memory()
        
        # Check disk
        statuses['disk'] = self._check_disk()
        
        # Check network
        statuses['network'] = self._check_network()
        
        # Store statuses
        for status in statuses.values():
            self.statuses.append(status)
            self._save_status(status)
        
        return statuses
    
    def _check_cpu(self) -> HealthStatus:
        """Check CPU health.
        
        Returns:
            HealthStatus: CPU health status
        """
        # Get CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Determine status
        if cpu_percent < 70:
            status = 'healthy'
        elif cpu_percent < 90:
            status = 'warning'
        else:
            status = 'critical'
        
        return HealthStatus(
            component='cpu',
            status=status,
            timestamp=datetime.utcnow(),
            details={
                'usage_percent': cpu_percent,
                'cpu_count': cpu_count
            }
        )
    
    def _check_memory(self) -> HealthStatus:
        """Check memory health.
        
        Returns:
            HealthStatus: Memory health status
        """
        # Get memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_total = memory.total / (1024 * 1024 * 1024)  # GB
        memory_used = memory.used / (1024 * 1024 * 1024)  # GB
        
        # Determine status
        if memory_percent < 70:
            status = 'healthy'
        elif memory_percent < 90:
            status = 'warning'
        else:
            status = 'critical'
        
        return HealthStatus(
            component='memory',
            status=status,
            timestamp=datetime.utcnow(),
            details={
                'usage_percent': memory_percent,
                'total_gb': memory_total,
                'used_gb': memory_used
            }
        )
    
    def _check_disk(self) -> HealthStatus:
        """Check disk health.
        
        Returns:
            HealthStatus: Disk health status
        """
        # Get disk usage
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_total = disk.total / (1024 * 1024 * 1024)  # GB
        disk_used = disk.used / (1024 * 1024 * 1024)  # GB
        
        # Determine status
        if disk_percent < 70:
            status = 'healthy'
        elif disk_percent < 90:
            status = 'warning'
        else:
            status = 'critical'
        
        return HealthStatus(
            component='disk',
            status=status,
            timestamp=datetime.utcnow(),
            details={
                'usage_percent': disk_percent,
                'total_gb': disk_total,
                'used_gb': disk_used
            }
        )
    
    def _check_network(self) -> HealthStatus:
        """Check network health.
        
        Returns:
            HealthStatus: Network health status
        """
        # Get network stats
        net_io = psutil.net_io_counters()
        bytes_sent = net_io.bytes_sent / (1024 * 1024)  # MB
        bytes_recv = net_io.bytes_recv / (1024 * 1024)  # MB
        
        # Determine status
        status = 'healthy'  # Network is always healthy if we can check it
        
        return HealthStatus(
            component='network',
            status=status,
            timestamp=datetime.utcnow(),
            details={
                'bytes_sent_mb': bytes_sent,
                'bytes_recv_mb': bytes_recv
            }
        )
    
    def _save_status(self, status: HealthStatus) -> None:
        """Save health status.
        
        Args:
            status: Health status
        """
        # Convert status to dict
        status_dict = {
            'component': status.component,
            'status': status.status,
            'timestamp': status.timestamp.isoformat(),
            'details': status.details
        }
        
        # Save to file
        with open(self.storage_path, 'a') as f:
            f.write(json.dumps(status_dict) + '\n')
    
    def get_statuses(
        self,
        component: Optional[str] = None,
        status: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[HealthStatus]:
        """Get health statuses.
        
        Args:
            component: Filter by component
            status: Filter by status
            start_time: Filter by start time
            end_time: Filter by end time
            
        Returns:
            List[HealthStatus]: Filtered statuses
        """
        statuses = self.statuses
        
        if component:
            statuses = [s for s in statuses if s.component == component]
            
        if status:
            statuses = [s for s in statuses if s.status == status]
            
        if start_time:
            statuses = [s for s in statuses if s.timestamp >= start_time]
            
        if end_time:
            statuses = [s for s in statuses if s.timestamp <= end_time]
            
        return statuses
    
    def get_health_summary(self) -> Dict[str, Dict[str, int]]:
        """Get health summary.
        
        Returns:
            Dict[str, Dict[str, int]]: Health counts by component and status
        """
        summary = {}
        
        for status in self.statuses:
            if status.component not in summary:
                summary[status.component] = {
                    'healthy': 0,
                    'warning': 0,
                    'critical': 0
                }
            
            summary[status.component][status.status] += 1
            
        return summary
    
    def clear_statuses(self) -> None:
        """Clear all statuses."""
        self.statuses.clear() 