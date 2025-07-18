"""
Process Utility Functions
========================

Utility functions for process management and subprocess operations.
"""

import subprocess
import sys
import time
from typing import Dict, Any, Optional, Tuple


class ProcessUtils:
    """Utility class for process operations"""
    
    @staticmethod
    def run_command(command: str, timeout: int = 30) -> Dict[str, Any]:
        """Run a command and return result"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'command': command
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'returncode': -1,
                'stdout': '',
                'stderr': f'Command timed out after {timeout} seconds',
                'command': command
            }
        except Exception as e:
            return {
                'success': False,
                'returncode': -1,
                'stdout': '',
                'stderr': str(e),
                'command': command
            }
    
    @staticmethod
    def test_import_isolated(module_name: str) -> Tuple[bool, str]:
        """Test importing a module in isolated subprocess"""
        command = f'{sys.executable} -c "import {module_name}; print(\'SUCCESS\')"'
        result = ProcessUtils.run_command(command, timeout=10)
        
        if result['success'] and 'SUCCESS' in result['stdout']:
            return True, "Import successful"
        else:
            error_msg = result['stderr'] or result['stdout'] or "Unknown import error"
            return False, error_msg
    
    @staticmethod
    def get_python_version() -> str:
        """Get Python version information"""
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    @staticmethod
    def check_package_installed(package_name: str) -> bool:
        """Check if a Python package is installed"""
        try:
            __import__(package_name)
            return True
        except ImportError:
            return False