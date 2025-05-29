#!/usr/bin/env python3
"""
Test script for validating MTO compliance requirements.
Tests various aspects of MTO compliance including instructor qualifications,
vehicle requirements, and lesson documentation.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import pytest
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class InstructorQualification(BaseModel):
    """Model for instructor qualifications."""
    id: str
    name: str
    age: int
    license_class: str
    years_experience: int
    certification_number: str
    certification_expiry: datetime
    medical_clearance: bool
    criminal_record_check: bool
    insurance_coverage: bool

class VehicleRequirement(BaseModel):
    """Model for vehicle requirements."""
    id: str
    make: str
    model: str
    year: int
    license_plate: str
    insurance_expiry: datetime
    safety_inspection_date: datetime
    dual_controls: bool
    safety_rating: str
    maintenance_records: List[Dict[str, datetime]]

class LessonDocumentation(BaseModel):
    """Model for lesson documentation."""
    id: str
    student_id: str
    instructor_id: str
    vehicle_id: str
    date: datetime
    duration: int
    type: str
    route: List[Dict[str, float]]
    objectives: List[str]
    progress_notes: str
    student_signature: bool
    instructor_signature: bool

class MTOComplianceTester:
    """Test class for MTO compliance validation."""
    
    def __init__(self):
        self.instructors: List[InstructorQualification] = []
        self.vehicles: List[VehicleRequirement] = []
        self.lessons: List[LessonDocumentation] = []
    
    def generate_test_data(self):
        """Generate test data for compliance validation."""
        # Generate instructor data
        self.instructors = [
            InstructorQualification(
                id="INS001",
                name="John Smith",
                age=35,
                license_class="G",
                years_experience=10,
                certification_number="CERT123456",
                certification_expiry=datetime.now() + timedelta(days=365),
                medical_clearance=True,
                criminal_record_check=True,
                insurance_coverage=True
            ),
            InstructorQualification(
                id="INS002",
                name="Jane Doe",
                age=28,
                license_class="G",
                years_experience=5,
                certification_number="CERT789012",
                certification_expiry=datetime.now() + timedelta(days=180),
                medical_clearance=True,
                criminal_record_check=True,
                insurance_coverage=True
            )
        ]
        
        # Generate vehicle data
        self.vehicles = [
            VehicleRequirement(
                id="VEH001",
                make="Toyota",
                model="Corolla",
                year=2020,
                license_plate="ABC123",
                insurance_expiry=datetime.now() + timedelta(days=180),
                safety_inspection_date=datetime.now() - timedelta(days=30),
                dual_controls=True,
                safety_rating="5-star",
                maintenance_records=[
                    {"type": "oil_change", "date": datetime.now() - timedelta(days=30)},
                    {"type": "brake_check", "date": datetime.now() - timedelta(days=60)}
                ]
            )
        ]
        
        # Generate lesson data
        self.lessons = [
            LessonDocumentation(
                id="LES001",
                student_id="STU001",
                instructor_id="INS001",
                vehicle_id="VEH001",
                date=datetime.now(),
                duration=60,
                type="In-Car",
                route=[
                    {"lat": 43.6532, "lon": -79.3832},
                    {"lat": 43.6519, "lon": -79.3817}
                ],
                objectives=["Parallel parking", "Highway merging"],
                progress_notes="Student showed good progress with parallel parking",
                student_signature=True,
                instructor_signature=True
            )
        ]
    
    def validate_instructor_qualifications(self) -> bool:
        """Validate instructor qualifications against MTO requirements."""
        try:
            for instructor in self.instructors:
                # Check age requirement
                assert instructor.age >= 21, f"Instructor {instructor.id} is too young"
                
                # Check license class
                assert instructor.license_class == "G", f"Instructor {instructor.id} has invalid license class"
                
                # Check experience
                assert instructor.years_experience >= 3, f"Instructor {instructor.id} has insufficient experience"
                
                # Check certification
                assert instructor.certification_expiry > datetime.now(), f"Instructor {instructor.id} certification expired"
                
                # Check required documents
                assert instructor.medical_clearance, f"Instructor {instructor.id} missing medical clearance"
                assert instructor.criminal_record_check, f"Instructor {instructor.id} missing criminal record check"
                assert instructor.insurance_coverage, f"Instructor {instructor.id} missing insurance coverage"
            
            return True
            
        except Exception as e:
            logger.error(f"Instructor validation failed: {str(e)}")
            return False
    
    def validate_vehicle_requirements(self) -> bool:
        """Validate vehicle requirements against MTO standards."""
        try:
            for vehicle in self.vehicles:
                # Check vehicle age
                assert datetime.now().year - vehicle.year <= 10, f"Vehicle {vehicle.id} is too old"
                
                # Check insurance
                assert vehicle.insurance_expiry > datetime.now(), f"Vehicle {vehicle.id} insurance expired"
                
                # Check safety inspection
                assert (datetime.now() - vehicle.safety_inspection_date).days <= 90, f"Vehicle {vehicle.id} needs safety inspection"
                
                # Check dual controls
                assert vehicle.dual_controls, f"Vehicle {vehicle.id} missing dual controls"
                
                # Check safety rating
                assert vehicle.safety_rating in ["4-star", "5-star"], f"Vehicle {vehicle.id} has insufficient safety rating"
                
                # Check maintenance records
                assert len(vehicle.maintenance_records) >= 2, f"Vehicle {vehicle.id} has insufficient maintenance records"
            
            return True
            
        except Exception as e:
            logger.error(f"Vehicle validation failed: {str(e)}")
            return False
    
    def validate_lesson_documentation(self) -> bool:
        """Validate lesson documentation against MTO requirements."""
        try:
            for lesson in self.lessons:
                # Check duration
                assert 30 <= lesson.duration <= 120, f"Lesson {lesson.id} has invalid duration"
                
                # Check route
                assert len(lesson.route) >= 2, f"Lesson {lesson.id} has insufficient route points"
                
                # Check objectives
                assert len(lesson.objectives) >= 1, f"Lesson {lesson.id} has no objectives"
                
                # Check progress notes
                assert len(lesson.progress_notes) >= 10, f"Lesson {lesson.id} has insufficient progress notes"
                
                # Check signatures
                assert lesson.student_signature, f"Lesson {lesson.id} missing student signature"
                assert lesson.instructor_signature, f"Lesson {lesson.id} missing instructor signature"
            
            return True
            
        except Exception as e:
            logger.error(f"Lesson documentation validation failed: {str(e)}")
            return False
    
    async def test_compliance(self):
        """Run the complete compliance test."""
        try:
            # Generate test data
            self.generate_test_data()
            logger.info("Generated test data")
            
            # Validate instructor qualifications
            instructor_valid = self.validate_instructor_qualifications()
            assert instructor_valid, "Instructor qualification validation failed"
            logger.info("Instructor qualification validation passed")
            
            # Validate vehicle requirements
            vehicle_valid = self.validate_vehicle_requirements()
            assert vehicle_valid, "Vehicle requirement validation failed"
            logger.info("Vehicle requirement validation passed")
            
            # Validate lesson documentation
            lesson_valid = self.validate_lesson_documentation()
            assert lesson_valid, "Lesson documentation validation failed"
            logger.info("Lesson documentation validation passed")
            
            logger.info("All compliance tests completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Compliance test failed: {str(e)}")
            return False

@pytest.mark.asyncio
async def test_mto_compliance():
    """Main test function."""
    tester = MTOComplianceTester()
    success = await tester.test_compliance()
    assert success, "MTO compliance test failed"

if __name__ == "__main__":
    asyncio.run(test_mto_compliance()) 