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
