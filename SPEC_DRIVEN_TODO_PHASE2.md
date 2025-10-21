# 🎯 Spec-Driven Todo List - Phase 2

**Created:** October 21, 2025  
**Approach:** Frontend-Backend Alignment with API Specifications  
**Status:** Ready for Implementation

---

## 🚨 CRITICAL FIXES (DO FIRST)

### 1. Fix "Failed to fetch" Navigation Errors ⚠️ **URGENT**
**Priority:** P0 - BLOCKING  
**Time Estimate:** 1-2 hours  
**Status:** 🔴 Not Started

**Issue:** Next.js router failing to fetch page data due to missing API routes

**Spec Requirements:**
```typescript
// Fix navigation errors by creating proper API route handlers
// Location: frontend/src/app/api/
```

**Tasks:**
- [ ] Create `frontend/src/app/api/route.ts` for health check
- [ ] Add proper error boundaries in layout
- [ ] Configure Next.js for client-side navigation
- [ ] Fix prefetch cache issues
- [ ] Add fallback pages for missing routes

**Acceptance Criteria:**
- ✅ No console errors on navigation
- ✅ All internal links work
- ✅ Smooth page transitions
- ✅ No "Failed to fetch" errors

**Files to Create/Modify:**
```
frontend/src/app/api/health/route.ts
frontend/src/app/error.tsx
frontend/src/app/not-found.tsx
frontend/src/middleware.ts (if needed)
```

---

## 📊 SPEC-ALIGNED FEATURES

### 2. API Route Specifications & Implementation
**Priority:** P0 - CRITICAL  
**Time Estimate:** 4-6 hours  
**Status:** 🔴 Not Started

**Spec:** Create RESTful API routes for frontend-backend communication

#### 2.1 FYERS API Routes
**Endpoint Spec:**
```typescript
// GET /api/fyers/credentials/:userId
// POST /api/fyers/credentials
// GET /api/fyers/status/:userId
// POST /api/fyers/test-connection/:userId
// DELETE /api/fyers/credentials/:userId
```

**Files to Create:**
```
frontend/src/app/api/fyers/credentials/route.ts
frontend/src/app/api/fyers/credentials/[userId]/route.ts
frontend/src/app/api/fyers/status/[userId]/route.ts
frontend/src/app/api/fyers/test-connection/[userId]/route.ts
```

#### 2.2 Exchange API Routes (CCXT)
**Endpoint Spec:**
```typescript
// GET /api/exchanges - List all exchanges
// GET /api/exchanges/:exchangeId - Exchange details
// GET /api/markets/:exchangeId - Market list
// GET /api/ticker/:exchangeId/:symbol - Ticker data
// GET /api/orderbook/:exchangeId/:symbol - Order book
// GET /api/trades/:exchangeId/:symbol - Recent trades
```

**Files to Create:**
```
frontend/src/app/api/exchanges/route.ts
frontend/src/app/api/exchanges/[exchangeId]/route.ts
frontend/src/app/api/markets/[exchangeId]/route.ts
frontend/src/app/api/ticker/[exchangeId]/[symbol]/route.ts
frontend/src/app/api/orderbook/[exchangeId]/[symbol]/route.ts
frontend/src/app/api/trades/[exchangeId]/[symbol]/route.ts
```

#### 2.3 Health Check Routes
**Endpoint Spec:**
```typescript
// GET /api/health - Overall health
// GET /api/health/ccxt - CCXT service health
// GET /api/health/fyers - FYERS service health
```

**Files to Create:**
```
frontend/src/app/api/health/route.ts
frontend/src/app/api/health/ccxt/route.ts
frontend/src/app/api/health/fyers/route.ts
```

**Acceptance Criteria:**
- ✅ All API routes return proper JSON responses
- ✅ Error handling with proper status codes
- ✅ TypeScript types for requests/responses
- ✅ CORS configured correctly
- ✅ Rate limiting implemented

---

### 3. Settings Page with API Integration
**Priority:** P1 - HIGH  
**Time Estimate:** 6-8 hours  
**Status:** 🟡 Planned

**Spec:** Complete settings interface with backend persistence

#### 3.1 Frontend Spec
**Component Structure:**
```
frontend/src/app/settings/
├── page.tsx                    # Main settings page
├── layout.tsx                  # Settings layout
└── components/
    ├── theme-selector.tsx      # Theme selection
    ├── api-keys-manager.tsx    # API key management
    ├── preferences.tsx         # User preferences
    └── notification-settings.tsx # Notifications
```

**State Management:**
```typescript
interface SettingsState {
  theme: 'light' | 'dark' | 'cosmic' | 'doodle';
  apiKeys: {
    fyers: { clientId: string; secretKey: string; };
    binance?: { apiKey: string; secretKey: string; };
  };
  preferences: {
    language: string;
    timezone: string;
    currency: string;
    notifications: boolean;
  };
}
```

#### 3.2 Backend Spec
**API Endpoints:**
```typescript
// GET /api/settings/:userId - Get user settings
// PUT /api/settings/:userId - Update settings
// POST /api/settings/:userId/reset - Reset to defaults
```

**Files to Create:**
```
frontend/src/app/api/settings/[userId]/route.ts
frontend/src/lib/settings-store.ts
frontend/src/types/settings.ts
```

**Acceptance Criteria:**
- ✅ Theme changes persist across sessions
- ✅ API keys stored securely (encrypted)
- ✅ Form validation on all inputs
- ✅ Real-time preview of changes
- ✅ Export/Import settings functionality

---

### 4. Trading Dashboard with Real-Time Data
**Priority:** P1 - HIGH  
**Time Estimate:** 12-16 hours  
**Status:** 🟡 Planned

**Spec:** Real-time trading dashboard with WebSocket integration

#### 4.1 Frontend Spec
**Component Architecture:**
```
frontend/src/app/dashboard/
├── page.tsx                    # Main dashboard
├── layout.tsx                  # Dashboard layout
└── components/
    ├── price-chart.tsx         # Live price charts
    ├── portfolio-overview.tsx  # Portfolio summary
    ├── positions-table.tsx     # Active positions
    ├── order-panel.tsx         # Place orders
    ├── watchlist.tsx          # Symbol watchlist
    └── market-stats.tsx       # Market statistics
```

**Data Flow Spec:**
```typescript
interface DashboardData {
  portfolio: {
    totalValue: number;
    dailyPnL: number;
    positions: Position[];
  };
  marketData: {
    symbols: Symbol[];
    updates: WebSocketUpdate[];
  };
  orders: Order[];
  trades: Trade[];
}
```

#### 4.2 Backend Spec
**WebSocket Endpoints:**
```typescript
// WS /api/ws/market-data - Real-time prices
// WS /api/ws/portfolio - Portfolio updates
// WS /api/ws/orders - Order updates
```

**REST Endpoints:**
```typescript
// GET /api/portfolio/:userId - Portfolio data
// GET /api/positions/:userId - Active positions
// POST /api/orders - Place order
// DELETE /api/orders/:orderId - Cancel order
// GET /api/trades/:userId - Trade history
```

**Files to Create:**
```
frontend/src/app/api/portfolio/[userId]/route.ts
frontend/src/app/api/positions/[userId]/route.ts
frontend/src/app/api/orders/route.ts
frontend/src/app/api/orders/[orderId]/route.ts
frontend/src/app/api/trades/[userId]/route.ts
frontend/src/lib/websocket-client.ts
frontend/src/hooks/useWebSocket.ts
frontend/src/hooks/useMarketData.ts
```

**Acceptance Criteria:**
- ✅ Real-time price updates (< 100ms latency)
- ✅ Portfolio recalculation on updates
- ✅ Order placement with confirmation
- ✅ P&L tracking (realized & unrealized)
- ✅ Responsive charts (mobile-friendly)
- ✅ WebSocket reconnection logic

---

### 5. Backend CCXT Integration Fix
**Priority:** P1 - HIGH  
**Time Estimate:** 2-4 hours  
**Status:** 🟡 Planned

**Spec:** Optimize cryptocurrency exchange integrations

**Current Issues:**
```python
# crypto/list_crypto_assets.py
# tools/backtest_evaluator.py
# Import errors due to blocking CCXT loads
```

**Solution Spec:**
```python
# Implement lazy loading pattern
class CCXTManager:
    _exchanges = {}
    
    @classmethod
    def get_exchange(cls, exchange_id: str):
        if exchange_id not in cls._exchanges:
            cls._exchanges[exchange_id] = getattr(ccxt, exchange_id)()
        return cls._exchanges[exchange_id]
```

**Files to Modify:**
```
crypto/list_crypto_assets.py
tools/backtest_evaluator.py
crypto/__init__.py
crypto/exchange_manager.py (new)
```

**Tasks:**
- [ ] Create `CCXTManager` class with lazy loading
- [ ] Replace direct imports with manager calls
- [ ] Add error handling for unsupported exchanges
- [ ] Implement connection pooling
- [ ] Add retry logic for API failures

**Acceptance Criteria:**
- ✅ Faster application startup
- ✅ No blocking imports
- ✅ Proper error messages
- ✅ Connection reuse
- ✅ Graceful fallback

---

### 6. WebSocket Integration for Real-Time Data
**Priority:** P2 - MEDIUM  
**Time Estimate:** 8-10 hours  
**Status:** 🟡 Planned

**Spec:** Real-time data streaming architecture

#### 6.1 WebSocket Server Spec
**Backend Setup:**
```python
# api/websocket_server.py
from fastapi import WebSocket
import asyncio

class MarketDataStreamer:
    async def stream_prices(websocket: WebSocket, symbols: list)
    async def stream_orderbook(websocket: WebSocket, symbol: str)
    async def stream_trades(websocket: WebSocket, symbol: str)
```

**Files to Create:**
```
api/websocket_server.py
api/ws_handlers/market_data.py
api/ws_handlers/portfolio.py
api/ws_handlers/orders.py
```

#### 6.2 Frontend WebSocket Client Spec
```typescript
// frontend/src/lib/websocket-client.ts
class WebSocketClient {
  connect(url: string): Promise<void>
  subscribe(channel: string, callback: Function): void
  unsubscribe(channel: string): void
  close(): void
}
```

**Files to Create:**
```
frontend/src/lib/websocket-client.ts
frontend/src/hooks/useWebSocket.ts
frontend/src/hooks/useMarketData.ts
frontend/src/hooks/usePortfolio.ts
frontend/src/context/websocket-context.tsx
```

**Acceptance Criteria:**
- ✅ Auto-reconnection on disconnect
- ✅ Heartbeat/ping-pong mechanism
- ✅ Message queuing during disconnection
- ✅ Multiple channel subscriptions
- ✅ Proper cleanup on unmount

---

### 7. Advanced Charting with TradingView
**Priority:** P2 - MEDIUM  
**Time Estimate:** 10-12 hours  
**Status:** 🟡 Planned

**Spec:** Integrate TradingView Lightweight Charts

**Component Spec:**
```typescript
interface ChartProps {
  symbol: string;
  interval: '1m' | '5m' | '15m' | '1h' | '4h' | '1d';
  indicators: Indicator[];
  drawings: Drawing[];
}
```

**Files to Create:**
```
frontend/src/components/charts/trading-chart.tsx
frontend/src/components/charts/chart-toolbar.tsx
frontend/src/components/charts/indicators-panel.tsx
frontend/src/components/charts/drawing-tools.tsx
frontend/src/lib/chart-manager.ts
frontend/src/hooks/useChart.ts
```

**Acceptance Criteria:**
- ✅ Real-time price updates on chart
- ✅ Multiple timeframes
- ✅ Technical indicators (MA, RSI, MACD, etc.)
- ✅ Drawing tools (lines, channels, etc.)
- ✅ Chart export functionality
- ✅ Mobile-optimized touch controls

---

### 8. Testing & QA Infrastructure
**Priority:** P2 - MEDIUM  
**Time Estimate:** 8-10 hours  
**Status:** 🟡 Planned

**Spec:** Comprehensive testing coverage

#### 8.1 Unit Tests
**Coverage Target:** 80%

**Test Files to Create:**
```
frontend/src/__tests__/components/
frontend/src/__tests__/hooks/
frontend/src/__tests__/lib/
frontend/src/__tests__/utils/
```

#### 8.2 Integration Tests
**API Testing:**
```typescript
// Test all API routes
describe('API Integration Tests', () => {
  test('GET /api/health returns 200')
  test('POST /api/orders places order')
  test('WebSocket connection succeeds')
})
```

#### 8.3 E2E Tests
**Critical Flows:**
```
- User login flow
- Place order flow
- Portfolio view flow
- Settings update flow
```

**Files to Create:**
```
frontend/e2e/login.spec.ts
frontend/e2e/trading.spec.ts
frontend/e2e/portfolio.spec.ts
frontend/jest.config.js
frontend/playwright.config.ts
```

**Acceptance Criteria:**
- ✅ 80%+ code coverage
- ✅ All critical flows tested
- ✅ CI/CD integration
- ✅ Performance benchmarks

---

## 📋 IMPLEMENTATION ORDER

### Week 1: Foundation (Critical Fixes)
1. **Day 1-2:** Fix navigation errors (Task #1)
2. **Day 3-4:** Create API routes (Task #2)
3. **Day 5:** Backend CCXT fixes (Task #5)

### Week 2: Core Features
1. **Day 1-3:** Settings page (Task #3)
2. **Day 4-5:** Dashboard foundation (Task #4 - part 1)

### Week 3: Real-Time Features
1. **Day 1-3:** WebSocket integration (Task #6)
2. **Day 4-5:** Dashboard real-time data (Task #4 - part 2)

### Week 4: Advanced Features & QA
1. **Day 1-3:** Advanced charting (Task #7)
2. **Day 4-5:** Testing & QA (Task #8)

---

## 📊 PROGRESS TRACKING

### Sprint Metrics
```
Total Tasks: 8
Critical (P0): 2
High (P1): 3
Medium (P2): 3

Estimated Total Time: 53-67 hours
Target Completion: 4 weeks
```

### Definition of Done
- [ ] Code reviewed and approved
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] No TypeScript errors
- [ ] No console errors/warnings
- [ ] Deployed to staging
- [ ] Tested on all browsers
- [ ] Mobile responsive verified

---

## 🔧 TECHNICAL SPECIFICATIONS

### Frontend Tech Stack
```
- Next.js 15.5.6 (App Router)
- React 18.2.0
- TypeScript 5.0
- Tailwind CSS 3.3.0
- TanStack Query (React Query)
- Zustand (State Management)
- Socket.io-client (WebSockets)
```

### Backend Tech Stack
```
- Python 3.14
- FastAPI
- CCXT (Crypto exchanges)
- WebSocket support
- SQLAlchemy (Database)
- Redis (Caching)
```

### API Design Principles
```
1. RESTful endpoints for CRUD operations
2. WebSocket for real-time data
3. Consistent error responses
4. Versioned APIs (/api/v1/)
5. Rate limiting
6. Authentication/Authorization
```

---

## 🎯 SUCCESS CRITERIA

### Phase 2 Complete When:
- ✅ All navigation errors fixed
- ✅ All API routes functional
- ✅ Settings page working with persistence
- ✅ Trading dashboard with real-time data
- ✅ WebSocket streaming operational
- ✅ 80%+ test coverage
- ✅ Zero critical bugs
- ✅ Performance benchmarks met

---

**Document Version:** 1.0  
**Last Updated:** October 21, 2025  
**Owner:** Development Team  
**Status:** Ready for Sprint Planning
