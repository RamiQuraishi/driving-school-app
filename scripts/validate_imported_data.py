#!/usr/bin/env python3
"""Script for validating imported data."""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional

from sqlalchemy.orm import Session

from ontario_driving_school_manager.data.db_setup import get_session
from ontario_driving_school_manager.services.migration import (
    StudentValidator,
    InstructorValidator,
    VehicleValidator,
    MigrationReport
)

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
        description="Validate imported data"
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("reports"),
        help="Output directory for reports"
    )
    
    parser.add_argument(
        "--types",
        nargs="+",
        choices=["student", "instructor", "vehicle"],
        default=["student", "instructor", "vehicle"],
        help="Types of data to validate"
    )
    
    return parser.parse_args()

def get_validators(
    session: Session,
    types: List[str]
) -> List[StudentValidator | InstructorValidator | VehicleValidator]:
    """Get appropriate validators.
    
    Args:
        session: Database session
        types: Types of validators to get
        
    Returns:
        List[StudentValidator | InstructorValidator | VehicleValidator]: Validators
    """
    validators = []
    
    if "student" in types:
        validators.append(StudentValidator(session))
    if "instructor" in types:
        validators.append(InstructorValidator(session))
    if "vehicle" in types:
        validators.append(VehicleValidator(session))
    
    return validators

def main() -> int:
    """Main entry point.
    
    Returns:
        int: Exit code
    """
    args = parse_args()
    
    try:
        # Get database session
        session = get_session()
        
        # Get validators
        validators = get_validators(session, args.types)
        
        # Initialize report generator
        report_generator = MigrationReport(args.output_dir)
        
        # Validate data
        for validator in validators:
            logger.info(f"Validating {validator.__class__.__name__}")
            
            # Get records to validate
            records = session.query(validator.model_class).all()
            
            # Validate records
            results = []
            for record in records:
                result = validator.validate(record.to_dict())
                results.append(result)
            
            # Generate report
            report_path = report_generator.generate_validation_report(
                results,
                validator.__class__.__name__
            )
            
            logger.info(f"Validation completed: {len(results)} records validated")
            logger.info(f"Report generated: {report_path}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Validation failed: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 