"""
Two-Factor Authentication Module

This module provides two-factor authentication functionality.
It handles TOTP generation, verification, and backup codes.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
from enum import Enum
from dataclasses import dataclass, asdict
import secrets
import base64
import hashlib
import hmac
import struct
import time
import qrcode
from io import BytesIO
import pyotp

logger = logging.getLogger(__name__)

class TwoFactorStatus(Enum):
    """Two-factor status."""
    ENABLED = "enabled"
    DISABLED = "disabled"
    PENDING = "pending"

@dataclass
class TwoFactorConfig:
    """Two-factor configuration."""
    user_id: str
    status: TwoFactorStatus
    secret: str
    backup_codes: List[str]
    created_at: datetime
    enabled_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

class TwoFactorAuthManager:
    """Two-factor authentication manager."""
    
    def __init__(self, secret_key: Optional[str] = None):
        """Initialize two-factor authentication manager.
        
        Args:
            secret_key: Secret key for TOTP generation
        """
        self.secret_key = secret_key or secrets.token_hex(32)
        self.backup_codes: Dict[int, List[str]] = {}
    
    def generate_totp_secret(self) -> str:
        """Generate TOTP secret.
        
        Returns:
            TOTP secret
        """
        return pyotp.random_base32()
    
    def generate_totp_uri(
        self,
        secret: str,
        username: str,
        issuer: str = "Rami Drive School"
    ) -> str:
        """Generate TOTP URI.
        
        Args:
            secret: TOTP secret
            username: Username
            issuer: Issuer name
            
        Returns:
            TOTP URI
        """
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(username, issuer_name=issuer)
    
    def verify_totp(
        self,
        secret: str,
        token: str
    ) -> bool:
        """Verify TOTP token.
        
        Args:
            secret: TOTP secret
            token: TOTP token
            
        Returns:
            True if valid, False otherwise
        """
        totp = pyotp.TOTP(secret)
        return totp.verify(token)
    
    def generate_backup_codes(
        self,
        user_id: int,
        count: int = 10
    ) -> List[str]:
        """Generate backup codes.
        
        Args:
            user_id: User ID
            count: Number of codes to generate
            
        Returns:
            List of backup codes
        """
        codes = []
        
        for _ in range(count):
            code = secrets.token_hex(4)
            codes.append(code)
        
        self.backup_codes[user_id] = codes
        
        return codes
    
    def verify_backup_code(
        self,
        user_id: int,
        code: str
    ) -> bool:
        """Verify backup code.
        
        Args:
            user_id: User ID
            code: Backup code
            
        Returns:
            True if valid, False otherwise
        """
        if user_id not in self.backup_codes:
            return False
        
        if code not in self.backup_codes[user_id]:
            return False
        
        # Remove used code
        self.backup_codes[user_id].remove(code)
        
        return True
    
    def get_remaining_backup_codes(
        self,
        user_id: int
    ) -> int:
        """Get number of remaining backup codes.
        
        Args:
            user_id: User ID
            
        Returns:
            Number of remaining backup codes
        """
        if user_id not in self.backup_codes:
            return 0
        
        return len(self.backup_codes[user_id])
    
    def verify_two_factor(
        self,
        user_id: int,
        totp: Optional[str] = None,
        backup_code: Optional[str] = None
    ) -> bool:
        """Verify two-factor authentication.
        
        Args:
            user_id: User ID
            totp: TOTP token
            backup_code: Backup code
            
        Returns:
            True if valid, False otherwise
        """
        if totp:
            # Get user's TOTP secret from database
            secret = self._get_user_totp_secret(user_id)
            
            if not secret:
                return False
            
            return self.verify_totp(secret, totp)
        
        if backup_code:
            return self.verify_backup_code(user_id, backup_code)
        
        return False
    
    def _get_user_totp_secret(self, user_id: int) -> Optional[str]:
        """Get user's TOTP secret.
        
        Args:
            user_id: User ID
            
        Returns:
            TOTP secret if found, None otherwise
        """
        # TODO: Get from database
        return None
    
    def _save_user_totp_secret(
        self,
        user_id: int,
        secret: str
    ) -> None:
        """Save user's TOTP secret.
        
        Args:
            user_id: User ID
            secret: TOTP secret
        """
        # TODO: Save to database
        pass
    
    def setup_two_factor(
        self,
        user_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Set up two-factor authentication.
        
        Args:
            user_id: User ID
            metadata: Additional metadata
            
        Returns:
            Setup information
            
        Raises:
            ValueError: If two-factor authentication already set up
        """
        if self._load_config(user_id):
            raise ValueError(f"Two-factor authentication already set up for user {user_id}")
        
        # Generate TOTP secret
        secret = self.generate_totp_secret()
        
        # Generate backup codes
        backup_codes = self.generate_backup_codes(int(user_id))
        
        # Create configuration
        config = TwoFactorConfig(
            user_id=user_id,
            status=TwoFactorStatus.PENDING,
            secret=secret,
            backup_codes=backup_codes,
            created_at=datetime.utcnow(),
            metadata=metadata
        )
        
        self._save_config(config)
        
        # Generate QR code
        qr_code = self._generate_qr_code(secret, user_id)
        
        logger.info(f"Set up two-factor authentication for user {user_id}")
        
        return {
            "secret": secret,
            "backup_codes": backup_codes,
            "qr_code": qr_code
        }
    
    def verify_setup(
        self,
        user_id: str,
        totp: str
    ) -> bool:
        """Verify two-factor authentication setup.
        
        Args:
            user_id: User ID
            totp: TOTP
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            ValueError: If two-factor authentication not set up
        """
        config = self._load_config(user_id)
        
        if not config:
            raise ValueError(f"Two-factor authentication not set up for user {user_id}")
        
        if config.status != TwoFactorStatus.PENDING:
            raise ValueError(f"Two-factor authentication already verified for user {user_id}")
        
        # Verify TOTP
        if not self.verify_totp(config.secret, totp):
            return False
        
        # Update status
        config.status = TwoFactorStatus.ENABLED
        config.enabled_at = datetime.utcnow()
        
        self._save_config(config)
        
        logger.info(f"Verified two-factor authentication setup for user {user_id}")
        
        return True
    
    def disable_two_factor(
        self,
        user_id: str,
        totp: Optional[str] = None,
        backup_code: Optional[str] = None
    ) -> None:
        """Disable two-factor authentication.
        
        Args:
            user_id: User ID
            totp: TOTP
            backup_code: Backup code
            
        Raises:
            ValueError: If two-factor authentication not set up or verification fails
        """
        config = self._load_config(user_id)
        
        if not config:
            raise ValueError(f"Two-factor authentication not set up for user {user_id}")
        
        if config.status != TwoFactorStatus.ENABLED:
            raise ValueError(f"Two-factor authentication not enabled for user {user_id}")
        
        # Verify TOTP or backup code
        if not self.verify_two_factor(int(user_id), totp, backup_code):
            raise ValueError("Invalid TOTP or backup code")
        
        # Update status
        config.status = TwoFactorStatus.DISABLED
        
        self._save_config(config)
        
        logger.info(f"Disabled two-factor authentication for user {user_id}")
    
    def regenerate_backup_codes(
        self,
        user_id: str,
        totp: Optional[str] = None,
        backup_code: Optional[str] = None
    ) -> List[str]:
        """Regenerate backup codes.
        
        Args:
            user_id: User ID
            totp: TOTP
            backup_code: Backup code
            
        Returns:
            List of new backup codes
            
        Raises:
            ValueError: If two-factor authentication not set up or verification fails
        """
        config = self._load_config(user_id)
        
        if not config:
            raise ValueError(f"Two-factor authentication not set up for user {user_id}")
        
        if config.status != TwoFactorStatus.ENABLED:
            raise ValueError(f"Two-factor authentication not enabled for user {user_id}")
        
        # Verify TOTP or backup code
        if not self.verify_two_factor(int(user_id), totp, backup_code):
            raise ValueError("Invalid TOTP or backup code")
        
        # Generate new backup codes
        backup_codes = self.generate_backup_codes(int(user_id))
        
        # Update configuration
        config.backup_codes = backup_codes
        
        self._save_config(config)
        
        logger.info(f"Regenerated backup codes for user {user_id}")
        
        return backup_codes
    
    def get_two_factor_status(
        self,
        user_id: str
    ) -> Optional[TwoFactorStatus]:
        """Get two-factor authentication status.
        
        Args:
            user_id: User ID
            
        Returns:
            Two-factor authentication status if set up, None otherwise
        """
        config = self._load_config(user_id)
        
        if not config:
            return None
        
        return config.status
    
    def get_two_factor_stats(
        self
    ) -> Dict[str, Any]:
        """Get two-factor authentication statistics.
        
        Returns:
            Two-factor authentication statistics dictionary
        """
        stats = {
            "total_users": 0,
            "status": {
                status.value: 0
                for status in TwoFactorStatus
            }
        }
        
        # Iterate through configuration files
        for config_file in Path(self.config_dir).glob("*.json"):
            with open(config_file, "r") as f:
                data = json.load(f)
            
            stats["total_users"] += 1
            stats["status"][data["status"]] += 1
        
        return stats
    
    def export_two_factor_data(
        self,
        format: str = "json"
    ) -> str:
        """Export two-factor authentication data.
        
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
        export_dir = os.path.join(self.config_dir, "exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # Create export file path
        export_file = os.path.join(
            export_dir,
            f"2fa_{datetime.now().strftime('%Y%m%d')}.{format}"
        )
        
        # Export data
        data = {}
        
        for config_file in Path(self.config_dir).glob("*.json"):
            with open(config_file, "r") as f:
                config_data = json.load(f)
            
            data[config_data["user_id"]] = config_data
        
        with open(export_file, "w") as f:
            json.dump(data, f, indent=2)
        
        return export_file 