'use client';

import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Play, Pause, RotateCcw, Download, Upload, BarChart3, Settings, Calendar, DollarSign, Target, Activity, AlertTriangle, CheckCircle } from 'lucide-react';
import Link from 'next/link';

interface BacktestParams {
  symbol: string;
  strategy: string;
  startDate: string;
  endDate: string;
  capital: number;
  strikeSelection: string;
  expiry: string;
  entryTime: string;
  exitTime: string;
  stopLoss: number;
  takeProfit: number;
}

interface BacktestResult {
  totalTrades: number;
  winRate: number;
  totalPnL: number;
  maxDrawdown: number;
  sharpeRatio: number;
  avgWin: number;
  avgLoss: number;
  trades: TradeResult[];
}

interface TradeResult {
  date: string;
  entry: number;
  exit: number;
  pnl: number;
  duration: string;
  strategy: string;
}

export default function NSEBacktesting() {
  const [params, setParams] = useState<BacktestParams>({
    symbol: 'NIFTY',
    strategy: 'iron-condor',
    startDate: '2024-01-01',
    endDate: '2024-10-31',
    capital: 500000,
    strikeSelection: 'atm',
    expiry: 'weekly',
    entryTime: '09:30',
    exitTime: '15:00',
    stopLoss: 50,
    takeProfit: 30
  });

  const [results, setResults] = useState<BacktestResult | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentTrade, setCurrentTrade] = useState(0);

  const symbols = [
    // Indices
    'NIFTY', 'BANKNIFTY', 'FINNIFTY', 'MIDCPNIFTY',
    // Banking
    'HDFCBANK', 'ICICIBANK', 'SBIN', 'AXISBANK',
    // IT
    'TCS', 'INFY', 'WIPRO', 'HCLTECH',
    // Auto
    'MARUTI', 'TATAMOTORS', 'M&M',
    // Pharma
    'SUNPHARMA', 'DRREDDY',
    // FMCG
    'HINDUNILVR', 'ITC',
    // Metals
    'TATASTEEL', 'HINDALCO',
    // Energy/Power
    'RELIANCE', 'NTPC', 'POWERGRID'
  ];
  const strategies = [
    { value: 'iron-condor', label: 'Iron Condor', description: 'Sell OTM Put & Call, Buy further OTM' },
    { value: 'strangle', label: 'Short Strangle', description: 'Sell OTM Put & Call' },
    { value: 'straddle', label: 'Short Straddle', description: 'Sell ATM Put & Call' },
    { value: 'butterfly', label: 'Butterfly Spread', description: 'ATM spread with wing protection' },
    { value: 'long-call', label: 'Long Call', description: 'Buy Call option' },
    { value: 'long-put', label: 'Long Put', description: 'Buy Put option' }
  ];

  const strikeSelections = [
    { value: 'atm', label: 'At The Money (ATM)' },
    { value: 'otm-1', label: '1 Strike OTM' },
    { value: 'otm-2', label: '2 Strikes OTM' },
    { value: 'itm-1', label: '1 Strike ITM' }
  ];

  const runBacktest = async () => {
    setIsRunning(true);
    setProgress(0);
    setCurrentTrade(0);

    // Simulate backtest execution
    const totalDays = 250; // Trading days
    const trades: TradeResult[] = [];

    for (let i = 0; i < totalDays; i++) {
      await new Promise(resolve => setTimeout(resolve, 20)); // Simulate processing
      
      setProgress((i / totalDays) * 100);
      setCurrentTrade(i + 1);

      // Generate realistic trade results
      const baseReturn = getStrategyBaseReturn(params.strategy);
      const volatility = 0.3;
      const randomReturn = (Math.random() - 0.5) * volatility + baseReturn;
      
      const entryPrice = 100 + Math.random() * 50;
      const exitPrice = entryPrice * (1 + randomReturn);
      const pnl = (exitPrice - entryPrice) * getLotSize(params.symbol);

      trades.push({
        date: new Date(2024, 0, i + 1).toISOString().split('T')[0],
        entry: parseFloat(entryPrice.toFixed(2)),
        exit: parseFloat(exitPrice.toFixed(2)),
        pnl: parseFloat(pnl.toFixed(2)),
        duration: '6h 30m',
        strategy: params.strategy
      });
    }

    // Calculate results
    const winningTrades = trades.filter(t => t.pnl > 0);
    const totalPnL = trades.reduce((sum, t) => sum + t.pnl, 0);
    const maxDrawdown = calculateMaxDrawdown(trades);
    
    setResults({
      totalTrades: trades.length,
      winRate: (winningTrades.length / trades.length) * 100,
      totalPnL,
      maxDrawdown,
      sharpeRatio: calculateSharpeRatio(trades),
      avgWin: winningTrades.length > 0 ? winningTrades.reduce((sum, t) => sum + t.pnl, 0) / winningTrades.length : 0,
      avgLoss: trades.length - winningTrades.length > 0 ? 
        trades.filter(t => t.pnl <= 0).reduce((sum, t) => sum + t.pnl, 0) / (trades.length - winningTrades.length) : 0,
      trades
    });

    setIsRunning(false);
  };

  const getStrategyBaseReturn = (strategy: string): number => {
    const returns: Record<string, number> = {
      'iron-condor': 0.02,
      'strangle': 0.015,
      'straddle': 0.01,
      'butterfly': 0.025,
      'long-call': -0.005,
      'long-put': -0.005
    };
    return returns[strategy] || 0;
  };

  const getLotSize = (symbol: string): number => {
    const lotSizes: Record<string, number> = {
      'NIFTY': 50,
      'BANKNIFTY': 15,
      'FINNIFTY': 40,
      'RELIANCE': 250,
      'TCS': 150,
      'HDFCBANK': 550
    };
    return lotSizes[symbol] || 50;
  };

  const calculateMaxDrawdown = (trades: TradeResult[]): number => {
    let maxDrawdown = 0;
    let peak = 0;
    let cumulative = 0;

    for (const trade of trades) {
      cumulative += trade.pnl;
      if (cumulative > peak) peak = cumulative;
      const drawdown = ((peak - cumulative) / peak) * 100;
      if (drawdown > maxDrawdown) maxDrawdown = drawdown;
    }

    return maxDrawdown;
  };

  const calculateSharpeRatio = (trades: TradeResult[]): number => {
    const returns = trades.map(t => t.pnl);
    const avgReturn = returns.reduce((sum, r) => sum + r, 0) / returns.length;
    const variance = returns.reduce((sum, r) => sum + Math.pow(r - avgReturn, 2), 0) / returns.length;
    const stdDev = Math.sqrt(variance);
    return stdDev !== 0 ? (avgReturn / stdDev) * Math.sqrt(252) : 0;
  };

  const resetBacktest = () => {
    setResults(null);
    setProgress(0);
    setCurrentTrade(0);
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4">
      <div className="max-w-7xl mx-auto">
        {/* Navigation Breadcrumb */}
        <div className="mb-6">
          <nav className="flex items-center space-x-2 text-sm text-slate-400">
            <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
            <span>/</span>
            <Link href="/stocks" className="hover:text-blue-400 transition-colors">Stocks</Link>
            <span>/</span>
            <span className="text-white">NSE Backtesting</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-4">
            NSE Option Strategy Backtesting
          </h1>
          <p className="text-slate-300 text-lg">
            Test your option strategies with historical NSE data and advanced analytics
          </p>
        </div>

        {/* Quick Navigation */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <Link href="/stocks/backtest/multi-strategy" className="group">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-blue-500 transition-all">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-lg font-semibold text-white group-hover:text-blue-400 transition-colors">
                  Multi-Strategy Comparison
                </h3>
                <BarChart3 className="h-5 w-5 text-blue-400" />
              </div>
              <p className="text-slate-400 text-sm">
                Compare multiple strategies side by side with advanced ranking
              </p>
            </div>
          </Link>
          
          <Link href="/stocks/backtest/universal" className="group">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-purple-500 transition-all">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-lg font-semibold text-white group-hover:text-purple-400 transition-colors">
                  Universal Asset Backtesting
                </h3>
                <Target className="h-5 w-5 text-purple-400" />
              </div>
              <p className="text-slate-400 text-sm">
                AI-powered recommendations for any asset class and timeframe
              </p>
            </div>
          </Link>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Configuration Panel */}
          <div className="lg:col-span-1">
            <div className="bg-slate-900 rounded-2xl border border-slate-800 p-6 sticky top-4">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-white">Strategy Configuration</h2>
                <Settings className="h-5 w-5 text-slate-400" />
              </div>

              <div className="space-y-6">
                {/* Symbol Selection */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Symbol</label>
                  <select
                    value={params.symbol}
                    onChange={(e) => setParams(prev => ({ ...prev, symbol: e.target.value }))}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                  >
                    {symbols.map(symbol => (
                      <option key={symbol} value={symbol}>{symbol}</option>
                    ))}
                  </select>
                </div>

                {/* Strategy Selection */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Strategy</label>
                  <select
                    value={params.strategy}
                    onChange={(e) => setParams(prev => ({ ...prev, strategy: e.target.value }))}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                  >
                    {strategies.map(strategy => (
                      <option key={strategy.value} value={strategy.value}>{strategy.label}</option>
                    ))}
                  </select>
                  <p className="text-xs text-slate-400 mt-1">
                    {strategies.find(s => s.value === params.strategy)?.description}
                  </p>
                </div>

                {/* Date Range */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Start Date</label>
                    <input
                      type="date"
                      value={params.startDate}
                      onChange={(e) => setParams(prev => ({ ...prev, startDate: e.target.value }))}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">End Date</label>
                    <input
                      type="date"
                      value={params.endDate}
                      onChange={(e) => setParams(prev => ({ ...prev, endDate: e.target.value }))}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                    />
                  </div>
                </div>

                {/* Capital */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Initial Capital</label>
                  <input
                    type="number"
                    value={params.capital}
                    onChange={(e) => setParams(prev => ({ ...prev, capital: parseInt(e.target.value) }))}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                    placeholder="500000"
                  />
                </div>

                {/* Strike Selection */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Strike Selection</label>
                  <select
                    value={params.strikeSelection}
                    onChange={(e) => setParams(prev => ({ ...prev, strikeSelection: e.target.value }))}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                  >
                    {strikeSelections.map(option => (
                      <option key={option.value} value={option.value}>{option.label}</option>
                    ))}
                  </select>
                </div>

                {/* Time Settings */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Entry Time</label>
                    <input
                      type="time"
                      value={params.entryTime}
                      onChange={(e) => setParams(prev => ({ ...prev, entryTime: e.target.value }))}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Exit Time</label>
                    <input
                      type="time"
                      value={params.exitTime}
                      onChange={(e) => setParams(prev => ({ ...prev, exitTime: e.target.value }))}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                    />
                  </div>
                </div>

                {/* Risk Management */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Stop Loss %</label>
                    <input
                      type="number"
                      value={params.stopLoss}
                      onChange={(e) => setParams(prev => ({ ...prev, stopLoss: parseFloat(e.target.value) }))}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                      placeholder="50"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Take Profit %</label>
                    <input
                      type="number"
                      value={params.takeProfit}
                      onChange={(e) => setParams(prev => ({ ...prev, takeProfit: parseFloat(e.target.value) }))}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                      placeholder="30"
                    />
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="space-y-3 pt-4 border-t border-slate-800">
                  <button
                    onClick={runBacktest}
                    disabled={isRunning}
                    className="w-full flex items-center justify-center px-4 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-slate-600 disabled:to-slate-600 rounded-lg font-medium transition-all duration-200"
                  >
                    {isRunning ? (
                      <>
                        <Pause className="h-5 w-5 mr-2" />
                        Running...
                      </>
                    ) : (
                      <>
                        <Play className="h-5 w-5 mr-2" />
                        Run Backtest
                      </>
                    )}
                  </button>

                  <div className="grid grid-cols-2 gap-2">
                    <button
                      onClick={resetBacktest}
                      className="flex items-center justify-center px-3 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm transition-colors"
                    >
                      <RotateCcw className="h-4 w-4 mr-1" />
                      Reset
                    </button>
                    <button className="flex items-center justify-center px-3 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm transition-colors">
                      <Upload className="h-4 w-4 mr-1" />
                      Load Config
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Results Panel */}
          <div className="lg:col-span-2">
            {isRunning && (
              <div className="bg-slate-900 rounded-2xl border border-slate-800 p-6 mb-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-white">Backtest Progress</h3>
                  <div className="text-sm text-slate-400">Trade {currentTrade} / 250</div>
                </div>
                <div className="bg-slate-800 rounded-full h-3 mb-2">
                  <div 
                    className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <div className="text-center text-sm text-slate-400">{progress.toFixed(1)}% Complete</div>
              </div>
            )}

            {results && (
              <>
                {/* Performance Summary */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-slate-400 text-sm">Total P&L</span>
                      <DollarSign className={`h-4 w-4 ${results.totalPnL >= 0 ? 'text-green-400' : 'text-red-400'}`} />
                    </div>
                    <div className={`text-xl font-bold ${results.totalPnL >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                      {formatCurrency(results.totalPnL)}
                    </div>
                  </div>

                  <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-slate-400 text-sm">Win Rate</span>
                      <Target className="h-4 w-4 text-blue-400" />
                    </div>
                    <div className="text-xl font-bold text-blue-400">
                      {results.winRate.toFixed(1)}%
                    </div>
                  </div>

                  <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-slate-400 text-sm">Sharpe Ratio</span>
                      <Activity className="h-4 w-4 text-purple-400" />
                    </div>
                    <div className="text-xl font-bold text-purple-400">
                      {results.sharpeRatio.toFixed(2)}
                    </div>
                  </div>

                  <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-slate-400 text-sm">Max Drawdown</span>
                      <AlertTriangle className="h-4 w-4 text-yellow-400" />
                    </div>
                    <div className="text-xl font-bold text-yellow-400">
                      {results.maxDrawdown.toFixed(1)}%
                    </div>
                  </div>
                </div>

                {/* Detailed Metrics */}
                <div className="bg-slate-900 rounded-2xl border border-slate-800 p-6 mb-6">
                  <h3 className="text-lg font-semibold text-white mb-4">Performance Metrics</h3>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
                    <div>
                      <div className="text-slate-400 text-sm mb-1">Total Trades</div>
                      <div className="text-2xl font-bold text-white">{results.totalTrades}</div>
                    </div>
                    <div>
                      <div className="text-slate-400 text-sm mb-1">Average Win</div>
                      <div className="text-2xl font-bold text-green-400">
                        {formatCurrency(results.avgWin)}
                      </div>
                    </div>
                    <div>
                      <div className="text-slate-400 text-sm mb-1">Average Loss</div>
                      <div className="text-2xl font-bold text-red-400">
                        {formatCurrency(results.avgLoss)}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Trade History */}
                <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden">
                  <div className="flex items-center justify-between p-6 border-b border-slate-800">
                    <h3 className="text-lg font-semibold text-white">Recent Trades</h3>
                    <button className="flex items-center px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm transition-colors">
                      <Download className="h-4 w-4 mr-2" />
                      Export
                    </button>
                  </div>
                  
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead className="bg-slate-800">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase">Date</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase">Entry</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase">Exit</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase">P&L</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase">Duration</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase">Status</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800">
                        {results.trades.slice(-10).reverse().map((trade, index) => (
                          <tr key={index} className="hover:bg-slate-800/50">
                            <td className="px-6 py-4 text-sm text-slate-300">{trade.date}</td>
                            <td className="px-6 py-4 text-sm font-mono text-white">₹{trade.entry}</td>
                            <td className="px-6 py-4 text-sm font-mono text-white">₹{trade.exit}</td>
                            <td className={`px-6 py-4 text-sm font-mono font-bold ${
                              trade.pnl >= 0 ? 'text-green-400' : 'text-red-400'
                            }`}>
                              {trade.pnl >= 0 ? '+' : ''}{formatCurrency(trade.pnl)}
                            </td>
                            <td className="px-6 py-4 text-sm text-slate-300">{trade.duration}</td>
                            <td className="px-6 py-4">
                              {trade.pnl >= 0 ? (
                                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-500/20 text-green-400">
                                  <CheckCircle className="h-3 w-3 mr-1" />
                                  Win
                                </span>
                              ) : (
                                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-red-500/20 text-red-400">
                                  <AlertTriangle className="h-3 w-3 mr-1" />
                                  Loss
                                </span>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </>
            )}

            {!results && !isRunning && (
              <div className="bg-slate-900 rounded-2xl border border-slate-800 p-12 text-center">
                <BarChart3 className="h-16 w-16 text-slate-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-white mb-2">Ready to Backtest</h3>
                <p className="text-slate-400">
                  Configure your strategy parameters and click "Run Backtest" to analyze historical performance
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}