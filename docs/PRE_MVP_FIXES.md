# Pre-MVP Critical Fixes - Implementation Plan

**Date**: October 22, 2025  
**Status**: In Progress

---

## 🎯 Issues to Fix

### Fix 1: Header Menu Consistency ❌
**Problem**: Landing page uses `<Header />` while other pages use `<MegaMenu />`  
**Impact**: Inconsistent navigation experience

**Solution**:
- Replace landing page Header with MegaMenu
- Ensure MegaMenu works on all pages
- Make menu sticky/fixed on scroll

---

### Fix 2: 404 Pages ❌
**Problem**: Many menu links lead to 404 pages  
**Impact**: Poor user experience, broken navigation

**Missing Pages Found**:
- `/analysis`
- `/orders`
- `/risk`
- `/backtest`
- `/charts`
- `/stocks/derivatives`
- `/stocks/etf`
- `/crypto/backtest`
- `/stocks/backtest/multi-strategy`
- `/stocks/backtest/universal`
- `/ai/strategies` (exists but empty)
- `/dashboard`
- `/analytics`
- `/reports`

**Solution**:
- Create placeholder pages for missing routes
- Add "Coming Soon" component
- Update menu to hide incomplete features

---

### Fix 3: Menu Layout & Word Wrap 🔴 CRITICAL
**Problem**: NSE/Crypto selector wraps to 2 lines, menu looks cluttered  
**Impact**: Unprofessional appearance

**Current Issue**:
```
[NSE Stocks    ▼]  [Paper Trading ▼]
```
Becomes:
```
[NSE 
 Stocks ▼]
```

**Solution**:
- Make selector compact with icons only on mobile
- Use single-line layout
- Add proper icon spacing
- Improve responsive breakpoints

---

### Fix 4: Data Feed Validation 🔴 CRITICAL
**Problem**: Need to verify data is flowing correctly to UI  
**Impact**: Platform unusable without real data

**Tasks**:
- Test NSE Free Provider → API → Frontend
- Test FYERS Provider (if configured)
- Test CCXT Crypto data
- Verify all hooks working
- Check data refresh rates

---

### Fix 5: Backend Scripts Inventory 📊
**Problem**: No clear list of what scripts do what  
**Impact**: Hard to maintain, unclear capabilities

**Scripts to Document**:

**API Scripts** (`api/`):
- `main.py` - Main FastAPI application
- `market_data_api.py` - Market data endpoints
- `settings_api.py` - Exchange settings
- `user_preferences_api.py` - User preferences
- `ccxt_service.py` - CCXT exchange service
- `fyers_user_service.py` - FYERS user management
- `fyers_data_service.py` - FYERS data provider

**Stock Scripts** (`stocks/`):
- `nse_free_data_provider.py` - FREE NSE data (PRIMARY)
- `fyers_data_provider.py` - FYERS NSE/BSE data
- `live_nse_quotes.py` - Live quotes
- `data_acquisition.py` - Generic data fetcher

**Crypto Scripts** (`crypto/`):
- TBD

---

### Fix 6: Scripts Documentation Page 📚
**Problem**: No centralized documentation for backend capabilities  
**Impact**: Hard for users to understand what's available

**Solution**:
- Create `/docs/backend-scripts` page
- List all scripts with:
  - Name & Path
  - Purpose
  - Features
  - Data capabilities
  - Usage examples

---

### Fix 7: Live Mode Validation ⚡ CRITICAL
**Problem**: Users can switch to Live mode without exchange setup  
**Impact**: Confusion, potential errors

**Solution**:
- Add validation in TradingContext
- Check exchange configuration status
- Show modal/redirect to settings if not configured
- Display clear instructions
- Add warning dialog before enabling Live mode

---

## 🚀 Implementation Order

1. **Fix 3** (Menu Layout) - 1-2 hours ⚡ HIGH
2. **Fix 1** (Header Consistency) - 1 hour
3. **Fix 7** (Live Mode Validation) - 2 hours ⚡ HIGH
4. **Fix 4** (Data Feed Validation) - 2-3 hours ⚡ HIGH
5. **Fix 2** (404 Pages) - 2-3 hours
6. **Fix 5** (Scripts Inventory) - 1 hour
7. **Fix 6** (Documentation Page) - 2 hours

**Total**: ~12-14 hours (1.5-2 days)

---

## ✅ Success Criteria

- [ ] MegaMenu on all pages including landing
- [ ] No 404 errors when clicking menu items
- [ ] Menu stays in single line on desktop
- [ ] Live NSE data flowing to UI
- [ ] Live Crypto data flowing to UI
- [ ] All backend scripts documented
- [ ] Live mode validation working
- [ ] Professional, consistent UI

---

**Next**: Start with Fix 3 (Menu Layout) as it's most visible
