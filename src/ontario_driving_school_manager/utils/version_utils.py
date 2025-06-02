"""
Version Utilities Module

This module provides version comparison and management functionality.
It includes version parsing, comparison, and validation.

Author: Rami Drive School
Date: 2024
"""

import re
from typing import Dict, Any, Optional, Union, List, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class Version:
    """Version information."""
    major: int
    minor: int
    patch: int
    prerelease: Optional[str] = None
    build: Optional[str] = None
    
    def __str__(self) -> str:
        """Get version string.
        
        Returns:
            Version string
        """
        version = f"{self.major}.{self.minor}.{self.patch}"
        
        if self.prerelease:
            version += f"-{self.prerelease}"
        
        if self.build:
            version += f"+{self.build}"
        
        return version
    
    def __eq__(self, other: "Version") -> bool:
        """Check if versions are equal.
        
        Args:
            other: Other version
            
        Returns:
            True if equal, False otherwise
        """
        if not isinstance(other, Version):
            return False
        
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
            and self.prerelease == other.prerelease
            and self.build == other.build
        )
    
    def __lt__(self, other: "Version") -> bool:
        """Check if version is less than other.
        
        Args:
            other: Other version
            
        Returns:
            True if less than, False otherwise
        """
        if not isinstance(other, Version):
            return False
        
        # Compare major version
        if self.major < other.major:
            return True
        elif self.major > other.major:
            return False
        
        # Compare minor version
        if self.minor < other.minor:
            return True
        elif self.minor > other.minor:
            return False
        
        # Compare patch version
        if self.patch < other.patch:
            return True
        elif self.patch > other.patch:
            return False
        
        # Compare prerelease
        if self.prerelease is None and other.prerelease is not None:
            return False
        elif self.prerelease is not None and other.prerelease is None:
            return True
        elif self.prerelease is not None and other.prerelease is not None:
            return self.prerelease < other.prerelease
        
        return False
    
    def __le__(self, other: "Version") -> bool:
        """Check if version is less than or equal to other.
        
        Args:
            other: Other version
            
        Returns:
            True if less than or equal, False otherwise
        """
        return self < other or self == other
    
    def __gt__(self, other: "Version") -> bool:
        """Check if version is greater than other.
        
        Args:
            other: Other version
            
        Returns:
            True if greater than, False otherwise
        """
        return not (self <= other)
    
    def __ge__(self, other: "Version") -> bool:
        """Check if version is greater than or equal to other.
        
        Args:
            other: Other version
            
        Returns:
            True if greater than or equal, False otherwise
        """
        return not (self < other)

class VersionError(Exception):
    """Version error."""
    pass

class VersionManager:
    """Version manager."""
    
    def __init__(self):
        """Initialize version manager."""
        self.version_pattern = re.compile(
            r"^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.-]+))?(?:\+([a-zA-Z0-9.-]+))?$"
        )
    
    def parse_version(
        self,
        version_str: str
    ) -> Version:
        """Parse version string.
        
        Args:
            version_str: Version string
            
        Returns:
            Version object
        
        Raises:
            VersionError: If version string is invalid
        """
        match = self.version_pattern.match(version_str)
        
        if not match:
            raise VersionError(f"Invalid version string: {version_str}")
        
        major = int(match.group(1))
        minor = int(match.group(2))
        patch = int(match.group(3))
        prerelease = match.group(4)
        build = match.group(5)
        
        return Version(
            major=major,
            minor=minor,
            patch=patch,
            prerelease=prerelease,
            build=build
        )
    
    def validate_version(
        self,
        version_str: str
    ) -> bool:
        """Validate version string.
        
        Args:
            version_str: Version string
            
        Returns:
            True if valid, False otherwise
        """
        try:
            self.parse_version(version_str)
            return True
        except VersionError:
            return False
    
    def compare_versions(
        self,
        version1: str,
        version2: str
    ) -> int:
        """Compare versions.
        
        Args:
            version1: First version string
            version2: Second version string
            
        Returns:
            -1 if version1 < version2,
            0 if version1 == version2,
            1 if version1 > version2
        
        Raises:
            VersionError: If version strings are invalid
        """
        v1 = self.parse_version(version1)
        v2 = self.parse_version(version2)
        
        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1
        else:
            return 0
    
    def is_compatible(
        self,
        version1: str,
        version2: str,
        strict: bool = False
    ) -> bool:
        """Check if versions are compatible.
        
        Args:
            version1: First version string
            version2: Second version string
            strict: Whether to use strict compatibility
            
        Returns:
            True if compatible, False otherwise
        
        Raises:
            VersionError: If version strings are invalid
        """
        v1 = self.parse_version(version1)
        v2 = self.parse_version(version2)
        
        if strict:
            return v1.major == v2.major
        else:
            return (
                v1.major == v2.major
                and v1.minor == v2.minor
            )
    
    def get_latest_version(
        self,
        versions: List[str]
    ) -> str:
        """Get latest version.
        
        Args:
            versions: List of version strings
            
        Returns:
            Latest version string
        
        Raises:
            VersionError: If version strings are invalid
        """
        if not versions:
            raise VersionError("Empty version list")
        
        latest = self.parse_version(versions[0])
        
        for version_str in versions[1:]:
            version = self.parse_version(version_str)
            if version > latest:
                latest = version
        
        return str(latest)
    
    def get_earliest_version(
        self,
        versions: List[str]
    ) -> str:
        """Get earliest version.
        
        Args:
            versions: List of version strings
            
        Returns:
            Earliest version string
        
        Raises:
            VersionError: If version strings are invalid
        """
        if not versions:
            raise VersionError("Empty version list")
        
        earliest = self.parse_version(versions[0])
        
        for version_str in versions[1:]:
            version = self.parse_version(version_str)
            if version < earliest:
                earliest = version
        
        return str(earliest)
    
    def sort_versions(
        self,
        versions: List[str],
        reverse: bool = False
    ) -> List[str]:
        """Sort versions.
        
        Args:
            versions: List of version strings
            reverse: Whether to sort in reverse order
            
        Returns:
            Sorted list of version strings
        
        Raises:
            VersionError: If version strings are invalid
        """
        parsed_versions = [
            self.parse_version(version)
            for version in versions
        ]
        
        sorted_versions = sorted(
            parsed_versions,
            reverse=reverse
        )
        
        return [str(version) for version in sorted_versions]
    
    def get_version_range(
        self,
        min_version: str,
        max_version: str
    ) -> List[str]:
        """Get version range.
        
        Args:
            min_version: Minimum version string
            max_version: Maximum version string
            
        Returns:
            List of version strings in range
        
        Raises:
            VersionError: If version strings are invalid
        """
        min_v = self.parse_version(min_version)
        max_v = self.parse_version(max_version)
        
        if min_v > max_v:
            raise VersionError(
                f"Minimum version {min_version} is greater than "
                f"maximum version {max_version}"
            )
        
        versions = []
        
        for major in range(min_v.major, max_v.major + 1):
            min_minor = min_v.minor if major == min_v.major else 0
            max_minor = max_v.minor if major == max_v.major else 999
            
            for minor in range(min_minor, max_minor + 1):
                min_patch = min_v.patch if (
                    major == min_v.major
                    and minor == min_v.minor
                ) else 0
                max_patch = max_v.patch if (
                    major == max_v.major
                    and minor == max_v.minor
                ) else 999
                
                for patch in range(min_patch, max_patch + 1):
                    version = Version(
                        major=major,
                        minor=minor,
                        patch=patch
                    )
                    versions.append(str(version))
        
        return versions
    
    def get_version_info(
        self,
        version_str: str
    ) -> Dict[str, Any]:
        """Get version information.
        
        Args:
            version_str: Version string
            
        Returns:
            Version information dictionary
        
        Raises:
            VersionError: If version string is invalid
        """
        version = self.parse_version(version_str)
        
        return {
            "version": str(version),
            "major": version.major,
            "minor": version.minor,
            "patch": version.patch,
            "prerelease": version.prerelease,
            "build": version.build,
            "is_prerelease": version.prerelease is not None,
            "is_build": version.build is not None
        }
    
    def get_version_diff(
        self,
        version1: str,
        version2: str
    ) -> Dict[str, Any]:
        """Get version difference.
        
        Args:
            version1: First version string
            version2: Second version string
            
        Returns:
            Version difference dictionary
        
        Raises:
            VersionError: If version strings are invalid
        """
        v1 = self.parse_version(version1)
        v2 = self.parse_version(version2)
        
        return {
            "major_diff": v2.major - v1.major,
            "minor_diff": v2.minor - v1.minor,
            "patch_diff": v2.patch - v1.patch,
            "is_major_update": v2.major > v1.major,
            "is_minor_update": (
                v2.major == v1.major
                and v2.minor > v1.minor
            ),
            "is_patch_update": (
                v2.major == v1.major
                and v2.minor == v1.minor
                and v2.patch > v1.patch
            ),
            "is_prerelease_update": (
                v1.prerelease is not None
                and v2.prerelease is not None
                and v1.prerelease != v2.prerelease
            ),
            "is_build_update": (
                v1.build is not None
                and v2.build is not None
                and v1.build != v2.build
            )
        }
    
    def get_version_summary(
        self,
        versions: List[str]
    ) -> Dict[str, Any]:
        """Get version summary.
        
        Args:
            versions: List of version strings
            
        Returns:
            Version summary dictionary
        
        Raises:
            VersionError: If version strings are invalid
        """
        if not versions:
            raise VersionError("Empty version list")
        
        parsed_versions = [
            self.parse_version(version)
            for version in versions
        ]
        
        return {
            "count": len(versions),
            "latest": str(max(parsed_versions)),
            "earliest": str(min(parsed_versions)),
            "major_versions": len(set(
                version.major
                for version in parsed_versions
            )),
            "minor_versions": len(set(
                (version.major, version.minor)
                for version in parsed_versions
            )),
            "patch_versions": len(set(
                (version.major, version.minor, version.patch)
                for version in parsed_versions
            )),
            "prerelease_versions": len([
                version
                for version in parsed_versions
                if version.prerelease is not None
            ]),
            "build_versions": len([
                version
                for version in parsed_versions
                if version.build is not None
            ])
        } 