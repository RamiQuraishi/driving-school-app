"""BDE curriculum models for tracking curriculum requirements and student progress."""

from datetime import datetime
from typing import List, Optional, Dict, Any

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, JSON, Enum
from sqlalchemy.orm import relationship

from .base import BaseModel

class BDECurriculum(BaseModel):
    """BDE curriculum model.
    
    This model manages:
    - Curriculum modules
    - Module requirements
    - Student progress
    - Completion tracking
    """
    
    name = Column(String(100), nullable=False)
    description = Column(Text)
    version = Column(String(20), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    requirements = Column(JSON)  # Module requirements and dependencies
    metadata = Column(JSON)  # Additional curriculum metadata
    
    # Relationships
    modules = relationship("CurriculumModule", back_populates="curriculum")
    student_progress = relationship("StudentProgress", back_populates="curriculum")
    
    def get_module_requirements(self) -> Dict[str, List[str]]:
        """Get module requirements.
        
        Returns:
            Dict[str, List[str]]: Module requirements
        """
        return self.requirements or {}
    
    def is_complete(self, student_id: int) -> bool:
        """Check if curriculum is complete for student.
        
        Args:
            student_id: Student ID
            
        Returns:
            bool: True if complete
        """
        progress = self.get_student_progress(student_id)
        if not progress:
            return False
        
        return all(
            module.is_complete(student_id)
            for module in self.modules
        )
    
    def get_student_progress(self, student_id: int) -> Optional["StudentProgress"]:
        """Get student progress.
        
        Args:
            student_id: Student ID
            
        Returns:
            Optional[StudentProgress]: Student progress if found
        """
        for progress in self.student_progress:
            if progress.student_id == student_id:
                return progress
        return None

class CurriculumModule(BaseModel):
    """Curriculum module model."""
    
    curriculum_id = Column(Integer, ForeignKey("bdecurriculum.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    module_type = Column(String(50), nullable=False)  # classroom, in-car, etc.
    duration_minutes = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)
    is_required = Column(Boolean, nullable=False, default=True)
    prerequisites = Column(JSON)  # List of prerequisite module IDs
    
    # Relationships
    curriculum = relationship("BDECurriculum", back_populates="modules")
    progress = relationship("ModuleProgress", back_populates="module")
    
    def is_complete(self, student_id: int) -> bool:
        """Check if module is complete for student.
        
        Args:
            student_id: Student ID
            
        Returns:
            bool: True if complete
        """
        for p in self.progress:
            if p.student_id == student_id:
                return p.is_complete()
        return False
    
    def get_prerequisites(self) -> List[int]:
        """Get prerequisite module IDs.
        
        Returns:
            List[int]: Prerequisite module IDs
        """
        return self.prerequisites or []

class StudentProgress(BaseModel):
    """Student progress model."""
    
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    curriculum_id = Column(Integer, ForeignKey("bdecurriculum.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    completion_date = Column(DateTime)
    status = Column(String(20), nullable=False, default="in_progress")
    notes = Column(Text)
    
    # Relationships
    student = relationship("Student")
    curriculum = relationship("BDECurriculum", back_populates="student_progress")
    module_progress = relationship("ModuleProgress", back_populates="student_progress")
    
    def is_complete(self) -> bool:
        """Check if curriculum is complete.
        
        Returns:
            bool: True if complete
        """
        return self.status == "completed" and self.completion_date is not None
    
    def get_completion_percentage(self) -> float:
        """Get completion percentage.
        
        Returns:
            float: Completion percentage
        """
        if not self.module_progress:
            return 0.0
        
        completed = sum(1 for p in self.module_progress if p.is_complete())
        total = len(self.module_progress)
        
        return (completed / total) * 100 if total > 0 else 0.0

class ModuleProgress(BaseModel):
    """Module progress model."""
    
    student_progress_id = Column(Integer, ForeignKey("studentprogress.id"), nullable=False)
    module_id = Column(Integer, ForeignKey("curriculummodule.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    completion_date = Column(DateTime)
    status = Column(String(20), nullable=False, default="not_started")
    score = Column(Integer)  # Optional score for assessments
    notes = Column(Text)
    
    # Relationships
    student_progress = relationship("StudentProgress", back_populates="module_progress")
    module = relationship("CurriculumModule", back_populates="progress")
    
    def is_complete(self) -> bool:
        """Check if module is complete.
        
        Returns:
            bool: True if complete
        """
        return self.status == "completed" and self.completion_date is not None
    
    def mark_complete(self, score: Optional[int] = None) -> None:
        """Mark module as complete.
        
        Args:
            score: Optional score for assessment
        """
        self.status = "completed"
        self.completion_date = datetime.utcnow()
        if score is not None:
            self.score = score 