@echo off
echo ============================================
echo    AlgoProject Frontend Quick Launcher
echo ============================================
echo.

set FRONTEND_DIR=%~dp0frontend

if not exist "%FRONTEND_DIR%" (
    echo ❌ Frontend directory not found!
    echo Please run this script from the AlgoProject root directory.
    pause
    exit /b 1
)

echo 📁 Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found! Please install Node.js 18+ first.
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js found
echo.

cd /d "%FRONTEND_DIR%"

echo 📦 Checking dependencies...
if not exist "node_modules" (
    echo 🔄 Installing dependencies... This may take a few minutes.
    call npm install
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed successfully
) else (
    echo ✅ Dependencies already installed
)

echo.
echo 🚀 Starting development server...
echo.
echo The frontend will be available at: http://localhost:3000
echo Backend API should be running at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev

pause