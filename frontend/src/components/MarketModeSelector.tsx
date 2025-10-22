"use client";

/**
 * Market & Mode Selector Component
 * 
 * Top-bar selector for switching between:
 * - Market: NSE (stocks) or Crypto
 * - Mode: Backtest, Paper Trading, or Live Trading
 * 
 * Features:
 * - Visual indicator of current selection
 * - Dropdown menus for easy switching
 * - Syncing status indicator
 * - Responsive design
 */

import React, { useState } from 'react';
import { useTradingContext, Market, TradingMode } from '@/contexts/TradingContext';
import { ChevronDown, Activity, Database, Zap, TrendingUp, Bitcoin } from 'lucide-react';

export default function MarketModeSelector() {
  const { market, mode, setMarket, setMode, isSyncing } = useTradingContext();
  const [showMarketMenu, setShowMarketMenu] = useState(false);
  const [showModeMenu, setShowModeMenu] = useState(false);

  // ===== MARKET OPTIONS =====

  const marketOptions: { value: Market; label: string; icon: React.ReactNode; description: string }[] = [
    {
      value: 'NSE',
      label: 'NSE Stocks',
      icon: <TrendingUp className="w-4 h-4" />,
      description: 'Indian Stock Market',
    },
    {
      value: 'Crypto',
      label: 'Cryptocurrency',
      icon: <Bitcoin className="w-4 h-4" />,
      description: 'Digital Assets',
    },
  ];

  // ===== MODE OPTIONS =====

  const modeOptions: { value: TradingMode; label: string; icon: React.ReactNode; description: string; color: string }[] = [
    {
      value: 'Backtest',
      label: 'Backtest',
      icon: <Database className="w-4 h-4" />,
      description: 'Test strategies on historical data',
      color: 'text-blue-500',
    },
    {
      value: 'Paper',
      label: 'Paper Trading',
      icon: <Activity className="w-4 h-4" />,
      description: 'Simulate real-time trading',
      color: 'text-yellow-500',
    },
    {
      value: 'Live',
      label: 'Live Trading',
      icon: <Zap className="w-4 h-4" />,
      description: 'Real money trading',
      color: 'text-red-500',
    },
  ];

  // ===== HANDLERS =====

  const handleMarketChange = (newMarket: Market) => {
    setMarket(newMarket);
    setShowMarketMenu(false);
  };

  const handleModeChange = (newMode: TradingMode) => {
    setMode(newMode);
    setShowModeMenu(false);
  };

  // ===== RENDER =====

  const currentMarket = marketOptions.find(m => m.value === market);
  const currentMode = modeOptions.find(m => m.value === mode);

  return (
    <div className="flex items-center gap-3">
      {/* ===== MARKET SELECTOR ===== */}
      <div className="relative">
        <button
          onClick={() => setShowMarketMenu(!showMarketMenu)}
          className="flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg border border-gray-600 transition-colors"
          aria-label="Select Market"
        >
          {currentMarket?.icon}
          <span className="font-medium text-white">{currentMarket?.label}</span>
          <ChevronDown className={`w-4 h-4 text-gray-400 transition-transform ${showMarketMenu ? 'rotate-180' : ''}`} />
        </button>

        {/* Market Dropdown */}
        {showMarketMenu && (
          <>
            <div 
              className="fixed inset-0 z-10" 
              onClick={() => setShowMarketMenu(false)}
            />
            <div className="absolute top-full left-0 mt-2 w-64 bg-gray-800 border border-gray-600 rounded-lg shadow-xl z-20 overflow-hidden">
              {marketOptions.map((option) => (
                <button
                  key={option.value}
                  onClick={() => handleMarketChange(option.value)}
                  className={`w-full flex items-start gap-3 px-4 py-3 hover:bg-gray-700 transition-colors ${
                    market === option.value ? 'bg-gray-700' : ''
                  }`}
                >
                  <div className="mt-0.5">{option.icon}</div>
                  <div className="flex-1 text-left">
                    <div className="font-medium text-white">{option.label}</div>
                    <div className="text-xs text-gray-400">{option.description}</div>
                  </div>
                  {market === option.value && (
                    <div className="w-2 h-2 rounded-full bg-green-500 mt-1.5" />
                  )}
                </button>
              ))}
            </div>
          </>
        )}
      </div>

      {/* ===== DIVIDER ===== */}
      <div className="h-8 w-px bg-gray-600" />

      {/* ===== MODE SELECTOR ===== */}
      <div className="relative">
        <button
          onClick={() => setShowModeMenu(!showModeMenu)}
          className="flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg border border-gray-600 transition-colors"
          aria-label="Select Trading Mode"
        >
          <span className={currentMode?.color}>{currentMode?.icon}</span>
          <span className="font-medium text-white">{currentMode?.label}</span>
          <ChevronDown className={`w-4 h-4 text-gray-400 transition-transform ${showModeMenu ? 'rotate-180' : ''}`} />
        </button>

        {/* Mode Dropdown */}
        {showModeMenu && (
          <>
            <div 
              className="fixed inset-0 z-10" 
              onClick={() => setShowModeMenu(false)}
            />
            <div className="absolute top-full left-0 mt-2 w-72 bg-gray-800 border border-gray-600 rounded-lg shadow-xl z-20 overflow-hidden">
              {modeOptions.map((option) => (
                <button
                  key={option.value}
                  onClick={() => handleModeChange(option.value)}
                  className={`w-full flex items-start gap-3 px-4 py-3 hover:bg-gray-700 transition-colors ${
                    mode === option.value ? 'bg-gray-700' : ''
                  }`}
                >
                  <div className={`mt-0.5 ${option.color}`}>{option.icon}</div>
                  <div className="flex-1 text-left">
                    <div className="font-medium text-white">{option.label}</div>
                    <div className="text-xs text-gray-400">{option.description}</div>
                  </div>
                  {mode === option.value && (
                    <div className={`w-2 h-2 rounded-full ${option.color.replace('text-', 'bg-')} mt-1.5`} />
                  )}
                </button>
              ))}
            </div>
          </>
        )}
      </div>

      {/* ===== SYNC INDICATOR ===== */}
      {isSyncing && (
        <div className="flex items-center gap-2 text-xs text-gray-400">
          <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
          Syncing...
        </div>
      )}
    </div>
  );
}
