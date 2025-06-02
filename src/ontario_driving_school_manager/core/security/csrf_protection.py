"""
CSRF Protection Module

This module provides CSRF protection functionality.
It handles CSRF token generation, validation, and storage.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import secrets

logger = logging.getLogger(__name__)

class CSRFProtectionManager:
    """CSRF protection manager."""
    
    def __init__(self, token_store: Optional[Dict[str, Any]] = None):
        """Initialize CSRF protection manager.
        
        Args:
            token_store: Token store
        """
        self.token_store = token_store or {}
    
    def generate_token(
        self,
        user_id: int,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Generate CSRF token.
        
        Args:
            user_id: User ID
            expires_delta: Token expiration delta
            
        Returns:
            CSRF token
        """
        token = secrets.token_hex(32)
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=1)
        
        self.token_store[token] = {
            "user_id": user_id,
            "expire": expire,
            "created_at": datetime.utcnow()
        }
        
        return token
    
    def verify_token(
        self,
        token_id: str,
        token: str
    ) -> bool:
        """Verify CSRF token.
        
        Args:
            token_id: Token ID
            token: CSRF token
            
        Returns:
            True if valid, False otherwise
        """
        if token_id not in self.token_store:
            return False
        
        stored_token = self.token_store[token_id]
        
        if stored_token["expire"] < datetime.utcnow():
            del self.token_store[token_id]
            return False
        
        return token == token_id
    
    def delete_token(self, token_id: str) -> bool:
        """Delete CSRF token.
        
        Args:
            token_id: Token ID
            
        Returns:
            True if successful, False otherwise
        """
        if token_id not in self.token_store:
            return False
        
        del self.token_store[token_id]
        return True
    
    def cleanup_expired_tokens(self) -> int:
        """Clean up expired tokens.
        
        Returns:
            Number of tokens cleaned up
        """
        now = datetime.utcnow()
        expired = [
            token_id
            for token_id, token in self.token_store.items()
            if token["expire"] < now
        ]
        
        for token_id in expired:
            del self.token_store[token_id]
        
        return len(expired)
    
    def get_user_tokens(self, user_id: int) -> Dict[str, Dict[str, Any]]:
        """Get user tokens.
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary of token ID to token data
        """
        return {
            token_id: token
            for token_id, token in self.token_store.items()
            if token["user_id"] == user_id
        }
    
    def invalidate_user_tokens(self, user_id: int) -> int:
        """Invalidate user tokens.
        
        Args:
            user_id: User ID
            
        Returns:
            Number of tokens invalidated
        """
        tokens = self.get_user_tokens(user_id)
        
        for token_id in tokens:
            del self.token_store[token_id]
        
        return len(tokens) 