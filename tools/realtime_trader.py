#!/usr/bin/env python3
"""
Real-time Trading Framework
==========================

Framework for real-time trading execution across crypto and stock markets.
Provides unified interface for live trading operations.
"""

import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path
import threading

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class RealTimeTrader:
    """
    Real-time trading framework supporting both crypto and stocks.
    """
    
    def __init__(self, mode='demo', initial_balance=10000):
        """
        Initialize real-time trader.
        
        Args:
            mode: 'demo' or 'live' trading mode
            initial_balance: Starting balance for demo mode
        """
        self.mode = mode
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.positions = {}
        self.trades = []
        self.is_running = False
        self.lock = threading.Lock()
        
        # Set up logging
        self.setup_logging()
        
        if mode == 'live':
            self.logger.warning("🔴 LIVE TRADING MODE - Real money at risk!")
        else:
            self.logger.info("🟡 DEMO TRADING MODE - Paper trading only")
    
    def setup_logging(self):
        """Set up logging for trading session."""
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"logs/realtime_trader_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Real-time trader initialized in {self.mode} mode")
    
    def start_crypto_trading(self, symbols=None, strategy='VWAPSigma2Strategy'):
        """Start real-time crypto trading."""
        self.logger.info(f"Starting crypto trading: {symbols or 'all symbols'}")
        
        try:
            if self.mode == 'demo':
                # Import and run crypto demo
                sys.path.append(str(project_root / 'crypto' / 'scripts'))
                from crypto_demo_live import run_crypto_demo_live
                run_crypto_demo_live()
            else:
                self.logger.error("Live crypto trading not implemented yet")
                return False
        except Exception as e:
            self.logger.error(f"Crypto trading failed: {e}")
            return False
        
        return True
    
    def start_stock_trading(self, symbols=None, strategy='VWAPSigma2Strategy'):
        """Start real-time stock trading."""
        self.logger.info(f"Starting stock trading: {symbols or 'all symbols'}")
        
        try:
            if self.mode == 'demo':
                # Import and run stock demo
                sys.path.append(str(project_root / 'stocks' / 'scripts'))
                from stocks_demo_live import run_stocks_demo_live
                run_stocks_demo_live()
            else:
                self.logger.error("Live stock trading not implemented yet")
                return False
        except Exception as e:
            self.logger.error(f"Stock trading failed: {e}")
            return False
        
        return True
    
    def start_multi_asset_trading(self, crypto_symbols=None, stock_symbols=None):
        """Start trading across multiple asset classes."""
        self.logger.info("Starting multi-asset trading session")
        
        if not crypto_symbols and not stock_symbols:
            self.logger.error("No symbols specified for trading")
            return False
        
        try:
            # Start crypto trading in separate thread if symbols provided
            if crypto_symbols:
                crypto_thread = threading.Thread(
                    target=self.start_crypto_trading,
                    args=(crypto_symbols,),
                    name="CryptoTrader"
                )
                crypto_thread.daemon = True
                crypto_thread.start()
                self.logger.info("Crypto trading thread started")
            
            # Start stock trading in separate thread if symbols provided
            if stock_symbols:
                stock_thread = threading.Thread(
                    target=self.start_stock_trading,
                    args=(stock_symbols,),
                    name="StockTrader"
                )
                stock_thread.daemon = True
                stock_thread.start()
                self.logger.info("Stock trading thread started")
            
            # Keep main thread alive
            try:
                while True:
                    time.sleep(30)
                    self.logger.info("Multi-asset trader heartbeat...")
            except KeyboardInterrupt:
                self.logger.info("Multi-asset trading stopped by user")
        
        except Exception as e:
            self.logger.error(f"Multi-asset trading failed: {e}")
            return False
        
        return True
    
    def stop_trading(self):
        """Stop all trading activities."""
        self.is_running = False
        self.logger.info("Trading stopped")

def main():
    """Main entry point for real-time trader."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Real-time Trading Framework')
    parser.add_argument('--mode', choices=['demo', 'live'], default='demo',
                       help='Trading mode (default: demo)')
    parser.add_argument('--market', choices=['crypto', 'stocks', 'both'], default='crypto',
                       help='Market to trade (default: crypto)')
    parser.add_argument('--crypto-symbols', nargs='*',
                       help='Crypto symbols to trade (e.g., BTC/USDT ETH/USDT)')
    parser.add_argument('--stock-symbols', nargs='*',
                       help='Stock symbols to trade (e.g., RELIANCE TCS)')
    parser.add_argument('--strategy', default='VWAPSigma2Strategy',
                       help='Strategy to use (default: VWAPSigma2Strategy)')
    
    args = parser.parse_args()
    
    print("🚀 AlgoProject Real-time Trader")
    print("=" * 50)
    print(f"Mode: {args.mode}")
    print(f"Market: {args.market}")
    print(f"Strategy: {args.strategy}")
    
    if args.mode == 'live':
        print("⚠️  WARNING: Live trading mode selected!")
        confirm = input("Are you sure you want to proceed with live trading? (type 'YES' to confirm): ")
        if confirm != 'YES':
            print("❌ Live trading cancelled")
            return
    
    print("=" * 50)
    
    trader = RealTimeTrader(mode=args.mode)
    
    try:
        if args.market == 'crypto':
            trader.start_crypto_trading(args.crypto_symbols, args.strategy)
        elif args.market == 'stocks':
            trader.start_stock_trading(args.stock_symbols, args.strategy)
        else:  # both
            trader.start_multi_asset_trading(args.crypto_symbols, args.stock_symbols)
    except KeyboardInterrupt:
        print("\n⚠️ Trading interrupted by user")
        trader.stop_trading()
    except Exception as e:
        print(f"\n❌ Trading failed: {e}")

if __name__ == "__main__":
    main()
