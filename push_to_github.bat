@echo off
REM AlgoProject - Push to GitHub Script
REM Complete migration package upload with specific Git path

echo.
echo ==================================================================================
echo         📤 AlgoProject - Pushing Complete Migration Package to GitHub
echo ==================================================================================
echo.
echo This script will push ALL changes including:
echo   • Updated setup scripts (setup.bat, setup_complete.bat)
echo   • New migration workflows (MIGRATE_TO_PERSONAL_LAPTOP.bat)
echo   • All launcher files (trading_launcher.py, crypto_launcher.py, stock_launcher.py)
echo   • Complete documentation (migration guides)
echo   • Updated requirements.txt (crypto + stocks)
echo   • All batch launchers (start_*.bat)
echo.

REM Set Git path
set "GIT_PATH=C:\Users\ASHISHAR\AppData\Local\Programs\Git\bin\git.exe"

echo 🔍 Checking Git installation...
"%GIT_PATH%" --version
if errorlevel 1 (
    echo ❌ ERROR: Git not found at specified path
    echo Please check: %GIT_PATH%
    pause
    exit /b 1
)

echo ✅ Git is available
echo.

echo 🔍 Checking Git status...
"%GIT_PATH%" status

echo.
echo 📋 Files to be added/updated:
echo ==========================================
echo.
echo 🔧 SETUP & MIGRATION SCRIPTS:
echo   • setup.bat (updated for crypto + stocks)
echo   • setup_complete.bat (comprehensive setup)
echo   • MIGRATE_TO_PERSONAL_LAPTOP.bat (migration workflow)
echo.
echo 🚀 LAUNCHER FILES:
echo   • trading_launcher.py (unified platform)
echo   • crypto_launcher.py (crypto focused)
echo   • stock_launcher.py (stocks focused)
echo   • start_trading_platform.bat (quick start unified)
echo   • start_crypto_trading.bat (quick start crypto)
echo   • start_stock_trading.bat (quick start stocks)
echo.
echo 📚 DOCUMENTATION:
echo   • PERSONAL_LAPTOP_MIGRATION.md (complete guide)
echo   • PERSONAL_LAPTOP_READY.md (package summary)
echo   • PERSONAL_LAPTOP_SETUP.md (setup instructions)
echo   • Updated README.md
echo.
echo 📦 CONFIGURATION:
echo   • requirements.txt (crypto + stocks dependencies)
echo   • Updated crypto assets and configs
echo.

set /p proceed="Proceed with pushing to GitHub? (y/n): "
if /i not "%proceed%"=="y" (
    echo ❌ Push cancelled
    exit /b 0
)

echo.
echo ==================================================================================
echo                           📤 PUSHING TO GITHUB
echo ==================================================================================
echo.

echo � Adding all new and modified files...
"%GIT_PATH%" add .

echo.
echo 📝 Committing changes...
"%GIT_PATH%" commit -m "Complete Personal Laptop Migration Package

✨ MAJOR UPDATE: Full crypto + stock trading migration package

🔧 NEW SETUP SCRIPTS:
- setup_complete.bat: Comprehensive setup for both crypto + stocks  
- MIGRATE_TO_PERSONAL_LAPTOP.bat: Complete migration workflow
- Updated setup.bat: Enhanced for both platforms

🚀 NEW LAUNCHERS:
- trading_launcher.py: Unified platform (crypto + stocks)
- crypto_launcher.py: Crypto-focused trading platform
- stock_launcher.py: Stock-focused trading platform
- start_trading_platform.bat: Quick start unified
- start_crypto_trading.bat: Quick start crypto only
- start_stock_trading.bat: Quick start stocks only

📚 NEW DOCUMENTATION:
- PERSONAL_LAPTOP_MIGRATION.md: Complete migration guide
- PERSONAL_LAPTOP_READY.md: Migration package summary
- PERSONAL_LAPTOP_SETUP.md: Setup instructions

📦 ENHANCED DEPENDENCIES:
- requirements.txt: Complete crypto + stock dependencies
- Added Fyers API, TradingView, NSE data providers
- Enhanced technical analysis libraries

🎯 FEATURES:
- 💰 Crypto: 100+ exchanges via CCXT
- 📈 Stocks: Indian markets via Fyers API
- 🔧 Automated setup with dependency management
- 🚀 Multiple launch options for different use cases
- 📊 Pre-configured assets (crypto pairs + stock symbols)
- ⚙️ Configuration templates for both platforms
- 🏠 Optimized for personal laptops (no restrictions)

Ready for complete migration to personal laptop with both crypto and stock trading!"

if errorlevel 1 (
    echo ❌ Commit failed!
    echo 💡 This might be because there are no new changes to commit
    echo 🔍 Checking status again...
    "%GIT_PATH%" status
    pause
    exit /b 1
)

echo.
echo 🚀 Pushing to GitHub...
"%GIT_PATH%" push origin main

if errorlevel 1 (
    echo ❌ Push failed!
    echo.
    echo 🔧 Possible issues:
    echo   • Network connection problems
    echo   • Authentication required
    echo   • Remote repository conflicts
    echo.
    echo 💡 Try running manually:
    echo   git push origin main
    echo.
    pause
    exit /b 1
)

echo.
echo ==================================================================================
echo                        🎉 SUCCESSFULLY PUSHED TO GITHUB!
echo ==================================================================================
echo.
echo ✅ All files uploaded successfully!
echo.
echo 📦 Migration package now includes:
echo   • Complete automated setup (crypto + stocks)
echo   • Multiple launcher options
echo   • Comprehensive documentation
echo   • Ready-to-use configuration templates
echo   • Full dependency management
echo.
echo 🏠 Your personal laptop migration package is ready!
echo.
echo 📋 Next steps:
echo   1. Clone repository on personal laptop
echo   2. Run MIGRATE_TO_PERSONAL_LAPTOP.bat
echo   3. Configure API credentials
echo   4. Start trading with start_trading_platform.bat
echo.
echo 🚀 GitHub repository updated with complete AlgoProject!
echo.
pause
- Complete UI/UX specifications

Documentation:
- Installation guides and FAQ
- Business model and launch strategy
- Frontend architecture specifications
- Product roadmap and requirements
- Comprehensive API documentation

Ready for web UI development and commercial launch!"

if errorlevel 1 (
    echo ❌ Failed to create commit
    pause
    exit /b 1
)

echo ✅ Initial commit created

REM Set up remote origin
echo.
echo 🔗 Setting up GitHub remote...
git remote add origin https://github.com/%GITHUB_USERNAME%/AlgoProject.git
if errorlevel 1 (
    echo ⚠️  Remote origin might already exist, continuing...
    git remote set-url origin https://github.com/%GITHUB_USERNAME%/AlgoProject.git
)

echo ✅ Remote origin set to: https://github.com/%GITHUB_USERNAME%/AlgoProject.git

REM Set main branch
echo.
echo 🌿 Setting main branch...
git branch -M main
if errorlevel 1 (
    echo ⚠️  Branch setup warning, continuing...
)

echo ✅ Main branch configured

REM Push to GitHub
echo.
echo 🚀 Pushing to GitHub...
echo.
echo ⚠️  You may be prompted to enter your GitHub credentials
echo    Use your GitHub username and Personal Access Token (not password)
echo    Get token from: https://github.com/settings/tokens
echo.
pause

git push -u origin main
if errorlevel 1 (
    echo.
    echo ❌ Failed to push to GitHub
    echo.
    echo Possible issues:
    echo 1. Repository doesn't exist - Create it on GitHub first
    echo 2. Authentication failed - Check your credentials
    echo 3. Network issues - Check your internet connection
    echo.
    echo Manual steps:
    echo 1. Go to https://github.com/new
    echo 2. Create repository named: AlgoProject
    echo 3. Don't initialize with README, .gitignore, or license
    echo 4. Run this script again
    echo.
    pause
    exit /b 1
)

echo.
echo ==================================================================================
echo                           🎉 GitHub Push Complete!
echo ==================================================================================
echo.
echo ✅ Your AlgoProject is now on GitHub!
echo.
echo 🔗 Repository URL: https://github.com/%GITHUB_USERNAME%/AlgoProject
echo.
echo 🚀 What's next?
echo.
echo 1. Visit your repository on GitHub
echo 2. Add a description and topics
echo 3. Enable Issues and Wiki if desired
echo 4. Star your own repository 😄
echo 5. Share it with the community!
echo.
echo 📚 For future updates, use:
echo    git add .
echo    git commit -m "Your commit message"
echo    git push
echo.
echo 🎯 Ready to start building the web UI and launch your startup!
echo.
pause

echo.
echo 🌐 Opening your GitHub repository...
start https://github.com/%GITHUB_USERNAME%/AlgoProject

echo.
echo 👋 Thank you for using AlgoProject!
echo    Repository: https://github.com/%GITHUB_USERNAME%/AlgoProject
echo.
pause
