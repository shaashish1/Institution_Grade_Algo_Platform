# 🚀 Installation & Setup Documentation

> **Complete installation guide for AlgoProject Enterprise Trading Platform**  
> **Updated October 2025** - Includes Multi-Theme UI, User Credentials, AI Strategies
> Part of the [AlgoProject Documentation](README.md)

## 🎯 **Quick Installation**

### **Full Stack Setup (Recommended)**

#### **Frontend + Backend (Windows)**
```powershell
# Clone repository
git clone https://github.com/yourusername/AlgoProject.git
cd AlgoProject

# Backend setup
cd api
pip install fastapi uvicorn ccxt fyers-apiv3 pandas pydantic
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# New terminal - Frontend setup
cd ../frontend
npm install
npm run dev
```

#### **Legacy Python-Only Setup**
```bash
git clone https://github.com/yourusername/AlgoProject.git
cd AlgoProject
setup.bat       # Windows
./setup.sh      # Linux/macOS
```

## 🔧 **What the Setup Scripts Do**

### **Automated Process**
1. **Python Verification** - Checks Python 3.8+ installation
2. **Virtual Environment** - Creates isolated Python environment
3. **Dependencies** - Installs all required packages
4. **Project Structure** - Creates necessary directories
5. **Configuration Check** - Verifies project setup
6. **Auto-Launch** - Starts the interactive launcher

### **Dependencies Installed**
- **Trading**: `ccxt`, `fyers-apiv3`, `backtrader`
- **Data Analysis**: `pandas`, `numpy`, `ta-lib`
- **Visualization**: `matplotlib`, `plotly`, `tabulate`
- **Utilities**: `requests`, `pyyaml`, `colorama`
- **Development**: `pytest`, `jupyter`

## 📋 **Manual Installation - Full Stack**

### **Prerequisites**
- **Node.js 18+** (for frontend) - [Download](https://nodejs.org/)
- **Python 3.8+** (for backend/legacy) - [Download](https://python.org/)
- **Git** (for repository management)
- **Modern browser** (Chrome, Firefox, Safari, Edge)

### **Full Stack Setup Guide**

#### **1. Repository Setup**
```powershell
git clone https://github.com/yourusername/AlgoProject.git
cd AlgoProject
```

#### **2. Backend API Setup**
```powershell
# Navigate to API directory
cd api

# Install Python dependencies
pip install fastapi uvicorn ccxt fyers-apiv3 pandas pydantic python-multipart

# Create data directory for user credentials
mkdir data

# Start backend server (development)
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### **3. Frontend Setup**
```powershell
# Open new terminal, navigate to frontend
cd frontend

# Install Node.js dependencies
npm install

# Start development server
npm run dev
```

#### **4. Legacy Python Setup (Optional)**
```powershell
# For original Python-only features
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/macOS

pip install -r requirements.txt
```

#### **5. Project Structure Creation**
```powershell
# Create necessary directories
mkdir logs, output, data
mkdir output\backtest_results, output\live_trades, output\scan_results
```

#### **6. Launch Application**
```bash
python tools/launcher.py
```

## 🔑 **API Configuration**

### **Fyers API (For Stock Trading)**
```bash
# After installation, set up Fyers API
python stocks/fyers/generate_token.py
```

**Required Information:**
- Fyers Client ID
- Fyers Secret Key
- Fyers Username
- TOTP Key (from Fyers app)
- Trading PIN

### **CCXT (For Crypto Trading)**
- No configuration needed for demo trading
- Uses public APIs from multiple exchanges

## 🚨 **Troubleshooting**

### **Common Issues**

#### **Python Not Found**
```bash
# Check Python installation
python --version
# or
python3 --version

# Add to PATH (Windows)
# Add Python installation directory to system PATH
```

#### **Permission Errors**
```bash
# Windows - Run as Administrator
# Linux/macOS - Use sudo for system operations
sudo pip install -r requirements.txt
```

#### **Virtual Environment Issues**
```bash
# Install venv module
python -m pip install virtualenv

# Linux - Install python3-venv
sudo apt install python3-venv
```

#### **Network/Firewall Issues**
```bash
# Use different index URL
pip install -r requirements.txt -i https://pypi.org/simple/

# Install with verbose output
pip install -r requirements.txt --verbose
```

### **Dependency Issues**

#### **TA-Lib Installation Problems**
```bash
# Windows - Download wheel from unofficial binaries
pip install https://download.lfd.uci.edu/pythonlibs/archived/TA_Lib-0.4.24-cp39-cp39-win_amd64.whl

# Linux - Install development tools
sudo apt install build-essential

# macOS - Install with Homebrew
brew install ta-lib
```

#### **CCXT Installation Issues**
```bash
# Install specific version
pip install ccxt==4.0.0

# Install from source
pip install git+https://github.com/ccxt/ccxt.git
```

## 🧪 **Verification Steps**

### **1. Test Installation**
```bash
python -c "import ccxt, pandas, numpy; print('✅ Core dependencies working')"
```

### **2. Test Project Structure**
```bash
python tools/launcher.py
# Should show the interactive menu
```

### **3. Test Quick Functionality**
```bash
# From the launcher menu, choose:
# 1. Quick Test (30 seconds)
```

## 📁 **Directory Structure After Setup**

```
AlgoProject/
├── venv/                    # Virtual environment (created by setup)
├── logs/                    # Application logs (created by setup)
├── output/                  # Results and outputs (created by setup)
│   ├── backtest_results/    # Backtesting results
│   ├── live_trades/         # Live trading logs
│   └── scan_results/        # Scanner outputs
├── config/                  # Configuration files
├── input/                   # Input data and credentials
├── docs/                    # Documentation
├── tools/                   # Utility scripts
├── setup.bat               # Windows setup script
├── setup.sh                # Linux/macOS setup script
└── requirements.txt        # Python dependencies
```

## 🔄 **Updates and Maintenance**

### **Update Dependencies**
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Update packages
pip install --upgrade -r requirements.txt
```

### **Update Project**
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt
```

## 🆘 **Getting Help**

### **Documentation**
- [Main README](../README.md) - Project overview
- [Fyers Setup Guide](FYERS_ONLY_SETUP.md) - Detailed API setup
- [Module Documentation](crypto-module.md) - Specific module guides

### **Support Channels**
- **Issues**: GitHub Issues tab
- **Documentation**: Check `docs/` folder
- **Community**: Discord/Forum links in main README

### **Reporting Problems**
When reporting issues, include:
- Operating system and version
- Python version (`python --version`)
- Error messages (full traceback)
- Steps to reproduce

---

## 🎉 **Success Indicators**

After successful installation, you should see:

```
🚀 AlgoProject Trading Platform
======================================================================
Progressive Testing: Test → Backtest → Demo → Live
Choose your trading mode:

🧪 **TESTING & VALIDATION**
   1. Quick Test           - Test 3 crypto symbols (30 seconds)
   2. Detailed Test        - Detailed backtest test (1 minute)
...
```

---

<div align="center">

### **🚀 Installation Complete!**

[![Launch App](https://img.shields.io/badge/Launch-🚀-brightgreen)](../tools/launcher.py)
[![Test System](https://img.shields.io/badge/Test-🧪-blue)](../tests/test_fyers_only.py)
[![Documentation](https://img.shields.io/badge/Docs-📚-orange)](README.md)

**Ready to start trading? Run `python tools/launcher.py`**

</div>
