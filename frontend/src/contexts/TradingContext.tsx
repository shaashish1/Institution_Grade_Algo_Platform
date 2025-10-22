"use client";

/**
 * Trading Context - Global Market & Mode Selector
 * 
 * Manages:
 * - Market selection: NSE (stocks) or Crypto
 * - Mode selection: Backtest, Paper Trading, or Live Trading
 * - Persistence: localStorage + backend user profile sync
 * - Global state: Available to all pages/components
 */

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

// ===== TYPE DEFINITIONS =====

export type Market = 'NSE' | 'Crypto';
export type TradingMode = 'Backtest' | 'Paper' | 'Live';

export interface TradingContextState {
  // Current selections
  market: Market;
  mode: TradingMode;
  
  // Actions
  setMarket: (market: Market) => void;
  setMode: (mode: TradingMode) => void;
  
  // Combined setter
  setContext: (market: Market, mode: TradingMode) => void;
  
  // Sync status
  isSyncing: boolean;
  lastSynced: Date | null;
}

// ===== DEFAULT VALUES =====

const DEFAULT_MARKET: Market = 'NSE';
const DEFAULT_MODE: TradingMode = 'Paper';

const STORAGE_KEYS = {
  MARKET: 'trading_market',
  MODE: 'trading_mode',
  LAST_SYNCED: 'trading_last_synced',
};

// ===== CONTEXT =====

const TradingContext = createContext<TradingContextState | undefined>(undefined);

// ===== PROVIDER =====

interface TradingProviderProps {
  children: ReactNode;
}

export function TradingProvider({ children }: TradingProviderProps) {
  const [market, setMarketState] = useState<Market>(DEFAULT_MARKET);
  const [mode, setModeState] = useState<TradingMode>(DEFAULT_MODE);
  const [isSyncing, setIsSyncing] = useState(false);
  const [lastSynced, setLastSynced] = useState<Date | null>(null);
  const [isInitialized, setIsInitialized] = useState(false);

  // ===== INITIALIZATION =====
  // Load from localStorage on mount
  useEffect(() => {
    if (typeof window === 'undefined') return;

    try {
      const savedMarket = localStorage.getItem(STORAGE_KEYS.MARKET) as Market | null;
      const savedMode = localStorage.getItem(STORAGE_KEYS.MODE) as TradingMode | null;
      const savedLastSynced = localStorage.getItem(STORAGE_KEYS.LAST_SYNCED);

      if (savedMarket && (savedMarket === 'NSE' || savedMarket === 'Crypto')) {
        setMarketState(savedMarket);
      }

      if (savedMode && ['Backtest', 'Paper', 'Live'].includes(savedMode)) {
        setModeState(savedMode);
      }

      if (savedLastSynced) {
        setLastSynced(new Date(savedLastSynced));
      }

      setIsInitialized(true);
      console.log('✅ Trading Context initialized:', { market: savedMarket || DEFAULT_MARKET, mode: savedMode || DEFAULT_MODE });
    } catch (error) {
      console.error('Error loading trading context from localStorage:', error);
      setIsInitialized(true);
    }
  }, []);

  // ===== PERSIST TO LOCALSTORAGE =====
  const persistToLocalStorage = (newMarket: Market, newMode: TradingMode) => {
    if (typeof window === 'undefined') return;

    try {
      localStorage.setItem(STORAGE_KEYS.MARKET, newMarket);
      localStorage.setItem(STORAGE_KEYS.MODE, newMode);
      localStorage.setItem(STORAGE_KEYS.LAST_SYNCED, new Date().toISOString());
      console.log('💾 Saved to localStorage:', { market: newMarket, mode: newMode });
    } catch (error) {
      console.error('Error saving to localStorage:', error);
    }
  };

  // ===== SYNC TO BACKEND =====
  const syncToBackend = async (newMarket: Market, newMode: TradingMode) => {
    setIsSyncing(true);

    try {
      const response = await fetch('http://localhost:8000/api/user/preferences', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          market: newMarket,
          mode: newMode,
          timestamp: new Date().toISOString(),
        }),
      });

      if (response.ok) {
        const syncTime = new Date();
        setLastSynced(syncTime);
        localStorage.setItem(STORAGE_KEYS.LAST_SYNCED, syncTime.toISOString());
        console.log('✅ Synced to backend:', { market: newMarket, mode: newMode });
      } else {
        console.warn('⚠️ Failed to sync to backend:', response.statusText);
      }
    } catch (error) {
      console.error('❌ Error syncing to backend:', error);
      // Non-critical error - continue with localStorage only
    } finally {
      setIsSyncing(false);
    }
  };

  // ===== SETTERS WITH PERSISTENCE =====

  const setMarket = (newMarket: Market) => {
    if (newMarket === market) return; // No change

    setMarketState(newMarket);
    persistToLocalStorage(newMarket, mode);
    syncToBackend(newMarket, mode);

    // Dispatch custom event for other components to listen
    window.dispatchEvent(new CustomEvent('tradingContextChanged', {
      detail: { market: newMarket, mode }
    }));

    console.log('🔄 Market changed:', newMarket);
  };

  const setMode = async (newMode: TradingMode) => {
    if (newMode === mode) return; // No change

    // ===== LIVE MODE VALIDATION =====
    if (newMode === 'Live') {
      console.log('🔴 Attempting to switch to Live mode - validating exchange configuration...');
      
      try {
        // Check if exchange is configured
        const response = await fetch('http://localhost:8000/api/settings/exchanges');
        const exchanges = await response.json();
        
        const hasConfiguredExchange = exchanges && exchanges.length > 0;
        
        if (!hasConfiguredExchange) {
          console.warn('⚠️ No exchanges configured - cannot switch to Live mode');
          
          // Show alert to user
          if (window.confirm(
            '⚠️ Live Trading requires exchange configuration.\n\n' +
            'Please configure your exchange API keys in Settings first.\n\n' +
            'Click OK to go to Settings, or Cancel to stay in current mode.'
          )) {
            window.location.href = '/settings/exchanges';
          }
          return; // Don't switch mode
        }
        
        // Show warning dialog before enabling Live mode
        const userConfirmed = window.confirm(
          '🔴 LIVE TRADING MODE\n\n' +
          'You are about to switch to LIVE trading mode.\n' +
          'Real money will be used for trades.\n\n' +
          'Are you sure you want to continue?'
        );
        
        if (!userConfirmed) {
          console.log('❌ User cancelled Live mode switch');
          return; // Don't switch mode
        }
        
        console.log('✅ Exchange configured - switching to Live mode');
      } catch (error) {
        console.error('❌ Error checking exchange configuration:', error);
        alert('Error: Could not verify exchange configuration. Please check your settings.');
        return; // Don't switch mode
      }
    }

    setModeState(newMode);
    persistToLocalStorage(market, newMode);
    syncToBackend(market, newMode);

    // Dispatch custom event
    window.dispatchEvent(new CustomEvent('tradingContextChanged', {
      detail: { market, mode: newMode }
    }));

    console.log('🔄 Mode changed:', newMode);
  };

  const setContext = (newMarket: Market, newMode: TradingMode) => {
    if (newMarket === market && newMode === mode) return; // No change

    setMarketState(newMarket);
    setModeState(newMode);
    persistToLocalStorage(newMarket, newMode);
    syncToBackend(newMarket, newMode);

    // Dispatch custom event
    window.dispatchEvent(new CustomEvent('tradingContextChanged', {
      detail: { market: newMarket, mode: newMode }
    }));

    console.log('🔄 Context changed:', { market: newMarket, mode: newMode });
  };

  // ===== CONTEXT VALUE =====

  const contextValue: TradingContextState = {
    market,
    mode,
    setMarket,
    setMode,
    setContext,
    isSyncing,
    lastSynced,
  };

  // Don't render children until initialized (prevents hydration issues)
  if (!isInitialized) {
    return null;
  }

  return (
    <TradingContext.Provider value={contextValue}>
      {children}
    </TradingContext.Provider>
  );
}

// ===== CUSTOM HOOK =====

export function useTradingContext() {
  const context = useContext(TradingContext);
  
  if (context === undefined) {
    throw new Error('useTradingContext must be used within a TradingProvider');
  }
  
  return context;
}

// ===== HELPER HOOKS =====

/**
 * Hook that returns true if current market is NSE
 */
export function useIsNSE() {
  const { market } = useTradingContext();
  return market === 'NSE';
}

/**
 * Hook that returns true if current market is Crypto
 */
export function useIsCrypto() {
  const { market } = useTradingContext();
  return market === 'Crypto';
}

/**
 * Hook that returns true if current mode is Live
 */
export function useIsLive() {
  const { mode } = useTradingContext();
  return mode === 'Live';
}

/**
 * Hook that returns true if current mode is Paper
 */
export function useIsPaper() {
  const { mode } = useTradingContext();
  return mode === 'Paper';
}

/**
 * Hook that returns true if current mode is Backtest
 */
export function useIsBacktest() {
  const { mode } = useTradingContext();
  return mode === 'Backtest';
}
