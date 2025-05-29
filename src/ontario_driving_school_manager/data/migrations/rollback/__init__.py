"""
Rollback system for database migrations.
Provides functionality to safely rollback database changes.
"""

from pathlib import Path
from typing import List, Dict, Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Rollback paths
ROLLBACK_DIR = Path(__file__).parent
BACKUP_DIR = ROLLBACK_DIR / 'backups'

def ensure_backup_dir():
    """Ensure the backup directory exists."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

def get_backup_files() -> List[Path]:
    """Get all backup files in the backup directory."""
    ensure_backup_dir()
    return sorted(BACKUP_DIR.glob('*.sql'))

def get_latest_backup() -> Optional[Path]:
    """Get the latest backup file."""
    backups = get_backup_files()
    return backups[-1] if backups else None

def generate_backup_filename() -> str:
    """Generate a backup filename with timestamp."""
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    return f'backup_{timestamp}.sql'

def get_rollback_metadata() -> Dict:
    """Get metadata about the rollback system."""
    return {
        'backup_dir': str(BACKUP_DIR),
        'latest_backup': str(get_latest_backup()) if get_latest_backup() else None,
        'backup_count': len(get_backup_files()),
        'rollback_files': [str(f) for f in ROLLBACK_DIR.glob('*.py') if f.name != '__init__.py']
    } 