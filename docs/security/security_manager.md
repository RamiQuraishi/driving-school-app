# Security Manager

The Security Manager provides enhanced security functionality by integrating field encryption and audit trail capabilities. It ensures data security and maintains a comprehensive audit trail of all system events and data changes.

## Features

- Field-level encryption for sensitive data
- Comprehensive audit trail of system events
- Version change tracking
- Key management with rotation and expiration
- Data export and cleanup utilities

## Components

### Field Encryption Manager

The Field Encryption Manager handles encryption and decryption of sensitive data fields. It supports:

- Multiple encryption algorithms (Fernet, AES)
- Key generation and management
- Key rotation and expiration
- Field-level encryption and decryption

### Audit Trail Manager

The Audit Trail Manager maintains a detailed record of system events and data changes. It provides:

- Event logging for all system actions
- Version change tracking
- Filtered event retrieval
- Data export capabilities

## Usage

### Initialization

```python
from ontario_driving_school_manager.core.security.security_manager import SecurityManager

# Create security manager
security_manager = SecurityManager(
    keys_dir="keys",
    audit_dir="audit",
    versions_dir="versions"
)
```

### Field Encryption

```python
# Generate encryption key
key = security_manager.generate_key(
    key_id="user_data_key",
    algorithm=EncryptionAlgorithm.FERNET
)

# Encrypt field
encrypted_field = security_manager.encrypt_field(
    value="sensitive_data",
    key_id=key.key_id,
    resource_type=AuditResourceType.USER,
    resource_id="user123",
    user_id="admin"
)

# Decrypt field
decrypted_value = security_manager.decrypt_field(
    field=encrypted_field,
    resource_type=AuditResourceType.USER,
    resource_id="user123",
    user_id="admin"
)
```

### Change Tracking

```python
# Track changes
version_change = security_manager.track_changes(
    resource_type=AuditResourceType.USER,
    resource_id="user123",
    user_id="admin",
    old_data={"name": "Old Name"},
    new_data={"name": "New Name"}
)

# Get version history
versions = security_manager.get_versions(
    resource_type=AuditResourceType.USER,
    resource_id="user123"
)
```

### Event Retrieval

```python
# Get events
events = security_manager.get_events(
    resource_type=AuditResourceType.USER,
    resource_id="user123",
    event_type=AuditEventType.UPDATE,
    user_id="admin",
    start_time=datetime.utcnow() - timedelta(days=1),
    end_time=datetime.utcnow()
)
```

### Key Management

```python
# Generate key
key = security_manager.generate_key(
    key_id="data_key",
    algorithm=EncryptionAlgorithm.FERNET,
    expires_at=datetime.utcnow() + timedelta(days=30)
)

# Rotate key
new_key = security_manager.rotate_key(
    key_id=key.key_id,
    new_key_id="new_data_key"
)

# Delete key
security_manager.delete_key(key_id=new_key.key_id)
```

### Data Export

```python
# Export security data
export_files = security_manager.export_security_data()

# Access exported files
audit_file = export_files["audit"]
versions_file = export_files["versions"]
keys_file = export_files["keys"]
```

### Data Cleanup

```python
# Clean up old data
security_manager.cleanup_security_data(max_age_days=365)
```

## Security Considerations

### Key Management

- Store encryption keys securely
- Rotate keys regularly
- Set appropriate key expiration times
- Use strong passwords for key derivation

### Audit Trail

- Monitor audit events regularly
- Export audit data periodically
- Clean up old audit data
- Protect audit data integrity

### Data Protection

- Encrypt sensitive data at rest
- Use appropriate encryption algorithms
- Implement proper access controls
- Follow security best practices

## Best Practices

1. **Key Management**
   - Generate strong encryption keys
   - Implement key rotation policies
   - Monitor key usage and expiration
   - Secure key storage

2. **Audit Trail**
   - Log all security-relevant events
   - Maintain comprehensive audit records
   - Regular audit data export
   - Periodic audit data cleanup

3. **Data Protection**
   - Encrypt sensitive data
   - Use appropriate encryption algorithms
   - Implement access controls
   - Follow security standards

4. **Monitoring**
   - Monitor security events
   - Track system changes
   - Review audit logs
   - Analyze security statistics

## Error Handling

The Security Manager includes comprehensive error handling for:

- Invalid keys
- Expired keys
- Invalid resource types
- Invalid event types
- Export format errors
- Data cleanup errors

## Performance Considerations

- Use appropriate key sizes
- Implement efficient audit logging
- Optimize data cleanup
- Monitor system performance

## Maintenance

Regular maintenance tasks include:

- Key rotation
- Audit data export
- Data cleanup
- Performance monitoring
- Security updates

## Troubleshooting

Common issues and solutions:

1. **Key Errors**
   - Verify key existence
   - Check key expiration
   - Validate key format
   - Rotate expired keys

2. **Audit Trail Issues**
   - Check file permissions
   - Verify directory structure
   - Monitor disk space
   - Validate audit data

3. **Performance Problems**
   - Optimize key operations
   - Clean up old data
   - Monitor system resources
   - Review audit logging

## API Reference

### SecurityManager

Main class for security management.

#### Methods

- `__init__(keys_dir, audit_dir, versions_dir, salt, iterations)`
- `encrypt_field(value, key_id, resource_type, resource_id, user_id, metadata)`
- `decrypt_field(field, resource_type, resource_id, user_id, value_type, metadata)`
- `track_changes(resource_type, resource_id, user_id, old_data, new_data, metadata)`
- `get_events(resource_type, resource_id, event_type, user_id, start_time, end_time)`
- `get_versions(resource_type, resource_id, user_id, start_time, end_time)`
- `get_version(resource_type, resource_id, version)`
- `generate_key(key_id, algorithm, password, expires_at, metadata)`
- `get_key(key_id)`
- `delete_key(key_id)`
- `rotate_key(key_id, new_key_id, metadata)`
- `get_security_stats()`
- `export_security_data(format)`
- `cleanup_security_data(max_age_days)`

### Enums

- `AuditEventType`
- `AuditResourceType`
- `EncryptionAlgorithm`

### Data Classes

- `AuditEvent`
- `VersionChange`
- `EncryptionKey`
- `EncryptedField`

## Examples

### Basic Usage

```python
# Initialize security manager
security_manager = SecurityManager()

# Generate key
key = security_manager.generate_key("data_key")

# Encrypt data
encrypted = security_manager.encrypt_field(
    value="sensitive_data",
    key_id=key.key_id,
    resource_type=AuditResourceType.USER,
    resource_id="user123",
    user_id="admin"
)

# Decrypt data
decrypted = security_manager.decrypt_field(
    field=encrypted,
    resource_type=AuditResourceType.USER,
    resource_id="user123",
    user_id="admin"
)
```

### Advanced Usage

```python
# Track changes with metadata
version_change = security_manager.track_changes(
    resource_type=AuditResourceType.USER,
    resource_id="user123",
    user_id="admin",
    old_data={"name": "Old Name"},
    new_data={"name": "New Name"},
    metadata={"reason": "Name update"}
)

# Get filtered events
events = security_manager.get_events(
    resource_type=AuditResourceType.USER,
    resource_id="user123",
    event_type=AuditEventType.UPDATE,
    user_id="admin",
    start_time=datetime.utcnow() - timedelta(days=1)
)

# Export security data
export_files = security_manager.export_security_data()
```

## Contributing

When contributing to the Security Manager:

1. Follow security best practices
2. Write comprehensive tests
3. Document all changes
4. Review security implications
5. Test thoroughly

## License

This module is part of the Rami Drive School Manager and is subject to its license terms. 