"""
Breach Notification Manager Module

This module provides breach notification management functionality for PIPEDA compliance.
It handles data breach detection, notification, and reporting.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import json
import os
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

class BreachError(Exception):
    """Breach error."""
    pass

class BreachNotification:
    """Breach notification."""
    
    def __init__(
        self,
        breach_id: str,
        description: str,
        severity: str,
        affected_data: List[str],
        affected_users: List[str],
        detected_at: datetime,
        reported_at: Optional[datetime] = None,
        resolved_at: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Initialize breach notification.
        
        Args:
            breach_id: Breach ID
            description: Breach description
            severity: Breach severity (low, medium, high, critical)
            affected_data: List of affected data types
            affected_users: List of affected user IDs
            detected_at: Detection timestamp
            reported_at: Report timestamp
            resolved_at: Resolution timestamp
            metadata: Additional metadata
        """
        self.breach_id = breach_id
        self.description = description
        self.severity = severity
        self.affected_data = affected_data
        self.affected_users = affected_users
        self.detected_at = detected_at
        self.reported_at = reported_at
        self.resolved_at = resolved_at
        self.metadata = metadata or {}

class BreachNotificationManager:
    """Breach notification manager."""
    
    def __init__(
        self,
        breaches_dir: str = "breaches",
        templates_dir: str = "templates",
        smtp_host: Optional[str] = None,
        smtp_port: Optional[int] = None,
        smtp_username: Optional[str] = None,
        smtp_password: Optional[str] = None
    ):
        """Initialize breach notification manager.
        
        Args:
            breaches_dir: Breaches directory
            templates_dir: Templates directory
            smtp_host: SMTP host
            smtp_port: SMTP port
            smtp_username: SMTP username
            smtp_password: SMTP password
        """
        self.breaches_dir = breaches_dir
        self.templates_dir = templates_dir
        
        # Create directories if they don't exist
        os.makedirs(breaches_dir, exist_ok=True)
        os.makedirs(templates_dir, exist_ok=True)
        
        # Initialize SMTP settings
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        
        # Load breach templates
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load breach templates.
        
        Returns:
            Dictionary of templates by name
        """
        templates = {}
        
        try:
            # Iterate through templates directory
            for template_file in Path(self.templates_dir).glob("*.txt"):
                with open(template_file, "r") as f:
                    templates[template_file.stem] = f.read()
        except Exception as e:
            logger.error(f"Error loading templates: {str(e)}")
        
        return templates
    
    def add_template(
        self,
        name: str,
        content: str
    ) -> None:
        """Add breach template.
        
        Args:
            name: Template name
            content: Template content
            
        Raises:
            BreachError: If template already exists
        """
        if name in self.templates:
            raise BreachError(f"Template already exists: {name}")
        
        try:
            # Create template file
            template_file = os.path.join(
                self.templates_dir,
                f"{name}.txt"
            )
            
            # Write template content
            with open(template_file, "w") as f:
                f.write(content)
            
            # Add template to dictionary
            self.templates[name] = content
            
            logger.info(f"Added breach template: {name}")
        except Exception as e:
            raise BreachError(f"Error adding template: {str(e)}")
    
    def update_template(
        self,
        name: str,
        content: str
    ) -> None:
        """Update breach template.
        
        Args:
            name: Template name
            content: Template content
            
        Raises:
            BreachError: If template doesn't exist
        """
        if name not in self.templates:
            raise BreachError(f"Template doesn't exist: {name}")
        
        try:
            # Update template file
            template_file = os.path.join(
                self.templates_dir,
                f"{name}.txt"
            )
            
            # Write template content
            with open(template_file, "w") as f:
                f.write(content)
            
            # Update template in dictionary
            self.templates[name] = content
            
            logger.info(f"Updated breach template: {name}")
        except Exception as e:
            raise BreachError(f"Error updating template: {str(e)}")
    
    def remove_template(
        self,
        name: str
    ) -> None:
        """Remove breach template.
        
        Args:
            name: Template name
            
        Raises:
            BreachError: If template doesn't exist
        """
        if name not in self.templates:
            raise BreachError(f"Template doesn't exist: {name}")
        
        try:
            # Remove template file
            template_file = os.path.join(
                self.templates_dir,
                f"{name}.txt"
            )
            
            os.remove(template_file)
            
            # Remove template from dictionary
            del self.templates[name]
            
            logger.info(f"Removed breach template: {name}")
        except Exception as e:
            raise BreachError(f"Error removing template: {str(e)}")
    
    def get_template(
        self,
        name: str
    ) -> Optional[str]:
        """Get breach template.
        
        Args:
            name: Template name
            
        Returns:
            Template content if found, None otherwise
        """
        return self.templates.get(name)
    
    def get_templates(self) -> Dict[str, str]:
        """Get breach templates.
        
        Returns:
            Dictionary of templates by name
        """
        return self.templates.copy()
    
    def report_breach(
        self,
        breach: BreachNotification
    ) -> None:
        """Report data breach.
        
        Args:
            breach: Breach notification
            
        Raises:
            BreachError: If breach already exists
        """
        try:
            # Create breach file
            breach_file = os.path.join(
                self.breaches_dir,
                f"{breach.breach_id}.json"
            )
            
            # Check if breach file exists
            if os.path.exists(breach_file):
                raise BreachError(f"Breach already exists: {breach.breach_id}")
            
            # Write breach data
            breach_data = {
                "breach_id": breach.breach_id,
                "description": breach.description,
                "severity": breach.severity,
                "affected_data": breach.affected_data,
                "affected_users": breach.affected_users,
                "detected_at": breach.detected_at.isoformat(),
                "reported_at": breach.reported_at.isoformat() if breach.reported_at else None,
                "resolved_at": breach.resolved_at.isoformat() if breach.resolved_at else None,
                "metadata": breach.metadata
            }
            
            with open(breach_file, "w") as f:
                json.dump(breach_data, f, indent=2)
            
            logger.info(f"Reported breach: {breach.breach_id}")
        except Exception as e:
            raise BreachError(f"Error reporting breach: {str(e)}")
    
    def update_breach(
        self,
        breach: BreachNotification
    ) -> None:
        """Update data breach.
        
        Args:
            breach: Breach notification
            
        Raises:
            BreachError: If breach doesn't exist
        """
        try:
            # Get breach file path
            breach_file = os.path.join(
                self.breaches_dir,
                f"{breach.breach_id}.json"
            )
            
            # Check if breach file exists
            if not os.path.exists(breach_file):
                raise BreachError(f"Breach doesn't exist: {breach.breach_id}")
            
            # Write breach data
            breach_data = {
                "breach_id": breach.breach_id,
                "description": breach.description,
                "severity": breach.severity,
                "affected_data": breach.affected_data,
                "affected_users": breach.affected_users,
                "detected_at": breach.detected_at.isoformat(),
                "reported_at": breach.reported_at.isoformat() if breach.reported_at else None,
                "resolved_at": breach.resolved_at.isoformat() if breach.resolved_at else None,
                "metadata": breach.metadata
            }
            
            with open(breach_file, "w") as f:
                json.dump(breach_data, f, indent=2)
            
            logger.info(f"Updated breach: {breach.breach_id}")
        except Exception as e:
            raise BreachError(f"Error updating breach: {str(e)}")
    
    def get_breach(
        self,
        breach_id: str
    ) -> Optional[BreachNotification]:
        """Get data breach.
        
        Args:
            breach_id: Breach ID
            
        Returns:
            Breach notification if found, None otherwise
        """
        try:
            # Get breach file path
            breach_file = os.path.join(
                self.breaches_dir,
                f"{breach_id}.json"
            )
            
            # Check if breach file exists
            if not os.path.exists(breach_file):
                return None
            
            # Read breach data
            with open(breach_file, "r") as f:
                breach_data = json.load(f)
            
            # Create breach notification
            return BreachNotification(
                breach_id=breach_data["breach_id"],
                description=breach_data["description"],
                severity=breach_data["severity"],
                affected_data=breach_data["affected_data"],
                affected_users=breach_data["affected_users"],
                detected_at=datetime.fromisoformat(breach_data["detected_at"]),
                reported_at=datetime.fromisoformat(breach_data["reported_at"]) if breach_data["reported_at"] else None,
                resolved_at=datetime.fromisoformat(breach_data["resolved_at"]) if breach_data["resolved_at"] else None,
                metadata=breach_data["metadata"]
            )
        except Exception as e:
            logger.error(f"Error getting breach: {str(e)}")
            return None
    
    def get_breaches(
        self,
        severity: Optional[str] = None,
        resolved: Optional[bool] = None
    ) -> List[BreachNotification]:
        """Get data breaches.
        
        Args:
            severity: Breach severity
            resolved: Whether breach is resolved
            
        Returns:
            List of breach notifications
        """
        breaches = []
        
        try:
            # Iterate through breaches directory
            for breach_file in Path(self.breaches_dir).glob("*.json"):
                with open(breach_file, "r") as f:
                    breach_data = json.load(f)
                
                # Filter by severity
                if severity and breach_data["severity"] != severity:
                    continue
                
                # Filter by resolution status
                if resolved is not None:
                    is_resolved = breach_data["resolved_at"] is not None
                    
                    if resolved != is_resolved:
                        continue
                
                # Create breach notification
                breach = BreachNotification(
                    breach_id=breach_data["breach_id"],
                    description=breach_data["description"],
                    severity=breach_data["severity"],
                    affected_data=breach_data["affected_data"],
                    affected_users=breach_data["affected_users"],
                    detected_at=datetime.fromisoformat(breach_data["detected_at"]),
                    reported_at=datetime.fromisoformat(breach_data["reported_at"]) if breach_data["reported_at"] else None,
                    resolved_at=datetime.fromisoformat(breach_data["resolved_at"]) if breach_data["resolved_at"] else None,
                    metadata=breach_data["metadata"]
                )
                
                breaches.append(breach)
        except Exception as e:
            logger.error(f"Error getting breaches: {str(e)}")
        
        return breaches
    
    def notify_users(
        self,
        breach: BreachNotification,
        template_name: str,
        subject: str,
        from_email: str,
        to_emails: List[str]
    ) -> None:
        """Notify users about data breach.
        
        Args:
            breach: Breach notification
            template_name: Template name
            subject: Email subject
            from_email: From email address
            to_emails: To email addresses
            
        Raises:
            BreachError: If notification fails
        """
        try:
            # Get template
            template = self.get_template(template_name)
            
            if not template:
                raise BreachError(f"Template doesn't exist: {template_name}")
            
            # Format template
            content = template.format(
                breach_id=breach.breach_id,
                description=breach.description,
                severity=breach.severity,
                affected_data=", ".join(breach.affected_data),
                detected_at=breach.detected_at.isoformat()
            )
            
            # Create email message
            message = MIMEMultipart()
            message["From"] = from_email
            message["To"] = ", ".join(to_emails)
            message["Subject"] = subject
            
            message.attach(MIMEText(content, "plain"))
            
            # Send email
            if self.smtp_host and self.smtp_port:
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    if self.smtp_username and self.smtp_password:
                        server.login(self.smtp_username, self.smtp_password)
                    
                    server.send_message(message)
            else:
                raise BreachError("SMTP settings not configured")
            
            logger.info(f"Notified users about breach: {breach.breach_id}")
        except Exception as e:
            raise BreachError(f"Error notifying users: {str(e)}")
    
    def get_breach_stats(
        self,
        severity: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get breach statistics.
        
        Args:
            severity: Breach severity
            
        Returns:
            Breach statistics dictionary
        """
        try:
            stats = {
                "total_breaches": 0,
                "resolved_breaches": 0,
                "severities": {
                    "low": 0,
                    "medium": 0,
                    "high": 0,
                    "critical": 0
                },
                "affected_users": 0,
                "affected_data": set()
            }
            
            # Get breaches
            breaches = self.get_breaches(severity=severity)
            
            # Calculate statistics
            for breach in breaches:
                stats["total_breaches"] += 1
                
                if breach.resolved_at:
                    stats["resolved_breaches"] += 1
                
                stats["severities"][breach.severity] += 1
                stats["affected_users"] += len(breach.affected_users)
                stats["affected_data"].update(breach.affected_data)
            
            # Convert affected data set to list
            stats["affected_data"] = list(stats["affected_data"])
            
            return stats
        except Exception as e:
            raise BreachError(f"Error getting breach stats: {str(e)}")
    
    def export_breaches(
        self,
        format: str = "json"
    ) -> str:
        """Export data breaches.
        
        Args:
            format: Export format
            
        Returns:
            Path to exported file
            
        Raises:
            BreachError: If export fails
        """
        try:
            # Create export directory
            export_dir = os.path.join(self.breaches_dir, "exports")
            os.makedirs(export_dir, exist_ok=True)
            
            # Create export file path
            export_file = os.path.join(
                export_dir,
                f"breaches_{datetime.now().strftime('%Y%m%d')}.{format}"
            )
            
            # Export breaches
            if format == "json":
                breaches_data = {
                    breach.breach_id: {
                        "breach_id": breach.breach_id,
                        "description": breach.description,
                        "severity": breach.severity,
                        "affected_data": breach.affected_data,
                        "affected_users": breach.affected_users,
                        "detected_at": breach.detected_at.isoformat(),
                        "reported_at": breach.reported_at.isoformat() if breach.reported_at else None,
                        "resolved_at": breach.resolved_at.isoformat() if breach.resolved_at else None,
                        "metadata": breach.metadata
                    }
                    for breach in self.get_breaches()
                }
                
                with open(export_file, "w") as f:
                    json.dump(breaches_data, f, indent=2)
            else:
                raise BreachError(f"Unsupported format: {format}")
            
            return export_file
        except Exception as e:
            raise BreachError(f"Error exporting breaches: {str(e)}") 