from tradingview_scraper import TradingView

def scrape_ideas(symbol):
    tv = TradingView()
    return tv.get_ideas(symbol=symbol)
