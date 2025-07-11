@echo off
REM AlgoProject - Personal Laptop Migration Script
REM Complete migration workflow from start to finish

echo.
echo ==================================================================================
echo         🏠 AlgoProject - Personal Laptop Migration Workflow
echo ==================================================================================
echo.
echo This script demonstrates the COMPLETE migration process for AlgoProject
echo to your personal laptop with BOTH crypto and stock trading capabilities.
echo.
echo 🎯 MIGRATION STAGES:
echo ==================================================================================
echo 1. 🔍 Pre-Migration Check
echo 2. 📦 Complete Setup (Python + Dependencies)  
echo 3. 🏗️  Project Structure Creation
echo 4. 📊 Asset & Configuration Files
echo 5. 🚀 Launcher Creation
echo 6. ✅ Verification & Testing
echo 7. 🎉 Ready to Trade!
echo.

set /p proceed="Ready to begin complete migration? (y/n): "
if /i not "%proceed%"=="y" (
    echo Migration cancelled.
    exit /b 0
)

echo.
echo ==================================================================================
echo                          🔍 STAGE 1: PRE-MIGRATION CHECK
echo ==================================================================================
echo.

REM Check if this is a fresh migration or existing setup
if exist "venv" (
    echo ⚠️  Existing AlgoProject installation detected!
    echo.
    set /p overwrite="Do you want to recreate everything fresh? (y/n): "
    if /i "%overwrite%"=="y" (
        echo 🧹 Cleaning existing installation...
        rmdir /s /q venv >nul 2>&1
        del crypto_launcher.py >nul 2>&1
        del stock_launcher.py >nul 2>&1  
        del trading_launcher.py >nul 2>&1
        del start_*.bat >nul 2>&1
        echo ✅ Clean slate ready for migration
    ) else (
        echo 📈 Continuing with existing installation...
    )
) else (
    echo ✅ Fresh migration - perfect for personal laptop setup!
)

echo.
echo 📋 Pre-migration checklist:
echo   • Target: Personal laptop (no corporate restrictions)
echo   • Goal: Both crypto AND stock trading capabilities
echo   • Method: Automated setup with manual verification
echo   • Time: ~5-10 minutes depending on internet speed

echo.
echo ==================================================================================
echo                     📦 STAGE 2: RUNNING COMPLETE SETUP
echo ==================================================================================
echo.

echo 🚀 Launching automated setup...
echo This will install EVERYTHING needed for both crypto and stock trading.
echo.

if exist "setup_complete.bat" (
    echo ✅ Running setup_complete.bat (comprehensive setup)...
    call setup_complete.bat
) else if exist "setup.bat" (
    echo ✅ Running setup.bat (fallback setup)...
    call setup.bat
) else (
    echo ❌ No setup script found!
    echo 💡 Please ensure you have setup_complete.bat or setup.bat
    pause
    exit /b 1
)

echo.
echo ==================================================================================
echo                      ✅ STAGE 3: POST-SETUP VERIFICATION
echo ==================================================================================
echo.

echo 🔍 Verifying migration success...

REM Check virtual environment
if exist "venv\Scripts\activate.bat" (
    echo ✅ Virtual environment: Created successfully
) else (
    echo ❌ Virtual environment: FAILED
)

REM Check project structure
set "success=1"
for %%d in (crypto stocks tools strategies) do (
    if exist "%%d" (
        echo ✅ Directory %%d: OK
    ) else (
        echo ❌ Directory %%d: MISSING
        set "success=0"
    )
)

REM Check key files
for %%f in (crypto\input\crypto_assets.csv stocks\input\stock_assets.csv crypto\input\config_crypto.yaml stocks\input\config_stocks.yaml) do (
    if exist "%%f" (
        echo ✅ File %%f: OK
    ) else (
        echo ❌ File %%f: MISSING
        set "success=0"
    )
)

REM Check launchers
for %%l in (trading_launcher.py crypto_launcher.py stock_launcher.py) do (
    if exist "%%l" (
        echo ✅ Launcher %%l: OK
    ) else (
        echo ❌ Launcher %%l: MISSING
        set "success=0"
    )
)

REM Check batch files
for %%b in (start_trading_platform.bat start_crypto_trading.bat start_stock_trading.bat) do (
    if exist "%%b" (
        echo ✅ Quick start %%b: OK
    ) else (
        echo ❌ Quick start %%b: MISSING
        set "success=0"
    )
)

echo.
if "%success%"=="1" (
    echo ✅ Migration verification: PASSED
) else (
    echo ❌ Migration verification: FAILED
    echo 💡 Some components are missing - setup may not have completed successfully
)

echo.
echo ==================================================================================
echo                       🎯 STAGE 4: CONFIGURATION GUIDE
echo ==================================================================================
echo.

echo 📋 Next steps for complete functionality:
echo.
echo 💰 CRYPTO TRADING CONFIGURATION:
echo ----------------------------------------
echo 1. Edit: crypto\input\config_crypto.yaml
echo 2. Add your exchange API keys (Binance, Coinbase, etc.)
echo 3. Start with sandbox/paper trading mode
echo 4. Test with: start_crypto_trading.bat
echo.
echo 📈 STOCK TRADING CONFIGURATION:
echo ----------------------------------------
echo 1. Edit: stocks\fyers\credentials.py
echo 2. Fill in your Fyers API details
echo 3. Run: stocks\fyers\generate_token.py
echo 4. Test with: start_stock_trading.bat
echo.

echo ==================================================================================
echo                          🎉 MIGRATION COMPLETE!
echo ==================================================================================
echo.
echo 🏠 AlgoProject is now fully migrated to your personal laptop!
echo.
echo 🚀 QUICK START OPTIONS:
echo ==================================================================================
echo.
echo 1. 🎯 UNIFIED PLATFORM (Crypto + Stocks):
echo    Double-click: start_trading_platform.bat
echo    OR run: python trading_launcher.py
echo.
echo 2. 💰 CRYPTO TRADING ONLY:
echo    Double-click: start_crypto_trading.bat
echo    OR run: python crypto_launcher.py
echo.
echo 3. 📈 STOCK TRADING ONLY:
echo    Double-click: start_stock_trading.bat
echo    OR run: python stock_launcher.py
echo.
echo 📚 DOCUMENTATION:
echo ==================================================================================
echo • Main guide: README.md
echo • Setup guide: PERSONAL_LAPTOP_MIGRATION.md
echo • Crypto docs: crypto\README.md  
echo • Stock docs: stocks\README.md
echo.
echo ⚠️  IMPORTANT REMINDERS:
echo ==================================================================================
echo 1. 🔐 Configure API credentials before live trading
echo 2. 🧪 Always start with paper/sandbox trading
echo 3. 📊 Run backtests to verify your strategies
echo 4. 💰 Use small amounts when going live
echo 5. 📈 Monitor your trades and risk management
echo.

set /p launch="Launch trading platform now? (y/n): "
if /i "%launch%"=="y" (
    echo.
    echo 🚀 Launching AlgoProject Trading Platform...
    if exist "start_trading_platform.bat" (
        start_trading_platform.bat
    ) else (
        echo ❌ Launcher not found - please run setup again
    )
) else (
    echo.
    echo 👋 Migration complete! You can start trading anytime with:
    echo    start_trading_platform.bat
)

echo.
echo 🎉 Welcome to AlgoProject on your personal laptop!
echo 💰📈 Happy trading with both crypto and stocks! 🚀
echo.
pause
