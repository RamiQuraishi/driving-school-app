"""
Docker Test Environment Setup Script

This script sets up a Docker test environment for the application.
It creates and configures necessary containers for testing.

Author: Rami Drive School
Date: 2024
"""

import os
import sys
import time
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add src to Python path
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DockerTestEnv:
    """Docker test environment setup."""
    
    def __init__(self, project_root: str):
        """Initialize Docker test environment.
        
        Args:
            project_root: Path to project root directory
        """
        self.project_root = project_root
        self.containers: Dict[str, str] = {}
        self.network_name = "ontario_driving_school_test"
    
    def create_network(self) -> bool:
        """Create Docker network.
        
        Returns:
            True if network created successfully
        """
        try:
            # Check if network exists
            result = subprocess.run(
                ['docker', 'network', 'ls', '--filter', f'name={self.network_name}'],
                capture_output=True,
                text=True
            )
            
            if self.network_name not in result.stdout:
                # Create network
                subprocess.run(
                    ['docker', 'network', 'create', self.network_name],
                    check=True
                )
                logger.info(f"Created network: {self.network_name}")
            else:
                logger.info(f"Network {self.network_name} already exists")
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create network: {e}")
            return False
    
    def start_redis(self) -> bool:
        """Start Redis container.
        
        Returns:
            True if Redis started successfully
        """
        try:
            # Start Redis container
            subprocess.run([
                'docker', 'run',
                '--name', 'redis_test',
                '--network', self.network_name,
                '-p', '6379:6379',
                '-d',
                'redis:7.0-alpine',
                'redis-server',
                '--appendonly', 'yes',
                '--maxmemory', '512mb',
                '--maxmemory-policy', 'allkeys-lru'
            ], check=True)
            
            self.containers['redis'] = 'redis_test'
            logger.info("Started Redis container")
            
            # Wait for Redis to be ready
            time.sleep(2)
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to start Redis: {e}")
            return False
    
    def start_postgres(self) -> bool:
        """Start PostgreSQL container.
        
        Returns:
            True if PostgreSQL started successfully
        """
        try:
            # Start PostgreSQL container
            subprocess.run([
                'docker', 'run',
                '--name', 'postgres_test',
                '--network', self.network_name,
                '-e', 'POSTGRES_DB=driving_school_test',
                '-e', 'POSTGRES_USER=test_user',
                '-e', 'POSTGRES_PASSWORD=test_password',
                '-p', '5432:5432',
                '-d',
                'postgres:15-alpine'
            ], check=True)
            
            self.containers['postgres'] = 'postgres_test'
            logger.info("Started PostgreSQL container")
            
            # Wait for PostgreSQL to be ready
            time.sleep(5)
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to start PostgreSQL: {e}")
            return False
    
    def start_elasticsearch(self) -> bool:
        """Start Elasticsearch container.
        
        Returns:
            True if Elasticsearch started successfully
        """
        try:
            # Start Elasticsearch container
            subprocess.run([
                'docker', 'run',
                '--name', 'elasticsearch_test',
                '--network', self.network_name,
                '-e', 'discovery.type=single-node',
                '-e', 'xpack.security.enabled=false',
                '-e', 'ES_JAVA_OPTS=-Xms512m -Xmx512m',
                '-p', '9200:9200',
                '-d',
                'elasticsearch:8.11.1'
            ], check=True)
            
            self.containers['elasticsearch'] = 'elasticsearch_test'
            logger.info("Started Elasticsearch container")
            
            # Wait for Elasticsearch to be ready
            time.sleep(10)
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to start Elasticsearch: {e}")
            return False
    
    def verify_containers(self) -> Dict[str, bool]:
        """Verify container status.
        
        Returns:
            Dictionary of container status
        """
        results = {}
        
        for name, container_id in self.containers.items():
            try:
                result = subprocess.run(
                    ['docker', 'ps', '--filter', f'name={container_id}'],
                    capture_output=True,
                    text=True
                )
                results[name] = container_id in result.stdout
            except subprocess.CalledProcessError:
                results[name] = False
        
        return results
    
    def cleanup(self) -> None:
        """Clean up containers and network."""
        try:
            # Stop and remove containers
            for container_id in self.containers.values():
                subprocess.run(['docker', 'stop', container_id], check=True)
                subprocess.run(['docker', 'rm', container_id], check=True)
            
            # Remove network
            subprocess.run(['docker', 'network', 'rm', self.network_name], check=True)
            
            logger.info("Cleanup completed successfully")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Cleanup failed: {e}")

def main():
    """Run Docker test environment setup."""
    # Get project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Initialize and run setup
    env = DockerTestEnv(project_root)
    
    try:
        # Create network
        if not env.create_network():
            sys.exit(1)
        
        # Start containers
        if not env.start_redis():
            sys.exit(1)
        
        if not env.start_postgres():
            sys.exit(1)
        
        if not env.start_elasticsearch():
            sys.exit(1)
        
        # Verify setup
        results = env.verify_containers()
        logger.info("Container status:")
        for name, status in results.items():
            logger.info(f"{name}: {'Running' if status else 'Not running'}")
        
    except KeyboardInterrupt:
        logger.info("Setup interrupted by user")
        env.cleanup()
        sys.exit(1)
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        env.cleanup()
        sys.exit(1)

if __name__ == "__main__":
    main() 