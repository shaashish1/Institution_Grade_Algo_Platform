"""
Crypto Asset Manager
===================

Manages cryptocurrency assets and symbols.
"""

import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any

class CryptoAssetManager:
    """Manages crypto assets and symbols"""
    
    def __init__(self):
        self.assets_file = Path("data/crypto_assets.json")
        self.assets = self.load_assets()
    
    def load_assets(self) -> List[Dict[str, Any]]:
        """Load crypto assets from file"""
        try:
            if self.assets_file.exists():
                with open(self.assets_file, 'r') as f:
                    return json.load(f)
            else:
                # Create default assets
                return self.create_default_assets()
        except Exception as e:
            print(f"❌ Error loading assets: {e}")
            return self.create_default_assets()
    
    def create_default_assets(self) -> List[Dict[str, Any]]:
        """Create default crypto assets"""
        default_assets = [
            {
                "symbol": "BTC/USDT",
                "name": "Bitcoin",
                "base": "BTC",
                "quote": "USDT",
                "exchange": "binance",
                "active": True,
                "category": "major",
                "market_cap_rank": 1
            },
            {
                "symbol": "ETH/USDT",
                "name": "Ethereum",
                "base": "ETH",
                "quote": "USDT",
                "exchange": "binance",
                "active": True,
                "category": "major",
                "market_cap_rank": 2
            },
            {
                "symbol": "BNB/USDT",
                "name": "Binance Coin",
                "base": "BNB",
                "quote": "USDT",
                "exchange": "binance",
                "active": True,
                "category": "major",
                "market_cap_rank": 4
            },
            {
                "symbol": "ADA/USDT",
                "name": "Cardano",
                "base": "ADA",
                "quote": "USDT",
                "exchange": "binance",
                "active": True,
                "category": "altcoin",
                "market_cap_rank": 8
            },
            {
                "symbol": "SOL/USDT",
                "name": "Solana",
                "base": "SOL",
                "quote": "USDT",
                "exchange": "binance",
                "active": True,
                "category": "altcoin",
                "market_cap_rank": 5
            },
            {
                "symbol": "DOT/USDT",
                "name": "Polkadot",
                "base": "DOT",
                "quote": "USDT",
                "exchange": "binance",
                "active": True,
                "category": "altcoin",
                "market_cap_rank": 12
            },
            {
                "symbol": "MATIC/USDT",
                "name": "Polygon",
                "base": "MATIC",
                "quote": "USDT",
                "exchange": "binance",
                "active": True,
                "category": "altcoin",
                "market_cap_rank": 15
            },
            {
                "symbol": "AVAX/USDT",
                "name": "Avalanche",
                "base": "AVAX",
                "quote": "USDT",
                "exchange": "binance",
                "active": True,
                "category": "altcoin",
                "market_cap_rank": 18
            },
            {
                "symbol": "LINK/USDT",
                "name": "Chainlink",
                "base": "LINK",
                "quote": "USDT",
                "exchange": "binance",
                "active": True,
                "category": "altcoin",
                "market_cap_rank": 20
            },
            {
                "symbol": "UNI/USDT",
                "name": "Uniswap",
                "base": "UNI",
                "quote": "USDT",
                "exchange": "binance",
                "active": True,
                "category": "defi",
                "market_cap_rank": 25
            }
        ]
        
        # Save default assets
        self.save_assets(default_assets)
        return default_assets
    
    def save_assets(self, assets: List[Dict[str, Any]]):
        """Save assets to file"""
        try:
            # Create data directory if it doesn't exist
            self.assets_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.assets_file, 'w') as f:
                json.dump(assets, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving assets: {e}")
    
    def get_available_assets(self) -> List[Dict[str, Any]]:
        """Get all available crypto assets"""
        return [asset for asset in self.assets if asset.get('active', True)]
    
    def get_assets_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get assets by category"""
        return [
            asset for asset in self.assets 
            if asset.get('category', '').lower() == category.lower() and asset.get('active', True)
        ]
    
    def get_major_cryptos(self) -> List[Dict[str, Any]]:
        """Get major cryptocurrencies"""
        return self.get_assets_by_category('major')
    
    def get_altcoins(self) -> List[Dict[str, Any]]:
        """Get altcoins"""
        return self.get_assets_by_category('altcoin')
    
    def get_defi_tokens(self) -> List[Dict[str, Any]]:
        """Get DeFi tokens"""
        return self.get_assets_by_category('defi')
    
    def search_assets(self, query: str) -> List[Dict[str, Any]]:
        """Search assets by symbol or name"""
        query = query.lower()
        return [
            asset for asset in self.assets
            if query in asset.get('symbol', '').lower() or 
               query in asset.get('name', '').lower() or
               query in asset.get('base', '').lower()
        ]
    
    def add_asset(self, symbol: str, name: str, base: str, quote: str, 
                  exchange: str = 'binance', category: str = 'altcoin') -> bool:
        """Add a new crypto asset"""
        try:
            new_asset = {
                "symbol": symbol,
                "name": name,
                "base": base,
                "quote": quote,
                "exchange": exchange,
                "active": True,
                "category": category,
                "market_cap_rank": 999
            }
            
            # Check if asset already exists
            existing = next((a for a in self.assets if a['symbol'] == symbol), None)
            if existing:
                print(f"⚠️  Asset {symbol} already exists")
                return False
            
            self.assets.append(new_asset)
            self.save_assets(self.assets)
            print(f"✅ Added asset: {symbol} - {name}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding asset: {e}")
            return False
    
    def remove_asset(self, symbol: str) -> bool:
        """Remove a crypto asset"""
        try:
            original_count = len(self.assets)
            self.assets = [a for a in self.assets if a['symbol'] != symbol]
            
            if len(self.assets) < original_count:
                self.save_assets(self.assets)
                print(f"✅ Removed asset: {symbol}")
                return True
            else:
                print(f"⚠️  Asset {symbol} not found")
                return False
                
        except Exception as e:
            print(f"❌ Error removing asset: {e}")
            return False
    
    def get_asset_info(self, symbol: str) -> Dict[str, Any]:
        """Get detailed info for a specific asset"""
        asset = next((a for a in self.assets if a['symbol'] == symbol), None)
        if asset:
            return asset
        else:
            return {}
    
    def get_symbols_list(self) -> List[str]:
        """Get list of all active symbols"""
        return [asset['symbol'] for asset in self.get_available_assets()]
    
    def get_base_currencies(self) -> List[str]:
        """Get list of unique base currencies"""
        bases = set()
        for asset in self.get_available_assets():
            bases.add(asset.get('base', ''))
        return sorted(list(bases))
    
    def get_quote_currencies(self) -> List[str]:
        """Get list of unique quote currencies"""
        quotes = set()
        for asset in self.get_available_assets():
            quotes.add(asset.get('quote', ''))
        return sorted(list(quotes))
    
    def export_to_csv(self, filename: str = None) -> str:
        """Export assets to CSV file"""
        try:
            if not filename:
                filename = f"crypto_assets_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            df = pd.DataFrame(self.assets)
            filepath = Path("data") / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            df.to_csv(filepath, index=False)
            print(f"✅ Assets exported to: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error exporting assets: {e}")
            return ""
    
    def import_from_csv(self, filepath: str) -> bool:
        """Import assets from CSV file"""
        try:
            df = pd.read_csv(filepath)
            new_assets = df.to_dict('records')
            
            # Validate required fields
            required_fields = ['symbol', 'name', 'base', 'quote']
            for asset in new_assets:
                for field in required_fields:
                    if field not in asset:
                        print(f"❌ Missing required field '{field}' in import data")
                        return False
            
            self.assets = new_assets
            self.save_assets(self.assets)
            print(f"✅ Imported {len(new_assets)} assets from {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Error importing assets: {e}")
            return False