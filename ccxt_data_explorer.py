import ccxt
import pandas as pd
from datetime import datetime, timedelta, timezone

def print_market_info(exchange, symbol):
    market = exchange.market(symbol)
    print(f"Market info for {symbol}:")
    for k, v in market.items():
        print(f"  {k}: {v}")

def get_ohlcv_info(exchange, symbol, timeframe="1d", limit=1000):
    print(f"\nFetching OHLCV for {symbol} ({timeframe}, limit={limit})...")
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    print(f"  Data points: {len(df)}")
    print(f"  Oldest: {df['datetime'].min()}  Newest: {df['datetime'].max()}")
    print(f"  Columns: {list(df.columns)}")
    print(df.head(3))
    print(df.tail(3))
    return df

def get_orderbook_info(exchange, symbol):
    print(f"\nOrderbook for {symbol}:")
    orderbook = exchange.fetch_order_book(symbol)
    print(f"  Bids (top 5): {orderbook['bids'][:5]}")
    print(f"  Asks (top 5): {orderbook['asks'][:5]}")
    print(f"  Best bid: {orderbook['bids'][0][0] if orderbook['bids'] else None}")
    print(f"  Best ask: {orderbook['asks'][0][0] if orderbook['asks'] else None}")

def get_ticker_info(exchange, symbol):
    print(f"\nTicker for {symbol}:")
    ticker = exchange.fetch_ticker(symbol)
    for k in ["bid", "ask", "last", "open", "high", "low", "close", "baseVolume", "quoteVolume", "percentage", "change"]:
        print(f"  {k}: {ticker.get(k)}")

def get_trades_info(exchange, symbol, limit=10):
    print(f"\nRecent trades for {symbol}:")
    # Kraken requires fetchTradesWarning option to be set to True to allow limit param
    if hasattr(exchange, "options"):
        exchange.options["fetchTradesWarning"] = True
    try:
        trades = exchange.fetch_trades(symbol, limit=limit)
        for t in trades:
            print(f"  {t}")
    except Exception as e:
        print(f"  Error fetching trades: {e}")

def get_exchange_info(exchange):
    print(f"Exchange: {exchange.name}")
    print(f"  Time: {exchange.iso8601(exchange.milliseconds())}")
    print(f"  Markets loaded: {len(exchange.markets)}")
    print(f"  Rate limits: {exchange.rateLimit} ms per request")
    print(f"  Has fetch_trades: {exchange.has.get('fetchTrades')}")
    print(f"  Has fetch_order_book: {exchange.has.get('fetchOrderBook')}")
    print(f"  Has fetch_ohlcv: {exchange.has.get('fetchOHLCV')}")
    print(f"  Has fetch_ticker: {exchange.has.get('fetchTicker')}")
    print(f"  Has fetch_balance: {exchange.has.get('fetchBalance')}")
    print(f"  Has create_order: {exchange.has.get('createOrder')}")
    print(f"  Has fetch_open_orders: {exchange.has.get('fetchOpenOrders')}")
    print(f"  Has fetch_closed_orders: {exchange.has.get('fetchClosedOrders')}")

def main():
    # You can change to any supported exchange, e.g., binance, coinbasepro, bybit, etc.
    # To use API keys, set them here:
    exchange = ccxt.kraken({
        "apiKey": "YOUR_API_KEY_HERE",
        "secret": "YOUR_API_SECRET_HERE",
        # "password": "YOUR_API_PASSWORD_HERE",  # if required by the exchange
    })
    exchange.load_markets()
    get_exchange_info(exchange)

    # List all spot symbols
    spot_symbols = [s for s in exchange.symbols if exchange.markets[s]['spot']]
    print(f"\nTotal spot symbols: {len(spot_symbols)}")
    print("Sample symbols:", spot_symbols[:10])

    # Pick a symbol to explore (change as needed)
    symbol = "BTC/USD" if "BTC/USD" in spot_symbols else spot_symbols[0]
    print_market_info(exchange, symbol)

    # Get OHLCV data (daily and 5m)
    get_ohlcv_info(exchange, symbol, timeframe="1d", limit=1000)
    get_ohlcv_info(exchange, symbol, timeframe="5m", limit=1000)

    # Get orderbook
    get_orderbook_info(exchange, symbol)

    # Get ticker info
    get_ticker_info(exchange, symbol)

    # Get recent trades
    get_trades_info(exchange, symbol, limit=5)

    # Show how to fetch open/closed orders (requires authentication)
    print("\nTo fetch open/closed orders or place trades, you must set your API keys and enable trading permissions.")

if __name__ == "__main__":
    main()
