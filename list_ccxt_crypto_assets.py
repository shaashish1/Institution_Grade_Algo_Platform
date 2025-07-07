import ccxt
import os
import pandas as pd

def list_kraken_symbols():
    os.environ["REQUESTS_CA_BUNDLE"] = ""
    os.environ["CURL_CA_BUNDLE"] = ""
    exchange = ccxt.kraken()
    exchange.session.verify = False
    markets = exchange.load_markets()
    # Kraken symbols are like 'BTC/USD', 'ETH/USD', etc.
    symbols = [s for s in markets if markets[s]['spot'] and '/' in s]
    # Filter for common USD/EUR pairs and ensure format is correct for Kraken
    crypto_usd = [s for s in symbols if s.endswith('/USD') or s.endswith('/EUR')]
    return crypto_usd

if __name__ == "__main__":
    try:
        symbols = list_kraken_symbols()
        print("Sample of available crypto assets on Kraken (spot):")
        for s in symbols[:50]:
            print(s)
        print(f"\nTotal symbols: {len(symbols)}")
        # Optional: Save to CSV for direct use
        pd.DataFrame({"symbol": symbols}).to_csv("crypto_assets.csv", index=False)
        print("Saved all Kraken spot USD/EUR pairs to crypto_assets.csv")
    except Exception as e:
        print("Error fetching symbols from Kraken:", e)
        print("If you are behind a proxy or have SSL issues, check your network or try running with VPN.")
