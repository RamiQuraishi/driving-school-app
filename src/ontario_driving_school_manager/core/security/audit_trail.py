"""
Audit Trail Manager Module

This module provides audit trail functionality with version change tracking.
It handles logging of system events, user actions, and data changes.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Dict, Any, Optional, List, Union, Type, TypeVar
from datetime import datetime
import json
import os
from pathlib import Path
from enum import Enum
from dataclasses import dataclass, asdict
import difflib
import hashlib

logger = logging.getLogger(__name__)

T = TypeVar("T")

class AuditEventType(Enum):
    """Audit event type."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"
    IMPORT = "import"
    CUSTOM = "custom"

class AuditResourceType(Enum):
    """Audit resource type."""
    USER = "user"
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    LESSON = "lesson"
    VEHICLE = "vehicle"
    PAYMENT = "payment"
    REPORT = "report"
    SETTING = "setting"
    SYSTEM = "system"

@dataclass
class AuditEvent:
    """Audit event."""
    event_id: str
    event_type: AuditEventType
    resource_type: AuditResourceType
    resource_id: str
    user_id: str
    timestamp: datetime
    changes: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class VersionChange:
    """Version change."""
    version: int
    timestamp: datetime
    user_id: str
    changes: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

class AuditTrailManager:
    """Audit trail manager."""
    
    def __init__(
        self,
        audit_dir: str = "audit",
        versions_dir: str = "versions"
    ):
        """Initialize audit trail manager.
        
        Args:
            audit_dir: Audit directory
            versions_dir: Versions directory
        """
        self.audit_dir = audit_dir
        self.versions_dir = versions_dir
        
        # Create directories if they don't exist
        os.makedirs(audit_dir, exist_ok=True)
        os.makedirs(versions_dir, exist_ok=True)
    
    def _get_audit_file(
        self,
        resource_type: AuditResourceType,
        resource_id: str
    ) -> str:
        """Get audit file path.
        
        Args:
            resource_type: Resource type
            resource_id: Resource ID
            
        Returns:
            Audit file path
        """
        return os.path.join(
            self.audit_dir,
            resource_type.value,
            f"{resource_id}.json"
        )
    
    def _get_version_file(
        self,
        resource_type: AuditResourceType,
        resource_id: str
    ) -> str:
        """Get version file path.
        
        Args:
            resource_type: Resource type
            resource_id: Resource ID
            
        Returns:
            Version file path
        """
        return os.path.join(
            self.versions_dir,
            resource_type.value,
            f"{resource_id}.json"
        )
    
    def _load_audit_events(
        self,
        resource_type: AuditResourceType,
        resource_id: str
    ) -> List[AuditEvent]:
        """Load audit events.
        
        Args:
            resource_type: Resource type
            resource_id: Resource ID
            
        Returns:
            List of audit events
        """
        audit_file = self._get_audit_file(resource_type, resource_id)
        
        if not os.path.exists(audit_file):
            return []
        
        with open(audit_file, "r") as f:
            data = json.load(f)
        
        return [
            AuditEvent(
                event_id=record["event_id"],
                event_type=AuditEventType(record["event_type"]),
                resource_type=AuditResourceType(record["resource_type"]),
                resource_id=record["resource_id"],
                user_id=record["user_id"],
                timestamp=datetime.fromisoformat(record["timestamp"]),
                changes=record["changes"],
                metadata=record["metadata"]
            )
            for record in data
        ]
    
    def _save_audit_events(
        self,
        resource_type: AuditResourceType,
        resource_id: str,
        events: List[AuditEvent]
    ) -> None:
        """Save audit events.
        
        Args:
            resource_type: Resource type
            resource_id: Resource ID
            events: List of audit events
        """
        audit_file = self._get_audit_file(resource_type, resource_id)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(audit_file), exist_ok=True)
        
        data = [
            {
                "event_id": event.event_id,
                "event_type": event.event_type.value,
                "resource_type": event.resource_type.value,
                "resource_id": event.resource_id,
                "user_id": event.user_id,
                "timestamp": event.timestamp.isoformat(),
                "changes": event.changes,
                "metadata": event.metadata
            }
            for event in events
        ]
        
        with open(audit_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def _load_versions(
        self,
        resource_type: AuditResourceType,
        resource_id: str
    ) -> List[VersionChange]:
        """Load versions.
        
        Args:
            resource_type: Resource type
            resource_id: Resource ID
            
        Returns:
            List of version changes
        """
        version_file = self._get_version_file(resource_type, resource_id)
        
        if not os.path.exists(version_file):
            return []
        
        with open(version_file, "r") as f:
            data = json.load(f)
        
        return [
            VersionChange(
                version=record["version"],
                timestamp=datetime.fromisoformat(record["timestamp"]),
                user_id=record["user_id"],
                changes=record["changes"],
                metadata=record["metadata"]
            )
            for record in data
        ]
    
    def _save_versions(
        self,
        resource_type: AuditResourceType,
        resource_id: str,
        versions: List[VersionChange]
    ) -> None:
        """Save versions.
        
        Args:
            resource_type: Resource type
            resource_id: Resource ID
            versions: List of version changes
        """
        version_file = self._get_version_file(resource_type, resource_id)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(version_file), exist_ok=True)
        
        data = [
            {
                "version": version.version,
                "timestamp": version.timestamp.isoformat(),
                "user_id": version.user_id,
                "changes": version.changes,
                "metadata": version.metadata
            }
            for version in versions
        ]
        
        with open(version_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def _compute_diff(
        self,
        old_data: Dict[str, Any],
        new_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compute diff between old and new data.
        
        Args:
            old_data: Old data
            new_data: New data
            
        Returns:
            Diff dictionary
        """
        diff = {}
        
        # Compare each field
        for key in set(old_data.keys()) | set(new_data.keys()):
            old_value = old_data.get(key)
            new_value = new_data.get(key)
            
            if old_value != new_value:
                diff[key] = {
                    "old": old_value,
                    "new": new_value
                }
        
        return diff
    
    def _compute_hash(
        self,
        data: Dict[str, Any]
    ) -> str:
        """Compute hash of data.
        
        Args:
            data: Data
            
        Returns:
            Hash string
        """
        return hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()
    
    def log_event(
        self,
        event_type: AuditEventType,
        resource_type: AuditResourceType,
        resource_id: str,
        user_id: str,
        changes: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AuditEvent:
        """Log audit event.
        
        Args:
            event_type: Event type
            resource_type: Resource type
            resource_id: Resource ID
            user_id: User ID
            changes: Changes
            metadata: Additional metadata
            
        Returns:
            Created audit event
        """
        # Create event ID
        event_id = f"{event_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create audit event
        event = AuditEvent(
            event_id=event_id,
            event_type=event_type,
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            timestamp=datetime.utcnow(),
            changes=changes,
            metadata=metadata
        )
        
        # Load existing events
        events = self._load_audit_events(resource_type, resource_id)
        
        # Add new event
        events.append(event)
        
        # Save events
        self._save_audit_events(resource_type, resource_id, events)
        
        logger.info(
            f"Logged {event_type.value} event for {resource_type.value} {resource_id}"
        )
        
        return event
    
    def get_events(
        self,
        resource_type: AuditResourceType,
        resource_id: str,
        event_type: Optional[AuditEventType] = None,
        user_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[AuditEvent]:
        """Get audit events.
        
        Args:
            resource_type: Resource type
            resource_id: Resource ID
            event_type: Event type
            user_id: User ID
            start_time: Start time
            end_time: End time
            
        Returns:
            List of audit events
        """
        events = self._load_audit_events(resource_type, resource_id)
        
        # Filter events
        if event_type:
            events = [
                event
                for event in events
                if event.event_type == event_type
            ]
        
        if user_id:
            events = [
                event
                for event in events
                if event.user_id == user_id
            ]
        
        if start_time:
            events = [
                event
                for event in events
                if event.timestamp >= start_time
            ]
        
        if end_time:
            events = [
                event
                for event in events
                if event.timestamp <= end_time
            ]
        
        return events
    
    def track_version(
        self,
        resource_type: AuditResourceType,
        resource_id: str,
        user_id: str,
        old_data: Dict[str, Any],
        new_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> VersionChange:
        """Track version change.
        
        Args:
            resource_type: Resource type
            resource_id: Resource ID
            user_id: User ID
            old_data: Old data
            new_data: New data
            metadata: Additional metadata
            
        Returns:
            Created version change
        """
        # Load existing versions
        versions = self._load_versions(resource_type, resource_id)
        
        # Compute version number
        version = len(versions) + 1
        
        # Compute diff
        changes = self._compute_diff(old_data, new_data)
        
        # Create version change
        version_change = VersionChange(
            version=version,
            timestamp=datetime.utcnow(),
            user_id=user_id,
            changes=changes,
            metadata=metadata
        )
        
        # Add new version
        versions.append(version_change)
        
        # Save versions
        self._save_versions(resource_type, resource_id, versions)
        
        logger.info(
            f"Tracked version {version} for {resource_type.value} {resource_id}"
        )
        
        return version_change
    
    def get_versions(
        self,
        resource_type: AuditResourceType,
        resource_id: str,
        user_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[VersionChange]:
        """Get version changes.
        
        Args:
            resource_type: Resource type
            resource_id: Resource ID
            user_id: User ID
            start_time: Start time
            end_time: End time
            
        Returns:
            List of version changes
        """
        versions = self._load_versions(resource_type, resource_id)
        
        # Filter versions
        if user_id:
            versions = [
                version
                for version in versions
                if version.user_id == user_id
            ]
        
        if start_time:
            versions = [
                version
                for version in versions
                if version.timestamp >= start_time
            ]
        
        if end_time:
            versions = [
                version
                for version in versions
                if version.timestamp <= end_time
            ]
        
        return versions
    
    def get_version(
        self,
        resource_type: AuditResourceType,
        resource_id: str,
        version: int
    ) -> Optional[VersionChange]:
        """Get version change.
        
        Args:
            resource_type: Resource type
            resource_id: Resource ID
            version: Version number
            
        Returns:
            Version change if found, None otherwise
        """
        versions = self._load_versions(resource_type, resource_id)
        
        for version_change in versions:
            if version_change.version == version:
                return version_change
        
        return None
    
    def get_audit_stats(
        self
    ) -> Dict[str, Any]:
        """Get audit statistics.
        
        Returns:
            Audit statistics dictionary
        """
        stats = {
            "total_events": 0,
            "event_types": {
                event_type.value: 0
                for event_type in AuditEventType
            },
            "resource_types": {
                resource_type.value: 0
                for resource_type in AuditResourceType
            },
            "total_versions": 0,
            "resource_versions": {}
        }
        
        # Iterate through audit files
        for audit_file in Path(self.audit_dir).glob("**/*.json"):
            with open(audit_file, "r") as f:
                data = json.load(f)
            
            stats["total_events"] += len(data)
            
            # Count event types
            for record in data:
                stats["event_types"][record["event_type"]] += 1
                stats["resource_types"][record["resource_type"]] += 1
        
        # Iterate through version files
        for version_file in Path(self.versions_dir).glob("**/*.json"):
            with open(version_file, "r") as f:
                data = json.load(f)
            
            stats["total_versions"] += len(data)
            
            # Count resource versions
            resource_type = version_file.parent.name
            resource_id = version_file.stem
            
            if resource_type not in stats["resource_versions"]:
                stats["resource_versions"][resource_type] = {}
            
            stats["resource_versions"][resource_type][resource_id] = len(data)
        
        return stats
    
    def export_audit(
        self,
        format: str = "json"
    ) -> str:
        """Export audit trail.
        
        Args:
            format: Export format
            
        Returns:
            Path to exported file
            
        Raises:
            ValueError: If format is not supported
        """
        if format != "json":
            raise ValueError(f"Unsupported format: {format}")
        
        # Create export directory
        export_dir = os.path.join(self.audit_dir, "exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # Create export file path
        export_file = os.path.join(
            export_dir,
            f"audit_{datetime.now().strftime('%Y%m%d')}.{format}"
        )
        
        # Export audit trail
        audit_data = {}
        
        for audit_file in Path(self.audit_dir).glob("**/*.json"):
            if audit_file.name == "exports":
                continue
            
            with open(audit_file, "r") as f:
                data = json.load(f)
            
            resource_type = audit_file.parent.name
            resource_id = audit_file.stem
            
            if resource_type not in audit_data:
                audit_data[resource_type] = {}
            
            audit_data[resource_type][resource_id] = data
        
        with open(export_file, "w") as f:
            json.dump(audit_data, f, indent=2)
        
        return export_file
    
    def export_versions(
        self,
        format: str = "json"
    ) -> str:
        """Export versions.
        
        Args:
            format: Export format
            
        Returns:
            Path to exported file
            
        Raises:
            ValueError: If format is not supported
        """
        if format != "json":
            raise ValueError(f"Unsupported format: {format}")
        
        # Create export directory
        export_dir = os.path.join(self.versions_dir, "exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # Create export file path
        export_file = os.path.join(
            export_dir,
            f"versions_{datetime.now().strftime('%Y%m%d')}.{format}"
        )
        
        # Export versions
        versions_data = {}
        
        for version_file in Path(self.versions_dir).glob("**/*.json"):
            if version_file.name == "exports":
                continue
            
            with open(version_file, "r") as f:
                data = json.load(f)
            
            resource_type = version_file.parent.name
            resource_id = version_file.stem
            
            if resource_type not in versions_data:
                versions_data[resource_type] = {}
            
            versions_data[resource_type][resource_id] = data
        
        with open(export_file, "w") as f:
            json.dump(versions_data, f, indent=2)
        
        return export_file
    
    def cleanup_audit(
        self,
        max_age_days: int = 365
    ) -> None:
        """Clean up old audit events.
        
        Args:
            max_age_days: Maximum age in days
        """
        # Get current time
        now = datetime.utcnow()
        
        # Iterate through audit files
        for audit_file in Path(self.audit_dir).glob("**/*.json"):
            if audit_file.name == "exports":
                continue
            
            with open(audit_file, "r") as f:
                data = json.load(f)
            
            # Filter old events
            data = [
                record
                for record in data
                if (now - datetime.fromisoformat(record["timestamp"])).days <= max_age_days
            ]
            
            # Save filtered events
            with open(audit_file, "w") as f:
                json.dump(data, f, indent=2)
    
    def cleanup_versions(
        self,
        max_age_days: int = 365
    ) -> None:
        """Clean up old versions.
        
        Args:
            max_age_days: Maximum age in days
        """
        # Get current time
        now = datetime.utcnow()
        
        # Iterate through version files
        for version_file in Path(self.versions_dir).glob("**/*.json"):
            if version_file.name == "exports":
                continue
            
            with open(version_file, "r") as f:
                data = json.load(f)
            
            # Filter old versions
            data = [
                record
                for record in data
                if (now - datetime.fromisoformat(record["timestamp"])).days <= max_age_days
            ]
            
            # Save filtered versions
            with open(version_file, "w") as f:
                json.dump(data, f, indent=2) 