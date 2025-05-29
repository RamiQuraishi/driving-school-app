"""MTO export logging models for tracking data exports."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship

from .base import BaseModel

class MTOExportLog(BaseModel):
    """MTO export log model.
    
    This model tracks:
    - Export operations
    - Export status
    - Export records
    - Export logs
    """
    
    export_type = Column(String(50), nullable=False)
    export_date = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False)
    file_path = Column(String(255))
    record_count = Column(Integer, nullable=False, default=0)
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    
    # Relationships
    records = relationship("MTOExportRecord", back_populates="export")
    logs = relationship("MTOExportLogEntry", back_populates="export")
    creator = relationship("User")
    
    def add_record(self, student_id: int, record_type: str, record_data: str) -> None:
        """Add export record.
        
        Args:
            student_id: Student ID
            record_type: Record type
            record_data: Record data
        """
        record = MTOExportRecord(
            export_id=self.id,
            student_id=student_id,
            record_type=record_type,
            record_data=record_data,
            status="pending"
        )
        self.records.append(record)
        self.record_count += 1
    
    def add_log(self, level: str, message: str) -> None:
        """Add log entry.
        
        Args:
            level: Log level
            message: Log message
        """
        log = MTOExportLogEntry(
            export_id=self.id,
            log_level=level,
            message=message
        )
        self.logs.append(log)
    
    def update_status(self, status: str) -> None:
        """Update export status.
        
        Args:
            status: New status
        """
        self.status = status
        self.add_log("info", f"Export status updated to {status}")

class MTOExportRecord(BaseModel):
    """MTO export record model."""
    
    export_id = Column(Integer, ForeignKey("mtoexportlog.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    record_type = Column(String(50), nullable=False)
    record_data = Column(Text, nullable=False)
    status = Column(String(20), nullable=False)
    error_message = Column(Text)
    
    # Relationships
    export = relationship("MTOExportLog", back_populates="records")
    student = relationship("Student")

class MTOExportLogEntry(BaseModel):
    """MTO export log entry model."""
    
    export_id = Column(Integer, ForeignKey("mtoexportlog.id"), nullable=False)
    log_level = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    
    # Relationships
    export = relationship("MTOExportLog", back_populates="logs") 