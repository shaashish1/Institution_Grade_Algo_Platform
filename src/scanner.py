from tradingview_ta import TA_Handler, Interval

def scan_symbols(symbols, exchange, interval, rsi_threshold):
    buy_signals = []
    for symbol in symbols:
        handler = TA_Handler(symbol=symbol, exchange=exchange, interval=interval)
        ind = handler.get_analysis().indicators
        if ind.get('RSI', 100) < rsi_threshold:
            buy_signals.append(symbol)
    return buy_signals
