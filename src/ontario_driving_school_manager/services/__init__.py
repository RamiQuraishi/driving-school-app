"""
Service Framework

This module provides the service framework for the Ontario Driving School Manager.
It includes base services and MTO-compliant implementations.

Author: Rami Drive School
Date: 2024
"""

from typing import Dict, Any, Optional, List, Type, TypeVar, Generic
from abc import ABC, abstractmethod

from .base import BaseService
from .mto_curriculum_service import MTOCurriculumService
from .mto_export_service import MTOExportService
from .offline_sync_service import OfflineSyncService
from .feature_flag_service import FeatureFlagService

__all__ = [
    'BaseService',
    'MTOCurriculumService',
    'MTOExportService',
    'OfflineSyncService',
    'FeatureFlagService'
]