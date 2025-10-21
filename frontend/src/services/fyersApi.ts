/**
 * FYERS API Service
 * Handles real-time market data, quotes, and trading operations via FYERS API
 */

const API_BASE_URL = 'http://localhost:8000/api';

export interface FyersQuote {
  symbol: string;
  ltp: number;  // Last traded price
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  change: number;
  change_percent: number;
}

export interface FyersPosition {
  symbol: string;
  quantity: number;
  buy_price: number;
  current_price: number;
  pnl: number;
  pnl_percent: number;
}

export interface MarketStatus {
  is_open: boolean;
  status: string;
  message: string;
  next_open?: string;
  next_close?: string;
}

export interface FyersMarketData {
  nifty: {
    symbol: string;
    price: number;
    change: number;
    change_percent: number;
    high: number;
    low: number;
    open: number;
    previous_close: number;
    last_updated: string;
  };
  bank_nifty: {
    symbol: string;
    price: number;
    change: number;
    change_percent: number;
    high: number;
    low: number;
    open: number;
    previous_close: number;
    last_updated: string;
  };
  market_status: MarketStatus;
  data_source: string;
  message: string;
}

/**
 * Get real-time quotes for multiple symbols
 */
export async function getQuotes(symbols: string[]): Promise<Record<string, FyersQuote>> {
  try {
    const response = await fetch(`${API_BASE_URL}/market/quotes`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ symbols }),
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch quotes: ${response.statusText}`);
    }

    return response.json();
  } catch (error) {
    console.error('Error fetching quotes:', error);
    throw error;
  }
}

/**
 * Get comprehensive market data (NIFTY, Bank NIFTY, etc.)
 */
export async function getMarketData(): Promise<FyersMarketData> {
  try {
    const response = await fetch(`${API_BASE_URL}/market/data`);

    if (!response.ok) {
      throw new Error(`Failed to fetch market data: ${response.statusText}`);
    }

    return response.json();
  } catch (error) {
    console.error('Error fetching market data:', error);
    throw error;
  }
}

/**
 * Get current positions from FYERS account
 */
export async function getPositions(): Promise<FyersPosition[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/positions`);

    if (!response.ok) {
      throw new Error(`Failed to fetch positions: ${response.statusText}`);
    }

    const data = await response.json();
    return data.positions || [];
  } catch (error) {
    console.error('Error fetching positions:', error);
    // Return empty array on error to prevent UI breaks
    return [];
  }
}

/**
 * Get historical data for a symbol
 */
export async function getHistoricalData(
  symbol: string,
  resolution: string = '5',
  bars: number = 100,
  exchange: string = 'NSE'
): Promise<any[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/market/historical`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        symbol,
        resolution,
        bars,
        exchange,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch historical data: ${response.statusText}`);
    }

    return response.json();
  } catch (error) {
    console.error('Error fetching historical data:', error);
    throw error;
  }
}

/**
 * Test FYERS API connection
 */
export async function testConnection(): Promise<{ success: boolean; message: string }> {
  try {
    const response = await fetch(`${API_BASE_URL}/market/health`);

    if (!response.ok) {
      return {
        success: false,
        message: 'Failed to connect to market data service',
      };
    }

    const data = await response.json();
    return {
      success: data.status === 'ok',
      message: data.message || 'Connected successfully',
    };
  } catch (error) {
    return {
      success: false,
      message: error instanceof Error ? error.message : 'Connection failed',
    };
  }
}

/**
 * Subscribe to real-time updates via WebSocket
 */
export class FyersWebSocket {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private subscribers: Map<string, Set<(data: any) => void>> = new Map();

  constructor(private url: string = 'ws://localhost:8000/ws/market') {}

  connect(): void {
    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        console.log('✅ WebSocket connected');
        this.reconnectAttempts = 0;
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.handleMessage(data);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      this.ws.onclose = () => {
        console.log('WebSocket disconnected');
        this.attemptReconnect();
      };
    } catch (error) {
      console.error('Error creating WebSocket:', error);
      this.attemptReconnect();
    }
  }

  private handleMessage(data: any): void {
    const { type, symbol, payload } = data;

    // Notify all subscribers for this symbol
    const subscribers = this.subscribers.get(symbol);
    if (subscribers) {
      subscribers.forEach((callback) => callback(payload));
    }

    // Notify wildcard subscribers (*)
    const wildcardSubscribers = this.subscribers.get('*');
    if (wildcardSubscribers) {
      wildcardSubscribers.forEach((callback) => callback(data));
    }
  }

  subscribe(symbol: string, callback: (data: any) => void): () => void {
    if (!this.subscribers.has(symbol)) {
      this.subscribers.set(symbol, new Set());
    }

    const subscribers = this.subscribers.get(symbol)!;
    subscribers.add(callback);

    // Send subscription message to server
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ action: 'subscribe', symbol }));
    }

    // Return unsubscribe function
    return () => {
      subscribers.delete(callback);
      if (subscribers.size === 0) {
        this.subscribers.delete(symbol);
        // Send unsubscribe message to server
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
          this.ws.send(JSON.stringify({ action: 'unsubscribe', symbol }));
        }
      }
    };
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * this.reconnectAttempts;

    console.log(`Attempting to reconnect in ${delay}ms...`);
    setTimeout(() => {
      this.connect();
    }, delay);
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.subscribers.clear();
  }

  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
  }
}

// Singleton WebSocket instance
let wsInstance: FyersWebSocket | null = null;

export function getFyersWebSocket(): FyersWebSocket {
  if (!wsInstance) {
    wsInstance = new FyersWebSocket();
  }
  return wsInstance;
}

/**
 * Format Indian currency
 */
export function formatIndianCurrency(amount: number): string {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 2,
  }).format(amount);
}

/**
 * Format number with Indian numbering system
 */
export function formatIndianNumber(num: number): string {
  return new Intl.NumberFormat('en-IN').format(num);
}

/**
 * Get color class based on change value
 */
export function getChangeColor(change: number): string {
  if (change > 0) return 'text-green-400';
  if (change < 0) return 'text-red-400';
  return 'text-slate-400';
}

/**
 * Get background color class based on change value
 */
export function getChangeBgColor(change: number): string {
  if (change > 0) return 'bg-green-500/10';
  if (change < 0) return 'bg-red-500/10';
  return 'bg-slate-500/10';
}
