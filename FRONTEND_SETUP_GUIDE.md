# 🎨 AlgoProject Frontend Setup Guide

## Overview
This guide will help you set up a modern React/Next.js frontend for your AlgoProject trading platform using Figma MCP server integration through VS Code AI Toolkit.

## 🔧 Prerequisites

### Required Software
- **Node.js 18+** - [Download here](https://nodejs.org/)
- **VS Code** with AI Toolkit extension
- **Git** for version control
- **PowerShell** (Windows)

### Environment Setup
1. **Figma Personal Access Token**
   - Go to [Figma.com](https://figma.com) → Settings → Personal Access Tokens
   - Generate a new token for MCP server access

2. **Figma File Key**
   - Open your Figma design file
   - Copy the file ID from URL: `figma.com/file/[FILE_KEY]/...`

## 🚀 Quick Setup

### Step 1: Configure Figma MCP Environment
```powershell
# Run the setup script to configure environment variables
.\setup_figma_env.bat

# Restart VS Code after setting environment variables
```

### Step 2: Install Frontend Dependencies
```powershell
# Navigate to frontend directory
cd frontend

# Install all dependencies
npm install

# Install additional development dependencies
npm install -D @types/react @types/react-dom next-themes
```

### Step 3: Start Development Server
```powershell
# Start the Next.js development server
npm run dev

# The frontend will be available at http://localhost:3000
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js 13 App Router
│   │   ├── layout.tsx         # Root layout component
│   │   └── page.tsx           # Home page
│   ├── components/            # React components
│   │   ├── dashboard.tsx      # Main dashboard container
│   │   ├── layout/            # Layout components
│   │   │   ├── header.tsx     # Top navigation
│   │   │   └── sidebar.tsx    # Side navigation
│   │   ├── trading/           # Trading interface
│   │   │   ├── trading-view.tsx
│   │   │   ├── trading-chart.tsx
│   │   │   ├── market-data.tsx
│   │   │   └── order-book.tsx
│   │   ├── portfolio/         # Portfolio management
│   │   ├── strategies/        # Strategy builder
│   │   ├── analytics/         # Analytics dashboard
│   │   └── settings/          # Settings panel
│   ├── styles/
│   │   └── globals.css        # Global styles with Tailwind
│   └── lib/                   # Utilities and services
├── package.json               # Dependencies and scripts
├── next.config.js            # Next.js configuration
├── tailwind.config.js        # Tailwind CSS configuration
└── tsconfig.json             # TypeScript configuration
```

## 🎯 Key Features

### Modern Trading Interface
- **Real-time Charts** - Interactive price charts with technical indicators
- **Order Book** - Live bid/ask orders display
- **Trading Panel** - Buy/sell order placement
- **Portfolio Dashboard** - Balance, P&L, and position tracking
- **Strategy Builder** - Visual strategy creation (coming soon)

### Technical Stack
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Recharts** - Trading charts and visualizations
- **Zustand** - Lightweight state management
- **React Query** - Server state synchronization

### Design System
- **Dark Theme** - Professional trading interface
- **Responsive Design** - Mobile and desktop optimized
- **Component Library** - Reusable UI components
- **Trading Colors** - Bullish green, bearish red indicators

## 🔗 Backend Integration

### API Configuration
The frontend is configured to proxy API requests to your FastAPI backend:

```javascript
// next.config.js
async rewrites() {
  return [
    {
      source: '/api/:path*',
      destination: 'http://localhost:8000/:path*', // Your FastAPI server
    },
  ];
}
```

### Real-time Data
WebSocket connections for live market data:
- Price updates
- Order book changes
- Trade executions
- Portfolio updates

## 📊 Figma Integration with MCP

### Using Figma MCP Server
1. **Access Design Assets**
   ```javascript
   // Example: Fetch design tokens from Figma
   const designTokens = await figmaMCP.getDesignTokens(fileKey);
   ```

2. **Export Components**
   ```javascript
   // Export Figma components as React components
   const components = await figmaMCP.exportComponents(frameIds);
   ```

3. **Design System Sync**
   - Colors, typography, and spacing from Figma
   - Component specifications
   - Asset exports

### AI Toolkit Integration
The AI Toolkit can help you:
- Generate React components from Figma designs
- Create responsive layouts
- Optimize component architecture
- Implement design system patterns

## 🛠 Development Workflow

### Adding New Features
1. **Design in Figma** - Create or update designs
2. **Use AI Toolkit** - Generate component scaffolding
3. **Implement Logic** - Add trading functionality
4. **Connect APIs** - Integrate with backend services
5. **Test & Deploy** - Validate and deploy changes

### Code Structure Guidelines
```typescript
// Component naming convention
export function TradingChart({ symbol }: TradingChartProps) {
  // Component logic
}

// Props interface
interface TradingChartProps {
  symbol: string;
  timeframe?: string;
}

// API service example
export const tradingAPI = {
  getMarketData: (symbol: string) => fetch(`/api/market/${symbol}`),
  placeOrder: (order: OrderRequest) => fetch('/api/orders', { ... }),
};
```

## 🚨 Troubleshooting

### Common Issues

**1. Figma MCP Connection Failed**
```powershell
# Check environment variables
echo $env:FIGMA_PAT
echo $env:FIGMA_FILE_KEY

# Restart VS Code after setting variables
```

**2. Module Not Found Errors**
```powershell
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**3. API Connection Issues**
```powershell
# Ensure FastAPI backend is running on port 8000
cd .. # Back to root project
python api/main.py
```

### Performance Optimization
- Enable Next.js production build: `npm run build`
- Use React.memo for expensive components
- Implement virtual scrolling for large datasets
- Optimize chart rendering frequency

## 🔄 Next Steps

### Immediate Tasks
1. **Start Backend API** - Run your FastAPI server
2. **Configure Real Data** - Connect to live market data feeds
3. **Implement Authentication** - Add user login/registration
4. **Add Trading Logic** - Connect order placement to exchanges

### Advanced Features
- **Strategy Backtesting** - Historical strategy testing
- **Risk Management** - Position sizing and stop-loss
- **Multi-Exchange Support** - Connect multiple crypto exchanges
- **Mobile App** - React Native companion app

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the Next.js documentation
3. Use VS Code AI Toolkit for component generation
4. Refer to your existing project documentation in `/docs`

---

**Happy Trading! 🚀📈**