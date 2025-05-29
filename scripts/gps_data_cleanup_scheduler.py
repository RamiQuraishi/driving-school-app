#!/usr/bin/env python3
"""Script for scheduling GPS data cleanup based on retention policies."""

import argparse
import logging
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from sqlalchemy.orm import Session

from ontario_driving_school_manager.data.db_setup import get_session
from ontario_driving_school_manager.services.gps_retention_service import GPSRetentionService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def parse_args() -> argparse.Namespace:
    """Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Schedule GPS data cleanup based on retention policies"
    )
    
    parser.add_argument(
        "--interval",
        type=int,
        default=24,
        help="Check interval in hours (default: 24)"
    )
    
    parser.add_argument(
        "--run-once",
        action="store_true",
        help="Run once and exit"
    )
    
    parser.add_argument(
        "--policy-id",
        type=int,
        help="Run specific policy ID"
    )
    
    return parser.parse_args()

def run_cleanup(
    session: Session,
    policy_id: Optional[int] = None
) -> None:
    """Run GPS data cleanup.
    
    Args:
        session: Database session
        policy_id: Optional policy ID to run
    """
    service = GPSRetentionService(session)
    
    try:
        if policy_id:
            # Run specific policy
            records_deleted, errors = service.execute_policy(policy_id)
            logger.info(
                f"Policy {policy_id}: deleted {records_deleted} records, "
                f"errors: {len(errors)}"
            )
        else:
            # Run all active policies
            policies = service.get_active_policies()
            for policy in policies:
                try:
                    records_deleted, errors = service.execute_policy(policy.id)
                    logger.info(
                        f"Policy {policy.name}: deleted {records_deleted} records, "
                        f"errors: {len(errors)}"
                    )
                except Exception as e:
                    logger.error(f"Error executing policy {policy.name}: {str(e)}")
        
        # Get retention stats
        stats = service.get_retention_stats()
        logger.info(f"Retention stats: {stats}")
        
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")
        raise

def main() -> int:
    """Main entry point.
    
    Returns:
        int: Exit code
    """
    args = parse_args()
    
    try:
        # Get database session
        session = get_session()
        
        if args.run_once:
            # Run once and exit
            run_cleanup(session, args.policy_id)
            return 0
        
        # Run continuously
        logger.info(f"Starting GPS cleanup scheduler (interval: {args.interval}h)")
        
        while True:
            try:
                run_cleanup(session, args.policy_id)
            except Exception as e:
                logger.error(f"Cleanup failed: {str(e)}")
            
            # Sleep until next interval
            next_run = datetime.utcnow() + timedelta(hours=args.interval)
            logger.info(f"Next cleanup scheduled for: {next_run}")
            time.sleep(args.interval * 3600)
        
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
        return 0
    except Exception as e:
        logger.error(f"Scheduler failed: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 