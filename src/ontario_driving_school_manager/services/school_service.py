"""
School service module handling school-related operations.
This module manages school creation, retrieval, and updates.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models.school import School

class SchoolService:
    """Service for managing driving schools."""
    
    def __init__(self, db: Session):
        """
        Initialize the SchoolService.
        
        Args:
            db: Database session
        """
        self.db = db

    def get_school_by_id(self, school_id: int) -> Optional[School]:
        """
        Retrieve a school by its ID.
        
        Args:
            school_id: The ID of the school to retrieve
            
        Returns:
            Optional[School]: The school if found, None otherwise
        """
        return self.db.query(School).filter(School.id == school_id).first()

    def get_school_by_name(self, name: str) -> Optional[School]:
        """
        Retrieve a school by its name.
        
        Args:
            name: The name of the school to retrieve
            
        Returns:
            Optional[School]: The school if found, None otherwise
        """
        return self.db.query(School).filter(School.name == name).first()

    def create_school(self, name: str, **kwargs) -> School:
        """
        Create a new school.
        
        Args:
            name: School's name
            **kwargs: Additional school attributes
            
        Returns:
            School: The created school
            
        Raises:
            HTTPException: If school with name already exists
        """
        if self.get_school_by_name(name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="School with this name already exists"
            )
            
        school = School(name=name, **kwargs)
        
        self.db.add(school)
        self.db.commit()
        self.db.refresh(school)
        return school

    def update_school(self, school_id: int, **kwargs) -> Optional[School]:
        """
        Update a school's information.
        
        Args:
            school_id: The ID of the school to update
            **kwargs: The attributes to update
            
        Returns:
            Optional[School]: The updated school if found, None otherwise
        """
        school = self.get_school_by_id(school_id)
        if not school:
            return None
            
        for key, value in kwargs.items():
            if hasattr(school, key):
                setattr(school, key, value)
                
        self.db.commit()
        self.db.refresh(school)
        return school

    def delete_school(self, school_id: int) -> bool:
        """
        Delete a school.
        
        Args:
            school_id: The ID of the school to delete
            
        Returns:
            bool: True if school was deleted, False if not found
        """
        school = self.get_school_by_id(school_id)
        if not school:
            return False
            
        self.db.delete(school)
        self.db.commit()
        return True

    def list_schools(self, skip: int = 0, limit: int = 100) -> List[School]:
        """
        List all schools with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[School]: List of schools
        """
        return self.db.query(School).offset(skip).limit(limit).all() 