#!/usr/bin/env python3
"""
Launch Comprehensive System Testing
==================================

Launch script for the comprehensive system testing framework.
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Launch the comprehensive system testing framework"""
    print("🚀 Launching Comprehensive System Testing Framework")
    print("=" * 60)
    
    try:
        # Import the main entry point
        from comprehensive_system_testing.comprehensive_system_test import main as cst_main
        
        # Set up arguments for comprehensive test of current directory
        original_argv = sys.argv.copy()
        
        # Run comprehensive test on current directory
        sys.argv = [
            "comprehensive_system_test.py",
            "--comprehensive", 
            ".",
            "--format", "all",
            "--verbose"
        ]
        
        print("🔍 Running comprehensive test on current AlgoProject...")
        print("📊 Generating reports in all formats...")
        print("⚡ This may take a few minutes...")
        print()
        
        # Launch the comprehensive test
        result = cst_main()
        
        # Restore original argv
        sys.argv = original_argv
        
        if result == 0:
            print("\n🎉 Comprehensive System Testing completed successfully!")
            print("� Checlk the test_reports/ directory for detailed reports")
        else:
            print(f"\n⚠️  Testing completed with issues (exit code: {result})")
            
        return result
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        return 1
        
    except Exception as e:
        print(f"❌ Launch Error: {e}")
        print("💡 Check the logs for more details")
        return 1

if __name__ == "__main__":
    exit_code = main()
    
    print("\n" + "=" * 60)
    print("🏁 Launch Complete")
    
    if exit_code == 0:
        print("✅ System testing framework is operational!")
        print("\n📖 Next steps:")
        print("   • Check test_reports/ for detailed results")
        print("   • Run: python comprehensive_system_testing/comprehensive_system_test.py --help")
        print("   • Create user account: python comprehensive_system_testing/comprehensive_system_test.py --user --create")
    else:
        print("⚠️  Some issues were detected during testing")
        print("💡 Review the output above for details")
    
    sys.exit(exit_code)