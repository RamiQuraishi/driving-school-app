#!/usr/bin/env python3
"""Script for importing data from competitor systems."""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from sqlalchemy.orm import Session

from ontario_driving_school_manager.data.db_setup import get_session
from ontario_driving_school_manager.services.migration import (
    DrivingSchoolSoftwareImporter,
    GenericCSVImporter,
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
        description="Import data from competitor systems"
    )
    
    parser.add_argument(
        "source",
        type=Path,
        help="Source file or directory"
    )
    
    parser.add_argument(
        "--type",
        choices=["dss", "csv"],
        required=True,
        help="Source data type"
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("reports"),
        help="Output directory for reports"
    )
    
    parser.add_argument(
        "--field-mapping",
        type=Path,
        help="Field mapping file for CSV import"
    )
    
    return parser.parse_args()

def get_importer(
    session: Session,
    importer_type: str,
    field_mapping: Optional[Path] = None
) -> DrivingSchoolSoftwareImporter | GenericCSVImporter:
    """Get appropriate importer.
    
    Args:
        session: Database session
        importer_type: Type of importer
        field_mapping: Field mapping file
        
    Returns:
        DrivingSchoolSoftwareImporter | GenericCSVImporter: Importer instance
    """
    if importer_type == "dss":
        return DrivingSchoolSoftwareImporter(session)
    elif importer_type == "csv":
        if not field_mapping:
            raise ValueError("Field mapping required for CSV import")
        
        # Load field mapping
        import json
        with field_mapping.open() as f:
            mapping = json.load(f)
        
        return GenericCSVImporter(session, mapping)
    else:
        raise ValueError(f"Unknown importer type: {importer_type}")

def main() -> int:
    """Main entry point.
    
    Returns:
        int: Exit code
    """
    args = parse_args()
    
    try:
        # Get database session
        session = get_session()
        
        # Get importer
        importer = get_importer(
            session,
            args.type,
            args.field_mapping
        )
        
        # Import data
        logger.info(f"Importing data from {args.source}")
        result = importer.import_data(args.source)
        
        # Generate report
        report_generator = MigrationReport(args.output_dir)
        report_path = report_generator.generate_import_report(
            result.to_dict(),
            result.errors,
            result.warnings
        )
        
        logger.info(f"Import completed: {result.records_imported} records imported")
        logger.info(f"Report generated: {report_path}")
        
        return 0 if result.success else 1
        
    except Exception as e:
        logger.error(f"Import failed: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 