#!/usr/bin/env python3
"""
Comprehensive System Test - Main Entry Point
===========================================

Main executable for the comprehensive system testing framework.
"""

import argparse
import sys
import os
from pathlib import Path
from datetime import datetime

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from comprehensive_system_testing.core.test_orchestrator import TestOrchestrator
from comprehensive_system_testing.core.config_manager import ConfigManager
from comprehensive_system_testing.core.models import TestConfiguration
from comprehensive_system_testing.user.user_manager import UserManager
from comprehensive_system_testing.user.auth_provider import AuthProvider
from comprehensive_system_testing.utils.logger import TestLogger


def print_banner():
    """Print application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🔍 COMPREHENSIVE SYSTEM TESTING                           ║
║                         AlgoProject Testing Framework                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def create_argument_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Comprehensive System Testing Framework for AlgoProject",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --comprehensive /path/to/project
  %(prog)s --quick /path/to/project
  %(prog)s --targeted syntax,imports /path/to/project
  %(prog)s --config --create-default
  %(prog)s --user --create user@example.com "User Name"
        """
    )
    
    # Test execution modes
    test_group = parser.add_argument_group('Test Execution')
    test_group.add_argument(
        '--comprehensive', '-c',
        metavar='TARGET',
        help='Run comprehensive system test on target directory'
    )
    test_group.add_argument(
        '--quick', '-q',
        metavar='TARGET',
        help='Run quick test on target directory'
    )
    test_group.add_argument(
        '--targeted', '-t',
        nargs=2,
        metavar=('COMPONENTS', 'TARGET'),
        help='Run targeted test on specific components (comma-separated) and target'
    )
    test_group.add_argument(
        '--continuous',
        nargs=2,
        metavar=('TARGET', 'INTERVAL'),
        help='Run continuous monitoring on target with interval in minutes'
    )
    
    # Configuration management
    config_group = parser.add_argument_group('Configuration')
    config_group.add_argument(
        '--config',
        action='store_true',
        help='Configuration management mode'
    )
    config_group.add_argument(
        '--create-default',
        action='store_true',
        help='Create default configuration files'
    )
    config_group.add_argument(
        '--validate-config',
        action='store_true',
        help='Validate configuration files'
    )
    config_group.add_argument(
        '--show-config',
        action='store_true',
        help='Show current configuration'
    )
    
    # User management
    user_group = parser.add_argument_group('User Management')
    user_group.add_argument(
        '--user',
        action='store_true',
        help='User management mode'
    )
    user_group.add_argument(
        '--create',
        nargs=2,
        metavar=('EMAIL', 'NAME'),
        help='Create new user profile'
    )
    user_group.add_argument(
        '--login',
        metavar='EMAIL',
        help='Login user'
    )
    user_group.add_argument(
        '--list-users',
        action='store_true',
        help='List all users'
    )
    
    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument(
        '--format',
        choices=['console', 'html', 'json', 'csv', 'all'],
        default='console',
        help='Output format (default: console)'
    )
    output_group.add_argument(
        '--output-dir',
        metavar='DIR',
        default='test_reports',
        help='Output directory for reports (default: test_reports)'
    )
    output_group.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    output_group.add_argument(
        '--quiet',
        action='store_true',
        help='Quiet mode (minimal output)'
    )
    
    # Advanced options
    advanced_group = parser.add_argument_group('Advanced Options')
    advanced_group.add_argument(
        '--no-auto-fix',
        action='store_true',
        help='Disable automatic fixing'
    )
    advanced_group.add_argument(
        '--parallel',
        action='store_true',
        help='Enable parallel execution'
    )
    advanced_group.add_argument(
        '--timeout',
        type=int,
        default=300,
        help='Test timeout in seconds (default: 300)'
    )
    advanced_group.add_argument(
        '--severity-threshold',
        choices=['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
        default='MEDIUM',
        help='Minimum severity threshold (default: MEDIUM)'
    )
    
    # Information
    info_group = parser.add_argument_group('Information')
    info_group.add_argument(
        '--version',
        action='version',
        version='Comprehensive System Testing Framework v1.0.0'
    )
    info_group.add_argument(
        '--info',
        action='store_true',
        help='Show system information'
    )
    
    return parser


def handle_comprehensive_test(target: str, args) -> int:
    """Handle comprehensive test execution"""
    logger = TestLogger()
    
    try:
        print(f"🔍 Starting comprehensive test on: {target}")
        print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Load configuration
        config_manager = ConfigManager()
        config = config_manager.load_configuration()
        
        # Apply command line overrides
        if args.no_auto_fix:
            config.auto_fix_enabled = False
        if args.parallel:
            config.parallel_execution = True
        if args.timeout:
            config.timeout_seconds = args.timeout
        
        # Create orchestrator and run test
        orchestrator = TestOrchestrator(config)
        result = orchestrator.run_comprehensive_test(target)
        
        # Handle results
        if "error" in result:
            print(f"❌ Test failed: {result['error']}")
            return 1
        
        results = result.get("results", [])
        system_health = result.get("system_health")
        
        print(f"✅ Comprehensive test completed!")
        print(f"📊 Total tests: {len(results)}")
        print(f"⏱️  Execution time: {result.get('execution_time', 0):.2f} seconds")
        
        if system_health:
            print(f"🏥 System health: {system_health.overall_score:.1f}/100")
        
        # Generate reports if requested
        if args.format != 'console':
            report_files = result.get("report_files", {})
            if report_files:
                print(f"📄 Reports generated:")
                for format_name, file_path in report_files.items():
                    print(f"   • {format_name.upper()}: {file_path}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Comprehensive test failed: {e}")
        print(f"❌ Error: {e}")
        return 1


def handle_quick_test(target: str, args) -> int:
    """Handle quick test execution"""
    logger = TestLogger()
    
    try:
        print(f"⚡ Starting quick test on: {target}")
        
        # Load configuration
        config_manager = ConfigManager()
        config = config_manager.load_configuration()
        
        # Create orchestrator and run test
        orchestrator = TestOrchestrator(config)
        result = orchestrator.run_quick_test(target)
        
        if "error" in result:
            print(f"❌ Test failed: {result['error']}")
            return 1
        
        results = result.get("results", [])
        print(f"✅ Quick test completed!")
        print(f"📊 Tests run: {len(results)}")
        print(f"⏱️  Execution time: {result.get('execution_time', 0):.2f} seconds")
        
        return 0
        
    except Exception as e:
        logger.error(f"Quick test failed: {e}")
        print(f"❌ Error: {e}")
        return 1


def handle_targeted_test(components_str: str, target: str, args) -> int:
    """Handle targeted test execution"""
    logger = TestLogger()
    
    try:
        components = [c.strip() for c in components_str.split(',')]
        print(f"🎯 Starting targeted test on: {target}")
        print(f"🔧 Components: {', '.join(components)}")
        
        # Load configuration
        config_manager = ConfigManager()
        config = config_manager.load_configuration()
        
        # Create orchestrator and run test
        orchestrator = TestOrchestrator(config)
        result = orchestrator.run_targeted_test(target, components)
        
        if "error" in result:
            print(f"❌ Test failed: {result['error']}")
            return 1
        
        results = result.get("results", [])
        print(f"✅ Targeted test completed!")
        print(f"📊 Tests run: {len(results)}")
        print(f"⏱️  Execution time: {result.get('execution_time', 0):.2f} seconds")
        
        return 0
        
    except Exception as e:
        logger.error(f"Targeted test failed: {e}")
        print(f"❌ Error: {e}")
        return 1


def handle_configuration_management(args) -> int:
    """Handle configuration management"""
    config_manager = ConfigManager()
    
    try:
        if args.create_default:
            print("🔧 Creating default configuration files...")
            success = config_manager.create_default_configuration()
            if success:
                print("✅ Default configuration created successfully!")
                return 0
            else:
                print("❌ Failed to create default configuration")
                return 1
        
        elif args.validate_config:
            print("🔍 Validating configuration files...")
            issues = config_manager.validate_configuration()
            
            if not issues:
                print("✅ All configuration files are valid!")
                return 0
            else:
                print("❌ Configuration issues found:")
                for issue in issues:
                    print(f"   • {issue}")
                return 1
        
        elif args.show_config:
            print("📋 Current Configuration:")
            print("-" * 50)
            
            config_info = config_manager.get_configuration_info()
            for key, value in config_info.items():
                if isinstance(value, list):
                    print(f"{key}: {', '.join(map(str, value))}")
                else:
                    print(f"{key}: {value}")
            
            return 0
        
        else:
            print("❓ No configuration action specified. Use --help for options.")
            return 1
            
    except Exception as e:
        print(f"❌ Configuration management error: {e}")
        return 1


def handle_user_management(args) -> int:
    """Handle user management"""
    user_manager = UserManager()
    
    try:
        if args.create:
            email, name = args.create
            print(f"👤 Creating user profile for: {email}")
            
            # Get password securely
            import getpass
            password = getpass.getpass("Enter password: ")
            
            profile = user_manager.create_user_profile(email, name, password)
            print(f"✅ User profile created successfully!")
            print(f"   User ID: {profile.user_id}")
            print(f"   Email: {profile.email}")
            print(f"   Name: {profile.name}")
            
            return 0
        
        elif args.login:
            email = args.login
            print(f"🔐 Logging in user: {email}")
            
            import getpass
            password = getpass.getpass("Enter password: ")
            
            profile = user_manager.authenticate_user(email, password)
            if profile:
                print(f"✅ Login successful!")
                print(f"   Welcome back, {profile.name}!")
                
                # Create session
                auth_provider = AuthProvider()
                session_token = auth_provider.create_session(profile.user_id)
                print(f"   Session token: {session_token}")
                
                return 0
            else:
                print("❌ Login failed. Invalid credentials.")
                return 1
        
        elif args.list_users:
            print("👥 Registered Users:")
            print("-" * 50)
            
            users = user_manager.list_users()
            if not users:
                print("No users found.")
                return 0
            
            for user in users:
                print(f"• {user['name']} ({user['email']})")
                print(f"  ID: {user['user_id']}")
                print(f"  Created: {user['created_at']}")
                print(f"  Tests: {user['test_count']}")
                print()
            
            return 0
        
        else:
            print("❓ No user action specified. Use --help for options.")
            return 1
            
    except Exception as e:
        print(f"❌ User management error: {e}")
        return 1


def show_system_info():
    """Show system information"""
    print("🖥️  System Information:")
    print("-" * 50)
    
    # Python version
    print(f"Python: {sys.version}")
    
    # Framework version
    print("Framework: Comprehensive System Testing v1.0.0")
    
    # Available components
    print("Available test components:")
    components = [
        "syntax_validator - Python syntax validation",
        "import_tester - Import and dependency testing", 
        "dependency_checker - External package validation",
        "config_validator - Configuration file validation",
        "integration_tester - API and module integration testing"
    ]
    
    for component in components:
        print(f"  • {component}")
    
    # Execution modes
    print("\nExecution modes:")
    modes = [
        "comprehensive - Full system validation",
        "quick - Essential checks only",
        "targeted - Specific component testing",
        "continuous - Background monitoring"
    ]
    
    for mode in modes:
        print(f"  • {mode}")


def main():
    """Main entry point"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Show banner unless in quiet mode
    if not args.quiet:
        print_banner()
    
    # Handle different modes
    try:
        # Information mode
        if args.info:
            show_system_info()
            return 0
        
        # Configuration management
        if args.config:
            return handle_configuration_management(args)
        
        # User management
        if args.user:
            return handle_user_management(args)
        
        # Test execution modes
        if args.comprehensive:
            return handle_comprehensive_test(args.comprehensive, args)
        
        elif args.quick:
            return handle_quick_test(args.quick, args)
        
        elif args.targeted:
            components, target = args.targeted
            return handle_targeted_test(components, target, args)
        
        elif args.continuous:
            target, interval = args.continuous
            print(f"🔄 Starting continuous monitoring on: {target}")
            print(f"⏰ Interval: {interval} minutes")
            print("Note: Continuous monitoring is not fully implemented in this version")
            return 0
        
        else:
            # No action specified, show help
            parser.print_help()
            return 0
            
    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user")
        return 130
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())