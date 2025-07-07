from tradingview_ta import TA_Handler, Interval

def analyze_symbol(symbol, exchange, interval):
    handler = TA_Handler(symbol=symbol, exchange=exchange, interval=interval)
    return handler.get_analysis().indicators
