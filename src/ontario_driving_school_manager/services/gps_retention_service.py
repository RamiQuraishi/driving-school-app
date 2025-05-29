"""GPS data retention service for managing GPS tracking data lifecycle."""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from ..models import (
    GPSTracking,
    GPSRetentionPolicy,
    GPSRetentionLog
)

logger = logging.getLogger(__name__)

class GPSRetentionService:
    """Service for managing GPS data retention and cleanup."""
    
    def __init__(self, session: Session):
        """Initialize GPS retention service.
        
        Args:
            session: Database session
        """
        self.session = session
    
    def create_policy(
        self,
        name: str,
        description: str,
        retention_days: int,
        is_active: bool = True
    ) -> GPSRetentionPolicy:
        """Create a new retention policy.
        
        Args:
            name: Policy name
            description: Policy description
            retention_days: Number of days to retain data
            is_active: Whether policy is active
            
        Returns:
            GPSRetentionPolicy: Created policy
        """
        policy = GPSRetentionPolicy(
            name=name,
            description=description,
            retention_days=retention_days,
            is_active=is_active
        )
        
        self.session.add(policy)
        self.session.commit()
        
        logger.info(f"Created GPS retention policy: {name}")
        return policy
    
    def get_active_policies(self) -> List[GPSRetentionPolicy]:
        """Get all active retention policies.
        
        Returns:
            List[GPSRetentionPolicy]: Active policies
        """
        return self.session.query(GPSRetentionPolicy).filter(
            GPSRetentionPolicy.is_active == True
        ).all()
    
    def execute_policy(self, policy_id: int) -> Tuple[int, List[Dict]]:
        """Execute a retention policy.
        
        Args:
            policy_id: Policy ID
            
        Returns:
            Tuple[int, List[Dict]]: Number of records deleted and errors
        """
        policy = self.session.query(GPSRetentionPolicy).get(policy_id)
        if not policy:
            raise ValueError(f"Policy not found: {policy_id}")
        
        if not policy.is_active:
            raise ValueError(f"Policy is not active: {policy_id}")
        
        # Calculate cutoff date
        cutoff_date = datetime.utcnow() - timedelta(days=policy.retention_days)
        
        # Get records to delete
        records = self.session.query(GPSTracking).filter(
            GPSTracking.timestamp < cutoff_date
        ).all()
        
        # Delete records
        records_deleted = 0
        errors = []
        
        for record in records:
            try:
                self.session.delete(record)
                records_deleted += 1
            except Exception as e:
                errors.append({
                    "record_id": record.id,
                    "error": str(e)
                })
        
        # Create log entry
        log = GPSRetentionLog(
            policy_id=policy_id,
            records_deleted=records_deleted,
            execution_time=datetime.utcnow(),
            status="success" if not errors else "partial",
            error_message=None if not errors else str(errors)
        )
        
        self.session.add(log)
        self.session.commit()
        
        logger.info(
            f"Executed GPS retention policy {policy.name}: "
            f"deleted {records_deleted} records"
        )
        
        return records_deleted, errors
    
    def get_retention_stats(self) -> Dict:
        """Get GPS data retention statistics.
        
        Returns:
            Dict: Retention statistics
        """
        # Get total records
        total_records = self.session.query(func.count(GPSTracking.id)).scalar()
        
        # Get records by age
        now = datetime.utcnow()
        age_ranges = [
            (0, 7),    # 0-7 days
            (8, 30),   # 8-30 days
            (31, 90),  # 31-90 days
            (91, 180), # 91-180 days
            (181, None) # 181+ days
        ]
        
        stats = {
            "total_records": total_records,
            "records_by_age": {},
            "storage_estimate_mb": self._estimate_storage_size()
        }
        
        for start_days, end_days in age_ranges:
            query = self.session.query(func.count(GPSTracking.id))
            
            if start_days is not None:
                start_date = now - timedelta(days=start_days)
                query = query.filter(GPSTracking.timestamp >= start_date)
            
            if end_days is not None:
                end_date = now - timedelta(days=end_days)
                query = query.filter(GPSTracking.timestamp < end_date)
            
            count = query.scalar()
            range_name = f"{start_days}-{end_days if end_days else 'inf'} days"
            stats["records_by_age"][range_name] = count
        
        return stats
    
    def _estimate_storage_size(self) -> float:
        """Estimate storage size of GPS tracking data.
        
        Returns:
            float: Estimated size in megabytes
        """
        # Average record size in bytes
        AVG_RECORD_SIZE = 100
        
        # Get total records
        total_records = self.session.query(func.count(GPSTracking.id)).scalar()
        
        # Calculate size in MB
        size_bytes = total_records * AVG_RECORD_SIZE
        size_mb = size_bytes / (1024 * 1024)
        
        return round(size_mb, 2)
    
    def get_retention_logs(
        self,
        policy_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: Optional[str] = None
    ) -> List[GPSRetentionLog]:
        """Get retention policy execution logs.
        
        Args:
            policy_id: Filter by policy ID
            start_date: Filter by start date
            end_date: Filter by end date
            status: Filter by status
            
        Returns:
            List[GPSRetentionLog]: Retention logs
        """
        query = self.session.query(GPSRetentionLog)
        
        if policy_id:
            query = query.filter(GPSRetentionLog.policy_id == policy_id)
        
        if start_date:
            query = query.filter(GPSRetentionLog.execution_time >= start_date)
        
        if end_date:
            query = query.filter(GPSRetentionLog.execution_time <= end_date)
        
        if status:
            query = query.filter(GPSRetentionLog.status == status)
        
        return query.order_by(GPSRetentionLog.execution_time.desc()).all() 