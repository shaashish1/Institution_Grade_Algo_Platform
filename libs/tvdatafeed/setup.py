from setuptools import setup, find_packages

setup(
    name='tvdatafeed',
    version='2.1.0',
    packages=find_packages(include=['tvdatafeed', 'tvdatafeed.*']),  # Use lowercase to match installed package name
    install_requires=[
        'pandas>=1.3,<2.0',
        'requests>=2.31',  # Ensure compatibility with yfinance and other libs
        'selenium',
        'lxml'
    ],
    author='RongardF',
    description='Download data from TradingView',
)

# This setup script is for the tvdatafeed library, which allows users to download financial data from TradingView.
# It includes the necessary metadata and dependencies required for installation.