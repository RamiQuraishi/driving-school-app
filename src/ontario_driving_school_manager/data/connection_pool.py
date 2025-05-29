"""Database connection pool management."""

import logging
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool
import os

logger = logging.getLogger(__name__)

class ConnectionPool:
    """Manages database connection pooling."""
    
    def __init__(
        self,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: int = 30,
        pool_recycle: int = 3600,
        engine: Optional[Engine] = Non e
    ):
        """Initialize the connection pool.
        
        Args:
            pool_size: Number of connections to keep open
            max_overflow: Maximum number of connections that can be created beyond pool_size
            pool_timeout: Seconds to wait before giving up on getting a connection
            pool_recycle: Seconds after which a connection is automatically recycled
            engine: SQLAlchemy engine to use. If None, creates a new engine.
        """
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_timeout = pool_timeout
        self.pool_recycle = pool_recycle
        self._engine = engine or self._create_engine()
    
    def _create_engine(self) -> Engine:
        """Create a new SQLAlchemy engine with connection pooling.
        
        Returns:
            Engine: Configured SQLAlchemy engine
        """
        database_url = os.getenv("DATABASE_URL", "sqlite:///./ontario_driving_school.db")
        
        return create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_timeout=self.pool_timeout,
            pool_recycle=self.pool_recycle,
            pool_pre_ping=True  # Enable connection health checks
        )
    
    @property
    def engine(self) -> Engine:
        """Get the SQLAlchemy engine.
        
        Returns:
            Engine: The configured SQLAlchemy engine
        """
        return self._engine
    
    def dispose(self) -> None:
        """Dispose of the connection pool and all its connections."""
        if self._engine:
            self._engine.dispose()
            logger.info("Connection pool disposed") 