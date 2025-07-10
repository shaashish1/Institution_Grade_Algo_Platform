@echo off
REM AlgoProject Enhanced Crypto Backtest Runner (Windows Batch)
REM Simplified wrapper to run the enhanced crypto backtest using the project's Python environment

echo 🚀 Running Enhanced Crypto Backtest with AlgoProject's Python environment...
echo 📂 Project Root: %~dp0
echo 🐍 Using AlgoProject's Python environment
echo ================================================================================

REM Change to the project directory
cd /d "%~dp0"

REM Run the enhanced crypto backtest with the project's Python environment
venv\Scripts\python.exe crypto\scripts\enhanced_crypto_backtest.py %*

echo ================================================================================
echo 🎉 Backtest completed!
pause
