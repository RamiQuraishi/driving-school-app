"""
Security Manager Module

This module provides enhanced security functionality by integrating
field encryption and audit trail capabilities.

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

from .field_encryption import (
    FieldEncryptionManager,
    EncryptionAlgorithm,
    EncryptionKey,
    EncryptedField
)
from .audit_trail import (
    AuditTrailManager,
    AuditEventType,
    AuditResourceType,
    AuditEvent,
    VersionChange
)

logger = logging.getLogger(__name__)

T = TypeVar("T")

class SecurityManager:
    """Security manager."""
    
    def __init__(
        self,
        keys_dir: str = "keys",
        audit_dir: str = "audit",
        versions_dir: str = "versions",
        salt: Optional[bytes] = None,
        iterations: int = 100000
    ):
        """Initialize security manager.
        
        Args:
            keys_dir: Keys directory
            audit_dir: Audit directory
            versions_dir: Versions directory
            salt: Salt for key derivation
            iterations: Number of iterations for key derivation
        """
        self.field_encryption = FieldEncryptionManager(
            keys_dir=keys_dir,
            salt=salt,
            iterations=iterations
        )
        
        self.audit_trail = AuditTrailManager(
            audit_dir=audit_dir,
            versions_dir=versions_dir
        )
    
    def encrypt_field(
        self,
        value: Any,
        key_id: str,
        resource_type: AuditResourceType,
        resource_id: str,
        user_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> EncryptedField:
        """Encrypt field value.
        
        Args:
            value: Field value
            key_id: Key ID
            resource_type: Resource type
            resource_id: Resource ID
            user_id: User ID
            metadata: Additional metadata
            
        Returns:
            Encrypted field
            
        Raises:
            ValueError: If key doesn't exist or is expired
        """
        # Encrypt field
        encrypted_field = self.field_encryption.encrypt_field(
            value=value,
            key_id=key_id,
            metadata=metadata
        )
        
        # Log encryption event
        self.audit_trail.log_event(
            event_type=AuditEventType.CUSTOM,
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            changes={
                "field": "encrypted_field",
                "key_id": key_id
            },
            metadata=metadata
        )
        
        return encrypted_field
    
    def decrypt_field(
        self,
        field: EncryptedField,
        resource_type: AuditResourceType,
        resource_id: str,
        user_id: str,
        value_type: Optional[Type[T]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Union[str, T]:
        """Decrypt field value.
        
        Args:
            field: Encrypted field
            resource_type: Resource type
            resource_id: Resource ID
            user_id: User ID
            value_type: Value type
            metadata: Additional metadata
            
        Returns:
            Decrypted value
            
        Raises:
            ValueError: If key doesn't exist or is expired
        """
        # Decrypt field
        decrypted_value = self.field_encryption.decrypt_field(
            field=field,
            value_type=value_type
        )
        
        # Log decryption event
        self.audit_trail.log_event(
            event_type=AuditEventType.CUSTOM,
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            changes={
                "field": "decrypted_field",
                "key_id": field.key_id
            },
            metadata=metadata
        )
        
        return decrypted_value
    
    def track_changes(
        self,
        resource_type: AuditResourceType,
        resource_id: str,
        user_id: str,
        old_data: Dict[str, Any],
        new_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> VersionChange:
        """Track changes.
        
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
        # Track version change
        version_change = self.audit_trail.track_version(
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            old_data=old_data,
            new_data=new_data,
            metadata=metadata
        )
        
        # Log change event
        self.audit_trail.log_event(
            event_type=AuditEventType.UPDATE,
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            changes=version_change.changes,
            metadata=metadata
        )
        
        return version_change
    
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
        return self.audit_trail.get_events(
            resource_type=resource_type,
            resource_id=resource_id,
            event_type=event_type,
            user_id=user_id,
            start_time=start_time,
            end_time=end_time
        )
    
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
        return self.audit_trail.get_versions(
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            start_time=start_time,
            end_time=end_time
        )
    
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
        return self.audit_trail.get_version(
            resource_type=resource_type,
            resource_id=resource_id,
            version=version
        )
    
    def generate_key(
        self,
        key_id: str,
        algorithm: EncryptionAlgorithm = EncryptionAlgorithm.FERNET,
        password: Optional[str] = None,
        expires_at: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> EncryptionKey:
        """Generate encryption key.
        
        Args:
            key_id: Key ID
            algorithm: Encryption algorithm
            password: Password for key derivation
            expires_at: Expiration timestamp
            metadata: Additional metadata
            
        Returns:
            Generated encryption key
            
        Raises:
            ValueError: If key already exists
        """
        return self.field_encryption.generate_key(
            key_id=key_id,
            algorithm=algorithm,
            password=password,
            expires_at=expires_at,
            metadata=metadata
        )
    
    def get_key(
        self,
        key_id: str
    ) -> Optional[EncryptionKey]:
        """Get encryption key.
        
        Args:
            key_id: Key ID
            
        Returns:
            Encryption key if found, None otherwise
        """
        return self.field_encryption.get_key(key_id=key_id)
    
    def delete_key(
        self,
        key_id: str
    ) -> None:
        """Delete encryption key.
        
        Args:
            key_id: Key ID
            
        Raises:
            ValueError: If key doesn't exist
        """
        self.field_encryption.delete_key(key_id=key_id)
    
    def rotate_key(
        self,
        key_id: str,
        new_key_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> EncryptionKey:
        """Rotate encryption key.
        
        Args:
            key_id: Old key ID
            new_key_id: New key ID
            metadata: Additional metadata
            
        Returns:
            New encryption key
            
        Raises:
            ValueError: If old key doesn't exist or new key already exists
        """
        return self.field_encryption.rotate_key(
            key_id=key_id,
            new_key_id=new_key_id,
            metadata=metadata
        )
    
    def get_security_stats(
        self
    ) -> Dict[str, Any]:
        """Get security statistics.
        
        Returns:
            Security statistics dictionary
        """
        # Get audit stats
        audit_stats = self.audit_trail.get_audit_stats()
        
        # Get key stats
        key_stats = self.field_encryption.get_key_stats()
        
        return {
            "audit": audit_stats,
            "keys": key_stats
        }
    
    def export_security_data(
        self,
        format: str = "json"
    ) -> Dict[str, str]:
        """Export security data.
        
        Args:
            format: Export format
            
        Returns:
            Dictionary mapping export type to file path
            
        Raises:
            ValueError: If format is not supported
        """
        # Export audit trail
        audit_file = self.audit_trail.export_audit(format=format)
        
        # Export versions
        versions_file = self.audit_trail.export_versions(format=format)
        
        # Export keys
        keys_file = self.field_encryption.export_keys(format=format)
        
        return {
            "audit": audit_file,
            "versions": versions_file,
            "keys": keys_file
        }
    
    def cleanup_security_data(
        self,
        max_age_days: int = 365
    ) -> None:
        """Clean up security data.
        
        Args:
            max_age_days: Maximum age in days
        """
        # Clean up audit trail
        self.audit_trail.cleanup_audit(max_age_days=max_age_days)
        
        # Clean up versions
        self.audit_trail.cleanup_versions(max_age_days=max_age_days) 