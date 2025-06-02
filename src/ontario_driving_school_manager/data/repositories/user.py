"""
User Repository

This module provides the User repository for database operations.

Author: Rami Drive School
Date: 2024
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ...models.user import User

class UserRepository:
    """User repository."""
    
    def __init__(self, session: Session):
        """Initialize user repository.
        
        Args:
            session: Database session
        """
        self.session = session
    
    def create(self, user: User) -> User:
        """Create user.
        
        Args:
            user: User to create
            
        Returns:
            Created user
        """
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User if found, None otherwise
        """
        return self.session.query(User).filter(User.id == user_id).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username.
        
        Args:
            username: Username
            
        Returns:
            User if found, None otherwise
        """
        return self.session.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email.
        
        Args:
            email: Email
            
        Returns:
            User if found, None otherwise
        """
        return self.session.query(User).filter(User.email == email).first()
    
    def get_by_verification_token(self, token: str) -> Optional[User]:
        """Get user by verification token.
        
        Args:
            token: Verification token
            
        Returns:
            User if found, None otherwise
        """
        return self.session.query(User).filter(User.verification_token == token).first()
    
    def get_by_reset_token(self, token: str) -> Optional[User]:
        """Get user by reset token.
        
        Args:
            token: Reset token
            
        Returns:
            User if found, None otherwise
        """
        return self.session.query(User).filter(
            User.reset_token == token,
            User.reset_token_expires > datetime.utcnow()
        ).first()
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[User]:
        """Get all users.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Filter criteria
            
        Returns:
            List of users
        """
        query = self.session.query(User)
        
        if filters:
            for key, value in filters.items():
                if hasattr(User, key):
                    query = query.filter(getattr(User, key) == value)
        
        return query.offset(skip).limit(limit).all()
    
    def search(
        self,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Search users.
        
        Args:
            query: Search query
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of users
        """
        return self.session.query(User).filter(
            or_(
                User.username.ilike(f"%{query}%"),
                User.email.ilike(f"%{query}%"),
                User.first_name.ilike(f"%{query}%"),
                User.last_name.ilike(f"%{query}%")
            )
        ).offset(skip).limit(limit).all()
    
    def update(self, user: User) -> User:
        """Update user.
        
        Args:
            user: User to update
            
        Returns:
            Updated user
        """
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def delete(self, user: User) -> None:
        """Delete user.
        
        Args:
            user: User to delete
        """
        self.session.delete(user)
        self.session.commit()
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count users.
        
        Args:
            filters: Filter criteria
            
        Returns:
            Number of users
        """
        query = self.session.query(User)
        
        if filters:
            for key, value in filters.items():
                if hasattr(User, key):
                    query = query.filter(getattr(User, key) == value)
        
        return query.count() 