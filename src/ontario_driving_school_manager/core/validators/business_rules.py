"""
Business Rules Validator

This module provides validation for business rules in the Ontario Driving School Manager.
It implements validation for scheduling, payments, and other business requirements.

Author: Rami Drive School
Date: 2024
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from . import Validator, ValidationError

class BusinessRules(Validator[Dict[str, Any]]):
    """Business rules validator."""
    
    def __init__(self):
        """Initialize business rules validator."""
        # Scheduling rules
        self.min_lesson_duration = timedelta(minutes=30)
        self.max_lesson_duration = timedelta(hours=2)
        self.min_booking_notice = timedelta(hours=24)
        self.max_booking_advance = timedelta(days=30)
        
        # Payment rules
        self.min_payment_amount = 50.0
        self.max_payment_amount = 1000.0
        self.payment_methods = ['credit_card', 'debit_card', 'cash', 'e_transfer']
        
        # Instructor rules
        self.max_students_per_instructor = 5
        self.max_hours_per_day = 8
        self.required_break_duration = timedelta(minutes=30)
    
    def validate(self, data: Dict[str, Any]) -> List[str]:
        """Validate business rules.
        
        Args:
            data: Data to validate
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Validate scheduling
        if 'schedule' in data:
            errors.extend(self._validate_schedule(data['schedule']))
        
        # Validate payment
        if 'payment' in data:
            errors.extend(self._validate_payment(data['payment']))
        
        # Validate instructor
        if 'instructor' in data:
            errors.extend(self._validate_instructor(data['instructor']))
        
        return errors
    
    def _validate_schedule(self, schedule_data: Dict[str, Any]) -> List[str]:
        """Validate scheduling rules.
        
        Args:
            schedule_data: Schedule data to validate
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Validate lesson duration
        if 'duration' in schedule_data:
            try:
                duration = timedelta(minutes=schedule_data['duration'])
                if duration < self.min_lesson_duration:
                    errors.append(f"Lesson duration must be at least {self.min_lesson_duration}")
                elif duration > self.max_lesson_duration:
                    errors.append(f"Lesson duration cannot exceed {self.max_lesson_duration}")
            except (ValueError, TypeError):
                errors.append("Invalid lesson duration")
        
        # Validate booking time
        if 'booking_time' in schedule_data:
            try:
                booking_time = datetime.fromisoformat(schedule_data['booking_time'])
                now = datetime.now()
                
                if booking_time < now + self.min_booking_notice:
                    errors.append(f"Booking must be at least {self.min_booking_notice} in advance")
                elif booking_time > now + self.max_booking_advance:
                    errors.append(f"Booking cannot be more than {self.max_booking_advance} in advance")
            except ValueError:
                errors.append("Invalid booking time format")
        
        return errors
    
    def _validate_payment(self, payment_data: Dict[str, Any]) -> List[str]:
        """Validate payment rules.
        
        Args:
            payment_data: Payment data to validate
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Validate amount
        if 'amount' not in payment_data:
            errors.append("Payment amount is required")
        else:
            try:
                amount = float(payment_data['amount'])
                if amount < self.min_payment_amount:
                    errors.append(f"Payment amount must be at least ${self.min_payment_amount}")
                elif amount > self.max_payment_amount:
                    errors.append(f"Payment amount cannot exceed ${self.max_payment_amount}")
            except (ValueError, TypeError):
                errors.append("Invalid payment amount")
        
        # Validate payment method
        if 'method' not in payment_data:
            errors.append("Payment method is required")
        elif payment_data['method'] not in self.payment_methods:
            errors.append(f"Invalid payment method. Must be one of: {', '.join(self.payment_methods)}")
        
        return errors
    
    def _validate_instructor(self, instructor_data: Dict[str, Any]) -> List[str]:
        """Validate instructor rules.
        
        Args:
            instructor_data: Instructor data to validate
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Validate student count
        if 'student_count' in instructor_data:
            try:
                count = int(instructor_data['student_count'])
                if count > self.max_students_per_instructor:
                    errors.append(f"Instructor cannot have more than {self.max_students_per_instructor} students")
            except (ValueError, TypeError):
                errors.append("Invalid student count")
        
        # Validate hours
        if 'hours_today' in instructor_data:
            try:
                hours = float(instructor_data['hours_today'])
                if hours > self.max_hours_per_day:
                    errors.append(f"Instructor cannot work more than {self.max_hours_per_day} hours per day")
            except (ValueError, TypeError):
                errors.append("Invalid hours")
        
        # Validate breaks
        if 'last_break' in instructor_data:
            try:
                last_break = datetime.fromisoformat(instructor_data['last_break'])
                time_since_break = datetime.now() - last_break
                if time_since_break > self.max_hours_per_day:
                    errors.append(f"Instructor must take a {self.required_break_duration} break after {self.max_hours_per_day} hours")
            except ValueError:
                errors.append("Invalid break time format")
        
        return errors