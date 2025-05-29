#!/usr/bin/env python3
"""
Demo Environment Setup Script

This script sets up a demo environment for the Ontario Driving School Manager application.
It creates test data, configures demo settings, and prepares the system for demonstration.

Author: Rami Drive School
Date: 2024
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DemoEnvironmentSetup:
    """Handles the setup of the demo environment."""

    def __init__(self):
        """Initialize the demo environment setup."""
        self.base_path = Path(__file__).parent.parent
        self.config_path = self.base_path / 'config'
        self.data_path = self.base_path / 'data'
        self.demo_path = self.base_path / 'demo'

    def setup_directories(self) -> None:
        """Create necessary directories for the demo environment."""
        directories = [
            self.demo_path,
            self.demo_path / 'data',
            self.demo_path / 'logs',
            self.demo_path / 'temp'
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")

    def create_demo_config(self) -> None:
        """Create demo configuration files."""
        config = {
            'demo_mode': True,
            'environment': 'demo',
            'database': {
                'host': 'localhost',
                'port': 5432,
                'name': 'demo_db',
                'user': 'demo_user',
                'password': 'demo_password'
            },
            'api': {
                'base_url': 'http://localhost:8000',
                'timeout': 30,
                'retry_attempts': 3
            },
            'logging': {
                'level': 'INFO',
                'file': 'demo.log'
            }
        }

        config_file = self.demo_path / 'config.json'
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        logger.info(f"Created demo configuration: {config_file}")

    def create_test_data(self) -> None:
        """Create test data for the demo environment."""
        test_data = {
            'students': [
                {
                    'id': 1,
                    'name': 'John Doe',
                    'email': 'john.doe@example.com',
                    'phone': '123-456-7890',
                    'status': 'active'
                },
                {
                    'id': 2,
                    'name': 'Jane Smith',
                    'email': 'jane.smith@example.com',
                    'phone': '123-456-7891',
                    'status': 'active'
                }
            ],
            'instructors': [
                {
                    'id': 1,
                    'name': 'Bob Wilson',
                    'email': 'bob.wilson@example.com',
                    'phone': '123-456-7892',
                    'status': 'active'
                }
            ],
            'vehicles': [
                {
                    'id': 1,
                    'make': 'Toyota',
                    'model': 'Corolla',
                    'year': 2020,
                    'status': 'available'
                }
            ]
        }

        data_file = self.demo_path / 'data' / 'test_data.json'
        with open(data_file, 'w') as f:
            json.dump(test_data, f, indent=4)
        logger.info(f"Created test data: {data_file}")

    def setup_logging(self) -> None:
        """Configure logging for the demo environment."""
        log_config = {
            'version': 1,
            'handlers': {
                'file': {
                    'class': 'logging.FileHandler',
                    'filename': str(self.demo_path / 'logs' / 'demo.log'),
                    'formatter': 'standard'
                }
            },
            'formatters': {
                'standard': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                }
            },
            'root': {
                'level': 'INFO',
                'handlers': ['file']
            }
        }

        log_file = self.demo_path / 'logging.json'
        with open(log_file, 'w') as f:
            json.dump(log_config, f, indent=4)
        logger.info(f"Created logging configuration: {log_file}")

    def create_readme(self) -> None:
        """Create a README file for the demo environment."""
        readme_content = """# Demo Environment

This is a demo environment for the Ontario Driving School Manager application.

## Setup
1. Run the setup script: `python scripts/demo_environment_setup.py`
2. Configure the environment variables
3. Start the application

## Test Data
- Students: 2
- Instructors: 1
- Vehicles: 1

## Configuration
- Demo mode enabled
- Local database
- Test API endpoints

## Notes
- This is a demo environment
- Data is reset daily
- No real data is used
- For testing purposes only
"""

        readme_file = self.demo_path / 'README.md'
        with open(readme_file, 'w') as f:
            f.write(readme_content)
        logger.info(f"Created README: {readme_file}")

    def setup_environment(self) -> None:
        """Set up the complete demo environment."""
        try:
            logger.info("Starting demo environment setup...")
            
            self.setup_directories()
            self.create_demo_config()
            self.create_test_data()
            self.setup_logging()
            self.create_readme()
            
            logger.info("Demo environment setup completed successfully")
            
        except Exception as e:
            logger.error(f"Error setting up demo environment: {str(e)}")
            sys.exit(1)

def main():
    """Main entry point for the script."""
    setup = DemoEnvironmentSetup()
    setup.setup_environment()

if __name__ == '__main__':
    main() 