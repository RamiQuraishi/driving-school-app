"""
User service module handling user-related operations.
This module manages user creation, retrieval, and updates.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models.user import User
from ..core.auth import AuthCore

class UserService:
    """Service for managing users."""
    
    def __init__(self, db: Session, auth_core: AuthCore):
        """
        Initialize the UserService.
        
        Args:
            db: Database session
            auth_core: Authentication core instance
        """
        self.db = db
        self.auth_core = auth_core

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their ID.
        
        Args:
            user_id: The ID of the user to retrieve
            
        Returns:
            Optional[User]: The user if found, None otherwise
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email.
        
        Args:
            email: The email of the user to retrieve
            
        Returns:
            Optional[User]: The user if found, None otherwise
        """
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, email: str, password: str, **kwargs) -> User:
        """
        Create a new user.
        
        Args:
            email: User's email
            password: User's plain text password
            **kwargs: Additional user attributes
            
        Returns:
            User: The created user
            
        Raises:
            HTTPException: If user with email already exists
        """
        if self.get_user_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
            
        hashed_password = self.auth_core.get_password_hash(password)
        user = User(email=email, hashed_password=hashed_password, **kwargs)
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        """
        Update a user's information.
        
        Args:
            user_id: The ID of the user to update
            **kwargs: The attributes to update
            
        Returns:
            Optional[User]: The updated user if found, None otherwise
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return None
            
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
                
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user.
        
        Args:
            user_id: The ID of the user to delete
            
        Returns:
            bool: True if user was deleted, False if not found
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return False
            
        self.db.delete(user)
        self.db.commit()
        return True 