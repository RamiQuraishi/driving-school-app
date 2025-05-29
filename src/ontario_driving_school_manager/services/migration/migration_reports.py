"""Migration reports for tracking and analyzing data migration."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from jinja2 import Environment, FileSystemLoader

from .competitor_importers import ImportResult
from .data_validators import ValidationResult

@dataclass
class ImportSummary:
    """Summary of import operations."""
    
    total_records: int
    successful_records: int
    failed_records: int
    warnings: int
    start_time: datetime
    end_time: datetime
    duration_seconds: float
    
    @classmethod
    def from_import_result(cls, result: ImportResult) -> "ImportSummary":
        """Create summary from import result.
        
        Args:
            result: Import result
            
        Returns:
            ImportSummary: Import summary
        """
        return cls(
            total_records=result.records_processed,
            successful_records=result.records_imported,
            failed_records=result.records_processed - result.records_imported,
            warnings=len(result.warnings),
            start_time=result.start_time,
            end_time=result.end_time,
            duration_seconds=result.duration_seconds
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert summary to dictionary."""
        return {
            "total_records": self.total_records,
            "successful_records": self.successful_records,
            "failed_records": self.failed_records,
            "warnings": self.warnings,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_seconds": self.duration_seconds,
            "success_rate": (self.successful_records / self.total_records * 100)
            if self.total_records > 0 else 0
        }

@dataclass
class ValidationReport:
    """Report of validation results."""
    
    total_validated: int
    valid_records: int
    invalid_records: int
    errors: List[Dict[str, Any]]
    warnings: List[Dict[str, Any]]
    start_time: datetime
    end_time: datetime
    
    @property
    def duration_seconds(self) -> float:
        """Get validation duration in seconds."""
        return (self.end_time - self.start_time).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            "total_validated": self.total_validated,
            "valid_records": self.valid_records,
            "invalid_records": self.invalid_records,
            "errors": self.errors,
            "warnings": self.warnings,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_seconds": self.duration_seconds,
            "validity_rate": (self.valid_records / self.total_validated * 100)
            if self.total_validated > 0 else 0
        }

class MigrationReport:
    """Migration report generator."""
    
    def __init__(self, output_dir: Path):
        """Initialize report generator.
        
        Args:
            output_dir: Output directory for reports
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup Jinja2 environment
        template_dir = Path(__file__).parent / "templates"
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=True
        )
    
    def generate_import_report(
        self,
        summary: ImportSummary,
        errors: List[Dict[str, Any]],
        warnings: List[Dict[str, Any]]
    ) -> Path:
        """Generate import report.
        
        Args:
            summary: Import summary
            errors: Import errors
            warnings: Import warnings
            
        Returns:
            Path: Report file path
        """
        template = self.env.get_template("import_report.html")
        
        # Prepare data
        data = {
            "summary": summary.to_dict(),
            "errors": errors,
            "warnings": warnings,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Generate report
        report_path = self.output_dir / f"import_report_{datetime.utcnow():%Y%m%d_%H%M%S}.html"
        report_path.write_text(template.render(**data))
        
        return report_path
    
    def generate_validation_report(
        self,
        report: ValidationReport
    ) -> Path:
        """Generate validation report.
        
        Args:
            report: Validation report
            
        Returns:
            Path: Report file path
        """
        template = self.env.get_template("validation_report.html")
        
        # Prepare data
        data = {
            "report": report.to_dict(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Generate report
        report_path = self.output_dir / f"validation_report_{datetime.utcnow():%Y%m%d_%H%M%S}.html"
        report_path.write_text(template.render(**data))
        
        return report_path
    
    def generate_summary_report(
        self,
        import_summaries: List[ImportSummary],
        validation_reports: List[ValidationReport]
    ) -> Path:
        """Generate summary report.
        
        Args:
            import_summaries: List of import summaries
            validation_reports: List of validation reports
            
        Returns:
            Path: Report file path
        """
        template = self.env.get_template("summary_report.html")
        
        # Prepare data
        data = {
            "import_summaries": [s.to_dict() for s in import_summaries],
            "validation_reports": [r.to_dict() for r in validation_reports],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Generate report
        report_path = self.output_dir / f"summary_report_{datetime.utcnow():%Y%m%d_%H%M%S}.html"
        report_path.write_text(template.render(**data))
        
        return report_path
    
    def export_to_csv(
        self,
        data: List[Dict[str, Any]],
        filename: str
    ) -> Path:
        """Export data to CSV.
        
        Args:
            data: Data to export
            filename: Output filename
            
        Returns:
            Path: CSV file path
        """
        df = pd.DataFrame(data)
        csv_path = self.output_dir / filename
        df.to_csv(csv_path, index=False)
        
        return csv_path 