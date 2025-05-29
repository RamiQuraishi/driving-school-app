"""Event handling and management system."""

import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set

from .exceptions import EventError

logger = logging.getLogger(__name__)

class EventType(Enum):
    """Types of events in the system."""
    
    # Student events
    STUDENT_CREATED = "student.created"
    STUDENT_UPDATED = "student.updated"
    STUDENT_DELETED = "student.deleted"
    STUDENT_LICENSE_EXPIRING = "student.license.expiring"
    
    # Instructor events
    INSTRUCTOR_CREATED = "instructor.created"
    INSTRUCTOR_UPDATED = "instructor.updated"
    INSTRUCTOR_DELETED = "instructor.deleted"
    INSTRUCTOR_CERTIFICATION_EXPIRING = "instructor.certification.expiring"
    
    # Vehicle events
    VEHICLE_CREATED = "vehicle.created"
    VEHICLE_UPDATED = "vehicle.updated"
    VEHICLE_DELETED = "vehicle.deleted"
    VEHICLE_INSPECTION_DUE = "vehicle.inspection.due"
    
    # Lesson events
    LESSON_CREATED = "lesson.created"
    LESSON_UPDATED = "lesson.updated"
    LESSON_CANCELLED = "lesson.cancelled"
    LESSON_COMPLETED = "lesson.completed"
    
    # Payment events
    PAYMENT_CREATED = "payment.created"
    PAYMENT_UPDATED = "payment.updated"
    PAYMENT_REFUNDED = "payment.refunded"
    PAYMENT_OVERDUE = "payment.overdue"
    
    # MTO events
    MTO_EXPORT_CREATED = "mto.export.created"
    MTO_EXPORT_COMPLETED = "mto.export.completed"
    MTO_EXPORT_FAILED = "mto.export.failed"
    
    # System events
    SYSTEM_STARTUP = "system.startup"
    SYSTEM_SHUTDOWN = "system.shutdown"
    SYSTEM_ERROR = "system.error"

@dataclass
class Event:
    """Event data structure."""
    
    type: EventType
    data: Dict[str, Any]
    timestamp: datetime
    source: str
    correlation_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary.
        
        Returns:
            Dict[str, Any]: Event data
        """
        return {
            "type": self.type.value,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "correlation_id": self.correlation_id
        }

class EventHandler:
    """Base class for event handlers."""
    
    def __init__(self, event_type: EventType):
        """Initialize event handler.
        
        Args:
            event_type: Type of event to handle
        """
        self.event_type = event_type
    
    def handle(self, event: Event) -> None:
        """Handle an event.
        
        Args:
            event: Event to handle
        """
        raise NotImplementedError

class EventBus:
    """Event bus for managing event handlers and dispatching events."""
    
    def __init__(self):
        """Initialize event bus."""
        self._handlers: Dict[EventType, Set[EventHandler]] = {}
        self._middleware: List[Callable[[Event], Event]] = []
    
    def register_handler(self, handler: EventHandler) -> None:
        """Register an event handler.
        
        Args:
            handler: Handler to register
        """
        if handler.event_type not in self._handlers:
            self._handlers[handler.event_type] = set()
        
        self._handlers[handler.event_type].add(handler)
        logger.info(f"Registered handler for event: {handler.event_type.value}")
    
    def unregister_handler(self, handler: EventHandler) -> None:
        """Unregister an event handler.
        
        Args:
            handler: Handler to unregister
        """
        if handler.event_type in self._handlers:
            self._handlers[handler.event_type].discard(handler)
            logger.info(f"Unregistered handler for event: {handler.event_type.value}")
    
    def add_middleware(self, middleware: Callable[[Event], Event]) -> None:
        """Add middleware to the event bus.
        
        Args:
            middleware: Middleware function
        """
        self._middleware.append(middleware)
        logger.info("Added event middleware")
    
    def publish(self, event: Event) -> None:
        """Publish an event to all registered handlers.
        
        Args:
            event: Event to publish
        """
        # Apply middleware
        for middleware in self._middleware:
            try:
                event = middleware(event)
            except Exception as e:
                logger.error(f"Middleware error: {str(e)}")
                raise EventError(
                    f"Middleware error: {str(e)}",
                    event_type=event.type.value
                )
        
        # Get handlers for event type
        handlers = self._handlers.get(event.type, set())
        
        if not handlers:
            logger.warning(f"No handlers registered for event: {event.type.value}")
            return
        
        # Dispatch to handlers
        errors = []
        for handler in handlers:
            try:
                handler.handle(event)
            except Exception as e:
                errors.append(str(e))
                logger.error(f"Handler error: {str(e)}")
        
        if errors:
            raise EventError(
                f"Handler errors: {', '.join(errors)}",
                event_type=event.type.value
            )
    
    def clear_handlers(self) -> None:
        """Clear all registered handlers."""
        self._handlers.clear()
        logger.info("Cleared all event handlers")
    
    def get_handler_count(self, event_type: EventType) -> int:
        """Get number of handlers for an event type.
        
        Args:
            event_type: Event type to check
            
        Returns:
            int: Number of handlers
        """
        return len(self._handlers.get(event_type, set())) 