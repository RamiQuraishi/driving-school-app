"""
Distributed Tracing

This module provides distributed tracing for the Ontario Driving School Manager.
It helps track and debug synchronization issues across services.

Author: Rami Drive School
Date: 2024
"""

import logging
import uuid
import time
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
from contextlib import contextmanager
from dataclasses import dataclass, field

from . import Metric, MetricType, MetricLabel, MetricsCollector

logger = logging.getLogger(__name__)

@dataclass
class Span:
    """Tracing span."""
    
    trace_id: str
    span_id: str
    parent_id: Optional[str]
    name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)
    status: str = "OK"
    error: Optional[str] = None

class Tracer:
    """Distributed tracer."""
    
    def __init__(self):
        """Initialize tracer."""
        self.spans: Dict[str, Span] = {}
        self.active_spans: Dict[str, str] = {}  # thread_id -> span_id
    
    def start_span(
        self,
        name: str,
        parent_id: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None
    ) -> str:
        """Start a new span.
        
        Args:
            name: Span name
            parent_id: Parent span ID
            attributes: Span attributes
            
        Returns:
            Span ID
        """
        trace_id = str(uuid.uuid4())
        span_id = str(uuid.uuid4())
        
        span = Span(
            trace_id=trace_id,
            span_id=span_id,
            parent_id=parent_id,
            name=name,
            start_time=datetime.now(),
            attributes=attributes or {}
        )
        
        self.spans[span_id] = span
        self.active_spans[str(uuid.getnode())] = span_id
        
        return span_id
    
    def end_span(
        self,
        span_id: str,
        status: str = "OK",
        error: Optional[str] = None
    ) -> None:
        """End a span.
        
        Args:
            span_id: Span ID
            status: Span status
            error: Error message
        """
        if span_id not in self.spans:
            logger.warning(f"Span {span_id} not found")
            return
        
        span = self.spans[span_id]
        span.end_time = datetime.now()
        span.status = status
        span.error = error
        
        # Remove from active spans
        thread_id = str(uuid.getnode())
        if thread_id in self.active_spans:
            del self.active_spans[thread_id]
    
    def add_event(
        self,
        span_id: str,
        name: str,
        attributes: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add event to span.
        
        Args:
            span_id: Span ID
            name: Event name
            attributes: Event attributes
        """
        if span_id not in self.spans:
            logger.warning(f"Span {span_id} not found")
            return
        
        event = {
            "name": name,
            "time": datetime.now(),
            "attributes": attributes or {}
        }
        
        self.spans[span_id].events.append(event)
    
    def get_active_span(self) -> Optional[Span]:
        """Get active span for current thread.
        
        Returns:
            Active span or None
        """
        thread_id = str(uuid.getnode())
        span_id = self.active_spans.get(thread_id)
        return self.spans.get(span_id) if span_id else None
    
    def get_trace(self, trace_id: str) -> List[Span]:
        """Get all spans for a trace.
        
        Args:
            trace_id: Trace ID
            
        Returns:
            List of spans
        """
        return [
            span for span in self.spans.values()
            if span.trace_id == trace_id
        ]
    
    def clear(self) -> None:
        """Clear all spans."""
        self.spans.clear()
        self.active_spans.clear()

class DistributedTracing:
    """Distributed tracing manager."""
    
    def __init__(self):
        """Initialize distributed tracing."""
        self.tracer = Tracer()
        self.collector = MetricsCollector()
        
        # Register metrics
        self.collector.register("span_duration", Metric[float])
        self.collector.register("span_count", Metric[int])
        self.collector.register("error_count", Metric[int])
    
    @contextmanager
    def trace(
        self,
        name: str,
        parent_id: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None
    ):
        """Trace a block of code.
        
        Args:
            name: Span name
            parent_id: Parent span ID
            attributes: Span attributes
            
        Yields:
            Span ID
        """
        span_id = self.tracer.start_span(name, parent_id, attributes)
        start_time = time.time()
        
        try:
            yield span_id
            self.tracer.end_span(span_id)
        except Exception as e:
            self.tracer.end_span(span_id, status="ERROR", error=str(e))
            raise
        finally:
            # Record metrics
            duration = time.time() - start_time
            self.collector.get_metric("span_duration").record(duration)
            self.collector.get_metric("span_count").record(1)
            
            if self.tracer.spans[span_id].status == "ERROR":
                self.collector.get_metric("error_count").record(1)
    
    def record_sync_event(
        self,
        event_type: str,
        status: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Record synchronization event.
        
        Args:
            event_type: Event type
            status: Event status
            metadata: Event metadata
        """
        with self.trace(
            f"sync_{event_type}",
            attributes={
                "type": event_type,
                "status": status,
                **(metadata or {})
            }
        ) as span_id:
            self.tracer.add_event(
                span_id,
                f"{event_type}_{status}",
                metadata
            )
    
    def get_trace_summary(self, trace_id: str) -> Dict[str, Any]:
        """Get trace summary.
        
        Args:
            trace_id: Trace ID
            
        Returns:
            Trace summary
        """
        spans = self.tracer.get_trace(trace_id)
        
        return {
            "trace_id": trace_id,
            "span_count": len(spans),
            "duration": sum(
                (span.end_time - span.start_time).total_seconds()
                for span in spans
                if span.end_time
            ),
            "error_count": sum(
                1 for span in spans
                if span.status == "ERROR"
            ),
            "spans": [
                {
                    "id": span.span_id,
                    "name": span.name,
                    "parent_id": span.parent_id,
                    "start_time": span.start_time.isoformat(),
                    "end_time": span.end_time.isoformat() if span.end_time else None,
                    "status": span.status,
                    "error": span.error,
                    "attributes": span.attributes,
                    "events": span.events
                }
                for span in spans
            ]
        }
    
    def clear_traces(self) -> None:
        """Clear all traces."""
        self.tracer.clear()
        self.collector.reset()