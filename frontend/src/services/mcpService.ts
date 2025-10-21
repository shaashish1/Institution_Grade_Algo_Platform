/**
 * MCP Service Integration
 * Provides unified access to CCXT and Fyers MCP servers
 */

interface MCPConfig {
  ccxtBaseUrl: string;
  fyersBaseUrl: string;
  apiKey: string;
}

interface ExchangeInfo {
  id: string;
  name: string;
  countries: string[];
  urls: {
    logo: string;
    api: string;
    www: string;
  };
  has: {
    spot: boolean;
    margin: boolean;
    future: boolean;
    option: boolean;
  };
  fees: {
    trading: {
      maker: number;
      taker: number;
    };
  };
}

interface MarketData {
  symbol: string;
  bid: number;
  ask: number;
  last: number;
  change: number;
  percentage: number;
  volume: number;
  timestamp: number;
}

interface HistoricalData {
  timestamp: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

interface OptionChainData {
  symbol: string;
  expiry: string;
  strikes: {
    strike: number;
    call: {
      bid: number;
      ask: number;
      last: number;
      volume: number;
      openInterest: number;
      iv: number;
      delta: number;
      gamma: number;
      theta: number;
      vega: number;
    };
    put: {
      bid: number;
      ask: number;
      last: number;
      volume: number;
      openInterest: number;
      iv: number;
      delta: number;
      gamma: number;
      theta: number;
      vega: number;
    };
  }[];
}

class MCPService {
  private config: MCPConfig;

  constructor() {
    this.config = {
      ccxtBaseUrl: process.env.NEXT_PUBLIC_CCXT_MCP_URL || 'http://localhost:8001',
      fyersBaseUrl: process.env.NEXT_PUBLIC_FYERS_MCP_URL || 'http://localhost:8002',
      apiKey: process.env.NEXT_PUBLIC_MCP_API_KEY || ''
    };
  }

  private get headers() {
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.config.apiKey}`,
      'X-API-Source': 'algoproject-frontend'
    };
  }

  private async handleResponse(response: Response) {
    if (!response.ok) {
      const error = await response.text();
      throw new Error(`MCP Error: ${response.status} - ${error}`);
    }
    return response.json();
  }

  // ===== CCXT Exchange Methods =====

  /**
   * Get list of all supported exchanges
   */
  async getExchanges(): Promise<ExchangeInfo[]> {
    try {
      const response = await fetch(`${this.config.ccxtBaseUrl}/api/exchanges`, {
        headers: this.headers
      });
      return this.handleResponse(response);
    } catch (error) {
      console.error('Failed to fetch exchanges:', error);
      // Return fallback data if MCP server is unavailable
      return this.getFallbackExchanges();
    }
  }

  /**
   * Get exchange information
   */
  async getExchangeInfo(exchangeId: string): Promise<ExchangeInfo> {
    const response = await fetch(`${this.config.ccxtBaseUrl}/api/exchanges/${exchangeId}`, {
      headers: this.headers
    });
    return this.handleResponse(response);
  }

  /**
   * Get markets for a specific exchange
   */
  async getMarkets(exchangeId: string): Promise<any[]> {
    const response = await fetch(`${this.config.ccxtBaseUrl}/api/markets/${exchangeId}`, {
      headers: this.headers
    });
    return this.handleResponse(response);
  }

  /**
   * Get ticker data for a symbol on an exchange
   */
  async getTicker(exchangeId: string, symbol: string): Promise<MarketData> {
    const response = await fetch(`${this.config.ccxtBaseUrl}/api/ticker/${exchangeId}/${symbol}`, {
      headers: this.headers
    });
    return this.handleResponse(response);
  }

  /**
   * Get multiple tickers
   */
  async getTickers(exchangeId: string, symbols?: string[]): Promise<MarketData[]> {
    const url = symbols 
      ? `${this.config.ccxtBaseUrl}/api/tickers/${exchangeId}?symbols=${symbols.join(',')}`
      : `${this.config.ccxtBaseUrl}/api/tickers/${exchangeId}`;
    
    const response = await fetch(url, {
      headers: this.headers
    });
    return this.handleResponse(response);
  }

  /**
   * Get order book for a symbol
   */
  async getOrderBook(exchangeId: string, symbol: string, limit?: number): Promise<any> {
    const url = limit 
      ? `${this.config.ccxtBaseUrl}/api/orderbook/${exchangeId}/${symbol}?limit=${limit}`
      : `${this.config.ccxtBaseUrl}/api/orderbook/${exchangeId}/${symbol}`;
    
    const response = await fetch(url, {
      headers: this.headers
    });
    return this.handleResponse(response);
  }

  /**
   * Get historical OHLCV data
   */
  async getOHLCV(
    exchangeId: string, 
    symbol: string, 
    timeframe: string = '1d',
    since?: number,
    limit?: number
  ): Promise<HistoricalData[]> {
    const params = new URLSearchParams();
    if (since) params.append('since', since.toString());
    if (limit) params.append('limit', limit.toString());
    
    const url = `${this.config.ccxtBaseUrl}/api/ohlcv/${exchangeId}/${symbol}/${timeframe}?${params}`;
    
    const response = await fetch(url, {
      headers: this.headers
    });
    return this.handleResponse(response);
  }

  // ===== Fyers API Methods =====

  /**
   * Get quotes from Fyers API
   */
  async getFyersQuotes(symbols: string[]): Promise<any> {
    const response = await fetch(`${this.config.fyersBaseUrl}/api/quotes`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({ symbols })
    });
    return this.handleResponse(response);
  }

  /**
   * Get historical data from Fyers API
   */
  async getFyersHistorical(params: {
    symbol: string;
    resolution: string;
    dateFrom: string;
    dateTo: string;
  }): Promise<HistoricalData[]> {
    const response = await fetch(`${this.config.fyersBaseUrl}/api/historical`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(params)
    });
    return this.handleResponse(response);
  }

  /**
   * Get option chain from Fyers API
   */
  async getFyersOptionChain(params: {
    symbol: string;
    strikeFrom?: number;
    strikeTo?: number;
    dateFrom?: string;
    dateTo?: string;
  }): Promise<OptionChainData> {
    const response = await fetch(`${this.config.fyersBaseUrl}/api/optionchain`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(params)
    });
    return this.handleResponse(response);
  }

  // ===== Health Check Methods =====

  /**
   * Check CCXT MCP server health
   */
  async checkCCXTHealth(): Promise<{ status: string; timestamp: string }> {
    try {
      const response = await fetch(`${this.config.ccxtBaseUrl}/api/health`);
      return this.handleResponse(response);
    } catch (error) {
      return { status: 'unhealthy', timestamp: new Date().toISOString() };
    }
  }

  /**
   * Check Fyers MCP server health
   */
  async checkFyersHealth(): Promise<{ status: string; timestamp: string }> {
    try {
      const response = await fetch(`${this.config.fyersBaseUrl}/api/health`);
      return this.handleResponse(response);
    } catch (error) {
      return { status: 'unhealthy', timestamp: new Date().toISOString() };
    }
  }

  /**
   * Check all MCP servers health
   */
  async checkAllHealth(): Promise<{
    ccxt: { status: string; timestamp: string };
    fyers: { status: string; timestamp: string };
  }> {
    const [ccxtHealth, fyersHealth] = await Promise.all([
      this.checkCCXTHealth(),
      this.checkFyersHealth()
    ]);

    return {
      ccxt: ccxtHealth,
      fyers: fyersHealth
    };
  }

  // ===== Fallback Methods =====

  /**
   * Fallback exchange data when MCP server is unavailable
   */
  private getFallbackExchanges(): ExchangeInfo[] {
    return [
      {
        id: 'binance',
        name: 'Binance',
        countries: ['Global'],
        urls: {
          logo: 'https://logo.clearbit.com/binance.com',
          api: 'https://api.binance.com',
          www: 'https://binance.com'
        },
        has: {
          spot: true,
          margin: true,
          future: true,
          option: false
        },
        fees: {
          trading: {
            maker: 0.001,
            taker: 0.001
          }
        }
      },
      {
        id: 'coinbase',
        name: 'Coinbase Advanced',
        countries: ['US'],
        urls: {
          logo: 'https://logo.clearbit.com/coinbase.com',
          api: 'https://api.coinbase.com',
          www: 'https://coinbase.com'
        },
        has: {
          spot: true,
          margin: true,
          future: false,
          option: false
        },
        fees: {
          trading: {
            maker: 0.005,
            taker: 0.005
          }
        }
      },
      {
        id: 'kraken',
        name: 'Kraken',
        countries: ['US'],
        urls: {
          logo: 'https://logo.clearbit.com/kraken.com',
          api: 'https://api.kraken.com',
          www: 'https://kraken.com'
        },
        has: {
          spot: true,
          margin: true,
          future: true,
          option: false
        },
        fees: {
          trading: {
            maker: 0.0016,
            taker: 0.0026
          }
        }
      }
    ];
  }

  // ===== Utility Methods =====

  /**
   * Format currency amounts
   */
  formatCurrency(amount: number, currency: string = 'USD'): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: 2,
      maximumFractionDigits: 8
    }).format(amount);
  }

  /**
   * Format percentage changes
   */
  formatPercentage(value: number): string {
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
  }

  /**
   * Calculate technical indicators (simple implementations)
   */
  calculateSMA(data: number[], period: number): number[] {
    const sma = [];
    for (let i = period - 1; i < data.length; i++) {
      const sum = data.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
      sma.push(sum / period);
    }
    return sma;
  }

  /**
   * Calculate RSI
   */
  calculateRSI(prices: number[], period: number = 14): number[] {
    const gains = [];
    const losses = [];
    
    for (let i = 1; i < prices.length; i++) {
      const change = prices[i] - prices[i - 1];
      gains.push(change > 0 ? change : 0);
      losses.push(change < 0 ? Math.abs(change) : 0);
    }
    
    const avgGains = this.calculateSMA(gains, period);
    const avgLosses = this.calculateSMA(losses, period);
    
    return avgGains.map((avgGain, i) => {
      const rs = avgGain / avgLosses[i];
      return 100 - (100 / (1 + rs));
    });
  }
}

// Export singleton instance
export const mcpService = new MCPService();
export type { ExchangeInfo, MarketData, HistoricalData, OptionChainData };