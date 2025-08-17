# AlgoProject Development Rules & Guidelines

## 📋 **Core Development Principles**

This document outlines the essential rules and guidelines for maintaining the AlgoProject codebase. These rules ensure consistency, clean architecture, and proper separation of concerns between crypto and stock trading modules.

---

## 🏗️ **Directory Structure & Separation**

### RULE 1: Maintain Strict Module Separation
```
✅ DO:
- crypto/ scripts MUST use crypto/data_acquisition.py (CCXT only)
- stocks/ scripts MUST use stocks/data_acquisition.py (Fyers API)
- NEVER mix crypto and stock dependencies
- Each module has its own __init__.py with appropriate exports

❌ DON'T:
- Import Fyers API in crypto scripts
- Import CCXT in stock-only scripts
- Use cross-dependencies between modules
- Share data acquisition modules between crypto and stocks
```

### RULE 2: Respect Established Directory Hierarchy
```
AlgoProject/
├── main.py, crypto_launcher.py, crypto_main.py    # Root launchers only
├── crypto/                                        # All crypto-related code
├── stocks/                                        # All stock-related code
├── docs/                                          # Documentation only
├── helper_scripts/                                # ALL test/analysis scripts
│   └── logs/                                      # ALL test and helper script logs
├── venv/                                          # Virtual environment
├── essential files only                           # README, requirements, etc.

🔥 CRITICAL: ALL test, analysis, and temporary scripts MUST go in helper_scripts/
- Never create test files in root directory
- Never create a separate tests/ folder - use helper_scripts/ only
- All test logs go to helper_scripts/logs/
- Check helper_scripts/ first before creating new analysis scripts
- Move any temporary scripts to helper_scripts/ immediately
```
│   ├── data_acquisition.py                       # CCXT only, no stock dependencies
│   ├── scripts/                                   # Crypto trading scripts
│   ├── output/                                    # Crypto results and reports
│   ├── logs/                                      # Crypto logging
│   └── tools/                                     # Crypto utilities
├── stocks/                                        # All stock-related code
│   ├── data_acquisition.py                       # Fyers API + CCXT for mixed portfolios
│   └── scripts/                                   # Stock trading scripts
├── strategies/                                    # Shared trading strategies
├── utils/                                         # Common utilities
├── docs/                                          # All .md files except README.md
├── helper_scripts/                                # Non-essential .bat files
└── venv/                                          # Python virtual environment
```

### RULE 3: Keep Root Directory Clean
```
✅ ALLOWED IN ROOT:
- Essential launcher files only (main.py, crypto_launcher.py, crypto_main.py)
- setup.bat, requirements.txt, README.md, LICENSE, .gitignore

❌ NOT ALLOWED IN ROOT:
- Test files (_test.py, _demo.py)
- Helper .bat files (move to helper_scripts/)
- Documentation files (move to docs/)
- Data or output files
- Temporary or experimental scripts
```

---

## 🔧 **File Management & Cleanup**

### RULE 4: Delete Test Files After Validation
```
✅ PROCESS:
1. Create test files for validation
2. Test and fix issues
3. Apply fixes to production files
4. DELETE test files immediately
5. Update final production files with tested fixes

❌ AVOID:
- Leaving _test.py, _demo.py files in the codebase
- Duplicate files with similar functionality
- Legacy files that are no longer used
```

### RULE 5: Consistent Import Patterns
```python
# ✅ CORRECT IMPORTS:

# Crypto scripts:
from crypto.data_acquisition import fetch_data

# Stock scripts:
from stocks.data_acquisition import fetch_data

# Strategies:
from strategies.strategy_name import StrategyClass

# ❌ NEVER USE:
from tools.data_acquisition import fetch_data  # (This file was removed)
```

---

## 💻 **Coding Standards & Best Practices**

### RULE 6: Professional Console Output
```python
# ✅ GOOD EXAMPLES:
print("🚀 Starting crypto backtest analysis...")
print("✅ SUCCESS: Data fetched successfully from Kraken")
print("❌ ERROR: Connection failed - retrying in 5 seconds")
print("⚠️  WARNING: Low data quality detected for BTC/USDT")
print("📊 Processing 5 symbols with RSI_MACD_VWAP strategy")

# ❌ BAD EXAMPLES:
print("starting")
print("error")
print("done")
```

### RULE 7: Comprehensive Logging
```python
# ✅ REQUIRED LOGGING:
import logging

logger = logging.getLogger(__name__)

# Log all data operations
logger.info(f"🔄 Fetching {symbol} from {exchange} - {bars} bars")
logger.info(f"✅ Successfully fetched {len(data)} bars in {elapsed:.2f}s")
logger.error(f"❌ Failed to fetch {symbol}: {error}")
logger.warning(f"⚠️  Timeout occurred for {symbol} - using cached data")

# Include context in logs
logger.info(f"📊 Starting backtest: {strategy} on {len(symbols)} symbols")
logger.info(f"💰 Trade executed: {symbol} {action} at ${price:.2f}")
```

### RULE 8: Error Handling & Validation
```python
# ✅ PROPER ERROR HANDLING:
def fetch_crypto_data(symbol, exchange, bars):
    """Fetch crypto data with comprehensive error handling."""
    try:
        # Validate inputs
        if not symbol or not exchange:
            raise ValueError("Symbol and exchange are required")
        
        if bars <= 0:
            raise ValueError("Bars must be positive")
        
        # Attempt data fetch with timeout
        data = exchange_api.fetch_ohlcv(symbol, limit=bars)
        
        if data is None or len(data) == 0:
            logger.warning(f"⚠️  No data returned for {symbol}")
            return pd.DataFrame()
        
        logger.info(f"✅ Fetched {len(data)} bars for {symbol}")
        return process_data(data)
        
    except Exception as e:
        logger.error(f"❌ Error fetching {symbol}: {e}")
        # Provide fallback or graceful degradation
        return pd.DataFrame()
```

---

## 🚀 **Module-Specific Rules**

### RULE 9: Crypto Module Independence
```python
# ✅ CRYPTO SCRIPTS MUST:
from crypto.data_acquisition import fetch_data  # CCXT only
from crypto.tools.backtest_evaluator import BacktestEvaluator

# Test crypto independence:
def test_crypto_independence():
    """Ensure crypto scripts work without stock dependencies."""
    try:
        from crypto.data_acquisition import fetch_data
        data = fetch_data('BTC/USDT', 'kraken', '1h', 24)
        print("✅ Crypto module is independent")
    except ImportError as e:
        if 'fyers' in str(e).lower():
            print("❌ FAILED: Crypto module has stock dependencies")
            raise
```

### RULE 10: Launcher Hierarchy Respect
```
🎯 LAUNCHER FLOW:
main.py (unified entry) 
    ↓ [calls]
crypto_launcher.py (full platform)
    ↓ [option 10 launches]
crypto_main.py (diagnostics)

PURPOSE SEPARATION:
- main.py: Complete platform access, project management
- crypto_launcher.py: Advanced crypto trading with full menu system  
- crypto_main.py: Fast diagnostics and system validation
```

### RULE 11: Data Acquisition Consistency
```python
# ✅ BOTH MODULES MUST HAVE:

# crypto/data_acquisition.py
def fetch_data(symbol, exchange, interval, bars, data_source="auto", fetch_timeout=15):
    """Pure CCXT implementation - no stock dependencies."""

def health_check():
    """Crypto module health check."""

# stocks/data_acquisition.py  
def fetch_data(symbol, exchange, interval, bars, data_source="auto", fetch_timeout=15):
    """Fyers API + CCXT for mixed portfolios."""

def health_check():
    """Stocks module health check."""
```

---

## 📊 **Output & Results Management**

### RULE 12: Centralized Output Locations
```
✅ OUTPUT STRUCTURE:
crypto/output/          # All crypto trading results
crypto/logs/           # All crypto logging
stocks/output/         # All stock trading results (if exists)
stocks/logs/          # All stock logging (if exists)

❌ NEVER:
output/ (root)        # Scattered output files
logs/ (root)          # Mixed logging
random locations      # Inconsistent file placement
```

### RULE 13: Consistent File Naming
```python
# ✅ GOOD FILE NAMING:
def save_backtest_results(results, strategy, timestamp):
    """Save with descriptive, timestamped filenames."""
    filename = f"backtest_{strategy}_{timestamp.strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join("crypto/output", filename)
    results.to_csv(filepath, index=False)
    logger.info(f"💾 Results saved: {filepath}")

# Examples:
# backtest_RSI_MACD_VWAP_20250715_143022.csv
# trades_BB_RSI_BTC_USDT_20250715_143022.csv
# live_scan_results_20250715_143022.csv
```

---

## 🧪 **Testing & Validation**

### RULE 14: Test Module Separation
```python
# ✅ REQUIRED TESTS:
def test_crypto_no_fyers_dependency():
    """Ensure crypto scripts never import Fyers."""
    try:
        from crypto.data_acquisition import fetch_data
        # This should work without any Fyers imports
        assert True
    except ImportError as e:
        if 'fyers' in str(e).lower():
            pytest.fail("❌ Crypto module has Fyers dependency")

def test_launcher_hierarchy():
    """Test launcher execution flow."""
    # main.py → crypto_launcher.py → crypto_main.py
    pass

def test_output_paths():
    """Ensure outputs go to correct directories."""
    # crypto results → crypto/output/
    # crypto logs → crypto/logs/
    pass
```

### RULE 15: Performance Validation
```python
# ✅ PERFORMANCE CHECKS:
def validate_data_fetch_performance():
    """Test data fetching speed and reliability."""
    start_time = time.time()
    data = fetch_data('BTC/USDT', 'kraken', '1h', 100)
    elapsed = time.time() - start_time
    
    assert data is not None, "Data fetch failed"
    assert len(data) > 0, "No data returned"
    assert elapsed < 30, f"Fetch took too long: {elapsed}s"
    
    logger.info(f"⚡ Data fetch performance: {elapsed:.2f}s for 100 bars")
```

---

## 📝 **Documentation & Updates**

### RULE 16: Keep README.md Current
```markdown
✅ README.md MUST INCLUDE:
- Current launcher hierarchy documentation
- Accurate module separation descriptions  
- Working command examples
- Up-to-date project structure
- Clear usage instructions

✅ UPDATE README.md WHEN:
- Adding new launchers or scripts
- Changing module structure
- Modifying data acquisition methods
- Adding new features or strategies
```

### RULE 17: Code Documentation Standards
```python
# ✅ REQUIRED DOCUMENTATION:
def fetch_crypto_data(symbol: str, exchange: str, interval: str, bars: int) -> pd.DataFrame:
    """
    Fetch cryptocurrency OHLCV data using CCXT.
    
    This function provides pure crypto data acquisition without any stock
    market dependencies. It uses CCXT library for multiple exchange support.
    
    Args:
        symbol (str): Trading pair symbol (e.g., 'BTC/USDT')
        exchange (str): Exchange name (e.g., 'kraken', 'binance') 
        interval (str): Time interval ('1m', '5m', '1h', '1d')
        bars (int): Number of historical bars to fetch
        
    Returns:
        pd.DataFrame: OHLCV data with timestamp index
        
    Raises:
        ValueError: If invalid parameters provided
        ConnectionError: If exchange connection fails
        
    Example:
        >>> data = fetch_crypto_data('BTC/USDT', 'kraken', '1h', 24)
        >>> print(f"Fetched {len(data)} hourly bars")
    """
```

---

## 🎯 **Quick Reference Checklist**

### Before Making Changes:
- [ ] Understand which module (crypto vs stocks) is affected
- [ ] Check if changes maintain module separation
- [ ] Verify import statements follow correct patterns
- [ ] Ensure no cross-dependencies are introduced

### Before Committing Code:
- [ ] Delete any test files created during development
- [ ] Update production files with tested fixes
- [ ] Verify console output uses professional messaging
- [ ] Check logging is comprehensive and structured
- [ ] Confirm outputs go to correct directories
- [ ] Update documentation if structure changed

### Testing Checklist:
- [ ] Crypto scripts work without Fyers dependencies
- [ ] Stock scripts work with Fyers API
- [ ] Launcher hierarchy functions correctly
- [ ] Data acquisition modules work independently
- [ ] Output files save to correct locations
- [ ] Error handling provides helpful messages

---

## 🚨 **Common Mistakes to Avoid**

### ❌ **NEVER DO THIS:**
```python
# Don't mix dependencies
from crypto.data_acquisition import fetch_data
from stocks.fyers_data_provider import FyersDataProvider  # ❌ Wrong!

# Don't leave test files
crypto_backtest_test.py      # ❌ Delete after testing
demo_live_test.py           # ❌ Delete after testing

# Don't use unclear console output
print("done")               # ❌ Not descriptive
print("error")              # ❌ No context

# Don't put outputs in wrong places
./output/crypto_results.csv # ❌ Should be crypto/output/
./backtest_log.txt          # ❌ Should be crypto/logs/
```

### ✅ **ALWAYS DO THIS:**
```python
# Clean module separation
from crypto.data_acquisition import fetch_data  # ✅ Crypto scripts only

# Professional output
print("✅ SUCCESS: Backtest completed with 85% win rate")  # ✅ Clear and informative

# Correct file paths
os.path.join("crypto", "output", "backtest_results.csv")  # ✅ Proper location
```

---

## 💡 **Memory Aids for Developers**

When working on AlgoProject, remember these key principles:

1. **🔒 Separation**: Crypto and stocks are completely separate ecosystems
2. **🧹 Cleanliness**: Root directory stays minimal and organized  
3. **📝 Clarity**: Every message and log entry should be self-explanatory
4. **🎯 Purpose**: Each file serves a specific, well-defined purpose
5. **🔄 Testing**: Always test module independence after changes
6. **📊 Structure**: Outputs and logs go to designated module directories
7. **📚 Documentation**: Keep README.md and code comments current

---

**Last Updated:** July 15, 2025  
**Version:** 1.0  
**Applies to:** AlgoProject v1.0+
