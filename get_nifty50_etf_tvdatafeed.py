from tvDatafeed import TvDatafeed
import pandas as pd

def get_nifty50_symbols():
    tv = TvDatafeed()
    # Nifty 50 stocks are all listed on NSE, get the list from TradingView
    # TradingView's NSE:NIFTY constituents as of July 2024
    nifty50 = [
        "RELIANCE", "HDFCBANK", "ICICIBANK", "INFY", "LT", "TCS", "KOTAKBANK", "ITC", "SBIN", "BHARTIARTL",
        "HINDUNILVR", "BAJFINANCE", "ASIANPAINT", "AXISBANK", "HCLTECH", "MARUTI", "SUNPHARMA", "TITAN",
        "ULTRACEMCO", "TATAMOTORS", "WIPRO", "NTPC", "POWERGRID", "ONGC", "JSWSTEEL", "TATASTEEL",
        "ADANIPORTS", "ADANIENT", "DIVISLAB", "EICHERMOT", "GRASIM", "HDFCLIFE", "HEROMOTOCO", "HINDALCO",
        "ICICIPRULI", "INDUSINDBK", "M&M", "NESTLEIND", "SBILIFE", "SHREECEM", "TECHM", "BPCL", "CIPLA",
        "COALINDIA", "DRREDDY", "BRITANNIA", "BAJAJFINSV", "APOLLOHOSP", "TATACONSUM", "BAJAJ-AUTO"
    ]
    return nifty50

def get_nse_etfs():
    tv = TvDatafeed()
    # Example: Get all ETFs from NSE (you can expand this list as needed)
    etfs = [
        "NIFTYBEES", "BANKBEES", "JUNIORBEES", "LIQUIDBEES", "GOLDBEES", "ICICINIFTY", "ICICIBANKNIFTY",
        "ICICINEXT50", "ICICILIQUID", "ICICIGOLD", "ICICISILVER", "ICICINV20", "ICICISENSEX"
    ]
    return etfs

if __name__ == "__main__":
    nifty50 = get_nifty50_symbols()
    etfs = get_nse_etfs()
    all_symbols = nifty50 + etfs
    df = pd.DataFrame({"symbol": all_symbols})
    df.to_csv("stock_assets.csv", index=False)
    print("Updated stock_assets.csv with Nifty 50 stocks and selected NSE ETFs.")
    print("Sample code to fetch 1-minute data for a symbol:")
    print("""
from tvDatafeed import TvDatafeed, Interval
tv = TvDatafeed()
data = tv.get_hist(symbol='RELIANCE', exchange='NSE', interval=Interval.in_1_minute, n_bars=100)
print(data.head())
""")
