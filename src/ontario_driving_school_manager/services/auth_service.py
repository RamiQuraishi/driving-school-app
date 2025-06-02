"""
Authentication service module handling login and token operations.
This module manages user authentication and token generation/validation.
"""

from datetime import timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status

from ..core.auth import AuthCore
from .user_service import UserService

class AuthService:
    """Service for handling authentication operations."""
    
    def __init__(self, auth_core: AuthCore, user_service: UserService):
        """
        Initialize the AuthService.
        
        Args:
            auth_core: Authentication core instance
            user_service: User service instance
        """
        self.auth_core = auth_core
        self.user_service = user_service

    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user and return their information.
        
        Args:
            email: User's email
            password: User's password
            
        Returns:
            Optional[Dict[str, Any]]: User information if authenticated, None otherwise
        """
        user = self.user_service.get_user_by_email(email)
        if not user:
            return None
        if not self.auth_core.verify_password(password, user.hashed_password):
            return None
        return {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser
        }

    def create_tokens(self, user_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Create access and refresh tokens for a user.
        
        Args:
            user_data: User data to encode in tokens
            
        Returns:
            Dict[str, str]: Dictionary containing access and refresh tokens
        """
        access_token_expires = timedelta(minutes=30)
        refresh_token_expires = timedelta(days=7)
        
        access_token = self.auth_core.create_access_token(
            data=user_data,
            expires_delta=access_token_expires
        )
        
        refresh_token = self.auth_core.create_access_token(
            data={"sub": str(user_data["id"]), "type": "refresh"},
            expires_delta=refresh_token_expires
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def refresh_access_token(self, refresh_token: str) -> Dict[str, str]:
        """
        Create a new access token using a refresh token.
        
        Args:
            refresh_token: The refresh token
            
        Returns:
            Dict[str, str]: New access token
            
        Raises:
            HTTPException: If refresh token is invalid
        """
        try:
            payload = self.auth_core.verify_token(refresh_token)
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )
                
            user = self.user_service.get_user_by_id(int(payload["sub"]))
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )
                
            user_data = {
                "id": user.id,
                "email": user.email,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser
            }
            
            access_token = self.auth_core.create_access_token(
                data=user_data,
                expires_delta=timedelta(minutes=30)
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer"
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate refresh token"
            ) 