#!/usr/bin/env python3
"""
Environment validation script for Ontario Driving School Manager.
Checks system requirements, dependencies, and configuration.
"""

import os
import sys
import platform
import subprocess
from typing import Dict, List, Tuple
import pkg_resources
import json
from pathlib import Path

class EnvironmentValidator:
    """Validates the development environment."""

    def __init__(self):
        self.requirements = {
            'python': '3.9.0',
            'node': '18.0.0',
            'npm': '8.0.0',
            'git': '2.30.0',
            'docker': '20.10.0'
        }
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def check_system(self) -> bool:
        """Check system requirements."""
        print("Checking system requirements...")
        
        # Check OS
        system = platform.system()
        if system not in ['Darwin', 'Windows', 'Linux']:
            self.errors.append(f"Unsupported operating system: {system}")
            return False

        # Check Python version
        python_version = platform.python_version()
        if not self._version_check(python_version, self.requirements['python']):
            self.errors.append(f"Python version {self.requirements['python']} or higher required")
            return False

        # Check Node.js version
        try:
            node_version = subprocess.check_output(['node', '--version']).decode().strip()
            if not self._version_check(node_version[1:], self.requirements['node']):
                self.errors.append(f"Node.js version {self.requirements['node']} or higher required")
                return False
        except subprocess.CalledProcessError:
            self.errors.append("Node.js not found")
            return False

        # Check npm version
        try:
            npm_version = subprocess.check_output(['npm', '--version']).decode().strip()
            if not self._version_check(npm_version, self.requirements['npm']):
                self.errors.append(f"npm version {self.requirements['npm']} or higher required")
                return False
        except subprocess.CalledProcessError:
            self.errors.append("npm not found")
            return False

        return True

    def check_dependencies(self) -> bool:
        """Check Python and Node.js dependencies."""
        print("Checking dependencies...")
        
        # Check Python dependencies
        try:
            with open('requirements-dev.txt') as f:
                required = pkg_resources.parse_requirements(f)
                installed = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
                for package in required:
                    if package.key not in installed:
                        self.errors.append(f"Missing Python package: {package.key}")
                        return False
        except FileNotFoundError:
            self.errors.append("requirements-dev.txt not found")
            return False

        # Check Node.js dependencies
        try:
            with open('package.json') as f:
                package_data = json.load(f)
                required_deps = {**package_data.get('dependencies', {}), 
                               **package_data.get('devDependencies', {})}
                
                # Check if node_modules exists
                if not Path('node_modules').exists():
                    self.errors.append("node_modules directory not found. Run 'npm install'")
                    return False
        except FileNotFoundError:
            self.errors.append("package.json not found")
            return False

        return True

    def check_configuration(self) -> bool:
        """Check configuration files."""
        print("Checking configuration...")
        
        required_files = [
            '.env.example',
            '.pre-commit-config.yaml',
            '.editorconfig',
            '.prettierrc',
            '.eslintrc.js'
        ]

        for file in required_files:
            if not Path(file).exists():
                self.warnings.append(f"Configuration file not found: {file}")

        return True

    def check_git(self) -> bool:
        """Check Git configuration."""
        print("Checking Git configuration...")
        
        try:
            # Check Git version
            git_version = subprocess.check_output(['git', '--version']).decode().strip()
            version = git_version.split()[2]
            if not self._version_check(version, self.requirements['git']):
                self.errors.append(f"Git version {self.requirements['git']} or higher required")
                return False

            # Check Git hooks
            if not Path('.git/hooks/pre-commit').exists():
                self.warnings.append("Git pre-commit hook not found")
        except subprocess.CalledProcessError:
            self.errors.append("Git not found")
            return False

        return True

    def check_docker(self) -> bool:
        """Check Docker configuration."""
        print("Checking Docker configuration...")
        
        try:
            # Check Docker version
            docker_version = subprocess.check_output(['docker', '--version']).decode().strip()
            version = docker_version.split()[2].rstrip(',')
            if not self._version_check(version, self.requirements['docker']):
                self.errors.append(f"Docker version {self.requirements['docker']} or higher required")
                return False

            # Check Docker Compose
            subprocess.check_output(['docker-compose', '--version'])
        except subprocess.CalledProcessError:
            self.errors.append("Docker or Docker Compose not found")
            return False

        return True

    def _version_check(self, current: str, required: str) -> bool:
        """Compare version strings."""
        current_parts = [int(x) for x in current.split('.')]
        required_parts = [int(x) for x in required.split('.')]
        return current_parts >= required_parts

    def run_all_checks(self) -> bool:
        """Run all environment checks."""
        checks = [
            self.check_system,
            self.check_dependencies,
            self.check_configuration,
            self.check_git,
            self.check_docker
        ]

        success = all(check() for check in checks)

        if self.errors:
            print("\nErrors:")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print("\nWarnings:")
            for warning in self.warnings:
                print(f"  - {warning}")

        return success

def main():
    """Main entry point."""
    validator = EnvironmentValidator()
    success = validator.run_all_checks()
    
    if success:
        print("\nEnvironment validation successful!")
        sys.exit(0)
    else:
        print("\nEnvironment validation failed!")
        sys.exit(1)

if __name__ == '__main__':
    main() 