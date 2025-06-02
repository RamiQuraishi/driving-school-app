"""
Role-Based Access Control (RBAC) Manager Module

This module provides role-based access control functionality.
It handles user roles, permissions, and access control.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Dict, Any, Optional, List, Union, Set
from datetime import datetime
import json
import os
from pathlib import Path
from enum import Enum
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

class Permission(Enum):
    """Permission."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

class Resource(Enum):
    """Resource."""
    USER = "user"
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    LESSON = "lesson"
    VEHICLE = "vehicle"
    PAYMENT = "payment"
    REPORT = "report"
    SETTING = "setting"

@dataclass
class Role:
    """Role."""
    name: str
    description: str
    permissions: Dict[str, Set[Permission]]
    created_at: datetime
    updated_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class UserRole:
    """User role."""
    user_id: str
    role_name: str
    assigned_at: datetime
    assigned_by: str
    expires_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

class RBACManager:
    """RBAC manager."""
    
    def __init__(
        self,
        roles_dir: str = "roles",
        user_roles_dir: str = "user_roles"
    ):
        """Initialize RBAC manager.
        
        Args:
            roles_dir: Roles directory
            user_roles_dir: User roles directory
        """
        self.roles_dir = roles_dir
        self.user_roles_dir = user_roles_dir
        
        # Create directories if they don't exist
        os.makedirs(roles_dir, exist_ok=True)
        os.makedirs(user_roles_dir, exist_ok=True)
    
    def _get_role_file(
        self,
        role_name: str
    ) -> str:
        """Get role file path.
        
        Args:
            role_name: Role name
            
        Returns:
            Role file path
        """
        return os.path.join(
            self.roles_dir,
            f"{role_name}.json"
        )
    
    def _get_user_roles_file(
        self,
        user_id: str
    ) -> str:
        """Get user roles file path.
        
        Args:
            user_id: User ID
            
        Returns:
            User roles file path
        """
        return os.path.join(
            self.user_roles_dir,
            f"{user_id}.json"
        )
    
    def _load_role(
        self,
        role_name: str
    ) -> Optional[Role]:
        """Load role.
        
        Args:
            role_name: Role name
            
        Returns:
            Role if found, None otherwise
        """
        role_file = self._get_role_file(role_name)
        
        if not os.path.exists(role_file):
            return None
        
        with open(role_file, "r") as f:
            data = json.load(f)
        
        return Role(
            name=data["name"],
            description=data["description"],
            permissions={
                resource: {
                    Permission(permission)
                    for permission in permissions
                }
                for resource, permissions in data["permissions"].items()
            },
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]) if data["updated_at"] else None,
            metadata=data["metadata"]
        )
    
    def _save_role(
        self,
        role: Role
    ) -> None:
        """Save role.
        
        Args:
            role: Role
        """
        role_file = self._get_role_file(role.name)
        
        data = {
            "name": role.name,
            "description": role.description,
            "permissions": {
                resource: [
                    permission.value
                    for permission in permissions
                ]
                for resource, permissions in role.permissions.items()
            },
            "created_at": role.created_at.isoformat(),
            "updated_at": role.updated_at.isoformat() if role.updated_at else None,
            "metadata": role.metadata
        }
        
        with open(role_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def _load_user_roles(
        self,
        user_id: str
    ) -> List[UserRole]:
        """Load user roles.
        
        Args:
            user_id: User ID
            
        Returns:
            List of user roles
        """
        user_roles_file = self._get_user_roles_file(user_id)
        
        if not os.path.exists(user_roles_file):
            return []
        
        with open(user_roles_file, "r") as f:
            data = json.load(f)
        
        return [
            UserRole(
                user_id=record["user_id"],
                role_name=record["role_name"],
                assigned_at=datetime.fromisoformat(record["assigned_at"]),
                assigned_by=record["assigned_by"],
                expires_at=datetime.fromisoformat(record["expires_at"]) if record["expires_at"] else None,
                metadata=record["metadata"]
            )
            for record in data
        ]
    
    def _save_user_roles(
        self,
        user_id: str,
        user_roles: List[UserRole]
    ) -> None:
        """Save user roles.
        
        Args:
            user_id: User ID
            user_roles: List of user roles
        """
        user_roles_file = self._get_user_roles_file(user_id)
        
        data = [
            {
                "user_id": role.user_id,
                "role_name": role.role_name,
                "assigned_at": role.assigned_at.isoformat(),
                "assigned_by": role.assigned_by,
                "expires_at": role.expires_at.isoformat() if role.expires_at else None,
                "metadata": role.metadata
            }
            for role in user_roles
        ]
        
        with open(user_roles_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def create_role(
        self,
        name: str,
        description: str,
        permissions: Dict[str, Set[Permission]],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Role:
        """Create role.
        
        Args:
            name: Role name
            description: Role description
            permissions: Role permissions
            metadata: Additional metadata
            
        Returns:
            Created role
            
        Raises:
            ValueError: If role already exists
        """
        if self._load_role(name):
            raise ValueError(f"Role already exists: {name}")
        
        role = Role(
            name=name,
            description=description,
            permissions=permissions,
            created_at=datetime.utcnow(),
            metadata=metadata
        )
        
        self._save_role(role)
        
        logger.info(f"Created role: {name}")
        
        return role
    
    def get_role(
        self,
        name: str
    ) -> Optional[Role]:
        """Get role.
        
        Args:
            name: Role name
            
        Returns:
            Role if found, None otherwise
        """
        return self._load_role(name)
    
    def update_role(
        self,
        role: Role
    ) -> None:
        """Update role.
        
        Args:
            role: Role
            
        Raises:
            ValueError: If role doesn't exist
        """
        if not self._load_role(role.name):
            raise ValueError(f"Role doesn't exist: {role.name}")
        
        role.updated_at = datetime.utcnow()
        
        self._save_role(role)
        
        logger.info(f"Updated role: {role.name}")
    
    def delete_role(
        self,
        name: str
    ) -> None:
        """Delete role.
        
        Args:
            name: Role name
            
        Raises:
            ValueError: If role doesn't exist
        """
        if not self._load_role(name):
            raise ValueError(f"Role doesn't exist: {name}")
        
        role_file = self._get_role_file(name)
        os.remove(role_file)
        
        logger.info(f"Deleted role: {name}")
    
    def assign_role(
        self,
        user_id: str,
        role_name: str,
        assigned_by: str,
        expires_at: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Assign role to user.
        
        Args:
            user_id: User ID
            role_name: Role name
            assigned_by: User ID of assigner
            expires_at: Expiration timestamp
            metadata: Additional metadata
            
        Raises:
            ValueError: If role doesn't exist
        """
        if not self._load_role(role_name):
            raise ValueError(f"Role doesn't exist: {role_name}")
        
        user_roles = self._load_user_roles(user_id)
        
        # Check if role is already assigned
        for role in user_roles:
            if role.role_name == role_name:
                return
        
        user_roles.append(
            UserRole(
                user_id=user_id,
                role_name=role_name,
                assigned_at=datetime.utcnow(),
                assigned_by=assigned_by,
                expires_at=expires_at,
                metadata=metadata
            )
        )
        
        self._save_user_roles(user_id, user_roles)
        
        logger.info(f"Assigned role {role_name} to user {user_id}")
    
    def revoke_role(
        self,
        user_id: str,
        role_name: str
    ) -> None:
        """Revoke role from user.
        
        Args:
            user_id: User ID
            role_name: Role name
        """
        user_roles = self._load_user_roles(user_id)
        
        # Remove role
        user_roles = [
            role
            for role in user_roles
            if role.role_name != role_name
        ]
        
        self._save_user_roles(user_id, user_roles)
        
        logger.info(f"Revoked role {role_name} from user {user_id}")
    
    def get_user_roles(
        self,
        user_id: str
    ) -> List[UserRole]:
        """Get user roles.
        
        Args:
            user_id: User ID
            
        Returns:
            List of user roles
        """
        return self._load_user_roles(user_id)
    
    def check_permission(
        self,
        user_id: str,
        resource: Resource,
        permission: Permission
    ) -> bool:
        """Check if user has permission.
        
        Args:
            user_id: User ID
            resource: Resource
            permission: Permission
            
        Returns:
            True if user has permission, False otherwise
        """
        user_roles = self._load_user_roles(user_id)
        
        # Get current time
        now = datetime.utcnow()
        
        # Check each role
        for user_role in user_roles:
            # Skip expired roles
            if user_role.expires_at and user_role.expires_at < now:
                continue
            
            role = self._load_role(user_role.role_name)
            
            if not role:
                continue
            
            # Check permissions
            if (
                resource.value in role.permissions and
                permission in role.permissions[resource.value]
            ):
                return True
        
        return False
    
    def get_role_stats(
        self
    ) -> Dict[str, Any]:
        """Get role statistics.
        
        Returns:
            Role statistics dictionary
        """
        stats = {
            "total_roles": 0,
            "total_users": 0,
            "roles": {},
            "permissions": {
                resource.value: {
                    permission.value: 0
                    for permission in Permission
                }
                for resource in Resource
            }
        }
        
        # Iterate through role files
        for role_file in Path(self.roles_dir).glob("*.json"):
            with open(role_file, "r") as f:
                data = json.load(f)
            
            stats["total_roles"] += 1
            stats["roles"][data["name"]] = {
                "description": data["description"],
                "permissions": len(data["permissions"])
            }
            
            # Count permissions
            for resource, permissions in data["permissions"].items():
                for permission in permissions:
                    stats["permissions"][resource][permission] += 1
        
        # Iterate through user roles files
        for user_roles_file in Path(self.user_roles_dir).glob("*.json"):
            with open(user_roles_file, "r") as f:
                data = json.load(f)
            
            stats["total_users"] += 1
        
        return stats
    
    def export_roles(
        self,
        format: str = "json"
    ) -> str:
        """Export roles.
        
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
        export_dir = os.path.join(self.roles_dir, "exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # Create export file path
        export_file = os.path.join(
            export_dir,
            f"roles_{datetime.now().strftime('%Y%m%d')}.{format}"
        )
        
        # Export roles
        roles_data = {}
        
        for role_file in Path(self.roles_dir).glob("*.json"):
            if role_file.name == "exports":
                continue
            
            with open(role_file, "r") as f:
                data = json.load(f)
            
            roles_data[data["name"]] = data
        
        with open(export_file, "w") as f:
            json.dump(roles_data, f, indent=2)
        
        return export_file
    
    def export_user_roles(
        self,
        format: str = "json"
    ) -> str:
        """Export user roles.
        
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
        export_dir = os.path.join(self.user_roles_dir, "exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # Create export file path
        export_file = os.path.join(
            export_dir,
            f"user_roles_{datetime.now().strftime('%Y%m%d')}.{format}"
        )
        
        # Export user roles
        user_roles_data = {}
        
        for user_roles_file in Path(self.user_roles_dir).glob("*.json"):
            if user_roles_file.name == "exports":
                continue
            
            with open(user_roles_file, "r") as f:
                data = json.load(f)
            
            user_roles_data[user_roles_file.stem] = data
        
        with open(export_file, "w") as f:
            json.dump(user_roles_data, f, indent=2)
        
        return export_file
    
    def cleanup_roles(
        self,
        max_age_days: int = 365
    ) -> None:
        """Clean up old roles.
        
        Args:
            max_age_days: Maximum age in days
        """
        # Get current time
        now = datetime.utcnow()
        
        # Iterate through role files
        for role_file in Path(self.roles_dir).glob("*.json"):
            if role_file.name == "exports":
                continue
            
            with open(role_file, "r") as f:
                data = json.load(f)
            
            # Check if role is old
            created_at = datetime.fromisoformat(data["created_at"])
            
            if (now - created_at).days > max_age_days:
                os.remove(role_file)
                
                logger.info(f"Removed old role file: {role_file}")
    
    def cleanup_user_roles(
        self,
        max_age_days: int = 365
    ) -> None:
        """Clean up old user roles.
        
        Args:
            max_age_days: Maximum age in days
        """
        # Get current time
        now = datetime.utcnow()
        
        # Iterate through user roles files
        for user_roles_file in Path(self.user_roles_dir).glob("*.json"):
            if user_roles_file.name == "exports":
                continue
            
            with open(user_roles_file, "r") as f:
                data = json.load(f)
            
            # Check if all roles are old
            all_old = True
            
            for record in data:
                assigned_at = datetime.fromisoformat(record["assigned_at"])
                
                if (now - assigned_at).days <= max_age_days:
                    all_old = False
                    break
            
            # Remove old user roles file
            if all_old:
                os.remove(user_roles_file)
                
                logger.info(f"Removed old user roles file: {user_roles_file}") 