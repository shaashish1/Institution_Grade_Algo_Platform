import backtrader as bt
from src.strategies.sma_cross import SmaCross

def run_backtest(data, cash=10000):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)
    cerebro.adddata(bt.feeds.PandasData(dataname=data))
    cerebro.broker.setcash(cash)
    cerebro.run()
    cerebro.plot()
