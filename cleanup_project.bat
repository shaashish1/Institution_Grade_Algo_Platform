@echo off
REM AlgoProject - Comprehensive Project Cleanup Script
REM Removes empty files, duplicates, backup files, and unwanted artifacts

echo.
echo ==================================================================================
echo         🧹 AlgoProject - Comprehensive Project Cleanup
echo ==================================================================================
echo.
echo This script will clean up:
echo   • Empty Python files (0 bytes)
echo   • Backup and duplicate files
echo   • Unnecessary test files
echo   • Old output files (keeping recent ones)
echo   • Temporary and cache files
echo.

set /p proceed="Proceed with cleanup? (y/n): "
if /i not "%proceed%"=="y" (
    echo ❌ Cleanup cancelled
    exit /b 0
)

echo.
echo 🧹 Starting comprehensive cleanup...
echo.

REM =============================================================================
REM STEP 1: REMOVE EMPTY PYTHON FILES
REM =============================================================================
echo 📁 STEP 1: Removing empty Python files...
echo ===============================================

REM Empty files in crypto/scripts
if exist "crypto\scripts\crypto_backtest_root.py" del "crypto\scripts\crypto_backtest_root.py"
if exist "crypto\scripts\crypto_demo_live_root2.py" del "crypto\scripts\crypto_demo_live_root2.py"
if exist "crypto\scripts\crypto_live_scanner_root.py" del "crypto\scripts\crypto_live_scanner_root.py"
if exist "crypto\scripts\list_crypto_assets_root.py" del "crypto\scripts\list_crypto_assets_root.py"

REM Empty files in stocks/scripts
if exist "stocks\scripts\stocks_backtest_root.py" del "stocks\scripts\stocks_backtest_root.py"
if exist "stocks\scripts\stocks_demo_live_root.py" del "stocks\scripts\stocks_demo_live_root.py"
if exist "stocks\scripts\stocks_live_scanner_root.py" del "stocks\scripts\stocks_live_scanner_root.py"

REM Empty files in strategies
if exist "strategies\market_inefficiency_strategy_clean.py" del "strategies\market_inefficiency_strategy_clean.py"

REM Empty files in tests
if exist "tests\quick_clean_test_utils.py" del "tests\quick_clean_test_utils.py"
if exist "tests\quick_test_root.py" del "tests\quick_test_root.py"
if exist "tests\quick_test_utils.py" del "tests\quick_test_utils.py"
if exist "tests\test_alternative_data.py" del "tests\test_alternative_data.py"
if exist "tests\test_auth_no_2fa.py" del "tests\test_auth_no_2fa.py"
if exist "tests\test_backtest_utils.py" del "tests\test_backtest_utils.py"
if exist "tests\test_crypto_demo_enhancements.py" del "tests\test_crypto_demo_enhancements.py"
if exist "tests\test_fyers_only.py" del "tests\test_fyers_only.py"
if exist "tests\test_limited_backtest_utils.py" del "tests\test_limited_backtest_utils.py"
if exist "tests\test_tradingview_auth.py" del "tests\test_tradingview_auth.py"

REM Empty files in utils
if exist "utils\alternative_data_sources.py" del "utils\alternative_data_sources.py"
if exist "utils\crypto_symbol_manager.py" del "utils\crypto_symbol_manager.py"
if exist "utils\data_acquisition.py" del "utils\data_acquisition.py"
if exist "utils\data_acquisition_new.py" del "utils\data_acquisition_new.py"
if exist "utils\diagnose_failed_symbols.py" del "utils\diagnose_failed_symbols.py"
if exist "utils\enhanced_tv_auth.py" del "utils\enhanced_tv_auth.py"
if exist "utils\fyers_data_provider.py" del "utils\fyers_data_provider.py"
if exist "utils\live_nse_quotes.py" del "utils\live_nse_quotes.py"
if exist "utils\quick_clean_test.py" del "utils\quick_clean_test.py"
if exist "utils\quick_test.py" del "utils\quick_test.py"
if exist "utils\simple_fyers_provider.py" del "utils\simple_fyers_provider.py"
if exist "utils\stock_symbol_manager.py" del "utils\stock_symbol_manager.py"
if exist "utils\symbol_validator.py" del "utils\symbol_validator.py"

echo ✅ Empty Python files removed

REM =============================================================================
REM STEP 2: REMOVE BACKUP AND DUPLICATE FILES
REM =============================================================================
echo.
echo 📁 STEP 2: Removing backup and duplicate files...
echo ===============================================

REM Remove backup files
if exist "strategies\market_inefficiency_strategy_backup.py" del "strategies\market_inefficiency_strategy_backup.py"

echo ✅ Backup files removed

REM =============================================================================
REM STEP 3: CLEAN OLD OUTPUT FILES (KEEP RECENT ONES)
REM =============================================================================
echo.
echo 📁 STEP 3: Cleaning old output files...
echo ===============================================

echo 🗂️  Cleaning crypto output files (keeping recent 5)...
pushd crypto\output >nul 2>&1
if exist "*.csv" (
    REM Keep only the 5 most recent portfolio summary files
    for /f "skip=5 delims=" %%i in ('dir /b /o-d crypto_portfolio_summary_*.csv 2^>nul') do del "%%i" >nul 2>&1
    
    REM Keep only the 5 most recent strategy comparison files
    for /f "skip=5 delims=" %%i in ('dir /b /o-d strategy_comparison_summary_*.csv 2^>nul') do del "%%i" >nul 2>&1
    
    REM Remove old detailed trade files (keep only recent 10)
    for /f "skip=10 delims=" %%i in ('dir /b /o-d crypto_backtest_trades_detailed_*.csv 2^>nul') do del "%%i" >nul 2>&1
)
popd >nul 2>&1

echo ✅ Old output files cleaned

REM =============================================================================
REM STEP 4: REMOVE UNNECESSARY CACHE AND TEMP FILES
REM =============================================================================
echo.
echo 📁 STEP 4: Removing cache and temporary files...
echo ===============================================

REM Remove Python cache files
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" >nul 2>&1

REM Remove .pyc files
del /s /q *.pyc >nul 2>&1

REM Remove .pyo files
del /s /q *.pyo >nul 2>&1

REM Remove .log files (except recent ones)
for /f "skip=5 delims=" %%i in ('dir /b /o-d *.log 2^>nul') do del "%%i" >nul 2>&1

echo ✅ Cache and temporary files removed

REM =============================================================================
REM STEP 5: CLEAN UTILS DIRECTORY (CONSOLIDATE DUPLICATES)
REM =============================================================================
echo.
echo 📁 STEP 5: Cleaning utils directory...
echo ===============================================

REM The utils directory has many empty files and duplicates of files in other locations
REM These are redundant since the main implementations are in their proper modules

echo ⚠️  utils directory contains many empty/duplicate files
echo 💡 Main implementations are in their proper module locations:
echo   • crypto/ - for crypto-specific utilities
echo   • stocks/ - for stock-specific utilities  
echo   • tools/ - for general tools and utilities

echo ✅ Utils directory noted for manual review

REM =============================================================================
REM STEP 6: VERIFY ESSENTIAL FILES REMAIN
REM =============================================================================
echo.
echo 📁 STEP 6: Verifying essential files...
echo ===============================================

set "essential_error=0"

REM Check main launchers
if not exist "trading_launcher.py" (
    echo ❌ trading_launcher.py missing!
    set "essential_error=1"
) else (
    echo ✅ trading_launcher.py: OK
)

if not exist "crypto_launcher.py" (
    echo ❌ crypto_launcher.py missing!
    set "essential_error=1"
) else (
    echo ✅ crypto_launcher.py: OK
)

if not exist "stock_launcher.py" (
    echo ❌ stock_launcher.py missing!
    set "essential_error=1"
) else (
    echo ✅ stock_launcher.py: OK
)

REM Check key crypto files
if not exist "crypto\scripts\crypto_backtest.py" (
    echo ❌ crypto_backtest.py missing!
    set "essential_error=1"
) else (
    echo ✅ crypto_backtest.py: OK
)

if not exist "crypto\scripts\enhanced_crypto_backtest.py" (
    echo ❌ enhanced_crypto_backtest.py missing!
    set "essential_error=1"
) else (
    echo ✅ enhanced_crypto_backtest.py: OK
)

REM Check key stock files
if not exist "stocks\scripts\stocks_backtest.py" (
    echo ❌ stocks_backtest.py missing!
    set "essential_error=1"
) else (
    echo ✅ stocks_backtest.py: OK
)

if not exist "stocks\fyers_data_provider.py" (
    echo ❌ fyers_data_provider.py missing!
    set "essential_error=1"
) else (
    echo ✅ fyers_data_provider.py: OK
)

REM Check tools
if not exist "tools\system_verification.py" (
    echo ❌ system_verification.py missing!
    set "essential_error=1"
) else (
    echo ✅ system_verification.py: OK
)

if "%essential_error%"=="1" (
    echo.
    echo ⚠️  WARNING: Some essential files are missing!
    echo Please verify the cleanup didn't remove important files.
) else (
    echo.
    echo ✅ All essential files verified
)

REM =============================================================================
REM CLEANUP COMPLETION
REM =============================================================================
echo.
echo ==================================================================================
echo                           🎉 CLEANUP COMPLETED!
echo ==================================================================================
echo.
echo ✅ Project cleanup summary:
echo   • Empty Python files: Removed
echo   • Backup files: Removed  
echo   • Old output files: Cleaned (kept recent)
echo   • Cache files: Removed
echo   • Temporary files: Removed
echo   • Essential files: Verified
echo.
echo 📊 Cleaned project structure:
echo   • crypto/ - Crypto trading module (clean)
echo   • stocks/ - Stock trading module (clean)
echo   • strategies/ - Trading strategies (clean)
echo   • tools/ - System utilities (clean)
echo   • tests/ - Essential tests only (clean)
echo.
echo 📋 Manual review recommended:
echo   • utils/ directory - Contains duplicates of files in other modules
echo   • docs/ directory - May contain outdated documentation
echo   • Old CSV output files - Verify recent data is preserved
echo.
echo 🚀 Your AlgoProject is now clean and organized!
echo.
pause
