#!/usr/bin/env python3
"""
AlgoProject Enhanced Crypto Backtest Runner
Simplified wrapper to run the enhanced crypto backtest using the project's Python environment
"""

import subprocess
import sys
import os

def main():
    """Run the enhanced crypto backtest with the project's Python environment."""
    
    # Get the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the project's Python executable
    python_exe = os.path.join(project_root, 'venv', 'Scripts', 'python.exe')
    
    # Path to the enhanced crypto backtest script
    backtest_script = os.path.join(project_root, 'crypto', 'scripts', 'enhanced_crypto_backtest.py')
    
    # Check if Python executable exists
    if not os.path.exists(python_exe):
        print(f"❌ Python executable not found at: {python_exe}")
        print("Please ensure the virtual environment is set up correctly.")
        return 1
    
    # Check if backtest script exists
    if not os.path.exists(backtest_script):
        print(f"❌ Backtest script not found at: {backtest_script}")
        return 1
    
    # Prepare the command
    cmd = [python_exe, backtest_script] + sys.argv[1:]
    
    print(f"🚀 Running Enhanced Crypto Backtest with AlgoProject's Python environment...")
    print(f"📂 Project Root: {project_root}")
    print(f"🐍 Python Executable: {python_exe}")
    print(f"📜 Command: {' '.join(cmd)}")
    print("=" * 80)
    
    # Run the command
    try:
        result = subprocess.run(cmd, cwd=project_root, check=False)
        return result.returncode
    except Exception as e:
        print(f"❌ Error running backtest: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
