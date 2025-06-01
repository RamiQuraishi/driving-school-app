"""
Scheduling Conflict Test Script

This script tests various scheduling conflict scenarios and resolution strategies.

Author: Rami Drive School
Date: 2024
"""

import pytest
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

class TimeSlot:
    """Represents a time slot for scheduling."""
    
    def __init__(self, start: datetime, end: datetime):
        """Initialize time slot.
        
        Args:
            start: Start time
            end: End time
        """
        self.start = start
        self.end = end
    
    def overlaps(self, other: 'TimeSlot') -> bool:
        """Check if time slot overlaps with another.
        
        Args:
            other: Other time slot to check
            
        Returns:
            True if slots overlap
        """
        return (self.start < other.end and self.end > other.start)
    
    def duration(self) -> timedelta:
        """Get duration of time slot.
        
        Returns:
            Duration as timedelta
        """
        return self.end - self.start

class Lesson:
    """Represents a driving lesson."""
    
    def __init__(
        self,
        id: str,
        student_id: str,
        instructor_id: str,
        time_slot: TimeSlot,
        location: str
    ):
        """Initialize lesson.
        
        Args:
            id: Lesson ID
            student_id: Student ID
            instructor_id: Instructor ID
            time_slot: Time slot
            location: Lesson location
        """
        self.id = id
        self.student_id = student_id
        self.instructor_id = instructor_id
        self.time_slot = time_slot
        self.location = location

class Schedule:
    """Manages lesson scheduling."""
    
    def __init__(self):
        """Initialize schedule."""
        self.lessons: List[Lesson] = []
    
    def add_lesson(self, lesson: Lesson) -> bool:
        """Add lesson to schedule.
        
        Args:
            lesson: Lesson to add
            
        Returns:
            True if lesson was added successfully
        """
        if self._check_conflicts(lesson):
            return False
        
        self.lessons.append(lesson)
        return True
    
    def _check_conflicts(self, lesson: Lesson) -> bool:
        """Check for scheduling conflicts.
        
        Args:
            lesson: Lesson to check
            
        Returns:
            True if conflicts exist
        """
        for existing_lesson in self.lessons:
            if (existing_lesson.student_id == lesson.student_id or
                existing_lesson.instructor_id == lesson.instructor_id):
                if existing_lesson.time_slot.overlaps(lesson.time_slot):
                    return True
        return False
    
    def get_conflicts(self, lesson: Lesson) -> List[Lesson]:
        """Get conflicting lessons.
        
        Args:
            lesson: Lesson to check
            
        Returns:
            List of conflicting lessons
        """
        conflicts = []
        for existing_lesson in self.lessons:
            if (existing_lesson.student_id == lesson.student_id or
                existing_lesson.instructor_id == lesson.instructor_id):
                if existing_lesson.time_slot.overlaps(lesson.time_slot):
                    conflicts.append(existing_lesson)
        return conflicts
    
    def find_available_slots(
        self,
        student_id: str,
        instructor_id: str,
        duration: timedelta,
        start_time: datetime,
        end_time: datetime
    ) -> List[TimeSlot]:
        """Find available time slots.
        
        Args:
            student_id: Student ID
            instructor_id: Instructor ID
            duration: Required duration
            start_time: Start of search window
            end_time: End of search window
            
        Returns:
            List of available time slots
        """
        available_slots = []
        current_time = start_time
        
        while current_time + duration <= end_time:
            slot = TimeSlot(current_time, current_time + duration)
            test_lesson = Lesson("test", student_id, instructor_id, slot, "test")
            
            if not self._check_conflicts(test_lesson):
                available_slots.append(slot)
            
            current_time += timedelta(minutes=30)
        
        return available_slots

def test_basic_scheduling():
    """Test basic scheduling functionality."""
    schedule = Schedule()
    base_time = datetime.now()
    
    # Create test lessons
    lesson1 = Lesson(
        "1",
        "student1",
        "instructor1",
        TimeSlot(base_time, base_time + timedelta(hours=1)),
        "Location 1"
    )
    
    lesson2 = Lesson(
        "2",
        "student2",
        "instructor1",
        TimeSlot(base_time + timedelta(hours=2), base_time + timedelta(hours=3)),
        "Location 2"
    )
    
    # Test adding non-conflicting lessons
    assert schedule.add_lesson(lesson1)
    assert schedule.add_lesson(lesson2)
    assert len(schedule.lessons) == 2

def test_student_conflict():
    """Test student scheduling conflict."""
    schedule = Schedule()
    base_time = datetime.now()
    
    # Create conflicting lessons for same student
    lesson1 = Lesson(
        "1",
        "student1",
        "instructor1",
        TimeSlot(base_time, base_time + timedelta(hours=1)),
        "Location 1"
    )
    
    lesson2 = Lesson(
        "2",
        "student1",
        "instructor2",
        TimeSlot(base_time + timedelta(minutes=30), base_time + timedelta(hours=1, minutes=30)),
        "Location 2"
    )
    
    # Test conflict detection
    assert schedule.add_lesson(lesson1)
    assert not schedule.add_lesson(lesson2)
    assert len(schedule.lessons) == 1

def test_instructor_conflict():
    """Test instructor scheduling conflict."""
    schedule = Schedule()
    base_time = datetime.now()
    
    # Create conflicting lessons for same instructor
    lesson1 = Lesson(
        "1",
        "student1",
        "instructor1",
        TimeSlot(base_time, base_time + timedelta(hours=1)),
        "Location 1"
    )
    
    lesson2 = Lesson(
        "2",
        "student2",
        "instructor1",
        TimeSlot(base_time + timedelta(minutes=30), base_time + timedelta(hours=1, minutes=30)),
        "Location 2"
    )
    
    # Test conflict detection
    assert schedule.add_lesson(lesson1)
    assert not schedule.add_lesson(lesson2)
    assert len(schedule.lessons) == 1

def test_available_slots():
    """Test finding available time slots."""
    schedule = Schedule()
    base_time = datetime.now()
    
    # Add some lessons
    lesson1 = Lesson(
        "1",
        "student1",
        "instructor1",
        TimeSlot(base_time, base_time + timedelta(hours=1)),
        "Location 1"
    )
    
    lesson2 = Lesson(
        "2",
        "student2",
        "instructor1",
        TimeSlot(base_time + timedelta(hours=2), base_time + timedelta(hours=3)),
        "Location 2"
    )
    
    schedule.add_lesson(lesson1)
    schedule.add_lesson(lesson2)
    
    # Find available slots
    available_slots = schedule.find_available_slots(
        "student3",
        "instructor1",
        timedelta(hours=1),
        base_time,
        base_time + timedelta(hours=4)
    )
    
    # Verify available slots
    assert len(available_slots) > 0
    for slot in available_slots:
        assert not any(
            existing_lesson.time_slot.overlaps(slot)
            for existing_lesson in schedule.lessons
        )

if __name__ == "__main__":
    pytest.main([__file__]) 