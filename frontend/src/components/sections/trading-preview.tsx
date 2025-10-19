'use client';

import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Play, Pause } from 'lucide-react';

const mockData = [
  { symbol: 'BTC/USDT', price: 45234.56, change: 2.34, volume: '2.1B' },
  { symbol: 'ETH/USDT', price: 2845.23, change: -1.23, volume: '1.8B' },
  { symbol: 'BNB/USDT', price: 345.67, change: 5.67, volume: '890M' },
  { symbol: 'ADA/USDT', price: 0.4523, change: 3.45, volume: '456M' },
  { symbol: 'SOL/USDT', price: 98.76, change: -2.34, volume: '345M' },
];

export function TradingPreview() {
  const [isPlaying, setIsPlaying] = useState(true);
  const [currentPrices, setCurrentPrices] = useState(mockData);

  useEffect(() => {
    if (!isPlaying) return;

    const interval = setInterval(() => {
      setCurrentPrices(prev => 
        prev.map(item => ({
          ...item,
          price: item.price + (Math.random() - 0.5) * item.price * 0.01,
          change: (Math.random() - 0.5) * 10
        }))
      );
    }, 2000);

    return () => clearInterval(interval);
  }, [isPlaying]);

  return (
    <section className="py-24 relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-slate-800 to-slate-900"></div>
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c0 1.105-.895 2-2 2s-2-.895-2-2 .895-2 2-2 2 .895 2 2zm24 0c0 1.105-.895 2-2 2s-2-.895-2-2 .895-2 2-2 2 .895 2 2z' fill='%23ffffff' fill-opacity='0.05'/%3E%3C/svg%3E")`,
        }}></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            See It In
            <span className="bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent"> Action</span>
          </h2>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Experience our real-time trading interface with live market data and advanced features
          </p>
        </div>

        {/* Mock Trading Interface */}
        <div className="bg-slate-900/80 backdrop-blur-sm border border-slate-700 rounded-2xl overflow-hidden shadow-2xl">
          {/* Header */}
          <div className="bg-slate-800 px-6 py-4 border-b border-slate-700">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-red-400 rounded-full"></div>
                  <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
                  <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                </div>
                <span className="text-white font-semibold">AlgoProject Trading Dashboard</span>
              </div>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setIsPlaying(!isPlaying)}
                  className="flex items-center space-x-2 px-3 py-1 bg-blue-500 hover:bg-blue-600 text-white rounded text-sm transition-colors"
                >
                  {isPlaying ? <Pause className="h-3 w-3" /> : <Play className="h-3 w-3" />}
                  <span>{isPlaying ? 'Pause' : 'Play'}</span>
                </button>
                <div className="flex items-center space-x-1 px-3 py-1 bg-green-500/20 border border-green-500 rounded text-green-400 text-sm">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  <span>Live</span>
                </div>
              </div>
            </div>
          </div>

          {/* Trading Interface */}
          <div className="p-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Market Watch */}
              <div className="lg:col-span-2">
                <h3 className="text-lg font-semibold text-white mb-4">Market Watch</h3>
                <div className="space-y-2">
                  {currentPrices.map((item, index) => (
                    <div
                      key={item.symbol}
                      className="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg hover:bg-slate-700/50 transition-colors"
                    >
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-sm font-semibold">
                          {item.symbol.split('/')[0].charAt(0)}
                        </div>
                        <div>
                          <div className="text-white font-medium">{item.symbol}</div>
                          <div className="text-slate-400 text-sm">Volume: {item.volume}</div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-white font-semibold">
                          ${item.price.toFixed(item.symbol.includes('ADA') ? 4 : 2)}
                        </div>
                        <div className={`flex items-center space-x-1 text-sm ${
                          item.change >= 0 ? 'text-green-400' : 'text-red-400'
                        }`}>
                          {item.change >= 0 ? (
                            <TrendingUp className="h-3 w-3" />
                          ) : (
                            <TrendingDown className="h-3 w-3" />
                          )}
                          <span>{item.change >= 0 ? '+' : ''}{item.change.toFixed(2)}%</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Quick Actions */}
              <div>
                <h3 className="text-lg font-semibold text-white mb-4">Quick Trade</h3>
                <div className="space-y-4">
                  <div className="bg-slate-800/50 rounded-lg p-4">
                    <div className="text-slate-400 text-sm mb-2">Symbol</div>
                    <div className="text-white font-semibold">BTC/USDT</div>
                  </div>
                  <div className="bg-slate-800/50 rounded-lg p-4">
                    <div className="text-slate-400 text-sm mb-2">Amount</div>
                    <div className="text-white">$10,000</div>
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <button className="bg-green-500 hover:bg-green-600 text-white py-3 rounded-lg font-semibold transition-colors">
                      BUY
                    </button>
                    <button className="bg-red-500 hover:bg-red-600 text-white py-3 rounded-lg font-semibold transition-colors">
                      SELL
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Features Highlight */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="w-16 h-16 bg-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <TrendingUp className="h-8 w-8 text-blue-400" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">Real-Time Updates</h3>
            <p className="text-slate-400">Live market data with millisecond precision</p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Play className="h-8 w-8 text-green-400" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">One-Click Trading</h3>
            <p className="text-slate-400">Execute trades instantly with advanced order types</p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-purple-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <TrendingDown className="h-8 w-8 text-purple-400" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">Advanced Analytics</h3>
            <p className="text-slate-400">Comprehensive charts and technical indicators</p>
          </div>
        </div>
      </div>
    </section>
  );
}