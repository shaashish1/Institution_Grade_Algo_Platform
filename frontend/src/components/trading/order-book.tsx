'use client';

import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Volume2, AlertCircle } from 'lucide-react';

interface OrderBookEntry {
  price: number;
  size: number;
  total: number;
  percentage: number;
}

interface OrderBookProps {
  symbol?: string;
  precision?: number;
}

export function OrderBook({ symbol = 'NIFTY', precision = 2 }: OrderBookProps) {
  const [bids, setBids] = useState<OrderBookEntry[]>([]);
  const [asks, setAsks] = useState<OrderBookEntry[]>([]);
  const [spread, setSpread] = useState(0);
  const [lastPrice, setLastPrice] = useState(23150.50);
  const [lastChange, setLastChange] = useState(125.75);

  useEffect(() => {
    // Generate mock order book data
    const generateOrderBook = () => {
      const basePrice = lastPrice;
      
      // Generate bids (buy orders)
      const newBids: OrderBookEntry[] = [];
      let totalBidSize = 0;
      for (let i = 0; i < 10; i++) {
        const price = basePrice - (i + 1) * 0.25;
        const size = Math.floor(Math.random() * 1000) + 100;
        totalBidSize += size;
        newBids.push({
          price,
          size,
          total: totalBidSize,
          percentage: 0 // Will be calculated after
        });
      }
      
      // Generate asks (sell orders)
      const newAsks: OrderBookEntry[] = [];
      let totalAskSize = 0;
      for (let i = 0; i < 10; i++) {
        const price = basePrice + (i + 1) * 0.25;
        const size = Math.floor(Math.random() * 1000) + 100;
        totalAskSize += size;
        newAsks.push({
          price,
          size,
          total: totalAskSize,
          percentage: 0 // Will be calculated after
        });
      }
      
      // Calculate percentages
      const maxBidTotal = Math.max(...newBids.map(b => b.total));
      const maxAskTotal = Math.max(...newAsks.map(a => a.total));
      
      newBids.forEach(bid => bid.percentage = (bid.total / maxBidTotal) * 100);
      newAsks.forEach(ask => ask.percentage = (ask.total / maxAskTotal) * 100);
      
      setBids(newBids);
      setAsks(newAsks);
      setSpread(newAsks[0]?.price - newBids[0]?.price);
    };

    generateOrderBook();
    const interval = setInterval(generateOrderBook, 2000);
    return () => clearInterval(interval);
  }, [lastPrice]);

  const formatPrice = (price: number) => price.toFixed(precision);
  const formatSize = (size: number) => size.toLocaleString();

  return (
    <div className="bg-slate-900 rounded-xl border border-slate-800 p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-white flex items-center">
          <Volume2 className="h-5 w-5 mr-2 text-blue-400" />
          Order Book - {symbol}
        </h3>
        <div className="flex items-center space-x-4 text-sm">
          <div className="text-slate-400">
            Spread: <span className="text-white font-medium">{spread.toFixed(2)}</span>
          </div>
          <div className="text-slate-400">
            Last: <span className={`font-medium ${lastChange >= 0 ? 'text-green-400' : 'text-red-400'}`}>
              {formatPrice(lastPrice)}
            </span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Bids (Buy Orders) */}
        <div>
          <div className="flex items-center justify-between mb-3">
            <h4 className="font-medium text-green-400 flex items-center">
              <TrendingUp className="h-4 w-4 mr-1" />
              Bids
            </h4>
            <div className="text-xs text-slate-400">Price | Size | Total</div>
          </div>
          
          <div className="space-y-1">
            {bids.map((bid, index) => (
              <div 
                key={index}
                className="relative grid grid-cols-3 gap-2 py-1 px-2 rounded text-sm hover:bg-slate-800/50 transition-colors"
              >
                <div 
                  className="absolute left-0 top-0 bottom-0 bg-green-500/10 rounded"
                  style={{ width: `${bid.percentage}%` }}
                />
                <div className="text-green-400 font-mono relative z-10">
                  {formatPrice(bid.price)}
                </div>
                <div className="text-white font-mono relative z-10 text-right">
                  {formatSize(bid.size)}
                </div>
                <div className="text-slate-400 font-mono relative z-10 text-right">
                  {formatSize(bid.total)}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Asks (Sell Orders) */}
        <div>
          <div className="flex items-center justify-between mb-3">
            <h4 className="font-medium text-red-400 flex items-center">
              <TrendingDown className="h-4 w-4 mr-1" />
              Asks
            </h4>
            <div className="text-xs text-slate-400">Price | Size | Total</div>
          </div>
          
          <div className="space-y-1">
            {asks.map((ask, index) => (
              <div 
                key={index}
                className="relative grid grid-cols-3 gap-2 py-1 px-2 rounded text-sm hover:bg-slate-800/50 transition-colors"
              >
                <div 
                  className="absolute left-0 top-0 bottom-0 bg-red-500/10 rounded"
                  style={{ width: `${ask.percentage}%` }}
                />
                <div className="text-red-400 font-mono relative z-10">
                  {formatPrice(ask.price)}
                </div>
                <div className="text-white font-mono relative z-10 text-right">
                  {formatSize(ask.size)}
                </div>
                <div className="text-slate-400 font-mono relative z-10 text-right">
                  {formatSize(ask.total)}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Market Statistics */}
      <div className="mt-6 pt-4 border-t border-slate-800">
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-slate-400 text-xs mb-1">Total Bid Volume</div>
            <div className="text-green-400 font-semibold">
              {formatSize(bids.reduce((sum, bid) => sum + bid.size, 0))}
            </div>
          </div>
          <div>
            <div className="text-slate-400 text-xs mb-1">Spread %</div>
            <div className="text-white font-semibold">
              {((spread / lastPrice) * 100).toFixed(4)}%
            </div>
          </div>
          <div>
            <div className="text-slate-400 text-xs mb-1">Total Ask Volume</div>
            <div className="text-red-400 font-semibold">
              {formatSize(asks.reduce((sum, ask) => sum + ask.size, 0))}
            </div>
          </div>
        </div>
      </div>

      {/* Market Depth Indicator */}
      <div className="mt-4 flex items-center justify-center text-xs text-slate-400">
        <AlertCircle className="h-3 w-3 mr-1" />
        Real-time market depth visualization
      </div>
    </div>
  );
}

export function TradingPanel({ symbol }: { symbol: string }) {
  return (
    <div className="bg-slate-900 rounded-lg border border-slate-700 p-4">
      <h3 className="text-lg font-semibold text-white mb-4">Trading Panel - {symbol}</h3>
      <div className="grid grid-cols-2 gap-4">
        <button className="bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-semibold">
          BUY
        </button>
        <button className="bg-red-600 hover:bg-red-700 text-white py-3 rounded-lg font-semibold">
          SELL
        </button>
      </div>
    </div>
  );
}

export function RecentTrades({ symbol }: { symbol: string }) {
  return (
    <div className="bg-slate-900 rounded-lg border border-slate-700 p-4 h-96">
      <h3 className="text-lg font-semibold text-white mb-4">Recent Trades - {symbol}</h3>
      <div className="text-center text-slate-400 mt-20">
        Recent trades will appear here
      </div>
    </div>
  );
}