"""
Security Manager Tests

This module contains tests for the enhanced security manager.

Author: Rami Drive School
Date: 2024
"""

import pytest
from datetime import datetime, timedelta
import json
import os
import shutil
from pathlib import Path

from ontario_driving_school_manager.core.security.security_manager import (
    SecurityManager,
    AuditEventType,
    AuditResourceType,
    EncryptionAlgorithm
)

@pytest.fixture
def security_manager(tmp_path):
    """Create security manager fixture."""
    # Create test directories
    keys_dir = tmp_path / "keys"
    audit_dir = tmp_path / "audit"
    versions_dir = tmp_path / "versions"
    
    # Create security manager
    manager = SecurityManager(
        keys_dir=str(keys_dir),
        audit_dir=str(audit_dir),
        versions_dir=str(versions_dir)
    )
    
    yield manager
    
    # Clean up
    shutil.rmtree(tmp_path)

def test_encrypt_decrypt_field(security_manager):
    """Test field encryption and decryption."""
    # Generate key
    key = security_manager.generate_key(
        key_id="test_key",
        algorithm=EncryptionAlgorithm.FERNET
    )
    
    # Test data
    value = "test_value"
    resource_type = AuditResourceType.USER
    resource_id = "test_user"
    user_id = "test_user"
    
    # Encrypt field
    encrypted_field = security_manager.encrypt_field(
        value=value,
        key_id=key.key_id,
        resource_type=resource_type,
        resource_id=resource_id,
        user_id=user_id
    )
    
    # Verify encrypted field
    assert encrypted_field.value != value
    assert encrypted_field.algorithm == EncryptionAlgorithm.FERNET
    assert encrypted_field.key_id == key.key_id
    
    # Decrypt field
    decrypted_value = security_manager.decrypt_field(
        field=encrypted_field,
        resource_type=resource_type,
        resource_id=resource_id,
        user_id=user_id
    )
    
    # Verify decrypted value
    assert decrypted_value == value
    
    # Get events
    events = security_manager.get_events(
        resource_type=resource_type,
        resource_id=resource_id
    )
    
    # Verify events
    assert len(events) == 2
    assert events[0].event_type == AuditEventType.CUSTOM
    assert events[1].event_type == AuditEventType.CUSTOM

def test_track_changes(security_manager):
    """Test change tracking."""
    # Test data
    resource_type = AuditResourceType.USER
    resource_id = "test_user"
    user_id = "test_user"
    
    old_data = {
        "name": "Old Name",
        "email": "old@example.com"
    }
    
    new_data = {
        "name": "New Name",
        "email": "new@example.com"
    }
    
    # Track changes
    version_change = security_manager.track_changes(
        resource_type=resource_type,
        resource_id=resource_id,
        user_id=user_id,
        old_data=old_data,
        new_data=new_data
    )
    
    # Verify version change
    assert version_change.version == 1
    assert version_change.user_id == user_id
    assert "name" in version_change.changes
    assert "email" in version_change.changes
    
    # Get events
    events = security_manager.get_events(
        resource_type=resource_type,
        resource_id=resource_id
    )
    
    # Verify events
    assert len(events) == 1
    assert events[0].event_type == AuditEventType.UPDATE
    
    # Get versions
    versions = security_manager.get_versions(
        resource_type=resource_type,
        resource_id=resource_id
    )
    
    # Verify versions
    assert len(versions) == 1
    assert versions[0].version == 1

def test_key_management(security_manager):
    """Test key management."""
    # Generate key
    key = security_manager.generate_key(
        key_id="test_key",
        algorithm=EncryptionAlgorithm.FERNET
    )
    
    # Verify key
    assert key.algorithm == EncryptionAlgorithm.FERNET
    
    # Get key
    retrieved_key = security_manager.get_key(key_id=key.key_id)
    
    # Verify retrieved key
    assert retrieved_key.key_id == key.key_id
    assert retrieved_key.algorithm == key.algorithm
    
    # Rotate key
    new_key = security_manager.rotate_key(
        key_id=key.key_id,
        new_key_id="new_test_key"
    )
    
    # Verify new key
    assert new_key.key_id == "new_test_key"
    assert new_key.algorithm == EncryptionAlgorithm.FERNET
    
    # Delete key
    security_manager.delete_key(key_id=new_key.key_id)
    
    # Verify key deletion
    assert security_manager.get_key(key_id=new_key.key_id) is None

def test_security_stats(security_manager):
    """Test security statistics."""
    # Generate key
    security_manager.generate_key(
        key_id="test_key",
        algorithm=EncryptionAlgorithm.FERNET
    )
    
    # Track changes
    security_manager.track_changes(
        resource_type=AuditResourceType.USER,
        resource_id="test_user",
        user_id="test_user",
        old_data={"name": "Old Name"},
        new_data={"name": "New Name"}
    )
    
    # Get stats
    stats = security_manager.get_security_stats()
    
    # Verify stats
    assert "audit" in stats
    assert "keys" in stats
    assert stats["audit"]["total_events"] > 0
    assert stats["keys"]["total_keys"] > 0

def test_export_security_data(security_manager, tmp_path):
    """Test security data export."""
    # Generate key
    security_manager.generate_key(
        key_id="test_key",
        algorithm=EncryptionAlgorithm.FERNET
    )
    
    # Track changes
    security_manager.track_changes(
        resource_type=AuditResourceType.USER,
        resource_id="test_user",
        user_id="test_user",
        old_data={"name": "Old Name"},
        new_data={"name": "New Name"}
    )
    
    # Export data
    export_files = security_manager.export_security_data()
    
    # Verify export files
    assert "audit" in export_files
    assert "versions" in export_files
    assert "keys" in export_files
    
    # Verify file contents
    for file_path in export_files.values():
        with open(file_path, "r") as f:
            data = json.load(f)
            assert data

def test_cleanup_security_data(security_manager):
    """Test security data cleanup."""
    # Generate key
    security_manager.generate_key(
        key_id="test_key",
        algorithm=EncryptionAlgorithm.FERNET
    )
    
    # Track changes
    security_manager.track_changes(
        resource_type=AuditResourceType.USER,
        resource_id="test_user",
        user_id="test_user",
        old_data={"name": "Old Name"},
        new_data={"name": "New Name"}
    )
    
    # Get initial stats
    initial_stats = security_manager.get_security_stats()
    
    # Clean up data
    security_manager.cleanup_security_data(max_age_days=0)
    
    # Get final stats
    final_stats = security_manager.get_security_stats()
    
    # Verify cleanup
    assert final_stats["audit"]["total_events"] < initial_stats["audit"]["total_events"]

def test_encrypt_decrypt_complex_types(security_manager):
    """Test encryption and decryption of complex types."""
    # Generate key
    key = security_manager.generate_key(
        key_id="test_key",
        algorithm=EncryptionAlgorithm.FERNET
    )
    
    # Test data
    value = {
        "name": "Test User",
        "age": 30,
        "address": {
            "street": "123 Main St",
            "city": "Toronto"
        },
        "phones": ["123-456-7890", "098-765-4321"]
    }
    
    resource_type = AuditResourceType.USER
    resource_id = "test_user"
    user_id = "test_user"
    
    # Encrypt field
    encrypted_field = security_manager.encrypt_field(
        value=value,
        key_id=key.key_id,
        resource_type=resource_type,
        resource_id=resource_id,
        user_id=user_id
    )
    
    # Decrypt field
    decrypted_value = security_manager.decrypt_field(
        field=encrypted_field,
        resource_type=resource_type,
        resource_id=resource_id,
        user_id=user_id,
        value_type=dict
    )
    
    # Verify decrypted value
    assert decrypted_value == value

def test_version_history(security_manager):
    """Test version history tracking."""
    # Test data
    resource_type = AuditResourceType.USER
    resource_id = "test_user"
    user_id = "test_user"
    
    # Track multiple changes
    changes = [
        ({"name": "Name 1"}, {"name": "Name 2"}),
        ({"name": "Name 2"}, {"name": "Name 3"}),
        ({"name": "Name 3"}, {"name": "Name 4"})
    ]
    
    for old_data, new_data in changes:
        security_manager.track_changes(
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            old_data=old_data,
            new_data=new_data
        )
    
    # Get versions
    versions = security_manager.get_versions(
        resource_type=resource_type,
        resource_id=resource_id
    )
    
    # Verify versions
    assert len(versions) == 3
    
    for i, version in enumerate(versions, 1):
        assert version.version == i
        assert "name" in version.changes

def test_filtered_events(security_manager):
    """Test filtered event retrieval."""
    # Test data
    resource_type = AuditResourceType.USER
    resource_id = "test_user"
    user_id = "test_user"
    
    # Track changes
    security_manager.track_changes(
        resource_type=resource_type,
        resource_id=resource_id,
        user_id=user_id,
        old_data={"name": "Old Name"},
        new_data={"name": "New Name"}
    )
    
    # Get events with filters
    events = security_manager.get_events(
        resource_type=resource_type,
        resource_id=resource_id,
        event_type=AuditEventType.UPDATE,
        user_id=user_id,
        start_time=datetime.utcnow() - timedelta(hours=1),
        end_time=datetime.utcnow() + timedelta(hours=1)
    )
    
    # Verify filtered events
    assert len(events) == 1
    assert events[0].event_type == AuditEventType.UPDATE
    assert events[0].user_id == user_id

def test_key_expiration(security_manager):
    """Test key expiration."""
    # Generate key with expiration
    key = security_manager.generate_key(
        key_id="test_key",
        algorithm=EncryptionAlgorithm.FERNET,
        expires_at=datetime.utcnow() - timedelta(days=1)
    )
    
    # Test data
    value = "test_value"
    resource_type = AuditResourceType.USER
    resource_id = "test_user"
    user_id = "test_user"
    
    # Attempt to encrypt field
    with pytest.raises(ValueError):
        security_manager.encrypt_field(
            value=value,
            key_id=key.key_id,
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id
        )

def test_invalid_key(security_manager):
    """Test invalid key handling."""
    # Test data
    value = "test_value"
    resource_type = AuditResourceType.USER
    resource_id = "test_user"
    user_id = "test_user"
    
    # Attempt to encrypt field with invalid key
    with pytest.raises(ValueError):
        security_manager.encrypt_field(
            value=value,
            key_id="invalid_key",
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id
        )

def test_duplicate_key(security_manager):
    """Test duplicate key handling."""
    # Generate key
    security_manager.generate_key(
        key_id="test_key",
        algorithm=EncryptionAlgorithm.FERNET
    )
    
    # Attempt to generate duplicate key
    with pytest.raises(ValueError):
        security_manager.generate_key(
            key_id="test_key",
            algorithm=EncryptionAlgorithm.FERNET
        )

def test_invalid_resource_type(security_manager):
    """Test invalid resource type handling."""
    # Test data
    value = "test_value"
    resource_id = "test_user"
    user_id = "test_user"
    
    # Generate key
    key = security_manager.generate_key(
        key_id="test_key",
        algorithm=EncryptionAlgorithm.FERNET
    )
    
    # Attempt to encrypt field with invalid resource type
    with pytest.raises(ValueError):
        security_manager.encrypt_field(
            value=value,
            key_id=key.key_id,
            resource_type="invalid_type",
            resource_id=resource_id,
            user_id=user_id
        )

def test_invalid_event_type(security_manager):
    """Test invalid event type handling."""
    # Test data
    resource_type = AuditResourceType.USER
    resource_id = "test_user"
    user_id = "test_user"
    
    # Attempt to log event with invalid event type
    with pytest.raises(ValueError):
        security_manager.audit_trail.log_event(
            event_type="invalid_type",
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id
        )

def test_invalid_export_format(security_manager):
    """Test invalid export format handling."""
    # Attempt to export with invalid format
    with pytest.raises(ValueError):
        security_manager.export_security_data(format="invalid_format")

def test_cleanup_empty_data(security_manager):
    """Test cleanup of empty data."""
    # Clean up empty data
    security_manager.cleanup_security_data()
    
    # Get stats
    stats = security_manager.get_security_stats()
    
    # Verify stats
    assert stats["audit"]["total_events"] == 0
    assert stats["keys"]["total_keys"] == 0 