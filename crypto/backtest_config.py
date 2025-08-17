# Optimal Crypto Backtesting Configuration
# Generated: 2025-07-15 18:56:52
# Based on maximum available data analysis

CRYPTO_BACKTEST_CONFIG = {
    # Maximum available data per timeframe
    'max_data_available': {
        '1m': {
            'max_bars': 720,
            'recommended_bars': 720,
            'time_coverage_days': 0,
            'suitability': "LIMITED - suitable for quick tests only"
        },
        '5m': {
            'max_bars': 720,
            'recommended_bars': 720,
            'time_coverage_days': 2,
            'suitability': "LIMITED - suitable for quick tests only"
        },
        '15m': {
            'max_bars': 720,
            'recommended_bars': 720,
            'time_coverage_days': 7,
            'suitability': "FAIR - limited historical depth"
        },
        '30m': {
            'max_bars': 720,
            'recommended_bars': 720,
            'time_coverage_days': 14,
            'suitability': "FAIR - limited historical depth"
        },
        '1h': {
            'max_bars': 720,
            'recommended_bars': 720,
            'time_coverage_days': 29,
            'suitability': "FAIR - consider longer timeframes"
        },
        '4h': {
            'max_bars': 720,
            'recommended_bars': 720,
            'time_coverage_days': 119,
            'suitability': "FAIR - limited long-term data"
        },
        '1d': {
            'max_bars': 720,
            'recommended_bars': 720,
            'time_coverage_days': 719,
            'suitability': "GOOD for position trading"
        },
    },
    
    # Recommended configurations by trading style
    'trading_styles': {
        'scalping': {
            'timeframes': ['1m', '5m'],
            'min_bars': 1000,
            'ideal_bars': 5000,
            'max_bars': 10000
        },
        'day_trading': {
            'timeframes': ['15m', '30m'],
            'min_bars': 500,
            'ideal_bars': 2000,
            'max_bars': 10000
        },
        'swing_trading': {
            'timeframes': ['1h', '2h', '4h'],
            'min_bars': 200,
            'ideal_bars': 1000,
            'max_bars': 5000
        },
        'position_trading': {
            'timeframes': ['4h', '1d'],
            'min_bars': 100,
            'ideal_bars': 500,
            'max_bars': 2000
        }
    },
    
    # Exchange preferences
    'exchanges': {
        'primary': 'kraken',      # Most stable
        'secondary': 'binance',   # High volume
        'tertiary': 'coinbase'    # Major pairs
    },
    
    # Symbol recommendations
    'symbols': {
        'major_pairs': ['BTC/USDT', 'ETH/USDT', 'BNB/USDT'],
        'altcoins': ['ADA/USDT', 'SOL/USDT', 'DOT/USDT', 'AVAX/USDT'],
        'test_symbol': 'BTC/USDT'  # Most reliable for testing
    }
}

# Quick access functions
def get_max_bars(timeframe):
    '''Get maximum available bars for a timeframe'''
    return CRYPTO_BACKTEST_CONFIG['max_data_available'][timeframe]['max_bars']

def get_recommended_bars(timeframe):
    '''Get recommended bars for optimal performance'''
    return CRYPTO_BACKTEST_CONFIG['max_data_available'][timeframe]['recommended_bars']

def get_config_for_style(trading_style):
    '''Get configuration for a specific trading style'''
    return CRYPTO_BACKTEST_CONFIG['trading_styles'][trading_style]
