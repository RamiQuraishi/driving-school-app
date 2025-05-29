"""Base model with version tracking support."""

from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import Column, Integer, DateTime, event
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import Session

Base = declarative_base()

class BaseModel(Base):
    """Base model with version tracking and common fields.
    
    This class provides:
    - Version tracking for sync and conflict resolution
    - Timestamps for auditing
    - Common utility methods
    """
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name from class name."""
        return cls.__name__.lower()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary.
        
        Returns:
            Dict[str, Any]: Model data as dictionary
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseModel":
        """Create model instance from dictionary.
        
        Args:
            data: Model data
            
        Returns:
            BaseModel: Model instance
        """
        return cls(**data)
    
    def update(self, data: Dict[str, Any]) -> None:
        """Update model with new data.
        
        Args:
            data: New data
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.version += 1
        self.updated_at = datetime.utcnow()
    
    @classmethod
    def get_by_id(cls, session: Session, id: int) -> Optional["BaseModel"]:
        """Get model by ID.
        
        Args:
            session: Database session
            id: Model ID
            
        Returns:
            Optional[BaseModel]: Model instance if found
        """
        return session.query(cls).filter(cls.id == id).first()
    
    @classmethod
    def get_all(cls, session: Session) -> list["BaseModel"]:
        """Get all models.
        
        Args:
            session: Database session
            
        Returns:
            list[BaseModel]: List of model instances
        """
        return session.query(cls).all()

@event.listens_for(BaseModel, "before_update")
def increment_version(mapper: Any, connection: Any, target: BaseModel) -> None:
    """Increment version before update.
    
    Args:
        mapper: SQLAlchemy mapper
        connection: Database connection
        target: Model instance
    """
    target.version += 1 