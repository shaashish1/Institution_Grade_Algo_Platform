# 🚀 AlgoProject Deployment Guide - October 2025 Update

## 📋 **Quick Deployment Checklist**

### **Frontend Setup (Next.js)**
```powershell
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Development server
npm run dev          # Runs on http://localhost:3000

# Production build
npm run build        # Creates optimized build
npm start           # Serves production build
```

### **Backend Setup (FastAPI)**
```powershell
# Navigate to API directory
cd api

# Install Python dependencies (if not already done)
pip install fastapi uvicorn ccxt fyers-apiv3 pandas pydantic

# Start development server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Production server
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 🔧 **Feature Configuration**

### **1. Theme System Setup**
The theme system works out of the box with no additional configuration required.

**Available Themes:**
- **Dark**: Default professional dark theme
- **Light**: Clean light theme with blue accents
- **Cosmic**: Space-inspired purple theme
- **Doodle**: Hand-drawn paper theme with animations

**Usage:**
- Theme switcher appears in top-right corner
- Themes persist in localStorage
- All components automatically adapt

### **2. Fyers User Credential Management**

#### **Data Directory Setup:**
```powershell
# Create data directory for user credentials
mkdir data
```

#### **User Credential Format:**
```json
{
  "user_id": "user@example.com",
  "client_id": "XA12345-100",
  "secret_key": "USER_SECRET_KEY",
  "user_name": "XA00330",
  "pin": "1234",
  "totp_key": "OPTIONAL_TOTP_KEY",
  "redirect_uri": "https://www.google.com",
  "is_active": true
}
```

#### **Required Fyers Setup:**
1. Users need Fyers trading account
2. API credentials from Fyers Developer Portal
3. TOTP key from Fyers mobile app (optional)
4. 4-digit trading PIN

### **3. CCXT Exchange Configuration**

#### **Supported Exchanges:**
- Binance
- Coinbase Pro
- Kraken
- KuCoin
- OKX
- Bybit
- Bitfinex
- Huobi
- Gate.io

#### **Trading Modes:**
```python
# No credentials needed
BACKTEST = "backtest"    # Historical data analysis
PAPER = "paper"          # Simulated trading

# Credentials required
LIVE = "live"            # Real trading with actual funds
```

### **4. AI Strategy Engine**

#### **PineScript Support:**
- Upload `.pine` files
- AI analysis of strategy logic
- Performance prediction
- Risk assessment

#### **Strategy Features:**
- Real-time signal generation
- AI-powered recommendations
- Backtesting integration
- Performance analytics

---

## 🔐 **Security Configuration**

### **API Security:**
```python
# Environment variables (recommended)
FYERS_SECRET_KEY=your_secret_key_here
EXCHANGE_API_KEY=your_exchange_key_here
EXCHANGE_SECRET=your_exchange_secret_here
```

### **Frontend Security:**
- API calls proxied through Next.js
- No direct API key exposure
- Secure credential input forms
- Token validation and refresh

### **File Permissions:**
```powershell
# Secure the data directory
icacls data /grant:r Users:(RX)
icacls data/fyers_users.json /grant:r Users:(R)
```

---

## 🌐 **Production Deployment**

### **Docker Setup (Optional)**
```dockerfile
# Frontend Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

```dockerfile
# Backend Dockerfile  
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Environment Variables:**
```bash
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=AlgoProject

# Backend (.env)
CORS_ORIGINS=http://localhost:3000,https://your-domain.com
LOG_LEVEL=INFO
DATA_DIR=./data
```

### **Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📊 **Monitoring & Logging**

### **Backend Logs:**
- FastAPI automatic request logging
- Custom logging for credential operations
- Error tracking for exchange connections
- Performance metrics collection

### **Frontend Monitoring:**
- Theme switching analytics
- User interaction tracking
- Error boundary reporting
- Performance monitoring

### **Log Locations:**
```
logs/
├── api/
│   ├── access.log          # API access logs
│   ├── error.log           # Error logs
│   └── fyers.log           # Fyers-specific logs
└── frontend/
    ├── build.log           # Build logs
    └── runtime.log         # Runtime logs
```

---

## 🧪 **Testing**

### **Frontend Testing:**
```powershell
cd frontend

# Run tests
npm test

# Test theme switching
npm run test:themes

# Build test
npm run build
```

### **Backend Testing:**
```powershell
cd api

# Test API endpoints
python test_fyers_api.py

# Test CCXT integration
python -m pytest tests/test_ccxt.py

# Test credential management
python -m pytest tests/test_fyers_service.py
```

### **Integration Testing:**
1. Start backend server
2. Start frontend server  
3. Test theme switching
4. Test credential management
5. Test trading mode authentication
6. Test AI strategy upload

---

## 🔧 **Troubleshooting**

### **Common Issues:**

#### **Theme Not Switching:**
- Check browser localStorage
- Clear cache and cookies
- Verify theme provider is wrapped around app

#### **Credential Management Issues:**
- Ensure data directory exists
- Check file permissions
- Verify Fyers API format

#### **CCXT Connection Errors:**
- Verify exchange API keys
- Check network connectivity
- Validate trading mode

#### **Build Errors:**
- Clear node_modules and reinstall
- Check TypeScript errors
- Verify all imports are correct

### **Debug Commands:**
```powershell
# Frontend debug
npm run dev -- --debug

# Backend debug
python -m uvicorn main:app --reload --log-level debug

# Check API status
curl http://localhost:8000/health

# Test specific endpoint
curl -X POST http://localhost:8000/fyers/test-connection/user123
```

---

## 📞 **Support Resources**

### **Documentation:**
- API Docs: `http://localhost:8000/docs`
- Component Docs: In source files
- Theme Guide: `/docs/THEME_GUIDE.md`
- Setup Guide: `/docs/SETUP_GUIDE.md`

### **Configuration Files:**
- Next.js: `frontend/next.config.js`
- Tailwind: `frontend/tailwind.config.js`
- FastAPI: `api/main.py`
- Themes: `frontend/src/styles/globals.css`

### **Key Directories:**
```
frontend/src/
├── app/                    # Next.js pages
├── components/             # React components
│   ├── theme/             # Theme system
│   └── fyers-credentials.tsx
├── styles/                # Global styles & themes
└── types/                 # TypeScript definitions

api/
├── main.py                # FastAPI app
├── ccxt_service.py        # Exchange service
├── fyers_user_service.py  # User management
└── data/                  # User data storage
```

---

## ✅ **Deployment Verification**

### **Checklist:**
- [ ] Frontend builds successfully
- [ ] Backend starts without errors
- [ ] Theme switching works
- [ ] Credential management functions
- [ ] CCXT authentication works
- [ ] AI strategy page loads
- [ ] API endpoints respond
- [ ] Data directory created
- [ ] Logging configured
- [ ] Security headers set

### **Health Check URLs:**
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000/health`
- API Docs: `http://localhost:8000/docs`
- Theme Test: `http://localhost:3000` (switch themes in top-right)

**🎉 Platform Ready for Production!**