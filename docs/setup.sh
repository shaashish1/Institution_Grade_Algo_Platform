#!/bin/bash

# AlgoProject - Automated Setup Script (Linux/macOS)
# This script will set up the entire AlgoProject trading platform automat# Check if configuration files exist
echo
echo "🔧 Checking configuration files..."
if [ ! -f "crypto/input/config_crypto.yaml" ]; then
    echo "⚠️  Crypto configuration files not found - this may indicate setup issues"
fi
if [ ! -f "stocks/fyers/access_token.py" ]; then
    echo "⚠️  Fyers access token not found - you'll need to set this up for stock trading"
ficho ""
echo "=================================================================================="
echo "               🚀 AlgoProject - Enterprise Trading Platform Setup"
echo "=================================================================================="
echo ""
echo "This script will automatically:"
echo "  • Check Python installation"
echo "  • Create virtual environment"
echo "  • Install all dependencies"
echo "  • Set up project structure"
echo "  • Launch the interactive menu"
echo ""
echo "Please ensure you have Python 3.8+ installed on your system."
echo ""
read -p "Press Enter to continue..."

# Check if Python is installed
echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo ""
        echo "❌ ERROR: Python is not installed or not in PATH"
        echo ""
        echo "Please install Python 3.8+ from: https://www.python.org/downloads/"
        echo "Or use your system package manager:"
        echo "  • Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
        echo "  • macOS: brew install python3"
        echo "  • CentOS/RHEL: sudo yum install python3 python3-pip"
        echo ""
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Display Python version
echo "✅ Python found:"
$PYTHON_CMD --version

# Check Python version
echo ""
echo "🔍 Checking Python version compatibility..."
$PYTHON_CMD -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ ERROR: Python 3.8+ required"
    echo "Your Python version is too old. Please install Python 3.8 or higher."
    echo "Download from: https://www.python.org/downloads/"
    echo ""
    exit 1
fi

echo "✅ Python version is compatible"

# Create virtual environment
echo ""
echo "🔧 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists, skipping creation"
else
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ ERROR: Failed to create virtual environment"
        echo "Please ensure you have python3-venv installed:"
        echo "  • Ubuntu/Debian: sudo apt install python3-venv"
        echo "  • macOS: Should work with standard Python installation"
        echo ""
        exit 1
    fi
    echo "✅ Virtual environment created successfully"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ ERROR: Failed to activate virtual environment"
    echo ""
    exit 1
fi

echo "✅ Virtual environment activated"

# Upgrade pip
echo ""
echo "🔧 Upgrading pip..."
python -m pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Warning: Failed to upgrade pip, continuing anyway..."
fi

# Install dependencies
echo ""
echo "📦 Installing project dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ ERROR: Failed to install dependencies"
    echo ""
    echo "Please check your internet connection and try again"
    echo "If the problem persists, try running: pip install -r requirements.txt --verbose"
    echo ""
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Verify key dependencies
echo ""
echo "🔍 Verifying key dependencies..."
python -c "import ccxt, pandas, numpy, requests, yaml; print('✅ All key dependencies verified')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Warning: Some dependencies may not be properly installed"
    echo "The application may still work, but you might encounter issues"
    echo ""
fi

# Create necessary directories
echo ""
echo "📁 Creating project directories..."
mkdir -p logs
mkdir -p output/backtest_results
mkdir -p output/live_trades
mkdir -p output/scan_results
echo "✅ Project directories created"

# Check if configuration files exist
echo ""
echo "🔧 Checking configuration files..."
if [ ! -f "config/config.yaml" ]; then
    echo "⚠️  Configuration files not found - this is normal for a fresh installation"
fi
if [ ! -f "input/access_token.py" ]; then
    echo "⚠️  Fyers access token not found - you'll need to set this up for stock trading"
fi

echo "✅ Configuration check completed"

# Display setup completion
echo ""
echo "=================================================================================="
echo "                           🎉 Setup Complete!"
echo "=================================================================================="
echo ""
echo "✅ Python environment: Ready"
echo "✅ Virtual environment: Activated"
echo "✅ Dependencies: Installed"
echo "✅ Project structure: Ready"
echo ""
echo "🚀 What's next?"
echo ""
echo "1. For STOCK TRADING (Fyers API):"
echo "   • Run: python stocks/fyers/generate_token.py"
echo "   • Follow the prompts to set up your Fyers API credentials"
echo ""
echo "2. For CRYPTO TRADING:"
echo "   • No additional setup needed - works out of the box!"
echo ""
echo "3. Launch the application:"
echo "   • Run: python tools/launcher.py"
echo "   • Or just wait - we'll launch it automatically in 10 seconds!"
echo ""
echo "📚 Documentation: Check docs/ folder for detailed guides"
echo "🆘 Support: Check README.md for troubleshooting"
echo ""

# Countdown and auto-launch
echo "Starting application in:"
for i in {10..1}; do
    echo "$i seconds..."
    sleep 1
done

echo ""
echo "🚀 Launching AlgoProject..."
echo ""
python tools/launcher.py

# If launcher fails, provide helpful information
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ The launcher encountered an issue"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "1. Make sure you're in the correct directory"
    echo "2. Check if all files were downloaded correctly"
    echo "3. Try running: python tools/launcher.py manually"
    echo "4. Make sure virtual environment is activated: source venv/bin/activate"
    echo ""
    echo "📧 For support, check the README.md file"
    echo ""
fi

echo ""
echo "👋 Thank you for using AlgoProject!"
