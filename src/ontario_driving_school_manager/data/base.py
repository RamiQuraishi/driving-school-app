"""Base SQLAlchemy configuration and declarative base."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

# Define naming convention for constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Create metadata with naming convention
metadata = MetaData(naming_convention=convention)

# Create declarative base with metadata
Base = declarative_base(metadata=metadata)

# Import all models here to ensure they are registered with the Base
from ..models import *  # noqa 