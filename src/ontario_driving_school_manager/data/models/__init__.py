"""Models package for the Ontario Driving School Manager.

This package contains SQLAlchemy models for the application, including:
- Base models with version tracking
- MTO compliance models
- Curriculum models
- Feature flags
- Driving zones
- Lesson cancellations
- Insurance and medical information
- Sync conflict tracking
"""

from .base import BaseModel
from .bde_curriculum import BDECurriculum
from .mto_compliance import MTOCompliance
from .mto_export_log import MTOExportLog
from .feature_flags import FeatureFlag
from .driving_zone import DrivingZone, ZoneBoundary, ZonePricing, ZoneAvailability
from .lesson_cancellation import Cancellation, CancellationPolicy, CancellationFee
from .instructor_insurance import InsurancePolicy, VehicleInsurance
from .student_medical_info import MedicalCertificate, MedicalCondition
from .sync_conflict import SyncConflict

__all__ = [
    "BaseModel",
    "BDECurriculum",
    "MTOCompliance",
    "MTOExportLog",
    "FeatureFlag",
    "DrivingZone",
    "ZoneBoundary",
    "ZonePricing",
    "ZoneAvailability",
    "Cancellation",
    "CancellationPolicy",
    "CancellationFee",
    "InsurancePolicy",
    "VehicleInsurance",
    "MedicalCertificate",
    "MedicalCondition",
    "SyncConflict",
] 