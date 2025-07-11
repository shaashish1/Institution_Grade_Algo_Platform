@echo off
REM Crypto Trading Platform Launcher
REM Focused on cryptocurrency trading only

echo.
echo ==================================================================================
echo         💰 AlgoProject - Crypto Trading Platform Launcher  
echo ==================================================================================
echo.
echo 🪙 Cryptocurrency Trading Platform
echo ⚡ 100+ exchanges via CCXT library
echo 🏠 Personal Laptop Edition - No restrictions!
echo.
echo Starting crypto trading platform...
echo.

REM Check if virtual environment exists and activate it
if exist "venv\Scripts\activate.bat" (
    echo 🔒 Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  Virtual environment not found - using system Python
)

REM Check if crypto_launcher.py exists
if exist "crypto_launcher.py" (
    echo 🚀 Launching crypto trading platform...
    python crypto_launcher.py
) else (
    echo ❌ crypto_launcher.py not found!
    echo 💡 Please run setup_complete.bat first
    pause
)

echo.
echo 👋 Crypto trading session ended
pause
