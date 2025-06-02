"""
Session Management Module

This module provides secure session management functionality.
It handles user sessions, session tokens, and session security.

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
import hashlib
import hmac

logger = logging.getLogger(__name__)

class SessionStatus(Enum):
    """Session status."""
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    SUSPENDED = "suspended"

@dataclass
class Session:
    """Session."""
    session_id: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    last_activity: datetime
    status: SessionStatus
    ip_address: str
    user_agent: str
    metadata: Optional[Dict[str, Any]] = None

class SessionManager:
    """Session manager."""
    
    def __init__(
        self,
        sessions_dir: str = "sessions",
        session_timeout: int = 3600,
        max_sessions: int = 5,
        secret_key: Optional[bytes] = None
    ):
        """Initialize session manager.
        
        Args:
            sessions_dir: Sessions directory
            session_timeout: Session timeout in seconds
            max_sessions: Maximum number of active sessions per user
            secret_key: Secret key for session token generation
        """
        self.sessions_dir = sessions_dir
        self.session_timeout = session_timeout
        self.max_sessions = max_sessions
        self.secret_key = secret_key or secrets.token_bytes(32)
        
        # Create sessions directory if it doesn't exist
        os.makedirs(sessions_dir, exist_ok=True)
    
    def _get_session_file(
        self,
        session_id: str
    ) -> str:
        """Get session file path.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session file path
        """
        return os.path.join(
            self.sessions_dir,
            f"{session_id}.json"
        )
    
    def _get_user_sessions_file(
        self,
        user_id: str
    ) -> str:
        """Get user sessions file path.
        
        Args:
            user_id: User ID
            
        Returns:
            User sessions file path
        """
        return os.path.join(
            self.sessions_dir,
            "users",
            f"{user_id}.json"
        )
    
    def _load_session(
        self,
        session_id: str
    ) -> Optional[Session]:
        """Load session.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session if found, None otherwise
        """
        session_file = self._get_session_file(session_id)
        
        if not os.path.exists(session_file):
            return None
        
        with open(session_file, "r") as f:
            data = json.load(f)
        
        return Session(
            session_id=data["session_id"],
            user_id=data["user_id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            expires_at=datetime.fromisoformat(data["expires_at"]),
            last_activity=datetime.fromisoformat(data["last_activity"]),
            status=SessionStatus(data["status"]),
            ip_address=data["ip_address"],
            user_agent=data["user_agent"],
            metadata=data["metadata"]
        )
    
    def _save_session(
        self,
        session: Session
    ) -> None:
        """Save session.
        
        Args:
            session: Session
        """
        session_file = self._get_session_file(session.session_id)
        
        data = {
            "session_id": session.session_id,
            "user_id": session.user_id,
            "created_at": session.created_at.isoformat(),
            "expires_at": session.expires_at.isoformat(),
            "last_activity": session.last_activity.isoformat(),
            "status": session.status.value,
            "ip_address": session.ip_address,
            "user_agent": session.user_agent,
            "metadata": session.metadata
        }
        
        with open(session_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def _load_user_sessions(
        self,
        user_id: str
    ) -> List[str]:
        """Load user sessions.
        
        Args:
            user_id: User ID
            
        Returns:
            List of session IDs
        """
        user_sessions_file = self._get_user_sessions_file(user_id)
        
        if not os.path.exists(user_sessions_file):
            return []
        
        with open(user_sessions_file, "r") as f:
            data = json.load(f)
        
        return data
    
    def _save_user_sessions(
        self,
        user_id: str,
        session_ids: List[str]
    ) -> None:
        """Save user sessions.
        
        Args:
            user_id: User ID
            session_ids: List of session IDs
        """
        user_sessions_file = self._get_user_sessions_file(user_id)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(user_sessions_file), exist_ok=True)
        
        with open(user_sessions_file, "w") as f:
            json.dump(session_ids, f, indent=2)
    
    def _generate_session_id(
        self,
        user_id: str,
        ip_address: str,
        user_agent: str
    ) -> str:
        """Generate session ID.
        
        Args:
            user_id: User ID
            ip_address: IP address
            user_agent: User agent
            
        Returns:
            Session ID
        """
        # Create message
        message = f"{user_id}:{ip_address}:{user_agent}:{datetime.utcnow().isoformat()}"
        
        # Generate HMAC
        h = hmac.new(self.secret_key, message.encode(), hashlib.sha256)
        
        return h.hexdigest()
    
    def create_session(
        self,
        user_id: str,
        ip_address: str,
        user_agent: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Session:
        """Create session.
        
        Args:
            user_id: User ID
            ip_address: IP address
            user_agent: User agent
            metadata: Additional metadata
            
        Returns:
            Created session
            
        Raises:
            ValueError: If maximum number of sessions reached
        """
        # Get user sessions
        session_ids = self._load_user_sessions(user_id)
        
        # Check maximum sessions
        if len(session_ids) >= self.max_sessions:
            raise ValueError(f"Maximum number of sessions reached for user {user_id}")
        
        # Generate session ID
        session_id = self._generate_session_id(user_id, ip_address, user_agent)
        
        # Create session
        now = datetime.utcnow()
        
        session = Session(
            session_id=session_id,
            user_id=user_id,
            created_at=now,
            expires_at=now + timedelta(seconds=self.session_timeout),
            last_activity=now,
            status=SessionStatus.ACTIVE,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata=metadata
        )
        
        # Save session
        self._save_session(session)
        
        # Add to user sessions
        session_ids.append(session_id)
        self._save_user_sessions(user_id, session_ids)
        
        logger.info(f"Created session {session_id} for user {user_id}")
        
        return session
    
    def get_session(
        self,
        session_id: str
    ) -> Optional[Session]:
        """Get session.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session if found and valid, None otherwise
        """
        session = self._load_session(session_id)
        
        if not session:
            return None
        
        # Check if session is expired
        if session.expires_at < datetime.utcnow():
            session.status = SessionStatus.EXPIRED
            self._save_session(session)
            return None
        
        # Check if session is revoked
        if session.status == SessionStatus.REVOKED:
            return None
        
        return session
    
    def update_session(
        self,
        session_id: str
    ) -> Optional[Session]:
        """Update session.
        
        Args:
            session_id: Session ID
            
        Returns:
            Updated session if found and valid, None otherwise
        """
        session = self.get_session(session_id)
        
        if not session:
            return None
        
        # Update last activity
        session.last_activity = datetime.utcnow()
        session.expires_at = session.last_activity + timedelta(seconds=self.session_timeout)
        
        self._save_session(session)
        
        return session
    
    def revoke_session(
        self,
        session_id: str
    ) -> None:
        """Revoke session.
        
        Args:
            session_id: Session ID
        """
        session = self._load_session(session_id)
        
        if not session:
            return
        
        # Update status
        session.status = SessionStatus.REVOKED
        
        self._save_session(session)
        
        # Remove from user sessions
        session_ids = self._load_user_sessions(session.user_id)
        session_ids.remove(session_id)
        self._save_user_sessions(session.user_id, session_ids)
        
        logger.info(f"Revoked session {session_id}")
    
    def revoke_user_sessions(
        self,
        user_id: str
    ) -> None:
        """Revoke all user sessions.
        
        Args:
            user_id: User ID
        """
        session_ids = self._load_user_sessions(user_id)
        
        for session_id in session_ids:
            self.revoke_session(session_id)
        
        logger.info(f"Revoked all sessions for user {user_id}")
    
    def get_user_sessions(
        self,
        user_id: str
    ) -> List[Session]:
        """Get user sessions.
        
        Args:
            user_id: User ID
            
        Returns:
            List of sessions
        """
        session_ids = self._load_user_sessions(user_id)
        
        sessions = []
        
        for session_id in session_ids:
            session = self.get_session(session_id)
            
            if session:
                sessions.append(session)
        
        return sessions
    
    def cleanup_sessions(
        self,
        max_age_days: int = 30
    ) -> None:
        """Clean up old sessions.
        
        Args:
            max_age_days: Maximum age in days
        """
        # Get current time
        now = datetime.utcnow()
        
        # Iterate through session files
        for session_file in Path(self.sessions_dir).glob("*.json"):
            if session_file.name == "users":
                continue
            
            with open(session_file, "r") as f:
                data = json.load(f)
            
            # Check if session is old
            created_at = datetime.fromisoformat(data["created_at"])
            
            if (now - created_at).days > max_age_days:
                os.remove(session_file)
                
                # Remove from user sessions
                session_ids = self._load_user_sessions(data["user_id"])
                session_ids.remove(data["session_id"])
                self._save_user_sessions(data["user_id"], session_ids)
                
                logger.info(f"Removed old session file: {session_file}")
    
    def get_session_stats(
        self
    ) -> Dict[str, Any]:
        """Get session statistics.
        
        Returns:
            Session statistics dictionary
        """
        stats = {
            "total_sessions": 0,
            "active_sessions": 0,
            "expired_sessions": 0,
            "revoked_sessions": 0,
            "suspended_sessions": 0,
            "users": {}
        }
        
        # Iterate through session files
        for session_file in Path(self.sessions_dir).glob("*.json"):
            if session_file.name == "users":
                continue
            
            with open(session_file, "r") as f:
                data = json.load(f)
            
            stats["total_sessions"] += 1
            stats["status"][data["status"]] += 1
            
            # Count user sessions
            user_id = data["user_id"]
            
            if user_id not in stats["users"]:
                stats["users"][user_id] = 0
            
            stats["users"][user_id] += 1
        
        return stats
    
    def export_sessions(
        self,
        format: str = "json"
    ) -> str:
        """Export sessions.
        
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
        export_dir = os.path.join(self.sessions_dir, "exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # Create export file path
        export_file = os.path.join(
            export_dir,
            f"sessions_{datetime.now().strftime('%Y%m%d')}.{format}"
        )
        
        # Export sessions
        sessions_data = {}
        
        for session_file in Path(self.sessions_dir).glob("*.json"):
            if session_file.name == "users":
                continue
            
            with open(session_file, "r") as f:
                data = json.load(f)
            
            sessions_data[data["session_id"]] = data
        
        with open(export_file, "w") as f:
            json.dump(sessions_data, f, indent=2)
        
        return export_file 