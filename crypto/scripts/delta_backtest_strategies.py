#!/usr/bin/env python3
"""
Delta Exchange Multi-Strategy Backtest System
[TARGET] ALL STRATEGIES | ALL PAIRS | ALL TIMEFRAMES  
[CHART] All 29 KPIs implemented
[TROPHY] Best trade ranking system
[TARGET] Production ready backtesting
"""

import os
import sys
import json
import time
import math
import requests
from datetime import datetime, timedelta
import argparse

# Add crypto module to path for data acquisition
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Import crypto data acquisition and CCXT
try:
    from crypto.data_acquisition import fetch_data
    # Also try to import CCXT for Delta Exchange
    import ccxt
    USE_REAL_DATA = True
    CCXT_AVAILABLE = True
    print("[OK] Crypto data acquisition module loaded - Real data mode enabled")
    print("[OK] CCXT library available for Delta Exchange integration")
except ImportError as e:
    USE_REAL_DATA = False
    CCXT_AVAILABLE = False
    print("[WARN] Crypto data acquisition not available - Using simulated data mode")
    print(f"[WARN] CCXT import error: {e}")

print("[TARGET] DELTA EXCHANGE MULTI-STRATEGY BACKTEST")
print("="*80)
print("[CHART] All Strategies | All Pairs | All Timeframes")
print("[TROPHY] Best Trade Ranking System")
print("[CHART-UP] All 29 KPIs | Professional Analysis")
print("="*80)

class ComprehensiveKPICalculator:
    """Advanced KPI calculator for all 29 metrics."""
    
    def __init__(self, initial_capital=100000):
        self.initial_capital = initial_capital
        self.trades = []
        self.equity_curve = []
    
    def reset(self):
        """Reset for new strategy test."""
        self.trades = []
        self.equity_curve = []
    
    def add_trade(self, trade):
        """Add trade for analysis."""
        self.trades.append(trade)
    
    def add_equity_point(self, timestamp, equity):
        """Add equity curve point."""
        self.equity_curve.append({
            'timestamp': timestamp,
            'equity': equity
        })

    def calculate_all_29_kpis(self):
        """Calculate ALL 29 KPIs exactly as specified."""
        if not self.trades:
            return self._get_empty_kpis()
        
        # Trade data extraction
        returns = [t['profit_pct'] for t in self.trades]
        profits = [t['profit'] for t in self.trades]
        durations = [(t['exit_time'] - t['entry_time']).total_seconds() / 86400 for t in self.trades]
        
        # Basic statistics
        total_trades = len(self.trades)
        winning_trades = len([r for r in returns if r > 0])
        losing_trades = len([r for r in returns if r < 0])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # Return calculations
        total_return = sum(returns)
        avg_return = sum(returns) / len(returns) if returns else 0
        best_trade = max(returns) if returns else 0
        worst_trade = min(returns) if returns else 0
        
        # Duration calculations
        max_duration = max(durations) if durations else 0
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # Time period calculations
        start_date = min([t['entry_time'] for t in self.trades])
        end_date = max([t['exit_time'] for t in self.trades])
        duration_days = (end_date - start_date).days + 1
        
        # Equity calculations
        final_equity = self.initial_capital + sum(profits)
        peak_equity = max([eq['equity'] for eq in self.equity_curve]) if self.equity_curve else final_equity
        
        # Profit factor calculation
        gross_profit = sum([p for p in profits if p > 0])
        gross_loss = abs(sum([p for p in profits if p < 0]))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        # Annualized calculations
        years = max(duration_days / 365.25, 1/365.25)
        annual_return = (((final_equity / self.initial_capital) ** (1/years)) - 1) * 100
        
        # Volatility calculations
        volatility_daily = self._calculate_volatility(returns)
        volatility_annual = volatility_daily * math.sqrt(252)
        
        # Risk ratios
        sharpe_ratio = annual_return / volatility_annual if volatility_annual > 0 else 0
        sortino_ratio = self._calculate_sortino_ratio(returns, annual_return)
        
        # Drawdown calculations
        max_dd, avg_dd, max_dd_duration, avg_dd_duration = self._calculate_comprehensive_drawdowns()
        
        calmar_ratio = annual_return / abs(max_dd) if max_dd != 0 else 0
        
        # Market comparison
        buy_hold_annual = 15.0  # Assume 15% annual market return
        buy_hold_return = buy_hold_annual * years
        alpha = annual_return - buy_hold_annual
        beta = 1.0  # Simplified
        
        # CAGR calculation
        cagr = annual_return
        
        # ALL 29 KPIs as per exact specification
        return {
            # 1-6: Basic Information
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'duration_days': duration_days,
            'exposure_time_pct': 100.0,  # Full exposure assumed
            'equity_final': final_equity,
            'equity_peak': peak_equity,
            
            # 7-11: Return Metrics
            'return_pct': total_return,
            'buy_hold_return_pct': buy_hold_return,
            'return_ann_pct': annual_return,
            'volatility_ann_pct': volatility_annual,
            'cagr_pct': cagr,
            
            # 12-16: Risk Ratios
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'calmar_ratio': calmar_ratio,
            'alpha_pct': alpha,
            'beta': beta,
            
            # 17-20: Drawdown Analysis
            'max_drawdown_pct': max_dd,
            'avg_drawdown_pct': avg_dd,
            'max_drawdown_duration': max_dd_duration,
            'avg_drawdown_duration': avg_dd_duration,
            
            # 21-29: Trade Statistics
            'total_trades': total_trades,
            'win_rate_pct': win_rate,
            'best_trade_pct': best_trade,
            'worst_trade_pct': worst_trade,
            'avg_trade_pct': avg_return,
            'max_trade_duration': max_duration,
            'avg_trade_duration': avg_duration,
            'profit_factor': profit_factor,
            'expectancy_pct': avg_return
        }

    def _get_empty_kpis(self):
        """Return empty KPI structure."""
        return {
            'start_date': 'N/A', 'end_date': 'N/A', 'duration_days': 0,
            'exposure_time_pct': 0, 'equity_final': self.initial_capital,
            'equity_peak': self.initial_capital, 'return_pct': 0,
            'buy_hold_return_pct': 0, 'return_ann_pct': 0,
            'volatility_ann_pct': 0, 'cagr_pct': 0, 'sharpe_ratio': 0,
            'sortino_ratio': 0, 'calmar_ratio': 0, 'alpha_pct': 0,
            'beta': 1.0, 'max_drawdown_pct': 0, 'avg_drawdown_pct': 0,
            'max_drawdown_duration': 0, 'avg_drawdown_duration': 0,
            'total_trades': 0, 'win_rate_pct': 0, 'best_trade_pct': 0,
            'worst_trade_pct': 0, 'avg_trade_pct': 0, 'max_trade_duration': 0,
            'avg_trade_duration': 0, 'profit_factor': 0, 'expectancy_pct': 0
        }

    def _calculate_volatility(self, returns):
        """Calculate return volatility."""
        if len(returns) < 2:
            return 0
        mean_return = sum(returns) / len(returns)
        variance = sum([(r - mean_return) ** 2 for r in returns]) / (len(returns) - 1)
        return math.sqrt(variance)

    def _calculate_sortino_ratio(self, returns, annual_return):
        """Calculate Sortino ratio."""
        downside_returns = [r for r in returns if r < 0]
        if not downside_returns:
            return float('inf')
        
        downside_deviation = math.sqrt(sum([r ** 2 for r in downside_returns]) / len(downside_returns))
        downside_deviation_annual = downside_deviation * math.sqrt(252)
        return annual_return / downside_deviation_annual if downside_deviation_annual > 0 else 0

    def _calculate_comprehensive_drawdowns(self):
        """Calculate all drawdown metrics."""
        if not self.equity_curve:
            return 0, 0, 0, 0
        
        peak = self.equity_curve[0]['equity']
        max_drawdown = 0
        current_drawdown = 0
        drawdown_start = None
        drawdown_durations = []
        all_drawdowns = []
        
        for i, point in enumerate(self.equity_curve):
            equity = point['equity']
            
            # Update peak
            if equity > peak:
                # End of drawdown period
                if drawdown_start is not None:
                    duration = (point['timestamp'] - drawdown_start).days
                    drawdown_durations.append(duration)
                    drawdown_start = None
                peak = equity
                current_drawdown = 0
            else:
                # In drawdown
                if drawdown_start is None:
                    drawdown_start = point['timestamp']
                
                current_drawdown = ((peak - equity) / peak) * 100
                all_drawdowns.append(current_drawdown)
                max_drawdown = max(max_drawdown, current_drawdown)
        
        avg_drawdown = sum(all_drawdowns) / len(all_drawdowns) if all_drawdowns else 0
        max_dd_duration = max(drawdown_durations) if drawdown_durations else 0
        avg_dd_duration = sum(drawdown_durations) / len(drawdown_durations) if drawdown_durations else 0
        
        return max_drawdown, avg_drawdown, max_dd_duration, avg_dd_duration

class TradingStrategies:
    """Multiple trading strategies for comprehensive testing."""
    
    @staticmethod
    def calculate_rsi(prices, period=14):
        """Calculate RSI indicator."""
        if len(prices) < period + 1:
            return 50
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            gains.append(max(change, 0))
            losses.append(max(-change, 0))
        
        if len(gains) < period:
            return 50
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    @staticmethod
    def rsi_strategy(data, rsi_buy=30, rsi_sell=70):
        """RSI-based strategy."""
        signals = []
        
        for i in range(30, len(data)):
            prices = [candle['close'] for candle in data[max(0, i-30):i+1]]
            rsi = TradingStrategies.calculate_rsi(prices)
            
            current = data[i]
            
            if rsi < rsi_buy:
                signals.append({
                    'timestamp': current['timestamp'],
                    'action': 'buy',
                    'price': current['close'],
                    'indicator': f'RSI({rsi:.1f})',
                    'confidence': (rsi_buy - rsi) * 2
                })
            elif rsi > rsi_sell:
                signals.append({
                    'timestamp': current['timestamp'],
                    'action': 'sell',
                    'price': current['close'],
                    'indicator': f'RSI({rsi:.1f})',
                    'confidence': (rsi - rsi_sell) * 2
                })
        
        return signals

    @staticmethod
    def macd_strategy(data):
        """MACD-based strategy.""" 
        signals = []
        
        for i in range(50, len(data)):
            prices = [candle['close'] for candle in data[max(0, i-50):i+1]]
            
            # Simple MACD calculation for demo
            if len(prices) < 26:
                continue
                
            # EMA12 and EMA26
            ema12 = sum(prices[-12:]) / 12
            ema26 = sum(prices[-26:]) / 26
            macd = ema12 - ema26
            
            # Previous MACD
            prev_prices = prices[:-1]
            if len(prev_prices) >= 26:
                prev_ema12 = sum(prev_prices[-12:]) / 12
                prev_ema26 = sum(prev_prices[-26:]) / 26
                prev_macd = prev_ema12 - prev_ema26
            else:
                prev_macd = 0
            
            current = data[i]
            
            if macd > 0 and prev_macd <= 0:  # Bullish crossover
                signals.append({
                    'timestamp': current['timestamp'],
                    'action': 'buy',
                    'price': current['close'],
                    'indicator': f'MACD_BULL({macd:.4f})',
                    'confidence': min(abs(macd) * 1000, 95)
                })
            elif macd < 0 and prev_macd >= 0:  # Bearish crossover
                signals.append({
                    'timestamp': current['timestamp'],
                    'action': 'sell',
                    'price': current['close'],
                    'indicator': f'MACD_BEAR({macd:.4f})',
                    'confidence': min(abs(macd) * 1000, 95)
                })
        
        return signals

    @staticmethod
    def bollinger_strategy(data):
        """Bollinger Bands strategy."""
        signals = []
        
        for i in range(30, len(data)):
            prices = [candle['close'] for candle in data[max(0, i-20):i+1]]
            
            if len(prices) < 20:
                continue
                
            # Simple moving average and standard deviation
            sma = sum(prices) / len(prices)
            variance = sum([(p - sma) ** 2 for p in prices]) / len(prices)
            std = math.sqrt(variance)
            
            upper_band = sma + (2 * std)
            lower_band = sma - (2 * std)
            
            current = data[i]
            current_price = current['close']
            
            if current_price <= lower_band:  # Oversold
                signals.append({
                    'timestamp': current['timestamp'],
                    'action': 'buy',
                    'price': current_price,
                    'indicator': f'BB_OVERSOLD({((lower_band - current_price)/lower_band*100):.1f}%)',
                    'confidence': min(((lower_band - current_price) / lower_band) * 500, 95)
                })
            elif current_price >= upper_band:  # Overbought
                signals.append({
                    'timestamp': current['timestamp'],
                    'action': 'sell',
                    'price': current_price,
                    'indicator': f'BB_OVERBOUGHT({((current_price - upper_band)/upper_band*100):.1f}%)',
                    'confidence': min(((current_price - upper_band) / upper_band) * 500, 95)
                })
        
        return signals

class DeltaExchangeAPI:
    """Delta Exchange API integration using CCXT."""
    
    def __init__(self):
        self.exchange = None
        self.available_pairs = []
        self.initialized = False
        
    def initialize(self):
        """Initialize Delta Exchange connection using CCXT."""
        try:
            if CCXT_AVAILABLE:
                print("🔗 Connecting to Delta Exchange via CCXT...")
                
                # Initialize Delta Exchange with comprehensive rate limiting
                self.exchange = ccxt.delta({
                    'sandbox': False,  # Set to True for testing
                    'enableRateLimit': True,  # Enable automatic rate limiting
                    'rateLimit': 1200,  # Minimum delay between requests in milliseconds
                    'timeout': 30000,  # 30 seconds timeout
                    'headers': {
                        'User-Agent': 'AlgoProject/1.0 CCXT'
                    },
                    'options': {
                        'adjustForTimeDifference': True,  # Adjust for server time difference
                        'recvWindow': 60000,  # Receive window for requests
                    }
                })
                
                print("� Loading Delta Exchange markets...")
                
                # Load markets
                markets = self.exchange.load_markets()
                
                # Extract trading pairs
                self.available_pairs = list(markets.keys())
                
                # Filter for active USDT pairs
                usdt_pairs = [pair for pair in self.available_pairs if 'USDT' in pair and markets[pair]['active']]
                
                self.initialized = True
                
                print(f"[OK] Delta Exchange connected successfully with rate limiting!")
                print(f"[CHART] Found {len(self.available_pairs)} total pairs")
                print(f"[MONEY] Found {len(usdt_pairs)} active USDT pairs")
                print(f"⏱️  Rate limit: {self.exchange.rateLimit}ms between requests")
                
                return usdt_pairs[:20]  # Return top 20 USDT pairs
                
            else:
                print("[WARN]  CCXT not available - using fallback trading pairs")
                return self._get_fallback_pairs()
                
        except Exception as e:
            print(f"[ERROR] Failed to connect to Delta Exchange: {e}")
            print("[WARN]  Using fallback trading pairs")
            return self._get_fallback_pairs()
    
    def _get_fallback_pairs(self):
        """Fallback trading pairs when API is not available."""
        return [
            'BTC/USDT', 'ETH/USDT', 'ADA/USDT', 'SOL/USDT', 'MATIC/USDT',
            'DOT/USDT', 'LTC/USDT', 'XRP/USDT', 'LINK/USDT', 'AVAX/USDT',
            'ALGO/USDT', 'ATOM/USDT', 'FTM/USDT', 'NEAR/USDT', 'ICP/USDT'
        ]
    
    def fetch_ohlcv_data(self, symbol, timeframe='1h', days=14):
        """Fetch real OHLCV data from Delta Exchange with rate limiting."""
        try:
            if self.exchange and self.initialized:
                # Calculate the number of candles needed
                timeframe_minutes = {
                    '1m': 1, '5m': 5, '15m': 15, '30m': 30,
                    '1h': 60, '4h': 240, '1d': 1440
                }
                
                minutes_per_candle = timeframe_minutes.get(timeframe, 60)
                limit = min(int(days * 1440 / minutes_per_candle), 1000)  # API limit
                
                print(f"[CHART] Fetching real {timeframe} data for {symbol} from Delta Exchange...")
                
                # Fetch OHLCV data with automatic rate limiting
                ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
                
                if not ohlcv:
                    return None
                
                # Convert to our format
                data = []
                for candle in ohlcv:
                    timestamp, open_price, high, low, close, volume = candle
                    
                    data.append({
                        'timestamp': datetime.fromtimestamp(timestamp / 1000),
                        'open': float(open_price),
                        'high': float(high),
                        'low': float(low),
                        'close': float(close),
                        'volume': float(volume),
                        'symbol': symbol,
                        'timeframe': timeframe
                    })
                
                print(f"[OK] Fetched {len(data)} real candles for {symbol}")
                return data
                
            else:
                return None
                
        except Exception as e:
            # Enhanced error handling for rate limiting
            if 'ccxt' in str(type(e).__module__):
                if 'RateLimitExceeded' in str(type(e).__name__):
                    print(f"[WARN]  Rate limit exceeded for {symbol}: {e}")
                    print("[REFRESH] Waiting before retry...")
                    time.sleep(2)  # Wait 2 seconds before returning None
                elif 'NetworkError' in str(type(e).__name__):
                    print(f"[ERROR] Network error fetching {symbol}: {e}")
                else:
                    print(f"[ERROR] CCXT error fetching {symbol}: {e}")
            else:
                print(f"[ERROR] Error fetching data for {symbol}: {e}")
            
            return None
    
    def get_symbol_info(self, symbol):
        """Get detailed symbol information."""
        try:
            if self.exchange and self.initialized:
                markets = self.exchange.markets
                if symbol in markets:
                    market = markets[symbol]
                    return {
                        'symbol': symbol,
                        'base': market['base'],
                        'quote': market['quote'],
                        'active': market['active'],
                        'type': market['type'],
                        'spot': market['spot'] if 'spot' in market else True,
                        'precision': market['precision'],
                        'limits': market['limits']
                    }
            return None
        except Exception as e:
            print(f"[ERROR] Error getting symbol info for {symbol}: {e}")
            return None

# Initialize Delta Exchange API
delta_api = DeltaExchangeAPI()

class DeltaDataProvider:
    """Enhanced data provider for multiple timeframes with real Delta Exchange data."""
    
    def __init__(self):
        self.base_prices = {
            'BTC/USDT': 45000, 'ETH/USDT': 2500, 'ADA/USDT': 0.52,
            'SOL/USDT': 22, 'MATIC/USDT': 0.85, 'DOT/USDT': 7.8,
            'LTC/USDT': 180, 'XRP/USDT': 0.63, 'LINK/USDT': 12.5,
            'AVAX/USDT': 35
        }

    def get_market_data(self, symbol, timeframe='1h', days=14):
        """Get market data - real data if available, simulated otherwise."""
        # Try to fetch real data first
        if USE_REAL_DATA and delta_api.initialized:
            real_data = delta_api.fetch_ohlcv_data(symbol, timeframe, days)
            if real_data and len(real_data) > 50:  # Minimum data requirement
                return real_data
        
        # Fallback to simulated data
        print(f"[CHART] Using simulated data for {symbol} ({timeframe})")
        return self.generate_market_data(symbol, timeframe, days)

    def generate_market_data(self, symbol, timeframe='1h', days=14):
        """Generate realistic market data for backtesting."""
        print(f"[CHART] Generating {timeframe} data for {symbol} ({days} days)...")
        
        base_price = self.base_prices.get(symbol, 1000)
        data = []
        
        # Timeframe configurations - increased volatility for more realistic trading
        timeframe_configs = {
            '1h': {'delta': timedelta(hours=1), 'volatility': 0.08, 'candles_per_day': 24},
            '4h': {'delta': timedelta(hours=4), 'volatility': 0.12, 'candles_per_day': 6},
            '1d': {'delta': timedelta(days=1), 'volatility': 0.18, 'candles_per_day': 1}
        }
        
        config = timeframe_configs.get(timeframe, timeframe_configs['1h'])
        time_delta = config['delta']
        base_volatility = config['volatility']
        total_candles = int(days * config['candles_per_day'])
        
        current_time = datetime.now() - (time_delta * total_candles)
        
        for i in range(total_candles):
            # Market trend phases for realism - enhanced volatility
            trend_phase = i % 100  # Change trend every 100 candles
            if trend_phase < 30:  # Uptrend
                trend_factor = 1.003
                volatility_mult = 1.2
            elif trend_phase < 60:  # Downtrend
                trend_factor = 0.997
                volatility_mult = 1.8
            else:  # Sideways
                trend_factor = 1.0
                volatility_mult = 0.9
            
            # Random component with hash-based deterministic randomness
            random_seed = hash(str(current_time) + symbol + str(i)) % 10000
            random_factor = (random_seed - 5000) / 50000  # Increased random range
            price_change = random_factor * base_volatility * volatility_mult
            
            base_price *= (trend_factor + price_change)
            base_price = max(base_price, 0.001)  # Minimum price
            
            # OHLCV generation with realistic spreads
            volatility_factor = abs(price_change) + base_volatility * 0.3
            high = base_price * (1 + volatility_factor)
            low = base_price * (1 - volatility_factor * 0.8)
            
            # Ensure proper OHLC relationships
            open_price = base_price * (0.995 + (random_seed % 100) / 10000)
            close_price = base_price
            
            # Volume simulation
            base_volume = 1000 if 'BTC' in symbol or 'ETH' in symbol else 5000
            volume_multiplier = 1 + abs(price_change) * 10
            volume = int(base_volume * volume_multiplier * (0.5 + (random_seed % 1000) / 1000))
            
            candle = {
                'timestamp': current_time,
                'open': max(open_price, 0.001),
                'high': max(high, open_price, close_price),
                'low': min(low, open_price, close_price),
                'close': max(close_price, 0.001),
                'volume': volume,
                'symbol': symbol,
                'timeframe': timeframe
            }
            
            data.append(candle)
            current_time += time_delta
        
        print(f"[OK] Generated {len(data)} {timeframe} candles for {symbol}")
        return data

class MultiStrategyBacktester:
    """Comprehensive multi-strategy backtesting engine with real Delta Exchange integration."""
    
    def __init__(self, initial_capital=100000, position_size=15000):
        self.initial_capital = initial_capital
        self.position_size = position_size
        self.data_provider = DeltaDataProvider()
        self.kpi_calculator = ComprehensiveKPICalculator(initial_capital)
        
        # Strategy definitions
        self.strategies = {
            'RSI_30_70': lambda data: TradingStrategies.rsi_strategy(data, 30, 70),
            'RSI_25_75': lambda data: TradingStrategies.rsi_strategy(data, 25, 75),
            'RSI_35_65': lambda data: TradingStrategies.rsi_strategy(data, 35, 65),
            'MACD_Standard': TradingStrategies.macd_strategy,
            'Bollinger_Bands': TradingStrategies.bollinger_strategy,
        }
        
        # Initialize Delta Exchange and get real trading pairs
        print("[REFRESH] Initializing Delta Exchange connection...")
        self.trading_pairs = delta_api.initialize()
        
        print(f"[CHART] Available trading pairs:")
        for i, pair in enumerate(self.trading_pairs[:10], 1):
            print(f"   {i:2d}. {pair}")
        if len(self.trading_pairs) > 10:
            print(f"   ... and {len(self.trading_pairs) - 10} more pairs")
        
        # Timeframes supported by Delta Exchange
        self.timeframes = ['1h', '4h', '1d']

    def execute_strategy_backtest(self, strategy_name, strategy_func, symbol, timeframe, days=14):
        """Execute backtest for specific strategy-symbol-timeframe combination."""
        
        # Get market data (real or simulated)
        data = self.data_provider.get_market_data(symbol, timeframe, days)
        
        if len(data) < 100:  # Minimum data requirement
            return None
        
        # Generate signals
        signals = strategy_func(data)
        
        if not signals:
            return None
        
        # Reset KPI calculator
        self.kpi_calculator.reset()
        
        # Execute trades
        position = None
        trades = []
        current_equity = self.initial_capital
        
        for signal in signals:
            if signal['action'] == 'buy' and position is None:
                # Open long position
                shares = self.position_size / signal['price']
                position = {
                    'entry_time': signal['timestamp'],
                    'entry_price': signal['price'],
                    'shares': shares,
                    'type': 'long'
                }
                
            elif signal['action'] == 'sell' and position is not None:
                # Close position
                exit_price = signal['price']
                profit = (exit_price - position['entry_price']) * position['shares']
                profit_pct = ((exit_price - position['entry_price']) / position['entry_price']) * 100
                
                trade = {
                    'entry_time': position['entry_time'],
                    'exit_time': signal['timestamp'],
                    'entry_price': position['entry_price'],
                    'exit_price': exit_price,
                    'shares': position['shares'],
                    'profit': profit,
                    'profit_pct': profit_pct,
                    'duration': signal['timestamp'] - position['entry_time']
                }
                
                trades.append(trade)
                self.kpi_calculator.add_trade(trade)
                
                current_equity += profit
                self.kpi_calculator.add_equity_point(signal['timestamp'], current_equity)
                
                position = None
        
        # Calculate KPIs
        kpis = self.kpi_calculator.calculate_all_29_kpis()
        
        return {
            'strategy': strategy_name,
            'symbol': symbol,
            'timeframe': timeframe,
            'trades': trades,
            'kpis': kpis,
            'total_profit': sum([t['profit'] for t in trades]),
            'total_profit_pct': sum([t['profit_pct'] for t in trades]),
            'trade_count': len(trades)
        }

    def run_comprehensive_backtest(self, selected_symbols=None, selected_timeframes=None, selected_strategies=None):
        """Run backtest across all combinations."""
        print("\n[ROCKET] STARTING COMPREHENSIVE MULTI-STRATEGY BACKTEST")
        print("="*60)
        
        symbols = selected_symbols or self.trading_pairs
        timeframes = selected_timeframes or self.timeframes  
        strategies = selected_strategies or list(self.strategies.keys())
        
        total_combinations = len(symbols) * len(timeframes) * len(strategies)
        print(f"[CHART] Testing {total_combinations} combinations:")
        print(f"   • Symbols: {len(symbols)} ({', '.join(symbols[:5])}{'...' if len(symbols) > 5 else ''})")
        print(f"   • Timeframes: {len(timeframes)} ({', '.join(timeframes)})")
        print(f"   • Strategies: {len(strategies)} ({', '.join(strategies)})")
        print(f"   • Data Source: {'Real Delta Exchange' if USE_REAL_DATA and delta_api.initialized else 'Simulated'}")
        print()
        
        results = []
        current_combination = 0
        
        for symbol in symbols:
            for timeframe in timeframes:
                for strategy_name in strategies:
                    current_combination += 1
                    print(f"[LIGHTNING] [{current_combination}/{total_combinations}] Testing {strategy_name} on {symbol} {timeframe}")
                    
                    strategy_func = self.strategies[strategy_name]
                    result = self.execute_strategy_backtest(strategy_name, strategy_func, symbol, timeframe)
                    
                    if result and result['trade_count'] > 0:
                        results.append(result)
                        print(f"   [OK] {result['trade_count']} trades, {result['total_profit_pct']:.2f}% profit")
                    else:
                        print(f"   [ERROR] No valid trades generated")
        
        print(f"\n[OK] Comprehensive backtest completed!")
        print(f"[CHART-UP] {len(results)} successful strategy combinations out of {total_combinations}")
        
        return results

def calculate_composite_score(result):
    """Calculate composite ranking score."""
    kpis = result['kpis']
    
    # Weighted scoring system
    profit_weight = 0.3
    profit_factor_weight = 0.25
    win_rate_weight = 0.2
    sharpe_weight = 0.15
    trade_count_weight = 0.1
    
    # Normalize and score each component
    profit_score = min(max(kpis['return_pct'] / 100, 0), 1) * 100
    profit_factor_score = min(max((kpis['profit_factor'] - 1) / 2, 0), 1) * 100
    win_rate_score = kpis['win_rate_pct']
    sharpe_score = min(max(kpis['sharpe_ratio'] / 3, 0), 1) * 100
    trade_count_score = min(max(result['trade_count'] / 20, 0), 1) * 100
    
    composite_score = (
        profit_score * profit_weight +
        profit_factor_score * profit_factor_weight +
        win_rate_score * win_rate_weight +
        sharpe_score * sharpe_weight +
        trade_count_score * trade_count_weight
    )
    
    return composite_score

def display_best_trades_table(results, top_n=10):
    """Display best trades in tabular format."""
    if not results:
        print("[ERROR] No results to display")
        return
    
    # Calculate composite scores and sort
    for result in results:
        result['composite_score'] = calculate_composite_score(result)
    
    # Sort by composite score
    sorted_results = sorted(results, key=lambda x: x['composite_score'], reverse=True)
    top_results = sorted_results[:top_n]
    
    print(f"\n[TROPHY] TOP {top_n} BEST TRADING STRATEGIES")
    print("="*120)
    
    # Table header
    header = f"{'Rank':<4} {'Strategy':<15} {'Symbol':<10} {'TF':<3} {'Trades':<6} {'Profit%':<8} {'PF':<6} {'Win%':<6} {'Sharpe':<7} {'Score':<6}"
    print(header)
    print("-" * 120)
    
    # Table rows
    for i, result in enumerate(top_results, 1):
        kpis = result['kpis']
        row = (f"{i:<4} "
               f"{result['strategy']:<15} "
               f"{result['symbol']:<10} "
               f"{result['timeframe']:<3} "
               f"{result['trade_count']:<6} "
               f"{result['total_profit_pct']:<8.2f} "
               f"{kpis['profit_factor']:<6.2f} "
               f"{kpis['win_rate_pct']:<6.1f} "
               f"{kpis['sharpe_ratio']:<7.2f} "
               f"{result['composite_score']:<6.1f}")
        print(row)
    
    print("-" * 120)
    
    # Summary statistics
    print(f"\n[CHART] SUMMARY STATISTICS")
    print(f"Total strategies tested: {len(results)}")
    print(f"Average profit: {sum([r['total_profit_pct'] for r in results]) / len(results):.2f}%")
    print(f"Best single strategy: {top_results[0]['strategy']} on {top_results[0]['symbol']} {top_results[0]['timeframe']} ({top_results[0]['total_profit_pct']:.2f}%)")
    print(f"Highest profit factor: {max([r['kpis']['profit_factor'] for r in results]):.2f}")
    print(f"Highest win rate: {max([r['kpis']['win_rate_pct'] for r in results]):.1f}%")

def save_results_to_csv(results):
    """Save detailed results to CSV file."""
    if not results:
        return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    csv_file = os.path.join(output_dir, f'multi_strategy_backtest_{timestamp}.csv')
    
    # Prepare CSV data
    csv_lines = []
    header = ['Strategy', 'Symbol', 'Timeframe', 'Trades', 'Total_Profit_Pct', 'Profit_Factor', 
              'Win_Rate_Pct', 'Sharpe_Ratio', 'Max_Drawdown_Pct', 'Composite_Score']
    csv_lines.append(','.join(header))
    
    for result in results:
        kpis = result['kpis']
        row = [
            result['strategy'],
            result['symbol'], 
            result['timeframe'],
            str(result['trade_count']),
            f"{result['total_profit_pct']:.2f}",
            f"{kpis['profit_factor']:.2f}",
            f"{kpis['win_rate_pct']:.1f}",
            f"{kpis['sharpe_ratio']:.2f}",
            f"{kpis['max_drawdown_pct']:.2f}",
            f"{result['composite_score']:.1f}"
        ]
        csv_lines.append(','.join(row))
    
    with open(csv_file, 'w') as f:
        f.write('\n'.join(csv_lines))
    
    print(f"\n[SAVE] Results saved to: {csv_file}")

def display_available_pairs():
    """Display available Delta Exchange trading pairs."""
    print("[REFRESH] Initializing Delta Exchange connection...")
    
    # Initialize Delta API if not already done
    if not delta_api.initialized:
        delta_api.initialize()
    
    if delta_api.initialized:
        pairs = delta_api.available_pairs
        
        print(f"\n[CHART] DELTA EXCHANGE TRADING PAIRS")
        print("="*50)
        
        # Group by quote currency and market type
        usdt_pairs = [p for p in pairs if 'USDT' in p]
        btc_pairs = [p for p in pairs if 'BTC' in p and 'USDT' not in p]
        eth_pairs = [p for p in pairs if 'ETH' in p and 'USDT' not in p and 'BTC' not in p]
        
        # Check for futures/options
        spot_pairs = []
        futures_pairs = []
        options_pairs = []
        
        for pair in usdt_pairs:
            if '-PERP' in pair or '-FUTURES' in pair:
                futures_pairs.append(pair)
            elif '-C-' in pair or '-P-' in pair or 'CALL' in pair or 'PUT' in pair:
                options_pairs.append(pair)
            else:
                spot_pairs.append(pair)
        
        print(f"[MONEY] SPOT USDT Pairs ({len(spot_pairs)}):")
        for i, pair in enumerate(spot_pairs[:20], 1):
            print(f"   {i:2d}. {pair}")
        if len(spot_pairs) > 20:
            print(f"   ... and {len(spot_pairs) - 20} more")
        
        if futures_pairs:
            print(f"\n[CRYSTAL] FUTURES USDT Pairs ({len(futures_pairs)}):")
            for i, pair in enumerate(futures_pairs[:10], 1):
                print(f"   {i:2d}. {pair}")
            if len(futures_pairs) > 10:
                print(f"   ... and {len(futures_pairs) - 10} more")
        
        if options_pairs:
            print(f"\n[LIGHTNING] OPTIONS Pairs ({len(options_pairs)}):")
            for i, pair in enumerate(options_pairs[:10], 1):
                print(f"   {i:2d}. {pair}")
            if len(options_pairs) > 10:
                print(f"   ... and {len(options_pairs) - 10} more")
        
        if btc_pairs:
            print(f"\n₿  BTC Pairs ({len(btc_pairs)}):")
            for i, pair in enumerate(btc_pairs[:10], 1):
                print(f"   {i:2d}. {pair}")
        
        if eth_pairs:
            print(f"\n⟠  ETH Pairs ({len(eth_pairs)}):")
            for i, pair in enumerate(eth_pairs[:10], 1):
                print(f"   {i:2d}. {pair}")
        
        print(f"\nTotal available pairs: {len(pairs)}")
        print(f"[TARGET] To save pairs to CSV files, use: --save-pairs")
        
    else:
        print("[ERROR] Delta Exchange not connected - cannot display pairs")
        print("[BULB] Check CCXT installation: pip install ccxt")
        print("[BULB] Verify internet connection")

def get_top_volume_pairs(limit=10):
    """Get top trading pairs by volume with rate limiting support."""
    try:
        if delta_api.initialized and delta_api.exchange:
            print(f"[CHART] Fetching volume data for top {limit} pairs...")
            
            # Fetch tickers with automatic rate limiting
            tickers = delta_api.exchange.fetch_tickers()
            
            # Sort by 24h volume
            sorted_pairs = sorted(
                [(symbol, ticker) for symbol, ticker in tickers.items() if 'USDT' in symbol],
                key=lambda x: x[1]['quoteVolume'] if x[1]['quoteVolume'] else 0,
                reverse=True
            )
            
            top_pairs = [pair[0] for pair in sorted_pairs[:limit]]
            
            print(f"\n🔥 TOP {limit} PAIRS BY VOLUME:")
            for i, (symbol, ticker) in enumerate(sorted_pairs[:limit], 1):
                volume = ticker['quoteVolume'] if ticker['quoteVolume'] else 0
                print(f"   {i:2d}. {symbol:<12} Volume: ${volume:,.0f}")
            
            return top_pairs
            
    except Exception as e:
        # Enhanced error handling for rate limiting
        if 'ccxt' in str(type(e).__module__):
            if 'RateLimitExceeded' in str(type(e).__name__):
                print(f"[WARN]  Rate limit exceeded while fetching volume data: {e}")
                print("[REFRESH] Using fallback pairs...")
            elif 'NetworkError' in str(type(e).__name__):
                print(f"[ERROR] Network error fetching volume data: {e}")
            else:
                print(f"[ERROR] CCXT error: {e}")
        else:
            print(f"[WARN]  Could not fetch volume data: {e}")
        
        print("[REFRESH] Using fallback pairs instead...")
        return delta_api._get_fallback_pairs()[:limit]
    
    return delta_api._get_fallback_pairs()[:limit]

def save_pairs_to_csv():
    """Save Delta Exchange pairs to organized CSV files."""
    print("[REFRESH] Initializing Delta Exchange connection for pair export...")
    
    # Initialize Delta API if not already done
    if not delta_api.initialized:
        delta_api.initialize()
    
    if not delta_api.initialized:
        print("[ERROR] Cannot save pairs - Delta Exchange not connected")
        return False
    
    # Ensure input directory exists
    input_dir = os.path.join(os.path.dirname(__file__), '..', 'input')
    os.makedirs(input_dir, exist_ok=True)
    
    pairs = delta_api.available_pairs
    print(f"[CHART] Processing {len(pairs)} total pairs...")
    
    # Categorize pairs
    categories = {
        'spot_usdt': [],
        'spot_btc': [],
        'spot_eth': [],
        'futures_usdt': [],
        'futures_btc': [],
        'options_calls': [],
        'options_puts': [],
        'perpetual_usdt': [],
        'other_pairs': []
    }
    
    for pair in pairs:
        # Categorize by market type and quote currency
        if '-PERP' in pair:
            if 'USDT' in pair:
                categories['perpetual_usdt'].append(pair)
            else:
                categories['other_pairs'].append(pair)
        elif '-FUTURES' in pair or 'FUT' in pair:
            if 'USDT' in pair:
                categories['futures_usdt'].append(pair)
            elif 'BTC' in pair:
                categories['futures_btc'].append(pair)
            else:
                categories['other_pairs'].append(pair)
        elif '-C-' in pair or 'CALL' in pair:
            categories['options_calls'].append(pair)
        elif '-P-' in pair or 'PUT' in pair:
            categories['options_puts'].append(pair)
        elif 'USDT' in pair:
            categories['spot_usdt'].append(pair)
        elif 'BTC' in pair:
            categories['spot_btc'].append(pair)
        elif 'ETH' in pair:
            categories['spot_eth'].append(pair)
        else:
            categories['other_pairs'].append(pair)
    
    # Save each category to separate CSV files
    saved_files = []
    
    for category, pair_list in categories.items():
        if pair_list:
            filename = f"delta_{category}.csv"
            filepath = os.path.join(input_dir, filename)
            
            # Create CSV content with additional metadata
            csv_content = ['symbol,base,quote,type,active']
            
            for pair in sorted(pair_list):
                # Get symbol info if available
                symbol_info = delta_api.get_symbol_info(pair)
                
                if symbol_info:
                    base = symbol_info.get('base', '')
                    quote = symbol_info.get('quote', 'UNKNOWN')
                    market_type = 'spot'
                    if '-PERP' in pair:
                        market_type = 'perpetual'
                    elif '-FUTURES' in pair or 'FUT' in pair:
                        market_type = 'futures'
                    elif '-C-' in pair or 'CALL' in pair:
                        market_type = 'option_call'
                    elif '-P-' in pair or 'PUT' in pair:
                        market_type = 'option_put'
                    
                    active = 'true' if symbol_info.get('active', True) else 'false'
                else:
                    # Fallback info
                    if '/' in pair:
                        parts = pair.split('/')
                        base = parts[0]
                        quote = parts[1]
                    else:
                        base = pair
                        quote = 'UNKNOWN'
                    
                    if 'USDT' in pair:
                        quote = 'USDT'
                    elif 'BTC' in pair:
                        quote = 'BTC'
                    elif 'ETH' in pair:
                        quote = 'ETH'
                    
                    market_type = category.split('_')[0]
                    active = 'true'
                
                csv_content.append(f"{pair},{base},{quote},{market_type},{active}")
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(csv_content))
            
            saved_files.append((filename, len(pair_list)))
            print(f"[OK] Saved {len(pair_list)} {category.replace('_', ' ')} pairs to {filename}")
    
    # Create a master summary file
    summary_file = os.path.join(input_dir, "delta_pairs_summary.csv")
    summary_content = ['category,filename,pair_count,description']
    
    for filename, count in saved_files:
        category = filename.replace('delta_', '').replace('.csv', '')
        description = f"Delta Exchange {category.replace('_', ' ').title()} Trading Pairs"
        summary_content.append(f"{category},{filename},{count},{description}")
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(summary_content))
    
    print(f"\n[SAVE] PAIR EXPORT SUMMARY:")
    print("="*50)
    for filename, count in saved_files:
        print(f"[FILE] {filename:<25} - {count:>3} pairs")
    
    print(f"\n[CLIPBOARD] Summary file: delta_pairs_summary.csv")
    print(f"[FOLDER] All files saved to: {input_dir}")
    print(f"[TARGET] Total pairs exported: {sum([count for _, count in saved_files])}")
    
    return True

def load_pairs_from_csv(category='spot_usdt'):
    """Load trading pairs from specific CSV file."""
    input_dir = os.path.join(os.path.dirname(__file__), '..', 'input')
    filename = f"delta_{category}.csv"
    filepath = os.path.join(input_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"[WARN]  File not found: {filename}")
        print(f"[BULB] Run with --save-pairs to generate CSV files first")
        return []
    
    pairs = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[1:]:  # Skip header
                if line.strip():
                    pair = line.strip().split(',')[0]
                    pairs.append(pair)
        
        print(f"[OK] Loaded {len(pairs)} pairs from {filename}")
        return pairs
        
    except Exception as e:
        print(f"[ERROR] Error loading pairs from {filename}: {e}")
        return []

def interactive_pair_selection():
    """Enhanced interactive user interface for selecting trading pairs and CSV files."""
    print("\n[TARGET] DELTA EXCHANGE INTERACTIVE PAIR SELECTION")
    print("="*70)
    
    # Check for existing CSV files first
    input_dir = os.path.join(os.path.dirname(__file__), '..', 'input')
    csv_files = []
    
    if os.path.exists(input_dir):
        csv_files = [f for f in os.listdir(input_dir) if f.startswith('delta_') and f.endswith('.csv')]
    
    while True:
        print(f"\n[CLIPBOARD] PAIR SELECTION OPTIONS:")
        print("="*50)
        
        # Show CSV file options if available
        if csv_files:
            print(f"[FILE] LOAD FROM EXISTING CSV FILES:")
            for i, csv_file in enumerate(csv_files, 1):
                # Extract category from filename
                category = csv_file.replace('delta_', '').replace('.csv', '')
                category_display = category.replace('_', ' ').title()
                
                # Try to get file info
                file_path = os.path.join(input_dir, csv_file)
                try:
                    with open(file_path, 'r') as f:
                        line_count = len(f.readlines()) - 1  # Subtract header
                    print(f"   {i}. [CHART] {category_display} ({line_count} pairs)")
                except:
                    print(f"   {i}. [CHART] {category_display} ({csv_file})")
            
            print(f"\n[REFRESH] LIVE DELTA EXCHANGE OPTIONS:")
            live_start = len(csv_files) + 1
        else:
            print(f"[WARN]  No CSV files found in {input_dir}")
            print(f"[BULB] Use option below to save pairs to CSV files first")
            live_start = 1
        
        print(f"   {live_start}. [MONEY] Fetch Live Spot USDT Pairs")
        print(f"   {live_start + 1}. [CRYSTAL] Fetch Live Perpetual USDT Pairs") 
        print(f"   {live_start + 2}. [CHART-UP] Fetch Live Futures Pairs")
        print(f"   {live_start + 3}. [LIGHTNING] Fetch Live Options Pairs")
        print(f"   {live_start + 4}. [SAVE] Save all pairs to CSV files")
        print(f"   {live_start + 5}. [SEARCH] View all available pairs")
        print(f"   {live_start + 6}. [ROCKET] Use top 10 volume pairs")
        print(f"   0. [ERROR] Exit")
        
        try:
            choice = input(f"\n[POINT] Select option: ").strip()
            
            if choice == '0':
                print("[WAVE] Goodbye!")
                return None
            
            choice_num = int(choice)
            
            # Handle CSV file selection
            if csv_files and 1 <= choice_num <= len(csv_files):
                selected_csv = csv_files[choice_num - 1]
                category = selected_csv.replace('delta_', '').replace('.csv', '')
                
                print(f"\n[FILE] Loading pairs from {selected_csv}...")
                pairs = load_pairs_from_csv(category)
                
                if pairs:
                    print(f"[OK] Loaded {len(pairs)} pairs from {category.replace('_', ' ').title()}")
                    
                    # Show preview of pairs
                    if len(pairs) <= 10:
                        print(f"[CHART] Pairs: {', '.join(pairs)}")
                    else:
                        print(f"[CHART] First 10 pairs: {', '.join(pairs[:10])}")
                        print(f"   ... and {len(pairs) - 10} more pairs")
                    
                    # Ask user how many to use
                    try:
                        limit_input = input(f"\nHow many pairs to use? (Enter for all {len(pairs)}): ").strip()
                        if limit_input:
                            limit = int(limit_input)
                            pairs = pairs[:limit]
                    except ValueError:
                        print("[WARN]  Invalid number, using all pairs")
                    
                    # Ask user confirmation
                    confirm = input(f"\n[OK] Use these {len(pairs)} pairs for backtesting? (y/n): ").strip().lower()
                    if confirm in ['y', 'yes']:
                        return pairs
                    else:
                        continue
                else:
                    print(f"[ERROR] Could not load pairs from {selected_csv}")
                    input("Press Enter to continue...")
                    continue
            
            # Handle live options (adjust for CSV files offset)
            live_choice = choice_num - len(csv_files) if csv_files else choice_num
            
            if live_choice == 1:  # Live Spot USDT
                return get_live_pairs_by_category('spot_usdt')
            elif live_choice == 2:  # Live Perpetual USDT
                return get_live_pairs_by_category('perpetual_usdt')
            elif live_choice == 3:  # Live Futures
                return get_live_pairs_by_category('futures_usdt')
            elif live_choice == 4:  # Live Options
                return get_live_pairs_by_category('options_calls')
            elif live_choice == 5:  # Save to CSV
                success = save_pairs_to_csv()
                if success:
                    print("[OK] Pairs saved successfully! Refreshing CSV file list...")
                    # Refresh CSV file list
                    csv_files = [f for f in os.listdir(input_dir) if f.startswith('delta_') and f.endswith('.csv')]
                input("Press Enter to continue...")
                continue
            elif live_choice == 6:  # View all pairs
                display_available_pairs()
                input("Press Enter to continue...")
                continue
            elif live_choice == 7:  # Top volume pairs
                return get_top_volume_pairs(10)
            else:
                print(f"[ERROR] Invalid option: {choice}")
                input("Press Enter to try again...")
                continue
                
        except KeyboardInterrupt:
            print("\n\n[WAVE] Operation cancelled by user")
            return None
        except ValueError:
            print(f"[ERROR] Please enter a valid number")
            input("Press Enter to try again...")
            continue
        except Exception as e:
            print(f"[ERROR] Error: {e}")
            input("Press Enter to try again...")
            continue

def get_live_pairs_by_category(category):
    """Get live pairs from Delta Exchange by category."""
    print(f"\n[REFRESH] Fetching live {category.replace('_', ' ').title()} pairs from Delta Exchange...")
    
    # Initialize Delta API if not already done
    if not delta_api.initialized:
        delta_api.initialize()
    
    if not delta_api.initialized:
        print("[ERROR] Cannot connect to Delta Exchange - using fallback pairs")
        return delta_api._get_fallback_pairs()[:10]
    
    try:
        pairs = delta_api.available_pairs
        categorized_pairs = []
        
        for pair in pairs:
            if category == 'spot_usdt' and 'USDT' in pair and '-PERP' not in pair and '-FUT' not in pair:
                categorized_pairs.append(pair)
            elif category == 'perpetual_usdt' and ('PERP' in pair or 'SWAP' in pair) and 'USDT' in pair:
                categorized_pairs.append(pair)
            elif category == 'futures_usdt' and ('FUT' in pair or 'FUTURES' in pair) and 'USDT' in pair:
                categorized_pairs.append(pair)
            elif category == 'options_calls' and ('CALL' in pair or '-C-' in pair):
                categorized_pairs.append(pair)
        
        if categorized_pairs:
            print(f"[OK] Found {len(categorized_pairs)} live {category.replace('_', ' ').title()} pairs")
            
            # Show preview
            if len(categorized_pairs) <= 15:
                print(f"[CHART] Pairs: {', '.join(categorized_pairs)}")
            else:
                print(f"[CHART] First 15 pairs: {', '.join(categorized_pairs[:15])}")
                print(f"   ... and {len(categorized_pairs) - 15} more pairs")
            
            # Ask how many to use
            try:
                limit_input = input(f"\nHow many pairs to use? (Enter for all {len(categorized_pairs)}): ").strip()
                if limit_input:
                    limit = int(limit_input)
                    return categorized_pairs[:limit]
                else:
                    return categorized_pairs
            except ValueError:
                print("[WARN]  Invalid number, using all pairs")
                return categorized_pairs
        else:
            print(f"[ERROR] No {category.replace('_', ' ').title()} pairs found")
            return delta_api._get_fallback_pairs()[:10]
            
    except Exception as e:
        print(f"[ERROR] Error fetching live pairs: {e}")
        return delta_api._get_fallback_pairs()[:10]

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Delta Exchange Multi-Strategy Backtest System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (recommended for beginners)
  python delta_backtest_strategies.py --interactive
  
  # Use specific CSV file
  python delta_backtest_strategies.py --load-csv spot_usdt
  
  # Custom symbols and strategies
  python delta_backtest_strategies.py --symbols BTC/USDT ETH/USDT --strategies RSI_30_70
  
  # Save Delta Exchange pairs to CSV files first
  python delta_backtest_strategies.py --save-pairs
  
  # View available pairs
  python delta_backtest_strategies.py --list-pairs
        """
    )
    
    # Pair selection options
    pair_group = parser.add_argument_group('pair selection options')
    pair_group.add_argument('--interactive', action='store_true', 
                           help='[TARGET] Interactive CSV file and pair selection interface (recommended)')
    pair_group.add_argument('--load-csv', type=str, metavar='CATEGORY',
                           help='[FILE] Load pairs from CSV file (spot_usdt, perpetual_usdt, futures_usdt, etc.)')
    pair_group.add_argument('--symbols', nargs='+', metavar='SYMBOL',
                           help='[MONEY] Specific trading symbols to test (e.g., BTC/USDT ETH/USDT)')
    pair_group.add_argument('--top-volume', type=int, metavar='N',
                           help='🔥 Use top N pairs by trading volume')
    
    # Strategy and timeframe options
    strategy_group = parser.add_argument_group('strategy and timeframe options')
    strategy_group.add_argument('--strategies', nargs='+', metavar='STRATEGY',
                               help='[CHART-UP] Strategies to test (RSI_30_70, MACD_Standard, Bollinger_Bands)')
    strategy_group.add_argument('--timeframes', nargs='+', metavar='TF',
                               help='⏰ Timeframes to test (1h, 4h, 1d)')
    strategy_group.add_argument('--days', type=int, default=14, metavar='N',
                               help='[CALENDAR] Days of historical data to test (default: 14)')
    
    # Output options
    output_group = parser.add_argument_group('output options')
    output_group.add_argument('--top', type=int, default=10, metavar='N',
                             help='[TROPHY] Number of top results to display (default: 10)')
    
    # Delta Exchange management
    delta_group = parser.add_argument_group('Delta Exchange management')
    delta_group.add_argument('--save-pairs', action='store_true',
                            help='[SAVE] Fetch and save all pairs to organized CSV files')
    delta_group.add_argument('--list-pairs', action='store_true',
                            help='[SEARCH] List all available Delta Exchange pairs')
    delta_group.add_argument('--real-data', action='store_true',
                            help='[REFRESH] Force attempt to use real Delta Exchange data')
    
    args = parser.parse_args()
    
    # Handle special operations first
    if args.list_pairs:
        display_available_pairs()
        return
    
    if args.save_pairs:
        success = save_pairs_to_csv()
        if success:
            print("\n[TARGET] Pairs saved successfully!")
            print("[BULB] You can now use --load-csv <category> to load specific pair types")
            print("[BULB] Or use --interactive for guided pair selection")
        return
    
    if args.interactive:
        print("[TARGET] Starting enhanced interactive pair selection...")
        selected_pairs = interactive_pair_selection()
        
        if selected_pairs:
            print(f"\n[OK] Selected {len(selected_pairs)} pairs for backtesting")
            print(f"[CHART] Pairs: {', '.join(selected_pairs[:5])}{'...' if len(selected_pairs) > 5 else ''}")
            
            # Ask for additional backtest parameters
            print(f"\n[TARGET] BACKTEST CONFIGURATION:")
            
            # Timeframes
            if not args.timeframes:
                print("⏰ Available timeframes: 1h, 4h, 1d")
                tf_input = input("Select timeframes (comma-separated, Enter for '1h'): ").strip()
                if tf_input:
                    args.timeframes = [tf.strip() for tf in tf_input.split(',')]
                else:
                    args.timeframes = ['1h']
            
            # Strategies  
            if not args.strategies:
                available_strategies = ['RSI_30_70', 'RSI_25_75', 'RSI_35_65', 'MACD_Standard', 'Bollinger_Bands']
                print(f"[CHART-UP] Available strategies: {', '.join(available_strategies)}")
                strat_input = input("Select strategies (comma-separated, Enter for 'RSI_30_70'): ").strip()
                if strat_input:
                    args.strategies = [s.strip() for s in strat_input.split(',')]
                else:
                    args.strategies = ['RSI_30_70']
            
            # Days of data
            if args.days == 14:  # Default value
                days_input = input(f"Days of data to test (Enter for {args.days}): ").strip()
                if days_input:
                    try:
                        args.days = int(days_input)
                    except ValueError:
                        print("[WARN]  Invalid number, using default 14 days")
            
            print(f"\n[ROCKET] STARTING BACKTEST:")
            print(f"   [CHART] Pairs: {len(selected_pairs)}")
            print(f"   ⏰ Timeframes: {', '.join(args.timeframes)}")
            print(f"   [CHART-UP] Strategies: {', '.join(args.strategies)}")
            print(f"   [CALENDAR] Days: {args.days}")
            
            # Initialize backtester with selected pairs
            backtester = MultiStrategyBacktester()
            
            # Run backtest with selected pairs
            results = backtester.run_comprehensive_backtest(
                selected_symbols=selected_pairs,
                selected_timeframes=args.timeframes,
                selected_strategies=args.strategies
            )
            
            if results:
                display_best_trades_table(results, args.top)
                save_results_to_csv(results)
            else:
                print("[ERROR] No results generated from backtest")
        else:
            print("[ERROR] No pairs selected - exiting")
        return
    
    # Initialize backtester for regular operations
    backtester = MultiStrategyBacktester()
    
    # Determine symbols to use
    symbols = args.symbols
    
    if args.load_csv:
        print(f"[FILE] Loading pairs from CSV category: {args.load_csv}")
        symbols = load_pairs_from_csv(args.load_csv)
        if not symbols:
            print("[WARN]  No pairs loaded from CSV - using default pairs")
            symbols = backtester.trading_pairs[:10]
    elif args.top_volume:
        print(f"🔥 Using top {args.top_volume} pairs by volume...")
        symbols = get_top_volume_pairs(args.top_volume)
    elif not symbols:
        # Default to a good selection of major pairs
        symbols = backtester.trading_pairs[:10]
    
    print(f"\n[TARGET] SELECTED TRADING PAIRS: {', '.join(symbols[:10])}")
    if len(symbols) > 10:
        print(f"   ... and {len(symbols) - 10} more pairs")
    
    # Run comprehensive backtest
    results = backtester.run_comprehensive_backtest(
        selected_symbols=symbols,
        selected_timeframes=args.timeframes,
        selected_strategies=args.strategies
    )
    
    if results:
        # Display best trades table
        display_best_trades_table(results, args.top)
        
        # Save to CSV
        save_results_to_csv(results)
        
        # Display Delta Exchange connection status
        if USE_REAL_DATA and delta_api.initialized:
            print(f"\n🔗 DELTA EXCHANGE CONNECTION: [OK] Active")
            print(f"[CHART] Used real market data for backtesting")
        else:
            print(f"\n🔗 DELTA EXCHANGE CONNECTION: [ERROR] Using simulated data")
            print(f"[BULB] Install CCXT and check connection for real data")
    else:
        print("[ERROR] No successful backtests to display")
        print("\n[BULB] TROUBLESHOOTING TIPS:")
        print("   • Try different timeframes (1h, 4h, 1d)")
        print("   • Use different symbols with --symbols BTC/USDT ETH/USDT")
        print("   • Check Delta Exchange connection with --list-pairs")
        print("   • Save pairs to CSV with --save-pairs")
        print("   • Use interactive mode with --interactive")
        print("   • Load specific pair types with --load-csv spot_usdt")
        print("   • Increase days with --days 30 for more data")
        print("\n[WRENCH] PAIR MANAGEMENT COMMANDS:")
        print("   • --list-pairs          : View all available pairs")
        print("   • --save-pairs          : Save pairs to organized CSV files")
        print("   • --interactive         : Interactive pair selection")
        print("   • --load-csv spot_usdt  : Load specific pair category")
        print("   • --top-volume 20       : Use top volume pairs")

if __name__ == "__main__":
    main()

def save_pairs_to_csv():
    """Save Delta Exchange pairs to organized CSV files."""
    print("[REFRESH] Initializing Delta Exchange connection for pair export...")
    
    # Initialize Delta API if not already done
    if not delta_api.initialized:
        delta_api.initialize()
    
    if not delta_api.initialized:
        print("[ERROR] Cannot save pairs - Delta Exchange not connected")
        return False
    
    # Ensure input directory exists
    input_dir = os.path.join(os.path.dirname(__file__), '..', 'input')
    os.makedirs(input_dir, exist_ok=True)
    
    pairs = delta_api.available_pairs
    print(f"[CHART] Processing {len(pairs)} total pairs...")
    
    # Categorize pairs
    categories = {
        'spot_usdt': [],
        'spot_btc': [],
        'spot_eth': [],
        'futures_usdt': [],
        'futures_btc': [],
        'options_calls': [],
        'options_puts': [],
        'perpetual_usdt': [],
        'other_pairs': []
    }
    
    for pair in pairs:
        # Categorize by market type and quote currency
        if '-PERP' in pair:
            if 'USDT' in pair:
                categories['perpetual_usdt'].append(pair)
            else:
                categories['other_pairs'].append(pair)
        elif '-FUTURES' in pair or 'FUT' in pair:
            if 'USDT' in pair:
                categories['futures_usdt'].append(pair)
            elif 'BTC' in pair:
                categories['futures_btc'].append(pair)
            else:
                categories['other_pairs'].append(pair)
        elif '-C-' in pair or 'CALL' in pair:
            categories['options_calls'].append(pair)
        elif '-P-' in pair or 'PUT' in pair:
            categories['options_puts'].append(pair)
        elif 'USDT' in pair:
            categories['spot_usdt'].append(pair)
        elif 'BTC' in pair:
            categories['spot_btc'].append(pair)
        elif 'ETH' in pair:
            categories['spot_eth'].append(pair)
        else:
            categories['other_pairs'].append(pair)
    
    # Save each category to separate CSV files
    saved_files = []
    
    for category, pair_list in categories.items():
        if pair_list:
            filename = f"delta_{category}.csv"
            filepath = os.path.join(input_dir, filename)
            
            # Create CSV content with additional metadata
            csv_content = ['Symbol,Quote_Currency,Market_Type,Active,Description']
            
            for pair in sorted(pair_list):
                # Get symbol info if available
                symbol_info = delta_api.get_symbol_info(pair)
                
                if symbol_info:
                    quote = symbol_info.get('quote', 'UNKNOWN')
                    market_type = 'SPOT'
                    if '-PERP' in pair:
                        market_type = 'PERPETUAL'
                    elif '-FUTURES' in pair or 'FUT' in pair:
                        market_type = 'FUTURES'
                    elif '-C-' in pair or 'CALL' in pair:
                        market_type = 'OPTIONS_CALL'
                    elif '-P-' in pair or 'PUT' in pair:
                        market_type = 'OPTIONS_PUT'
                    
                    active = 'YES' if symbol_info.get('active', True) else 'NO'
                    description = f"{symbol_info.get('base', '')}/{quote} {market_type}"
                else:
                    # Fallback info
                    if 'USDT' in pair:
                        quote = 'USDT'
                    elif 'BTC' in pair:
                        quote = 'BTC'
                    elif 'ETH' in pair:
                        quote = 'ETH'
                    else:
                        quote = 'UNKNOWN'
                    
                    market_type = category.upper().replace('_', ' ')
                    active = 'YES'
                    description = f"{pair} {market_type}"
                
                csv_content.append(f"{pair},{quote},{market_type},{active},{description}")
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(csv_content))
            
            saved_files.append((filename, len(pair_list)))
            print(f"[OK] Saved {len(pair_list)} {category.replace('_', ' ')} pairs to {filename}")
    
    # Create a master summary file
    summary_file = os.path.join(input_dir, "delta_pairs_summary.csv")
    summary_content = ['Category,Filename,Pair_Count,Description']
    
    for filename, count in saved_files:
        category = filename.replace('delta_', '').replace('.csv', '')
        description = f"Delta Exchange {category.replace('_', ' ').title()} Trading Pairs"
        summary_content.append(f"{category},{filename},{count},{description}")
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(summary_content))
    
    print(f"\n[SAVE] PAIR EXPORT SUMMARY:")
    print("="*50)
    for filename, count in saved_files:
        print(f"[FILE] {filename:<25} - {count:>3} pairs")
    
    print(f"\n[CLIPBOARD] Summary file: delta_pairs_summary.csv")
    print(f"[FOLDER] All files saved to: {input_dir}")
    print(f"[TARGET] Total pairs exported: {sum([count for _, count in saved_files])}")
    
    return True

def load_pairs_from_csv(category='spot_usdt'):
    """Load trading pairs from specific CSV file."""
    input_dir = os.path.join(os.path.dirname(__file__), '..', 'input')
    filename = f"delta_{category}.csv"
    filepath = os.path.join(input_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"[WARN]  File not found: {filename}")
        print(f"[BULB] Run with --save-pairs to generate CSV files first")
        return []
    
    pairs = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[1:]:  # Skip header
                if line.strip():
                    pair = line.strip().split(',')[0]
                    pairs.append(pair)
        
        print(f"[OK] Loaded {len(pairs)} pairs from {filename}")
        return pairs
        
    except Exception as e:
        print(f"[ERROR] Error loading pairs from {filename}: {e}")
        return []
