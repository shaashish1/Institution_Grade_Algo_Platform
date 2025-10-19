'use client';

import React from 'react';

interface MarketDataProps {
  symbol: string;
  onSymbolChange: (symbol: string) => void;
}

const popularSymbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'SOL/USDT'];

export function MarketData({ symbol, onSymbolChange }: MarketDataProps) {
  return (
    <div className="bg-slate-900 rounded-lg border border-slate-700 p-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-6">
          <select
            value={symbol}
            onChange={(e) => onSymbolChange(e.target.value)}
            className="bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-white focus:border-blue-500"
          >
            {popularSymbols.map(sym => (
              <option key={sym} value={sym}>{sym}</option>
            ))}
          </select>
          
          <div className="flex items-center space-x-4">
            <div>
              <span className="text-sm text-slate-400">24h Volume</span>
              <p className="text-white font-semibold">$1.2B</p>
            </div>
            <div>
              <span className="text-sm text-slate-400">24h High</span>
              <p className="text-green-400 font-semibold">$47,250</p>
            </div>
            <div>
              <span className="text-sm text-slate-400">24h Low</span>
              <p className="text-red-400 font-semibold">$44,800</p>
            </div>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          <span className="text-sm text-green-400">Real-time data</span>
        </div>
      </div>
    </div>
  );
}