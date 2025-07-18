@echo off
REM AlgoProject - Complete Trading Platform Setup Script
REM Fixed version - removes problematic dependencies and fixes display issues

echo.
echo ================================================================================
echo          AlgoProject - Complete Trading Platform Setup (Fixed)
echo ================================================================================
echo.
echo This script will handle all prerequisites for:
echo.
echo CRYPTO TRADING:
echo   * 100+ cryptocurrency exchanges via CCXT
echo   * Real-time crypto data and trading
echo   * Crypto backtesting and scanning
echo.
echo STOCK TRADING:
echo   * Stock market data access
echo   * Stock backtesting and analysis
echo.
echo SETUP INCLUDES:
echo   * Check Python installation
echo   * Create virtual environment
echo   * Install working dependencies (NO TA-Lib)
echo   * Create project structure
echo   * Verify installation
echo.
echo Starting setup in 3 seconds...
for /l %%i in (3,-1,1) do (
    echo %%i...
    timeout /t 1 /nobreak >nul
)
echo.

REM =============================================================================
REM STEP 1: CHECK PYTHON
REM =============================================================================
echo STEP 1: Checking Python installation...
echo ===============================================

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo SUCCESS: Python found: %PYTHON_VERSION%

REM =============================================================================
REM STEP 2: CREATE VIRTUAL ENVIRONMENT
REM =============================================================================
echo.
echo STEP 2: Setting up virtual environment...
echo ===============================================

if exist "venv" (
    echo WARNING: Virtual environment exists, recreating...
    rmdir /s /q venv
)

echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo SUCCESS: Virtual environment created

REM =============================================================================
REM STEP 3: INSTALL DEPENDENCIES
REM =============================================================================
echo.
echo STEP 3: Installing dependencies...
echo ===============================================

echo Upgrading pip...
venv\Scripts\python.exe -m pip install --upgrade pip --quiet

echo Installing core packages...
echo   * CCXT (crypto exchange library)
venv\Scripts\python.exe -m pip install "ccxt>=4.0.0" --quiet

echo   * Data analysis libraries
venv\Scripts\python.exe -m pip install "pandas>=1.3.0" "numpy>=1.21.0" --quiet

echo   * Technical analysis (ta library - pure Python)
venv\Scripts\python.exe -m pip install "ta>=0.10.0" --quiet

echo   * Visualization libraries
venv\Scripts\python.exe -m pip install "matplotlib>=3.5.0" "plotly>=5.0.0" --quiet

echo   * Utility libraries
venv\Scripts\python.exe -m pip install "requests>=2.31.0" "pyyaml>=6.0" "python-dotenv>=1.0.0" --quiet

echo   * Display libraries
venv\Scripts\python.exe -m pip install "colorama>=0.4.6" "rich>=13.0.0" "tabulate>=0.9.0" --quiet

echo   * Additional libraries
venv\Scripts\python.exe -m pip install "websocket-client>=1.8.0" "yfinance>=0.2.0" "scipy>=1.10.0" "scikit-learn>=1.3.0" "joblib>=1.3.0" "pytz>=2023.3" --quiet

echo SUCCESS: Core packages installed

REM =============================================================================
REM STEP 4: CREATE PROJECT STRUCTURE
REM =============================================================================
echo.
echo STEP 4: Creating project structure...
echo ===============================================

REM Create main crypto directories
if not exist "crypto" mkdir crypto
if not exist "crypto\input" mkdir crypto\input
if not exist "crypto\output" mkdir crypto\output
if not exist "crypto\logs" mkdir crypto\logs
if not exist "crypto\scripts" mkdir crypto\scripts

REM Create specific output subdirectories
if not exist "crypto\output\backtest_results" mkdir crypto\output\backtest_results
if not exist "crypto\output\live_trades" mkdir crypto\output\live_trades
if not exist "crypto\output\scan_results" mkdir crypto\output\scan_results

REM Remove any old scripts/output directory if it exists
if exist "scripts\output" (
    echo Removing old scripts\output directory...
    rmdir /s /q "scripts\output"
)

echo SUCCESS: Project directories created

REM =============================================================================
REM STEP 5: VERIFY INSTALLATION
REM =============================================================================
echo.
echo STEP 5: Verifying installation...
echo ===============================================

echo Testing core libraries...
venv\Scripts\python.exe -c "import ccxt; print('SUCCESS: CCXT v' + ccxt.__version__)" 2>nul || echo "ERROR: CCXT import failed"
venv\Scripts\python.exe -c "import pandas; print('SUCCESS: Pandas imported')" 2>nul || echo "ERROR: Pandas import failed"
venv\Scripts\python.exe -c "import numpy; print('SUCCESS: NumPy imported')" 2>nul || echo "ERROR: NumPy import failed"
venv\Scripts\python.exe -c "import ta; print('SUCCESS: TA library imported')" 2>nul || echo "ERROR: TA library import failed"

REM =============================================================================
REM STEP 6: FINAL STATUS
REM =============================================================================
echo.
echo ================================================================================
echo                              SETUP COMPLETE
echo ================================================================================
echo.
echo To start the crypto trading platform:
echo   1. Run: venv\Scripts\python.exe crypto_launcher.py
echo   2. Or:  venv\Scripts\python.exe main.py
echo.
echo All outputs will be saved to:
echo   * Crypto outputs: crypto\output\
echo   * Log files: crypto\logs\
echo.
echo Press any key to launch the crypto trading platform...
pause >nul

echo.
echo Launching crypto trading platform...
venv\Scripts\python.exe crypto_launcher.py
