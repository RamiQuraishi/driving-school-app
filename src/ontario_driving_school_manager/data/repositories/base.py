"""Base repository class for data access."""

import logging
from typing import Any, Dict, List, Optional, TypeVar, Generic
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError

from ..offline import OfflineManager

logger = logging.getLogger(__name__)

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """Base repository class providing common CRUD operations.
    
    This class provides a foundation for all repository classes, implementing
    common CRUD operations and offline support.
    """
    
    def __init__(
        self,
        session: Session,
        offline_manager: Optional[OfflineManager] = None
    ):
        """Initialize repository.
        
        Args:
            session: SQLAlchemy session
            offline_manager: Optional offline manager for offline support
        """
        self.session = session
        self.offline_manager = offline_manager
    
    async def create(self, data: Dict[str, Any]) -> T:
        """Create a new record.
        
        Args:
            data: Record data
            
        Returns:
            T: Created record
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            # Add timestamps
            now = datetime.utcnow()
            data["created_at"] = now
            data["updated_at"] = now
            
            # Create record
            record = self._create_record(data)
            self.session.add(record)
            self.session.commit()
            self.session.refresh(record)
            
            # Store offline if manager is available
            if self.offline_manager:
                await self.offline_manager.create_record(
                    self._get_table_name(),
                    self._get_record_id(record),
                    self._to_dict(record)
                )
            
            return record
            
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating record: {e}")
            raise
    
    async def update(self, record_id: int, data: Dict[str, Any]) -> Optional[T]:
        """Update an existing record.
        
        Args:
            record_id: ID of the record to update
            data: Updated data
            
        Returns:
            Optional[T]: Updated record if found
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            # Add timestamp
            data["updated_at"] = datetime.utcnow()
            
            # Update record
            stmt = (
                update(self._get_model())
                .where(self._get_id_column() == record_id)
                .values(**data)
                .execution_options(synchronize_session="fetch")
            )
            result = self.session.execute(stmt)
            
            if result.rowcount == 0:
                return None
            
            self.session.commit()
            
            # Get updated record
            record = self.get(record_id)
            
            # Update offline if manager is available
            if self.offline_manager and record:
                await self.offline_manager.update_record(
                    self._get_table_name(),
                    record_id,
                    self._to_dict(record)
                )
            
            return record
            
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating record: {e}")
            raise
    
    async def delete(self, record_id: int) -> bool:
        """Delete a record.
        
        Args:
            record_id: ID of the record to delete
            
        Returns:
            bool: True if record was deleted
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            # Delete record
            stmt = (
                delete(self._get_model())
                .where(self._get_id_column() == record_id)
            )
            result = self.session.execute(stmt)
            
            if result.rowcount == 0:
                return False
            
            self.session.commit()
            
            # Delete offline if manager is available
            if self.offline_manager:
                await self.offline_manager.delete_record(
                    self._get_table_name(),
                    record_id
                )
            
            return True
            
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting record: {e}")
            raise
    
    def get(self, record_id: int) -> Optional[T]:
        """Get a record by ID.
        
        Args:
            record_id: ID of the record
            
        Returns:
            Optional[T]: Record if found
        """
        try:
            stmt = select(self._get_model()).where(
                self._get_id_column() == record_id
            )
            return self.session.execute(stmt).scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Error getting record: {e}")
            return None
    
    def get_many(
        self,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[T]:
        """Get multiple records.
        
        Args:
            filters: Filter conditions
            order_by: Order by clause
            limit: Maximum number of records
            offset: Offset for pagination
            
        Returns:
            List[T]: List of records
        """
        try:
            stmt = select(self._get_model())
            
            # Apply filters
            if filters:
                for key, value in filters.items():
                    stmt = stmt.where(getattr(self._get_model(), key) == value)
            
            # Apply ordering
            if order_by:
                stmt = stmt.order_by(order_by)
            
            # Apply pagination
            if limit is not None:
                stmt = stmt.limit(limit)
            if offset is not None:
                stmt = stmt.offset(offset)
            
            return list(self.session.execute(stmt).scalars().all())
            
        except SQLAlchemyError as e:
            logger.error(f"Error getting records: {e}")
            return []
    
    def _get_model(self) -> type:
        """Get the SQLAlchemy model class.
        
        Returns:
            type: Model class
        """
        raise NotImplementedError
    
    def _get_table_name(self) -> str:
        """Get the table name.
        
        Returns:
            str: Table name
        """
        return self._get_model().__tablename__
    
    def _get_id_column(self) -> Any:
        """Get the ID column.
        
        Returns:
            Any: ID column
        """
        return self._get_model().id
    
    def _get_record_id(self, record: T) -> int:
        """Get the ID of a record.
        
        Args:
            record: Record instance
            
        Returns:
            int: Record ID
        """
        return record.id
    
    def _create_record(self, data: Dict[str, Any]) -> T:
        """Create a record instance.
        
        Args:
            data: Record data
            
        Returns:
            T: Record instance
        """
        return self._get_model()(**data)
    
    def _to_dict(self, record: T) -> Dict[str, Any]:
        """Convert a record to a dictionary.
        
        Args:
            record: Record instance
            
        Returns:
            Dict[str, Any]: Record data
        """
        return {
            column.name: getattr(record, column.name)
            for column in record.__table__.columns
        } 