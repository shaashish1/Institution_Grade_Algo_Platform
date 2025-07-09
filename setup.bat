@echo off
REM AlgoProject - Automated Setup Script
REM This script will set up the entire AlgoProject trading platform automatically

echo.
echo ==================================================================================
echo               🚀 AlgoProject - Enterprise Trading Platform Setup
echo ==================================================================================
echo.
echo This script will automatically:
echo   • Check Python installation
echo   • Create virtual environment
echo   • Install all dependencies
echo   • Set up project structure
echo   • Launch the interactive menu
echo.
echo Please ensure you have Python 3.8+ installed on your system.
echo.
pause

REM Check if Python is installed
echo 🔍 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Display Python version
echo ✅ Python found:
python --version

REM Check Python version (basic check)
echo.
echo 🔍 Checking Python version compatibility...
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python 3.8+ required
    echo Your Python version is too old. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python version is compatible

REM Create virtual environment
echo.
echo 🔧 Creating virtual environment...
if exist "venv" (
    echo ⚠️  Virtual environment already exists, skipping creation
) else (
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo ❌ ERROR: Failed to create virtual environment
        echo Please ensure you have sufficient permissions and disk space
        echo.
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created successfully
)

REM Activate virtual environment
echo.
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Failed to activate virtual environment
    echo.
    pause
    exit /b 1
)

echo ✅ Virtual environment activated

REM Upgrade pip
echo.
echo 🔧 Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo.
    echo ⚠️  Warning: Failed to upgrade pip, continuing anyway...
)

REM Install dependencies
echo.
echo 📦 Installing project dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Failed to install dependencies
    echo.
    echo Please check your internet connection and try again
    echo If the problem persists, try running: pip install -r requirements.txt --verbose
    echo.
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully

REM Verify key dependencies
echo.
echo 🔍 Verifying key dependencies...
python -c "import ccxt, pandas, numpy, requests, pyyaml; print('✅ All key dependencies verified')" 2>nul
if errorlevel 1 (
    echo.
    echo ⚠️  Warning: Some dependencies may not be properly installed
    echo The application may still work, but you might encounter issues
    echo.
)

REM Create necessary directories
echo.
echo 📁 Creating project directories...
if not exist "logs" mkdir logs
if not exist "output" mkdir output
if not exist "output\backtest_results" mkdir output\backtest_results
if not exist "output\live_trades" mkdir output\live_trades
if not exist "output\scan_results" mkdir output\scan_results
echo ✅ Project directories created

REM Check if configuration files exist
echo.
echo 🔧 Checking configuration files...
if not exist "config\config.yaml" (
    echo ⚠️  Configuration files not found - this is normal for a fresh installation
)
if not exist "input\access_token.py" (
    echo ⚠️  Fyers access token not found - you'll need to set this up for stock trading
)

echo ✅ Configuration check completed

REM Display setup completion
echo.
echo ==================================================================================
echo                           🎉 Setup Complete!
echo ==================================================================================
echo.
echo ✅ Python environment: Ready
echo ✅ Virtual environment: Activated
echo ✅ Dependencies: Installed
echo ✅ Project structure: Ready
echo.
echo 🚀 What's next?
echo.
echo 1. For STOCK TRADING (Fyers API):
echo    • Run: python stocks\fyers\generate_token.py
echo    • Follow the prompts to set up your Fyers API credentials
echo.
echo 2. For CRYPTO TRADING:
echo    • No additional setup needed - works out of the box!
echo.
echo 3. Launch the application:
echo    • Run: python tools\launcher.py
echo    • Or just wait - we'll launch it automatically in 10 seconds!
echo.
echo 📚 Documentation: Check docs\ folder for detailed guides
echo 🆘 Support: Check README.md for troubleshooting
echo.

REM Countdown and auto-launch
echo Starting application in:
for /l %%i in (10,-1,1) do (
    echo %%i seconds...
    timeout /t 1 /nobreak >nul
)

echo.
echo 🚀 Launching AlgoProject...
echo.
python tools\launcher.py

REM If launcher fails, provide helpful information
if errorlevel 1 (
    echo.
    echo ❌ The launcher encountered an issue
    echo.
    echo 🔧 Troubleshooting:
    echo 1. Make sure you're in the correct directory
    echo 2. Check if all files were downloaded correctly
    echo 3. Try running: python tools\launcher.py manually
    echo.
    echo 📧 For support, check the README.md file
    echo.
    pause
)

echo.
echo 👋 Thank you for using AlgoProject!
pause
