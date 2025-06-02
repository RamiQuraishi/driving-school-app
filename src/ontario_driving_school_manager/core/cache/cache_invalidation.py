"""
Cache Invalidation Strategy

This module provides cache invalidation strategies for the Ontario Driving School Manager.
It implements various invalidation patterns and pub/sub mechanisms.

Author: Rami Drive School
Date: 2024
"""

import json
import logging
from typing import Dict, Any, Optional, List, Set, Callable
from datetime import datetime, timedelta
import redis

logger = logging.getLogger(__name__)

class CacheInvalidator:
    """Cache invalidation manager."""
    
    def __init__(
        self,
        redis_client: redis.Redis,
        channel: str = "cache:invalidate"
    ):
        """Initialize cache invalidator.
        
        Args:
            redis_client: Redis client instance
            channel: Redis pub/sub channel for invalidation
        """
        self.redis = redis_client
        self.channel = channel
        self.pubsub = redis_client.pubsub()
        self.pubsub.subscribe(channel)
        self._handlers: Dict[str, List[Callable[[str], None]]] = {}
    
    def invalidate(self, pattern: str) -> bool:
        """Invalidate cache entries matching pattern.
        
        Args:
            pattern: Pattern to match keys
            
        Returns:
            True if successful
        """
        try:
            # Publish invalidation message
            message = {
                'pattern': pattern,
                'timestamp': datetime.now().isoformat()
            }
            self.redis.publish(self.channel, json.dumps(message))
            return True
            
        except redis.RedisError as e:
            logger.error(f"Redis error publishing invalidation: {e}")
            return False
    
    def register_handler(
        self,
        pattern: str,
        handler: Callable[[str], None]
    ) -> None:
        """Register invalidation handler.
        
        Args:
            pattern: Pattern to match keys
            handler: Handler function
        """
        if pattern not in self._handlers:
            self._handlers[pattern] = []
        self._handlers[pattern].append(handler)
    
    def unregister_handler(
        self,
        pattern: str,
        handler: Callable[[str], None]
    ) -> None:
        """Unregister invalidation handler.
        
        Args:
            pattern: Pattern to match keys
            handler: Handler function
        """
        if pattern in self._handlers:
            self._handlers[pattern].remove(handler)
            if not self._handlers[pattern]:
                del self._handlers[pattern]
    
    def process_messages(self) -> None:
        """Process invalidation messages."""
        try:
            for message in self.pubsub.listen():
                if message['type'] != 'message':
                    continue
                
                try:
                    data = json.loads(message['data'])
                    pattern = data['pattern']
                    
                    # Call handlers
                    for handler_pattern, handlers in self._handlers.items():
                        if self._match_pattern(pattern, handler_pattern):
                            for handler in handlers:
                                handler(pattern)
                                
                except json.JSONDecodeError as e:
                    logger.error(f"Error decoding message: {e}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    
        except redis.RedisError as e:
            logger.error(f"Redis error processing messages: {e}")
    
    def _match_pattern(self, key: str, pattern: str) -> bool:
        """Match key against pattern.
        
        Args:
            key: Key to match
            pattern: Pattern to match against
            
        Returns:
            True if key matches pattern
        """
        # Convert glob pattern to regex
        import re
        pattern = pattern.replace('*', '.*').replace('?', '.')
        return bool(re.match(f"^{pattern}$", key))
    
    def start(self) -> None:
        """Start processing invalidation messages."""
        import threading
        thread = threading.Thread(target=self.process_messages, daemon=True)
        thread.start()
    
    def stop(self) -> None:
        """Stop processing invalidation messages."""
        self.pubsub.unsubscribe(self.channel)
        self.pubsub.close()