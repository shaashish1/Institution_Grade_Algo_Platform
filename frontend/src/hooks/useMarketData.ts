/**
 * React Hook for FYERS Market Data
 * Manages real-time market data with WebSocket updates
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import {
  getMarketData,
  getQuotes,
  getPositions,
  testConnection,
  FyersWebSocket,
  getFyersWebSocket,
  type FyersMarketData,
  type FyersQuote,
  type FyersPosition,
} from '../services/fyersApi';

interface UseMarketDataOptions {
  symbols?: string[];
  autoRefresh?: boolean;
  refreshInterval?: number;
  useWebSocket?: boolean;
}

interface MarketDataState {
  marketData: FyersMarketData | null;
  quotes: Record<string, FyersQuote>;
  positions: FyersPosition[];
  isLoading: boolean;
  error: string | null;
  isConnected: boolean;
  lastUpdate: Date | null;
}

export function useMarketData(options: UseMarketDataOptions = {}) {
  const {
    symbols = [],
    autoRefresh = true,
    refreshInterval = 5000,
    useWebSocket = false,
  } = options;

  const [state, setState] = useState<MarketDataState>({
    marketData: null,
    quotes: {},
    positions: [],
    isLoading: true,
    error: null,
    isConnected: false,
    lastUpdate: null,
  });

  const wsRef = useRef<FyersWebSocket | null>(null);
  const refreshTimerRef = useRef<NodeJS.Timeout | null>(null);

  // Fetch comprehensive market data
  const fetchMarketData = useCallback(async () => {
    try {
      const data = await getMarketData();
      setState((prev) => ({
        ...prev,
        marketData: data,
        lastUpdate: new Date(),
        error: null,
      }));
    } catch (error) {
      console.error('Error fetching market data:', error);
      setState((prev) => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Failed to fetch market data',
      }));
    }
  }, []);

  // Fetch quotes for specific symbols
  const fetchQuotes = useCallback(async (symbolList: string[]) => {
    if (symbolList.length === 0) return;

    try {
      const quotes = await getQuotes(symbolList);
      setState((prev) => ({
        ...prev,
        quotes: { ...prev.quotes, ...quotes },
        lastUpdate: new Date(),
        error: null,
      }));
    } catch (error) {
      console.error('Error fetching quotes:', error);
      setState((prev) => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Failed to fetch quotes',
      }));
    }
  }, []);

  // Fetch positions
  const fetchPositions = useCallback(async () => {
    try {
      const positions = await getPositions();
      setState((prev) => ({
        ...prev,
        positions,
        lastUpdate: new Date(),
        error: null,
      }));
    } catch (error) {
      console.error('Error fetching positions:', error);
      setState((prev) => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Failed to fetch positions',
      }));
    }
  }, []);

  // Test API connection
  const checkConnection = useCallback(async () => {
    try {
      const result = await testConnection();
      setState((prev) => ({
        ...prev,
        isConnected: result.success,
        error: result.success ? null : result.message,
      }));
      return result.success;
    } catch (error) {
      setState((prev) => ({
        ...prev,
        isConnected: false,
        error: 'Connection test failed',
      }));
      return false;
    }
  }, []);

  // Initialize WebSocket connection
  const setupWebSocket = useCallback(() => {
    if (!useWebSocket) return;

    const ws = getFyersWebSocket();
    wsRef.current = ws;

    // Subscribe to all symbols
    symbols.forEach((symbol) => {
      ws.subscribe(symbol, (data) => {
        setState((prev) => ({
          ...prev,
          quotes: {
            ...prev.quotes,
            [symbol]: data,
          },
          lastUpdate: new Date(),
        }));
      });
    });

    ws.connect();

    setState((prev) => ({ ...prev, isConnected: ws.isConnected() }));
  }, [symbols, useWebSocket]);

  // Cleanup WebSocket
  const cleanupWebSocket = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.disconnect();
      wsRef.current = null;
    }
  }, []);

  // Initial data fetch
  useEffect(() => {
    const initialize = async () => {
      setState((prev) => ({ ...prev, isLoading: true }));

      await checkConnection();
      await fetchMarketData();

      if (symbols.length > 0) {
        await fetchQuotes(symbols);
      }

      await fetchPositions();

      setState((prev) => ({ ...prev, isLoading: false }));
    };

    initialize();
  }, []); // Run once on mount

  // Setup auto-refresh
  useEffect(() => {
    if (!autoRefresh || useWebSocket) return;

    refreshTimerRef.current = setInterval(() => {
      fetchMarketData();
      if (symbols.length > 0) {
        fetchQuotes(symbols);
      }
      fetchPositions();
    }, refreshInterval);

    return () => {
      if (refreshTimerRef.current) {
        clearInterval(refreshTimerRef.current);
      }
    };
  }, [autoRefresh, useWebSocket, refreshInterval, fetchMarketData, fetchQuotes, fetchPositions, symbols]);

  // Setup WebSocket
  useEffect(() => {
    if (useWebSocket) {
      setupWebSocket();
    }

    return () => {
      cleanupWebSocket();
    };
  }, [useWebSocket, setupWebSocket, cleanupWebSocket]);

  // Manual refresh function
  const refresh = useCallback(async () => {
    setState((prev) => ({ ...prev, isLoading: true }));
    await fetchMarketData();
    if (symbols.length > 0) {
      await fetchQuotes(symbols);
    }
    await fetchPositions();
    setState((prev) => ({ ...prev, isLoading: false }));
  }, [fetchMarketData, fetchQuotes, fetchPositions, symbols]);

  return {
    ...state,
    refresh,
    checkConnection,
    fetchQuotes: useCallback((syms: string[]) => fetchQuotes(syms), [fetchQuotes]),
  };
}

// Hook specifically for index data (NIFTY, Bank NIFTY, etc.)
export function useIndices() {
  const { marketData, isLoading, error, lastUpdate, refresh } = useMarketData({
    autoRefresh: true,
    refreshInterval: 5000,
  });

  const indices = marketData?.nifty && marketData?.bank_nifty
    ? [
        {
          ...marketData.nifty,
          symbol: 'NIFTY 50',
        },
        {
          ...marketData.bank_nifty,
          symbol: 'BANK NIFTY',
        },
      ]
    : [];

  return {
    indices,
    marketStatus: marketData?.market_status,
    dataSource: marketData?.data_source,
    isLoading,
    error,
    lastUpdate,
    refresh,
  };
}

// Hook for positions with P&L calculation
export function usePositions() {
  const { positions, isLoading, error, lastUpdate, refresh } = useMarketData({
    autoRefresh: true,
    refreshInterval: 10000,
  });

  const totalPnL = positions.reduce((sum, pos) => sum + pos.pnl, 0);
  const profitablePositions = positions.filter((pos) => pos.pnl > 0).length;
  const losingPositions = positions.filter((pos) => pos.pnl < 0).length;

  return {
    positions,
    totalPnL,
    profitablePositions,
    losingPositions,
    isLoading,
    error,
    lastUpdate,
    refresh,
  };
}
