'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { 
  TrendingUp, BarChart3, DollarSign, Activity, Target, 
  Clock, Play, Pause, RefreshCw, Bell, Settings, Eye,
  ArrowUp, ArrowDown, Info, AlertCircle
} from 'lucide-react';
import { useMarketData, useIndices, usePositions } from '../../hooks/useMarketData';
import { formatIndianCurrency, formatIndianNumber, getChangeColor } from '../../services/fyersApi';

export default function TradingPage() {
  const [isLive, setIsLive] = useState(false);
  
  // Use market data hooks
  const { 
    marketData, 
    isLoading: marketLoading, 
    error: marketError, 
    lastUpdate,
    refresh: refreshMarket,
    isConnected
  } = useMarketData({
    autoRefresh: true,
    refreshInterval: 5000
  });

  const { 
    indices,
    marketStatus,
    dataSource,
    isLoading: indicesLoading,
    error: indicesError
  } = useIndices();

  const {
    positions,
    totalPnL,
    profitablePositions,
    losingPositions,
    isLoading: positionsLoading,
    error: positionsError,
    refresh: refreshPositions
  } = usePositions();

  // Handle refresh
  const handleRefresh = async () => {
    await refreshMarket();
    await refreshPositions();
  };

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
              <div className={`w-2 h-2 rounded-full ${marketStatus?.is_open ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`}></div>
              <span className="text-slate-300">
                {marketStatus?.is_open ? 'Market Open' : 'Market Closed'}
              </span>
            </div>
            <div className="flex items-center space-x-2 text-slate-400">
              <Clock className="h-4 w-4" />
              <span>
                Last Update: {lastUpdate ? lastUpdate.toLocaleTimeString() : 'N/A'}
              </span>
            </div>
            {dataSource && (
              <span className="text-xs px-2 py-1 bg-slate-800 rounded text-slate-400">
                {dataSource === 'live' ? '🔴 Live Data' : '📊 Cached Data'}
              </span>
            )}
            <button 
              onClick={handleRefresh}
              disabled={marketLoading}
              className="flex items-center space-x-2 text-blue-400 hover:text-blue-300 disabled:opacity-50"
            >
              <RefreshCw className={`h-4 w-4 ${marketLoading ? 'animate-spin' : ''}`} />
              <span>Refresh</span>
            </button>
            {!isConnected && (
              <span className="text-xs px-2 py-1 bg-red-500/10 text-red-400 rounded">
                ⚠️ Disconnected
              </span>
            )}
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-slate-400">Total P&L</span>
              <DollarSign className={`h-5 w-5 ${totalPnL >= 0 ? 'text-green-400' : 'text-red-400'}`} />
            </div>
            <div className={`text-2xl font-bold ${totalPnL >= 0 ? 'text-green-400' : 'text-red-400'}`}>
              {formatIndianCurrency(totalPnL)}
            </div>
            <div className="text-sm text-slate-400 mt-1">
              {positions.length > 0 ? `From ${positions.length} positions` : 'No active positions'}
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-slate-400">Active Positions</span>
              <Activity className="h-5 w-5 text-blue-400" />
            </div>
            <div className="text-2xl font-bold text-white">{positions.length}</div>
            <div className="text-sm text-slate-400 mt-1">
              {profitablePositions} profitable, {losingPositions} losing
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-slate-400">Market Status</span>
              <Target className="h-5 w-5 text-purple-400" />
            </div>
            <div className="text-2xl font-bold text-white">
              {marketStatus?.is_open ? 'OPEN' : 'CLOSED'}
            </div>
            <div className="text-sm text-slate-400 mt-1">
              {marketStatus?.message || 'Checking...'}
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-slate-400">NIFTY 50</span>
              <BarChart3 className="h-5 w-5 text-yellow-400" />
            </div>
            <div className="text-2xl font-bold text-white">
              {indices[0] ? formatIndianNumber(indices[0].price) : 'Loading...'}
            </div>
            <div className={`text-sm mt-1 ${indices[0] ? getChangeColor(indices[0].change) : 'text-slate-400'}`}>
              {indices[0] ? `${indices[0].change >= 0 ? '+' : ''}${indices[0].change.toFixed(2)} (${indices[0].change_percent.toFixed(2)}%)` : 'N/A'}
            </div>
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
                {indicesLoading ? (
                  <tr>
                    <td colSpan={6} className="py-8 text-center text-slate-400">
                      <div className="flex items-center justify-center space-x-2">
                        <RefreshCw className="h-5 w-5 animate-spin" />
                        <span>Loading market data...</span>
                      </div>
                    </td>
                  </tr>
                ) : indicesError ? (
                  <tr>
                    <td colSpan={6} className="py-8 text-center text-red-400">
                      <div className="flex flex-col items-center space-y-2">
                        <AlertCircle className="h-8 w-8" />
                        <span>Failed to load market data</span>
                        <button 
                          onClick={handleRefresh}
                          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors text-sm"
                        >
                          Retry
                        </button>
                      </div>
                    </td>
                  </tr>
                ) : indices.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="py-8 text-center text-slate-400">
                      No market data available
                    </td>
                  </tr>
                ) : (
                  indices.map((item, idx) => (
                    <tr key={idx} className="border-b border-slate-800 hover:bg-slate-800/50 transition-colors">
                      <td className="py-4 px-4">
                        <div className="font-medium text-white">{item.symbol}</div>
                      </td>
                      <td className="py-4 px-4 text-right text-white font-mono">
                        {formatIndianCurrency(item.price)}
                      </td>
                      <td className={`py-4 px-4 text-right font-mono ${getChangeColor(item.change)}`}>
                        {item.change >= 0 ? '+' : ''}{formatIndianNumber(item.change)}
                      </td>
                      <td className="py-4 px-4 text-right">
                        <div className={`flex items-center justify-end space-x-1 ${getChangeColor(item.change_percent)}`}>
                          {item.change_percent >= 0 ? <ArrowUp className="h-4 w-4" /> : <ArrowDown className="h-4 w-4" />}
                          <span className="font-mono">{Math.abs(item.change_percent).toFixed(2)}%</span>
                        </div>
                      </td>
                      <td className="py-4 px-4 text-right text-slate-300 font-mono">
                        N/A
                      </td>
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
                  ))
                )}
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

          {positionsLoading ? (
            <div className="text-center py-12">
              <div className="flex items-center justify-center space-x-2 text-slate-400">
                <RefreshCw className="h-6 w-6 animate-spin" />
                <span>Loading positions...</span>
              </div>
            </div>
          ) : positionsError ? (
            <div className="text-center py-12">
              <AlertCircle className="h-12 w-12 text-red-400 mx-auto mb-4" />
              <p className="text-red-400 mb-4">Failed to load positions</p>
              <button 
                onClick={handleRefresh}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors text-sm"
              >
                Retry
              </button>
            </div>
          ) : positions.length > 0 ? (
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
                  {positions.map((position, index) => {
                    const pnlPercent = ((position.current_price - position.buy_price) / position.buy_price) * 100;
                    return (
                      <tr key={index} className="border-b border-slate-800 hover:bg-slate-800/50 transition-colors">
                        <td className="py-4 px-4">
                          <div className="font-medium text-white">{position.symbol}</div>
                        </td>
                        <td className="py-4 px-4 text-right text-slate-300 font-mono">{position.quantity}</td>
                        <td className="py-4 px-4 text-right text-slate-300 font-mono">
                          {formatIndianCurrency(position.buy_price)}
                        </td>
                        <td className="py-4 px-4 text-right text-white font-mono">
                          {formatIndianCurrency(position.current_price)}
                        </td>
                        <td className={`py-4 px-4 text-right font-mono font-bold ${getChangeColor(position.pnl)}`}>
                          <div>
                            {position.pnl >= 0 ? '+' : ''}{formatIndianCurrency(position.pnl)}
                          </div>
                          <div className="text-xs">
                            ({pnlPercent >= 0 ? '+' : ''}{pnlPercent.toFixed(2)}%)
                          </div>
                        </td>
                        <td className="py-4 px-4">
                          <div className="flex items-center justify-center space-x-2">
                            <button className="px-3 py-1 bg-slate-700 hover:bg-slate-600 text-white text-sm rounded transition-colors">
                              Exit
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
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
