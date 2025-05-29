"""Repository package for data access.

This package provides repository classes for accessing and manipulating data.
Each repository is responsible for a specific domain entity and provides
methods for CRUD operations and domain-specific queries.
"""

from .base import BaseRepository

__all__ = ["BaseRepository"] 