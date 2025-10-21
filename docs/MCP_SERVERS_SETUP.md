# MCP Servers Setup Guide for AlgoProject Platform
## VPS Deployment Configuration

This guide helps you set up Model Context Protocol (MCP) servers for CCXT and Fyers integration on your VPS.

## 🚀 Quick Start

### Prerequisites
- Ubuntu/CentOS VPS server
- Node.js 18+ installed
- Python 3.8+ installed
- Docker (optional but recommended)

## 📊 CCXT MCP Server Setup

### 1. Install CCXT MCP Server

```bash
# On your VPS
mkdir -p /opt/algoproject/mcp-servers
cd /opt/algoproject/mcp-servers

# Clone and install CCXT MCP server
git clone https://github.com/doggybee/mcp-server-ccxt.git ccxt-server
cd ccxt-server

npm install
```

### 2. Configure CCXT MCP Server

Create configuration file:

```bash
# /opt/algoproject/mcp-servers/ccxt-server/config.json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8001,
    "ssl": false
  },
  "exchanges": {
    "binance": {
      "apiKey": "YOUR_BINANCE_API_KEY",
      "secret": "YOUR_BINANCE_SECRET",
      "sandbox": false,
      "enableRateLimit": true
    },
    "coinbase": {
      "apiKey": "YOUR_COINBASE_API_KEY",
      "secret": "YOUR_COINBASE_SECRET",
      "passphrase": "YOUR_COINBASE_PASSPHRASE",
      "sandbox": false,
      "enableRateLimit": true
    },
    "kraken": {
      "apiKey": "YOUR_KRAKEN_API_KEY",
      "secret": "YOUR_KRAKEN_SECRET",
      "sandbox": false,
      "enableRateLimit": true
    }
  },
  "rateLimits": {
    "requests_per_second": 10,
    "burst_limit": 50
  },
  "security": {
    "cors": {
      "origin": ["https://yourdomain.com", "http://localhost:3000"],
      "credentials": true
    },
    "api_key_required": true,
    "whitelist_ips": ["YOUR_FRONTEND_SERVER_IP"]
  }
}
```

### 3. Create Systemd Service

```bash
# /etc/systemd/system/ccxt-mcp.service
[Unit]
Description=CCXT MCP Server
After=network.target

[Service]
Type=simple
User=algoproject
WorkingDirectory=/opt/algoproject/mcp-servers/ccxt-server
ExecStart=/usr/bin/node server.js
Restart=always
RestartSec=10
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl enable ccxt-mcp
sudo systemctl start ccxt-mcp
sudo systemctl status ccxt-mcp
```

## 📈 Fyers MCP Server Setup

### 1. Create Fyers MCP Server

Since Fyers doesn't have an official MCP server, we'll create one:

```bash
cd /opt/algoproject/mcp-servers
mkdir fyers-server
cd fyers-server

# Initialize Node.js project
npm init -y
npm install express cors helmet rate-limiter-flexible fyers-apiv3 dotenv
```

### 2. Fyers MCP Server Implementation

Create the server:

```javascript
// /opt/algoproject/mcp-servers/fyers-server/server.js
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const { RateLimiterMemory } = require('rate-limiter-flexible');
const { fyersModel } = require('fyers-apiv3');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 8002;

// Rate limiting
const rateLimiter = new RateLimiterMemory({
  keyGenerator: (req) => req.ip,
  points: 100, // Number of requests
  duration: 60, // per 60 seconds
});

// Middleware
app.use(helmet());
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
  credentials: true
}));
app.use(express.json());

// Rate limiting middleware
app.use(async (req, res, next) => {
  try {
    await rateLimiter.consume(req.ip);
    next();
  } catch (rejRes) {
    res.status(429).json({ error: 'Too many requests' });
  }
});

// Initialize Fyers client
const fyers = fyersModel();
fyers.setAppId(process.env.FYERS_APP_ID);
fyers.setAccessToken(process.env.FYERS_ACCESS_TOKEN);

// Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// Get quotes
app.post('/api/quotes', async (req, res) => {
  try {
    const { symbols } = req.body;
    const response = await fyers.getQuotes({ symbols });
    res.json(response);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get historical data
app.post('/api/historical', async (req, res) => {
  try {
    const { symbol, resolution, dateFrom, dateTo } = req.body;
    const response = await fyers.getHistoricalData({
      symbol,
      resolution,
      dateFrom,
      dateTo
    });
    res.json(response);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get option chain
app.post('/api/optionchain', async (req, res) => {
  try {
    const { symbol, strikeFrom, strikeTo, dateFrom, dateTo } = req.body;
    const response = await fyers.optionChain({
      symbol,
      strikeFrom,
      strikeTo,
      dateFrom,
      dateTo
    });
    res.json(response);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Fyers MCP Server running on port ${PORT}`);
});
```

### 3. Fyers Environment Configuration

```bash
# /opt/algoproject/mcp-servers/fyers-server/.env
FYERS_APP_ID=YOUR_FYERS_APP_ID
FYERS_ACCESS_TOKEN=YOUR_FYERS_ACCESS_TOKEN
ALLOWED_ORIGINS=https://yourdomain.com,http://localhost:3000
PORT=8002
NODE_ENV=production
```

### 4. Create Fyers Systemd Service

```bash
# /etc/systemd/system/fyers-mcp.service
[Unit]
Description=Fyers MCP Server
After=network.target

[Service]
Type=simple
User=algoproject
WorkingDirectory=/opt/algoproject/mcp-servers/fyers-server
ExecStart=/usr/bin/node server.js
Restart=always
RestartSec=10
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable fyers-mcp
sudo systemctl start fyers-mcp
sudo systemctl status fyers-mcp
```

## 🔧 Nginx Configuration

Configure reverse proxy for both servers:

```nginx
# /etc/nginx/sites-available/algoproject-mcp
server {
    listen 80;
    server_name your-vps-domain.com;

    # CCXT MCP Server
    location /api/ccxt/ {
        proxy_pass http://localhost:8001/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Fyers MCP Server
    location /api/fyers/ {
        proxy_pass http://localhost:8002/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/algoproject-mcp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔐 SSL Configuration with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-vps-domain.com
```

## 📱 Frontend Integration

Update your frontend environment variables:

```bash
# .env.local in your frontend
NEXT_PUBLIC_CCXT_MCP_URL=https://your-vps-domain.com/api/ccxt
NEXT_PUBLIC_FYERS_MCP_URL=https://your-vps-domain.com/api/fyers
NEXT_PUBLIC_MCP_API_KEY=your-mcp-api-key
```

### Frontend API Service

```typescript
// src/services/mcpService.ts
const MCP_BASE_URL = process.env.NEXT_PUBLIC_CCXT_MCP_URL;
const FYERS_BASE_URL = process.env.NEXT_PUBLIC_FYERS_MCP_URL;
const API_KEY = process.env.NEXT_PUBLIC_MCP_API_KEY;

class MCPService {
  private headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${API_KEY}`
  };

  // CCXT Methods
  async getCCXTExchanges() {
    const response = await fetch(`${MCP_BASE_URL}/exchanges`, {
      headers: this.headers
    });
    return response.json();
  }

  async getCCXTMarkets(exchange: string) {
    const response = await fetch(`${MCP_BASE_URL}/markets/${exchange}`, {
      headers: this.headers
    });
    return response.json();
  }

  async getCCXTOrderBook(exchange: string, symbol: string) {
    const response = await fetch(`${MCP_BASE_URL}/orderbook/${exchange}/${symbol}`, {
      headers: this.headers
    });
    return response.json();
  }

  // Fyers Methods
  async getFyersQuotes(symbols: string[]) {
    const response = await fetch(`${FYERS_BASE_URL}/quotes`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({ symbols })
    });
    return response.json();
  }

  async getFyersHistorical(params: any) {
    const response = await fetch(`${FYERS_BASE_URL}/historical`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(params)
    });
    return response.json();
  }

  async getFyersOptionChain(params: any) {
    const response = await fetch(`${FYERS_BASE_URL}/optionchain`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(params)
    });
    return response.json();
  }
}

export const mcpService = new MCPService();
```

## 🔍 Monitoring and Logging

### 1. Set up log rotation

```bash
# /etc/logrotate.d/algoproject-mcp
/opt/algoproject/mcp-servers/*/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 algoproject algoproject
    postrotate
        systemctl reload ccxt-mcp
        systemctl reload fyers-mcp
    endscript
}
```

### 2. Health Check Script

```bash
#!/bin/bash
# /opt/algoproject/scripts/health-check.sh

echo "Checking MCP Servers Health..."

# Check CCXT MCP
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ CCXT MCP Server: Healthy"
else
    echo "❌ CCXT MCP Server: Down"
    systemctl restart ccxt-mcp
fi

# Check Fyers MCP
if curl -f http://localhost:8002/api/health > /dev/null 2>&1; then
    echo "✅ Fyers MCP Server: Healthy"
else
    echo "❌ Fyers MCP Server: Down"
    systemctl restart fyers-mcp
fi
```

Add to crontab:
```bash
# Run health check every 5 minutes
*/5 * * * * /opt/algoproject/scripts/health-check.sh >> /var/log/algoproject-health.log 2>&1
```

## 🚀 Deployment Checklist

- [ ] VPS server configured with Node.js and Python
- [ ] CCXT MCP Server installed and configured
- [ ] Fyers MCP Server created and configured
- [ ] Both services enabled in systemd
- [ ] Nginx reverse proxy configured
- [ ] SSL certificates installed
- [ ] Firewall configured (ports 80, 443, 8001, 8002)
- [ ] Frontend environment variables updated
- [ ] Health monitoring script deployed
- [ ] Log rotation configured

## 📞 Support

For issues with MCP server setup:
1. Check service logs: `sudo journalctl -u ccxt-mcp -f`
2. Verify port availability: `sudo netstat -tlnp | grep :8001`
3. Test endpoints: `curl http://localhost:8001/health`

---

**Generated:** October 2025  
**Platform:** AlgoProject Institution Grade  
**Version:** MCP Integration v1.0