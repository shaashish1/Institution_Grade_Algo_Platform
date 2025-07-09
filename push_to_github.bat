@echo off
REM GitHub Setup Helper Script for AlgoProject
REM This script will help you push your AlgoProject to GitHub

echo.
echo ==================================================================================
echo                    📤 AlgoProject - GitHub Push Setup
echo ==================================================================================
echo.

REM Check if Git is installed
echo 🔍 Checking Git installation...
git --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Git is not installed
    echo.
    echo Please install Git first:
    echo 1. Download from: https://git-scm.com/download/win
    echo 2. Run the installer with default settings
    echo 3. Restart this script after installation
    echo.
    pause
    exit /b 1
)

echo ✅ Git is installed
git --version

REM Check if already a git repository
echo.
echo 🔍 Checking if this is already a Git repository...
if exist ".git" (
    echo ✅ Git repository already initialized
) else (
    echo 🔧 Initializing Git repository...
    git init
    if errorlevel 1 (
        echo ❌ Failed to initialize Git repository
        pause
        exit /b 1
    )
    echo ✅ Git repository initialized
)

REM Check git configuration
echo.
echo 🔍 Checking Git configuration...
git config --global user.name >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️  Git user name not configured
    echo Please configure Git first:
    echo.
    echo git config --global user.name "Your Name"
    echo git config --global user.email "your.email@example.com"
    echo.
    echo Then run this script again.
    pause
    exit /b 1
)

echo ✅ Git is configured
echo User: 
git config --global user.name
echo Email: 
git config --global user.email

REM Prompt for GitHub username
echo.
set /p GITHUB_USERNAME=Enter your GitHub username: 

if "%GITHUB_USERNAME%"=="" (
    echo ❌ GitHub username is required
    pause
    exit /b 1
)

echo.
echo 🔧 Setting up repository for user: %GITHUB_USERNAME%

REM Add all files
echo.
echo 📁 Adding all files to Git...
git add .
if errorlevel 1 (
    echo ❌ Failed to add files
    pause
    exit /b 1
)

echo ✅ Files added to Git staging

REM Create commit
echo.
echo 📝 Creating initial commit...
git commit -m "Initial commit: Complete AlgoProject Enterprise Trading Platform

✅ Multi-asset trading (Stocks via Fyers, Crypto via CCXT)
✅ Advanced backtesting and analytics
✅ Real-time market data integration
✅ Comprehensive strategy framework
✅ Production-ready architecture
✅ Complete documentation suite
✅ Automated setup scripts
✅ Startup-ready with business strategy

Features:
- Stock trading with Fyers API integration
- Cryptocurrency trading with CCXT
- Advanced technical analysis
- Risk management and backtesting
- Real-time data processing
- Interactive launcher and tools
- Cross-platform compatibility
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
