"""
School Repository

This module provides the School repository for database operations.

Author: Rami Drive School
Date: 2024
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ...models.school import School

class SchoolRepository:
    """School repository."""
    
    def __init__(self, session: Session):
        """Initialize school repository.
        
        Args:
            session: Database session
        """
        self.session = session
    
    def create(self, school: School) -> School:
        """Create school.
        
        Args:
            school: School to create
            
        Returns:
            Created school
        """
        self.session.add(school)
        self.session.commit()
        self.session.refresh(school)
        return school
    
    def get_by_id(self, school_id: int) -> Optional[School]:
        """Get school by ID.
        
        Args:
            school_id: School ID
            
        Returns:
            School if found, None otherwise
        """
        return self.session.query(School).filter(School.id == school_id).first()
    
    def get_by_license_number(self, license_number: str) -> Optional[School]:
        """Get school by license number.
        
        Args:
            license_number: License number
            
        Returns:
            School if found, None otherwise
        """
        return self.session.query(School).filter(School.license_number == license_number).first()
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[School]:
        """Get all schools.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Filter criteria
            
        Returns:
            List of schools
        """
        query = self.session.query(School)
        
        if filters:
            for key, value in filters.items():
                if hasattr(School, key):
                    query = query.filter(getattr(School, key) == value)
        
        return query.offset(skip).limit(limit).all()
    
    def search(
        self,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[School]:
        """Search schools.
        
        Args:
            query: Search query
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of schools
        """
        return self.session.query(School).filter(
            or_(
                School.name.ilike(f"%{query}%"),
                School.license_number.ilike(f"%{query}%"),
                School.address.ilike(f"%{query}%"),
                School.city.ilike(f"%{query}%"),
                School.province.ilike(f"%{query}%"),
                School.postal_code.ilike(f"%{query}%"),
                School.phone.ilike(f"%{query}%"),
                School.email.ilike(f"%{query}%")
            )
        ).offset(skip).limit(limit).all()
    
    def update(self, school: School) -> School:
        """Update school.
        
        Args:
            school: School to update
            
        Returns:
            Updated school
        """
        self.session.commit()
        self.session.refresh(school)
        return school
    
    def delete(self, school: School) -> None:
        """Delete school.
        
        Args:
            school: School to delete
        """
        self.session.delete(school)
        self.session.commit()
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count schools.
        
        Args:
            filters: Filter criteria
            
        Returns:
            Number of schools
        """
        query = self.session.query(School)
        
        if filters:
            for key, value in filters.items():
                if hasattr(School, key):
                    query = query.filter(getattr(School, key) == value)
        
        return query.count()
    
    def get_by_location(
        self,
        city: str,
        province: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[School]:
        """Get schools by location.
        
        Args:
            city: City
            province: Province
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of schools
        """
        return self.session.query(School).filter(
            School.city == city,
            School.province == province
        ).offset(skip).limit(limit).all()
    
    def get_active_schools(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[School]:
        """Get active schools.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of active schools
        """
        return self.session.query(School).filter(
            School.is_active == True
        ).offset(skip).limit(limit).all() 