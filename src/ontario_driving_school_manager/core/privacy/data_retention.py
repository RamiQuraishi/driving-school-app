"""
Data Retention Manager Module

This module provides data retention management functionality for PIPEDA compliance.
It handles data retention policies, cleanup, and compliance.

Author: Rami Drive School
Date: 2024
"""

import logging
from typing import Dict, Any, Optional, List, Union, Callable
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import shutil

logger = logging.getLogger(__name__)

class RetentionError(Exception):
    """Retention error."""
    pass

class RetentionPolicy:
    """Retention policy."""
    
    def __init__(
        self,
        name: str,
        description: str,
        retention_period: int,  # days
        data_types: List[str],
        cleanup_action: str = "delete",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Initialize retention policy.
        
        Args:
            name: Policy name
            description: Policy description
            retention_period: Retention period in days
            data_types: List of data types
            cleanup_action: Cleanup action (delete, archive, anonymize)
            metadata: Additional metadata
        """
        self.name = name
        self.description = description
        self.retention_period = retention_period
        self.data_types = data_types
        self.cleanup_action = cleanup_action
        self.metadata = metadata or {}
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

class DataRetentionManager:
    """Data retention manager."""
    
    def __init__(
        self,
        policies_dir: str = "policies",
        data_dir: str = "data",
        archive_dir: str = "archives"
    ):
        """Initialize data retention manager.
        
        Args:
            policies_dir: Policies directory
            data_dir: Data directory
            archive_dir: Archive directory
        """
        self.policies_dir = policies_dir
        self.data_dir = data_dir
        self.archive_dir = archive_dir
        
        # Create directories if they don't exist
        os.makedirs(policies_dir, exist_ok=True)
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(archive_dir, exist_ok=True)
        
        # Load policies
        self.policies = self._load_policies()
    
    def _load_policies(self) -> Dict[str, RetentionPolicy]:
        """Load retention policies.
        
        Returns:
            Dictionary of policies by name
        """
        policies = {}
        
        try:
            # Iterate through policies directory
            for policy_file in Path(self.policies_dir).glob("*.json"):
                with open(policy_file, "r") as f:
                    policy_data = json.load(f)
                    
                    policy = RetentionPolicy(
                        name=policy_data["name"],
                        description=policy_data["description"],
                        retention_period=policy_data["retention_period"],
                        data_types=policy_data["data_types"],
                        cleanup_action=policy_data["cleanup_action"],
                        metadata=policy_data.get("metadata")
                    )
                    
                    policies[policy.name] = policy
        except Exception as e:
            logger.error(f"Error loading policies: {str(e)}")
        
        return policies
    
    def add_policy(
        self,
        policy: RetentionPolicy
    ) -> None:
        """Add retention policy.
        
        Args:
            policy: Retention policy
            
        Raises:
            RetentionError: If policy already exists
        """
        if policy.name in self.policies:
            raise RetentionError(f"Policy already exists: {policy.name}")
        
        try:
            # Create policy file
            policy_file = os.path.join(
                self.policies_dir,
                f"{policy.name}.json"
            )
            
            # Write policy data
            policy_data = {
                "name": policy.name,
                "description": policy.description,
                "retention_period": policy.retention_period,
                "data_types": policy.data_types,
                "cleanup_action": policy.cleanup_action,
                "metadata": policy.metadata,
                "created_at": policy.created_at.isoformat(),
                "updated_at": policy.updated_at.isoformat()
            }
            
            with open(policy_file, "w") as f:
                json.dump(policy_data, f, indent=2)
            
            # Add policy to dictionary
            self.policies[policy.name] = policy
            
            logger.info(f"Added retention policy: {policy.name}")
        except Exception as e:
            raise RetentionError(f"Error adding policy: {str(e)}")
    
    def update_policy(
        self,
        policy: RetentionPolicy
    ) -> None:
        """Update retention policy.
        
        Args:
            policy: Retention policy
            
        Raises:
            RetentionError: If policy doesn't exist
        """
        if policy.name not in self.policies:
            raise RetentionError(f"Policy doesn't exist: {policy.name}")
        
        try:
            # Update policy
            policy.updated_at = datetime.utcnow()
            self.policies[policy.name] = policy
            
            # Update policy file
            policy_file = os.path.join(
                self.policies_dir,
                f"{policy.name}.json"
            )
            
            policy_data = {
                "name": policy.name,
                "description": policy.description,
                "retention_period": policy.retention_period,
                "data_types": policy.data_types,
                "cleanup_action": policy.cleanup_action,
                "metadata": policy.metadata,
                "created_at": policy.created_at.isoformat(),
                "updated_at": policy.updated_at.isoformat()
            }
            
            with open(policy_file, "w") as f:
                json.dump(policy_data, f, indent=2)
            
            logger.info(f"Updated retention policy: {policy.name}")
        except Exception as e:
            raise RetentionError(f"Error updating policy: {str(e)}")
    
    def remove_policy(
        self,
        policy_name: str
    ) -> None:
        """Remove retention policy.
        
        Args:
            policy_name: Policy name
            
        Raises:
            RetentionError: If policy doesn't exist
        """
        if policy_name not in self.policies:
            raise RetentionError(f"Policy doesn't exist: {policy_name}")
        
        try:
            # Remove policy file
            policy_file = os.path.join(
                self.policies_dir,
                f"{policy_name}.json"
            )
            
            os.remove(policy_file)
            
            # Remove policy from dictionary
            del self.policies[policy_name]
            
            logger.info(f"Removed retention policy: {policy_name}")
        except Exception as e:
            raise RetentionError(f"Error removing policy: {str(e)}")
    
    def get_policy(
        self,
        policy_name: str
    ) -> Optional[RetentionPolicy]:
        """Get retention policy.
        
        Args:
            policy_name: Policy name
            
        Returns:
            Retention policy if found, None otherwise
        """
        return self.policies.get(policy_name)
    
    def get_policies(
        self,
        data_type: Optional[str] = None
    ) -> List[RetentionPolicy]:
        """Get retention policies.
        
        Args:
            data_type: Data type
            
        Returns:
            List of retention policies
        """
        if data_type:
            return [
                policy for policy in self.policies.values()
                if data_type in policy.data_types
            ]
        else:
            return list(self.policies.values())
    
    def apply_policy(
        self,
        policy_name: str,
        data_path: str
    ) -> None:
        """Apply retention policy.
        
        Args:
            policy_name: Policy name
            data_path: Data path
            
        Raises:
            RetentionError: If policy doesn't exist
        """
        policy = self.get_policy(policy_name)
        
        if not policy:
            raise RetentionError(f"Policy doesn't exist: {policy_name}")
        
        try:
            # Get data age
            data_age = datetime.utcnow() - datetime.fromtimestamp(
                os.path.getmtime(data_path)
            )
            
            # Check if data should be cleaned up
            if data_age.days > policy.retention_period:
                if policy.cleanup_action == "delete":
                    os.remove(data_path)
                elif policy.cleanup_action == "archive":
                    # Create archive directory
                    archive_path = os.path.join(
                        self.archive_dir,
                        policy.name,
                        os.path.basename(data_path)
                    )
                    
                    os.makedirs(os.path.dirname(archive_path), exist_ok=True)
                    
                    # Move data to archive
                    shutil.move(data_path, archive_path)
                elif policy.cleanup_action == "anonymize":
                    # Anonymize data
                    self._anonymize_data(data_path)
                
                logger.info(
                    f"Applied {policy.name} policy to {data_path}"
                )
        except Exception as e:
            raise RetentionError(f"Error applying policy: {str(e)}")
    
    def _anonymize_data(
        self,
        data_path: str
    ) -> None:
        """Anonymize data.
        
        Args:
            data_path: Data path
        """
        try:
            # Read data
            with open(data_path, "r") as f:
                data = json.load(f)
            
            # Anonymize data
            if isinstance(data, dict):
                for key in data:
                    if isinstance(data[key], str):
                        data[key] = "***"
                    elif isinstance(data[key], dict):
                        self._anonymize_data(data[key])
                    elif isinstance(data[key], list):
                        for item in data[key]:
                            if isinstance(item, dict):
                                self._anonymize_data(item)
            
            # Write anonymized data
            with open(data_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error anonymizing data: {str(e)}")
    
    def cleanup_data(
        self,
        policy_name: Optional[str] = None
    ) -> None:
        """Clean up data.
        
        Args:
            policy_name: Policy name
        """
        try:
            # Get policies to apply
            policies = (
                [self.get_policy(policy_name)]
                if policy_name
                else self.get_policies()
            )
            
            # Apply policies
            for policy in policies:
                if not policy:
                    continue
                
                # Get data files
                for data_type in policy.data_types:
                    data_dir = os.path.join(self.data_dir, data_type)
                    
                    if not os.path.exists(data_dir):
                        continue
                    
                    # Apply policy to data files
                    for data_file in Path(data_dir).glob("*"):
                        if data_file.is_file():
                            self.apply_policy(policy.name, str(data_file))
        except Exception as e:
            logger.error(f"Error cleaning up data: {str(e)}")
    
    def get_retention_stats(
        self,
        policy_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get retention statistics.
        
        Args:
            policy_name: Policy name
            
        Returns:
            Retention statistics dictionary
        """
        try:
            stats = {
                "total_policies": len(self.policies),
                "total_data_types": len(set(
                    data_type
                    for policy in self.policies.values()
                    for data_type in policy.data_types
                )),
                "policies": {}
            }
            
            # Get policies to include
            policies = (
                [self.get_policy(policy_name)]
                if policy_name
                else self.get_policies()
            )
            
            # Get policy statistics
            for policy in policies:
                if not policy:
                    continue
                
                policy_stats = {
                    "name": policy.name,
                    "description": policy.description,
                    "retention_period": policy.retention_period,
                    "data_types": policy.data_types,
                    "cleanup_action": policy.cleanup_action,
                    "created_at": policy.created_at.isoformat(),
                    "updated_at": policy.updated_at.isoformat(),
                    "data_files": 0,
                    "archived_files": 0
                }
                
                # Count data files
                for data_type in policy.data_types:
                    data_dir = os.path.join(self.data_dir, data_type)
                    
                    if os.path.exists(data_dir):
                        policy_stats["data_files"] += len(list(
                            Path(data_dir).glob("*")
                        ))
                
                # Count archived files
                archive_dir = os.path.join(
                    self.archive_dir,
                    policy.name
                )
                
                if os.path.exists(archive_dir):
                    policy_stats["archived_files"] += len(list(
                        Path(archive_dir).glob("*")
                    ))
                
                stats["policies"][policy.name] = policy_stats
            
            return stats
        except Exception as e:
            raise RetentionError(f"Error getting retention stats: {str(e)}")
    
    def export_policies(
        self,
        format: str = "json"
    ) -> str:
        """Export retention policies.
        
        Args:
            format: Export format
            
        Returns:
            Path to exported file
            
        Raises:
            RetentionError: If export fails
        """
        try:
            # Create export directory
            export_dir = os.path.join(self.policies_dir, "exports")
            os.makedirs(export_dir, exist_ok=True)
            
            # Create export file path
            export_file = os.path.join(
                export_dir,
                f"policies_{datetime.now().strftime('%Y%m%d')}.{format}"
            )
            
            # Export policies
            if format == "json":
                policies_data = {
                    policy.name: {
                        "name": policy.name,
                        "description": policy.description,
                        "retention_period": policy.retention_period,
                        "data_types": policy.data_types,
                        "cleanup_action": policy.cleanup_action,
                        "metadata": policy.metadata,
                        "created_at": policy.created_at.isoformat(),
                        "updated_at": policy.updated_at.isoformat()
                    }
                    for policy in self.policies.values()
                }
                
                with open(export_file, "w") as f:
                    json.dump(policies_data, f, indent=2)
            else:
                raise RetentionError(f"Unsupported format: {format}")
            
            return export_file
        except Exception as e:
            raise RetentionError(f"Error exporting policies: {str(e)}") 