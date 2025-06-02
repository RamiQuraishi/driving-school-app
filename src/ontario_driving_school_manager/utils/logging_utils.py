"""
Logging Utilities Module

This module provides structured logging functionality for the application.
It includes log setup, formatting, and handlers.

Author: Rami Drive School
Date: 2024
"""

import logging
import logging.handlers
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, Union
from pathlib import Path

class StructuredLogFormatter(logging.Formatter):
    """Structured log formatter."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record.
        
        Args:
            record: Log record
            
        Returns:
            Formatted log message
        """
        # Create structured log data
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info)
            }
        
        # Add extra fields if present
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        return json.dumps(log_data)

def setup_logging(
    log_dir: str = "logs",
    log_level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> None:
    """Set up logging.
    
    Args:
        log_dir: Log directory
        log_level: Log level
        max_bytes: Maximum bytes per log file
        backup_count: Number of backup files
    """
    # Create log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # Create formatters
    structured_formatter = StructuredLogFormatter()
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Create handlers
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    
    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, "app.log"),
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setFormatter(structured_formatter)
    
    error_file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, "error.log"),
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    error_file_handler.setFormatter(structured_formatter)
    error_file_handler.setLevel(logging.ERROR)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_file_handler)
    
    # Configure specific loggers
    loggers = {
        "mto": logging.INFO,
        "database": logging.INFO,
        "api": logging.INFO,
        "auth": logging.WARNING
    }
    
    for logger_name, level in loggers.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)

def get_logger(
    name: str,
    extra: Optional[Dict[str, Any]] = None
) -> logging.Logger:
    """Get logger.
    
    Args:
        name: Logger name
        extra: Extra fields to include in logs
        
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    
    if extra:
        logger = logging.LoggerAdapter(logger, extra)
    
    return logger

class LogContext:
    """Log context manager."""
    
    def __init__(
        self,
        logger: logging.Logger,
        extra: Optional[Dict[str, Any]] = None
    ):
        """Initialize log context.
        
        Args:
            logger: Logger instance
            extra: Extra fields to include in logs
        """
        self.logger = logger
        self.extra = extra or {}
    
    def __enter__(self) -> logging.Logger:
        """Enter context.
        
        Returns:
            Logger instance
        """
        return logging.LoggerAdapter(self.logger, self.extra)
    
    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[Exception],
        exc_tb: Optional[Any]
    ) -> None:
        """Exit context."""
        pass

def log_exception(
    logger: logging.Logger,
    exc: Exception,
    extra: Optional[Dict[str, Any]] = None
) -> None:
    """Log exception.
    
    Args:
        logger: Logger instance
        exc: Exception
        extra: Extra fields to include in logs
    """
    logger.error(
        f"Exception: {str(exc)}",
        exc_info=True,
        extra=extra
    )

def log_metric(
    logger: logging.Logger,
    metric_name: str,
    value: Union[int, float],
    tags: Optional[Dict[str, str]] = None
) -> None:
    """Log metric.
    
    Args:
        logger: Logger instance
        metric_name: Metric name
        value: Metric value
        tags: Metric tags
    """
    extra = {
        "metric": {
            "name": metric_name,
            "value": value,
            "tags": tags or {}
        }
    }
    
    logger.info(
        f"Metric: {metric_name}={value}",
        extra=extra
    )

def log_event(
    logger: logging.Logger,
    event_name: str,
    data: Optional[Dict[str, Any]] = None
) -> None:
    """Log event.
    
    Args:
        logger: Logger instance
        event_name: Event name
        data: Event data
    """
    extra = {
        "event": {
            "name": event_name,
            "data": data or {}
        }
    }
    
    logger.info(
        f"Event: {event_name}",
        extra=extra
    ) 