#!/usr/bin/env python3
"""
AlgoProject - Main Entry Point
=============================

Unified entry point for the complete AlgoProject trading platform.
Provides access to both crypto and stock trading functionality.
"""

import os
import sys
import json
from datetime import datetime

def get_python_executable():
    """Get the correct Python executable (virtual environment if available)"""
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        return venv_python
    return "python"

def main():
    """Main AlgoProject entry point"""
    print("🚀 AlgoProject - Complete Trading Platform")
    print("=" * 50)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🏠 Personal Laptop Edition - Full Functionality")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("crypto"):
        print("❌ Error: Project structure not found!")
        print("💡 Make sure you're running this from the AlgoProject root directory")
        return
    
    while True:
        print("\n🎯 AlgoProject Trading Platform:")
        print("=" * 35)
        print("1. 💰 Crypto Trading Platform")
        print("2. 📈 Stock Trading Platform") 
        print("3. 🔧 System Health Check")
        print("4. 📁 Project Management")
        print("5. 📖 Documentation")
        print("6. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            print("\n🚀 Launching Crypto Trading Platform...")
            try:
                python_exec = get_python_executable()
                os.system(f"{python_exec} crypto_launcher.py")
            except Exception as e:
                print(f"❌ Error launching crypto platform: {e}")
                
        elif choice == "2":
            print("\n📈 Stock Trading Platform...")
            print("⚠️  Stock trading functionality is currently under development")
            print("💡 Focus on crypto trading for full functionality")
            print("📁 Stock modules available in stocks/ directory")
            print("🔧 For stock trading, configure Fyers API manually")
            input("Press Enter to continue...")
                
        elif choice == "3":
            run_system_health_check()
            
        elif choice == "4":
            show_project_management()
            
        elif choice == "5":
            show_documentation()
            
        elif choice == "6":
            print("\n👋 Goodbye! Happy trading!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

def run_system_health_check():
    """Comprehensive system health check"""
    print("\n🔧 AlgoProject System Health Check")
    print("=" * 35)
    
    # Check Python libraries
    libraries = [
        ("ccxt", "Crypto exchange library"),
        ("pandas", "Data analysis"),
        ("numpy", "Numerical computing"),
        ("requests", "HTTP requests"),
        ("matplotlib", "Plotting"),
        ("ta", "Technical analysis")
    ]
    
    print("\n📚 Library Check:")
    print("-" * 20)
    for lib, desc in libraries:
        try:
            __import__(lib)
            print(f"✅ {lib}: OK ({desc})")
        except ImportError:
            print(f"❌ {lib}: Missing ({desc})")
    
    # Check directory structure
    directories = [
        "crypto/",
        "crypto/input/",
        "crypto/output/", 
        "crypto/logs/",
        "crypto/scripts/",
        "stocks/",
        "strategies/",
        "tools/",
        "docs/"
    ]
    
    print("\n📁 Directory Structure:")
    print("-" * 25)
    for directory in directories:
        if os.path.exists(directory):
            print(f"✅ {directory}: OK")
        else:
            print(f"❌ {directory}: Missing")
    
    # Check key files
    key_files = [
        "requirements.txt",
        "crypto_launcher.py",
        "crypto_main.py",
        "main.py"
    ]
    
    print("\n📄 Key Files:")
    print("-" * 15)
    for file_path in key_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}: OK")
        else:
            print(f"❌ {file_path}: Missing")
    
    print("\n🎯 Health Check Complete!")

def show_project_management():
    """Show project management options"""
    print("\n📁 Project Management")
    print("=" * 20)
    print("1. View project structure")
    print("2. Check log files")
    print("3. View output files")
    print("4. Clean temporary files")
    print("5. Back to main menu")
    
    choice = input("\nEnter your choice: ").strip()
    
    if choice == "1":
        print("\n📂 Project Structure:")
        os.system("tree /F" if os.name == "nt" else "find . -type f")
    elif choice == "2":
        print("\n📝 Recent log files:")
        if os.path.exists("crypto/logs"):
            os.system("dir crypto\\logs" if os.name == "nt" else "ls -la crypto/logs/")
    elif choice == "3":
        print("\n📊 Output files:")
        if os.path.exists("crypto/output"):
            os.system("dir crypto\\output" if os.name == "nt" else "ls -la crypto/output/")

def show_documentation():
    """Show documentation links"""
    print("\n📖 AlgoProject Documentation")
    print("=" * 30)
    print("📄 Available Documentation:")
    print("• README.md - Project overview")
    print("• docs/ - Complete documentation")
    print("• SETUP_ISSUES_RESOLVED.md - Setup troubleshooting")
    print()
    print("🚀 Quick Start:")
    print("• Crypto Trading: python crypto_launcher.py")
    print("• System Check: python main.py (option 3)")
    print("• Health Check: Use crypto_launcher.py option 8")

if __name__ == "__main__":
    main()
