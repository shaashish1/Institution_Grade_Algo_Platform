"""
Logging Configuration for Testing Framework
==========================================

Centralized logging setup for the comprehensive system testing framework.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


class TestLogger:
    """Centralized logger for the testing framework"""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        """Setup the logger with appropriate handlers"""
        self._logger = logging.getLogger('comprehensive_system_testing')
        self._logger.setLevel(logging.INFO)
        
        # Create logs directory
        log_dir = Path('comprehensive_system_testing/logs')
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # File handler
        log_file = log_dir / f'test_run_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
    
    def get_logger(self):
        """Get the configured logger"""
        return self._logger
    
    @classmethod
    def info(cls, message: str):
        """Log info message"""
        logger = cls().get_logger()
        logger.info(message)
    
    @classmethod
    def error(cls, message: str):
        """Log error message"""
        logger = cls().get_logger()
        logger.error(message)
    
    @classmethod
    def warning(cls, message: str):
        """Log warning message"""
        logger = cls().get_logger()
        logger.warning(message)
    
    @classmethod
    def debug(cls, message: str):
        """Log debug message"""
        logger = cls().get_logger()
        logger.debug(message)