"""Database session management."""

import contextlib
from typing import Generator, Optional
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import os

from .connection_pool import ConnectionPool

# Create session factory
Session = sessionmaker(autocommit=False, autoflush=False)

def get_session() -> Generator[Session, None, None]:
    """Get a database session.
    
    Yields:
        Session: A SQLAlchemy session.
    """
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

@contextlib.contextmanager
def session_scope() -> Generator[Session, None, None]:
    """Context manager for database sessions.
    
    Yields:
        Session: A SQLAlchemy session.
        
    Example:
        with session_scope() as session:
            session.add(some_object)
            # Session is automatically committed if no exceptions occur
    """
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def init_session(engine: Optional[Engine] = None) -> None:
    """Initialize the session factory with an engine.
    
    Args:
        engine: SQLAlchemy engine to use. If None, uses the default engine.
    """
    if engine is None:
        engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///./ontario_driving_school.db"))
    Session.configure(bind=engine) 