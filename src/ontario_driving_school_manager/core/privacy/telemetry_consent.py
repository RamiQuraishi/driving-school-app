"""
Telemetry Consent Manager Module

This module provides telemetry consent management functionality for PIPEDA compliance.
It handles user consent for telemetry data collection, tracking, and management.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import json
import os
from pathlib import Path
from enum import Enum
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

class ConsentStatus(Enum):
    """Consent status."""
    GRANTED = "granted"
    DENIED = "denied"
    PENDING = "pending"
    WITHDRAWN = "withdrawn"

class TelemetryType(Enum):
    """Telemetry type."""
    USAGE = "usage"
    PERFORMANCE = "performance"
    ERROR = "error"
    CUSTOM = "custom"

@dataclass
class ConsentRecord:
    """Consent record."""
    user_id: str
    telemetry_type: TelemetryType
    status: ConsentStatus
    granted_at: Optional[datetime] = None
    withdrawn_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

class TelemetryConsentManager:
    """Telemetry consent manager."""
    
    def __init__(
        self,
        consent_dir: str = "consents",
        default_consent: bool = False
    ):
        """Initialize telemetry consent manager.
        
        Args:
            consent_dir: Consent directory
            default_consent: Default consent status
        """
        self.consent_dir = consent_dir
        self.default_consent = default_consent
        
        # Create consent directory if it doesn't exist
        os.makedirs(consent_dir, exist_ok=True)
    
    def _get_consent_file(
        self,
        user_id: str
    ) -> str:
        """Get consent file path.
        
        Args:
            user_id: User ID
            
        Returns:
            Consent file path
        """
        return os.path.join(
            self.consent_dir,
            f"{user_id}.json"
        )
    
    def _load_consents(
        self,
        user_id: str
    ) -> Dict[str, ConsentRecord]:
        """Load user consents.
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary of consent records
        """
        consent_file = self._get_consent_file(user_id)
        
        if not os.path.exists(consent_file):
            return {}
        
        with open(consent_file, "r") as f:
            data = json.load(f)
        
        return {
            telemetry_type: ConsentRecord(
                user_id=record["user_id"],
                telemetry_type=TelemetryType(record["telemetry_type"]),
                status=ConsentStatus(record["status"]),
                granted_at=datetime.fromisoformat(record["granted_at"]) if record["granted_at"] else None,
                withdrawn_at=datetime.fromisoformat(record["withdrawn_at"]) if record["withdrawn_at"] else None,
                metadata=record["metadata"]
            )
            for telemetry_type, record in data.items()
        }
    
    def _save_consents(
        self,
        user_id: str,
        consents: Dict[str, ConsentRecord]
    ) -> None:
        """Save user consents.
        
        Args:
            user_id: User ID
            consents: Dictionary of consent records
        """
        consent_file = self._get_consent_file(user_id)
        
        data = {
            telemetry_type: {
                "user_id": record.user_id,
                "telemetry_type": record.telemetry_type.value,
                "status": record.status.value,
                "granted_at": record.granted_at.isoformat() if record.granted_at else None,
                "withdrawn_at": record.withdrawn_at.isoformat() if record.withdrawn_at else None,
                "metadata": record.metadata
            }
            for telemetry_type, record in consents.items()
        }
        
        with open(consent_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def get_consent(
        self,
        user_id: str,
        telemetry_type: TelemetryType
    ) -> ConsentStatus:
        """Get user consent status.
        
        Args:
            user_id: User ID
            telemetry_type: Telemetry type
            
        Returns:
            Consent status
        """
        consents = self._load_consents(user_id)
        
        if telemetry_type.value not in consents:
            return ConsentStatus.GRANTED if self.default_consent else ConsentStatus.DENIED
        
        return consents[telemetry_type.value].status
    
    def grant_consent(
        self,
        user_id: str,
        telemetry_type: TelemetryType,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Grant user consent.
        
        Args:
            user_id: User ID
            telemetry_type: Telemetry type
            metadata: Additional metadata
        """
        consents = self._load_consents(user_id)
        
        consents[telemetry_type.value] = ConsentRecord(
            user_id=user_id,
            telemetry_type=telemetry_type,
            status=ConsentStatus.GRANTED,
            granted_at=datetime.utcnow(),
            metadata=metadata
        )
        
        self._save_consents(user_id, consents)
        
        logger.info(
            f"Granted consent for user {user_id} and telemetry type {telemetry_type.value}"
        )
    
    def deny_consent(
        self,
        user_id: str,
        telemetry_type: TelemetryType,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Deny user consent.
        
        Args:
            user_id: User ID
            telemetry_type: Telemetry type
            metadata: Additional metadata
        """
        consents = self._load_consents(user_id)
        
        consents[telemetry_type.value] = ConsentRecord(
            user_id=user_id,
            telemetry_type=telemetry_type,
            status=ConsentStatus.DENIED,
            metadata=metadata
        )
        
        self._save_consents(user_id, consents)
        
        logger.info(
            f"Denied consent for user {user_id} and telemetry type {telemetry_type.value}"
        )
    
    def withdraw_consent(
        self,
        user_id: str,
        telemetry_type: TelemetryType,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Withdraw user consent.
        
        Args:
            user_id: User ID
            telemetry_type: Telemetry type
            metadata: Additional metadata
        """
        consents = self._load_consents(user_id)
        
        if telemetry_type.value not in consents:
            return
        
        consents[telemetry_type.value] = ConsentRecord(
            user_id=user_id,
            telemetry_type=telemetry_type,
            status=ConsentStatus.WITHDRAWN,
            granted_at=consents[telemetry_type.value].granted_at,
            withdrawn_at=datetime.utcnow(),
            metadata=metadata
        )
        
        self._save_consents(user_id, consents)
        
        logger.info(
            f"Withdrawn consent for user {user_id} and telemetry type {telemetry_type.value}"
        )
    
    def get_all_consents(
        self,
        user_id: str
    ) -> Dict[str, ConsentRecord]:
        """Get all user consents.
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary of consent records
        """
        return self._load_consents(user_id)
    
    def get_consent_stats(
        self,
        telemetry_type: Optional[TelemetryType] = None
    ) -> Dict[str, Any]:
        """Get consent statistics.
        
        Args:
            telemetry_type: Telemetry type
            
        Returns:
            Consent statistics dictionary
        """
        stats = {
            "total_users": 0,
            "status": {
                status.value: 0
                for status in ConsentStatus
            },
            "telemetry_types": {
                telemetry_type.value: {
                    status.value: 0
                    for status in ConsentStatus
                }
                for telemetry_type in TelemetryType
            }
        }
        
        # Iterate through consent files
        for consent_file in Path(self.consent_dir).glob("*.json"):
            with open(consent_file, "r") as f:
                data = json.load(f)
            
            stats["total_users"] += 1
            
            # Calculate statistics
            for telemetry_type_value, record in data.items():
                status = ConsentStatus(record["status"])
                
                stats["status"][status.value] += 1
                stats["telemetry_types"][telemetry_type_value][status.value] += 1
        
        return stats
    
    def export_consents(
        self,
        format: str = "json"
    ) -> str:
        """Export consents.
        
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
        export_dir = os.path.join(self.consent_dir, "exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # Create export file path
        export_file = os.path.join(
            export_dir,
            f"consents_{datetime.now().strftime('%Y%m%d')}.{format}"
        )
        
        # Export consents
        consents_data = {}
        
        for consent_file in Path(self.consent_dir).glob("*.json"):
            if consent_file.name == "exports":
                continue
            
            with open(consent_file, "r") as f:
                data = json.load(f)
            
            consents_data[consent_file.stem] = data
        
        with open(export_file, "w") as f:
            json.dump(consents_data, f, indent=2)
        
        return export_file
    
    def cleanup_consents(
        self,
        max_age_days: int = 365
    ) -> None:
        """Clean up old consents.
        
        Args:
            max_age_days: Maximum age in days
        """
        # Get current time
        now = datetime.utcnow()
        
        # Iterate through consent files
        for consent_file in Path(self.consent_dir).glob("*.json"):
            if consent_file.name == "exports":
                continue
            
            with open(consent_file, "r") as f:
                data = json.load(f)
            
            # Check if all consents are old
            all_old = True
            
            for record in data.values():
                if record["granted_at"]:
                    granted_at = datetime.fromisoformat(record["granted_at"])
                    
                    if (now - granted_at).days <= max_age_days:
                        all_old = False
                        break
            
            # Remove old consent file
            if all_old:
                consent_file.unlink()
                
                logger.info(f"Removed old consent file: {consent_file}") 