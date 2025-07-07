# Entry point for AlgoProject

import argparse
import yaml
import pandas as pd
import importlib.util
from pathlib import Path
import time

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def load_assets(asset_type, config):
    asset_file = config["assets"]["crypto"] if asset_type == "crypto" else config["assets"]["stocks"]
    return pd.read_csv(asset_file)["symbol"].tolist()

def load_strategy(strategy_path, class_name):
    spec = importlib.util.spec_from_file_location(class_name, strategy_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)

def fetch_data(symbol, exchange, interval, bars, data_source):
    if data_source == "tvdatafeed":
        from tvDatafeed import TvDatafeed, Interval
        tv = TvDatafeed()
        return tv.get_hist(symbol=symbol, exchange=exchange, interval=getattr(Interval, interval), n_bars=bars)
    elif data_source == "ccxt":
        import ccxt
        # Use Kraken for crypto
        if exchange.upper() == "KRAKEN":
            exchange_obj = ccxt.kraken()
        else:
            exchange_obj = getattr(ccxt, exchange.lower())()
        exchange_obj.session.verify = False  # disables SSL verification for requests
        # Map symbol to Kraken's market id if needed
        kraken_markets = exchange_obj.load_markets()
        if symbol not in kraken_markets:
            # Try to find the correct symbol (Kraken uses XBT instead of BTC, etc.)
            for market in kraken_markets:
                if market.replace('/', '') == symbol.replace('/', ''):
                    symbol = market
                    break
        # For Kraken, intervals should be like '1m', '5m', '1h', etc.
        # Remove signal.SIGALRM (not available on Windows)
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
        thread.join(timeout=15)  # 15 seconds timeout

        if thread.is_alive():
            raise RuntimeError(f"Timeout fetching data for {symbol} on {exchange}")
        if 'error' in result:
            raise RuntimeError(f"Error fetching data for {symbol} on {exchange}: {result['error']}")
        ohlcv = result.get('data', [])
        import pandas as pd
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        if df.empty:
            raise RuntimeError(f"No data returned for {symbol} on {exchange}")
        return df
    else:
        raise ValueError("Unsupported data source")

def main():
    parser = argparse.ArgumentParser(description="Algo Trading Platform")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to config file")
    args = parser.parse_args()

    config = load_config(args.config)
    asset_type = config["asset_type"]
    strategy_file = config["strategy"]["file"]
    strategy_class = config["strategy"]["class"]
    exchange = config["exchange"]
    interval = config["interval"]
    bars = config.get("bars", 100)
    data_source = config.get("data_source", "tvdatafeed")
    start_date = config.get("start_date", None)
    trading_amount = config.get("trading_amount", 1000)

    # Load assets
    symbols = load_assets(asset_type, config)

    # Load strategy
    strategy_path = Path("src/strategies") / strategy_file
    StrategyClass = load_strategy(str(strategy_path), strategy_class)
    strategy = StrategyClass()

    # Detect data source and interval based on asset_type
    if asset_type == "crypto":
        data_source = "ccxt"
        interval = "1m"
    else:
        data_source = "tvdatafeed"
        interval = "in_1_minute"

    print(f"Scanning {asset_type} assets: {symbols}")
    results = []
    backtest_trades = []
    for symbol in symbols:
        try:
            data = fetch_data(symbol, exchange, interval, bars, data_source)
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
                    print(f"{symbol}: {signal_result} | Price: {price} | Time: {ts}")

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
                            # Calculate P/L in USD for each trade
                            trades["amount"] = trading_amount
                            trades["pnl_usd"] = trades["pnl"] * (trades["amount"] / trades["entry_price"])
                            backtest_trades.append(trades)
                except Exception as e:
                    print(f"{symbol}: Error applying strategy: {e}")
            else:
                print(f"{symbol}: No data")
            time.sleep(1)
        except Exception as e:
            print(f"{symbol}: Error fetching data: {e}")

    pd.DataFrame(results).to_csv(f"scan_results_{asset_type}.csv", index=False)
    print(f"Scan results saved to scan_results_{asset_type}.csv")

    # Save backtest trades to CSV and print summary
    if backtest_trades:
        all_trades = pd.concat(backtest_trades, ignore_index=True)
        out_csv = f"backtest_trades_{asset_type}.csv"
        try:
            all_trades.to_csv(out_csv, index=False)
            print(f"Backtest trades saved to {out_csv}")
        except PermissionError:
            print(f"Permission denied: Could not write to {out_csv}. Please close the file if it's open in another program and try again.")
        total_pnl = all_trades["pnl_usd"].sum()
        print(f"Total P/L (USD) for all trades with ${trading_amount} per trade: {total_pnl:.2f}")

if __name__ == "__main__":
    main()
    main()
