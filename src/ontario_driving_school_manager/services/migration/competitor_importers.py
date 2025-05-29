"""Competitor data importers for migrating from other systems."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd
from sqlalchemy.orm import Session

from ...models import (
    Student,
    Instructor,
    Vehicle,
    Lesson,
    Payment,
    MTOCompliance
)

@dataclass
class ImportResult:
    """Result of an import operation."""
    
    success: bool
    records_processed: int
    records_imported: int
    errors: List[Dict[str, Any]]
    warnings: List[Dict[str, Any]]
    start_time: datetime
    end_time: datetime
    
    @property
    def duration_seconds(self) -> float:
        """Get import duration in seconds."""
        return (self.end_time - self.start_time).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "success": self.success,
            "records_processed": self.records_processed,
            "records_imported": self.records_imported,
            "errors": self.errors,
            "warnings": self.warnings,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_seconds": self.duration_seconds
        }

class BaseImporter(ABC):
    """Base class for data importers."""
    
    def __init__(self, session: Session):
        """Initialize importer.
        
        Args:
            session: Database session
        """
        self.session = session
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
    
    @abstractmethod
    def import_data(self, source: Union[str, Path, pd.DataFrame]) -> ImportResult:
        """Import data from source.
        
        Args:
            source: Data source (file path or DataFrame)
            
        Returns:
            ImportResult: Import result
        """
        pass
    
    def add_error(self, message: str, record: Optional[Dict[str, Any]] = None) -> None:
        """Add error message.
        
        Args:
            message: Error message
            record: Related record
        """
        self.errors.append({
            "message": message,
            "record": record,
            "timestamp": datetime.utcnow()
        })
    
    def add_warning(self, message: str, record: Optional[Dict[str, Any]] = None) -> None:
        """Add warning message.
        
        Args:
            message: Warning message
            record: Related record
        """
        self.warnings.append({
            "message": message,
            "record": record,
            "timestamp": datetime.utcnow()
        })

class DrivingSchoolSoftwareImporter(BaseImporter):
    """Importer for Driving School Software data."""
    
    def import_data(self, source: Union[str, Path, pd.DataFrame]) -> ImportResult:
        """Import data from Driving School Software.
        
        Args:
            source: Data source (file path or DataFrame)
            
        Returns:
            ImportResult: Import result
        """
        start_time = datetime.utcnow()
        records_processed = 0
        records_imported = 0
        
        try:
            # Load data
            if isinstance(source, (str, Path)):
                df = pd.read_csv(source)
            else:
                df = source
            
            # Process records
            for _, row in df.iterrows():
                records_processed += 1
                try:
                    self._process_record(row)
                    records_imported += 1
                except Exception as e:
                    self.add_error(str(e), row.to_dict())
            
            # Commit changes
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            self.add_error(f"Import failed: {str(e)}")
        
        return ImportResult(
            success=len(self.errors) == 0,
            records_processed=records_processed,
            records_imported=records_imported,
            errors=self.errors,
            warnings=self.warnings,
            start_time=start_time,
            end_time=datetime.utcnow()
        )
    
    def _process_record(self, record: pd.Series) -> None:
        """Process single record.
        
        Args:
            record: Record to process
        """
        # Map fields based on Driving School Software schema
        student_data = {
            "first_name": record.get("FirstName"),
            "last_name": record.get("LastName"),
            "email": record.get("Email"),
            "phone": record.get("Phone"),
            "address": record.get("Address"),
            "city": record.get("City"),
            "province": record.get("Province"),
            "postal_code": record.get("PostalCode"),
            "date_of_birth": pd.to_datetime(record.get("DateOfBirth")).date(),
            "license_number": record.get("LicenseNumber")
        }
        
        # Create student
        student = Student(**student_data)
        self.session.add(student)
        
        # Process related records
        self._process_lessons(record, student)
        self._process_payments(record, student)

class GenericCSVImporter(BaseImporter):
    """Importer for generic CSV data."""
    
    def __init__(self, session: Session, field_mapping: Dict[str, str]):
        """Initialize importer.
        
        Args:
            session: Database session
            field_mapping: Field mapping from CSV to model
        """
        super().__init__(session)
        self.field_mapping = field_mapping
    
    def import_data(self, source: Union[str, Path, pd.DataFrame]) -> ImportResult:
        """Import data from generic CSV.
        
        Args:
            source: Data source (file path or DataFrame)
            
        Returns:
            ImportResult: Import result
        """
        start_time = datetime.utcnow()
        records_processed = 0
        records_imported = 0
        
        try:
            # Load data
            if isinstance(source, (str, Path)):
                df = pd.read_csv(source)
            else:
                df = source
            
            # Validate required fields
            missing_fields = self._validate_fields(df.columns)
            if missing_fields:
                raise ValueError(f"Missing required fields: {missing_fields}")
            
            # Process records
            for _, row in df.iterrows():
                records_processed += 1
                try:
                    self._process_record(row)
                    records_imported += 1
                except Exception as e:
                    self.add_error(str(e), row.to_dict())
            
            # Commit changes
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            self.add_error(f"Import failed: {str(e)}")
        
        return ImportResult(
            success=len(self.errors) == 0,
            records_processed=records_processed,
            records_imported=records_imported,
            errors=self.errors,
            warnings=self.warnings,
            start_time=start_time,
            end_time=datetime.utcnow()
        )
    
    def _validate_fields(self, columns: List[str]) -> List[str]:
        """Validate required fields.
        
        Args:
            columns: CSV columns
            
        Returns:
            List[str]: Missing fields
        """
        return [
            field for field in self.field_mapping.values()
            if field not in columns
        ]
    
    def _process_record(self, record: pd.Series) -> None:
        """Process single record.
        
        Args:
            record: Record to process
        """
        # Map fields using provided mapping
        data = {
            model_field: record.get(csv_field)
            for csv_field, model_field in self.field_mapping.items()
        }
        
        # Create record
        model_class = self._get_model_class()
        instance = model_class(**data)
        self.session.add(instance)
    
    def _get_model_class(self) -> type:
        """Get model class for import.
        
        Returns:
            type: Model class
        """
        # This should be overridden by subclasses
        raise NotImplementedError 