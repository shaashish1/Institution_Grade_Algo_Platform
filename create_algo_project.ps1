param(
    [string]$BaseDir = "C:\vscode\AlgoProject"
)

Write-Host "Creating project at $BaseDir..." -ForegroundColor Cyan
New-Item -Path $BaseDir -ItemType Directory -Force | Out-Null

# Create folders
$folders = @("src", "src\strategies", "tests")
foreach ($f in $folders) {
    New-Item -Path (Join-Path $BaseDir $f) -ItemType Directory -Force | Out-Null
}

# Create file contents
Set-Content "$BaseDir\.gitignore" @"
__pycache__/
algo_env/
*.py[cod]
build/
dist/
*.egg-info/
*.log
"@

Set-Content "$BaseDir\LICENSE" @"
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge...
"@

Set-Content "$BaseDir\requirements.txt" @"
ccxt==3.0.59
pandas==1.5.3
numpy==1.26.0
requests==2.30.0
tradingview_ta==3.2.6
backtrader==1.9.76.123
tvdatafeed @ git+https://github.com/rongardF/tvdatafeed.git
tradingview-scraper==0.0.1
"@

Set-Content "$BaseDir\setup.py" @"
from setuptools import setup, find_packages

setup(
    name='AlgoProject',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'ccxt==3.0.59',
        'pandas==1.5.3',
        'numpy==1.26.0',
        'requests==2.30.0',
        'tradingview_ta==3.2.6',
        'backtrader==1.9.76.123',
        'tvdatafeed @ git+https://github.com/rongardF/tvdatafeed.git',
        'tradingview-scraper==0.0.1'
    ],
    entry_points={
        'console_scripts': [
            'fetch_data=src.data_acquisition:fetch_data',
            'analyze_symbol=src.technical_analysis:analyze_symbol',
            'scrape_ideas=src.web_scraper:scrape_ideas',
            'run_backtest=src.backtest:run_backtest',
            'scan_symbols=src.scanner:scan_symbols'
        ]
    }
)
"@

$srcFiles = @{
    "src\data_acquisition.py" = @"
from tvDatafeed import TvDatafeed, Interval

def fetch_data(symbol, exchange, interval, bars):
    tv = TvDatafeed()
    return tv.get_hist(symbol=symbol, exchange=exchange, interval=interval, n_bars=bars)
"@
    "src\technical_analysis.py" = @"
from tradingview_ta import TA_Handler, Interval

def analyze_symbol(symbol, exchange, interval):
    handler = TA_Handler(symbol=symbol, exchange=exchange, interval=interval)
    return handler.get_analysis().indicators
"@
    "src\web_scraper.py" = @"
from tradingview_scraper import TradingView

def scrape_ideas(symbol):
    tv = TradingView()
    return tv.get_ideas(symbol=symbol)
"@
    "src\scanner.py" = @"
from tradingview_ta import TA_Handler, Interval

def scan_symbols(symbols, exchange, interval, rsi_threshold):
    buy_signals = []
    for symbol in symbols:
        handler = TA_Handler(symbol=symbol, exchange=exchange, interval=interval)
        ind = handler.get_analysis().indicators
        if ind.get('RSI', 100) < rsi_threshold:
            buy_signals.append(symbol)
    return buy_signals
"@
    "src\backtest.py" = @"
import backtrader as bt
from src.strategies.sma_cross import SmaCross

def run_backtest(data, cash=10000):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)
    cerebro.adddata(bt.feeds.PandasData(dataname=data))
    cerebro.broker.setcash(cash)
    cerebro.run()
    cerebro.plot()
"@
    "src\strategies\sma_cross.py" = @"
import backtrader as bt

class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1 = bt.ind.SMA(period=10)
        sma2 = bt.ind.SMA(period=30)
        self.signal_add(bt.SIGNAL_LONG, bt.ind.CrossOver(sma1, sma2))
"@
    "tests\test_main.py" = @"
import unittest

class TestPlaceholder(unittest.TestCase):
    def test_true(self):
        self.assertTrue(True)
"@
}

foreach ($path in $srcFiles.Keys) {
    $full = Join-Path $BaseDir $path
    Set-Content -Path $full -Value $srcFiles[$path]
}

Write-Host "Project created successfully at $BaseDir" -ForegroundColor Green
