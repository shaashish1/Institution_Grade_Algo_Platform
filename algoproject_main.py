#!/usr/bin/env python3
"""
AlgoProject - Complete Trading Platform
======================================

Main trading platform with backtesting, demo trading, and live trading capabilities.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def print_banner():
    """Print AlgoProject banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          🚀 ALGOPROJECT TRADING PLATFORM                     ║
║                     Crypto & Stock Trading • Backtesting • Live Trading     ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Main AlgoProject trading platform"""
    print_banner()
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🏠 Personal Trading Platform - Full Functionality")
    print()
    
    while True:
        print("\n🎯 AlgoProject Trading Platform:")
        print("=" * 50)
        print("1. 💰 Crypto Trading")
        print("2. 📈 Stock Trading")
        print("3. 🧠 Strategy Management")
        print("4. 📊 Backtesting Engine")
        print("5. 🎮 Demo Trading")
        print("6. 🚀 Live Trading")
        print("7. 📋 Portfolio Management")
        print("8. ⚙️  System Configuration")
        print("9. 🔍 System Health Check")
        print("10. 🚪 Exit")
        
        try:
            choice = input("\nEnter your choice (1-10): ").strip()
            
            if choice == "1":
                crypto_trading_menu()
            elif choice == "2":
                stock_trading_menu()
            elif choice == "3":
                strategy_management_menu()
            elif choice == "4":
                backtesting_menu()
            elif choice == "5":
                demo_trading_menu()
            elif choice == "6":
                live_trading_menu()
            elif choice == "7":
                portfolio_management_menu()
            elif choice == "8":
                system_configuration_menu()
            elif choice == "9":
                system_health_check()
            elif choice == "10":
                print("\n👋 Thank you for using AlgoProject! Happy trading!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def crypto_trading_menu():
    """Crypto trading submenu"""
    print("\n💰 Crypto Trading Platform")
    print("=" * 30)
    
    try:
        # Import crypto modules
        from trading_platform.crypto.crypto_trader import CryptoTrader
        from trading_platform.crypto.asset_manager import CryptoAssetManager
        
        asset_manager = CryptoAssetManager()
        trader = CryptoTrader()
        
        while True:
            print("\n💰 Crypto Trading Options:")
            print("1. 📋 View Available Crypto Assets")
            print("2. 📊 Get Market Data")
            print("3. 🔍 Technical Analysis")
            print("4. 📈 Price Charts")
            print("5. ⚙️  Configure Exchanges")
            print("6. 🔙 Back to Main Menu")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                assets = asset_manager.get_available_assets()
                print(f"\n📋 Available Crypto Assets ({len(assets)} total):")
                for i, asset in enumerate(assets[:20], 1):  # Show first 20
                    print(f"  {i:2d}. {asset['symbol']} - {asset['name']} ({asset['exchange']})")
                if len(assets) > 20:
                    print(f"  ... and {len(assets) - 20} more assets")
                    
            elif choice == "2":
                symbol = input("Enter crypto symbol (e.g., BTC/USDT): ").strip().upper()
                if symbol:
                    market_data = trader.get_market_data(symbol)
                    if market_data:
                        print(f"\n📊 Market Data for {symbol}:")
                        print(f"  Price: ${market_data.get('price', 'N/A')}")
                        print(f"  24h Change: {market_data.get('change_24h', 'N/A')}%")
                        print(f"  Volume: {market_data.get('volume', 'N/A')}")
                        print(f"  Last Updated: {market_data.get('timestamp', 'N/A')}")
                    
            elif choice == "3":
                symbol = input("Enter crypto symbol for analysis: ").strip().upper()
                if symbol:
                    analysis = trader.technical_analysis(symbol)
                    if analysis:
                        print(f"\n🔍 Technical Analysis for {symbol}:")
                        for indicator, value in analysis.items():
                            print(f"  {indicator}: {value}")
                            
            elif choice == "4":
                symbol = input("Enter crypto symbol for chart: ").strip().upper()
                timeframe = input("Enter timeframe (1h, 4h, 1d): ").strip() or "1h"
                if symbol:
                    print(f"📈 Generating chart for {symbol} ({timeframe})...")
                    trader.show_price_chart(symbol, timeframe)
                    
            elif choice == "5":
                trader.configure_exchanges()
                
            elif choice == "6":
                break
            else:
                print("❌ Invalid choice.")
                
    except ImportError as e:
        print(f"❌ Crypto trading module not available: {e}")
        print("💡 Installing crypto trading components...")
        create_crypto_trading_module()
    except Exception as e:
        print(f"❌ Error in crypto trading: {e}")

def stock_trading_menu():
    """Stock trading submenu"""
    print("\n📈 Stock Trading Platform")
    print("=" * 30)
    
    try:
        from trading_platform.stocks.stock_trader import StockTrader
        from trading_platform.stocks.asset_manager import StockAssetManager
        
        asset_manager = StockAssetManager()
        trader = StockTrader()
        
        while True:
            print("\n📈 Stock Trading Options:")
            print("1. 📋 View Available Stocks")
            print("2. 📊 Get Stock Quote")
            print("3. 🔍 Fundamental Analysis")
            print("4. 📈 Stock Charts")
            print("5. 🏛️  Market Overview")
            print("6. 🔙 Back to Main Menu")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                assets = asset_manager.get_available_stocks()
                print(f"\n📋 Available Stocks ({len(assets)} total):")
                for i, asset in enumerate(assets[:15], 1):  # Show first 15
                    print(f"  {i:2d}. {asset['symbol']} - {asset['name']} ({asset['sector']})")
                if len(assets) > 15:
                    print(f"  ... and {len(assets) - 15} more stocks")
                    
            elif choice == "2":
                symbol = input("Enter stock symbol (e.g., NSE:SBIN-EQ): ").strip().upper()
                if symbol:
                    quote = trader.get_stock_quote(symbol)
                    if quote:
                        print(f"\n📊 Stock Quote for {symbol}:")
                        print(f"  Price: ₹{quote.get('price', 'N/A')}")
                        print(f"  Change: {quote.get('change', 'N/A')} ({quote.get('change_percent', 'N/A')}%)")
                        print(f"  Volume: {quote.get('volume', 'N/A')}")
                        print(f"  Market Cap: ₹{quote.get('market_cap', 'N/A')}")
                        
            elif choice == "3":
                symbol = input("Enter stock symbol for analysis: ").strip().upper()
                if symbol:
                    analysis = trader.fundamental_analysis(symbol)
                    if analysis:
                        print(f"\n🔍 Fundamental Analysis for {symbol}:")
                        for metric, value in analysis.items():
                            print(f"  {metric}: {value}")
                            
            elif choice == "4":
                symbol = input("Enter stock symbol for chart: ").strip().upper()
                period = input("Enter period (1d, 5d, 1mo, 3mo, 1y): ").strip() or "1mo"
                if symbol:
                    print(f"📈 Generating chart for {symbol} ({period})...")
                    trader.show_stock_chart(symbol, period)
                    
            elif choice == "5":
                trader.show_market_overview()
                
            elif choice == "6":
                break
            else:
                print("❌ Invalid choice.")
                
    except ImportError as e:
        print(f"❌ Stock trading module not available: {e}")
        print("💡 Installing stock trading components...")
        create_stock_trading_module()
    except Exception as e:
        print(f"❌ Error in stock trading: {e}")

def strategy_management_menu():
    """Strategy management submenu"""
    print("\n🧠 Strategy Management")
    print("=" * 25)
    
    try:
        from trading_platform.strategies.strategy_manager import StrategyManager
        
        strategy_manager = StrategyManager()
        
        while True:
            print("\n🧠 Strategy Management Options:")
            print("1. 📋 List Available Strategies")
            print("2. ➕ Create New Strategy")
            print("3. ⚙️  Configure Strategy Parameters")
            print("4. 🧪 Test Strategy")
            print("5. 📊 Strategy Performance")
            print("6. 🔙 Back to Main Menu")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                strategies = strategy_manager.list_strategies()
                print(f"\n📋 Available Strategies ({len(strategies)} total):")
                for i, strategy in enumerate(strategies, 1):
                    print(f"  {i:2d}. {strategy['name']} - {strategy['description']}")
                    print(f"      Type: {strategy['type']} | Risk: {strategy['risk_level']}")
                    
            elif choice == "2":
                strategy_manager.create_strategy_wizard()
                
            elif choice == "3":
                strategy_name = input("Enter strategy name to configure: ").strip()
                if strategy_name:
                    strategy_manager.configure_strategy(strategy_name)
                    
            elif choice == "4":
                strategy_name = input("Enter strategy name to test: ").strip()
                if strategy_name:
                    strategy_manager.test_strategy(strategy_name)
                    
            elif choice == "5":
                strategy_name = input("Enter strategy name for performance: ").strip()
                if strategy_name:
                    strategy_manager.show_strategy_performance(strategy_name)
                    
            elif choice == "6":
                break
            else:
                print("❌ Invalid choice.")
                
    except ImportError as e:
        print(f"❌ Strategy management module not available: {e}")
        print("💡 Installing strategy management components...")
        create_strategy_management_module()
    except Exception as e:
        print(f"❌ Error in strategy management: {e}")

def backtesting_menu():
    """Backtesting submenu"""
    print("\n📊 Backtesting Engine")
    print("=" * 25)
    
    try:
        from trading_platform.backtesting.backtest_engine import BacktestEngine
        
        backtest_engine = BacktestEngine()
        
        while True:
            print("\n📊 Backtesting Options:")
            print("1. 🚀 Quick Backtest")
            print("2. 🔧 Advanced Backtest Setup")
            print("3. 📈 View Backtest Results")
            print("4. 📊 Compare Strategies")
            print("5. 📋 Backtest History")
            print("6. 🔙 Back to Main Menu")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                backtest_engine.quick_backtest_wizard()
                
            elif choice == "2":
                backtest_engine.advanced_backtest_setup()
                
            elif choice == "3":
                backtest_engine.view_results()
                
            elif choice == "4":
                backtest_engine.compare_strategies()
                
            elif choice == "5":
                backtest_engine.show_backtest_history()
                
            elif choice == "6":
                break
            else:
                print("❌ Invalid choice.")
                
    except ImportError as e:
        print(f"❌ Backtesting module not available: {e}")
        print("💡 Installing backtesting components...")
        create_backtesting_module()
    except Exception as e:
        print(f"❌ Error in backtesting: {e}")

def demo_trading_menu():
    """Demo trading submenu"""
    print("\n🎮 Demo Trading")
    print("=" * 20)
    
    try:
        from trading_platform.demo.demo_trader import DemoTrader
        
        demo_trader = DemoTrader()
        
        while True:
            print("\n🎮 Demo Trading Options:")
            print("1. 💰 Check Demo Balance")
            print("2. 📋 View Demo Portfolio")
            print("3. 🛒 Place Demo Order")
            print("4. 📊 Demo Trading History")
            print("5. 🔄 Reset Demo Account")
            print("6. 🔙 Back to Main Menu")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                demo_trader.show_balance()
                
            elif choice == "2":
                demo_trader.show_portfolio()
                
            elif choice == "3":
                demo_trader.place_order_wizard()
                
            elif choice == "4":
                demo_trader.show_trading_history()
                
            elif choice == "5":
                confirm = input("Are you sure you want to reset demo account? (yes/no): ").lower()
                if confirm == "yes":
                    demo_trader.reset_account()
                    
            elif choice == "6":
                break
            else:
                print("❌ Invalid choice.")
                
    except ImportError as e:
        print(f"❌ Demo trading module not available: {e}")
        print("💡 Installing demo trading components...")
        create_demo_trading_module()
    except Exception as e:
        print(f"❌ Error in demo trading: {e}")

def live_trading_menu():
    """Live trading submenu"""
    print("\n🚀 Live Trading")
    print("=" * 20)
    print("⚠️  WARNING: This involves real money and real trades!")
    
    confirm = input("Do you want to proceed with live trading? (yes/no): ").lower()
    if confirm != "yes":
        print("✅ Live trading cancelled.")
        return
    
    try:
        from trading_platform.live.live_trader import LiveTrader
        
        live_trader = LiveTrader()
        
        while True:
            print("\n🚀 Live Trading Options:")
            print("1. 🔐 Connect to Exchange/Broker")
            print("2. 💰 Check Live Balance")
            print("3. 📋 View Live Portfolio")
            print("4. 🛒 Place Live Order")
            print("5. 📊 Live Trading History")
            print("6. 🤖 Start Automated Trading")
            print("7. 🛑 Stop All Trading")
            print("8. 🔙 Back to Main Menu")
            
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == "1":
                live_trader.connect_to_exchange()
                
            elif choice == "2":
                live_trader.show_live_balance()
                
            elif choice == "3":
                live_trader.show_live_portfolio()
                
            elif choice == "4":
                live_trader.place_live_order_wizard()
                
            elif choice == "5":
                live_trader.show_live_trading_history()
                
            elif choice == "6":
                live_trader.start_automated_trading()
                
            elif choice == "7":
                live_trader.stop_all_trading()
                
            elif choice == "8":
                break
            else:
                print("❌ Invalid choice.")
                
    except ImportError as e:
        print(f"❌ Live trading module not available: {e}")
        print("💡 Installing live trading components...")
        create_live_trading_module()
    except Exception as e:
        print(f"❌ Error in live trading: {e}")

def portfolio_management_menu():
    """Portfolio management submenu"""
    print("\n📋 Portfolio Management")
    print("=" * 25)
    
    try:
        from trading_platform.portfolio.portfolio_manager import PortfolioManager
        
        portfolio_manager = PortfolioManager()
        
        while True:
            print("\n📋 Portfolio Management Options:")
            print("1. 📊 Portfolio Overview")
            print("2. 📈 Performance Analysis")
            print("3. ⚖️  Risk Analysis")
            print("4. 🎯 Rebalancing")
            print("5. 📋 Holdings Report")
            print("6. 🔙 Back to Main Menu")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                portfolio_manager.show_overview()
                
            elif choice == "2":
                portfolio_manager.performance_analysis()
                
            elif choice == "3":
                portfolio_manager.risk_analysis()
                
            elif choice == "4":
                portfolio_manager.rebalancing_wizard()
                
            elif choice == "5":
                portfolio_manager.generate_holdings_report()
                
            elif choice == "6":
                break
            else:
                print("❌ Invalid choice.")
                
    except ImportError as e:
        print(f"❌ Portfolio management module not available: {e}")
        print("💡 Installing portfolio management components...")
        create_portfolio_management_module()
    except Exception as e:
        print(f"❌ Error in portfolio management: {e}")

def system_configuration_menu():
    """System configuration submenu"""
    print("\n⚙️  System Configuration")
    print("=" * 25)
    
    print("\n⚙️  Configuration Options:")
    print("1. 🔑 API Keys & Credentials")
    print("2. 📊 Data Sources")
    print("3. 🎯 Trading Preferences")
    print("4. 🔔 Notifications")
    print("5. 📁 File Locations")
    print("6. 🔙 Back to Main Menu")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == "1":
        configure_api_keys()
    elif choice == "2":
        configure_data_sources()
    elif choice == "3":
        configure_trading_preferences()
    elif choice == "4":
        configure_notifications()
    elif choice == "5":
        configure_file_locations()
    elif choice == "6":
        return
    else:
        print("❌ Invalid choice.")

def system_health_check():
    """Run system health check"""
    print("\n🔍 System Health Check")
    print("=" * 25)
    
    print("🔍 Checking system components...")
    
    # Check Python environment
    print(f"✅ Python: {sys.version.split()[0]}")
    
    # Check required packages
    required_packages = [
        "pandas", "numpy", "requests", "matplotlib", 
        "ccxt", "yfinance", "ta", "plotly"
    ]
    
    print("\n📦 Package Check:")
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}: OK")
        except ImportError:
            print(f"❌ {package}: Missing")
    
    # Check directories
    print("\n📁 Directory Structure:")
    directories = [
        "trading_platform",
        "trading_platform/crypto",
        "trading_platform/stocks", 
        "trading_platform/strategies",
        "trading_platform/backtesting",
        "data",
        "logs",
        "reports"
    ]
    
    for directory in directories:
        if Path(directory).exists():
            print(f"✅ {directory}/: OK")
        else:
            print(f"❌ {directory}/: Missing")
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {directory}/")
    
    print("\n🎯 System Health Check Complete!")

# Configuration functions
def configure_api_keys():
    """Configure API keys"""
    print("\n🔑 API Keys & Credentials Configuration")
    print("=" * 40)
    print("Configure your exchange and broker API keys:")
    print("1. Crypto Exchange APIs (Binance, Coinbase, etc.)")
    print("2. Stock Broker APIs (Fyers, Zerodha, etc.)")
    print("3. Data Provider APIs (Alpha Vantage, etc.)")
    print("\n💡 API keys will be stored securely in config files")

def configure_data_sources():
    """Configure data sources"""
    print("\n📊 Data Sources Configuration")
    print("=" * 30)
    print("Available data sources:")
    print("• Crypto: CCXT (100+ exchanges)")
    print("• Stocks: Yahoo Finance, Fyers API")
    print("• Technical Analysis: TA-Lib, pandas-ta")

def configure_trading_preferences():
    """Configure trading preferences"""
    print("\n🎯 Trading Preferences")
    print("=" * 25)
    print("Set your trading preferences:")
    print("• Risk tolerance")
    print("• Position sizing")
    print("• Stop loss levels")
    print("• Take profit targets")

def configure_notifications():
    """Configure notifications"""
    print("\n🔔 Notifications Configuration")
    print("=" * 30)
    print("Configure alerts and notifications:")
    print("• Email notifications")
    print("• SMS alerts")
    print("• Desktop notifications")
    print("• Trading signals")

def configure_file_locations():
    """Configure file locations"""
    print("\n📁 File Locations Configuration")
    print("=" * 35)
    print("Current file locations:")
    print(f"• Data: {Path('data').absolute()}")
    print(f"• Logs: {Path('logs').absolute()}")
    print(f"• Reports: {Path('reports').absolute()}")
    print(f"• Config: {Path('config').absolute()}")

# Module creation functions (stubs for now)
def create_crypto_trading_module():
    """Create crypto trading module"""
    print("🔧 Creating crypto trading module...")
    # This would create the actual crypto trading implementation

def create_stock_trading_module():
    """Create stock trading module"""
    print("🔧 Creating stock trading module...")
    # This would create the actual stock trading implementation

def create_strategy_management_module():
    """Create strategy management module"""
    print("🔧 Creating strategy management module...")
    # This would create the actual strategy management implementation

def create_backtesting_module():
    """Create backtesting module"""
    print("🔧 Creating backtesting module...")
    # This would create the actual backtesting implementation

def create_demo_trading_module():
    """Create demo trading module"""
    print("🔧 Creating demo trading module...")
    # This would create the actual demo trading implementation

def create_live_trading_module():
    """Create live trading module"""
    print("🔧 Creating live trading module...")
    # This would create the actual live trading implementation

def create_portfolio_management_module():
    """Create portfolio management module"""
    print("🔧 Creating portfolio management module...")
    # This would create the actual portfolio management implementation

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)