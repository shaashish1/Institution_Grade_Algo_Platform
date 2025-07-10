# 🚀 AlgoProject - Quick Setup Guide

## 🎯 **One-Click Setup**

### **Windows Users**
```bash
# 1. Download or clone the repository
git clone https://github.com/yourusername/AlgoProject.git
cd AlgoProject

# 2. Run the automated setup
setup.bat
```

### **Linux/macOS Users**
```bash
# 1. Download or clone the repository
git clone https://github.com/yourusername/AlgoProject.git
cd AlgoProject

# 2. Make setup script executable and run
chmod +x setup.sh
./setup.sh
```

## 🔧 **What the Setup Script Does**

### **Automated Installation**
- ✅ **Python Check**: Verifies Python 3.8+ is installed
- ✅ **Virtual Environment**: Creates isolated Python environment
- ✅ **Dependencies**: Installs all required packages from requirements.txt
- ✅ **Directory Structure**: Creates necessary folders (logs, output, etc.)
- ✅ **Configuration Check**: Verifies project structure
- ✅ **Auto-Launch**: Starts the interactive launcher automatically

### **Prerequisites Handled**
- Python 3.8+ installation verification
- Virtual environment creation
- Package installation (pandas, numpy, ccxt, requests, etc.)
- Project folder structure setup
- Dependency verification

## 📋 **Manual Setup (if needed)**

If the automated setup doesn't work, follow these steps:

### **Step 1: Install Python**
- Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
- **Windows**: Check "Add Python to PATH" during installation
- **Linux**: `sudo apt install python3 python3-pip python3-venv`
- **macOS**: `brew install python3`

### **Step 2: Clone Repository**
```bash
git clone https://github.com/yourusername/AlgoProject.git
cd AlgoProject
```

### **Step 3: Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### **Step 4: Install Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### **Step 5: Create Directories**
```bash
mkdir logs output
mkdir output/backtest_results output/live_trades output/scan_results
```

### **Step 6: Launch Application**
```bash
python tools/launcher.py
```

## 🔑 **API Setup (Optional)**

### **For Stock Trading (Fyers API)**
```bash
# After setup, configure Fyers API
python stocks/fyers/generate_token.py
```

### **For Crypto Trading**
- No setup needed - works out of the box!
- Uses public APIs for demo trading

## 🚨 **Troubleshooting**

### **Common Issues**

**Python Not Found**
- Ensure Python 3.8+ is installed
- Check PATH environment variable
- Try `python3` instead of `python`

**Permission Errors**
- Run as administrator (Windows)
- Use `sudo` for directory creation (Linux/macOS)

**Network Issues**
- Check internet connection
- Use VPN if behind firewall
- Try: `pip install -r requirements.txt --verbose`

**Virtual Environment Issues**
- Install venv: `sudo apt install python3-venv` (Linux)
- Use full path: `python -m venv venv`

### **Getting Help**
- Check `README.md` for detailed documentation
- Review `docs/` folder for specific guides
- Run `python tools/launcher.py` for interactive help

## 🎉 **Success Verification**

After setup, you should see:
```
🚀 AlgoProject Trading Platform
======================================================================
Choose your trading mode:
🧪 **TESTING & VALIDATION**
   1. Quick Test           - Test 3 crypto symbols (30 seconds)
   2. Detailed Test        - Detailed backtest test (1 minute)
...
```

## 📚 **Next Steps**

1. **Test the System**: Choose option 1 (Quick Test) from the launcher
2. **Configure APIs**: Set up Fyers API for stock trading if needed
3. **Explore Features**: Try different trading modes and strategies
4. **Read Documentation**: Check `docs/` folder for detailed guides

---

<div align="center">

**🚀 Ready to Start Trading?**

[![Launch Application](https://img.shields.io/badge/Launch-🚀-brightgreen)](tools/launcher.py)
[![Documentation](https://img.shields.io/badge/Docs-📚-blue)](docs/)
[![Support](https://img.shields.io/badge/Support-💬-orange)](README.md)

</div>
