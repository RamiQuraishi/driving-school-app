"""Lesson cancellation models for managing cancellations."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from .base import BaseModel

class Cancellation(BaseModel):
    """Lesson cancellation model.
    
    This model manages:
    - Cancellation records
    - Cancellation policies
    - Cancellation fees
    """
    
    lesson_id = Column(Integer, ForeignKey("lesson.id"), nullable=False)
    cancelled_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    cancellation_type = Column(String(50), nullable=False)
    reason = Column(Text)
    cancelled_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    lesson = relationship("Lesson")
    cancelled_by = relationship("User")
    fees = relationship("CancellationFee", back_populates="cancellation")
    
    def calculate_fee(self) -> float:
        """Calculate cancellation fee.
        
        Returns:
            float: Cancellation fee
        """
        total_fee = 0.0
        for fee in self.fees:
            if fee.status == "pending":
                total_fee += fee.amount
        return total_fee
    
    def is_fee_paid(self) -> bool:
        """Check if cancellation fee is paid.
        
        Returns:
            bool: True if paid
        """
        return all(fee.status == "paid" for fee in self.fees)

class CancellationPolicy(BaseModel):
    """Cancellation policy model."""
    
    name = Column(String(100), nullable=False)
    description = Column(Text)
    hours_before_lesson = Column(Integer, nullable=False)
    fee_amount = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    fees = relationship("CancellationFee", back_populates="policy")
    
    def applies_to_cancellation(self, cancellation: Cancellation) -> bool:
        """Check if policy applies to cancellation.
        
        Args:
            cancellation: Cancellation record
            
        Returns:
            bool: True if applies
        """
        if not self.is_active:
            return False
        
        hours_before = (cancellation.lesson.start_time - cancellation.cancelled_at).total_seconds() / 3600
        return hours_before <= self.hours_before_lesson

class CancellationFee(BaseModel):
    """Cancellation fee model."""
    
    cancellation_id = Column(Integer, ForeignKey("cancellation.id"), nullable=False)
    policy_id = Column(Integer, ForeignKey("cancellationpolicy.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    paid_at = Column(DateTime)
    
    # Relationships
    cancellation = relationship("Cancellation", back_populates="fees")
    policy = relationship("CancellationPolicy", back_populates="fees")
    
    def mark_as_paid(self) -> None:
        """Mark fee as paid."""
        self.status = "paid"
        self.paid_at = datetime.utcnow() 