"""
Base Validator Abstract Class
============================

Abstract base class for all validation components in the testing framework.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .models import TestResult, TestConfiguration


class BaseValidator(ABC):
    """Abstract base class for all validators"""
    
    def __init__(self, config: TestConfiguration):
        self.config = config
        self.name = self.__class__.__name__
        
    @abstractmethod
    def validate(self, target: Any) -> List[TestResult]:
        """
        Perform validation on the target
        
        Args:
            target: The object/path/data to validate
            
        Returns:
            List of TestResult objects
        """
        pass
    
    @abstractmethod
    def can_auto_fix(self, issue: TestResult) -> bool:
        """
        Check if an issue can be automatically fixed
        
        Args:
            issue: TestResult representing the issue
            
        Returns:
            True if the issue can be auto-fixed
        """
        pass
    
    @abstractmethod
    def auto_fix(self, issue: TestResult) -> TestResult:
        """
        Attempt to automatically fix an issue
        
        Args:
            issue: TestResult representing the issue to fix
            
        Returns:
            TestResult with the fix attempt result
        """
        pass
    
    def get_validator_info(self) -> Dict[str, Any]:
        """Get information about this validator"""
        return {
            'name': self.name,
            'description': self.__doc__ or 'No description available',
            'auto_fix_enabled': self.config.auto_fix_enabled
        }