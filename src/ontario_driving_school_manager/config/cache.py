"""
Cache configuration for Ontario Driving School Manager.
Handles caching settings and strategies.
"""

import logging
from typing import Dict, Any, Optional
from pydantic import BaseSettings, Field
import os

logger = logging.getLogger(__name__)

class CacheConfig(BaseSettings):
    """Cache configuration settings."""
    
    # General settings
    ENABLED: bool = Field(default=True, env="CACHE_ENABLED")
    TYPE: str = Field(default="redis", env="CACHE_TYPE")  # redis, memory, file
    TTL: int = Field(default=3600, env="CACHE_TTL")  # 1 hour in seconds
    
    # Redis settings
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="CACHE_REDIS_URL")
    REDIS_PASSWORD: Optional[str] = Field(None, env="CACHE_REDIS_PASSWORD")
    REDIS_DB: int = Field(default=0, env="CACHE_REDIS_DB")
    REDIS_POOL_SIZE: int = Field(default=10, env="CACHE_REDIS_POOL_SIZE")
    
    # Memory cache settings
    MAX_ITEMS: int = Field(default=1000, env="CACHE_MAX_ITEMS")
    CLEANUP_INTERVAL: int = Field(default=300, env="CACHE_CLEANUP_INTERVAL")  # 5 minutes
    
    # File cache settings
    FILE_PATH: str = Field(default="cache", env="CACHE_FILE_PATH")
    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024, env="CACHE_MAX_FILE_SIZE")  # 10MB
    
    # Strategy settings
    STRATEGY: str = Field(default="lru", env="CACHE_STRATEGY")  # lru, fifo, lfu
    COMPRESSION: bool = Field(default=True, env="CACHE_COMPRESSION")
    COMPRESSION_LEVEL: int = Field(default=6, env="CACHE_COMPRESSION_LEVEL")  # 0-9
    
    # Performance settings
    ENABLE_STATS: bool = Field(default=True, env="CACHE_ENABLE_STATS")
    ENABLE_METRICS: bool = Field(default=True, env="CACHE_ENABLE_METRICS")
    
    # Debug settings
    DEBUG_MODE: bool = Field(default=False, env="CACHE_DEBUG_MODE")
    VERBOSE_LOGGING: bool = Field(default=False, env="CACHE_VERBOSE_LOGGING")
    
    class Config:
        """Pydantic model configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    def get_redis_config(self) -> Dict[str, Any]:
        """Get Redis configuration."""
        return {
            "url": self.REDIS_URL,
            "password": self.REDIS_PASSWORD,
            "db": self.REDIS_DB,
            "pool_size": self.REDIS_POOL_SIZE
        }
    
    def get_memory_config(self) -> Dict[str, Any]:
        """Get memory cache configuration."""
        return {
            "max_items": self.MAX_ITEMS,
            "cleanup_interval": self.CLEANUP_INTERVAL,
            "strategy": self.STRATEGY
        }
    
    def get_file_config(self) -> Dict[str, Any]:
        """Get file cache configuration."""
        return {
            "path": self.FILE_PATH,
            "max_size": self.MAX_FILE_SIZE,
            "compression": self.COMPRESSION,
            "compression_level": self.COMPRESSION_LEVEL
        }
    
    def get_strategy_config(self) -> Dict[str, Any]:
        """Get cache strategy configuration."""
        return {
            "type": self.STRATEGY,
            "ttl": self.TTL,
            "compression": self.COMPRESSION,
            "compression_level": self.COMPRESSION_LEVEL
        }
    
    def validate_config(self) -> bool:
        """Validate cache configuration."""
        try:
            if self.ENABLED:
                if self.TYPE not in ["redis", "memory", "file"]:
                    logger.error("Invalid cache type")
                    return False
                
                if self.TYPE == "redis" and not self.REDIS_URL:
                    logger.error("Redis URL is required for Redis cache")
                    return False
                
                if self.TYPE == "file" and not self.FILE_PATH:
                    logger.error("File path is required for file cache")
                    return False
                
                if self.STRATEGY not in ["lru", "fifo", "lfu"]:
                    logger.error("Invalid cache strategy")
                    return False
                
                if self.COMPRESSION_LEVEL < 0 or self.COMPRESSION_LEVEL > 9:
                    logger.error("Compression level must be between 0 and 9")
                    return False
            
            return True
        
        except Exception as e:
            logger.error(f"Error validating cache configuration: {str(e)}")
            return False 