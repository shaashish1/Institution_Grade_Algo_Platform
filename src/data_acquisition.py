from tvDatafeed import TvDatafeed, Interval

def fetch_data(symbol, exchange, interval, bars):
    tv = TvDatafeed()
    return tv.get_hist(symbol=symbol, exchange=exchange, interval=interval, n_bars=bars)
