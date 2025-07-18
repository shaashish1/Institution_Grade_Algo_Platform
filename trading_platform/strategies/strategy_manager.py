"""
Strategy Manager
===============

Manages trading strategies and their configurations.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class StrategyManager:
    """Manages trading strategies"""
    
    def __init__(self):
        self.strategies_dir = Path("data/strategies")
        self.strategies_dir.mkdir(parents=True, exist_ok=True)
        
        self.strategies_file = self.strategies_dir / "strategies.json"
        self.strategies = self.load_strategies()
    
    def load_strategies(self) -> List[Dict[str, Any]]:
        """Load available strategies"""
        try:
            if self.strategies_file.exists():
                with open(self.strategies_file, 'r') as f:
                    return json.load(f)
            else:
                return self.create_default_strategies()
        except Exception as e:
            print(f"❌ Error loading strategies: {e}")
            return self.create_default_strategies()
    
    def create_default_strategies(self) -> List[Dict[str, Any]]:
        """Create default trading strategies"""
        default_strategies = [
            {
                "id": "sma_crossover",
                "name": "SMA Crossover",
                "description": "Simple Moving Average crossover strategy",
                "type": "trend_following",
                "risk_level": "Medium",
                "parameters": {
                    "short_period": 10,
                    "long_period": 30,
                    "stop_loss": 0.02,
                    "take_profit": 0.04
                },
                "markets": ["crypto", "stocks"],
                "timeframes": ["1h", "4h", "1d"],
                "created_at": datetime.now().isoformat(),
                "active": True
            },
            {
                "id": "rsi_mean_reversion",
                "name": "RSI Mean Reversion",
                "description": "RSI-based mean reversion strategy",
                "type": "mean_reversion",
                "risk_level": "High",
                "parameters": {
                    "rsi_period": 14,
                    "oversold_level": 30,
                    "overbought_level": 70,
                    "stop_loss": 0.03,
                    "take_profit": 0.02
                },
                "markets": ["crypto", "stocks"],
                "timeframes": ["1h", "4h"],
                "created_at": datetime.now().isoformat(),
                "active": True
            },
            {
                "id": "macd_signal",
                "name": "MACD Signal",
                "description": "MACD signal line crossover strategy",
                "type": "momentum",
                "risk_level": "Medium",
                "parameters": {
                    "fast_period": 12,
                    "slow_period": 26,
                    "signal_period": 9,
                    "stop_loss": 0.025,
                    "take_profit": 0.035
                },
                "markets": ["crypto", "stocks"],
                "timeframes": ["1h", "4h", "1d"],
                "created_at": datetime.now().isoformat(),
                "active": True
            },
            {
                "id": "bollinger_bands",
                "name": "Bollinger Bands",
                "description": "Bollinger Bands breakout/reversion strategy",
                "type": "volatility",
                "risk_level": "Medium",
                "parameters": {
                    "period": 20,
                    "std_dev": 2,
                    "stop_loss": 0.02,
                    "take_profit": 0.03
                },
                "markets": ["crypto", "stocks"],
                "timeframes": ["1h", "4h", "1d"],
                "created_at": datetime.now().isoformat(),
                "active": True
            },
            {
                "id": "breakout_strategy",
                "name": "Breakout Strategy",
                "description": "Price breakout from consolidation ranges",
                "type": "breakout",
                "risk_level": "High",
                "parameters": {
                    "lookback_period": 20,
                    "breakout_threshold": 0.02,
                    "volume_confirmation": True,
                    "stop_loss": 0.015,
                    "take_profit": 0.045
                },
                "markets": ["crypto", "stocks"],
                "timeframes": ["4h", "1d"],
                "created_at": datetime.now().isoformat(),
                "active": True
            }
        ]
        
        self.save_strategies(default_strategies)
        return default_strategies
    
    def save_strategies(self, strategies: List[Dict[str, Any]]):
        """Save strategies to file"""
        try:
            with open(self.strategies_file, 'w') as f:
                json.dump(strategies, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving strategies: {e}")
    
    def list_strategies(self) -> List[Dict[str, Any]]:
        """List all available strategies"""
        return [s for s in self.strategies if s.get('active', True)]
    
    def get_strategy(self, strategy_id: str) -> Optional[Dict[str, Any]]:
        """Get strategy by ID"""
        return next((s for s in self.strategies if s['id'] == strategy_id), None)
    
    def get_strategies_by_type(self, strategy_type: str) -> List[Dict[str, Any]]:
        """Get strategies by type"""
        return [s for s in self.strategies if s.get('type', '').lower() == strategy_type.lower()]
    
    def get_strategies_by_market(self, market: str) -> List[Dict[str, Any]]:
        """Get strategies suitable for a market"""
        return [s for s in self.strategies if market.lower() in [m.lower() for m in s.get('markets', [])]]
    
    def create_strategy_wizard(self):
        """Interactive strategy creation wizard"""
        print("\n➕ Create New Strategy")
        print("=" * 25)
        
        try:
            # Get strategy details
            name = input("Strategy name: ").strip()
            if not name:
                print("❌ Strategy name is required")
                return
            
            description = input("Strategy description: ").strip()
            
            print("\nStrategy types:")
            print("1. Trend Following")
            print("2. Mean Reversion")
            print("3. Momentum")
            print("4. Volatility")
            print("5. Breakout")
            print("6. Arbitrage")
            
            type_choice = input("Select strategy type (1-6): ").strip()
            type_map = {
                "1": "trend_following",
                "2": "mean_reversion",
                "3": "momentum",
                "4": "volatility",
                "5": "breakout",
                "6": "arbitrage"
            }
            strategy_type = type_map.get(type_choice, "trend_following")
            
            print("\nRisk levels:")
            print("1. Low")
            print("2. Medium")
            print("3. High")
            
            risk_choice = input("Select risk level (1-3) [2]: ").strip() or "2"
            risk_map = {"1": "Low", "2": "Medium", "3": "High"}
            risk_level = risk_map.get(risk_choice, "Medium")
            
            # Markets
            print("\nSupported markets (comma-separated):")
            print("Available: crypto, stocks")
            markets_input = input("Markets [crypto,stocks]: ").strip() or "crypto,stocks"
            markets = [m.strip() for m in markets_input.split(',')]
            
            # Timeframes
            print("\nSupported timeframes (comma-separated):")
            print("Available: 1h, 4h, 1d")
            timeframes_input = input("Timeframes [1h,4h,1d]: ").strip() or "1h,4h,1d"
            timeframes = [t.strip() for t in timeframes_input.split(',')]
            
            # Create strategy
            strategy_id = name.lower().replace(' ', '_').replace('-', '_')
            
            new_strategy = {
                "id": strategy_id,
                "name": name,
                "description": description,
                "type": strategy_type,
                "risk_level": risk_level,
                "parameters": {
                    "stop_loss": 0.02,
                    "take_profit": 0.04
                },
                "markets": markets,
                "timeframes": timeframes,
                "created_at": datetime.now().isoformat(),
                "active": True,
                "custom": True
            }
            
            # Add to strategies
            self.strategies.append(new_strategy)
            self.save_strategies(self.strategies)
            
            print(f"\n✅ Strategy '{name}' created successfully!")
            print(f"Strategy ID: {strategy_id}")
            
        except Exception as e:
            print(f"❌ Error creating strategy: {e}")
    
    def configure_strategy(self, strategy_name: str):
        """Configure strategy parameters"""
        print(f"\n⚙️  Configure Strategy: {strategy_name}")
        print("=" * 40)
        
        # Find strategy
        strategy = None
        for s in self.strategies:
            if s['name'].lower() == strategy_name.lower() or s['id'].lower() == strategy_name.lower():
                strategy = s
                break
        
        if not strategy:
            print(f"❌ Strategy '{strategy_name}' not found")
            return
        
        print(f"Strategy: {strategy['name']}")
        print(f"Type: {strategy['type'].replace('_', ' ').title()}")
        print(f"Risk Level: {strategy['risk_level']}")
        print()
        
        print("Current parameters:")
        for param, value in strategy['parameters'].items():
            print(f"  {param}: {value}")
        
        print("\n💡 Parameter configuration coming soon!")
        print("   • Interactive parameter editing")
        print("   • Parameter validation")
        print("   • Backtesting with new parameters")
    
    def test_strategy(self, strategy_name: str):
        """Test a strategy"""
        print(f"\n🧪 Test Strategy: {strategy_name}")
        print("=" * 30)
        
        # Find strategy
        strategy = None
        for s in self.strategies:
            if s['name'].lower() == strategy_name.lower() or s['id'].lower() == strategy_name.lower():
                strategy = s
                break
        
        if not strategy:
            print(f"❌ Strategy '{strategy_name}' not found")
            return
        
        print(f"Testing strategy: {strategy['name']}")
        print(f"Type: {strategy['type'].replace('_', ' ').title()}")
        print()
        
        # Quick test setup
        print("Quick test options:")
        print("1. Test on BTC/USDT (crypto)")
        print("2. Test on NSE:SBIN-EQ (stock)")
        print("3. Custom symbol")
        
        choice = input("Select option (1-3) [1]: ").strip() or "1"
        
        if choice == "1":
            symbol = "BTC/USDT"
            asset_type = "crypto"
        elif choice == "2":
            symbol = "NSE:SBIN-EQ"
            asset_type = "stock"
        else:
            symbol = input("Enter symbol: ").strip().upper()
            asset_type = input("Asset type (crypto/stock): ").strip().lower() or "crypto"
        
        print(f"\n🔄 Running quick test...")
        print(f"   Strategy: {strategy['name']}")
        print(f"   Symbol: {symbol}")
        print(f"   Asset Type: {asset_type}")
        
        # Run backtest using the strategy
        try:
            from ..backtesting.backtest_engine import BacktestEngine
            
            backtest_engine = BacktestEngine()
            results = backtest_engine.run_backtest(
                symbol=symbol,
                strategy=strategy['id'],
                timeframe='1h',
                days=30,
                initial_capital=10000.0,
                asset_type=asset_type
            )
            
            if results:
                print("\n✅ Strategy test completed!")
                print("Check the backtest results above.")
            else:
                print("❌ Strategy test failed")
                
        except Exception as e:
            print(f"❌ Error testing strategy: {e}")
    
    def show_strategy_performance(self, strategy_name: str):
        """Show strategy performance metrics"""
        print(f"\n📊 Strategy Performance: {strategy_name}")
        print("=" * 40)
        
        # Find strategy
        strategy = None
        for s in self.strategies:
            if s['name'].lower() == strategy_name.lower() or s['id'].lower() == strategy_name.lower():
                strategy = s
                break
        
        if not strategy:
            print(f"❌ Strategy '{strategy_name}' not found")
            return
        
        print(f"Strategy: {strategy['name']}")
        print(f"Description: {strategy['description']}")
        print(f"Type: {strategy['type'].replace('_', ' ').title()}")
        print(f"Risk Level: {strategy['risk_level']}")
        print()
        
        print("Supported Markets:")
        for market in strategy['markets']:
            print(f"  • {market.title()}")
        
        print("\nSupported Timeframes:")
        for timeframe in strategy['timeframes']:
            print(f"  • {timeframe}")
        
        print("\nParameters:")
        for param, value in strategy['parameters'].items():
            print(f"  • {param.replace('_', ' ').title()}: {value}")
        
        print("\n💡 Historical performance tracking coming soon!")
        print("   • Win rate statistics")
        print("   • Risk-adjusted returns")
        print("   • Drawdown analysis")
        print("   • Performance across different market conditions")
    
    def delete_strategy(self, strategy_id: str) -> bool:
        """Delete a strategy"""
        try:
            original_count = len(self.strategies)
            self.strategies = [s for s in self.strategies if s['id'] != strategy_id]
            
            if len(self.strategies) < original_count:
                self.save_strategies(self.strategies)
                print(f"✅ Strategy '{strategy_id}' deleted")
                return True
            else:
                print(f"⚠️  Strategy '{strategy_id}' not found")
                return False
                
        except Exception as e:
            print(f"❌ Error deleting strategy: {e}")
            return False
    
    def export_strategy(self, strategy_id: str, filename: str = None) -> str:
        """Export strategy to file"""
        try:
            strategy = self.get_strategy(strategy_id)
            if not strategy:
                print(f"❌ Strategy '{strategy_id}' not found")
                return ""
            
            if not filename:
                filename = f"strategy_{strategy_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            filepath = self.strategies_dir / filename
            
            with open(filepath, 'w') as f:
                json.dump(strategy, f, indent=2)
            
            print(f"✅ Strategy exported to: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error exporting strategy: {e}")
            return ""
    
    def import_strategy(self, filepath: str) -> bool:
        """Import strategy from file"""
        try:
            with open(filepath, 'r') as f:
                strategy = json.load(f)
            
            # Validate required fields
            required_fields = ['id', 'name', 'description', 'type']
            for field in required_fields:
                if field not in strategy:
                    print(f"❌ Missing required field '{field}' in strategy file")
                    return False
            
            # Check if strategy already exists
            existing = self.get_strategy(strategy['id'])
            if existing:
                print(f"⚠️  Strategy '{strategy['id']}' already exists")
                overwrite = input("Overwrite existing strategy? (y/n): ").lower()
                if overwrite != 'y':
                    return False
                
                # Remove existing strategy
                self.strategies = [s for s in self.strategies if s['id'] != strategy['id']]
            
            # Add imported strategy
            strategy['imported_at'] = datetime.now().isoformat()
            self.strategies.append(strategy)
            self.save_strategies(self.strategies)
            
            print(f"✅ Strategy '{strategy['name']}' imported successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error importing strategy: {e}")
            return False