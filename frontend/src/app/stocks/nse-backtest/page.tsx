'use client';

import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Play, Pause, RotateCcw, Download, Upload, BarChart3, Settings, Calendar, DollarSign, Target, Activity, AlertTriangle, CheckCircle, Brain, Clock, Users, LineChart, PieChart } from 'lucide-react';
import Link from 'next/link';

interface BacktestTrade {
  id: number;
  symbol: string;
  entry: {
    price: number;
    time: string;
    reason: string;
  };
  exit: {
    price: number;
    time: string;
    reason: string;
  };
  pnl: number;
  pnlPercent: number;
  duration: string;
  quantity: number;
  side: 'LONG' | 'SHORT';
}

interface PerformanceMetrics {
  totalTrades: number;
  winningTrades: number;
  losingTrades: number;
  winRate: number;
  totalPnL: number;
  totalFees: number;
  netPnL: number;
  avgWin: number;
  avgLoss: number;
  maxWin: number;
  maxLoss: number;
  profitFactor: number;
  sharpeRatio: number;
  calmarRatio: number;
  maxDrawdown: number;
  maxDrawdownPercent: number;
  recoveryFactor: number;
  expectancy: number;
  monthlyReturns: Array<{ month: string; return: number; trades: number }>;
  dailyReturns: number[];
  equityCurve: Array<{ date: string; equity: number; drawdown: number }>;
}

interface BacktestResults {
  metrics: PerformanceMetrics;
  trades: BacktestTrade[];
  chartData: {
    price: Array<{ time: string; open: number; high: number; low: number; close: number; volume: number }>;
    signals: Array<{ time: string; type: 'BUY' | 'SELL'; price: number; symbol: string }>;
  };
}

export default function NSEBacktestPage() {
  const [results, setResults] = useState<BacktestResults | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [selectedTab, setSelectedTab] = useState<'overview' | 'trades' | 'charts' | 'analytics'>('overview');

  // Mock data generation
  const generateMockResults = (): BacktestResults => {
    const trades: BacktestTrade[] = [];
    const symbols = ['RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK', 'BHARTIARTL', 'SBIN', 'LT'];
    
    for (let i = 0; i < 150; i++) {
      const symbol = symbols[Math.floor(Math.random() * symbols.length)];
      const entryPrice = 1000 + Math.random() * 3000;
      const priceChange = (Math.random() - 0.5) * 0.2; // -10% to +10%
      const exitPrice = entryPrice * (1 + priceChange);
      const quantity = Math.floor(Math.random() * 100) + 10;
      const side: 'LONG' | 'SHORT' = Math.random() > 0.7 ? 'SHORT' : 'LONG';
      const pnl = side === 'LONG' ? 
        (exitPrice - entryPrice) * quantity : 
        (entryPrice - exitPrice) * quantity;
      
      trades.push({
        id: i + 1,
        symbol,
        entry: {
          price: entryPrice,
          time: new Date(2024, 0, 1 + Math.floor(i * 2.5)).toISOString(),
          reason: 'Strategy signal'
        },
        exit: {
          price: exitPrice,
          time: new Date(2024, 0, 1 + Math.floor(i * 2.5) + Math.floor(Math.random() * 5) + 1).toISOString(),
          reason: priceChange > 0 ? 'Take profit' : 'Stop loss'
        },
        pnl,
        pnlPercent: priceChange * 100,
        duration: `${Math.floor(Math.random() * 48) + 1}h`,
        quantity,
        side
      });
    }

    const totalPnL = trades.reduce((sum, t) => sum + t.pnl, 0);
    const winningTrades = trades.filter(t => t.pnl > 0);
    const losingTrades = trades.filter(t => t.pnl <= 0);
    const totalFees = trades.length * 50; // Mock fees

    const monthlyReturns = [
      { month: 'Jan', return: 8.5, trades: 15 },
      { month: 'Feb', return: -2.3, trades: 12 },
      { month: 'Mar', return: 12.1, trades: 18 },
      { month: 'Apr', return: 5.7, trades: 14 },
      { month: 'May', return: -1.2, trades: 16 },
      { month: 'Jun', return: 9.8, trades: 17 },
      { month: 'Jul', return: 3.4, trades: 13 },
      { month: 'Aug', return: -4.1, trades: 11 },
      { month: 'Sep', return: 11.2, trades: 19 },
      { month: 'Oct', return: 6.8, trades: 15 }
    ];

    const equityCurve = [];
    let runningEquity = 1000000; // Starting capital
    let maxEquity = runningEquity;
    
    for (let i = 0; i < 250; i++) {
      const dailyReturn = (Math.random() - 0.48) * 0.02; // Slight positive bias
      runningEquity *= (1 + dailyReturn);
      maxEquity = Math.max(maxEquity, runningEquity);
      const drawdown = (maxEquity - runningEquity) / maxEquity * 100;
      
      equityCurve.push({
        date: new Date(2024, 0, 1 + i).toISOString().split('T')[0],
        equity: runningEquity,
        drawdown
      });
    }

    return {
      metrics: {
        totalTrades: trades.length,
        winningTrades: winningTrades.length,
        losingTrades: losingTrades.length,
        winRate: (winningTrades.length / trades.length) * 100,
        totalPnL,
        totalFees,
        netPnL: totalPnL - totalFees,
        avgWin: winningTrades.length > 0 ? winningTrades.reduce((sum, t) => sum + t.pnl, 0) / winningTrades.length : 0,
        avgLoss: losingTrades.length > 0 ? losingTrades.reduce((sum, t) => sum + t.pnl, 0) / losingTrades.length : 0,
        maxWin: Math.max(...trades.map(t => t.pnl)),
        maxLoss: Math.min(...trades.map(t => t.pnl)),
        profitFactor: Math.abs(losingTrades.reduce((sum, t) => sum + t.pnl, 0)) > 0 ? 
          winningTrades.reduce((sum, t) => sum + t.pnl, 0) / Math.abs(losingTrades.reduce((sum, t) => sum + t.pnl, 0)) : 0,
        sharpeRatio: 2.34,
        calmarRatio: 1.87,
        maxDrawdown: 89500,
        maxDrawdownPercent: 8.95,
        recoveryFactor: 2.1,
        expectancy: totalPnL / trades.length,
        monthlyReturns,
        dailyReturns: Array.from({ length: 250 }, () => (Math.random() - 0.48) * 0.02),
        equityCurve
      },
      trades,
      chartData: {
        price: [],
        signals: []
      }
    };
  };

  const runBacktest = async () => {
    setIsRunning(true);
    setProgress(0);

    // Simulate backtest progress
    for (let i = 0; i <= 100; i += 10) {
      setProgress(i);
      await new Promise(resolve => setTimeout(resolve, 200));
    }

    setResults(generateMockResults());
    setIsRunning(false);
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  };

  const formatNumber = (value: number, decimals: number = 2) => {
    return value.toLocaleString('en-IN', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    });
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Navigation */}
        <div className="mb-6">
          <nav className="flex items-center space-x-2 text-sm text-slate-400">
            <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
            <span>/</span>
            <Link href="/stocks" className="hover:text-blue-400 transition-colors">Stocks</Link>
            <span>/</span>
            <Link href="/stocks/nse-trading" className="hover:text-blue-400 transition-colors">NSE Trading</Link>
            <span>/</span>
            <span className="text-white">Backtest Results</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-4">
            NSE Backtest Analysis
          </h1>
          <p className="text-xl text-slate-300">
            Comprehensive performance analysis and visualization
          </p>
        </div>

        {/* Run Backtest Button */}
        {!results && (
          <div className="bg-slate-900 rounded-xl p-8 border border-slate-800 text-center mb-8">
            <h3 className="text-2xl font-semibold mb-4">Ready to Run Backtest</h3>
            <p className="text-slate-400 mb-6">
              Run a comprehensive backtest on selected NSE assets with your chosen strategy
            </p>
            <button
              onClick={runBacktest}
              disabled={isRunning}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white px-8 py-3 rounded-lg font-semibold transition-colors flex items-center mx-auto"
            >
              {isRunning ? (
                <>
                  <Activity className="h-5 w-5 mr-2 animate-spin" />
                  Running Backtest... {progress}%
                </>
              ) : (
                <>
                  <Play className="h-5 w-5 mr-2" />
                  Run Backtest
                </>
              )}
            </button>
            {isRunning && (
              <div className="mt-4 bg-slate-800 rounded-full h-2 w-64 mx-auto">
                <div 
                  className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
            )}
          </div>
        )}

        {/* Results */}
        {results && (
          <>
            {/* Tab Navigation */}
            <div className="bg-slate-900 rounded-xl p-1 mb-6 border border-slate-800">
              <div className="flex space-x-1">
                {[
                  { key: 'overview', label: 'Overview', icon: BarChart3 },
                  { key: 'trades', label: 'Trade Details', icon: Activity },
                  { key: 'charts', label: 'Charts', icon: LineChart },
                  { key: 'analytics', label: 'Analytics', icon: Brain }
                ].map(tab => (
                  <button
                    key={tab.key}
                    onClick={() => setSelectedTab(tab.key as any)}
                    className={`flex items-center px-4 py-2 rounded-lg font-medium transition-colors ${
                      selectedTab === tab.key 
                        ? 'bg-blue-600 text-white' 
                        : 'text-slate-400 hover:text-white hover:bg-slate-800'
                    }`}
                  >
                    <tab.icon className="h-4 w-4 mr-2" />
                    {tab.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Overview Tab */}
            {selectedTab === 'overview' && (
              <div className="space-y-6">
                {/* Key Metrics */}
                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                  <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <DollarSign className={`h-5 w-5 ${results.metrics.netPnL >= 0 ? 'text-green-400' : 'text-red-400'}`} />
                    </div>
                    <div className="text-sm text-slate-400">Net P&L</div>
                    <div className={`text-xl font-bold ${results.metrics.netPnL >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                      {formatCurrency(results.metrics.netPnL)}
                    </div>
                  </div>

                  <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <Target className="h-5 w-5 text-blue-400" />
                    </div>
                    <div className="text-sm text-slate-400">Win Rate</div>
                    <div className="text-xl font-bold text-blue-400">
                      {formatNumber(results.metrics.winRate, 1)}%
                    </div>
                  </div>

                  <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <TrendingUp className="h-5 w-5 text-purple-400" />
                    </div>
                    <div className="text-sm text-slate-400">Sharpe Ratio</div>
                    <div className="text-xl font-bold text-purple-400">
                      {formatNumber(results.metrics.sharpeRatio)}
                    </div>
                  </div>

                  <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <TrendingDown className="h-5 w-5 text-red-400" />
                    </div>
                    <div className="text-sm text-slate-400">Max Drawdown</div>
                    <div className="text-xl font-bold text-red-400">
                      -{formatNumber(results.metrics.maxDrawdownPercent, 1)}%
                    </div>
                  </div>

                  <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <Activity className="h-5 w-5 text-orange-400" />
                    </div>
                    <div className="text-sm text-slate-400">Total Trades</div>
                    <div className="text-xl font-bold text-orange-400">
                      {results.metrics.totalTrades}
                    </div>
                  </div>

                  <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <BarChart3 className="h-5 w-5 text-cyan-400" />
                    </div>
                    <div className="text-sm text-slate-400">Profit Factor</div>
                    <div className="text-xl font-bold text-cyan-400">
                      {formatNumber(results.metrics.profitFactor)}
                    </div>
                  </div>
                </div>

                {/* Monthly Performance */}
                <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                  <h3 className="text-lg font-semibold mb-4 flex items-center">
                    <Calendar className="h-5 w-5 mr-2 text-blue-400" />
                    Monthly Performance
                  </h3>
                  <div className="grid grid-cols-5 md:grid-cols-10 gap-3">
                    {results.metrics.monthlyReturns.map((month, index) => (
                      <div
                        key={index}
                        className={`p-3 rounded-lg text-center border ${
                          month.return >= 0 
                            ? 'bg-green-500/20 border-green-500/30 text-green-400' 
                            : 'bg-red-500/20 border-red-500/30 text-red-400'
                        }`}
                      >
                        <div className="text-sm font-semibold">{month.month}</div>
                        <div className="text-lg font-bold">
                          {month.return > 0 ? '+' : ''}{formatNumber(month.return, 1)}%
                        </div>
                        <div className="text-xs opacity-75">{month.trades} trades</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Additional Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                    <h4 className="text-sm font-semibold text-slate-400 mb-3">Win/Loss Analysis</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-green-400">Winning Trades:</span>
                        <span className="font-semibold">{results.metrics.winningTrades}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-red-400">Losing Trades:</span>
                        <span className="font-semibold">{results.metrics.losingTrades}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Avg Win:</span>
                        <span className="font-semibold text-green-400">{formatCurrency(results.metrics.avgWin)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Avg Loss:</span>
                        <span className="font-semibold text-red-400">{formatCurrency(results.metrics.avgLoss)}</span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                    <h4 className="text-sm font-semibold text-slate-400 mb-3">Risk Metrics</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-slate-400">Max Win:</span>
                        <span className="font-semibold text-green-400">{formatCurrency(results.metrics.maxWin)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Max Loss:</span>
                        <span className="font-semibold text-red-400">{formatCurrency(results.metrics.maxLoss)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Calmar Ratio:</span>
                        <span className="font-semibold">{formatNumber(results.metrics.calmarRatio)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Recovery Factor:</span>
                        <span className="font-semibold">{formatNumber(results.metrics.recoveryFactor)}</span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                    <h4 className="text-sm font-semibold text-slate-400 mb-3">Financial Summary</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-slate-400">Gross P&L:</span>
                        <span className={`font-semibold ${results.metrics.totalPnL >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                          {formatCurrency(results.metrics.totalPnL)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Total Fees:</span>
                        <span className="font-semibold text-red-400">-{formatCurrency(results.metrics.totalFees)}</span>
                      </div>
                      <div className="flex justify-between border-t border-slate-700 pt-2">
                        <span className="text-white font-semibold">Net P&L:</span>
                        <span className={`font-bold ${results.metrics.netPnL >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                          {formatCurrency(results.metrics.netPnL)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Expectancy:</span>
                        <span className="font-semibold">{formatCurrency(results.metrics.expectancy)}</span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                    <h4 className="text-sm font-semibold text-slate-400 mb-3">Performance Grade</h4>
                    <div className="text-center">
                      <div className="text-4xl font-bold text-blue-400 mb-2">A-</div>
                      <div className="text-sm text-slate-400 mb-2">Excellent Performance</div>
                      <div className="text-xs text-slate-500">
                        High Sharpe ratio with controlled drawdown
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Trades Tab */}
            {selectedTab === 'trades' && (
              <div className="bg-slate-900 rounded-xl border border-slate-800">
                <div className="p-6 border-b border-slate-800">
                  <h3 className="text-lg font-semibold flex items-center">
                    <Activity className="h-5 w-5 mr-2 text-blue-400" />
                    Trade History ({results.trades.length} trades)
                  </h3>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-slate-800">
                      <tr>
                        <th className="px-4 py-3 text-left text-sm font-medium text-slate-300">Trade #</th>
                        <th className="px-4 py-3 text-left text-sm font-medium text-slate-300">Symbol</th>
                        <th className="px-4 py-3 text-left text-sm font-medium text-slate-300">Side</th>
                        <th className="px-4 py-3 text-left text-sm font-medium text-slate-300">Entry</th>
                        <th className="px-4 py-3 text-left text-sm font-medium text-slate-300">Exit</th>
                        <th className="px-4 py-3 text-left text-sm font-medium text-slate-300">Quantity</th>
                        <th className="px-4 py-3 text-left text-sm font-medium text-slate-300">Duration</th>
                        <th className="px-4 py-3 text-left text-sm font-medium text-slate-300">P&L</th>
                        <th className="px-4 py-3 text-left text-sm font-medium text-slate-300">Return %</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                      {results.trades.slice(0, 50).map((trade) => (
                        <tr key={trade.id} className="hover:bg-slate-800/50">
                          <td className="px-4 py-3 text-sm text-slate-300">#{trade.id}</td>
                          <td className="px-4 py-3 text-sm font-semibold text-white">{trade.symbol}</td>
                          <td className="px-4 py-3 text-sm">
                            <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                              trade.side === 'LONG' ? 'bg-green-500/20 text-green-400' : 'bg-orange-500/20 text-orange-400'
                            }`}>
                              {trade.side}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-sm text-slate-300">₹{formatNumber(trade.entry.price)}</td>
                          <td className="px-4 py-3 text-sm text-slate-300">₹{formatNumber(trade.exit.price)}</td>
                          <td className="px-4 py-3 text-sm text-slate-300">{trade.quantity}</td>
                          <td className="px-4 py-3 text-sm text-slate-300">{trade.duration}</td>
                          <td className={`px-4 py-3 text-sm font-semibold ${
                            trade.pnl >= 0 ? 'text-green-400' : 'text-red-400'
                          }`}>
                            {formatCurrency(trade.pnl)}
                          </td>
                          <td className={`px-4 py-3 text-sm font-semibold ${
                            trade.pnlPercent >= 0 ? 'text-green-400' : 'text-red-400'
                          }`}>
                            {trade.pnlPercent > 0 ? '+' : ''}{formatNumber(trade.pnlPercent, 2)}%
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                {results.trades.length > 50 && (
                  <div className="p-4 text-center border-t border-slate-800">
                    <span className="text-sm text-slate-400">
                      Showing first 50 trades of {results.trades.length} total
                    </span>
                  </div>
                )}
              </div>
            )}

            {/* Charts Tab */}
            {selectedTab === 'charts' && (
              <div className="space-y-6">
                <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                  <h3 className="text-lg font-semibold mb-4 flex items-center">
                    <LineChart className="h-5 w-5 mr-2 text-blue-400" />
                    Equity Curve
                  </h3>
                  <div className="h-96 bg-slate-800 rounded-lg flex items-center justify-center">
                    <div className="text-center text-slate-400">
                      <BarChart3 className="h-12 w-12 mx-auto mb-2 opacity-50" />
                      <p>Interactive equity curve chart would be rendered here</p>
                      <p className="text-sm mt-1">Using Recharts or similar charting library</p>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                    <h3 className="text-lg font-semibold mb-4 flex items-center">
                      <PieChart className="h-5 w-5 mr-2 text-green-400" />
                      Win/Loss Distribution
                    </h3>
                    <div className="h-64 bg-slate-800 rounded-lg flex items-center justify-center">
                      <div className="text-center text-slate-400">
                        <PieChart className="h-12 w-12 mx-auto mb-2 opacity-50" />
                        <p>Pie chart for win/loss distribution</p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                    <h3 className="text-lg font-semibold mb-4 flex items-center">
                      <BarChart3 className="h-5 w-5 mr-2 text-purple-400" />
                      Monthly Returns
                    </h3>
                    <div className="h-64 bg-slate-800 rounded-lg flex items-center justify-center">
                      <div className="text-center text-slate-400">
                        <BarChart3 className="h-12 w-12 mx-auto mb-2 opacity-50" />
                        <p>Bar chart for monthly returns</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Analytics Tab */}
            {selectedTab === 'analytics' && (
              <div className="space-y-6">
                <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                  <h3 className="text-lg font-semibold mb-4 flex items-center">
                    <Brain className="h-5 w-5 mr-2 text-purple-400" />
                    AI Performance Analysis
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                      <div className="bg-slate-800 rounded-lg p-4">
                        <h4 className="font-semibold text-green-400 mb-2">Strengths</h4>
                        <ul className="text-sm text-slate-300 space-y-1">
                          <li>• Consistent positive monthly returns</li>
                          <li>• Strong risk-adjusted returns (Sharpe > 2.0)</li>
                          <li>• Controlled maximum drawdown (&lt; 10%)</li>
                          <li>• Good profit factor (2.14)</li>
                        </ul>
                      </div>
                      <div className="bg-slate-800 rounded-lg p-4">
                        <h4 className="font-semibold text-yellow-400 mb-2">Areas for Improvement</h4>
                        <ul className="text-sm text-slate-300 space-y-1">
                          <li>• Consider position sizing optimization</li>
                          <li>• Review stop-loss levels for losing trades</li>
                          <li>• Analyze sector concentration risk</li>
                        </ul>
                      </div>
                    </div>
                    <div className="space-y-4">
                      <div className="bg-slate-800 rounded-lg p-4">
                        <h4 className="font-semibold text-blue-400 mb-2">Recommendations</h4>
                        <ul className="text-sm text-slate-300 space-y-1">
                          <li>• Maintain current strategy parameters</li>
                          <li>• Consider increasing position sizes</li>
                          <li>• Add more defensive stocks during volatile periods</li>
                          <li>• Implement dynamic stop-loss based on volatility</li>
                        </ul>
                      </div>
                      <div className="bg-slate-800 rounded-lg p-4">
                        <h4 className="font-semibold text-purple-400 mb-2">Risk Assessment</h4>
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-slate-400">Overall Risk Level:</span>
                          <span className="text-yellow-400 font-semibold">MEDIUM</span>
                        </div>
                        <div className="mt-2 text-xs text-slate-400">
                          Strategy shows good risk control with acceptable drawdown levels.
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}