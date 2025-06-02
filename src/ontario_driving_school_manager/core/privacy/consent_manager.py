"""
Consent Manager Module

This module provides consent management functionality for PIPEDA compliance.
It handles user consent tracking, updates, and verification.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import json
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class ConsentError(Exception):
    """Consent error."""
    pass

class ConsentManager:
    """Consent manager."""
    
    def __init__(
        self,
        consent_dir: str = "consents",
        consent_types: Optional[List[str]] = None
    ):
        """Initialize consent manager.
        
        Args:
            consent_dir: Consent directory
            consent_types: List of consent types
        """
        self.consent_dir = consent_dir
        self.consent_types = consent_types or [
            "marketing",
            "data_collection",
            "data_sharing",
            "cookies",
            "analytics",
            "third_party"
        ]
        
        # Create consent directory if it doesn't exist
        os.makedirs(consent_dir, exist_ok=True)
    
    def record_consent(
        self,
        user_id: str,
        consent_type: str,
        granted: bool,
        timestamp: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Record user consent.
        
        Args:
            user_id: User ID
            consent_type: Type of consent
            granted: Whether consent was granted
            timestamp: Consent timestamp
            metadata: Additional metadata
            
        Raises:
            ConsentError: If consent type is invalid
        """
        if consent_type not in self.consent_types:
            raise ConsentError(f"Invalid consent type: {consent_type}")
        
        try:
            # Create user consent directory
            user_dir = os.path.join(self.consent_dir, user_id)
            os.makedirs(user_dir, exist_ok=True)
            
            # Create consent record
            consent = {
                "user_id": user_id,
                "consent_type": consent_type,
                "granted": granted,
                "timestamp": (timestamp or datetime.utcnow()).isoformat(),
                "metadata": metadata or {}
            }
            
            # Write consent record
            consent_file = os.path.join(
                user_dir,
                f"{consent_type}.json"
            )
            
            with open(consent_file, "w") as f:
                json.dump(consent, f, indent=2)
            
            logger.info(
                f"Recorded {consent_type} consent for user {user_id}"
            )
        except Exception as e:
            raise ConsentError(f"Error recording consent: {str(e)}")
    
    def get_consent(
        self,
        user_id: str,
        consent_type: str
    ) -> Optional[Dict[str, Any]]:
        """Get user consent.
        
        Args:
            user_id: User ID
            consent_type: Type of consent
            
        Returns:
            Consent record if found, None otherwise
            
        Raises:
            ConsentError: If consent type is invalid
        """
        if consent_type not in self.consent_types:
            raise ConsentError(f"Invalid consent type: {consent_type}")
        
        try:
            # Get consent file path
            consent_file = os.path.join(
                self.consent_dir,
                user_id,
                f"{consent_type}.json"
            )
            
            # Check if consent file exists
            if not os.path.exists(consent_file):
                return None
            
            # Read consent record
            with open(consent_file, "r") as f:
                return json.load(f)
        except Exception as e:
            raise ConsentError(f"Error getting consent: {str(e)}")
    
    def get_all_consents(
        self,
        user_id: str
    ) -> Dict[str, Dict[str, Any]]:
        """Get all user consents.
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary of consent records by type
        """
        try:
            consents = {}
            
            # Get user consent directory
            user_dir = os.path.join(self.consent_dir, user_id)
            
            # Check if user directory exists
            if not os.path.exists(user_dir):
                return consents
            
            # Read all consent records
            for consent_type in self.consent_types:
                consent_file = os.path.join(
                    user_dir,
                    f"{consent_type}.json"
                )
                
                if os.path.exists(consent_file):
                    with open(consent_file, "r") as f:
                        consents[consent_type] = json.load(f)
            
            return consents
        except Exception as e:
            raise ConsentError(f"Error getting consents: {str(e)}")
    
    def revoke_consent(
        self,
        user_id: str,
        consent_type: str
    ) -> None:
        """Revoke user consent.
        
        Args:
            user_id: User ID
            consent_type: Type of consent
            
        Raises:
            ConsentError: If consent type is invalid
        """
        if consent_type not in self.consent_types:
            raise ConsentError(f"Invalid consent type: {consent_type}")
        
        try:
            # Get consent file path
            consent_file = os.path.join(
                self.consent_dir,
                user_id,
                f"{consent_type}.json"
            )
            
            # Check if consent file exists
            if not os.path.exists(consent_file):
                return
            
            # Read consent record
            with open(consent_file, "r") as f:
                consent = json.load(f)
            
            # Update consent record
            consent["granted"] = False
            consent["timestamp"] = datetime.utcnow().isoformat()
            
            # Write updated consent record
            with open(consent_file, "w") as f:
                json.dump(consent, f, indent=2)
            
            logger.info(
                f"Revoked {consent_type} consent for user {user_id}"
            )
        except Exception as e:
            raise ConsentError(f"Error revoking consent: {str(e)}")
    
    def has_consent(
        self,
        user_id: str,
        consent_type: str
    ) -> bool:
        """Check if user has given consent.
        
        Args:
            user_id: User ID
            consent_type: Type of consent
            
        Returns:
            True if consent was granted, False otherwise
            
        Raises:
            ConsentError: If consent type is invalid
        """
        consent = self.get_consent(user_id, consent_type)
        return consent is not None and consent["granted"]
    
    def get_consent_history(
        self,
        user_id: str,
        consent_type: str
    ) -> List[Dict[str, Any]]:
        """Get user consent history.
        
        Args:
            user_id: User ID
            consent_type: Type of consent
            
        Returns:
            List of consent records
            
        Raises:
            ConsentError: If consent type is invalid
        """
        if consent_type not in self.consent_types:
            raise ConsentError(f"Invalid consent type: {consent_type}")
        
        try:
            # Get consent history file path
            history_file = os.path.join(
                self.consent_dir,
                user_id,
                f"{consent_type}_history.json"
            )
            
            # Check if history file exists
            if not os.path.exists(history_file):
                return []
            
            # Read consent history
            with open(history_file, "r") as f:
                return json.load(f)
        except Exception as e:
            raise ConsentError(f"Error getting consent history: {str(e)}")
    
    def add_consent_type(
        self,
        consent_type: str
    ) -> None:
        """Add consent type.
        
        Args:
            consent_type: Type of consent
            
        Raises:
            ConsentError: If consent type already exists
        """
        if consent_type in self.consent_types:
            raise ConsentError(f"Consent type already exists: {consent_type}")
        
        self.consent_types.append(consent_type)
    
    def remove_consent_type(
        self,
        consent_type: str
    ) -> None:
        """Remove consent type.
        
        Args:
            consent_type: Type of consent
            
        Raises:
            ConsentError: If consent type doesn't exist
        """
        if consent_type not in self.consent_types:
            raise ConsentError(f"Consent type doesn't exist: {consent_type}")
        
        self.consent_types.remove(consent_type)
    
    def get_consent_types(self) -> List[str]:
        """Get consent types.
        
        Returns:
            List of consent types
        """
        return self.consent_types.copy()
    
    def get_consent_stats(
        self,
        consent_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get consent statistics.
        
        Args:
            consent_type: Type of consent
            
        Returns:
            Consent statistics dictionary
        """
        try:
            stats = {
                "total_users": 0,
                "consented_users": 0,
                "consent_types": {}
            }
            
            # Iterate through consent directory
            for user_dir in Path(self.consent_dir).iterdir():
                if not user_dir.is_dir():
                    continue
                
                stats["total_users"] += 1
                
                # Check consent type
                if consent_type:
                    consent_file = user_dir / f"{consent_type}.json"
                    
                    if consent_file.exists():
                        with open(consent_file, "r") as f:
                            consent = json.load(f)
                            
                            if consent["granted"]:
                                stats["consented_users"] += 1
                else:
                    # Check all consent types
                    for consent_type in self.consent_types:
                        consent_file = user_dir / f"{consent_type}.json"
                        
                        if consent_file.exists():
                            with open(consent_file, "r") as f:
                                consent = json.load(f)
                                
                                if consent["granted"]:
                                    if consent_type not in stats["consent_types"]:
                                        stats["consent_types"][consent_type] = 0
                                    
                                    stats["consent_types"][consent_type] += 1
            
            return stats
        except Exception as e:
            raise ConsentError(f"Error getting consent stats: {str(e)}")
    
    def cleanup_consents(
        self,
        max_age_days: int = 365
    ) -> None:
        """Clean up old consents.
        
        Args:
            max_age_days: Maximum age in days
        """
        try:
            # Get current time
            now = datetime.utcnow()
            
            # Iterate through consent directory
            for user_dir in Path(self.consent_dir).iterdir():
                if not user_dir.is_dir():
                    continue
                
                # Check consent files
                for consent_file in user_dir.glob("*.json"):
                    # Skip history files
                    if consent_file.name.endswith("_history.json"):
                        continue
                    
                    # Get file age
                    file_age = now - datetime.fromtimestamp(
                        consent_file.stat().st_mtime
                    )
                    
                    # Remove old files
                    if file_age.days > max_age_days:
                        consent_file.unlink()
        except Exception as e:
            logger.error(f"Error cleaning up consents: {str(e)}")
    
    def export_consents(
        self,
        user_id: str,
        format: str = "json"
    ) -> str:
        """Export user consents.
        
        Args:
            user_id: User ID
            format: Export format
            
        Returns:
            Path to exported file
            
        Raises:
            ConsentError: If export fails
        """
        try:
            # Get all consents
            consents = self.get_all_consents(user_id)
            
            # Create export directory
            export_dir = os.path.join(self.consent_dir, "exports")
            os.makedirs(export_dir, exist_ok=True)
            
            # Create export file path
            export_file = os.path.join(
                export_dir,
                f"{user_id}_consents.{format}"
            )
            
            # Export consents
            if format == "json":
                with open(export_file, "w") as f:
                    json.dump(consents, f, indent=2)
            else:
                raise ConsentError(f"Unsupported format: {format}")
            
            return export_file
        except Exception as e:
            raise ConsentError(f"Error exporting consents: {str(e)}") 