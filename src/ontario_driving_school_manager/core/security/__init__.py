"""
Security Module

This module provides security functionality for the Ontario Driving School Manager.
It includes authentication, authorization, encryption, and other security features.

Author: Rami Drive School
Date: 2024
Version: 1.0.0
"""

from .authentication import AuthenticationManager
from .authorization import AuthorizationManager
from .encryption import EncryptionManager
from .rbac import RBACManager
from .field_encryption import FieldEncryptionManager
from .audit_trail import AuditTrailManager
from .session_management import SessionManager
from .two_factor_auth import TwoFactorAuthManager
from .csrf_protection import CSRFProtectionManager
from .xss_prevention import XSSPreventionManager

__version__ = "1.0.0"
__all__ = [
    "AuthenticationManager",
    "AuthorizationManager",
    "EncryptionManager",
    "RBACManager",
    "FieldEncryptionManager",
    "AuditTrailManager",
    "SessionManager",
    "TwoFactorAuthManager",
    "CSRFProtectionManager",
    "XSSPreventionManager"
] 