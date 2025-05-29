#!/usr/bin/env python3
"""
Test script for MTO data export functionality.
Tests data export in various formats and validates against MTO requirements.
"""

import asyncio
import csv
import json
import logging
import os
import tempfile
from datetime import datetime
from typing import Dict, List, Optional
from xml.etree import ElementTree

import aiohttp
import pytest
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StudentData(BaseModel):
    """Model for student data export."""
    id: str
    first_name: str
    last_name: str
    date_of_birth: str
    license_number: str
    test_date: str
    result: str
    instructor_id: str
    vehicle_id: str
    lesson_date: str
    duration: int
    type: str
    status: str

class MTOExportTester:
    """Test class for MTO data export validation."""
    
    def __init__(self):
        self.test_data: List[StudentData] = []
        self.export_dir = tempfile.mkdtemp()
    
    def generate_test_data(self, num_records: int) -> List[StudentData]:
        """Generate test data for export."""
        data = []
        for i in range(num_records):
            student = StudentData(
                id=f"STU{i:03d}",
                first_name=f"John{i}",
                last_name=f"Smith{i}",
                date_of_birth="1990-01-01",
                license_number=f"G1234-{i:06d}-12",
                test_date="2024-03-15",
                result="PASS",
                instructor_id=f"INS{i:03d}",
                vehicle_id=f"VEH{i:03d}",
                lesson_date="2024-03-16",
                duration=60,
                type="In-Car",
                status="Completed"
            )
            data.append(student)
        return data
    
    def export_to_csv(self, data: List[StudentData], filename: str) -> str:
        """Export data to CSV format."""
        filepath = os.path.join(self.export_dir, filename)
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=StudentData.__fields__)
            writer.writeheader()
            for record in data:
                writer.writerow(record.dict())
        return filepath
    
    def export_to_xml(self, data: List[StudentData], filename: str) -> str:
        """Export data to XML format."""
        filepath = os.path.join(self.export_dir, filename)
        root = ElementTree.Element("MTOExport")
        
        for record in data:
            student = ElementTree.SubElement(root, "Student")
            for field, value in record.dict().items():
                elem = ElementTree.SubElement(student, field)
                elem.text = str(value)
        
        tree = ElementTree.ElementTree(root)
        tree.write(filepath, encoding='utf-8', xml_declaration=True)
        return filepath
    
    def export_to_json(self, data: List[StudentData], filename: str) -> str:
        """Export data to JSON format."""
        filepath = os.path.join(self.export_dir, filename)
        with open(filepath, 'w') as f:
            json.dump([record.dict() for record in data], f, indent=2)
        return filepath
    
    def validate_csv(self, filepath: str) -> bool:
        """Validate CSV export format."""
        try:
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                
                # Check required fields
                required_fields = StudentData.__fields__.keys()
                assert all(field in headers for field in required_fields), "Missing required fields"
                
                # Validate data
                for row in reader:
                    assert all(row[field] for field in required_fields), "Empty required fields"
                    assert row['duration'].isdigit(), "Invalid duration format"
                    assert row['result'] in ['PASS', 'FAIL'], "Invalid result value"
                
                return True
                
        except Exception as e:
            logger.error(f"CSV validation failed: {str(e)}")
            return False
    
    def validate_xml(self, filepath: str) -> bool:
        """Validate XML export format."""
        try:
            tree = ElementTree.parse(filepath)
            root = tree.getroot()
            
            # Check root element
            assert root.tag == "MTOExport", "Invalid root element"
            
            # Validate student records
            for student in root.findall("Student"):
                required_fields = StudentData.__fields__.keys()
                assert all(student.find(field) is not None for field in required_fields), "Missing required fields"
                
                # Validate field values
                duration = student.find("duration")
                assert duration is not None and duration.text.isdigit(), "Invalid duration format"
                
                result = student.find("result")
                assert result is not None and result.text in ['PASS', 'FAIL'], "Invalid result value"
            
            return True
            
        except Exception as e:
            logger.error(f"XML validation failed: {str(e)}")
            return False
    
    def validate_json(self, filepath: str) -> bool:
        """Validate JSON export format."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
                # Validate data structure
                assert isinstance(data, list), "Invalid JSON structure"
                
                # Validate each record
                for record in data:
                    required_fields = StudentData.__fields__.keys()
                    assert all(field in record for field in required_fields), "Missing required fields"
                    assert all(record[field] for field in required_fields), "Empty required fields"
                    assert str(record['duration']).isdigit(), "Invalid duration format"
                    assert record['result'] in ['PASS', 'FAIL'], "Invalid result value"
                
                return True
                
        except Exception as e:
            logger.error(f"JSON validation failed: {str(e)}")
            return False
    
    async def test_export_formats(self):
        """Test export in all supported formats."""
        try:
            # Generate test data
            self.test_data = self.generate_test_data(5)
            logger.info(f"Generated {len(self.test_data)} test records")
            
            # Test CSV export
            csv_file = self.export_to_csv(self.test_data, "export.csv")
            assert self.validate_csv(csv_file), "CSV export validation failed"
            logger.info("CSV export test passed")
            
            # Test XML export
            xml_file = self.export_to_xml(self.test_data, "export.xml")
            assert self.validate_xml(xml_file), "XML export validation failed"
            logger.info("XML export test passed")
            
            # Test JSON export
            json_file = self.export_to_json(self.test_data, "export.json")
            assert self.validate_json(json_file), "JSON export validation failed"
            logger.info("JSON export test passed")
            
            logger.info("All export format tests completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Export test failed: {str(e)}")
            return False

@pytest.mark.asyncio
async def test_mto_export():
    """Main test function."""
    tester = MTOExportTester()
    success = await tester.test_export_formats()
    assert success, "MTO export test failed"

if __name__ == "__main__":
    asyncio.run(test_mto_export()) 