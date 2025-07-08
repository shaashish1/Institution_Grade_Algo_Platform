#!/usr/bin/env python3
"""
Real-time Trader - Forward testing and live trading module for AlgoProject
Renamed from main.py for better clarity
"""

import argparse
import yaml
import pandas as pd
import importlib.util
from pathlib import Path
import time
import asyncio
import ccxt
import os
from datetime import datetime
import pytz
from tabulate import tabulate
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

def load_config(config_path="config/config.yaml"):
    """Load configuration from YAML file."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def load_assets(asset_type, config):
    """Load asset symbols from the configured CSV file."""
    asset_file = config["assets"]["crypto"] if asset_type == "crypto" else config["assets"]["stocks"]
    return pd.read_csv(asset_file)["symbol"].tolist()

def load_strategy(strategy_path, class_name):
    """Dynamically import and return the strategy class."""
    spec = importlib.util.spec_from_file_location(class_name, strategy_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)

def fetch_data(symbol, exchange, interval, bars, data_source, fetch_timeout):
    """Fetch historical data for a symbol using the specified data source."""
    if data_source == "tvdatafeed":
        try:
            from tvDatafeed import TvDatafeed, Interval
            tv = TvDatafeed()
            
            # Convert interval string to Interval enum
            interval_map = {
                "1m": Interval.in_1_minute,
                "5m": Interval.in_5_minute,
                "15m": Interval.in_15_minute,
                "1h": Interval.in_1_hour,
                "4h": Interval.in_4_hour,
                "1d": Interval.in_daily
            }
            
            tv_interval = interval_map.get(interval, Interval.in_5_minute)
            return tv.get_hist(symbol=symbol, exchange=exchange, interval=tv_interval, n_bars=bars)
        except Exception as e:
            print(f"TvDatafeed error for {symbol}: {e}")
            # Fallback to CCXT
            data_source = "ccxt"
    
    if data_source == "ccxt":
        try:
            # Use Kraken for crypto
            if exchange.upper() == "KRAKEN":
                exchange_obj = ccxt.kraken()
            else:
                exchange_obj = getattr(ccxt, exchange.lower())()
            
            exchange_obj.enableRateLimit = True
            kraken_markets = exchange_obj.load_markets()
            
            # Symbol mapping for Kraken
            if symbol not in kraken_markets:
                for market in kraken_markets:
                    if market.replace('/', '') == symbol.replace('/', ''):
                        symbol = market
                        break
            
            import threading
            result = {}
            
            def fetch():
                try:
                    ohlcv = exchange_obj.fetch_ohlcv(symbol, timeframe=interval, limit=bars)
                    result['data'] = ohlcv
                except Exception as e:
                    result['error'] = e

            thread = threading.Thread(target=fetch)
            thread.start()
            thread.join(timeout=fetch_timeout)  # Configurable timeout

            if thread.is_alive():
                raise RuntimeError(f"Timeout fetching data for {symbol} on {exchange}")
            if 'error' in result:
                raise RuntimeError(f"Error fetching data for {symbol} on {exchange}: {result['error']}")
            
            ohlcv = result.get('data', [])
            df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
            if df.empty:
                raise RuntimeError(f"No data returned for {symbol} on {exchange}")
            return df
        except Exception as e:
            print(f"CCXT error for {symbol}: {e}")
            return pd.DataFrame()
    else:
        raise ValueError("Unsupported data source")

# --- Async data fetch for real-time scanning ---
async def async_fetch_data(symbol, exchange, interval, bars, fetch_timeout, api_creds=None):
    import asyncio
    import threading
    
    def sync_fetch():
        try:
            exchange_class = getattr(ccxt, exchange.lower())
            if api_creds and api_creds.get('api_key'):
                exchange_obj = exchange_class({
                    'apiKey': api_creds.get('api_key'),
                    'secret': api_creds.get('api_secret'),
                    'enableRateLimit': True,
                    'sandbox': False
                })
            else:
                exchange_obj = exchange_class({'enableRateLimit': True})
            
            # Load markets synchronously
            markets = exchange_obj.load_markets()
            
            # Fetch OHLCV data
            ohlcv = exchange_obj.fetch_ohlcv(symbol, timeframe=interval, limit=bars)
            
            df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
            return df
        except Exception as e:
            print(f"Error fetching {symbol} from {exchange}: {e}")
            return pd.DataFrame()
    
    # Run sync function in thread
    loop = asyncio.get_event_loop()
    df = await loop.run_in_executor(None, sync_fetch)
    return df

# --- Trade lifecycle management ---
class TradeManager:
    def __init__(self):
        self.open_trades = []
        self.closed_trades = []

    def has_open_trade(self, symbol):
        """Check if there's already an open trade for this symbol."""
        return any(trade['symbol'] == symbol for trade in self.open_trades)

    def open_trade(self, symbol, side, entry_price, entry_time, amount):
        # Don't open a new trade if one is already open for this symbol
        if self.has_open_trade(symbol):
            return False
            
        trade = {
            'symbol': symbol,
            'side': side,
            'entry_price': entry_price,
            'entry_time': entry_time,
            'amount': amount,
            'exit_price': None,
            'exit_time': None,
            'pnl': 0,
            'pnl_usd': 0,
            'status': 'OPEN'
        }
        self.open_trades.append(trade)
        print(f"🟢 TRADE OPENED: {symbol} {side} @ {entry_price} at {self.format_timestamp_ist(entry_time)}")
        return True

    def close_trade(self, symbol, exit_price, exit_time):
        for trade in self.open_trades:
            if trade['symbol'] == symbol:
                trade['exit_price'] = exit_price
                trade['exit_time'] = exit_time
                # Fix PnL calculation: For LONG, profit when exit > entry
                if trade['side'] == 'LONG':
                    trade['pnl'] = (exit_price - trade['entry_price']) / trade['entry_price']
                else:  # SHORT
                    trade['pnl'] = (trade['entry_price'] - exit_price) / trade['entry_price']
                trade['pnl_usd'] = trade['pnl'] * trade['amount']
                trade['status'] = 'CLOSED'
                self.closed_trades.append(trade)
                self.open_trades.remove(trade)
                print(f"🔴 TRADE CLOSED: {symbol} {trade['side']} @ {exit_price} at {self.format_timestamp_ist(exit_time)} | PnL: ${trade['pnl_usd']:.2f}")
                break

    def update_unrealized_pnl(self, symbol, current_price):
        for trade in self.open_trades:
            if trade['symbol'] == symbol:
                trade['current_price'] = current_price
                # Fix unrealized PnL calculation
                if trade['side'] == 'LONG':
                    unrealized_pnl = (current_price - trade['entry_price']) / trade['entry_price']
                else:  # SHORT
                    unrealized_pnl = (trade['entry_price'] - current_price) / trade['entry_price']
                trade['unrealized_pnl'] = unrealized_pnl
                trade['unrealized_pnl_usd'] = unrealized_pnl * trade['amount']

    def format_timestamp_ist(self, timestamp):
        """Format timestamp to IST timezone string."""
        if hasattr(timestamp, 'strftime'):
            # If it's already timezone-aware, convert to IST
            if hasattr(timestamp, 'tz_convert'):
                ist_time = timestamp.tz_convert('Asia/Kolkata')
                return ist_time.strftime('%Y-%m-%d %H:%M:%S IST')
            else:
                return timestamp.strftime('%Y-%m-%d %H:%M:%S IST')
        else:
            return str(timestamp)

    def get_open_trades_df(self):
        if not self.open_trades:
            return pd.DataFrame()
        
        trades_data = []
        for trade in self.open_trades:
            # Calculate unrealized PnL
            current_price = trade.get('current_price', trade['entry_price'])
            unrealized_pnl_usd = trade.get('unrealized_pnl_usd', 0)
            
            trades_data.append({
                'Symbol': trade['symbol'][:8],  # Shorter symbol
                'Side': trade['side'],
                'Entry_Time': self.format_timestamp_ist(trade['entry_time'])[11:16],  # Just time HH:MM
                'Entry_Price': f"{trade['entry_price']:.2f}",
                'Current_Price': f"{current_price:.2f}",
                'Amount': f"${trade['amount']:.0f}",
                'Unrealized_PnL': f"${unrealized_pnl_usd:.2f}"
            })
        return pd.DataFrame(trades_data)

    def get_closed_trades_df(self):
        if not self.closed_trades:
            return pd.DataFrame()
        
        trades_data = []
        for trade in self.closed_trades:
            trades_data.append({
                'Symbol': trade['symbol'][:8],  # Shorter symbol
                'Side': trade['side'],
                'Entry_Time': self.format_timestamp_ist(trade['entry_time'])[11:16],  # Just time HH:MM
                'Entry_Price': f"{trade['entry_price']:.2f}",
                'Exit_Time': self.format_timestamp_ist(trade['exit_time'])[11:16],  # Just time HH:MM
                'Exit_Price': f"{trade['exit_price']:.2f}",
                'Amount': f"${trade['amount']:.0f}",
                'PnL': f"${trade['pnl_usd']:.2f}"
            })
        return pd.DataFrame(trades_data)

    def get_total_pnl(self):
        realized_pnl = sum(trade['pnl_usd'] for trade in self.closed_trades)
        unrealized_pnl = sum(trade.get('unrealized_pnl_usd', 0) for trade in self.open_trades)
        return realized_pnl, unrealized_pnl, realized_pnl + unrealized_pnl

    def get_open_trades(self):
        return self.open_trades

    def get_closed_trades(self):
        return self.closed_trades

# --- Async main for real-time scan and forward test ---
async def async_main(config_path="config/config.yaml"):
    config = load_config(config_path)
    asset_type = config['asset_type']
    symbols = load_assets(asset_type, config)
    strategy_file = config['strategy']['file']
    strategy_class = config['strategy']['class']
    exchange = config['exchange']
    interval = config.get('interval', '5m')
    bars = config.get('bars', 100)
    trading_amount = config.get('trading_amount', 1000)
    fetch_timeout = config.get('fetch_timeout', 15)
    api_creds = {
        'api_key': os.environ.get('API_KEY', config.get('api_key', '')),
        'api_secret': os.environ.get('API_SECRET', config.get('api_secret', ''))
    }
    strategy_path = Path('src/strategies') / strategy_file
    StrategyClass = load_strategy(str(strategy_path), strategy_class)
    strategy = StrategyClass()
    trade_manager = TradeManager()

    print(f"🚀 [FORWARD TEST] Scanning {len(symbols)} symbols on {exchange}...")
    print(f"📊 Strategy: {strategy_class} | Interval: {interval} | Amount per trade: ${trading_amount}")
    print("=" * 80)
    
    scan_count = 0
    while True:
        scan_count += 1
        # Clear previous output for cleaner display
        if scan_count > 1:
            print("\n" + "🔄" * 40 + f" SCAN #{scan_count} " + "🔄" * 40)
        
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')} | 🔍 Scanning {len(symbols)} symbols...")
        
        # Fetch data with progress indication
        start_time = time.time()
        tasks = [async_fetch_data(symbol, exchange, interval, bars, fetch_timeout, api_creds) for symbol in symbols]
        results = await asyncio.gather(*tasks)
        fetch_time = time.time() - start_time
        
        print(f"✅ Data fetched in {fetch_time:.1f}s | Processing signals...")
        
        current_prices = {}
        signals_found = 0
        
        for symbol, df in zip(symbols, results):
            if df is not None and not df.empty:
                if 'timestamp' in df.columns:
                    df['datetime_ist'] = pd.to_datetime(df['timestamp'], unit='ms' if df['timestamp'].max() > 1e12 else 's').dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
                
                signal = strategy.generate_signal(df)
                last_row = df.iloc[-1]
                price = last_row['close']
                ts = last_row['datetime_ist']
                current_prices[symbol] = price
                
                # Update unrealized PnL for open trades
                trade_manager.update_unrealized_pnl(symbol, price)
                
                # Enhanced trading logic with better signal handling
                has_open_trade = trade_manager.has_open_trade(symbol)
                
                if signal != "HOLD":
                    signals_found += 1
                    status = "🔒 Open" if has_open_trade else "🆓 Available"
                    print(f"🎯 {symbol}: {signal} | Price: {price:.4f} | {status}")
                
                # Trade management with proper state checking
                if signal.startswith('BUY') and not has_open_trade:
                    # Only open new trade if no existing trade
                    trade_manager.open_trade(symbol, 'LONG', price, ts, trading_amount)
                elif signal.startswith('SELL') and has_open_trade:
                    # Only close trade if we have an open position
                    trade_manager.close_trade(symbol, price, ts)

        # Update current prices and unrealized PnL for all open trades
        for trade in trade_manager.get_open_trades():
            if trade['symbol'] in current_prices:
                trade['current_price'] = current_prices[trade['symbol']]
                trade_manager.update_unrealized_pnl(trade['symbol'], current_prices[trade['symbol']])
        
        # Scan summary
        open_positions = len(trade_manager.get_open_trades())
        closed_trades = len(trade_manager.get_closed_trades())
        print(f"\n📊 Scan Complete: {signals_found} signals found | {open_positions} open positions | {closed_trades} closed trades")
        
        # Display current positions with enhanced formatting (only if there are positions or trades)
        if open_positions > 0 or closed_trades > 0:
            print("\n" + "=" * 100)
            print("📈 OPEN POSITIONS:")
            print("=" * 100)
            open_trades_df = trade_manager.get_open_trades_df()
            if not open_trades_df.empty:
                print(tabulate(open_trades_df, headers='keys', tablefmt='grid', stralign='center'))
            else:
                print("No open positions")
            
            if closed_trades > 0:
                print("\n" + "=" * 100)
                print("📊 RECENT CLOSED TRADES:")
                print("=" * 100)
                closed_trades_df = trade_manager.get_closed_trades_df()
                if not closed_trades_df.empty:
                    print(tabulate(closed_trades_df.tail(3), headers='keys', tablefmt='grid', stralign='center'))
            
            # Show PnL summary with better formatting
            realized_pnl, unrealized_pnl, total_pnl = trade_manager.get_total_pnl()
            print("\n" + "=" * 100)
            print("💰 PnL SUMMARY:")
            print("=" * 100)
            print(f"{'Realized PnL:':<20} ${realized_pnl:>10.2f}")
            print(f"{'Unrealized PnL:':<20} ${unrealized_pnl:>10.2f}")
            print(f"{'Total PnL:':<20} ${total_pnl:>10.2f}")
            print("=" * 100)
        
        # Wait before next scan
        sleep_time = config.get('sleep_between_symbols', 60)  # Default 60 seconds between scans
        print(f"\n⏳ Waiting {sleep_time} seconds before next scan...")
        await asyncio.sleep(sleep_time)

def main():
    parser = argparse.ArgumentParser(description="Algo Trading Platform")
    parser.add_argument("--config", type=str, default="config/config.yaml", help="Path to config file")
    parser.add_argument("--forward", action="store_true", help="Run in forward test mode (real-time)")
    args = parser.parse_args()

    if args.forward:
        asyncio.run(async_main(args.config))
        return

    # === Load configuration ===
    config = load_config(args.config)

    # --- Fix: Provide a clear error if asset_type is missing, and show all config keys for debugging ---
    if "asset_type" not in config:
        print("ERROR: 'asset_type' is missing from your config.yaml.")
        print("Your config.yaml keys are:", list(config.keys()))
        print("Please add a line like: asset_type: crypto")
        return

    # === Extract configuration values ===
    # Asset type: "crypto" or "stocks"
    asset_type = config["asset_type"]
    # Asset CSV files
    assets_config = config["assets"]
    # Strategy file and class
    strategy_file = config["strategy"]["file"]
    strategy_class = config["strategy"]["class"]
    # Exchange and data source
    exchange = config["exchange"]
    data_source = config.get("data_source", "tvdatafeed")
    # Timeframe/interval and bars to fetch
    interval = config.get("interval", "1m" if asset_type == "crypto" else "in_1_minute")
    bars = config.get("bars", 100)
    # Trading simulation amount per trade
    trading_amount = config.get("trading_amount", 1000)
    # Start date for backtest (optional)
    start_date = config.get("start_date", None)
    # Data fetch timeout (seconds)
    fetch_timeout = config.get("fetch_timeout", 15)
    # Output file names
    scan_results_file = config.get("scan_results_file", f"output/scan_results_{asset_type}.csv")
    backtest_trades_file = config.get("backtest_trades_file", f"output/backtest_trades_{asset_type}.csv")
    # Sleep between symbols (for rate limiting)
    sleep_between_symbols = config.get("sleep_between_symbols", 1)

    # === Load assets ===
    symbols = load_assets(asset_type, config)

    # === Load strategy ===
    strategy_path = Path("src/strategies") / strategy_file
    StrategyClass = load_strategy(str(strategy_path), strategy_class)
    strategy = StrategyClass()

    print(f"🔍 Scanning {asset_type} assets: {len(symbols)} symbols")
    print(f"📊 Strategy: {strategy_class} | Exchange: {exchange} | Data: {data_source}")
    print("=" * 80)
    
    # Fetch data with progress indication (similar to forward mode)
    start_time = time.time()
    results = []
    backtest_trades = []
    current_prices = {}
    signals_found = 0
    
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')} | 🔍 Processing {len(symbols)} symbols...")
    
    for i, symbol in enumerate(symbols, 1):
        try:
            # Progress indicator
            if i % 10 == 0 or i == len(symbols):
                print(f"📊 Progress: {i}/{len(symbols)} symbols processed...")
            
            data = fetch_data(symbol, exchange, interval, bars, data_source, fetch_timeout)
            if data is not None and not data.empty:
                try:
                    df = data.copy()
                    if "timestamp" in df.columns:
                        df["datetime_ist"] = pd.to_datetime(df["timestamp"], unit="ms" if df["timestamp"].max() > 1e12 else "s").dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
                    else:
                        df["datetime_ist"] = pd.NaT

                    # Filter by start_date if provided
                    if start_date:
                        df = df[df["datetime_ist"] >= pd.to_datetime(start_date).tz_localize("Asia/Kolkata")]

                    signal_result = strategy.generate_signal(df)
                    last_row = df.iloc[-1]
                    price = last_row["close"]
                    ts = last_row["datetime_ist"]
                    current_prices[symbol] = price
                    
                    if signal_result != "HOLD":
                        signals_found += 1
                        print(f"🎯 {symbol}: {signal_result} | Price: {price:.4f}")

                    # For backtest: store all signals, prices, timestamps
                    results.append({
                        "symbol": symbol,
                        "signal": signal_result,
                        "price": price,
                        "datetime_ist": ts
                    })

                    # Backtest and collect trades
                    if hasattr(strategy, "backtest"):
                        trades = strategy.backtest(df)
                        if not trades.empty:
                            trades["symbol"] = symbol
                            trades["amount"] = trading_amount
                            trades["pnl_usd"] = trades["pnl"] * (trades["amount"] / trades["entry_price"])
                            backtest_trades.append(trades)
                except Exception as e:
                    print(f"   ❌ Error applying strategy for {symbol}: {e}")
            else:
                pass  # Remove the "No data available" message to reduce clutter
            # Remove sleep to process faster like forward mode
        except Exception as e:
            print(f"   ❌ Error fetching data for {symbol}: {e}")

    fetch_time = time.time() - start_time
    print(f"✅ All data processed in {fetch_time:.1f}s | {signals_found} signals found")
    
    # === Save scan results ===
    results_df = pd.DataFrame(results)
    results_df.to_csv(scan_results_file, index=False)
    print(f"💾 Scan results saved to {scan_results_file}")

    # === Save backtest trades and display enhanced summary ===
    if backtest_trades:
        all_trades = pd.concat(backtest_trades, ignore_index=True)
        try:
            all_trades.to_csv(backtest_trades_file, index=False)
            print(f"💾 Backtest trades saved to {backtest_trades_file}")
        except PermissionError:
            print(f"❌ Permission denied: Could not write to {backtest_trades_file}. Please close the file if it's open in another program and try again.")
        
        # Enhanced display using the same format as forward mode
        print("\n" + "=" * 100)
        print("📊 BACKTEST SUMMARY")
        print("=" * 100)
        
        # Format trades for display using the same TradeManager style
        def format_timestamp_ist(timestamp):
            """Format timestamp to IST timezone string."""
            if hasattr(timestamp, 'strftime'):
                if hasattr(timestamp, 'tz_convert'):
                    ist_time = timestamp.tz_convert('Asia/Kolkata')
                    return ist_time.strftime('%H:%M')  # Just time HH:MM like forward mode
                else:
                    return timestamp.strftime('%H:%M')
            else:
                return str(timestamp)[:5]  # Fallback to first 5 chars
        
        # Create display data in the same format as forward mode
        trades_data = []
        for _, trade in all_trades.iterrows():
            trades_data.append({
                'Symbol': trade['symbol'][:8],  # Shorter symbol like forward mode
                'Side': 'LONG' if trade['side'].startswith('BUY') else 'SHORT',
                'Entry_Time': format_timestamp_ist(trade['entry_time']),
                'Entry_Price': f"{trade['entry_price']:.2f}",
                'Exit_Time': format_timestamp_ist(trade['exit_time']),
                'Exit_Price': f"{trade['exit_price']:.2f}",
                'Amount': f"${trade['amount']:.0f}",
                'PnL': f"${trade['pnl_usd']:.2f}"
            })
        
        trades_display_df = pd.DataFrame(trades_data)
        
        # Display using tabulate with same styling as forward mode
        print(tabulate(trades_display_df, headers='keys', tablefmt='grid', stralign='center'))
        
        # PnL Summary in same format as forward mode
        total_pnl = all_trades["pnl_usd"].sum()
        win_trades = len(all_trades[all_trades["pnl_usd"] > 0])
        total_trades = len(all_trades)
        win_rate = (win_trades / total_trades * 100) if total_trades > 0 else 0
        
        print("\n" + "=" * 100)
        print("💰 PnL SUMMARY:")
        print("=" * 100)
        print(f"{'Realized PnL:':<20} ${total_pnl:>10.2f}")
        print(f"{'Unrealized PnL:':<20} ${0:>10.2f}")  # No unrealized PnL in backtest
        print(f"{'Total PnL:':<20} ${total_pnl:>10.2f}")
        print(f"{'Total Trades:':<20} {total_trades:>10}")
        print(f"{'Win Rate:':<20} {win_rate:>9.1f}%")
        print("=" * 100)
    else:
        print("\n⚠️  No trades generated in backtest.")

if __name__ == "__main__":
    main()
