"""
Session service module handling user session operations.
This module manages user sessions, including creation, validation, and cleanup.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
import jwt

from ..core.auth import AuthCore
from .user_service import UserService

class SessionService:
    """Service for managing user sessions."""
    
    def __init__(self, auth_core: AuthCore, user_service: UserService):
        """
        Initialize the SessionService.
        
        Args:
            auth_core: Authentication core instance
            user_service: User service instance
        """
        self.auth_core = auth_core
        self.user_service = user_service

    def create_session(self, user_id: int, session_data: Dict[str, Any]) -> str:
        """
        Create a new session for a user.
        
        Args:
            user_id: The ID of the user
            session_data: Additional session data to store
            
        Returns:
            str: Session token
            
        Raises:
            HTTPException: If user not found
        """
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        session_token = self.auth_core.create_access_token(
            data={
                "sub": str(user_id),
                "type": "session",
                "session_data": session_data
            },
            expires_delta=timedelta(minutes=30)
        )
        
        return session_token

    def validate_session(self, session_token: str) -> Dict[str, Any]:
        """
        Validate a session token and return session data.
        
        Args:
            session_token: The session token to validate
            
        Returns:
            Dict[str, Any]: Session data if valid
            
        Raises:
            HTTPException: If session token is invalid
        """
        try:
            payload = self.auth_core.verify_token(session_token)
            if payload.get("type") != "session":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid session token"
                )
                
            user = self.user_service.get_user_by_id(int(payload["sub"]))
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )
                
            return {
                "user_id": user.id,
                "session_data": payload.get("session_data", {})
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate session"
            )

    def refresh_session(self, session_token: str) -> str:
        """
        Refresh a session token.
        
        Args:
            session_token: The current session token
            
        Returns:
            str: New session token
            
        Raises:
            HTTPException: If session token is invalid
        """
        try:
            payload = self.auth_core.verify_token(session_token)
            if payload.get("type") != "session":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid session token"
                )
                
            return self.create_session(
                int(payload["sub"]),
                payload.get("session_data", {})
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not refresh session"
            ) 