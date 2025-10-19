'use client';

import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, TrendingDown, Target, AlertCircle, Play, Pause, RotateCcw, Download, Settings, Eye, Plus, X, Zap, CheckSquare, Square, Crown, Medal, Award, Filter, ArrowUpDown } from 'lucide-react';
import Link from 'next/link';

interface StrategyConfig {
  id: string;
  name: string;
  type: 'straddle' | 'strangle' | 'iron_condor' | 'iron_butterfly' | 'covered_call' | 'protective_put' | 'bull_call_spread' | 'bear_put_spread';
  symbol: string;
  expiry: string;
  entry_date: string;
  strikes: number[];
  quantities: number[];
  entry_prices: number[];
  active: boolean;
  color: string;
}

interface BacktestResult {
  strategy_id: string;
  total_pnl: number;
  max_profit: number;
  max_loss: number;
  win_rate: number;
  total_trades: number;
  winning_trades: number;
  losing_trades: number;
  avg_profit: number;
  avg_loss: number;
  profit_factor: number;
  sharpe_ratio: number;
  max_drawdown: number;
  calmar_ratio: number;
  daily_pnl: { date: string; pnl: number; cumulative_pnl: number }[];
  trades: {
    entry_date: string;
    exit_date: string;
    pnl: number;
    max_profit_during_trade: number;
    max_loss_during_trade: number;
  }[];
}

interface ComparisonMetrics {
  best_performer: string;
  most_consistent: string;
  highest_sharpe: string;
  lowest_drawdown: string;
  best_win_rate: string;
  highest_profit_factor: string;
  correlation_matrix: { [key: string]: { [key: string]: number } };
  performance_ranking: {
    strategy_id: string;
    rank: number;
    score: number;
    reasons: string[];
  }[];
}

interface StrategySelection {
  [key: string]: boolean;
}

interface SortConfig {
  key: keyof BacktestResult;
  direction: 'asc' | 'desc';
}

const STRATEGY_TEMPLATES = [
  { type: 'straddle', name: 'Long Straddle', color: 'bg-blue-600' },
  { type: 'strangle', name: 'Long Strangle', color: 'bg-purple-600' },
  { type: 'iron_condor', name: 'Iron Condor', color: 'bg-green-600' },
  { type: 'iron_butterfly', name: 'Iron Butterfly', color: 'bg-yellow-600' },
  { type: 'covered_call', name: 'Covered Call', color: 'bg-red-600' },
  { type: 'protective_put', name: 'Protective Put', color: 'bg-indigo-600' },
  { type: 'bull_call_spread', name: 'Bull Call Spread', color: 'bg-emerald-600' },
  { type: 'bear_put_spread', name: 'Bear Put Spread', color: 'bg-orange-600' },
];

const SAMPLE_SYMBOLS = ['NIFTY', 'BANKNIFTY', 'FINNIFTY', 'RELIANCE', 'TCS', 'HDFCBANK'];

// Generate sample backtest results
const generateBacktestResults = (strategies: StrategyConfig[]): BacktestResult[] => {
  return strategies.map(strategy => {
    const totalTrades = 50 + Math.floor(Math.random() * 100);
    const winRate = 0.4 + Math.random() * 0.4; // 40-80% win rate
    const winningTrades = Math.floor(totalTrades * winRate);
    const losingTrades = totalTrades - winningTrades;
    
    const avgProfit = 2000 + Math.random() * 3000;
    const avgLoss = -(1000 + Math.random() * 2000);
    const totalPnL = (winningTrades * avgProfit) + (losingTrades * avgLoss);
    
    const maxProfit = avgProfit * 2;
    const maxLoss = avgLoss * 2;
    const profitFactor = Math.abs((winningTrades * avgProfit) / (losingTrades * avgLoss));
    const sharpeRatio = 0.5 + Math.random() * 1.5;
    const maxDrawdown = -(totalPnL * 0.1 + Math.random() * totalPnL * 0.2);
    const calmarRatio = (totalPnL / 365) / Math.abs(maxDrawdown);

    // Generate daily P&L data
    const dailyPnL = [];
    let cumulativePnL = 0;
    for (let i = 0; i < 90; i++) {
      const dailyReturn = (Math.random() - 0.5) * 1000;
      cumulativePnL += dailyReturn;
      dailyPnL.push({
        date: new Date(2025, 6, i + 1).toISOString().split('T')[0],
        pnl: dailyReturn,
        cumulative_pnl: cumulativePnL
      });
    }

    // Generate individual trades
    const trades = [];
    for (let i = 0; i < totalTrades; i++) {
      const isWinning = Math.random() < winRate;
      const pnl = isWinning ? avgProfit * (0.5 + Math.random()) : avgLoss * (0.5 + Math.random());
      trades.push({
        entry_date: new Date(2025, 6, Math.floor(Math.random() * 90)).toISOString().split('T')[0],
        exit_date: new Date(2025, 6, Math.floor(Math.random() * 90) + 1).toISOString().split('T')[0],
        pnl,
        max_profit_during_trade: Math.max(0, pnl * 1.2),
        max_loss_during_trade: Math.min(0, pnl * 1.3)
      });
    }

    return {
      strategy_id: strategy.id,
      total_pnl: totalPnL,
      max_profit: maxProfit,
      max_loss: maxLoss,
      win_rate: winRate,
      total_trades: totalTrades,
      winning_trades: winningTrades,
      losing_trades: losingTrades,
      avg_profit: avgProfit,
      avg_loss: avgLoss,
      profit_factor: profitFactor,
      sharpe_ratio: sharpeRatio,
      max_drawdown: maxDrawdown,
      calmar_ratio: calmarRatio,
      daily_pnl: dailyPnL,
      trades
    };
  });
};

export function MultiStrategyBacktest() {
  const [strategies, setStrategies] = useState<StrategyConfig[]>([]);
  const [results, setResults] = useState<BacktestResult[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [showAddStrategy, setShowAddStrategy] = useState(false);
  const [comparisonView, setComparisonView] = useState<'overview' | 'detailed' | 'chart' | 'ranking'>('overview');
  const [selectedMetric, setSelectedMetric] = useState<'pnl' | 'sharpe' | 'drawdown' | 'win_rate'>('pnl');
  const [selectedStrategies, setSelectedStrategies] = useState<StrategySelection>({});
  const [sortConfig, setSortConfig] = useState<SortConfig>({ key: 'total_pnl', direction: 'desc' });
  const [showOnlySelected, setShowOnlySelected] = useState(false);

  const addStrategy = (type: string) => {
    const template = STRATEGY_TEMPLATES.find(t => t.type === type);
    if (!template) return;

    const newStrategy: StrategyConfig = {
      id: `strategy_${Date.now()}`,
      name: `${template.name} ${strategies.length + 1}`,
      type: type as any,
      symbol: 'NIFTY',
      expiry: '28-NOV-2025',
      entry_date: '2025-07-01',
      strikes: type === 'straddle' ? [25700] : [25600, 25800],
      quantities: [1],
      entry_prices: [250],
      active: true,
      color: template.color
    };

    setStrategies([...strategies, newStrategy]);
    setShowAddStrategy(false);
  };

  const removeStrategy = (id: string) => {
    setStrategies(strategies.filter(s => s.id !== id));
    setResults(results.filter(r => r.strategy_id !== id));
  };

  const toggleStrategy = (id: string) => {
    setStrategies(strategies.map(s => 
      s.id === id ? { ...s, active: !s.active } : s
    ));
  };

  const runBacktest = async () => {
    setIsRunning(true);
    
    // Simulate backtest execution
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const activeStrategies = strategies.filter(s => s.active);
    const backtestResults = generateBacktestResults(activeStrategies);
    setResults(backtestResults);
    setIsRunning(false);
  };

  const getComparisonMetrics = (): ComparisonMetrics => {
    if (results.length === 0) {
      return {
        best_performer: '',
        most_consistent: '',
        highest_sharpe: '',
        lowest_drawdown: '',
        best_win_rate: '',
        highest_profit_factor: '',
        correlation_matrix: {},
        performance_ranking: []
      };
    }

    const bestPerformer = results.reduce((max, r) => r.total_pnl > max.total_pnl ? r : max);
    const highestSharpe = results.reduce((max, r) => r.sharpe_ratio > max.sharpe_ratio ? r : max);
    const lowestDrawdown = results.reduce((min, r) => r.max_drawdown > min.max_drawdown ? r : min);
    const mostConsistent = results.reduce((min, r) => Math.abs(r.max_drawdown) < Math.abs(min.max_drawdown) ? r : min);
    const bestWinRate = results.reduce((max, r) => r.win_rate > max.win_rate ? r : max);
    const highestProfitFactor = results.reduce((max, r) => r.profit_factor > max.profit_factor ? r : max);

    // Calculate performance ranking with composite score
    const performanceRanking = results.map(result => {
      const strategy = strategies.find(s => s.id === result.strategy_id);
      const normalizedPnL = (result.total_pnl - Math.min(...results.map(r => r.total_pnl))) / 
                           (Math.max(...results.map(r => r.total_pnl)) - Math.min(...results.map(r => r.total_pnl)) || 1);
      const normalizedSharpe = (result.sharpe_ratio - Math.min(...results.map(r => r.sharpe_ratio))) / 
                              (Math.max(...results.map(r => r.sharpe_ratio)) - Math.min(...results.map(r => r.sharpe_ratio)) || 1);
      const normalizedDrawdown = 1 - ((Math.abs(result.max_drawdown) - Math.min(...results.map(r => Math.abs(r.max_drawdown)))) / 
                                     (Math.max(...results.map(r => Math.abs(r.max_drawdown))) - Math.min(...results.map(r => Math.abs(r.max_drawdown))) || 1));
      const normalizedWinRate = (result.win_rate - Math.min(...results.map(r => r.win_rate))) / 
                               (Math.max(...results.map(r => r.win_rate)) - Math.min(...results.map(r => r.win_rate)) || 1);

      // Composite score with weights
      const score = (normalizedPnL * 0.3) + (normalizedSharpe * 0.25) + (normalizedDrawdown * 0.25) + (normalizedWinRate * 0.2);
      
      const reasons = [];
      if (result.strategy_id === bestPerformer.strategy_id) reasons.push('Highest P&L');
      if (result.strategy_id === highestSharpe.strategy_id) reasons.push('Best Sharpe Ratio');
      if (result.strategy_id === lowestDrawdown.strategy_id) reasons.push('Lowest Drawdown');
      if (result.strategy_id === bestWinRate.strategy_id) reasons.push('Highest Win Rate');
      if (result.strategy_id === highestProfitFactor.strategy_id) reasons.push('Best Profit Factor');
      
      return {
        strategy_id: result.strategy_id,
        rank: 0, // Will be set after sorting
        score,
        reasons
      };
    }).sort((a, b) => b.score - a.score).map((item, index) => ({ ...item, rank: index + 1 }));

    return {
      best_performer: strategies.find(s => s.id === bestPerformer.strategy_id)?.name || '',
      most_consistent: strategies.find(s => s.id === mostConsistent.strategy_id)?.name || '',
      highest_sharpe: strategies.find(s => s.id === highestSharpe.strategy_id)?.name || '',
      lowest_drawdown: strategies.find(s => s.id === lowestDrawdown.strategy_id)?.name || '',
      best_win_rate: strategies.find(s => s.id === bestWinRate.strategy_id)?.name || '',
      highest_profit_factor: strategies.find(s => s.id === highestProfitFactor.strategy_id)?.name || '',
      correlation_matrix: {},
      performance_ranking: performanceRanking
    };
  };

  const formatNumber = (num: number) => {
    if (Math.abs(num) >= 10000000) return (num / 10000000).toFixed(1) + 'Cr';
    if (Math.abs(num) >= 100000) return (num / 100000).toFixed(1) + 'L';
    if (Math.abs(num) >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toFixed(0);
  };

  // Multi-select helper functions
  const toggleStrategySelection = (strategyId: string) => {
    setSelectedStrategies(prev => ({
      ...prev,
      [strategyId]: !prev[strategyId]
    }));
  };

  const selectAllStrategies = () => {
    const newSelection: StrategySelection = {};
    results.forEach(result => {
      newSelection[result.strategy_id] = true;
    });
    setSelectedStrategies(newSelection);
  };

  const clearAllSelections = () => {
    setSelectedStrategies({});
  };

  const getSelectedResults = () => {
    if (showOnlySelected) {
      return results.filter(result => selectedStrategies[result.strategy_id]);
    }
    return results;
  };

  const handleSort = (key: keyof BacktestResult) => {
    const direction = sortConfig.key === key && sortConfig.direction === 'desc' ? 'asc' : 'desc';
    setSortConfig({ key, direction });
  };

  const getSortedResults = () => {
    const resultsToSort = getSelectedResults();
    return [...resultsToSort].sort((a, b) => {
      const aValue = a[sortConfig.key] as number;
      const bValue = b[sortConfig.key] as number;
      
      if (sortConfig.direction === 'asc') {
        return aValue - bValue;
      }
      return bValue - aValue;
    });
  };

  const getSelectedCount = () => {
    return Object.values(selectedStrategies).filter(Boolean).length;
  };

  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1: return <Crown className="h-5 w-5 text-yellow-400" />;
      case 2: return <Medal className="h-5 w-5 text-gray-400" />;
      case 3: return <Award className="h-5 w-5 text-orange-400" />;
      default: return <span className="text-slate-400 font-bold">#{rank}</span>;
    }
  };

  const comparisonMetrics = getComparisonMetrics();

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4">
      <div className="max-w-full mx-auto">
        {/* Navigation Breadcrumb */}
        <div className="mb-6">
          <nav className="flex items-center space-x-2 text-sm text-slate-400">
            <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
            <span>/</span>
            <Link href="/stocks" className="hover:text-blue-400 transition-colors">Stocks</Link>
            <span>/</span>
            <Link href="/stocks/backtest" className="hover:text-blue-400 transition-colors">Backtest</Link>
            <span>/</span>
            <span className="text-white">Multi-Strategy Comparison</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
                Multi-Strategy Backtesting Hub
              </h1>
              <p className="text-slate-400">
                Compare multiple option strategies side-by-side with comprehensive performance analytics
              </p>
            </div>
            
            <div className="flex items-center gap-4">
              <button
                onClick={() => setShowAddStrategy(true)}
                className="flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg transition-colors"
              >
                <Plus className="h-4 w-4 mr-2" />
                Add Strategy
              </button>
              <button
                onClick={runBacktest}
                disabled={isRunning || strategies.filter(s => s.active).length === 0}
                className="flex items-center px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:cursor-not-allowed rounded-lg transition-colors"
              >
                {isRunning ? (
                  <>
                    <div className="animate-spin h-4 w-4 mr-2 border-2 border-white border-t-transparent rounded-full" />
                    Running...
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4 mr-2" />
                    Run Backtest
                  </>
                )}
              </button>
              <button className="flex items-center px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors">
                <Download className="h-4 w-4 mr-2" />
                Export
              </button>
            </div>
          </div>

          {/* Strategy Management */}
          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800 mb-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-white">Strategy Configuration</h2>
              <span className="text-sm text-slate-400">
                {strategies.filter(s => s.active).length} active of {strategies.length} total
              </span>
            </div>

            {strategies.length === 0 ? (
              <div className="text-center py-8">
                <Target className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                <p className="text-slate-400 mb-4">No strategies configured yet</p>
                <button
                  onClick={() => setShowAddStrategy(true)}
                  className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
                >
                  Add Your First Strategy
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {strategies.map((strategy) => (
                  <div
                    key={strategy.id}
                    className={`bg-slate-800 rounded-xl p-4 border ${
                      strategy.active ? 'border-blue-500/50' : 'border-slate-700'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-2">
                        <div className={`w-3 h-3 rounded-full ${strategy.color}`} />
                        <h3 className="font-medium text-white">{strategy.name}</h3>
                      </div>
                      <button
                        onClick={() => removeStrategy(strategy.id)}
                        className="text-slate-400 hover:text-red-400 transition-colors"
                      >
                        <X className="h-4 w-4" />
                      </button>
                    </div>
                    
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-slate-400">Symbol:</span>
                        <span className="text-white">{strategy.symbol}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Type:</span>
                        <span className="text-white">{strategy.type.replace('_', ' ')}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Strikes:</span>
                        <span className="text-white">{strategy.strikes.join(', ')}</span>
                      </div>
                    </div>
                    
                    <div className="mt-4">
                      <button
                        onClick={() => toggleStrategy(strategy.id)}
                        className={`w-full py-2 px-3 rounded-lg text-sm font-medium transition-colors ${
                          strategy.active
                            ? 'bg-green-600 hover:bg-green-700 text-white'
                            : 'bg-slate-700 hover:bg-slate-600 text-slate-300'
                        }`}
                      >
                        {strategy.active ? 'Active' : 'Inactive'}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Add Strategy Modal */}
        {showAddStrategy && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800 max-w-2xl w-full mx-4">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-white">Add New Strategy</h2>
                <button
                  onClick={() => setShowAddStrategy(false)}
                  className="text-slate-400 hover:text-white transition-colors"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {STRATEGY_TEMPLATES.map((template) => (
                  <button
                    key={template.type}
                    onClick={() => addStrategy(template.type)}
                    className="p-4 bg-slate-800 hover:bg-slate-700 rounded-xl border border-slate-700 hover:border-blue-500/50 transition-all"
                  >
                    <div className="flex items-center space-x-3">
                      <div className={`w-4 h-4 rounded-full ${template.color}`} />
                      <span className="font-medium text-white">{template.name}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Results Section */}
        {results.length > 0 && (
          <div className="space-y-6">
            {/* Comparison View Toggle */}
            <div className="flex space-x-1 bg-slate-800 rounded-lg p-1">
              <button
                onClick={() => setComparisonView('overview')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  comparisonView === 'overview' 
                    ? 'bg-blue-600 text-white' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-700'
                }`}
              >
                Overview
              </button>
              <button
                onClick={() => setComparisonView('ranking')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  comparisonView === 'ranking' 
                    ? 'bg-yellow-600 text-white' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-700'
                }`}
              >
                <Crown className="h-4 w-4 mr-1 inline" />
                Rankings
              </button>
              <button
                onClick={() => setComparisonView('detailed')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  comparisonView === 'detailed' 
                    ? 'bg-purple-600 text-white' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-700'
                }`}
              >
                Detailed Metrics
              </button>
              <button
                onClick={() => setComparisonView('chart')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  comparisonView === 'chart' 
                    ? 'bg-green-600 text-white' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-700'
                }`}
              >
                Performance Chart
              </button>
            </div>

            {/* Overview */}
            {comparisonView === 'overview' && (
              <div className="space-y-6">
                {/* Winner Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
                  <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-slate-400">Best Performer</span>
                      <TrendingUp className="h-4 w-4 text-green-400" />
                    </div>
                    <div className="text-sm font-bold text-green-400">{comparisonMetrics.best_performer}</div>
                  </div>
                  <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-slate-400">Highest Sharpe</span>
                      <BarChart3 className="h-4 w-4 text-blue-400" />
                    </div>
                    <div className="text-sm font-bold text-blue-400">{comparisonMetrics.highest_sharpe}</div>
                  </div>
                  <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-slate-400">Most Consistent</span>
                      <Target className="h-4 w-4 text-purple-400" />
                    </div>
                    <div className="text-sm font-bold text-purple-400">{comparisonMetrics.most_consistent}</div>
                  </div>
                  <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-slate-400">Lowest Drawdown</span>
                      <AlertCircle className="h-4 w-4 text-yellow-400" />
                    </div>
                    <div className="text-sm font-bold text-yellow-400">{comparisonMetrics.lowest_drawdown}</div>
                  </div>
                  <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-slate-400">Best Win Rate</span>
                      <Target className="h-4 w-4 text-cyan-400" />
                    </div>
                    <div className="text-sm font-bold text-cyan-400">{comparisonMetrics.best_win_rate}</div>
                  </div>
                  <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-slate-400">Best Profit Factor</span>
                      <Crown className="h-4 w-4 text-orange-400" />
                    </div>
                    <div className="text-sm font-bold text-orange-400">{comparisonMetrics.highest_profit_factor}</div>
                  </div>
                </div>

                {/* Multi-Select Controls */}
                <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-bold text-white">Strategy Selection & Comparison</h3>
                    <div className="flex items-center space-x-4">
                      <span className="text-sm text-slate-400">
                        {getSelectedCount()} of {results.length} selected
                      </span>
                      <div className="flex space-x-2">
                        <button
                          onClick={selectAllStrategies}
                          className="px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm transition-colors"
                        >
                          Select All
                        </button>
                        <button
                          onClick={clearAllSelections}
                          className="px-3 py-1 bg-slate-700 hover:bg-slate-600 rounded text-sm transition-colors"
                        >
                          Clear All
                        </button>
                        <button
                          onClick={() => setShowOnlySelected(!showOnlySelected)}
                          className={`px-3 py-1 rounded text-sm transition-colors ${
                            showOnlySelected 
                              ? 'bg-green-600 hover:bg-green-700' 
                              : 'bg-slate-700 hover:bg-slate-600'
                          }`}
                        >
                          <Filter className="h-3 w-3 mr-1 inline" />
                          {showOnlySelected ? 'Show All' : 'Show Selected'}
                        </button>
                      </div>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                    {results.map((result, index) => {
                      const strategy = strategies.find(s => s.id === result.strategy_id);
                      const ranking = comparisonMetrics.performance_ranking.find(r => r.strategy_id === result.strategy_id);
                      const isSelected = selectedStrategies[result.strategy_id];
                      
                      return (
                        <div
                          key={index}
                          onClick={() => toggleStrategySelection(result.strategy_id)}
                          className={`p-3 rounded-lg border cursor-pointer transition-all ${
                            isSelected 
                              ? 'border-blue-500 bg-blue-500/10' 
                              : 'border-slate-700 bg-slate-800 hover:border-slate-600'
                          }`}
                        >
                          <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center space-x-2">
                              {isSelected ? 
                                <CheckSquare className="h-4 w-4 text-blue-400" /> : 
                                <Square className="h-4 w-4 text-slate-400" />
                              }
                              <div className={`w-3 h-3 rounded-full ${strategy?.color}`} />
                              <span className="font-medium text-white text-sm">{strategy?.name}</span>
                            </div>
                            {ranking && getRankIcon(ranking.rank)}
                          </div>
                          
                          <div className="space-y-1 text-xs">
                            <div className="flex justify-between">
                              <span className="text-slate-400">P&L:</span>
                              <span className={`font-bold ${result.total_pnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                                ₹{formatNumber(result.total_pnl)}
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-slate-400">Win Rate:</span>
                              <span className="text-white">{(result.win_rate * 100).toFixed(1)}%</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-slate-400">Sharpe:</span>
                              <span className="text-blue-400">{result.sharpe_ratio.toFixed(2)}</span>
                            </div>
                            {ranking && ranking.reasons.length > 0 && (
                              <div className="text-xs text-yellow-400 mt-1">
                                {ranking.reasons[0]}
                              </div>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Performance Summary Table */}
                <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden">
                  <div className="p-4 border-b border-slate-800 flex items-center justify-between">
                    <h2 className="text-xl font-bold text-white">Performance Summary</h2>
                    <div className="flex items-center space-x-2 text-sm text-slate-400">
                      <span>Showing {getSortedResults().length} strategies</span>
                      {getSelectedCount() > 0 && (
                        <span className="text-blue-400">({getSelectedCount()} selected)</span>
                      )}
                    </div>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead className="bg-slate-800">
                        <tr>
                          <th className="px-4 py-3 text-left">Rank</th>
                          <th className="px-4 py-3 text-left">Strategy</th>
                          <th className="px-4 py-3 text-right cursor-pointer hover:bg-slate-700" onClick={() => handleSort('total_pnl')}>
                            <div className="flex items-center justify-end">
                              Total P&L
                              <ArrowUpDown className="h-3 w-3 ml-1" />
                            </div>
                          </th>
                          <th className="px-4 py-3 text-right cursor-pointer hover:bg-slate-700" onClick={() => handleSort('win_rate')}>
                            <div className="flex items-center justify-end">
                              Win Rate
                              <ArrowUpDown className="h-3 w-3 ml-1" />
                            </div>
                          </th>
                          <th className="px-4 py-3 text-right cursor-pointer hover:bg-slate-700" onClick={() => handleSort('sharpe_ratio')}>
                            <div className="flex items-center justify-end">
                              Sharpe Ratio
                              <ArrowUpDown className="h-3 w-3 ml-1" />
                            </div>
                          </th>
                          <th className="px-4 py-3 text-right cursor-pointer hover:bg-slate-700" onClick={() => handleSort('max_drawdown')}>
                            <div className="flex items-center justify-end">
                              Max Drawdown
                              <ArrowUpDown className="h-3 w-3 ml-1" />
                            </div>
                          </th>
                          <th className="px-4 py-3 text-right cursor-pointer hover:bg-slate-700" onClick={() => handleSort('profit_factor')}>
                            <div className="flex items-center justify-end">
                              Profit Factor
                              <ArrowUpDown className="h-3 w-3 ml-1" />
                            </div>
                          </th>
                          <th className="px-4 py-3 text-right">Total Trades</th>
                        </tr>
                      </thead>
                      <tbody>
                        {getSortedResults().map((result, index) => {
                          const strategy = strategies.find(s => s.id === result.strategy_id);
                          const ranking = comparisonMetrics.performance_ranking.find(r => r.strategy_id === result.strategy_id);
                          const isSelected = selectedStrategies[result.strategy_id];
                          
                          return (
                            <tr 
                              key={index} 
                              className={`border-t border-slate-800 hover:bg-slate-800/50 cursor-pointer ${
                                isSelected ? 'bg-blue-500/5' : ''
                              }`}
                              onClick={() => toggleStrategySelection(result.strategy_id)}
                            >
                              <td className="px-4 py-3">
                                {ranking && getRankIcon(ranking.rank)}
                              </td>
                              <td className="px-4 py-3">
                                <div className="flex items-center space-x-2">
                                  {isSelected ? 
                                    <CheckSquare className="h-4 w-4 text-blue-400" /> : 
                                    <Square className="h-4 w-4 text-slate-400" />
                                  }
                                  <div className={`w-3 h-3 rounded-full ${strategy?.color}`} />
                                  <span className="font-medium text-white">{strategy?.name}</span>
                                </div>
                              </td>
                              <td className={`px-4 py-3 text-right font-mono font-bold ${
                                result.total_pnl >= 0 ? 'text-green-400' : 'text-red-400'
                              }`}>
                                ₹{formatNumber(result.total_pnl)}
                              </td>
                              <td className="px-4 py-3 text-right font-mono text-white">
                                {(result.win_rate * 100).toFixed(1)}%
                              </td>
                              <td className="px-4 py-3 text-right font-mono text-blue-400">
                                {result.sharpe_ratio.toFixed(2)}
                              </td>
                              <td className="px-4 py-3 text-right font-mono text-red-400">
                                ₹{formatNumber(result.max_drawdown)}
                              </td>
                              <td className="px-4 py-3 text-right font-mono text-purple-400">
                                {result.profit_factor.toFixed(2)}
                              </td>
                              <td className="px-4 py-3 text-right font-mono text-slate-300">
                                {result.total_trades}
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}

            {/* Rankings View */}
            {comparisonView === 'ranking' && (
              <div className="space-y-6">
                {/* Ranking Overview */}
                <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-xl font-bold text-white flex items-center">
                      <Crown className="h-6 w-6 text-yellow-400 mr-2" />
                      Strategy Performance Rankings
                    </h2>
                    <div className="text-sm text-slate-400">
                      Ranked by composite performance score
                    </div>
                  </div>

                  {/* Top 3 Podium */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    {comparisonMetrics.performance_ranking.slice(0, 3).map((ranking, index) => {
                      const strategy = strategies.find(s => s.id === ranking.strategy_id);
                      const result = results.find(r => r.strategy_id === ranking.strategy_id);
                      
                      return (
                        <div
                          key={index}
                          className={`relative p-6 rounded-2xl border-2 ${
                            ranking.rank === 1 
                              ? 'border-yellow-400 bg-yellow-400/5' 
                              : ranking.rank === 2 
                              ? 'border-gray-400 bg-gray-400/5' 
                              : 'border-orange-400 bg-orange-400/5'
                          }`}
                        >
                          <div className="text-center">
                            <div className="mb-4">
                              {getRankIcon(ranking.rank)}
                            </div>
                            <div className="flex items-center justify-center space-x-2 mb-2">
                              <div className={`w-4 h-4 rounded-full ${strategy?.color}`} />
                              <h3 className="text-lg font-bold text-white">{strategy?.name}</h3>
                            </div>
                            <div className="text-2xl font-bold text-white mb-2">
                              Score: {(ranking.score * 100).toFixed(1)}
                            </div>
                            {result && (
                              <div className="space-y-1 text-sm">
                                <div className={`font-bold ${result.total_pnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                                  P&L: ₹{formatNumber(result.total_pnl)}
                                </div>
                                <div className="text-slate-300">
                                  Win Rate: {(result.win_rate * 100).toFixed(1)}%
                                </div>
                                <div className="text-blue-400">
                                  Sharpe: {result.sharpe_ratio.toFixed(2)}
                                </div>
                              </div>
                            )}
                            {ranking.reasons.length > 0 && (
                              <div className="mt-3 space-y-1">
                                {ranking.reasons.map((reason, idx) => (
                                  <div key={idx} className="text-xs text-yellow-400 bg-yellow-400/10 px-2 py-1 rounded">
                                    {reason}
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  {/* Complete Rankings Table */}
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead className="bg-slate-800">
                        <tr>
                          <th className="px-4 py-3 text-left">Rank</th>
                          <th className="px-4 py-3 text-left">Strategy</th>
                          <th className="px-4 py-3 text-right">Score</th>
                          <th className="px-4 py-3 text-right">Total P&L</th>
                          <th className="px-4 py-3 text-right">Win Rate</th>
                          <th className="px-4 py-3 text-right">Sharpe</th>
                          <th className="px-4 py-3 text-right">Max DD</th>
                          <th className="px-4 py-3 text-left">Achievements</th>
                        </tr>
                      </thead>
                      <tbody>
                        {comparisonMetrics.performance_ranking.map((ranking, index) => {
                          const strategy = strategies.find(s => s.id === ranking.strategy_id);
                          const result = results.find(r => r.strategy_id === ranking.strategy_id);
                          
                          return (
                            <tr 
                              key={index} 
                              className={`border-t border-slate-800 hover:bg-slate-800/50 ${
                                ranking.rank <= 3 ? 'bg-slate-800/30' : ''
                              }`}
                            >
                              <td className="px-4 py-3">
                                <div className="flex items-center">
                                  {getRankIcon(ranking.rank)}
                                </div>
                              </td>
                              <td className="px-4 py-3">
                                <div className="flex items-center space-x-2">
                                  <div className={`w-3 h-3 rounded-full ${strategy?.color}`} />
                                  <span className="font-medium text-white">{strategy?.name}</span>
                                </div>
                              </td>
                              <td className="px-4 py-3 text-right">
                                <div className="font-bold text-white">{(ranking.score * 100).toFixed(1)}</div>
                                <div className="text-xs text-slate-400">/100</div>
                              </td>
                              {result && (
                                <>
                                  <td className={`px-4 py-3 text-right font-mono font-bold ${
                                    result.total_pnl >= 0 ? 'text-green-400' : 'text-red-400'
                                  }`}>
                                    ₹{formatNumber(result.total_pnl)}
                                  </td>
                                  <td className="px-4 py-3 text-right font-mono text-white">
                                    {(result.win_rate * 100).toFixed(1)}%
                                  </td>
                                  <td className="px-4 py-3 text-right font-mono text-blue-400">
                                    {result.sharpe_ratio.toFixed(2)}
                                  </td>
                                  <td className="px-4 py-3 text-right font-mono text-red-400">
                                    ₹{formatNumber(result.max_drawdown)}
                                  </td>
                                </>
                              )}
                              <td className="px-4 py-3">
                                <div className="flex flex-wrap gap-1">
                                  {ranking.reasons.slice(0, 2).map((reason, idx) => (
                                    <span key={idx} className="text-xs text-yellow-400 bg-yellow-400/10 px-2 py-1 rounded">
                                      {reason}
                                    </span>
                                  ))}
                                  {ranking.reasons.length > 2 && (
                                    <span className="text-xs text-slate-400">+{ranking.reasons.length - 2} more</span>
                                  )}
                                </div>
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>

                  {/* Ranking Methodology */}
                  <div className="mt-6 p-4 bg-slate-800 rounded-lg">
                    <h3 className="text-sm font-bold text-white mb-2">Ranking Methodology</h3>
                    <div className="text-xs text-slate-400 space-y-1">
                      <p>• <span className="font-medium">Composite Score</span> = Total P&L (30%) + Sharpe Ratio (25%) + Low Drawdown (25%) + Win Rate (20%)</p>
                      <p>• <span className="font-medium">Achievements</span> = Individual category winners (Best P&L, Highest Sharpe, etc.)</p>
                      <p>• <span className="font-medium">Normalization</span> = All metrics normalized to 0-1 scale for fair comparison</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
            {comparisonView === 'detailed' && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {results.map((result, index) => {
                  const strategy = strategies.find(s => s.id === result.strategy_id);
                  return (
                    <div key={index} className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                      <div className="flex items-center space-x-2 mb-4">
                        <div className={`w-4 h-4 rounded-full ${strategy?.color}`} />
                        <h3 className="text-lg font-bold text-white">{strategy?.name}</h3>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div className="space-y-3">
                          <div className="flex justify-between">
                            <span className="text-slate-400">Total P&L:</span>
                            <span className={`font-bold ${result.total_pnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                              ₹{formatNumber(result.total_pnl)}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-400">Win Rate:</span>
                            <span className="text-white">{(result.win_rate * 100).toFixed(1)}%</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-400">Avg Profit:</span>
                            <span className="text-green-400">₹{formatNumber(result.avg_profit)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-400">Avg Loss:</span>
                            <span className="text-red-400">₹{formatNumber(result.avg_loss)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-400">Total Trades:</span>
                            <span className="text-white">{result.total_trades}</span>
                          </div>
                        </div>
                        
                        <div className="space-y-3">
                          <div className="flex justify-between">
                            <span className="text-slate-400">Sharpe Ratio:</span>
                            <span className="text-blue-400">{result.sharpe_ratio.toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-400">Max Drawdown:</span>
                            <span className="text-red-400">₹{formatNumber(result.max_drawdown)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-400">Profit Factor:</span>
                            <span className="text-purple-400">{result.profit_factor.toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-400">Calmar Ratio:</span>
                            <span className="text-yellow-400">{result.calmar_ratio.toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-400">Winning Trades:</span>
                            <span className="text-green-400">{result.winning_trades}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}

            {/* Performance Chart */}
            {comparisonView === 'chart' && (
              <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-bold text-white">Performance Comparison Chart</h2>
                  <div className="flex items-center space-x-4">
                    <select
                      value={selectedMetric}
                      onChange={(e) => setSelectedMetric(e.target.value as any)}
                      className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white text-sm focus:border-blue-500 focus:outline-none"
                    >
                      <option value="pnl">Cumulative P&L</option>
                      <option value="sharpe">Sharpe Ratio</option>
                      <option value="drawdown">Drawdown</option>
                      <option value="win_rate">Win Rate</option>
                    </select>
                    <div className="text-sm text-slate-400">
                      {getSelectedCount() > 0 ? `Comparing ${getSelectedCount()} selected` : `Showing all ${results.length}`} strategies
                    </div>
                  </div>
                </div>
                
                {/* Chart Placeholder with Strategy Performance Bars */}
                <div className="h-80 bg-slate-800 rounded-xl p-6">
                  <div className="h-full flex items-end justify-center space-x-4">
                    {(getSelectedCount() > 0 ? getSortedResults() : results).map((result, index) => {
                      const strategy = strategies.find(s => s.id === result.strategy_id);
                      const ranking = comparisonMetrics.performance_ranking.find(r => r.strategy_id === result.strategy_id);
                      const maxValue = Math.max(...results.map(r => Math.abs(r.total_pnl)));
                      const height = Math.abs(result.total_pnl) / maxValue * 100;
                      
                      return (
                        <div key={index} className="flex flex-col items-center space-y-2">
                          <div className="text-xs text-slate-400 transform -rotate-45 origin-bottom-left whitespace-nowrap">
                            {strategy?.name}
                          </div>
                          <div 
                            className={`w-8 rounded-t-md ${strategy?.color} opacity-80 relative group cursor-pointer`}
                            style={{ height: `${height}%`, minHeight: '20px' }}
                          >
                            {ranking && ranking.rank <= 3 && (
                              <div className="absolute -top-6 left-1/2 transform -translate-x-1/2">
                                {getRankIcon(ranking.rank)}
                              </div>
                            )}
                            
                            {/* Tooltip */}
                            <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-slate-700 rounded-lg text-xs text-white opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-10 whitespace-nowrap">
                              <div className="font-bold">{strategy?.name}</div>
                              <div className="text-green-400">P&L: ₹{formatNumber(result.total_pnl)}</div>
                              <div className="text-blue-400">Sharpe: {result.sharpe_ratio.toFixed(2)}</div>
                              <div className="text-yellow-400">Win Rate: {(result.win_rate * 100).toFixed(1)}%</div>
                              {ranking && (
                                <div className="text-purple-400">Rank: #{ranking.rank}</div>
                              )}
                            </div>
                          </div>
                          <div className={`text-xs font-bold ${result.total_pnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                            ₹{formatNumber(result.total_pnl)}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
                
                {/* Strategy Legend */}
                <div className="mt-6">
                  <h3 className="text-sm font-bold text-white mb-3">Strategy Legend</h3>
                  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                    {(getSelectedCount() > 0 ? getSortedResults() : results).map((result, index) => {
                      const strategy = strategies.find(s => s.id === result.strategy_id);
                      const ranking = comparisonMetrics.performance_ranking.find(r => r.strategy_id === result.strategy_id);
                      const isSelected = selectedStrategies[result.strategy_id];
                      
                      return (
                        <div 
                          key={index} 
                          className={`flex items-center space-x-2 p-2 rounded-lg ${
                            isSelected ? 'bg-blue-500/10 border border-blue-500/30' : 'bg-slate-800'
                          }`}
                        >
                          <div className={`w-3 h-3 rounded-full ${strategy?.color}`} />
                          <span className="text-sm text-slate-300">{strategy?.name}</span>
                          {ranking && ranking.rank <= 3 && (
                            <div className="ml-auto">
                              {getRankIcon(ranking.rank)}
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Chart Controls */}
                {getSelectedCount() > 0 && (
                  <div className="mt-4 p-3 bg-blue-500/10 rounded-lg border border-blue-500/30">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-blue-400">
                        <Filter className="h-4 w-4 mr-1 inline" />
                        Showing {getSelectedCount()} selected strategies
                      </span>
                      <button
                        onClick={clearAllSelections}
                        className="text-sm text-slate-400 hover:text-white transition-colors"
                      >
                        Show All Strategies
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}