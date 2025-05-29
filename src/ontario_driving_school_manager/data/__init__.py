"""Database and data management package.

This package provides database connection management, session handling,
and data access functionality for the Ontario Driving School Manager.
"""

from .base import Base
from .session import get_session, Session
from .db_setup import setup_database, teardown_database
from .connection_pool import ConnectionPool

__all__ = [
    'Base',
    'get_session',
    'Session',
    'setup_database',
    'teardown_database',
    'ConnectionPool',
] 