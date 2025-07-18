"""
Integration Hooks Manager
=========================

Manages integration with existing AlgoProject system verification tools.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime

from ..core.test_orchestrator import TestOrchestrator
from ..core.models import TestConfiguration
from ..utils.logger import TestLogger


class HooksManager:
    """Manages integration hooks with existing system tools"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.logger = TestLogger()
        self.hooks = {}
        self.orchestrator = None
        
        # Initialize orchestrator
        self._initialize_orchestrator()
        
        # Register default hooks
        self._register_default_hooks()
    
    def _initialize_orchestrator(self):
        """Initialize test orchestrator"""
        try:
            config = TestConfiguration()
            self.orchestrator = TestOrchestrator(config)
        except Exception as e:
            self.logger.error(f"Failed to initialize orchestrator: {e}")
    
    def _register_default_hooks(self):
        """Register default integration hooks"""
        # Hook into existing system validation scripts
        self.register_hook(
            "system_validation",
            self._hook_system_validation,
            "Integration with helper_scripts/system_validation.py"
        )
        
        self.register_hook(
            "quick_status",
            self._hook_quick_status,
            "Integration with helper_scripts/quick_status.py"
        )
        
        self.register_hook(
            "tools_verification",
            self._hook_tools_verification,
            "Integration with tools/system_verification.py"
        )
        
        # Hook for main launchers
        self.register_hook(
            "main_launcher",
            self._hook_main_launcher,
            "Integration with main.py launcher"
        )
        
        self.register_hook(
            "crypto_launcher",
            self._hook_crypto_launcher,
            "Integration with crypto_launcher.py"
        )
    
    def register_hook(self, name: str, callback: Callable, description: str = ""):
        """
        Register an integration hook
        
        Args:
            name: Hook name
            callback: Function to call when hook is triggered
            description: Hook description
        """
        self.hooks[name] = {
            "callback": callback,
            "description": description,
            "registered_at": datetime.now(),
            "call_count": 0,
            "last_called": None
        }
        
        self.logger.info(f"Registered hook: {name}")
    
    def trigger_hook(self, name: str, *args, **kwargs) -> Any:
        """
        Trigger a registered hook
        
        Args:
            name: Hook name
            *args: Positional arguments for hook
            **kwargs: Keyword arguments for hook
            
        Returns:
            Hook callback result
        """
        if name not in self.hooks:
            self.logger.warning(f"Hook not found: {name}")
            return None
        
        hook = self.hooks[name]
        
        try:
            # Update hook statistics
            hook["call_count"] += 1
            hook["last_called"] = datetime.now()
            
            # Call the hook
            result = hook["callback"](*args, **kwargs)
            
            self.logger.info(f"Hook triggered successfully: {name}")
            return result
            
        except Exception as e:
            self.logger.error(f"Hook failed: {name} - {e}")
            return None
    
    def _hook_system_validation(self, target: Optional[str] = None) -> Dict[str, Any]:
        """Hook for system validation integration"""
        target = target or str(self.project_root)
        
        self.logger.info("Running comprehensive test via system validation hook")
        
        # Run our comprehensive test
        if self.orchestrator:
            result = self.orchestrator.run_comprehensive_test(target)
            
            # Also try to run the original system validation if it exists
            original_script = self.project_root / "helper_scripts" / "system_validation.py"
            if original_script.exists():
                try:
                    subprocess.run([sys.executable, str(original_script)], 
                                 capture_output=True, text=True, timeout=60)
                    self.logger.info("Original system validation also executed")
                except Exception as e:
                    self.logger.warning(f"Could not run original system validation: {e}")
            
            return result
        
        return {"error": "Orchestrator not available"}
    
    def _hook_quick_status(self, target: Optional[str] = None) -> Dict[str, Any]:
        """Hook for quick status integration"""
        target = target or str(self.project_root)
        
        self.logger.info("Running quick test via quick status hook")
        
        if self.orchestrator:
            result = self.orchestrator.run_quick_test(target)
            
            # Also try to run the original quick status if it exists
            original_script = self.project_root / "helper_scripts" / "quick_status.py"
            if original_script.exists():
                try:
                    subprocess.run([sys.executable, str(original_script)], 
                                 capture_output=True, text=True, timeout=30)
                    self.logger.info("Original quick status also executed")
                except Exception as e:
                    self.logger.warning(f"Could not run original quick status: {e}")
            
            return result
        
        return {"error": "Orchestrator not available"}
    
    def _hook_tools_verification(self, target: Optional[str] = None) -> Dict[str, Any]:
        """Hook for tools verification integration"""
        target = target or str(self.project_root)
        
        self.logger.info("Running targeted test via tools verification hook")
        
        if self.orchestrator:
            # Run targeted test focusing on tools and integration
            components = ["integration", "dependencies"]
            result = self.orchestrator.run_targeted_test(target, components)
            
            # Also try to run the original tools verification if it exists
            original_script = self.project_root / "tools" / "system_verification.py"
            if original_script.exists():
                try:
                    subprocess.run([sys.executable, str(original_script)], 
                                 capture_output=True, text=True, timeout=90)
                    self.logger.info("Original tools verification also executed")
                except Exception as e:
                    self.logger.warning(f"Could not run original tools verification: {e}")
            
            return result
        
        return {"error": "Orchestrator not available"}
    
    def _hook_main_launcher(self, action: str = "health_check") -> Dict[str, Any]:
        """Hook for main launcher integration"""
        self.logger.info(f"Main launcher hook triggered: {action}")
        
        if action == "health_check" and self.orchestrator:
            # Run quick health check
            result = self.orchestrator.run_quick_test(str(self.project_root))
            
            # Extract health summary
            results = result.get("results", [])
            passed = len([r for r in results if r.status.value == "PASS"])
            total = len(results)
            
            return {
                "status": "healthy" if passed / total > 0.8 else "warning" if passed / total > 0.6 else "critical",
                "score": (passed / total * 100) if total > 0 else 0,
                "tests_run": total,
                "tests_passed": passed
            }
        
        return {"status": "unknown", "message": f"Action {action} not implemented"}
    
    def _hook_crypto_launcher(self, action: str = "crypto_health_check") -> Dict[str, Any]:
        """Hook for crypto launcher integration"""
        self.logger.info(f"Crypto launcher hook triggered: {action}")
        
        if action == "crypto_health_check" and self.orchestrator:
            # Run targeted test on crypto components
            crypto_components = ["integration", "config"]
            result = self.orchestrator.run_targeted_test(str(self.project_root), crypto_components)
            
            # Filter results for crypto-related tests
            results = result.get("results", [])
            crypto_results = [r for r in results if "crypto" in r.component.lower() or "ccxt" in r.message.lower()]
            
            if crypto_results:
                passed = len([r for r in crypto_results if r.status.value == "PASS"])
                total = len(crypto_results)
                
                return {
                    "crypto_status": "healthy" if passed / total > 0.8 else "warning",
                    "crypto_score": (passed / total * 100) if total > 0 else 0,
                    "crypto_tests": total,
                    "ccxt_available": any("ccxt" in r.message.lower() and r.status.value == "PASS" for r in crypto_results)
                }
        
        return {"crypto_status": "unknown", "message": f"Action {action} not implemented"}
    
    def create_wrapper_script(self, original_script: str, hook_name: str) -> bool:
        """
        Create a wrapper script that calls both original and our hook
        
        Args:
            original_script: Path to original script
            hook_name: Name of hook to trigger
            
        Returns:
            True if wrapper created successfully
        """
        try:
            original_path = Path(original_script)
            if not original_path.exists():
                self.logger.error(f"Original script not found: {original_script}")
                return False
            
            # Create backup of original
            backup_path = original_path.with_suffix(original_path.suffix + ".original")
            if not backup_path.exists():
                import shutil
                shutil.copy2(original_path, backup_path)
            
            # Create wrapper script
            wrapper_content = f'''#!/usr/bin/env python3
"""
Wrapper script for {original_path.name}
Integrates with Comprehensive System Testing Framework
"""

import sys
import os
from pathlib import Path

# Add comprehensive testing to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from comprehensive_system_testing.integration.hooks_manager import HooksManager
    
    # Initialize hooks manager
    hooks_manager = HooksManager()
    
    # Trigger our hook
    result = hooks_manager.trigger_hook("{hook_name}")
    
    if result and "error" not in result:
        print("✅ Comprehensive system test completed")
        if "score" in result:
            print(f"🏥 System health: {{result['score']:.1f}}/100")
    else:
        print("⚠️  Comprehensive test had issues")
    
except Exception as e:
    print(f"⚠️  Could not run comprehensive test: {{e}}")

# Also run original script
try:
    exec(open("{backup_path}").read())
except Exception as e:
    print(f"⚠️  Original script failed: {{e}}")
'''
            
            # Write wrapper
            with open(original_path, 'w') as f:
                f.write(wrapper_content)
            
            self.logger.info(f"Created wrapper script for: {original_script}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create wrapper script: {e}")
            return False
    
    def install_hooks(self) -> Dict[str, bool]:
        """Install hooks by creating wrapper scripts"""
        results = {}
        
        # Scripts to wrap
        scripts_to_wrap = [
            ("helper_scripts/system_validation.py", "system_validation"),
            ("helper_scripts/quick_status.py", "quick_status"),
            ("tools/system_verification.py", "tools_verification")
        ]
        
        for script_path, hook_name in scripts_to_wrap:
            full_path = self.project_root / script_path
            if full_path.exists():
                success = self.create_wrapper_script(str(full_path), hook_name)
                results[script_path] = success
            else:
                self.logger.warning(f"Script not found for wrapping: {script_path}")
                results[script_path] = False
        
        return results
    
    def uninstall_hooks(self) -> Dict[str, bool]:
        """Uninstall hooks by restoring original scripts"""
        results = {}
        
        scripts_to_restore = [
            "helper_scripts/system_validation.py",
            "helper_scripts/quick_status.py", 
            "tools/system_verification.py"
        ]
        
        for script_path in scripts_to_restore:
            try:
                original_path = self.project_root / script_path
                backup_path = original_path.with_suffix(original_path.suffix + ".original")
                
                if backup_path.exists():
                    import shutil
                    shutil.copy2(backup_path, original_path)
                    backup_path.unlink()  # Remove backup
                    results[script_path] = True
                    self.logger.info(f"Restored original script: {script_path}")
                else:
                    results[script_path] = False
                    self.logger.warning(f"No backup found for: {script_path}")
                    
            except Exception as e:
                self.logger.error(f"Failed to restore {script_path}: {e}")
                results[script_path] = False
        
        return results
    
    def get_hook_statistics(self) -> Dict[str, Any]:
        """Get statistics about registered hooks"""
        stats = {
            "total_hooks": len(self.hooks),
            "hooks": {}
        }
        
        for name, hook in self.hooks.items():
            stats["hooks"][name] = {
                "description": hook["description"],
                "call_count": hook["call_count"],
                "last_called": hook["last_called"].isoformat() if hook["last_called"] else None,
                "registered_at": hook["registered_at"].isoformat()
            }
        
        return stats
    
    def list_available_hooks(self) -> List[str]:
        """List all available hooks"""
        return list(self.hooks.keys())
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get overall integration status"""
        # Check if original scripts exist
        original_scripts = [
            "helper_scripts/system_validation.py",
            "helper_scripts/quick_status.py",
            "tools/system_verification.py",
            "main.py",
            "crypto_launcher.py"
        ]
        
        script_status = {}
        for script in original_scripts:
            script_path = self.project_root / script
            backup_path = script_path.with_suffix(script_path.suffix + ".original")
            
            script_status[script] = {
                "exists": script_path.exists(),
                "has_backup": backup_path.exists(),
                "integrated": backup_path.exists()  # If backup exists, we've integrated
            }
        
        return {
            "project_root": str(self.project_root),
            "orchestrator_available": self.orchestrator is not None,
            "registered_hooks": len(self.hooks),
            "script_status": script_status,
            "integration_ready": all(status["exists"] for status in script_status.values())
        }