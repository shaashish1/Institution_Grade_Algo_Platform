@echo off
REM Stock Trading Platform Launcher  
REM Focused on Indian stock market trading via Fyers API

echo.
echo ==================================================================================
echo         📈 AlgoProject - Stock Trading Platform Launcher
echo ==================================================================================
echo.
echo 🇮🇳 Indian Stock Market Trading
echo 📊 NSE/BSE access via Fyers API
echo 🏠 Personal Laptop Edition - Full API access!
echo.
echo Starting stock trading platform...
echo.

REM Check if virtual environment exists and activate it
if exist "venv\Scripts\activate.bat" (
    echo 🔒 Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  Virtual environment not found - using system Python
)

REM Check if stock_launcher.py exists
if exist "stock_launcher.py" (
    echo 🚀 Launching stock trading platform...
    python stock_launcher.py
) else (
    echo ❌ stock_launcher.py not found!
    echo 💡 Please run setup_complete.bat first
    pause
)

echo.
echo 👋 Stock trading session ended
pause
