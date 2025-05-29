"""Database setup and teardown utilities."""

import logging
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import os

from .base import Base
from .session import init_session

logger = logging.getLogger(__name__)

def setup_database(engine: Optional[Engine] = None) -> None:
    """Set up the database.
    
    This function:
    1. Creates the database engine if not provided
    2. Initializes the session factory
    3. Creates all tables if they don't exist
    
    Args:
        engine: SQLAlchemy engine to use. If None, creates a new engine.
    """
    try:
        if engine is None:
            database_url = os.getenv("DATABASE_URL", "sqlite:///./ontario_driving_school.db")
            engine = create_engine(database_url)
        
        # Initialize session factory
        init_session(engine)
        
        # Create all tables
        Base.metadata.create_all(engine)
        
        logger.info("Database setup completed successfully")
    except Exception as e:
        logger.error(f"Error setting up database: {e}")
        raise

def teardown_database(engine: Optional[Engine] = None) -> None:
    """Tear down the database.
    
    This function drops all tables from the database.
    Use with caution in production!
    
    Args:
        engine: SQLAlchemy engine to use. If None, creates a new engine.
    """
    try:
        if engine is None:
            database_url = os.getenv("DATABASE_URL", "sqlite:///./ontario_driving_school.db")
            engine = create_engine(database_url)
        
        # Drop all tables
        Base.metadata.drop_all(engine)
        
        logger.info("Database teardown completed successfully")
    except Exception as e:
        logger.error(f"Error tearing down database: {e}")
        raise 