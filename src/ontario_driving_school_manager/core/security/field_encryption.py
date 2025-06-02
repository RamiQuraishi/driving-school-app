"""
Field Encryption Manager Module

This module provides field-level encryption functionality.
It handles encryption and decryption of sensitive data fields.

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
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

logger = logging.getLogger(__name__)

T = TypeVar("T")

class EncryptionAlgorithm(Enum):
    """Encryption algorithm."""
    FERNET = "fernet"
    AES = "aes"

@dataclass
class EncryptionKey:
    """Encryption key."""
    key: bytes
    algorithm: EncryptionAlgorithm
    created_at: datetime
    expires_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class EncryptedField:
    """Encrypted field."""
    value: str
    algorithm: EncryptionAlgorithm
    key_id: str
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = None

class FieldEncryptionManager:
    """Field encryption manager."""
    
    def __init__(
        self,
        keys_dir: str = "keys",
        salt: Optional[bytes] = None,
        iterations: int = 100000
    ):
        """Initialize field encryption manager.
        
        Args:
            keys_dir: Keys directory
            salt: Salt for key derivation
            iterations: Number of iterations for key derivation
        """
        self.keys_dir = keys_dir
        self.salt = salt or os.urandom(16)
        self.iterations = iterations
        
        # Create keys directory if it doesn't exist
        os.makedirs(keys_dir, exist_ok=True)
        
        # Initialize key store
        self._keys: Dict[str, EncryptionKey] = {}
    
    def _get_key_file(
        self,
        key_id: str
    ) -> str:
        """Get key file path.
        
        Args:
            key_id: Key ID
            
        Returns:
            Key file path
        """
        return os.path.join(
            self.keys_dir,
            f"{key_id}.json"
        )
    
    def _load_key(
        self,
        key_id: str
    ) -> Optional[EncryptionKey]:
        """Load encryption key.
        
        Args:
            key_id: Key ID
            
        Returns:
            Encryption key if found, None otherwise
        """
        # Check if key is in memory
        if key_id in self._keys:
            return self._keys[key_id]
        
        key_file = self._get_key_file(key_id)
        
        if not os.path.exists(key_file):
            return None
        
        with open(key_file, "r") as f:
            data = json.load(f)
        
        key = EncryptionKey(
            key=base64.b64decode(data["key"]),
            algorithm=EncryptionAlgorithm(data["algorithm"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            expires_at=datetime.fromisoformat(data["expires_at"]) if data["expires_at"] else None,
            metadata=data["metadata"]
        )
        
        # Cache key
        self._keys[key_id] = key
        
        return key
    
    def _save_key(
        self,
        key_id: str,
        key: EncryptionKey
    ) -> None:
        """Save encryption key.
        
        Args:
            key_id: Key ID
            key: Encryption key
        """
        key_file = self._get_key_file(key_id)
        
        data = {
            "key": base64.b64encode(key.key).decode(),
            "algorithm": key.algorithm.value,
            "created_at": key.created_at.isoformat(),
            "expires_at": key.expires_at.isoformat() if key.expires_at else None,
            "metadata": key.metadata
        }
        
        with open(key_file, "w") as f:
            json.dump(data, f, indent=2)
        
        # Cache key
        self._keys[key_id] = key
    
    def _derive_key(
        self,
        password: str,
        algorithm: EncryptionAlgorithm
    ) -> bytes:
        """Derive encryption key from password.
        
        Args:
            password: Password
            algorithm: Encryption algorithm
            
        Returns:
            Derived key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=self.iterations
        )
        
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
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
        if self._load_key(key_id):
            raise ValueError(f"Key already exists: {key_id}")
        
        if password:
            key = self._derive_key(password, algorithm)
        else:
            key = Fernet.generate_key()
        
        encryption_key = EncryptionKey(
            key=key,
            algorithm=algorithm,
            created_at=datetime.utcnow(),
            expires_at=expires_at,
            metadata=metadata
        )
        
        self._save_key(key_id, encryption_key)
        
        logger.info(f"Generated key: {key_id}")
        
        return encryption_key
    
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
        return self._load_key(key_id)
    
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
        if not self._load_key(key_id):
            raise ValueError(f"Key doesn't exist: {key_id}")
        
        key_file = self._get_key_file(key_id)
        os.remove(key_file)
        
        # Remove from cache
        if key_id in self._keys:
            del self._keys[key_id]
        
        logger.info(f"Deleted key: {key_id}")
    
    def encrypt_field(
        self,
        value: Any,
        key_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> EncryptedField:
        """Encrypt field value.
        
        Args:
            value: Field value
            key_id: Key ID
            metadata: Additional metadata
            
        Returns:
            Encrypted field
            
        Raises:
            ValueError: If key doesn't exist or is expired
        """
        key = self._load_key(key_id)
        
        if not key:
            raise ValueError(f"Key doesn't exist: {key_id}")
        
        # Check if key is expired
        if key.expires_at and key.expires_at < datetime.utcnow():
            raise ValueError(f"Key is expired: {key_id}")
        
        # Convert value to string
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        else:
            value = str(value)
        
        # Encrypt value
        if key.algorithm == EncryptionAlgorithm.FERNET:
            fernet = Fernet(key.key)
            encrypted_value = fernet.encrypt(value.encode())
        else:
            raise ValueError(f"Unsupported algorithm: {key.algorithm}")
        
        return EncryptedField(
            value=base64.b64encode(encrypted_value).decode(),
            algorithm=key.algorithm,
            key_id=key_id,
            created_at=datetime.utcnow(),
            metadata=metadata
        )
    
    def decrypt_field(
        self,
        field: EncryptedField,
        value_type: Optional[Type[T]] = None
    ) -> Union[str, T]:
        """Decrypt field value.
        
        Args:
            field: Encrypted field
            value_type: Value type
            
        Returns:
            Decrypted value
            
        Raises:
            ValueError: If key doesn't exist or is expired
        """
        key = self._load_key(field.key_id)
        
        if not key:
            raise ValueError(f"Key doesn't exist: {field.key_id}")
        
        # Check if key is expired
        if key.expires_at and key.expires_at < datetime.utcnow():
            raise ValueError(f"Key is expired: {field.key_id}")
        
        # Decrypt value
        if field.algorithm == EncryptionAlgorithm.FERNET:
            fernet = Fernet(key.key)
            decrypted_value = fernet.decrypt(
                base64.b64decode(field.value)
            ).decode()
        else:
            raise ValueError(f"Unsupported algorithm: {field.algorithm}")
        
        # Convert value to type
        if value_type:
            if value_type == dict:
                return json.loads(decrypted_value)
            elif value_type == list:
                return json.loads(decrypted_value)
            else:
                return value_type(decrypted_value)
        
        return decrypted_value
    
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
        old_key = self._load_key(key_id)
        
        if not old_key:
            raise ValueError(f"Key doesn't exist: {key_id}")
        
        if self._load_key(new_key_id):
            raise ValueError(f"Key already exists: {new_key_id}")
        
        # Generate new key
        new_key = self.generate_key(
            key_id=new_key_id,
            algorithm=old_key.algorithm,
            expires_at=old_key.expires_at,
            metadata=metadata
        )
        
        # Delete old key
        self.delete_key(key_id)
        
        logger.info(f"Rotated key {key_id} to {new_key_id}")
        
        return new_key
    
    def get_key_stats(
        self
    ) -> Dict[str, Any]:
        """Get key statistics.
        
        Returns:
            Key statistics dictionary
        """
        stats = {
            "total_keys": 0,
            "algorithms": {
                algorithm.value: 0
                for algorithm in EncryptionAlgorithm
            },
            "expired_keys": 0
        }
        
        # Get current time
        now = datetime.utcnow()
        
        # Iterate through key files
        for key_file in Path(self.keys_dir).glob("*.json"):
            with open(key_file, "r") as f:
                data = json.load(f)
            
            stats["total_keys"] += 1
            stats["algorithms"][data["algorithm"]] += 1
            
            # Check if key is expired
            if data["expires_at"]:
                expires_at = datetime.fromisoformat(data["expires_at"])
                
                if expires_at < now:
                    stats["expired_keys"] += 1
        
        return stats
    
    def export_keys(
        self,
        format: str = "json"
    ) -> str:
        """Export keys.
        
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
        export_dir = os.path.join(self.keys_dir, "exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # Create export file path
        export_file = os.path.join(
            export_dir,
            f"keys_{datetime.now().strftime('%Y%m%d')}.{format}"
        )
        
        # Export keys
        keys_data = {}
        
        for key_file in Path(self.keys_dir).glob("*.json"):
            if key_file.name == "exports":
                continue
            
            with open(key_file, "r") as f:
                data = json.load(f)
            
            keys_data[key_file.stem] = data
        
        with open(export_file, "w") as f:
            json.dump(keys_data, f, indent=2)
        
        return export_file
    
    def cleanup_keys(
        self,
        max_age_days: int = 365
    ) -> None:
        """Clean up old keys.
        
        Args:
            max_age_days: Maximum age in days
        """
        # Get current time
        now = datetime.utcnow()
        
        # Iterate through key files
        for key_file in Path(self.keys_dir).glob("*.json"):
            if key_file.name == "exports":
                continue
            
            with open(key_file, "r") as f:
                data = json.load(f)
            
            # Check if key is old
            created_at = datetime.fromisoformat(data["created_at"])
            
            if (now - created_at).days > max_age_days:
                os.remove(key_file)
                
                # Remove from cache
                key_id = key_file.stem
                if key_id in self._keys:
                    del self._keys[key_id]
                
                logger.info(f"Removed old key file: {key_file}") 