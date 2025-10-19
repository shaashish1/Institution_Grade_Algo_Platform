'use client';

import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Play, Pause, RotateCcw, Download, Upload, BarChart3, Settings, Calendar, DollarSign, Target, Activity, AlertTriangle, CheckCircle, Zap, Bitcoin } from 'lucide-react';
import Link from 'next/link';

interface CryptoBacktestParams {
  exchange: string;
  pair: string;
  strategy: string;
  startDate: string;
  endDate: string;
  capital: number;
  timeframe: string;
  leverage: number;
  stopLoss: number;
  takeProfit: number;
  riskPerTrade: number;
}

interface CryptoBacktestResult {
  totalTrades: number;
  winRate: number;
  totalPnL: number;
  totalPnLPercent: number;
  maxDrawdown: number;
  sharpeRatio: number;
  calmarRatio: number;
  avgWin: number;
  avgLoss: number;
  profitFactor: number;
  trades: CryptoTradeResult[];
  monthlyReturns: MonthlyReturn[];
}

interface CryptoTradeResult {
  date: string;
  pair: string;
  side: string;
  entry: number;
  exit: number;
  quantity: number;
  pnl: number;
  pnlPercent: number;
  duration: string;
  fees: number;
}

interface MonthlyReturn {
  month: string;
  return: number;
  trades: number;
}

export default function CryptoBacktesting() {
  const [params, setParams] = useState<CryptoBacktestParams>({
    exchange: 'binance',
    pair: 'BTC/USDT',
    strategy: 'grid-trading',
    startDate: '2024-01-01',
    endDate: '2024-10-31',
    capital: 10000,
    timeframe: '1h',
    leverage: 1,
    stopLoss: 5,
    takeProfit: 10,
    riskPerTrade: 2
  });

  const [results, setResults] = useState<CryptoBacktestResult | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentTrade, setCurrentTrade] = useState(0);

  const exchanges = [
    { value: 'binance', label: 'Binance', logo: '🟡' },
    { value: 'delta', label: 'Delta Exchange', logo: '🔺' },
    { value: 'coinbase', label: 'Coinbase Pro', logo: '🔵' },
    { value: 'bybit', label: 'Bybit', logo: '🟠' }
  ];

  const cryptoPairs = [
    'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'SOL/USDT', 
    'MATIC/USDT', 'DOT/USDT', 'AVAX/USDT', 'LINK/USDT', 'UNI/USDT'
  ];

  const strategies = [
    { value: 'grid-trading', label: 'Grid Trading', description: 'Buy low, sell high in grid pattern' },
    { value: 'dca', label: 'DCA Strategy', description: 'Dollar Cost Averaging' },
    { value: 'momentum', label: 'Momentum Trading', description: 'Follow price momentum' },
    { value: 'mean-reversion', label: 'Mean Reversion', description: 'Buy oversold, sell overbought' },
    { value: 'arbitrage', label: 'Arbitrage', description: 'Price differences between exchanges' },
    { value: 'hodl', label: 'HODL Strategy', description: 'Buy and hold long-term' }
  ];

  const timeframes = [
    { value: '1m', label: '1 Minute' },
    { value: '5m', label: '5 Minutes' },
    { value: '15m', label: '15 Minutes' },
    { value: '1h', label: '1 Hour' },
    { value: '4h', label: '4 Hours' },
    { value: '1d', label: '1 Day' }
  ];

  const runBacktest = async () => {
    setIsRunning(true);
    setProgress(0);
    setCurrentTrade(0);

    // Simulate backtest execution with crypto market conditions
    const totalDays = 300;
    const trades: CryptoTradeResult[] = [];
    const monthlyReturns: MonthlyReturn[] = [];

    for (let i = 0; i < totalDays; i++) {
      await new Promise(resolve => setTimeout(resolve, 15));
      
      setProgress((i / totalDays) * 100);
      setCurrentTrade(i + 1);

      // Generate realistic crypto trade results
      const baseReturn = getCryptoStrategyReturn(params.strategy);
      const cryptoVolatility = 0.6; // Higher volatility for crypto
      const randomReturn = (Math.random() - 0.5) * cryptoVolatility + baseReturn;
      
      const entryPrice = getCryptoPrice(params.pair, i);
      const exitPrice = entryPrice * (1 + randomReturn);
      const quantity = (params.capital * params.riskPerTrade / 100) / entryPrice;
      const pnl = (exitPrice - entryPrice) * quantity * params.leverage;
      const fees = (entryPrice + exitPrice) * quantity * 0.001; // 0.1% trading fees

      trades.push({
        date: new Date(2024, 0, i + 1).toISOString().split('T')[0],
        pair: params.pair,
        side: randomReturn > 0 ? 'LONG' : 'SHORT',
        entry: parseFloat(entryPrice.toFixed(2)),
        exit: parseFloat(exitPrice.toFixed(2)),
        quantity: parseFloat(quantity.toFixed(6)),
        pnl: parseFloat((pnl - fees).toFixed(2)),
        pnlPercent: parseFloat((randomReturn * 100).toFixed(2)),
        duration: getRandomDuration(),
        fees: parseFloat(fees.toFixed(2))
      });
    }

    // Generate monthly returns
    for (let month = 0; month < 10; month++) {
      const monthTrades = trades.filter(t => new Date(t.date).getMonth() === month);
      const monthReturn = monthTrades.reduce((sum, t) => sum + t.pnlPercent, 0);
      monthlyReturns.push({
        month: new Date(2024, month).toLocaleString('default', { month: 'short' }),
        return: parseFloat(monthReturn.toFixed(2)),
        trades: monthTrades.length
      });
    }

    // Calculate comprehensive results
    const winningTrades = trades.filter(t => t.pnl > 0);
    const losingTrades = trades.filter(t => t.pnl < 0);
    const totalPnL = trades.reduce((sum, t) => sum + t.pnl, 0);
    const totalFees = trades.reduce((sum, t) => sum + t.fees, 0);
    
    setResults({
      totalTrades: trades.length,
      winRate: (winningTrades.length / trades.length) * 100,
      totalPnL: totalPnL,
      totalPnLPercent: (totalPnL / params.capital) * 100,
      maxDrawdown: calculateCryptoDrawdown(trades),
      sharpeRatio: calculateCryptoSharpe(trades),
      calmarRatio: calculateCalmarRatio(trades),
      avgWin: winningTrades.length > 0 ? winningTrades.reduce((sum, t) => sum + t.pnl, 0) / winningTrades.length : 0,
      avgLoss: losingTrades.length > 0 ? losingTrades.reduce((sum, t) => sum + t.pnl, 0) / losingTrades.length : 0,
      profitFactor: Math.abs(losingTrades.reduce((sum, t) => sum + t.pnl, 0)) > 0 ? 
        winningTrades.reduce((sum, t) => sum + t.pnl, 0) / Math.abs(losingTrades.reduce((sum, t) => sum + t.pnl, 0)) : 0,
      trades,
      monthlyReturns
    });

    setIsRunning(false);
  };

  const getCryptoStrategyReturn = (strategy: string): number => {
    const returns: Record<string, number> = {
      'grid-trading': 0.015,
      'dca': 0.008,
      'momentum': 0.02,
      'mean-reversion': 0.012,
      'arbitrage': 0.005,
      'hodl': 0.001
    };
    return returns[strategy] || 0;
  };

  const getCryptoPrice = (pair: string, day: number): number => {
    const basePrices: Record<string, number> = {
      'BTC/USDT': 45000,
      'ETH/USDT': 2500,
      'BNB/USDT': 300,
      'ADA/USDT': 0.5,
      'SOL/USDT': 100
    };
    
    const basePrice = basePrices[pair] || 100;
    const trend = Math.sin(day * 0.02) * 0.1; // Simulate market cycles
    const noise = (Math.random() - 0.5) * 0.05;
    
    return basePrice * (1 + trend + noise);
  };

  const getRandomDuration = (): string => {
    const durations = ['2h 15m', '6h 30m', '1d 4h', '3h 45m', '8h 20m', '12h 30m'];
    return durations[Math.floor(Math.random() * durations.length)];
  };

  const calculateCryptoDrawdown = (trades: CryptoTradeResult[]): number => {
    let maxDrawdown = 0;
    let peak = 0;
    let cumulative = 0;

    for (const trade of trades) {
      cumulative += trade.pnl;
      if (cumulative > peak) peak = cumulative;
      const drawdown = peak > 0 ? ((peak - cumulative) / peak) * 100 : 0;
      if (drawdown > maxDrawdown) maxDrawdown = drawdown;
    }

    return maxDrawdown;
  };

  const calculateCryptoSharpe = (trades: CryptoTradeResult[]): number => {
    const returns = trades.map(t => t.pnlPercent);
    const avgReturn = returns.reduce((sum, r) => sum + r, 0) / returns.length;
    const variance = returns.reduce((sum, r) => sum + Math.pow(r - avgReturn, 2), 0) / returns.length;
    const stdDev = Math.sqrt(variance);
    return stdDev !== 0 ? (avgReturn / stdDev) * Math.sqrt(365) : 0; // Assuming daily trading
  };

  const calculateCalmarRatio = (trades: CryptoTradeResult[]): number => {
    const totalReturn = trades.reduce((sum, t) => sum + t.pnlPercent, 0);
    const maxDrawdown = calculateCryptoDrawdown(trades);
    return maxDrawdown !== 0 ? totalReturn / maxDrawdown : 0;
  };

  const resetBacktest = () => {
    setResults(null);
    setProgress(0);
    setCurrentTrade(0);
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
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
            <Link href="/crypto" className="hover:text-blue-400 transition-colors">Crypto</Link>
            <span>/</span>
            <span className="text-white">Backtesting</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center mb-4">
            <Bitcoin className="h-8 w-8 text-orange-400 mr-3" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-orange-400 to-yellow-400 bg-clip-text text-transparent">
              Crypto Strategy Backtesting
            </h1>
          </div>
          <p className="text-slate-300 text-lg">
            Test your cryptocurrency trading strategies across multiple exchanges with advanced risk metrics
          </p>
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
                {/* Exchange Selection */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Exchange</label>
                  <select
                    value={params.exchange}
                    onChange={(e) => setParams(prev => ({ ...prev, exchange: e.target.value }))}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-orange-500 focus:outline-none"
                  >
                    {exchanges.map(exchange => (
                      <option key={exchange.value} value={exchange.value}>
                        {exchange.logo} {exchange.label}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Trading Pair */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Trading Pair</label>
                  <select
                    value={params.pair}
                    onChange={(e) => setParams(prev => ({ ...prev, pair: e.target.value }))}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-orange-500 focus:outline-none"
                  >
                    {cryptoPairs.map(pair => (
                      <option key={pair} value={pair}>{pair}</option>
                    ))}
                  </select>
                </div>

                {/* Strategy Selection */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Strategy</label>
                  <select
                    value={params.strategy}
                    onChange={(e) => setParams(prev => ({ ...prev, strategy: e.target.value }))}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-orange-500 focus:outline-none"
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
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-orange-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">End Date</label>
                    <input
                      type="date"
                      value={params.endDate}
                      onChange={(e) => setParams(prev => ({ ...prev, endDate: e.target.value }))}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-orange-500 focus:outline-none"
                    />
                  </div>
                </div>

                {/* Capital and Timeframe */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Capital (USDT)</label>
                    <input
                      type="number"
                      value={params.capital}
                      onChange={(e) => setParams(prev => ({ ...prev, capital: parseFloat(e.target.value) }))}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-orange-500 focus:outline-none"
                      placeholder="10000"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Timeframe</label>
                    <select
                      value={params.timeframe}
                      onChange={(e) => setParams(prev => ({ ...prev, timeframe: e.target.value }))}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-orange-500 focus:outline-none"
                    >
                      {timeframes.map(tf => (
                        <option key={tf.value} value={tf.value}>{tf.label}</option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Leverage and Risk */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Leverage</label>
                    <input
                      type="number"
                      min="1"
                      max="100"
                      value={params.leverage}
                      onChange={(e) => setParams(prev => ({ ...prev, leverage: parseFloat(e.target.value) }))}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-orange-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Risk per Trade %</label>
                    <input
                      type="number"
                      value={params.riskPerTrade}
                      onChange={(e) => setParams(prev => ({ ...prev, riskPerTrade: parseFloat(e.target.value) }))}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-orange-500 focus:outline-none"
                    />
                  </div>
                </div>

                {/* Stop Loss and Take Profit */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Stop Loss %</label>
                    <input
                      type="number"
                      value={params.stopLoss}
                      onChange={(e) => setParams(prev => ({ ...prev, stopLoss: parseFloat(e.target.value) }))}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-orange-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Take Profit %</label>
                    <input
                      type="number"
                      value={params.takeProfit}
                      onChange={(e) => setParams(prev => ({ ...prev, takeProfit: parseFloat(e.target.value) }))}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-orange-500 focus:outline-none"
                    />
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="space-y-3 pt-4 border-t border-slate-800">
                  <button
                    onClick={runBacktest}
                    disabled={isRunning}
                    className="w-full flex items-center justify-center px-4 py-3 bg-gradient-to-r from-orange-600 to-yellow-600 hover:from-orange-700 hover:to-yellow-700 disabled:from-slate-600 disabled:to-slate-600 rounded-lg font-medium transition-all duration-200"
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
                  <h3 className="text-lg font-semibold text-white flex items-center">
                    <Zap className="h-5 w-5 mr-2 text-yellow-400" />
                    Backtest Progress
                  </h3>
                  <div className="text-sm text-slate-400">Trade {currentTrade} / 300</div>
                </div>
                <div className="bg-slate-800 rounded-full h-3 mb-2">
                  <div 
                    className="bg-gradient-to-r from-orange-500 to-yellow-500 h-3 rounded-full transition-all duration-300"
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
                    <div className="text-xs text-slate-400">
                      {results.totalPnLPercent >= 0 ? '+' : ''}{results.totalPnLPercent.toFixed(2)}%
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
                      <AlertTriangle className="h-4 w-4 text-red-400" />
                    </div>
                    <div className="text-xl font-bold text-red-400">
                      {results.maxDrawdown.toFixed(1)}%
                    </div>
                  </div>
                </div>

                {/* Additional Crypto Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                  <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                    <div className="text-slate-400 text-sm mb-1">Profit Factor</div>
                    <div className="text-2xl font-bold text-orange-400">
                      {results.profitFactor.toFixed(2)}
                    </div>
                  </div>

                  <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                    <div className="text-slate-400 text-sm mb-1">Calmar Ratio</div>
                    <div className="text-2xl font-bold text-yellow-400">
                      {results.calmarRatio.toFixed(2)}
                    </div>
                  </div>

                  <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                    <div className="text-slate-400 text-sm mb-1">Total Trades</div>
                    <div className="text-2xl font-bold text-white">
                      {results.totalTrades}
                    </div>
                  </div>
                </div>

                {/* Monthly Performance */}
                <div className="bg-slate-900 rounded-2xl border border-slate-800 p-6 mb-6">
                  <h3 className="text-lg font-semibold text-white mb-4">Monthly Performance</h3>
                  <div className="grid grid-cols-5 gap-2">
                    {results.monthlyReturns.map((month, index) => (
                      <div 
                        key={index}
                        className={`p-3 rounded-lg text-center ${
                          month.return >= 0 ? 'bg-green-500/20 border border-green-500/30' : 'bg-red-500/20 border border-red-500/30'
                        }`}
                      >
                        <div className="text-xs text-slate-400 mb-1">{month.month}</div>
                        <div className={`text-sm font-bold ${month.return >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                          {month.return >= 0 ? '+' : ''}{month.return.toFixed(1)}%
                        </div>
                        <div className="text-xs text-slate-500">{month.trades} trades</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Trade History */}
                <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden">
                  <div className="flex items-center justify-between p-6 border-b border-slate-800">
                    <h3 className="text-lg font-semibold text-white">Recent Trades</h3>
                    <button className="flex items-center px-3 py-2 bg-orange-600 hover:bg-orange-700 rounded-lg text-sm transition-colors">
                      <Download className="h-4 w-4 mr-2" />
                      Export CSV
                    </button>
                  </div>
                  
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead className="bg-slate-800">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase">Date</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase">Pair</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase">Side</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase">Entry</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase">Exit</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase">P&L</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase">Fees</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800">
                        {results.trades.slice(-15).reverse().map((trade, index) => (
                          <tr key={index} className="hover:bg-slate-800/50">
                            <td className="px-6 py-4 text-sm text-slate-300">{trade.date}</td>
                            <td className="px-6 py-4 text-sm text-white font-medium">{trade.pair}</td>
                            <td className="px-6 py-4">
                              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                                trade.side === 'LONG' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                              }`}>
                                {trade.side}
                              </span>
                            </td>
                            <td className="px-6 py-4 text-sm font-mono text-white">${trade.entry}</td>
                            <td className="px-6 py-4 text-sm font-mono text-white">${trade.exit}</td>
                            <td className={`px-6 py-4 text-sm font-mono font-bold ${
                              trade.pnl >= 0 ? 'text-green-400' : 'text-red-400'
                            }`}>
                              {trade.pnl >= 0 ? '+' : ''}{formatCurrency(trade.pnl)}
                            </td>
                            <td className="px-6 py-4 text-sm font-mono text-slate-400">
                              ${trade.fees.toFixed(2)}
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
                <Bitcoin className="h-16 w-16 text-orange-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-white mb-2">Ready to Backtest Crypto Strategy</h3>
                <p className="text-slate-400">
                  Configure your cryptocurrency trading strategy and click "Run Backtest" to analyze performance
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}