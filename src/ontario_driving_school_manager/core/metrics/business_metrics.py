
"""
Business Metrics

This module provides business metrics and KPIs for the Ontario Driving School Manager.
It tracks key performance indicators for the driving school business.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from collections import defaultdict

from . import Metric, MetricType, MetricLabel, MetricsCollector

logger = logging.getLogger(__name__)

class Counter(Metric[int]):
    """Counter metric."""
    
    def __init__(self):
        """Initialize counter."""
        self._values: Dict[str, int] = defaultdict(int)
    
    def record(self, value: int = 1, labels: Optional[Dict[str, str]] = None) -> None:
        """Record a value.
        
        Args:
            value: Value to record
            labels: Metric labels
        """
        key = self._get_key(labels)
        self._values[key] += value
    
    def get(self, labels: Optional[Dict[str, str]] = None) -> int:
        """Get counter value.
        
        Args:
            labels: Metric labels
            
        Returns:
            Counter value
        """
        key = self._get_key(labels)
        return self._values[key]
    
    def reset(self, labels: Optional[Dict[str, str]] = None) -> None:
        """Reset counter value.
        
        Args:
            labels: Metric labels
        """
        key = self._get_key(labels)
        self._values[key] = 0
    
    def _get_key(self, labels: Optional[Dict[str, str]]) -> str:
        """Get key for labels.
        
        Args:
            labels: Metric labels
            
        Returns:
            Key string
        """
        if not labels:
            return "default"
        return ",".join(f"{k}={v}" for k, v in sorted(labels.items()))

class Gauge(Metric[float]):
    """Gauge metric."""
    
    def __init__(self):
        """Initialize gauge."""
        self._values: Dict[str, float] = defaultdict(float)
    
    def record(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Record a value.
        
        Args:
            value: Value to record
            labels: Metric labels
        """
        key = self._get_key(labels)
        self._values[key] = value
    
    def get(self, labels: Optional[Dict[str, str]] = None) -> float:
        """Get gauge value.
        
        Args:
            labels: Metric labels
            
        Returns:
            Gauge value
        """
        key = self._get_key(labels)
        return self._values[key]
    
    def reset(self, labels: Optional[Dict[str, str]] = None) -> None:
        """Reset gauge value.
        
        Args:
            labels: Metric labels
        """
        key = self._get_key(labels)
        self._values[key] = 0.0
    
    def _get_key(self, labels: Optional[Dict[str, str]]) -> str:
        """Get key for labels.
        
        Args:
            labels: Metric labels
            
        Returns:
            Key string
        """
        if not labels:
            return "default"
        return ",".join(f"{k}={v}" for k, v in sorted(labels.items()))

class BusinessMetrics:
    """Business metrics collector."""
    
    def __init__(self):
        """Initialize business metrics."""
        self.collector = MetricsCollector()
        
        # Student metrics
        self.collector.register("total_students", Counter())
        self.collector.register("active_students", Gauge())
        self.collector.register("completed_lessons", Counter())
        self.collector.register("failed_tests", Counter())
        
        # Instructor metrics
        self.collector.register("total_instructors", Counter())
        self.collector.register("active_instructors", Gauge())
        self.collector.register("instructor_hours", Counter())
        
        # Financial metrics
        self.collector.register("total_revenue", Counter())
        self.collector.register("average_lesson_price", Gauge())
        self.collector.register("payment_success_rate", Gauge())
        
        # Performance metrics
        self.collector.register("lesson_completion_rate", Gauge())
        self.collector.register("test_pass_rate", Gauge())
        self.collector.register("student_satisfaction", Gauge())
    
    def record_student_activity(
        self,
        student_id: str,
        activity_type: str,
        status: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Record student activity.
        
        Args:
            student_id: Student ID
            activity_type: Type of activity
            status: Activity status
            metadata: Additional metadata
        """
        labels = {
            MetricLabel.SERVICE.value: "student",
            MetricLabel.OPERATION.value: activity_type,
            MetricLabel.STATUS.value: status
        }
        
        if activity_type == "lesson":
            self.collector.get_metric("completed_lessons").record(1, labels)
        elif activity_type == "test":
            if status == "failed":
                self.collector.get_metric("failed_tests").record(1, labels)
    
    def record_instructor_activity(
        self,
        instructor_id: str,
        activity_type: str,
        hours: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Record instructor activity.
        
        Args:
            instructor_id: Instructor ID
            activity_type: Type of activity
            hours: Hours worked
            metadata: Additional metadata
        """
        labels = {
            MetricLabel.SERVICE.value: "instructor",
            MetricLabel.OPERATION.value: activity_type
        }
        
        self.collector.get_metric("instructor_hours").record(int(hours), labels)
    
    def record_payment(
        self,
        amount: float,
        method: str,
        status: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Record payment.
        
        Args:
            amount: Payment amount
            method: Payment method
            status: Payment status
            metadata: Additional metadata
        """
        labels = {
            MetricLabel.SERVICE.value: "payment",
            MetricLabel.OPERATION.value: method,
            MetricLabel.STATUS.value: status
        }
        
        self.collector.get_metric("total_revenue").record(int(amount), labels)
        
        # Update average lesson price
        if status == "success":
            avg_price = self.collector.get_metric("average_lesson_price")
            current_avg = avg_price.get()
            count = self.collector.get_metric("completed_lessons").get()
            new_avg = ((current_avg * count) + amount) / (count + 1)
            avg_price.record(new_avg)
    
    def update_performance_metrics(self) -> None:
        """Update performance metrics."""
        # Calculate lesson completion rate
        completed = self.collector.get_metric("completed_lessons").get()
        total = self.collector.get_metric("total_students").get()
        if total > 0:
            completion_rate = completed / total
            self.collector.get_metric("lesson_completion_rate").record(completion_rate)
        
        # Calculate test pass rate
        failed = self.collector.get_metric("failed_tests").get()
        if completed > 0:
            pass_rate = 1 - (failed / completed)
            self.collector.get_metric("test_pass_rate").record(pass_rate)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics.
        
        Returns:
            Dictionary of metric values
        """
        return self.collector.collect()
    
    def reset_metrics(self) -> None:
        """Reset all metrics."""
        self.collector.reset()