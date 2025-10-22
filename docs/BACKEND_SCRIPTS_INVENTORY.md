# Backend Scripts Inventory & Documentation

**Last Updated**: October 22, 2025  
**Status**: Complete Inventory

---

## 📊 Overview

This document lists all backend scripts, their capabilities, data sources, and usage.

**Total Scripts**: 15+  
**Data Sources**: NSE (FREE), FYERS (Paid), CCXT (200+ Exchanges)  
**Languages**: Python 3.14

---

## 🔥 API Scripts (`api/`)

### 1. **main.py** - Main FastAPI Application
**Path**: `api/main.py`  
**Status**: ✅ Operational  
**Purpose**: Core FastAPI server with all endpoints

**Features**:
- Health check endpoint
- Portfolio management
- Backtesting API
- Strategy management
- Trading control
- WebSocket support
- CORS enabled

**Endpoints** (30+):
```python
GET  /health
GET  /portfolio
POST /backtest
GET  /strategies
GET  /positions
POST /orders/create
GET  /orders/history
# ... and more
```

**Usage**:
```bash
cd api
uvicorn main:app --reload --port 8000
```

---

### 2. **market_data_api.py** - Market Data Endpoints
**Path**: `api/market_data_api.py`  
**Status**: ✅ Operational  
**Purpose**: Real-time market data API (NSE & Crypto)

**Data Sources**:
- PRIMARY: NSE Free Provider (no credentials needed)
- SECONDARY: FYERS Provider (optional)
- TERTIARY: CCXT for crypto

**Features**:
- Real-time NSE indices (NIFTY 50, BANK NIFTY, etc.)
- Stock quotes (NSE/BSE)
- Top gainers/losers
- Market status (open/closed)
- Multiple exchange support

**Endpoints**:
```python
GET  /api/market/health          # Health check
GET  /api/market/indices          # NIFTY indices
POST /api/market/quotes           # Stock quotes
GET  /api/market/data             # Market data
GET  /api/market/positions        # Current positions
GET  /api/market-data/provider-status  # Data source status
```

**Data Capabilities**:
- ✅ NIFTY 50 (real-time, FREE)
- ✅ BANK NIFTY (real-time, FREE)
- ✅ NSE stocks (real-time quotes)
- ✅ Top 10 gainers/losers
- ✅ Market open/close status

**Usage**:
```python
import requests

# Get NIFTY indices
response = requests.get('http://localhost:8000/api/market/indices')
indices = response.json()

# Get stock quotes
response = requests.post('http://localhost:8000/api/market/quotes', 
    json={'symbols': ['RELIANCE', 'TCS'], 'exchange': 'NSE'})
quotes = response.json()
```

---

### 3. **settings_api.py** - Exchange Settings
**Path**: `api/settings_api.py`  
**Status**: ✅ Operational  
**Purpose**: Manage exchange configurations

**Features**:
- Store exchange API keys
- Manage credentials
- Configure trading accounts
- Enable/disable exchanges

**Endpoints**:
```python
GET    /api/settings/exchanges          # List all exchanges
POST   /api/settings/exchanges          # Add exchange
PUT    /api/settings/exchanges/{name}   # Update exchange
DELETE /api/settings/exchanges/{name}   # Remove exchange
```

**Supported Exchanges**:
- FYERS (NSE/BSE stocks)
- Binance, Coinbase, Kraken (Crypto)
- 200+ exchanges via CCXT

---

### 4. **user_preferences_api.py** - User Preferences
**Path**: `api/user_preferences_api.py`  
**Status**: ✅ Operational  
**Purpose**: Store user settings (Market, Mode selection)

**Features**:
- Market preference (NSE/Crypto)
- Mode preference (Backtest/Paper/Live)
- localStorage sync
- Persistence across sessions

**Endpoints**:
```python
GET  /api/user/preferences         # Get preferences
POST /api/user/preferences         # Update preferences
GET  /api/user/preferences/status  # Check status
```

**Storage**: `user_preferences.json` (will be DB later)

---

### 5. **ccxt_service.py** - Crypto Exchange Service
**Path**: `api/ccxt_service.py`  
**Status**: ✅ Operational  
**Purpose**: Unified interface for 200+ crypto exchanges

**Features**:
- Multi-exchange support
- Real-time crypto data
- Order execution
- Balance checking
- Historical data

**Supported Exchanges**: 200+ including:
- Binance, Coinbase, Kraken
- Bybit, OKX, Huobi
- KuCoin, Gate.io, Bitfinex

**Data Capabilities**:
- ✅ Real-time crypto prices
- ✅ Order book data
- ✅ Historical OHLCV
- ✅ 24h volume
- ✅ Market cap data

---

### 6. **fyers_user_service.py** - FYERS User Management
**Path**: `api/fyers_user_service.py`  
**Status**: ✅ Operational (optional)  
**Purpose**: Manage FYERS user accounts

**Features**:
- Store FYERS credentials
- Generate access tokens
- User authentication
- Account management

**Note**: Optional - only needed for live NSE/BSE trading

---

### 7. **fyers_data_service.py** - FYERS Data Provider
**Path**: `api/fyers_data_service.py`  
**Status**: ✅ Operational (optional)  
**Purpose**: FYERS-specific data fetching

**Features**:
- NSE/BSE live data
- Historical data
- Order placement
- Position tracking

**Note**: Requires FYERS subscription (paid)

---

## 📈 Stock Scripts (`stocks/`)

### 8. **nse_free_data_provider.py** ⭐ PRIMARY
**Path**: `stocks/nse_free_data_provider.py`  
**Status**: ✅ Operational  
**Purpose**: FREE real-time NSE data (NO CREDENTIALS NEEDED)

**Features**:
- Real-time NSE indices
- Live stock quotes
- Top gainers/losers
- Market status
- Session management

**Data Sources**:
1. NSE India API (primary)
2. Yahoo Finance (backup)
3. Mock data (fallback)

**Data Capabilities**:
```python
# Available Methods
get_nifty_indices()          # NIFTY 50, BANK NIFTY, etc.
get_quote(symbols, exchange) # Stock quotes
get_top_gainers(limit=10)    # Top gainers
get_top_losers(limit=10)     # Top losers
get_market_status()          # Open/closed status
```

**Example Data**:
```json
{
  "NIFTY 50": {
    "last": 25868.6,
    "change": 25.8,
    "pChange": 0.1
  },
  "NIFTY BANK": {
    "last": 58007.2,
    "change": -22.3,
    "pChange": -0.04
  }
}
```

**Usage**:
```python
from stocks.nse_free_data_provider import NSEFreeDataProvider

provider = NSEFreeDataProvider()
indices = provider.get_nifty_indices()
quotes = provider.get_quote(['RELIANCE', 'TCS'], 'NSE')
```

---

### 9. **fyers_data_provider.py** - FYERS NSE/BSE Data
**Path**: `stocks/fyers_data_provider.py`  
**Status**: ✅ Operational (optional)  
**Purpose**: FYERS API integration for NSE/BSE

**Features**:
- Real-time NSE/BSE data
- Historical data
- Order execution
- Position management

**Note**: Requires FYERS subscription + API credentials

---

### 10. **live_nse_quotes.py** - Live NSE Quotes
**Path**: `stocks/live_nse_quotes.py`  
**Status**: ✅ Operational  
**Purpose**: Fetch live NSE stock quotes

**Features**:
- Real-time quotes
- Multiple symbols
- Fast response

---

### 11. **data_acquisition.py** - Generic Data Fetcher
**Path**: `stocks/data_acquisition.py`  
**Status**: ✅ Operational  
**Purpose**: Unified data fetching interface

**Features**:
- Multi-source data fetching
- Fallback mechanisms
- Caching

---

## 🪙 Crypto Scripts (`crypto/`)

### 12. **crypto_assets_manager.py**
**Path**: `crypto/crypto_assets_manager.py`  
**Status**: ✅ Operational  
**Purpose**: Manage crypto asset lists

**Features**:
- Load crypto symbols
- Symbol validation
- Asset categorization

---

### 13. **crypto_symbol_manager.py**
**Path**: `crypto/crypto_symbol_manager.py`  
**Status**: ✅ Operational  
**Purpose**: Crypto symbol management

---

### 14. **data_acquisition.py** (Crypto)
**Path**: `crypto/data_acquisition.py`  
**Status**: ✅ Operational  
**Purpose**: Fetch crypto market data

**Features**:
- Multi-exchange support
- Historical data
- Real-time prices

---

## 🧪 Test Scripts

### 15. **test_nse_free_data.py**
**Path**: `test_nse_free_data.py`  
**Status**: ✅ Operational  
**Purpose**: Test NSE Free Data Provider

**Usage**:
```bash
python test_nse_free_data.py
```

**Output**: Validates NSE data fetching and displays results

---

## 📊 Data Capabilities Summary

### **NSE Market Data** (FREE - No Credentials)
✅ **Indices**: NIFTY 50, BANK NIFTY, IT, AUTO, PHARMA, etc.  
✅ **Stocks**: All NSE listed stocks  
✅ **Top Movers**: Gainers, losers, volume leaders  
✅ **Market Status**: Open/closed, session times  
✅ **Real-time Quotes**: Last price, change, volume  

**Refresh Rate**: 5-10 seconds  
**Cost**: FREE ✅  
**Credentials**: NOT NEEDED ✅

---

### **NSE via FYERS** (Paid - Optional)
✅ **Historical Data**: 1min to 1day  
✅ **Order Execution**: Market, Limit, Stop orders  
✅ **Position Management**: Live positions  
✅ **Account Info**: Balance, margins  

**Cost**: FYERS subscription required  
**Use Case**: Live trading only

---

### **Crypto Data** (FREE)
✅ **200+ Exchanges**: Binance, Coinbase, etc.  
✅ **Real-time Prices**: BTC, ETH, all major coins  
✅ **Historical Data**: OHLCV, tick data  
✅ **Order Books**: Bid/ask spreads  
✅ **24h Stats**: Volume, market cap, changes  

**Cost**: FREE (API rate limits apply)  
**Credentials**: Optional (for trading only)

---

## 🚀 Quick Start Guide

### **1. Start Backend Server**
```bash
cd C:\Users\NEELAM\Institution_Grade_Algo_Platform
python start_backend.py
```

Server starts on: http://localhost:8000  
API Docs: http://localhost:8000/docs

---

### **2. Test NSE Data**
```bash
python test_nse_free_data.py
```

Expected output:
```json
{
  "provider_status": "operational",
  "data_source": "NSE India API",
  "indices": {
    "NIFTY 50": 25868.6,
    "NIFTY BANK": 58007.2
  }
}
```

---

### **3. Test API Endpoints**
```bash
# Health check
curl http://localhost:8000/health

# Get indices
curl http://localhost:8000/api/market/indices

# Get quotes
curl -X POST http://localhost:8000/api/market/quotes \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["RELIANCE"], "exchange": "NSE"}'
```

---

## 📚 API Documentation

**Swagger UI**: http://localhost:8000/docs  
**ReDoc**: http://localhost:8000/redoc

---

## 🔧 Configuration

### **Exchange Configuration**
File: `api/data/fyers_users.json`

```json
{
  "exchanges": [
    {
      "name": "FYERS",
      "type": "stocks",
      "credentials": {
        "client_id": "YOUR_CLIENT_ID",
        "access_token": "YOUR_TOKEN"
      }
    }
  ]
}
```

---

### **User Preferences**
File: `user_preferences.json`

```json
{
  "market": "NSE",
  "mode": "Paper",
  "timestamp": "2025-10-22T12:00:00"
}
```

---

## ✅ Script Status Summary

| Script | Status | Credentials Needed | Cost | Primary Use |
|--------|--------|-------------------|------|-------------|
| NSE Free Provider | ✅ Operational | ❌ NO | FREE | Market data |
| FYERS Provider | ✅ Optional | ✅ YES | Paid | Live trading |
| CCXT Service | ✅ Operational | ❌ NO* | FREE | Crypto data |
| Market Data API | ✅ Operational | ❌ NO | FREE | API endpoint |
| Settings API | ✅ Operational | N/A | FREE | Configuration |
| User Preferences | ✅ Operational | N/A | FREE | User settings |

*Credentials only needed for crypto trading, not data fetching

---

## 🎯 Recommended Setup

### **For Development/Testing**:
✅ Use NSE Free Provider (no credentials)  
✅ Use CCXT for crypto (no credentials)  
✅ Paper trading mode only  

**Total Cost**: $0 ✅

---

### **For Live Trading**:
✅ Configure FYERS (for NSE stocks)  
✅ Configure Binance/Coinbase (for crypto)  
✅ Enable Live mode  

**Cost**: Exchange subscription fees

---

## 📞 Support

**Documentation**: `docs/` folder  
**API Docs**: http://localhost:8000/docs  
**GitHub**: https://github.com/shaashish1/Institution_Grade_Algo_Platform

---

**Status**: ✅ All scripts documented and operational  
**Last Updated**: October 22, 2025
