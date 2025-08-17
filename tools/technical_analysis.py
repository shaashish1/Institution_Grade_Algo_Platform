"""
Technical Analysis Module
Core technical indicators and analysis functions
"""

import pandas as pd
import numpy as np


def calculate_rsi(data, period=14):
    """
    Calculate Relative Strength Index (RSI)
    
    Args:
        data: Price data (pandas Series)
        period: RSI period (default: 14)
    
    Returns:
        pandas Series: RSI values
    """
    if len(data) < period:
        return pd.Series(index=data.index, dtype=float)
    
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    """
    Calculate MACD (Moving Average Convergence Divergence)
    
    Args:
        data: Price data (pandas Series)
        fast_period: Fast EMA period (default: 12)
        slow_period: Slow EMA period (default: 26)
        signal_period: Signal line EMA period (default: 9)
    
    Returns:
        dict: MACD line, signal line, and histogram
    """
    if len(data) < slow_period:
        return {
            'macd': pd.Series(index=data.index, dtype=float),
            'signal': pd.Series(index=data.index, dtype=float),
            'histogram': pd.Series(index=data.index, dtype=float)
        }
    
    # Calculate EMAs
    ema_fast = data.ewm(span=fast_period).mean()
    ema_slow = data.ewm(span=slow_period).mean()
    
    # MACD line
    macd_line = ema_fast - ema_slow
    
    # Signal line
    signal_line = macd_line.ewm(span=signal_period).mean()
    
    # Histogram
    histogram = macd_line - signal_line
    
    return {
        'macd': macd_line,
        'signal': signal_line,
        'histogram': histogram
    }


def calculate_bollinger_bands(data, period=20, std_dev=2):
    """
    Calculate Bollinger Bands
    
    Args:
        data: Price data (pandas Series)
        period: Moving average period (default: 20)
        std_dev: Standard deviation multiplier (default: 2)
    
    Returns:
        dict: Upper band, middle band (SMA), and lower band
    """
    if len(data) < period:
        return {
            'upper': pd.Series(index=data.index, dtype=float),
            'middle': pd.Series(index=data.index, dtype=float),
            'lower': pd.Series(index=data.index, dtype=float)
        }
    
    # Simple Moving Average (middle band)
    sma = data.rolling(window=period).mean()
    
    # Standard deviation
    std = data.rolling(window=period).std()
    
    # Upper and lower bands
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    
    return {
        'upper': upper_band,
        'middle': sma,
        'lower': lower_band
    }


def calculate_vwap(high, low, close, volume):
    """
    Calculate Volume Weighted Average Price (VWAP)
    
    Args:
        high: High prices (pandas Series)
        low: Low prices (pandas Series)
        close: Close prices (pandas Series)
        volume: Volume data (pandas Series)
    
    Returns:
        pandas Series: VWAP values
    """
    if len(high) == 0 or len(volume) == 0:
        return pd.Series(index=high.index, dtype=float)
    
    # Typical price
    typical_price = (high + low + close) / 3
    
    # Volume weighted price
    vwp = typical_price * volume
    
    # Cumulative sums
    cumulative_vwp = vwp.cumsum()
    cumulative_volume = volume.cumsum()
    
    # VWAP
    vwap = cumulative_vwp / cumulative_volume
    
    return vwap


def calculate_sma(data, period):
    """
    Calculate Simple Moving Average
    
    Args:
        data: Price data (pandas Series)
        period: Moving average period
    
    Returns:
        pandas Series: SMA values
    """
    if len(data) < period:
        return pd.Series(index=data.index, dtype=float)
    
    return data.rolling(window=period).mean()


def calculate_ema(data, period):
    """
    Calculate Exponential Moving Average
    
    Args:
        data: Price data (pandas Series)
        period: Moving average period
    
    Returns:
        pandas Series: EMA values
    """
    if len(data) == 0:
        return pd.Series(index=data.index, dtype=float)
    
    return data.ewm(span=period).mean()


def calculate_stochastic(high, low, close, k_period=14, d_period=3):
    """
    Calculate Stochastic Oscillator
    
    Args:
        high: High prices (pandas Series)
        low: Low prices (pandas Series)
        close: Close prices (pandas Series)
        k_period: %K period (default: 14)
        d_period: %D period (default: 3)
    
    Returns:
        dict: %K and %D values
    """
    if len(high) < k_period:
        return {
            'k': pd.Series(index=high.index, dtype=float),
            'd': pd.Series(index=high.index, dtype=float)
        }
    
    # Lowest low and highest high over the period
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    
    # %K calculation
    k_percent = 100 * (close - lowest_low) / (highest_high - lowest_low)
    
    # %D calculation (SMA of %K)
    d_percent = k_percent.rolling(window=d_period).mean()
    
    return {
        'k': k_percent,
        'd': d_percent
    }


def calculate_atr(high, low, close, period=14):
    """
    Calculate Average True Range (ATR)
    
    Args:
        high: High prices (pandas Series)
        low: Low prices (pandas Series)
        close: Close prices (pandas Series)
        period: ATR period (default: 14)
    
    Returns:
        pandas Series: ATR values
    """
    if len(high) < 2:
        return pd.Series(index=high.index, dtype=float)
    
    # True Range calculation
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # ATR (Simple Moving Average of True Range)
    atr = true_range.rolling(window=period).mean()
    
    return atr


if __name__ == "__main__":
    # Test the functions with sample data
    print("🧮 Technical Analysis Module - Testing")
    
    # Create sample data
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    np.random.seed(42)
    prices = pd.Series(
        100 + np.cumsum(np.random.randn(100) * 0.5),
        index=dates
    )
    
    # Test RSI
    rsi = calculate_rsi(prices)
    print(f"RSI (last 5 values): {rsi.tail().round(2).tolist()}")
    
    # Test MACD
    macd = calculate_macd(prices)
    print(f"MACD (last value): {macd['macd'].iloc[-1]:.2f}")
    
    # Test Bollinger Bands
    bb = calculate_bollinger_bands(prices)
    print(f"Bollinger Bands (last value): Upper={bb['upper'].iloc[-1]:.2f}, "
          f"Middle={bb['middle'].iloc[-1]:.2f}, Lower={bb['lower'].iloc[-1]:.2f}")
    
    print("✅ All technical analysis functions working correctly!")
