"""Offline data management package.

This package provides functionality for managing data when the application
is offline or in a disconnected state. It includes:
- Local data storage
- Data synchronization
- Conflict resolution
- Offline-first data access
"""

from .storage import LocalStorage
from .sync import DataSynchronizer
from .conflict import ConflictResolver

__all__ = [
    'LocalStorage',
    'DataSynchronizer',
    'ConflictResolver',
] 