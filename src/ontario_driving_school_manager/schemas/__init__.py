"""
Schema definitions for Ontario Driving School Manager.
These schemas define the data structures used throughout the application.
"""

from .base import BaseSchema
from .bde_curriculum import BDECurriculumSchema
from .mto_export import MTOExportSchema
from .driving_zone import DrivingZoneSchema
from .lesson_cancellation import LessonCancellationSchema
from .sync_conflict import SyncConflictSchema

__all__ = [
    'BaseSchema',
    'BDECurriculumSchema',
    'MTOExportSchema',
    'DrivingZoneSchema',
    'LessonCancellationSchema',
    'SyncConflictSchema'
] 