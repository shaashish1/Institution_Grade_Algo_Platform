"""
Base Tester Abstract Class
==========================

Abstract base class for all testing components in the framework.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .models import TestResult, TestConfiguration


class BaseTester(ABC):
    """Abstract base class for all testers"""
    
    def __init__(self, config: TestConfiguration):
        self.config = config
        self.name = self.__class__.__name__
        
    @abstractmethod
    def run_tests(self, target: Any) -> List[TestResult]:
        """
        Run tests on the target
        
        Args:
            target: The object/path/data to test
            
        Returns:
            List of TestResult objects
        """
        pass
    
    @abstractmethod
    def get_test_info(self) -> Dict[str, Any]:
        """
        Get information about this tester
        
        Returns:
            Dictionary with tester information
        """
        pass
    
    def is_enabled(self, test_name: str) -> bool:
        """Check if a specific test is enabled"""
        if not self.config.enabled_tests:
            return True  # If no specific tests configured, run all
        return test_name in self.config.enabled_tests or self.name in self.config.enabled_tests