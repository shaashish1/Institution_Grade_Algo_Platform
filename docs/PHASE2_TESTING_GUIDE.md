# Market & Mode Selector - Testing Guide

## 🧪 How to Test

### Prerequisites
- ✅ Backend running on http://localhost:8000
- ✅ Frontend running on http://localhost:3000
- ✅ Browser open (Chrome/Edge/Firefox)

---

## Test 1: Initial State

1. Open http://localhost:3000 in browser
2. **Look at top-right navigation bar**
3. You should see two selector buttons:
   - **"NSE Stocks"** (with TrendingUp icon)
   - **"Paper Trading"** (with Activity icon in yellow)

**Expected Result**: ✅ Both selectors visible and showing defaults

---

## Test 2: Market Switching

1. **Click on "NSE Stocks" button**
2. Dropdown appears with 2 options:
   - NSE Stocks (Indian Stock Market) ← Green dot (selected)
   - Cryptocurrency (Digital Assets)

3. **Click on "Cryptocurrency"**
4. Dropdown closes
5. Button text changes to "Cryptocurrency"
6. Icon changes to Bitcoin

**Expected Result**: ✅ Market switched from NSE to Crypto

---

## Test 3: Mode Switching

1. **Click on "Paper Trading" button**
2. Dropdown appears with 3 options:
   - Backtest (Database icon, blue)
   - Paper Trading (Activity icon, yellow) ← Green dot
   - Live Trading (Zap icon, red)

3. **Click on "Live Trading"**
4. Dropdown closes
5. Button shows "Live Trading" in red
6. Icon changes to Zap (lightning bolt)

**Expected Result**: ✅ Mode switched to Live

---

## Test 4: Persistence Across Pages

1. Switch to Market: **Crypto**, Mode: **Backtest**
2. Navigate to **/trading** page
3. Look under the page title
4. You should see: "Trading: Crypto • Mode: Backtest" (in blue)

5. Navigate to **/** (home page)
6. Check top bar selectors
7. Should still show: "Cryptocurrency" and "Backtest"

**Expected Result**: ✅ Context preserved across navigation

---

## Test 5: Persistence Across Reloads

1. Set Market: **NSE**, Mode: **Live**
2. Note the current selection
3. **Refresh the page** (F5 or Ctrl+R)
4. Wait for page to load
5. Check selectors again

**Expected Result**: ✅ Still shows NSE and Live after reload

---

## Test 6: Browser Close/Reopen

1. Set Market: **Crypto**, Mode: **Paper**
2. **Close the browser tab completely**
3. **Reopen** http://localhost:3000
4. Check selectors

**Expected Result**: ✅ Shows Crypto and Paper (localStorage works)

---

## Test 7: Backend Sync

1. Switch to Market: **NSE**, Mode: **Backtest**
2. Open DevTools (F12)
3. Go to **Network** tab
4. Switch mode to **Live**
5. Look for POST request to `/api/user/preferences`

**Expected Request**:
```
POST http://localhost:8000/api/user/preferences
Content-Type: application/json

{
  "market": "NSE",
  "mode": "Live",
  "timestamp": "2025-10-22T..."
}
```

6. Check **Response** (should be 200 OK):
```json
{
  "market": "NSE",
  "mode": "Live",
  "timestamp": "2025-10-22T..."
}
```

**Expected Result**: ✅ Backend API called and responded successfully

---

## Test 8: File Storage

1. Switch to Market: **Crypto**, Mode: **Paper**
2. Wait 2 seconds
3. Navigate to project root directory
4. Check if file exists: `user_preferences.json`

**Expected File Content**:
```json
{
  "market": "Crypto",
  "mode": "Paper",
  "timestamp": "2025-10-22T12:00:00"
}
```

**Expected Result**: ✅ Preferences stored in JSON file

---

## Test 9: localStorage Check

1. Switch to Market: **NSE**, Mode: **Live**
2. Open DevTools (F12)
3. Go to **Application** tab
4. Expand **Local Storage** > `http://localhost:3000`
5. Look for these keys:
   - `trading_market` → "NSE"
   - `trading_mode` → "Live"
   - `trading_last_synced` → ISO timestamp

**Expected Result**: ✅ All three keys present with correct values

---

## Test 10: Sync Status Indicator

1. Watch the top bar when switching
2. When you click to change Market or Mode
3. You should briefly see:
   - **Blue pulsing dot** + "Syncing..." text
   - Appears to the right of mode selector
   - Disappears after <1 second

**Expected Result**: ✅ Sync indicator shows and hides

---

## Test 11: Multiple Rapid Switches

1. **Quickly switch** Market: NSE → Crypto → NSE → Crypto
2. Wait 2 seconds
3. Check final selection
4. Reload page
5. Verify final selection persisted

**Expected Result**: ✅ Final selection saved correctly (no race conditions)

---

## Test 12: Trading Page Context Display

1. Navigate to http://localhost:3000/trading
2. Look under the "Live Trading Dashboard" title
3. You should see:
   ```
   Trading: [Market Name]  •  Mode: [Mode Name]
   ```
4. Mode name color:
   - **Red** if Live
   - **Yellow** if Paper
   - **Blue** if Backtest

5. Switch mode in top bar
6. Context indicator updates immediately

**Expected Result**: ✅ Context displayed and updates in real-time

---

## Test 13: API Status Endpoint

1. Open browser and navigate to:
   ```
   http://localhost:8000/api/user/preferences/status
   ```

2. You should see JSON response:
```json
{
  "storage": "file",
  "storage_location": "C:\\Users\\...\\user_preferences.json",
  "file_exists": true,
  "last_modified": "2025-10-22T...",
  "status": "operational"
}
```

**Expected Result**: ✅ Status endpoint returns correct information

---

## Test 14: API Docs

1. Navigate to http://localhost:8000/docs
2. Scroll down to **"User Preferences"** section
3. You should see 3 endpoints:
   - `GET /api/user/preferences`
   - `POST /api/user/preferences`
   - `GET /api/user/preferences/status`

4. **Try the GET endpoint**:
   - Click "Try it out"
   - Click "Execute"
   - Should return current preferences

5. **Try the POST endpoint**:
   - Click "Try it out"
   - Edit the request body (change market or mode)
   - Click "Execute"
   - Should return 200 OK with updated preferences

**Expected Result**: ✅ All API endpoints functional in Swagger UI

---

## Test 15: Console Logging

1. Open DevTools Console (F12 → Console tab)
2. Switch Market from NSE to Crypto
3. You should see console logs:
   ```
   💾 Saved to localStorage: { market: 'Crypto', mode: 'Paper' }
   🔄 Market changed: Crypto
   ✅ Synced to backend: { market: 'Crypto', mode: 'Paper' }
   ```

**Expected Result**: ✅ Detailed logging helps with debugging

---

## 🐛 Troubleshooting

### Issue: Selectors not visible
**Solution**: Check if frontend compiled without errors. Look for console errors.

### Issue: Dropdown not opening
**Solution**: Check browser console for React errors. Verify z-index not conflicting.

### Issue: Changes not persisting
**Solution**: Check localStorage is enabled. Check backend API is running.

### Issue: Backend sync failing
**Solution**: Verify backend running on port 8000. Check CORS settings.

### Issue: Context not updating across pages
**Solution**: Verify TradingProvider wraps the entire app in layout.tsx

---

## ✅ All Tests Passing?

If all 15 tests pass, Phase 2 is **100% complete** and ready for production! 🎉

---

## 🔍 Manual Inspection Checklist

- [ ] Selectors visible in top navigation bar
- [ ] Market dropdown shows NSE and Crypto options
- [ ] Mode dropdown shows Backtest, Paper, Live options
- [ ] Icons display correctly
- [ ] Colors match design (blue/yellow/red)
- [ ] Hover effects work smoothly
- [ ] Active selection has green dot
- [ ] Dropdowns close when clicking outside
- [ ] Context persists on page reload
- [ ] Context persists on browser close/reopen
- [ ] Trading page shows context indicator
- [ ] Backend API responds to requests
- [ ] localStorage contains correct keys
- [ ] File `user_preferences.json` created
- [ ] No console errors
- [ ] Sync indicator appears briefly

**All checked?** → Phase 2 COMPLETE! ✅
