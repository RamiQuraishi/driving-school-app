"""
Data Export Manager Module

This module provides data export management functionality for PIPEDA compliance.
It handles data export requests, processing, and delivery.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import zipfile
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

logger = logging.getLogger(__name__)

class ExportError(Exception):
    """Export error."""
    pass

class ExportRequest:
    """Export request."""
    
    def __init__(
        self,
        request_id: str,
        user_id: str,
        data_types: List[str],
        format: str,
        created_at: datetime,
        completed_at: Optional[datetime] = None,
        status: str = "pending",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Initialize export request.
        
        Args:
            request_id: Request ID
            user_id: User ID
            data_types: List of data types
            format: Export format
            created_at: Creation timestamp
            completed_at: Completion timestamp
            status: Request status (pending, processing, completed, failed)
            metadata: Additional metadata
        """
        self.request_id = request_id
        self.user_id = user_id
        self.data_types = data_types
        self.format = format
        self.created_at = created_at
        self.completed_at = completed_at
        self.status = status
        self.metadata = metadata or {}

class DataExportManager:
    """Data export manager."""
    
    def __init__(
        self,
        requests_dir: str = "requests",
        exports_dir: str = "exports",
        data_dir: str = "data",
        smtp_host: Optional[str] = None,
        smtp_port: Optional[int] = None,
        smtp_username: Optional[str] = None,
        smtp_password: Optional[str] = None
    ):
        """Initialize data export manager.
        
        Args:
            requests_dir: Requests directory
            exports_dir: Exports directory
            data_dir: Data directory
            smtp_host: SMTP host
            smtp_port: SMTP port
            smtp_username: SMTP username
            smtp_password: SMTP password
        """
        self.requests_dir = requests_dir
        self.exports_dir = exports_dir
        self.data_dir = data_dir
        
        # Create directories if they don't exist
        os.makedirs(requests_dir, exist_ok=True)
        os.makedirs(exports_dir, exist_ok=True)
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize SMTP settings
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
    
    def create_request(
        self,
        user_id: str,
        data_types: List[str],
        format: str = "json",
        metadata: Optional[Dict[str, Any]] = None
    ) -> ExportRequest:
        """Create export request.
        
        Args:
            user_id: User ID
            data_types: List of data types
            format: Export format
            metadata: Additional metadata
            
        Returns:
            Export request
            
        Raises:
            ExportError: If request creation fails
        """
        try:
            # Create request ID
            request_id = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create export request
            request = ExportRequest(
                request_id=request_id,
                user_id=user_id,
                data_types=data_types,
                format=format,
                created_at=datetime.utcnow(),
                metadata=metadata
            )
            
            # Create request file
            request_file = os.path.join(
                self.requests_dir,
                f"{request_id}.json"
            )
            
            # Write request data
            request_data = {
                "request_id": request.request_id,
                "user_id": request.user_id,
                "data_types": request.data_types,
                "format": request.format,
                "created_at": request.created_at.isoformat(),
                "completed_at": request.completed_at.isoformat() if request.completed_at else None,
                "status": request.status,
                "metadata": request.metadata
            }
            
            with open(request_file, "w") as f:
                json.dump(request_data, f, indent=2)
            
            logger.info(f"Created export request: {request_id}")
            
            return request
        except Exception as e:
            raise ExportError(f"Error creating request: {str(e)}")
    
    def get_request(
        self,
        request_id: str
    ) -> Optional[ExportRequest]:
        """Get export request.
        
        Args:
            request_id: Request ID
            
        Returns:
            Export request if found, None otherwise
        """
        try:
            # Get request file path
            request_file = os.path.join(
                self.requests_dir,
                f"{request_id}.json"
            )
            
            # Check if request file exists
            if not os.path.exists(request_file):
                return None
            
            # Read request data
            with open(request_file, "r") as f:
                request_data = json.load(f)
            
            # Create export request
            return ExportRequest(
                request_id=request_data["request_id"],
                user_id=request_data["user_id"],
                data_types=request_data["data_types"],
                format=request_data["format"],
                created_at=datetime.fromisoformat(request_data["created_at"]),
                completed_at=datetime.fromisoformat(request_data["completed_at"]) if request_data["completed_at"] else None,
                status=request_data["status"],
                metadata=request_data["metadata"]
            )
        except Exception as e:
            logger.error(f"Error getting request: {str(e)}")
            return None
    
    def get_requests(
        self,
        user_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[ExportRequest]:
        """Get export requests.
        
        Args:
            user_id: User ID
            status: Request status
            
        Returns:
            List of export requests
        """
        requests = []
        
        try:
            # Iterate through requests directory
            for request_file in Path(self.requests_dir).glob("*.json"):
                with open(request_file, "r") as f:
                    request_data = json.load(f)
                
                # Filter by user ID
                if user_id and request_data["user_id"] != user_id:
                    continue
                
                # Filter by status
                if status and request_data["status"] != status:
                    continue
                
                # Create export request
                request = ExportRequest(
                    request_id=request_data["request_id"],
                    user_id=request_data["user_id"],
                    data_types=request_data["data_types"],
                    format=request_data["format"],
                    created_at=datetime.fromisoformat(request_data["created_at"]),
                    completed_at=datetime.fromisoformat(request_data["completed_at"]) if request_data["completed_at"] else None,
                    status=request_data["status"],
                    metadata=request_data["metadata"]
                )
                
                requests.append(request)
        except Exception as e:
            logger.error(f"Error getting requests: {str(e)}")
        
        return requests
    
    def update_request(
        self,
        request: ExportRequest
    ) -> None:
        """Update export request.
        
        Args:
            request: Export request
            
        Raises:
            ExportError: If request doesn't exist
        """
        try:
            # Get request file path
            request_file = os.path.join(
                self.requests_dir,
                f"{request.request_id}.json"
            )
            
            # Check if request file exists
            if not os.path.exists(request_file):
                raise ExportError(f"Request doesn't exist: {request.request_id}")
            
            # Write request data
            request_data = {
                "request_id": request.request_id,
                "user_id": request.user_id,
                "data_types": request.data_types,
                "format": request.format,
                "created_at": request.created_at.isoformat(),
                "completed_at": request.completed_at.isoformat() if request.completed_at else None,
                "status": request.status,
                "metadata": request.metadata
            }
            
            with open(request_file, "w") as f:
                json.dump(request_data, f, indent=2)
            
            logger.info(f"Updated export request: {request.request_id}")
        except Exception as e:
            raise ExportError(f"Error updating request: {str(e)}")
    
    def process_request(
        self,
        request: ExportRequest
    ) -> str:
        """Process export request.
        
        Args:
            request: Export request
            
        Returns:
            Path to exported file
            
        Raises:
            ExportError: If processing fails
        """
        try:
            # Update request status
            request.status = "processing"
            self.update_request(request)
            
            # Create export directory
            export_dir = os.path.join(
                self.exports_dir,
                request.request_id
            )
            
            os.makedirs(export_dir, exist_ok=True)
            
            # Export data
            for data_type in request.data_types:
                data_dir = os.path.join(self.data_dir, data_type)
                
                if not os.path.exists(data_dir):
                    continue
                
                # Copy data files
                for data_file in Path(data_dir).glob("*"):
                    if data_file.is_file():
                        shutil.copy2(
                            data_file,
                            os.path.join(export_dir, data_file.name)
                        )
            
            # Create export file
            if request.format == "zip":
                export_file = os.path.join(
                    self.exports_dir,
                    f"{request.request_id}.zip"
                )
                
                with zipfile.ZipFile(export_file, "w") as zip_file:
                    for file in Path(export_dir).glob("*"):
                        if file.is_file():
                            zip_file.write(
                                file,
                                file.name
                            )
                
                # Remove export directory
                shutil.rmtree(export_dir)
            else:
                export_file = export_dir
            
            # Update request status
            request.status = "completed"
            request.completed_at = datetime.utcnow()
            self.update_request(request)
            
            logger.info(f"Processed export request: {request.request_id}")
            
            return export_file
        except Exception as e:
            # Update request status
            request.status = "failed"
            self.update_request(request)
            
            raise ExportError(f"Error processing request: {str(e)}")
    
    def send_export(
        self,
        request: ExportRequest,
        export_file: str,
        subject: str,
        from_email: str,
        to_email: str
    ) -> None:
        """Send export file.
        
        Args:
            request: Export request
            export_file: Path to export file
            subject: Email subject
            from_email: From email address
            to_email: To email address
            
        Raises:
            ExportError: If sending fails
        """
        try:
            # Create email message
            message = MIMEMultipart()
            message["From"] = from_email
            message["To"] = to_email
            message["Subject"] = subject
            
            # Add message body
            body = f"""
            Your data export request ({request.request_id}) has been completed.
            
            Request details:
            - User ID: {request.user_id}
            - Data types: {", ".join(request.data_types)}
            - Format: {request.format}
            - Created at: {request.created_at.isoformat()}
            - Completed at: {request.completed_at.isoformat()}
            
            The exported data is attached to this email.
            """
            
            message.attach(MIMEText(body, "plain"))
            
            # Add export file
            with open(export_file, "rb") as f:
                attachment = MIMEApplication(f.read())
                attachment.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=os.path.basename(export_file)
                )
                message.attach(attachment)
            
            # Send email
            if self.smtp_host and self.smtp_port:
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    if self.smtp_username and self.smtp_password:
                        server.login(self.smtp_username, self.smtp_password)
                    
                    server.send_message(message)
            else:
                raise ExportError("SMTP settings not configured")
            
            logger.info(f"Sent export file: {export_file}")
        except Exception as e:
            raise ExportError(f"Error sending export: {str(e)}")
    
    def get_request_stats(
        self,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get request statistics.
        
        Args:
            user_id: User ID
            
        Returns:
            Request statistics dictionary
        """
        try:
            stats = {
                "total_requests": 0,
                "status": {
                    "pending": 0,
                    "processing": 0,
                    "completed": 0,
                    "failed": 0
                },
                "data_types": {},
                "formats": {}
            }
            
            # Get requests
            requests = self.get_requests(user_id=user_id)
            
            # Calculate statistics
            for request in requests:
                stats["total_requests"] += 1
                stats["status"][request.status] += 1
                
                # Count data types
                for data_type in request.data_types:
                    if data_type not in stats["data_types"]:
                        stats["data_types"][data_type] = 0
                    
                    stats["data_types"][data_type] += 1
                
                # Count formats
                if request.format not in stats["formats"]:
                    stats["formats"][request.format] = 0
                
                stats["formats"][request.format] += 1
            
            return stats
        except Exception as e:
            raise ExportError(f"Error getting request stats: {str(e)}")
    
    def cleanup_exports(
        self,
        max_age_days: int = 30
    ) -> None:
        """Clean up old exports.
        
        Args:
            max_age_days: Maximum age in days
        """
        try:
            # Get current time
            now = datetime.utcnow()
            
            # Iterate through exports directory
            for export_file in Path(self.exports_dir).glob("*"):
                if not export_file.is_file():
                    continue
                
                # Get file age
                file_age = now - datetime.fromtimestamp(
                    export_file.stat().st_mtime
                )
                
                # Remove old files
                if file_age.days > max_age_days:
                    export_file.unlink()
        except Exception as e:
            logger.error(f"Error cleaning up exports: {str(e)}")
    
    def export_requests(
        self,
        format: str = "json"
    ) -> str:
        """Export requests.
        
        Args:
            format: Export format
            
        Returns:
            Path to exported file
            
        Raises:
            ExportError: If export fails
        """
        try:
            # Create export directory
            export_dir = os.path.join(self.requests_dir, "exports")
            os.makedirs(export_dir, exist_ok=True)
            
            # Create export file path
            export_file = os.path.join(
                export_dir,
                f"requests_{datetime.now().strftime('%Y%m%d')}.{format}"
            )
            
            # Export requests
            if format == "json":
                requests_data = {
                    request.request_id: {
                        "request_id": request.request_id,
                        "user_id": request.user_id,
                        "data_types": request.data_types,
                        "format": request.format,
                        "created_at": request.created_at.isoformat(),
                        "completed_at": request.completed_at.isoformat() if request.completed_at else None,
                        "status": request.status,
                        "metadata": request.metadata
                    }
                    for request in self.get_requests()
                }
                
                with open(export_file, "w") as f:
                    json.dump(requests_data, f, indent=2)
            else:
                raise ExportError(f"Unsupported format: {format}")
            
            return export_file
        except Exception as e:
            raise ExportError(f"Error exporting requests: {str(e)}") 