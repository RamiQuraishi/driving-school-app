"""
Database migrations package for Ontario Driving School Manager.
Handles database schema migrations and rollbacks.
"""

from pathlib import Path
from typing import List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Migration paths
MIGRATIONS_DIR = Path(__file__).parent
ROLLBACK_DIR = MIGRATIONS_DIR / 'rollback'

def get_migration_files() -> List[Path]:
    """Get all migration files in the migrations directory."""
    return sorted(MIGRATIONS_DIR.glob('*.py'))

def get_rollback_files() -> List[Path]:
    """Get all rollback files in the rollback directory."""
    return sorted(ROLLBACK_DIR.glob('*.py'))

def get_latest_migration() -> Optional[Path]:
    """Get the latest migration file."""
    migrations = get_migration_files()
    return migrations[-1] if migrations else None

def get_latest_rollback() -> Optional[Path]:
    """Get the latest rollback file."""
    rollbacks = get_rollback_files()
    return rollbacks[-1] if rollbacks else None 