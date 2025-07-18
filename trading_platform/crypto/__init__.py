"""
Crypto Trading Module
====================

Cryptocurrency trading functionality with CCXT integration.
"""

from .crypto_trader import CryptoTrader
from .asset_manager import CryptoAssetManager

__all__ = ['CryptoTrader', 'CryptoAssetManager']