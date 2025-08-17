# 🎯 Delta Exchange Symbol Fetcher Usage Guide

## ✅ **Script Created: `delta_fetch_symbols.py`**

The dedicated script for fetching and organizing all Delta Exchange trading pairs into CSV input files.

---

## 🚀 **Basic Usage**

### **1. Fetch All Pairs and Save to CSV Files:**
```bash
python crypto\scripts\delta_fetch_symbols.py
```
**Result:** Creates organized CSV files in `d:\AlgoProject\crypto\input\`

### **2. Test Connection Only:**
```bash
python crypto\scripts\delta_fetch_symbols.py --test
```
**Result:** Tests Delta Exchange connection without saving files

### **3. Display Pair Counts:**
```bash
python crypto\scripts\delta_fetch_symbols.py --display
```
**Result:** Shows categorized pair counts without creating files

### **4. Save to Custom Directory:**
```bash
python crypto\scripts\delta_fetch_symbols.py --output custom_folder\
```
**Result:** Saves CSV files to specified directory

---

## 📁 **Files Created**

When you run the script, it creates these CSV files in `crypto\input\`:

### **Trading Pair Files:**
- `delta_spot_usdt.csv` - All BTC/USDT, ETH/USDT spot pairs
- `delta_spot_btc.csv` - BTC-quoted spot pairs  
- `delta_spot_eth.csv` - ETH-quoted spot pairs
- `delta_perpetual_usdt.csv` - Perpetual futures (USDT)
- `delta_perpetual_btc.csv` - Perpetual futures (BTC)
- `delta_futures_usdt.csv` - Futures contracts (USDT)
- `delta_futures_btc.csv` - Futures contracts (BTC)
- `delta_options_calls.csv` - Call options
- `delta_options_puts.csv` - Put options
- `delta_other_pairs.csv` - Other trading pairs

### **Summary File:**
- `delta_pairs_summary.csv` - Master overview of all categories

---

## 📊 **CSV File Format**

Each CSV file contains detailed metadata:

```csv
Symbol,Base,Quote,Market_Type,Active,Spot,Future,Option,Swap,Description,Generated
BTC/USDT,BTC,USDT,SPOT,YES,YES,NO,NO,NO,BTC/USDT SPOT,2025-07-16 19:59:17
ETH/USDT,ETH,USDT,SPOT,YES,YES,NO,NO,NO,ETH/USDT SPOT,2025-07-16 19:59:17
```

**Columns:**
- `Symbol` - Trading pair symbol
- `Base` - Base currency
- `Quote` - Quote currency  
- `Market_Type` - SPOT, FUTURES, OPTION, PERPETUAL
- `Active` - YES/NO if pair is active
- `Spot/Future/Option/Swap` - Market type flags
- `Description` - Human-readable description
- `Generated` - Timestamp when file was created

---

## 🔗 **Integration with Backtesting**

After creating CSV files, use them in backtesting:

### **Load Specific Pair Types:**
```bash
# Load spot USDT pairs
python crypto\scripts\delta_backtest_strategies.py --load-csv spot_usdt

# Load perpetual futures
python crypto\scripts\delta_backtest_strategies.py --load-csv perpetual_usdt

# Load options
python crypto\scripts\delta_backtest_strategies.py --load-csv options_calls
```

### **Interactive Selection:**
```bash
python crypto\scripts\delta_backtest_strategies.py --interactive
```

---

## 🎯 **Key Features**

### **✅ Comprehensive Coverage:**
- Fetches ALL available Delta Exchange pairs
- Categorizes by market type and quote currency
- Includes metadata for each trading pair
- Rate limiting for API compliance

### **✅ Organized Structure:**
- Separate files for each category
- Master summary file for overview
- Timestamped for tracking updates
- UTF-8 encoding for international symbols

### **✅ Error Handling:**
- Connection testing before fetching
- Graceful handling of API errors
- Detailed progress reporting
- Fallback options for missing data

---

## 🔧 **Command Line Options**

```bash
python crypto\scripts\delta_fetch_symbols.py [OPTIONS]

Options:
  --output, -o DIR     Output directory for CSV files (default: ../input)
  --display, -d        Display pair counts without saving files
  --test, -t          Test Delta Exchange connection only
  --verbose, -v       Verbose output with detailed progress
  --help, -h          Show help message
```

---

## 📋 **Example Output**

```
🎯 DELTA EXCHANGE SYMBOL FETCHER
============================================================
📊 Fetch All Trading Pairs | Organize by Category
💾 Create CSV Input Files for Backtesting
============================================================
✅ CCXT library available for Delta Exchange integration
🔗 Connecting to Delta Exchange via CCXT...
📊 Loading Delta Exchange markets...
✅ Delta Exchange connected successfully with rate limiting!
📊 Found 847 total pairs
🔥 Found 463 active pairs
⏱️  Rate limit: 1200ms between requests

📊 Categorizing 463 pairs...

📋 CATEGORIZATION SUMMARY:
   Spot Usdt            : 156 pairs
   Spot Btc             :  23 pairs
   Spot Eth             :  12 pairs
   Perpetual Usdt       :  89 pairs
   Futures Usdt         :  67 pairs
   Options Calls        :  45 pairs
   Options Puts         :  45 pairs
   Other Pairs          :  26 pairs

💾 Saving pairs to CSV files in: d:\AlgoProject\crypto\input
📄 Creating delta_spot_usdt.csv with 156 pairs...
✅ Saved 156 pairs to delta_spot_usdt.csv
[... continues for all categories ...]

💾 EXPORT COMPLETED SUCCESSFULLY!
============================================================
📁 Output Directory: d:\AlgoProject\crypto\input
📋 Files Created:
   📄 delta_spot_usdt.csv        - 156 pairs
   📄 delta_perpetual_usdt.csv   -  89 pairs
   [... all files listed ...]

📊 Summary:
   📋 Summary file: delta_pairs_summary.csv
   🎯 Total pairs exported: 463
   📅 Generated: 2025-07-16 19:59:17
```

---

## 🎉 **Success! Ready to Use**

The `delta_fetch_symbols.py` script is now ready to:

1. **Fetch all 460+ Delta Exchange pairs**
2. **Organize them into categorized CSV files**
3. **Provide input files for your backtesting system**
4. **Support the full Delta Exchange trading ecosystem**

Simply run: `python crypto\scripts\delta_fetch_symbols.py` and your input files will be ready!
