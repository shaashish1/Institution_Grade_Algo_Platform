'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { 
  TrendingUp, BarChart3, DollarSign, Activity, Target, 
  Clock, Play, Pause, RefreshCw, Bell, Settings, Eye,
  ArrowUp, ArrowDown, Info
} from 'lucide-react';

export default function TradingPage() {
  const [isLive, setIsLive] = useState(false);

  const marketData = [
    { symbol: 'NIFTY 50', price: 21450.30, change: 156.80, changePercent: 0.74, volume: '45.2M' },
    { symbol: 'BANK NIFTY', price: 45234.50, change: -123.40, changePercent: -0.27, volume: '32.8M' },
    { symbol: 'SENSEX', price: 71289.50, change: 234.60, changePercent: 0.33, volume: '51.3M' },
    { symbol: 'FINNIFTY', price: 19876.20, change: 89.30, changePercent: 0.45, volume: '28.1M' },
  ];

  const activePositions = [
    { symbol: 'RELIANCE', qty: 50, entry: 2450.00, current: 2478.50, pnl: 1425.00 },
    { symbol: 'TCS', qty: 30, entry: 3650.00, current: 3625.00, pnl: -750.00 },
    { symbol: 'INFY', qty: 100, entry: 1550.00, current: 1568.00, pnl: 1800.00 },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Breadcrumb */}
      <div className="bg-slate-900 border-b border-slate-800 px-6 py-4">
        <nav className="flex items-center space-x-2 text-sm text-slate-400">
          <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
          <span>/</span>
          <span className="text-white">Live Trading</span>
        </nav>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
                Live Trading Dashboard
              </h1>
              <p className="text-xl text-slate-300">
                Real-time market data and order execution
              </p>
            </div>
            
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setIsLive(!isLive)}
                className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-medium transition-all ${
                  isLive 
                    ? 'bg-green-600 hover:bg-green-700 text-white' 
                    : 'bg-slate-800 hover:bg-slate-700 text-slate-300'
                }`}
              >
                {isLive ? <Pause className="h-5 w-5" /> : <Play className="h-5 w-5" />}
                <span>{isLive ? 'Trading Live' : 'Start Trading'}</span>
              </button>
              
              <button className="p-3 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors">
                <Settings className="h-5 w-5" />
              </button>
            </div>
          </div>

          {/* Status Bar */}
          <div className="flex items-center space-x-6 text-sm">
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${isLive ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`}></div>
              <span className="text-slate-300">
                {isLive ? 'Market Open' : 'Market Closed'}
              </span>
            </div>
            <div className="flex items-center space-x-2 text-slate-400">
              <Clock className="h-4 w-4" />
              <span>Last Update: {new Date().toLocaleTimeString()}</span>
            </div>
            <button className="flex items-center space-x-2 text-blue-400 hover:text-blue-300">
              <RefreshCw className="h-4 w-4" />
              <span>Refresh</span>
            </button>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-slate-400">Total P&L</span>
              <DollarSign className="h-5 w-5 text-green-400" />
            </div>
            <div className="text-2xl font-bold text-green-400">₹24,750</div>
            <div className="text-sm text-slate-400 mt-1">+5.2% today</div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-slate-400">Active Positions</span>
              <Activity className="h-5 w-5 text-blue-400" />
            </div>
            <div className="text-2xl font-bold text-white">3</div>
            <div className="text-sm text-slate-400 mt-1">2 profitable</div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-slate-400">Orders Today</span>
              <Target className="h-5 w-5 text-purple-400" />
            </div>
            <div className="text-2xl font-bold text-white">12</div>
            <div className="text-sm text-slate-400 mt-1">8 executed</div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-slate-400">Win Rate</span>
              <BarChart3 className="h-5 w-5 text-yellow-400" />
            </div>
            <div className="text-2xl font-bold text-white">68%</div>
            <div className="text-sm text-slate-400 mt-1">This week</div>
          </div>
        </div>

        {/* Market Watch */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-white">Market Watch</h2>
            <button className="flex items-center space-x-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors text-sm">
              <Bell className="h-4 w-4" />
              <span>Add Alert</span>
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-800">
                  <th className="text-left py-3 px-4 text-sm font-medium text-slate-400">Symbol</th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-slate-400">Price</th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-slate-400">Change</th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-slate-400">% Change</th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-slate-400">Volume</th>
                  <th className="text-center py-3 px-4 text-sm font-medium text-slate-400">Action</th>
                </tr>
              </thead>
              <tbody>
                {marketData.map((item, index) => (
                  <tr key={index} className="border-b border-slate-800 hover:bg-slate-800/50 transition-colors">
                    <td className="py-4 px-4">
                      <div className="font-medium text-white">{item.symbol}</div>
                    </td>
                    <td className="py-4 px-4 text-right text-white font-mono">
                      ₹{item.price.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                    </td>
                    <td className={`py-4 px-4 text-right font-mono ${item.change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                      {item.change >= 0 ? '+' : ''}{item.change.toFixed(2)}
                    </td>
                    <td className="py-4 px-4 text-right">
                      <div className={`flex items-center justify-end space-x-1 ${item.changePercent >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {item.changePercent >= 0 ? <ArrowUp className="h-4 w-4" /> : <ArrowDown className="h-4 w-4" />}
                        <span className="font-mono">{Math.abs(item.changePercent)}%</span>
                      </div>
                    </td>
                    <td className="py-4 px-4 text-right text-slate-300 font-mono">{item.volume}</td>
                    <td className="py-4 px-4">
                      <div className="flex items-center justify-center space-x-2">
                        <button className="px-3 py-1 bg-green-600 hover:bg-green-700 text-white text-sm rounded transition-colors">
                          Buy
                        </button>
                        <button className="px-3 py-1 bg-red-600 hover:bg-red-700 text-white text-sm rounded transition-colors">
                          Sell
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Active Positions */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-white">Active Positions</h2>
            <Link 
              href="/portfolio"
              className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors text-sm"
            >
              <Eye className="h-4 w-4" />
              <span>View All</span>
            </Link>
          </div>

          {activePositions.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-slate-800">
                    <th className="text-left py-3 px-4 text-sm font-medium text-slate-400">Symbol</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-slate-400">Qty</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-slate-400">Entry</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-slate-400">Current</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-slate-400">P&L</th>
                    <th className="text-center py-3 px-4 text-sm font-medium text-slate-400">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {activePositions.map((position, index) => (
                    <tr key={index} className="border-b border-slate-800 hover:bg-slate-800/50 transition-colors">
                      <td className="py-4 px-4">
                        <div className="font-medium text-white">{position.symbol}</div>
                      </td>
                      <td className="py-4 px-4 text-right text-slate-300 font-mono">{position.qty}</td>
                      <td className="py-4 px-4 text-right text-slate-300 font-mono">
                        ₹{position.entry.toFixed(2)}
                      </td>
                      <td className="py-4 px-4 text-right text-white font-mono">
                        ₹{position.current.toFixed(2)}
                      </td>
                      <td className={`py-4 px-4 text-right font-mono font-bold ${position.pnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {position.pnl >= 0 ? '+' : ''}₹{position.pnl.toFixed(2)}
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center justify-center space-x-2">
                          <button className="px-3 py-1 bg-slate-700 hover:bg-slate-600 text-white text-sm rounded transition-colors">
                            Exit
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-12">
              <Activity className="h-12 w-12 text-slate-600 mx-auto mb-4" />
              <p className="text-slate-400">No active positions</p>
            </div>
          )}
        </div>

        {/* Info Banner */}
        <div className="mt-8 bg-blue-500/10 border border-blue-500/20 rounded-xl p-4">
          <div className="flex items-start space-x-3">
            <Info className="h-5 w-5 text-blue-400 mt-0.5 flex-shrink-0" />
            <div className="flex-1">
              <p className="text-sm text-blue-200">
                <strong>Note:</strong> This is a demo trading interface. To enable live trading, 
                connect your broker account in <Link href="/settings" className="underline hover:text-blue-300">Settings</Link>.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
