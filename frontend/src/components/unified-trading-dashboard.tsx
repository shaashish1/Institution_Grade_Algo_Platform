'use client';

import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, TrendingDown, BarChart3, DollarSign, Target, Activity, 
  Crown, Zap, AlertCircle, CheckCircle, Eye, PlayCircle, Settings,
  Calendar, Clock, Bell, RefreshCw, ArrowUpRight, ArrowDownRight,
  PieChart, LineChart, Users, Building2, Coins, BarChart2
} from 'lucide-react';
import Link from 'next/link';

interface MarketData {
  symbol: string;
  price: number;
  change: number;
  changePercent: number;
  volume: string;
  high: number;
  low: number;
}

interface Position {
  symbol: string;
  type: 'stock' | 'option' | 'crypto' | 'etf';
  quantity: number;
  entryPrice: number;
  currentPrice: number;
  pnl: number;
  pnlPercent: number;
  strike?: number;
  expiry?: string;
}

interface PortfolioSummary {
  totalValue: number;
  dayChange: number;
  dayChangePercent: number;
  totalPnL: number;
  totalPnLPercent: number;
  cash: number;
  positions: number;
}

interface RecentTrade {
  id: string;
  symbol: string;
  type: 'BUY' | 'SELL';
  quantity: number;
  price: number;
  timestamp: string;
  pnl?: number;
}

interface StrategyPerformance {
  name: string;
  totalTrades: number;
  winRate: number;
  totalPnL: number;
  monthlyReturn: number;
  status: 'active' | 'paused' | 'stopped';
}

export function UnifiedTradingDashboard() {
  const [portfolioSummary, setPortfolioSummary] = useState<PortfolioSummary>({
    totalValue: 12450000,
    dayChange: 156000,
    dayChangePercent: 1.27,
    totalPnL: 2450000,
    totalPnLPercent: 24.5,
    cash: 3200000,
    positions: 47
  });

  const [marketData, setMarketData] = useState<MarketData[]>([
    { symbol: 'NIFTY', price: 25709, change: 127.5, changePercent: 0.50, volume: '2.1M', high: 25750, low: 25650 },
    { symbol: 'BANKNIFTY', price: 54890, change: -245.8, changePercent: -0.45, volume: '1.8M', high: 55100, low: 54820 },
    { symbol: 'SENSEX', price: 84234, change: 89.2, changePercent: 0.11, volume: '890K', high: 84350, low: 84150 },
    { symbol: 'BTC/USDT', price: 98456, change: 1245.6, changePercent: 1.28, volume: '$2.1B', high: 98890, low: 97800 }
  ]);

  const [activePositions, setActivePositions] = useState<Position[]>([
    { symbol: 'NIFTY 25700 CE', type: 'option', quantity: 100, entryPrice: 156, currentPrice: 189, pnl: 3300, pnlPercent: 21.15, strike: 25700, expiry: '28-Nov-24' },
    { symbol: 'RELIANCE', type: 'stock', quantity: 50, entryPrice: 2450, currentPrice: 2478, pnl: 1400, pnlPercent: 1.14 },
    { symbol: 'BTC/USDT', type: 'crypto', quantity: 0.5, entryPrice: 96800, currentPrice: 98456, pnl: 828, pnlPercent: 1.71 },
    { symbol: 'NIFTYBEES', type: 'etf', quantity: 1000, entryPrice: 257.5, currentPrice: 259.2, pnl: 1700, pnlPercent: 0.66 }
  ]);

  const [recentTrades, setRecentTrades] = useState<RecentTrade[]>([
    { id: '1', symbol: 'NIFTY 25800 CE', type: 'SELL', quantity: 50, price: 92, timestamp: '2024-10-20 15:24', pnl: 2150 },
    { id: '2', symbol: 'HDFCBANK', type: 'BUY', quantity: 25, price: 1678, timestamp: '2024-10-20 14:58' },
    { id: '3', symbol: 'ETH/USDT', type: 'SELL', quantity: 2, price: 3456, timestamp: '2024-10-20 14:35', pnl: 189 }
  ]);

  const [strategyPerformance, setStrategyPerformance] = useState<StrategyPerformance[]>([
    { name: 'Iron Condor Weekly', totalTrades: 156, winRate: 68.5, totalPnL: 485000, monthlyReturn: 12.4, status: 'active' },
    { name: 'Momentum Breakout', totalTrades: 89, winRate: 62.1, totalPnL: 234000, monthlyReturn: 8.7, status: 'active' },
    { name: 'Grid Trading BTC', totalTrades: 234, winRate: 71.2, totalPnL: 156000, monthlyReturn: 15.2, status: 'paused' }
  ]);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  };

  const formatNumber = (value: number) => {
    if (value >= 10000000) return `₹${(value / 10000000).toFixed(1)}Cr`;
    if (value >= 100000) return `₹${(value / 100000).toFixed(1)}L`;
    if (value >= 1000) return `₹${(value / 1000).toFixed(1)}K`;
    return `₹${value.toFixed(0)}`;
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-400 bg-green-500/10';
      case 'paused': return 'text-yellow-400 bg-yellow-500/10';
      case 'stopped': return 'text-red-400 bg-red-500/10';
      default: return 'text-slate-400 bg-slate-500/10';
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4">
      <div className="max-w-full mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
              Trading Dashboard
            </h1>
            <p className="text-slate-400">
              Unified view of your portfolio, positions, and market opportunities
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            <button className="flex items-center px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors">
              <RefreshCw className="h-4 w-4 mr-2" />
              Refresh
            </button>
            <button className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors">
              <Settings className="h-4 w-4 mr-2" />
              Settings
            </button>
          </div>
        </div>

        {/* Portfolio Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-slate-400 text-sm font-medium">Total Portfolio Value</h3>
              <DollarSign className="h-5 w-5 text-blue-400" />
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              {formatCurrency(portfolioSummary.totalValue)}
            </div>
            <div className={`flex items-center text-sm ${
              portfolioSummary.dayChange >= 0 ? 'text-green-400' : 'text-red-400'
            }`}>
              {portfolioSummary.dayChange >= 0 ? (
                <TrendingUp className="h-4 w-4 mr-1" />
              ) : (
                <TrendingDown className="h-4 w-4 mr-1" />
              )}
              {formatNumber(Math.abs(portfolioSummary.dayChange))} ({portfolioSummary.dayChangePercent.toFixed(2)}%)
            </div>
          </div>

          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-slate-400 text-sm font-medium">Total P&L</h3>
              <Target className="h-5 w-5 text-green-400" />
            </div>
            <div className="text-2xl font-bold text-green-400 mb-1">
              +{formatCurrency(portfolioSummary.totalPnL)}
            </div>
            <div className="text-sm text-green-400">
              +{portfolioSummary.totalPnLPercent.toFixed(1)}% All Time
            </div>
          </div>

          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-slate-400 text-sm font-medium">Available Cash</h3>
              <Activity className="h-5 w-5 text-purple-400" />
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              {formatCurrency(portfolioSummary.cash)}
            </div>
            <div className="text-sm text-slate-400">
              Ready for trading
            </div>
          </div>

          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-slate-400 text-sm font-medium">Active Positions</h3>
              <BarChart3 className="h-5 w-5 text-yellow-400" />
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              {portfolioSummary.positions}
            </div>
            <div className="text-sm text-slate-400">
              Across all markets
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 mb-8">
          <Link href="/stocks/option-chain" className="group">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-blue-500 transition-all text-center">
              <Zap className="h-6 w-6 text-blue-400 mx-auto mb-2" />
              <div className="text-sm font-medium text-white group-hover:text-blue-400 transition-colors">
                Option Chain
              </div>
            </div>
          </Link>

          <Link href="/stocks/backtest/universal" className="group">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-purple-500 transition-all text-center">
              <Target className="h-6 w-6 text-purple-400 mx-auto mb-2" />
              <div className="text-sm font-medium text-white group-hover:text-purple-400 transition-colors">
                Backtest
              </div>
            </div>
          </Link>

          <Link href="/crypto" className="group">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-yellow-500 transition-all text-center">
              <Coins className="h-6 w-6 text-yellow-400 mx-auto mb-2" />
              <div className="text-sm font-medium text-white group-hover:text-yellow-400 transition-colors">
                Crypto
              </div>
            </div>
          </Link>

          <Link href="/stocks/derivatives" className="group">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-green-500 transition-all text-center">
              <BarChart2 className="h-6 w-6 text-green-400 mx-auto mb-2" />
              <div className="text-sm font-medium text-white group-hover:text-green-400 transition-colors">
                Derivatives
              </div>
            </div>
          </Link>

          <Link href="/analytics" className="group">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-orange-500 transition-all text-center">
              <PieChart className="h-6 w-6 text-orange-400 mx-auto mb-2" />
              <div className="text-sm font-medium text-white group-hover:text-orange-400 transition-colors">
                Analytics
              </div>
            </div>
          </Link>

          <Link href="/portfolio" className="group">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-indigo-500 transition-all text-center">
              <Building2 className="h-6 w-6 text-indigo-400 mx-auto mb-2" />
              <div className="text-sm font-medium text-white group-hover:text-indigo-400 transition-colors">
                Portfolio
              </div>
            </div>
          </Link>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Market Overview */}
          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-white">Market Overview</h2>
              <Eye className="h-5 w-5 text-slate-400" />
            </div>
            
            <div className="space-y-4">
              {marketData.map((market, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-slate-800 rounded-lg">
                  <div>
                    <div className="font-medium text-white">{market.symbol}</div>
                    <div className="text-sm text-slate-400">Vol: {market.volume}</div>
                  </div>
                  <div className="text-right">
                    <div className="font-mono text-white">{market.price.toLocaleString()}</div>
                    <div className={`text-sm flex items-center ${
                      market.change >= 0 ? 'text-green-400' : 'text-red-400'
                    }`}>
                      {market.change >= 0 ? (
                        <ArrowUpRight className="h-3 w-3 mr-1" />
                      ) : (
                        <ArrowDownRight className="h-3 w-3 mr-1" />
                      )}
                      {market.change >= 0 ? '+' : ''}{market.change.toFixed(1)} ({market.changePercent.toFixed(2)}%)
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Active Positions */}
          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-white">Active Positions</h2>
              <Link href="/portfolio" className="text-blue-400 hover:text-blue-300 text-sm">
                View All
              </Link>
            </div>
            
            <div className="space-y-4">
              {activePositions.slice(0, 4).map((position, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-slate-800 rounded-lg">
                  <div>
                    <div className="font-medium text-white">{position.symbol}</div>
                    <div className="text-sm text-slate-400 capitalize">
                      {position.type} • Qty: {position.quantity}
                      {position.expiry && ` • ${position.expiry}`}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className={`font-mono ${
                      position.pnl >= 0 ? 'text-green-400' : 'text-red-400'
                    }`}>
                      {position.pnl >= 0 ? '+' : ''}{formatNumber(position.pnl)}
                    </div>
                    <div className={`text-sm ${
                      position.pnl >= 0 ? 'text-green-400' : 'text-red-400'
                    }`}>
                      {position.pnlPercent >= 0 ? '+' : ''}{position.pnlPercent.toFixed(2)}%
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recent Trades */}
          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-white">Recent Trades</h2>
              <Clock className="h-5 w-5 text-slate-400" />
            </div>
            
            <div className="space-y-4">
              {recentTrades.map((trade) => (
                <div key={trade.id} className="flex items-center justify-between p-3 bg-slate-800 rounded-lg">
                  <div>
                    <div className="flex items-center space-x-2 mb-1">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        trade.type === 'BUY' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                      }`}>
                        {trade.type}
                      </span>
                      <span className="font-medium text-white">{trade.symbol}</span>
                    </div>
                    <div className="text-sm text-slate-400">
                      {trade.quantity} @ ₹{trade.price} • {trade.timestamp}
                    </div>
                  </div>
                  {trade.pnl && (
                    <div className={`text-right font-mono ${
                      trade.pnl >= 0 ? 'text-green-400' : 'text-red-400'
                    }`}>
                      {trade.pnl >= 0 ? '+' : ''}₹{trade.pnl}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Strategy Performance */}
          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-white">Strategy Performance</h2>
              <Link href="/stocks/backtest/multi-strategy" className="text-blue-400 hover:text-blue-300 text-sm">
                Optimize
              </Link>
            </div>
            
            <div className="space-y-4">
              {strategyPerformance.map((strategy, index) => (
                <div key={index} className="p-4 bg-slate-800 rounded-lg">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-2">
                      {index === 0 && <Crown className="h-4 w-4 text-yellow-400" />}
                      <h3 className="font-medium text-white">{strategy.name}</h3>
                    </div>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(strategy.status)}`}>
                      {strategy.status}
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <div className="text-slate-400">Win Rate</div>
                      <div className="text-white font-medium">{strategy.winRate.toFixed(1)}%</div>
                    </div>
                    <div>
                      <div className="text-slate-400">Monthly Return</div>
                      <div className="text-green-400 font-medium">+{strategy.monthlyReturn.toFixed(1)}%</div>
                    </div>
                    <div>
                      <div className="text-slate-400">Total P&L</div>
                      <div className="text-green-400 font-medium">+{formatNumber(strategy.totalPnL)}</div>
                    </div>
                    <div>
                      <div className="text-slate-400">Trades</div>
                      <div className="text-white font-medium">{strategy.totalTrades}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}