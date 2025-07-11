@echo off
REM Unified Trading Platform Launcher
REM Supports both crypto and stock trading

echo.
echo ==================================================================================
echo         🚀 AlgoProject - Unified Trading Platform Launcher
echo ==================================================================================
echo.
echo 💰 Crypto Trading: 100+ exchanges via CCXT
echo 📈 Stock Trading: NSE/BSE via Fyers API  
echo 🏠 Personal Laptop Edition - Full Functionality!
echo.
echo Starting unified trading platform...
echo.

REM Check if virtual environment exists and activate it
if exist "venv\Scripts\activate.bat" (
    echo 🔒 Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  Virtual environment not found - using system Python
)

REM Check if trading_launcher.py exists
if exist "trading_launcher.py" (
    echo 🚀 Launching unified trading platform...
    python trading_launcher.py
) else (
    echo ❌ trading_launcher.py not found!
    echo 💡 Please run setup_complete.bat first
    pause
)

echo.
echo 👋 Trading session ended
pause
