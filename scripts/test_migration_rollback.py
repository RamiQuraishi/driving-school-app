#!/usr/bin/env python3
"""
Test script for database migration rollback procedures.
Ensures that database migrations can be safely rolled back.
"""

import os
import sys
import pytest
from pathlib import Path
from datetime import datetime
import logging
from typing import List, Dict, Any
import alembic
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MigrationRollbackTester:
    """Tests database migration rollback procedures."""

    def __init__(self, db_url: str, alembic_cfg_path: str):
        """Initialize the tester."""
        self.db_url = db_url
        self.alembic_cfg_path = alembic_cfg_path
        self.engine = create_engine(db_url)
        self.alembic_cfg = Config(alembic_cfg_path)
        self.script = ScriptDirectory.from_config(self.alembic_cfg)

    def get_current_revision(self) -> str:
        """Get the current database revision."""
        with self.engine.connect() as conn:
            context = MigrationContext.configure(conn)
            return context.get_current_revision()

    def get_all_revisions(self) -> List[str]:
        """Get all available migration revisions."""
        return [rev.revision for rev in self.script.walk_revisions()]

    def test_rollback_to_revision(self, target_revision: str) -> bool:
        """Test rolling back to a specific revision."""
        try:
            logger.info(f"Testing rollback to revision: {target_revision}")
            
            # Get current revision
            current_rev = self.get_current_revision()
            logger.info(f"Current revision: {current_rev}")

            # Perform rollback
            alembic.command.downgrade(self.alembic_cfg, target_revision)
            logger.info(f"Successfully rolled back to revision: {target_revision}")

            # Verify rollback
            new_rev = self.get_current_revision()
            if new_rev != target_revision:
                logger.error(f"Rollback verification failed. Expected {target_revision}, got {new_rev}")
                return False

            # Roll forward to original revision
            alembic.command.upgrade(self.alembic_cfg, current_rev)
            logger.info(f"Successfully rolled forward to original revision: {current_rev}")

            return True

        except Exception as e:
            logger.error(f"Error during rollback test: {str(e)}")
            return False

    def test_all_rollbacks(self) -> Dict[str, bool]:
        """Test rolling back through all revisions."""
        results = {}
        revisions = self.get_all_revisions()
        
        for i in range(len(revisions) - 1):
            target_rev = revisions[i]
            success = self.test_rollback_to_revision(target_rev)
            results[target_rev] = success
            
            if not success:
                logger.error(f"Failed to rollback to revision: {target_rev}")
                break

        return results

    def verify_database_state(self) -> bool:
        """Verify the database state after rollback."""
        try:
            with self.engine.connect() as conn:
                # Check if all tables exist
                result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
                tables = [row[0] for row in result]
                
                # Verify critical tables
                critical_tables = ['students', 'instructors', 'lessons', 'vehicles']
                missing_tables = [table for table in critical_tables if table not in tables]
                
                if missing_tables:
                    logger.error(f"Missing critical tables: {missing_tables}")
                    return False

                # Check table constraints
                for table in critical_tables:
                    result = conn.execute(text(f"SELECT constraint_name FROM information_schema.table_constraints WHERE table_name = '{table}'"))
                    constraints = [row[0] for row in result]
                    if not constraints:
                        logger.error(f"No constraints found for table: {table}")
                        return False

                return True

        except SQLAlchemyError as e:
            logger.error(f"Database verification failed: {str(e)}")
            return False

def main():
    """Main entry point for the test script."""
    # Get database URL from environment
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        logger.error("DATABASE_URL environment variable not set")
        sys.exit(1)

    # Get alembic config path
    alembic_cfg_path = os.getenv('ALEMBIC_CONFIG', 'alembic.ini')
    if not Path(alembic_cfg_path).exists():
        logger.error(f"Alembic config file not found: {alembic_cfg_path}")
        sys.exit(1)

    # Initialize tester
    tester = MigrationRollbackTester(db_url, alembic_cfg_path)

    # Run tests
    logger.info("Starting migration rollback tests...")
    results = tester.test_all_rollbacks()

    # Report results
    success = all(results.values())
    if success:
        logger.info("All rollback tests passed!")
        sys.exit(0)
    else:
        logger.error("Some rollback tests failed!")
        for revision, result in results.items():
            status = "PASSED" if result else "FAILED"
            logger.error(f"Revision {revision}: {status}")
        sys.exit(1)

if __name__ == '__main__':
    main() 