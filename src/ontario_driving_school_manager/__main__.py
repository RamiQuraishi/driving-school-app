"""
Main Entry Point

This module serves as the main entry point for the Ontario Driving School Manager.
It initializes the application and starts the FastAPI server.

Author: Rami Drive School
Date: 2024
"""

import sys
import logging
from pathlib import Path

# Add src to Python path
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)

from ontario_driving_school_manager.main import main

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run main function
    main() 