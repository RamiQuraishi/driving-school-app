"""
Privacy Officer Module

This module provides privacy officer functionality for PIPEDA compliance.
It handles privacy officer responsibilities, compliance monitoring, and reporting.

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

class PrivacyOfficerError(Exception):
    """Privacy officer error."""
    pass

class ComplianceReport:
    """Compliance report."""
    
    def __init__(
        self,
        report_id: str,
        title: str,
        description: str,
        findings: List[Dict[str, Any]],
        recommendations: List[str],
        created_at: datetime,
        updated_at: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Initialize compliance report.
        
        Args:
            report_id: Report ID
            title: Report title
            description: Report description
            findings: List of findings
            recommendations: List of recommendations
            created_at: Creation timestamp
            updated_at: Update timestamp
            metadata: Additional metadata
        """
        self.report_id = report_id
        self.title = title
        self.description = description
        self.findings = findings
        self.recommendations = recommendations
        self.created_at = created_at
        self.updated_at = updated_at
        self.metadata = metadata or {}

class PrivacyOfficer:
    """Privacy officer."""
    
    def __init__(
        self,
        reports_dir: str = "reports",
        templates_dir: str = "templates",
        smtp_host: Optional[str] = None,
        smtp_port: Optional[int] = None,
        smtp_username: Optional[str] = None,
        smtp_password: Optional[str] = None
    ):
        """Initialize privacy officer.
        
        Args:
            reports_dir: Reports directory
            templates_dir: Templates directory
            smtp_host: SMTP host
            smtp_port: SMTP port
            smtp_username: SMTP username
            smtp_password: SMTP password
        """
        self.reports_dir = reports_dir
        self.templates_dir = templates_dir
        
        # Create directories if they don't exist
        os.makedirs(reports_dir, exist_ok=True)
        os.makedirs(templates_dir, exist_ok=True)
        
        # Initialize SMTP settings
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        
        # Load report templates
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load report templates.
        
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
        """Add report template.
        
        Args:
            name: Template name
            content: Template content
            
        Raises:
            PrivacyOfficerError: If template already exists
        """
        if name in self.templates:
            raise PrivacyOfficerError(f"Template already exists: {name}")
        
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
            
            logger.info(f"Added report template: {name}")
        except Exception as e:
            raise PrivacyOfficerError(f"Error adding template: {str(e)}")
    
    def update_template(
        self,
        name: str,
        content: str
    ) -> None:
        """Update report template.
        
        Args:
            name: Template name
            content: Template content
            
        Raises:
            PrivacyOfficerError: If template doesn't exist
        """
        if name not in self.templates:
            raise PrivacyOfficerError(f"Template doesn't exist: {name}")
        
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
            
            logger.info(f"Updated report template: {name}")
        except Exception as e:
            raise PrivacyOfficerError(f"Error updating template: {str(e)}")
    
    def remove_template(
        self,
        name: str
    ) -> None:
        """Remove report template.
        
        Args:
            name: Template name
            
        Raises:
            PrivacyOfficerError: If template doesn't exist
        """
        if name not in self.templates:
            raise PrivacyOfficerError(f"Template doesn't exist: {name}")
        
        try:
            # Remove template file
            template_file = os.path.join(
                self.templates_dir,
                f"{name}.txt"
            )
            
            os.remove(template_file)
            
            # Remove template from dictionary
            del self.templates[name]
            
            logger.info(f"Removed report template: {name}")
        except Exception as e:
            raise PrivacyOfficerError(f"Error removing template: {str(e)}")
    
    def get_template(
        self,
        name: str
    ) -> Optional[str]:
        """Get report template.
        
        Args:
            name: Template name
            
        Returns:
            Template content if found, None otherwise
        """
        return self.templates.get(name)
    
    def get_templates(self) -> Dict[str, str]:
        """Get report templates.
        
        Returns:
            Dictionary of templates by name
        """
        return self.templates.copy()
    
    def create_report(
        self,
        report: ComplianceReport
    ) -> None:
        """Create compliance report.
        
        Args:
            report: Compliance report
            
        Raises:
            PrivacyOfficerError: If report already exists
        """
        try:
            # Create report file
            report_file = os.path.join(
                self.reports_dir,
                f"{report.report_id}.json"
            )
            
            # Check if report file exists
            if os.path.exists(report_file):
                raise PrivacyOfficerError(f"Report already exists: {report.report_id}")
            
            # Write report data
            report_data = {
                "report_id": report.report_id,
                "title": report.title,
                "description": report.description,
                "findings": report.findings,
                "recommendations": report.recommendations,
                "created_at": report.created_at.isoformat(),
                "updated_at": report.updated_at.isoformat() if report.updated_at else None,
                "metadata": report.metadata
            }
            
            with open(report_file, "w") as f:
                json.dump(report_data, f, indent=2)
            
            logger.info(f"Created compliance report: {report.report_id}")
        except Exception as e:
            raise PrivacyOfficerError(f"Error creating report: {str(e)}")
    
    def update_report(
        self,
        report: ComplianceReport
    ) -> None:
        """Update compliance report.
        
        Args:
            report: Compliance report
            
        Raises:
            PrivacyOfficerError: If report doesn't exist
        """
        try:
            # Get report file path
            report_file = os.path.join(
                self.reports_dir,
                f"{report.report_id}.json"
            )
            
            # Check if report file exists
            if not os.path.exists(report_file):
                raise PrivacyOfficerError(f"Report doesn't exist: {report.report_id}")
            
            # Write report data
            report_data = {
                "report_id": report.report_id,
                "title": report.title,
                "description": report.description,
                "findings": report.findings,
                "recommendations": report.recommendations,
                "created_at": report.created_at.isoformat(),
                "updated_at": report.updated_at.isoformat() if report.updated_at else None,
                "metadata": report.metadata
            }
            
            with open(report_file, "w") as f:
                json.dump(report_data, f, indent=2)
            
            logger.info(f"Updated compliance report: {report.report_id}")
        except Exception as e:
            raise PrivacyOfficerError(f"Error updating report: {str(e)}")
    
    def get_report(
        self,
        report_id: str
    ) -> Optional[ComplianceReport]:
        """Get compliance report.
        
        Args:
            report_id: Report ID
            
        Returns:
            Compliance report if found, None otherwise
        """
        try:
            # Get report file path
            report_file = os.path.join(
                self.reports_dir,
                f"{report_id}.json"
            )
            
            # Check if report file exists
            if not os.path.exists(report_file):
                return None
            
            # Read report data
            with open(report_file, "r") as f:
                report_data = json.load(f)
            
            # Create compliance report
            return ComplianceReport(
                report_id=report_data["report_id"],
                title=report_data["title"],
                description=report_data["description"],
                findings=report_data["findings"],
                recommendations=report_data["recommendations"],
                created_at=datetime.fromisoformat(report_data["created_at"]),
                updated_at=datetime.fromisoformat(report_data["updated_at"]) if report_data["updated_at"] else None,
                metadata=report_data["metadata"]
            )
        except Exception as e:
            logger.error(f"Error getting report: {str(e)}")
            return None
    
    def get_reports(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[ComplianceReport]:
        """Get compliance reports.
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            List of compliance reports
        """
        reports = []
        
        try:
            # Iterate through reports directory
            for report_file in Path(self.reports_dir).glob("*.json"):
                with open(report_file, "r") as f:
                    report_data = json.load(f)
                
                # Filter by date range
                created_at = datetime.fromisoformat(report_data["created_at"])
                
                if start_date and created_at < start_date:
                    continue
                
                if end_date and created_at > end_date:
                    continue
                
                # Create compliance report
                report = ComplianceReport(
                    report_id=report_data["report_id"],
                    title=report_data["title"],
                    description=report_data["description"],
                    findings=report_data["findings"],
                    recommendations=report_data["recommendations"],
                    created_at=created_at,
                    updated_at=datetime.fromisoformat(report_data["updated_at"]) if report_data["updated_at"] else None,
                    metadata=report_data["metadata"]
                )
                
                reports.append(report)
        except Exception as e:
            logger.error(f"Error getting reports: {str(e)}")
        
        return reports
    
    def generate_report(
        self,
        template_name: str,
        title: str,
        description: str,
        findings: List[Dict[str, Any]],
        recommendations: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> ComplianceReport:
        """Generate compliance report.
        
        Args:
            template_name: Template name
            title: Report title
            description: Report description
            findings: List of findings
            recommendations: List of recommendations
            metadata: Additional metadata
            
        Returns:
            Compliance report
            
        Raises:
            PrivacyOfficerError: If template doesn't exist
        """
        try:
            # Get template
            template = self.get_template(template_name)
            
            if not template:
                raise PrivacyOfficerError(f"Template doesn't exist: {template_name}")
            
            # Create report ID
            report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create compliance report
            report = ComplianceReport(
                report_id=report_id,
                title=title,
                description=description,
                findings=findings,
                recommendations=recommendations,
                created_at=datetime.utcnow(),
                metadata=metadata
            )
            
            # Create report
            self.create_report(report)
            
            return report
        except Exception as e:
            raise PrivacyOfficerError(f"Error generating report: {str(e)}")
    
    def send_report(
        self,
        report: ComplianceReport,
        template_name: str,
        subject: str,
        from_email: str,
        to_emails: List[str]
    ) -> None:
        """Send compliance report.
        
        Args:
            report: Compliance report
            template_name: Template name
            subject: Email subject
            from_email: From email address
            to_emails: To email addresses
            
        Raises:
            PrivacyOfficerError: If sending fails
        """
        try:
            # Get template
            template = self.get_template(template_name)
            
            if not template:
                raise PrivacyOfficerError(f"Template doesn't exist: {template_name}")
            
            # Format template
            content = template.format(
                report_id=report.report_id,
                title=report.title,
                description=report.description,
                findings="\n".join(
                    f"- {finding['description']}"
                    for finding in report.findings
                ),
                recommendations="\n".join(
                    f"- {recommendation}"
                    for recommendation in report.recommendations
                ),
                created_at=report.created_at.isoformat()
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
                raise PrivacyOfficerError("SMTP settings not configured")
            
            logger.info(f"Sent compliance report: {report.report_id}")
        except Exception as e:
            raise PrivacyOfficerError(f"Error sending report: {str(e)}")
    
    def get_report_stats(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get report statistics.
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            Report statistics dictionary
        """
        try:
            stats = {
                "total_reports": 0,
                "findings": {
                    "total": 0,
                    "by_severity": {
                        "low": 0,
                        "medium": 0,
                        "high": 0,
                        "critical": 0
                    }
                },
                "recommendations": {
                    "total": 0,
                    "implemented": 0
                }
            }
            
            # Get reports
            reports = self.get_reports(start_date, end_date)
            
            # Calculate statistics
            for report in reports:
                stats["total_reports"] += 1
                
                # Count findings
                for finding in report.findings:
                    stats["findings"]["total"] += 1
                    stats["findings"]["by_severity"][finding["severity"]] += 1
                
                # Count recommendations
                stats["recommendations"]["total"] += len(report.recommendations)
                
                if report.metadata.get("recommendations_implemented"):
                    stats["recommendations"]["implemented"] += len(
                        report.metadata["recommendations_implemented"]
                    )
            
            return stats
        except Exception as e:
            raise PrivacyOfficerError(f"Error getting report stats: {str(e)}")
    
    def export_reports(
        self,
        format: str = "json"
    ) -> str:
        """Export compliance reports.
        
        Args:
            format: Export format
            
        Returns:
            Path to exported file
            
        Raises:
            PrivacyOfficerError: If export fails
        """
        try:
            # Create export directory
            export_dir = os.path.join(self.reports_dir, "exports")
            os.makedirs(export_dir, exist_ok=True)
            
            # Create export file path
            export_file = os.path.join(
                export_dir,
                f"reports_{datetime.now().strftime('%Y%m%d')}.{format}"
            )
            
            # Export reports
            if format == "json":
                reports_data = {
                    report.report_id: {
                        "report_id": report.report_id,
                        "title": report.title,
                        "description": report.description,
                        "findings": report.findings,
                        "recommendations": report.recommendations,
                        "created_at": report.created_at.isoformat(),
                        "updated_at": report.updated_at.isoformat() if report.updated_at else None,
                        "metadata": report.metadata
                    }
                    for report in self.get_reports()
                }
                
                with open(export_file, "w") as f:
                    json.dump(reports_data, f, indent=2)
            else:
                raise PrivacyOfficerError(f"Unsupported format: {format}")
            
            return export_file
        except Exception as e:
            raise PrivacyOfficerError(f"Error exporting reports: {str(e)}") 