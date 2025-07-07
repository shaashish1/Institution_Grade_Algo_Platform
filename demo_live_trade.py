import ccxt
import pandas as pd
import time
from datetime import datetime
from src.strategies.VWAPSigma2Strategy import VWAPSigma2Strategy

def fetch_latest_ohlcv(exchange, symbol, timeframe="5m", window=30):
    # Fetch the latest N bars (window) for live calculation
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=window)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["datetime_ist"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True).dt.tz_convert("Asia/Kolkata")
    return df

def main():
    # --- CONFIG ---
    symbol = "BTC/USD"  # Change as needed
    timeframe = "5m"
    window = 30  # Number of bars to use for VWAP/STD calculation
    trading_amount = 1000  # USD per trade (simulated)
    demo_iterations = 10   # How many live bars to simulate
    sleep_seconds = 300    # 5 minutes between checks

    # --- INIT ---
    exchange = ccxt.kraken()
    exchange.load_markets()
    strat = VWAPSigma2Strategy()
    trades = []
    position = None
    entry_price = 0
    entry_time = None

    print(f"Starting demo live trade for {symbol} on {exchange.name} ({timeframe})...")

    for i in range(demo_iterations):
        df = fetch_latest_ohlcv(exchange, symbol, timeframe, window)
        signal = strat.generate_signal(df)
        last_row = df.iloc[-1]
        price = last_row["close"]
        ts = last_row["datetime_ist"]

        print(f"[{ts}] {symbol} | Price: {price} | Signal: {signal}")

        # Simulate trade logic (long only, TP/SL as in backtest)
        take_profit = 0.0628
        stop_loss = -0.0314

        if position == "long":
            change = (price - entry_price) / entry_price
            if change >= take_profit:
                trades.append({
                    "entry_time": entry_time,
                    "exit_time": ts,
                    "side": "BUY_TP",
                    "entry_price": entry_price,
                    "exit_price": price,
                    "pnl": price - entry_price,
                    "pnl_usd": (price - entry_price) * (trading_amount / entry_price)
                })
                print(f"TAKE PROFIT: Closed long at {price} (PnL: {trades[-1]['pnl_usd']:.2f} USD)")
                position = None
            elif change <= stop_loss:
                trades.append({
                    "entry_time": entry_time,
                    "exit_time": ts,
                    "side": "BUY_SL",
                    "entry_price": entry_price,
                    "exit_price": price,
                    "pnl": price - entry_price,
                    "pnl_usd": (price - entry_price) * (trading_amount / entry_price)
                })
                print(f"STOP LOSS: Closed long at {price} (PnL: {trades[-1]['pnl_usd']:.2f} USD)")
                position = None

        # Entry logic
        if position is None and signal.startswith("BUY"):
            position = "long"
            entry_price = price
            entry_time = ts
            print(f"OPEN LONG: {symbol} at {price} ({ts})")

        # Wait for next bar
        if i < demo_iterations - 1:
            print(f"Waiting for next bar ({sleep_seconds} seconds)...")
            time.sleep(sleep_seconds)

    # Close any open position at the end
    if position == "long":
        trades.append({
            "entry_time": entry_time,
            "exit_time": ts,
            "side": "BUY_EOD",
            "entry_price": entry_price,
            "exit_price": price,
            "pnl": price - entry_price,
            "pnl_usd": (price - entry_price) * (trading_amount / entry_price)
        })
        print(f"END OF DEMO: Closed long at {price} (PnL: {trades[-1]['pnl_usd']:.2f} USD)")

    # Save trades
    if trades:
        pd.DataFrame(trades).to_csv("demo_live_trades.csv", index=False)
        print("Demo trades saved to demo_live_trades.csv")
    else:
        print("No trades executed in demo.")

if __name__ == "__main__":
    main()
