"""
Dead Letter Queue

This module implements a dead letter queue for handling failed operations
that need to be retried or processed later.

Author: Rami Drive School
Date: 2024
"""

import json
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type

class MessageStatus(Enum):
    """Message status in dead letter queue."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class DeadLetterMessage:
    """Message in dead letter queue."""
    id: str
    operation: str
    data: Dict[str, Any]
    error: Optional[str]
    status: MessageStatus
    created_at: datetime
    updated_at: datetime
    attempts: int = 0
    next_retry: Optional[datetime] = None

class DeadLetterQueue:
    """Dead letter queue implementation."""
    
    def __init__(
        self,
        max_retries: int = 3,
        retry_delay: float = 300.0,  # 5 minutes
        max_messages: int = 1000
    ):
        """Initialize dead letter queue.
        
        Args:
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            max_messages: Maximum number of messages to store
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.max_messages = max_messages
        self.messages: Dict[str, DeadLetterMessage] = {}
        self.handlers: Dict[str, Callable] = {}
    
    def add_message(
        self,
        operation: str,
        data: Dict[str, Any],
        error: Optional[str] = None
    ) -> DeadLetterMessage:
        """Add message to queue.
        
        Args:
            operation: Operation name
            data: Message data
            error: Error message
            
        Returns:
            DeadLetterMessage: Added message
        """
        # Remove oldest message if at capacity
        if len(self.messages) >= self.max_messages:
            oldest = min(
                self.messages.values(),
                key=lambda m: m.created_at
            )
            del self.messages[oldest.id]
        
        # Create message
        message = DeadLetterMessage(
            id=str(len(self.messages) + 1),
            operation=operation,
            data=data,
            error=error,
            status=MessageStatus.PENDING,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self.messages[message.id] = message
        return message
    
    def register_handler(
        self,
        operation: str,
        handler: Callable[[Dict[str, Any]], Any]
    ) -> None:
        """Register handler for operation.
        
        Args:
            operation: Operation name
            handler: Message handler
        """
        self.handlers[operation] = handler
    
    def process_messages(self) -> List[DeadLetterMessage]:
        """Process pending messages.
        
        Returns:
            List[DeadLetterMessage]: Processed messages
        """
        processed = []
        now = datetime.utcnow()
        
        for message in self.messages.values():
            if (
                message.status == MessageStatus.PENDING
                and message.next_retry is None
                or message.next_retry <= now
            ):
                try:
                    self._process_message(message)
                    processed.append(message)
                except Exception as e:
                    self._handle_processing_error(message, str(e))
        
        return processed
    
    def _process_message(self, message: DeadLetterMessage) -> None:
        """Process single message.
        
        Args:
            message: Message to process
        """
        if message.operation not in self.handlers:
            raise ValueError(f"No handler for operation: {message.operation}")
        
        message.status = MessageStatus.PROCESSING
        message.updated_at = datetime.utcnow()
        
        try:
            self.handlers[message.operation](message.data)
            message.status = MessageStatus.COMPLETED
        except Exception as e:
            raise e
        finally:
            message.updated_at = datetime.utcnow()
    
    def _handle_processing_error(
        self,
        message: DeadLetterMessage,
        error: str
    ) -> None:
        """Handle message processing error.
        
        Args:
            message: Failed message
            error: Error message
        """
        message.attempts += 1
        message.error = error
        
        if message.attempts >= self.max_retries:
            message.status = MessageStatus.FAILED
        else:
            message.status = MessageStatus.PENDING
            message.next_retry = datetime.utcnow().timestamp() + self.retry_delay
        
        message.updated_at = datetime.utcnow()
    
    def get_pending_messages(self) -> List[DeadLetterMessage]:
        """Get pending messages.
        
        Returns:
            List[DeadLetterMessage]: Pending messages
        """
        return [
            m for m in self.messages.values()
            if m.status == MessageStatus.PENDING
        ]
    
    def get_failed_messages(self) -> List[DeadLetterMessage]:
        """Get failed messages.
        
        Returns:
            List[DeadLetterMessage]: Failed messages
        """
        return [
            m for m in self.messages.values()
            if m.status == MessageStatus.FAILED
        ]
    
    def clear_completed_messages(self) -> None:
        """Clear completed messages."""
        self.messages = {
            id: msg for id, msg in self.messages.items()
            if msg.status != MessageStatus.COMPLETED
        } 