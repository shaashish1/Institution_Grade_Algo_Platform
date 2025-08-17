# 🎨 Frontend Architecture & Design System

## Overview
This document outlines the frontend architecture, design system, and implementation strategy for the AlgoProject web-based trading platform.

## Technology Stack

### Core Framework
- **React 18**: Modern React with hooks and concurrent features
- **Next.js 13**: App Router, SSR, and performance optimization
- **TypeScript**: Type safety and better development experience
- **Tailwind CSS**: Utility-first CSS framework

### State Management
- **Zustand**: Lightweight state management
- **React Query**: Server state management and caching
- **SWR**: Data fetching and synchronization
- **React Hook Form**: Form state management

### UI Components
- **Shadcn/ui**: Modern, accessible component library
- **Recharts**: Trading charts and data visualization
- **Framer Motion**: Smooth animations and transitions
- **Headless UI**: Unstyled, accessible components

### Development Tools
- **ESLint**: Code linting and consistency
- **Prettier**: Code formatting
- **Storybook**: Component documentation
- **Jest**: Unit testing
- **Cypress**: End-to-end testing

## Architecture Overview

### Component Architecture
```
src/
├── components/           # Reusable UI components
│   ├── ui/              # Basic UI components (Button, Input, etc.)
│   ├── layout/          # Layout components (Header, Sidebar, etc.)
│   ├── trading/         # Trading-specific components
│   ├── charts/          # Chart components
│   └── forms/           # Form components
├── pages/               # Next.js pages
├── hooks/               # Custom React hooks
├── services/            # API services and utilities
├── stores/              # Global state management
├── types/               # TypeScript type definitions
├── utils/               # Utility functions
└── styles/              # Global styles and themes
```

### Page Structure
```
app/
├── (auth)/              # Authentication pages
│   ├── login/
│   ├── register/
│   └── forgot-password/
├── (dashboard)/         # Main application
│   ├── dashboard/       # Dashboard overview
│   ├── trading/         # Trading interface
│   ├── strategies/      # Strategy management
│   ├── portfolio/       # Portfolio management
│   ├── analytics/       # Analytics and reports
│   └── settings/        # User settings
├── (marketing)/         # Marketing pages
│   ├── pricing/
│   ├── features/
│   └── about/
└── api/                 # API routes
```

## Design System

### Color Palette
```css
/* Primary Colors */
--primary-50: #f0f9ff;
--primary-100: #e0f2fe;
--primary-500: #0ea5e9;
--primary-600: #0284c7;
--primary-900: #0c4a6e;

/* Success/Profit Colors */
--success-50: #f0fdf4;
--success-500: #10b981;
--success-600: #059669;

/* Error/Loss Colors */
--error-50: #fef2f2;
--error-500: #ef4444;
--error-600: #dc2626;

/* Neutral Colors */
--neutral-50: #fafafa;
--neutral-100: #f5f5f5;
--neutral-500: #737373;
--neutral-900: #171717;
```

### Typography Scale
```css
/* Headings */
--text-xs: 0.75rem;      /* 12px */
--text-sm: 0.875rem;     /* 14px */
--text-base: 1rem;       /* 16px */
--text-lg: 1.125rem;     /* 18px */
--text-xl: 1.25rem;      /* 20px */
--text-2xl: 1.5rem;      /* 24px */
--text-3xl: 1.875rem;    /* 30px */
--text-4xl: 2.25rem;     /* 36px */

/* Font Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### Spacing System
```css
/* Spacing Scale (4px base) */
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
--space-12: 3rem;    /* 48px */
--space-16: 4rem;    /* 64px */
```

## Core Components

### 1. Button Component
```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'outline' | 'ghost';
  size: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  onClick,
  children
}) => {
  // Implementation
};
```

### 2. TradingChart Component
```typescript
interface TradingChartProps {
  data: CandlestickData[];
  indicators?: TechnicalIndicator[];
  height?: number;
  width?: number;
  theme?: 'light' | 'dark';
  onTimeRangeChange?: (range: TimeRange) => void;
}

const TradingChart: React.FC<TradingChartProps> = ({
  data,
  indicators,
  height = 400,
  width = 800,
  theme = 'light',
  onTimeRangeChange
}) => {
  // Implementation using Recharts or TradingView
};
```

### 3. StrategyCard Component
```typescript
interface StrategyCardProps {
  strategy: Strategy;
  isRunning: boolean;
  performance: PerformanceMetrics;
  onStart: () => void;
  onStop: () => void;
  onEdit: () => void;
  onDelete: () => void;
}

const StrategyCard: React.FC<StrategyCardProps> = ({
  strategy,
  isRunning,
  performance,
  onStart,
  onStop,
  onEdit,
  onDelete
}) => {
  // Implementation
};
```

### 4. PortfolioSummary Component
```typescript
interface PortfolioSummaryProps {
  portfolio: Portfolio;
  performance: PerformanceData;
  timeRange: TimeRange;
  onTimeRangeChange: (range: TimeRange) => void;
}

const PortfolioSummary: React.FC<PortfolioSummaryProps> = ({
  portfolio,
  performance,
  timeRange,
  onTimeRangeChange
}) => {
  // Implementation
};
```

## State Management

### Global State Structure
```typescript
interface AppState {
  user: UserState;
  trading: TradingState;
  strategies: StrategyState;
  portfolio: PortfolioState;
  ui: UIState;
}

interface UserState {
  profile: UserProfile | null;
  preferences: UserPreferences;
  subscription: SubscriptionInfo;
}

interface TradingState {
  activePositions: Position[];
  orders: Order[];
  marketData: MarketData;
  selectedAsset: Asset | null;
}

interface StrategyState {
  strategies: Strategy[];
  activeStrategies: string[];
  backtestResults: BacktestResult[];
}

interface PortfolioState {
  holdings: Holding[];
  performance: PerformanceData;
  transactions: Transaction[];
}

interface UIState {
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  activeTab: string;
  notifications: Notification[];
}
```

### State Management Patterns
```typescript
// Using Zustand for global state
const useAppStore = create<AppState>((set, get) => ({
  user: initialUserState,
  trading: initialTradingState,
  strategies: initialStrategyState,
  portfolio: initialPortfolioState,
  ui: initialUIState,
  
  // Actions
  updateUser: (updates) => set((state) => ({
    user: { ...state.user, ...updates }
  })),
  
  setSelectedAsset: (asset) => set((state) => ({
    trading: { ...state.trading, selectedAsset: asset }
  })),
  
  addStrategy: (strategy) => set((state) => ({
    strategies: {
      ...state.strategies,
      strategies: [...state.strategies.strategies, strategy]
    }
  }))
}));

// Using React Query for server state
const useStrategies = () => {
  return useQuery({
    queryKey: ['strategies'],
    queryFn: () => api.getStrategies(),
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
  });
};
```

## Real-time Data Integration

### WebSocket Implementation
```typescript
class WebSocketManager {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  connect(url: string) {
    this.ws = new WebSocket(url);
    
    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
    };
    
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleMessage(data);
    };
    
    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      this.reconnect();
    };
    
    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  private handleMessage(data: any) {
    // Handle different message types
    switch (data.type) {
      case 'MARKET_DATA':
        updateMarketData(data.payload);
        break;
      case 'POSITION_UPDATE':
        updatePosition(data.payload);
        break;
      case 'ORDER_UPDATE':
        updateOrder(data.payload);
        break;
    }
  }

  private reconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      setTimeout(() => {
        this.reconnectAttempts++;
        this.connect(this.ws?.url || '');
      }, this.reconnectDelay * Math.pow(2, this.reconnectAttempts));
    }
  }
}
```

### Real-time Hooks
```typescript
const useRealTimeData = <T>(
  topic: string,
  initialData: T
): [T, boolean] => {
  const [data, setData] = useState<T>(initialData);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const ws = new WebSocketManager();
    
    ws.connect(`${WS_URL}/${topic}`);
    
    ws.onMessage = (message) => {
      setData(message.data);
    };
    
    ws.onConnect = () => setIsConnected(true);
    ws.onDisconnect = () => setIsConnected(false);
    
    return () => ws.disconnect();
  }, [topic]);

  return [data, isConnected];
};
```

## Performance Optimization

### Code Splitting
```typescript
// Lazy loading for route components
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Trading = lazy(() => import('./pages/Trading'));
const Strategies = lazy(() => import('./pages/Strategies'));

// Component-level lazy loading
const TradingChart = lazy(() => import('./components/TradingChart'));
const StrategyBuilder = lazy(() => import('./components/StrategyBuilder'));
```

### Memoization
```typescript
// Memoized components
const MemoizedTradingChart = memo(TradingChart);
const MemoizedStrategyCard = memo(StrategyCard);

// Memoized calculations
const useCalculatedMetrics = (data: MarketData[]) => {
  return useMemo(() => {
    return calculateTechnicalIndicators(data);
  }, [data]);
};
```

### Virtual Scrolling
```typescript
const VirtualizedTable = ({ data, itemHeight = 50 }) => {
  const [scrollTop, setScrollTop] = useState(0);
  const containerHeight = 400;
  
  const startIndex = Math.floor(scrollTop / itemHeight);
  const endIndex = Math.min(
    startIndex + Math.ceil(containerHeight / itemHeight),
    data.length
  );
  
  const visibleItems = data.slice(startIndex, endIndex);
  
  return (
    <div
      style={{ height: containerHeight, overflow: 'auto' }}
      onScroll={(e) => setScrollTop(e.target.scrollTop)}
    >
      <div style={{ height: data.length * itemHeight }}>
        <div style={{ transform: `translateY(${startIndex * itemHeight}px)` }}>
          {visibleItems.map((item, index) => (
            <div key={startIndex + index} style={{ height: itemHeight }}>
              {/* Item content */}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
```

## Responsive Design

### Breakpoint System
```css
/* Tailwind CSS breakpoints */
/* sm: 640px */
/* md: 768px */
/* lg: 1024px */
/* xl: 1280px */
/* 2xl: 1536px */
```

### Mobile-First Approach
```typescript
const ResponsiveLayout = ({ children }) => {
  return (
    <div className="
      grid grid-cols-1 gap-4
      md:grid-cols-2 md:gap-6
      lg:grid-cols-3 lg:gap-8
      xl:grid-cols-4 xl:gap-10
    ">
      {children}
    </div>
  );
};
```

### Adaptive Components
```typescript
const AdaptiveNavigation = () => {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  return isMobile ? <MobileNav /> : <DesktopNav />;
};
```

## Accessibility

### ARIA Implementation
```typescript
const AccessibleButton = ({ 
  children, 
  onClick, 
  disabled = false,
  ariaLabel,
  ...props 
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      aria-label={ariaLabel}
      aria-disabled={disabled}
      role="button"
      tabIndex={disabled ? -1 : 0}
      {...props}
    >
      {children}
    </button>
  );
};
```

### Keyboard Navigation
```typescript
const KeyboardHandler = ({ children }) => {
  const handleKeyDown = (e: KeyboardEvent) => {
    switch (e.key) {
      case 'Tab':
        // Handle tab navigation
        break;
      case 'Enter':
      case ' ':
        // Handle activation
        break;
      case 'Escape':
        // Handle escape
        break;
    }
  };

  return (
    <div onKeyDown={handleKeyDown}>
      {children}
    </div>
  );
};
```

## Testing Strategy

### Unit Testing
```typescript
// Component testing with Jest and React Testing Library
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Integration Testing
```typescript
// API integration testing
import { renderHook, waitFor } from '@testing-library/react';
import { useStrategies } from './hooks/useStrategies';

describe('useStrategies', () => {
  it('fetches strategies successfully', async () => {
    const { result } = renderHook(() => useStrategies());
    
    await waitFor(() => {
      expect(result.current.data).toBeDefined();
      expect(result.current.isLoading).toBe(false);
    });
  });
});
```

### End-to-End Testing
```typescript
// Cypress E2E testing
describe('Trading Flow', () => {
  it('should create and execute a strategy', () => {
    cy.visit('/strategies');
    cy.get('[data-testid="create-strategy"]').click();
    cy.get('[data-testid="strategy-name"]').type('Test Strategy');
    cy.get('[data-testid="save-strategy"]').click();
    cy.get('[data-testid="start-strategy"]').click();
    cy.get('[data-testid="strategy-status"]').should('contain', 'Running');
  });
});
```

## Deployment Strategy

### Build Configuration
```javascript
// next.config.js
module.exports = {
  output: 'standalone',
  compress: true,
  poweredByHeader: false,
  
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    NEXT_PUBLIC_WS_URL: process.env.NEXT_PUBLIC_WS_URL,
  },
  
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.API_URL}/:path*`,
      },
    ];
  },
};
```

### Container Configuration
```dockerfile
# Dockerfile
FROM node:18-alpine AS base

# Install dependencies
FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Build application
FROM base AS builder
WORKDIR /app
COPY . .
RUN npm run build

# Production image
FROM base AS runner
WORKDIR /app
ENV NODE_ENV production
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT 3000

CMD ["node", "server.js"]
```

## Security Considerations

### Authentication & Authorization
```typescript
// JWT token management
const useAuth = () => {
  const [token, setToken] = useState<string | null>(null);
  
  const login = async (credentials: LoginCredentials) => {
    const response = await api.login(credentials);
    setToken(response.token);
    localStorage.setItem('token', response.token);
  };
  
  const logout = () => {
    setToken(null);
    localStorage.removeItem('token');
  };
  
  return { token, login, logout };
};
```

### Input Validation
```typescript
// Form validation with Zod
import { z } from 'zod';

const strategySchema = z.object({
  name: z.string().min(1, 'Name is required').max(100),
  type: z.enum(['buy', 'sell', 'both']),
  parameters: z.object({
    stopLoss: z.number().positive(),
    takeProfit: z.number().positive(),
  }),
});

const StrategyForm = () => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(strategySchema),
  });
  
  // Form implementation
};
```

### Content Security Policy
```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: `
              default-src 'self';
              script-src 'self' 'unsafe-eval' 'unsafe-inline';
              style-src 'self' 'unsafe-inline';
              connect-src 'self' ${process.env.NEXT_PUBLIC_API_URL};
            `.replace(/\s+/g, ' ').trim(),
          },
        ],
      },
    ];
  },
};
```

## Conclusion

This frontend architecture provides a solid foundation for building a modern, scalable, and maintainable trading platform. The combination of React, Next.js, and TypeScript ensures type safety and developer productivity, while the component-based architecture allows for easy testing and reusability.

The focus on performance, accessibility, and security ensures that the platform will provide an excellent user experience while maintaining enterprise-grade reliability and security standards.

---

*For backend integration details, see [PRODUCT_REQUIREMENTS.md](PRODUCT_REQUIREMENTS.md) and [UI_UX_DESIGN.md](UI_UX_DESIGN.md)*
