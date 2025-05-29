"""
Business Metrics

This module implements business metrics tracking for the Ontario Driving School Manager.
It tracks key performance indicators (KPIs) and business metrics.

Author: Rami Drive School
Date: 2024
"""

import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

@dataclass
class BusinessMetric:
    """Business metric data."""
    metric_type: str
    value: float
    timestamp: datetime
    period: str
    metadata: Dict[str, Any]

class BusinessMetrics:
    """Business metrics implementation."""
    
    def __init__(
        self,
        storage_path: str,
        max_metrics: int = 10000
    ):
        """Initialize business metrics.
        
        Args:
            storage_path: Path to store metrics data
            max_metrics: Maximum number of metrics to store
        """
        self.storage_path = storage_path
        self.max_metrics = max_metrics
        self.metrics: List[BusinessMetric] = []
    
    def track_metric(
        self,
        metric_type: str,
        value: float,
        period: str = 'daily',
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Track business metric.
        
        Args:
            metric_type: Type of metric
            value: Metric value
            period: Time period
            metadata: Additional metadata
        """
        # Create metric
        metric = BusinessMetric(
            metric_type=metric_type,
            value=value,
            timestamp=datetime.utcnow(),
            period=period,
            metadata=metadata or {}
        )
        
        # Store metric
        self.metrics.append(metric)
        self._save_metric(metric)
        
        # Trim metrics if needed
        if len(self.metrics) > self.max_metrics:
            self.metrics = self.metrics[-self.max_metrics:]
    
    def _save_metric(self, metric: BusinessMetric) -> None:
        """Save business metric.
        
        Args:
            metric: Business metric
        """
        # Convert metric to dict
        metric_dict = {
            'metric_type': metric.metric_type,
            'value': metric.value,
            'timestamp': metric.timestamp.isoformat(),
            'period': metric.period,
            'metadata': metric.metadata
        }
        
        # Save to file
        with open(self.storage_path, 'a') as f:
            f.write(json.dumps(metric_dict) + '\n')
    
    def get_metrics(
        self,
        metric_type: Optional[str] = None,
        period: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[BusinessMetric]:
        """Get business metrics.
        
        Args:
            metric_type: Filter by metric type
            period: Filter by period
            start_time: Filter by start time
            end_time: Filter by end time
            
        Returns:
            List[BusinessMetric]: Filtered metrics
        """
        metrics = self.metrics
        
        if metric_type:
            metrics = [m for m in metrics if m.metric_type == metric_type]
            
        if period:
            metrics = [m for m in metrics if m.period == period]
            
        if start_time:
            metrics = [m for m in metrics if m.timestamp >= start_time]
            
        if end_time:
            metrics = [m for m in metrics if m.timestamp <= end_time]
            
        return metrics
    
    def get_metric_summary(
        self,
        metric_type: str,
        period: str = 'daily',
        days: int = 30
    ) -> Dict[str, float]:
        """Get metric summary.
        
        Args:
            metric_type: Type of metric
            period: Time period
            days: Number of days
            
        Returns:
            Dict[str, float]: Metric summary
        """
        # Get metrics
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)
        
        metrics = self.get_metrics(
            metric_type=metric_type,
            period=period,
            start_time=start_time,
            end_time=end_time
        )
        
        if not metrics:
            return {
                'min': 0.0,
                'max': 0.0,
                'avg': 0.0,
                'total': 0.0
            }
        
        values = [m.value for m in metrics]
        
        return {
            'min': min(values),
            'max': max(values),
            'avg': sum(values) / len(values),
            'total': sum(values)
        }
    
    def get_trend(
        self,
        metric_type: str,
        period: str = 'daily',
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """Get metric trend.
        
        Args:
            metric_type: Type of metric
            period: Time period
            days: Number of days
            
        Returns:
            List[Dict[str, Any]]: Metric trend
        """
        # Get metrics
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)
        
        metrics = self.get_metrics(
            metric_type=metric_type,
            period=period,
            start_time=start_time,
            end_time=end_time
        )
        
        # Group by date
        trend = {}
        
        for metric in metrics:
            date = metric.timestamp.date().isoformat()
            
            if date not in trend:
                trend[date] = []
                
            trend[date].append(metric.value)
        
        # Calculate daily averages
        return [
            {
                'date': date,
                'value': sum(values) / len(values)
            }
            for date, values in sorted(trend.items())
        ]
    
    def clear_metrics(self) -> None:
        """Clear all metrics."""
        self.metrics.clear() 