"""
Rollback handler service for database migrations.
Provides functionality to handle database rollbacks safely.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging
import subprocess
import shutil
import json
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RollbackHandler:
    """Handles database rollback operations."""

    def __init__(self, db_url: str, backup_dir: Optional[Path] = None):
        """Initialize the rollback handler."""
        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.backup_dir = backup_dir or Path(__file__).parent.parent.parent / 'data' / 'migrations' / 'rollback' / 'backups'
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self) -> Optional[Path]:
        """Create a database backup."""
        try:
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            backup_file = self.backup_dir / f'backup_{timestamp}.sql'
            
            # Use pg_dump for PostgreSQL databases
            if 'postgresql' in self.db_url:
                cmd = [
                    'pg_dump',
                    '--dbname=' + self.db_url,
                    '--file=' + str(backup_file),
                    '--format=custom',
                    '--verbose'
                ]
                subprocess.run(cmd, check=True)
            else:
                raise ValueError(f'Unsupported database type in URL: {self.db_url}')

            logger.info(f'Created backup: {backup_file}')
            return backup_file

        except Exception as e:
            logger.error(f'Failed to create backup: {str(e)}')
            return None

    def restore_backup(self, backup_file: Path) -> bool:
        """Restore a database backup."""
        try:
            if not backup_file.exists():
                raise FileNotFoundError(f'Backup file not found: {backup_file}')

            # Use pg_restore for PostgreSQL databases
            if 'postgresql' in self.db_url:
                cmd = [
                    'pg_restore',
                    '--dbname=' + self.db_url,
                    '--verbose',
                    '--clean',
                    '--if-exists',
                    str(backup_file)
                ]
                subprocess.run(cmd, check=True)
            else:
                raise ValueError(f'Unsupported database type in URL: {self.db_url}')

            logger.info(f'Restored backup: {backup_file}')
            return True

        except Exception as e:
            logger.error(f'Failed to restore backup: {str(e)}')
            return False

    def verify_database_state(self) -> Tuple[bool, List[str]]:
        """Verify the database state after rollback."""
        errors = []
        try:
            with self.engine.connect() as conn:
                # Check if all tables exist
                result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
                tables = [row[0] for row in result]
                
                # Verify critical tables
                critical_tables = ['students', 'instructors', 'lessons', 'vehicles']
                missing_tables = [table for table in critical_tables if table not in tables]
                
                if missing_tables:
                    errors.append(f'Missing critical tables: {missing_tables}')

                # Check table constraints
                for table in critical_tables:
                    if table in tables:
                        result = conn.execute(text(f"SELECT constraint_name FROM information_schema.table_constraints WHERE table_name = '{table}'"))
                        constraints = [row[0] for row in result]
                        if not constraints:
                            errors.append(f'No constraints found for table: {table}')

                # Check for data integrity
                for table in critical_tables:
                    if table in tables:
                        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                        count = result.scalar()
                        if count < 0:
                            errors.append(f'Invalid row count for table {table}: {count}')

                return len(errors) == 0, errors

        except SQLAlchemyError as e:
            errors.append(f'Database verification failed: {str(e)}')
            return False, errors

    def get_backup_info(self) -> Dict:
        """Get information about available backups."""
        backups = sorted(self.backup_dir.glob('*.sql'))
        return {
            'backup_count': len(backups),
            'latest_backup': str(backups[-1]) if backups else None,
            'backup_size': sum(f.stat().st_size for f in backups),
            'backup_files': [str(f) for f in backups]
        }

    def cleanup_old_backups(self, keep_last_n: int = 5) -> int:
        """Clean up old backups, keeping only the last N backups."""
        try:
            backups = sorted(self.backup_dir.glob('*.sql'))
            if len(backups) <= keep_last_n:
                return 0

            to_delete = backups[:-keep_last_n]
            for backup in to_delete:
                backup.unlink()
                logger.info(f'Deleted old backup: {backup}')

            return len(to_delete)

        except Exception as e:
            logger.error(f'Failed to cleanup old backups: {str(e)}')
            return 0

    def rollback_to_revision(self, target_revision: str) -> bool:
        """Rollback database to a specific revision."""
        try:
            # Create backup before rollback
            backup_file = self.create_backup()
            if not backup_file:
                raise Exception('Failed to create backup before rollback')

            # Perform rollback using Alembic
            cmd = [
                'alembic',
                'downgrade',
                target_revision
            ]
            subprocess.run(cmd, check=True)

            # Verify database state
            success, errors = self.verify_database_state()
            if not success:
                logger.error(f'Database verification failed after rollback: {errors}')
                # Restore from backup
                self.restore_backup(backup_file)
                return False

            logger.info(f'Successfully rolled back to revision: {target_revision}')
            return True

        except Exception as e:
            logger.error(f'Failed to rollback to revision {target_revision}: {str(e)}')
            return False 