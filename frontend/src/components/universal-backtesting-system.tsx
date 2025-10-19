'use client';

import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, BarChart3, Target, Clock, DollarSign, Zap, Crown, Medal, Award, Filter, Download, Play, Settings, RefreshCw, AlertCircle, CheckCircle, Brain, Lightbulb } from 'lucide-react';
import Link from 'next/link';

interface AssetClass {
  id: string;
  name: string;
  type: 'stocks' | 'etfs' | 'options' | 'futures' | 'crypto';
  icon: string;
  color: string;
  examples: string[];
  availableStrategies: string[];
}

interface Timeframe {
  id: string;
  name: string;
  duration: string;
  suitableFor: string[];
  color: string;
}

interface StrategyRecommendation {
  strategy: string;
  confidence: number;
  expectedReturn: number;
  riskLevel: 'low' | 'medium' | 'high';
  timeHorizon: string;
  reasoning: string[];
  historicalPerformance: {
    winRate: number;
    avgReturn: number;
    maxDrawdown: number;
    sharpeRatio: number;
  };
}

interface BacktestConfig {
  assetClass: string;
  timeframe: string;
  strategies: string[];
  startDate: string;
  endDate: string;
  initialCapital: number;
}

interface AssetSpecificResult {
  asset: string;
  performance: {
    totalReturn: number;
    annualizedReturn: number;
    volatility: number;
    sharpeRatio: number;
    maxDrawdown: number;
    winRate: number;
    totalTrades: number;
  };
  bestTimeframes: string[];
  recommendedStrategies: StrategyRecommendation[];
}

const ASSET_CLASSES: AssetClass[] = [
  {
    id: 'stocks',
    name: 'Individual Stocks',
    type: 'stocks',
    icon: '📈',
    color: 'bg-blue-600',
    examples: ['RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK'],
    availableStrategies: ['momentum', 'mean_reversion', 'breakout', 'swing_trading', 'position_trading']
  },
  {
    id: 'etfs',
    name: 'ETFs & Index Funds',
    type: 'etfs',
    icon: '🏛️',
    color: 'bg-green-600',
    examples: ['NIFTYBEES', 'BANKBEES', 'GOLDBEES', 'LIQUIDBEES', 'JUNIORBEES'],
    availableStrategies: ['trend_following', 'sector_rotation', 'momentum', 'dollar_cost_averaging']
  },
  {
    id: 'options',
    name: 'Options Strategies',
    type: 'options',
    icon: '⚡',
    color: 'bg-purple-600',
    examples: ['Straddle', 'Strangle', 'Iron Condor', 'Covered Call', 'Protective Put'],
    availableStrategies: ['volatility_trading', 'income_generation', 'hedging', 'speculation']
  },
  {
    id: 'futures',
    name: 'Futures Contracts',
    type: 'futures',
    icon: '🔮',
    color: 'bg-orange-600',
    examples: ['NIFTY FUT', 'BANKNIFTY FUT', 'CRUDEOIL', 'GOLD', 'SILVER'],
    availableStrategies: ['trend_following', 'arbitrage', 'hedging', 'momentum']
  },
  {
    id: 'crypto',
    name: 'Cryptocurrencies',
    type: 'crypto',
    icon: '₿',
    color: 'bg-yellow-600',
    examples: ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'DOT/USDT'],
    availableStrategies: ['grid_trading', 'dca', 'momentum', 'arbitrage', 'swing_trading']
  }
];

const TIMEFRAMES: Timeframe[] = [
  {
    id: '1m',
    name: '1 Minute',
    duration: '1min',
    suitableFor: ['scalping', 'high_frequency'],
    color: 'bg-red-500'
  },
  {
    id: '5m',
    name: '5 Minutes',
    duration: '5min',
    suitableFor: ['scalping', 'day_trading'],
    color: 'bg-orange-500'
  },
  {
    id: '15m',
    name: '15 Minutes',
    duration: '15min',
    suitableFor: ['day_trading', 'intraday'],
    color: 'bg-yellow-500'
  },
  {
    id: '1h',
    name: '1 Hour',
    duration: '1hour',
    suitableFor: ['swing_trading', 'day_trading'],
    color: 'bg-green-500'
  },
  {
    id: '4h',
    name: '4 Hours',
    duration: '4hour',
    suitableFor: ['swing_trading', 'position_trading'],
    color: 'bg-blue-500'
  },
  {
    id: '1d',
    name: '1 Day',
    duration: '1day',
    suitableFor: ['position_trading', 'investment'],
    color: 'bg-purple-500'
  },
  {
    id: '1w',
    name: '1 Week',
    duration: '1week',
    suitableFor: ['long_term', 'investment'],
    color: 'bg-indigo-500'
  }
];

const STRATEGY_DEFINITIONS = {
  momentum: 'Trend-following strategy that buys assets moving upward',
  mean_reversion: 'Strategy that bets on price returning to average',
  breakout: 'Trades on price breaking key support/resistance levels',
  swing_trading: 'Holds positions for days to weeks',
  position_trading: 'Long-term strategy holding for months',
  trend_following: 'Follows major market trends',
  sector_rotation: 'Rotates between different market sectors',
  dollar_cost_averaging: 'Regular fixed-amount investments',
  volatility_trading: 'Profits from volatility changes',
  income_generation: 'Focused on generating regular income',
  hedging: 'Protects against adverse price movements',
  speculation: 'High-risk, high-reward directional bets',
  arbitrage: 'Profits from price differences across markets',
  grid_trading: 'Places buy/sell orders at regular intervals',
  dca: 'Dollar Cost Averaging with regular purchases',
  high_frequency: 'Very short-term, algorithm-driven trades',
  scalping: 'Many small profits throughout the day'
};

export function UniversalBacktestingSystem() {
  const [selectedAssetClass, setSelectedAssetClass] = useState<string>('stocks');
  const [selectedTimeframe, setSelectedTimeframe] = useState<string>('1d');
  const [selectedStrategies, setSelectedStrategies] = useState<string[]>([]);
  const [backtestConfig, setBacktestConfig] = useState<BacktestConfig>({
    assetClass: 'stocks',
    timeframe: '1d',
    strategies: [],
    startDate: '2024-01-01',
    endDate: '2025-10-20',
    initialCapital: 1000000
  });
  const [recommendations, setRecommendations] = useState<StrategyRecommendation[]>([]);
  const [results, setResults] = useState<AssetSpecificResult[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [showRecommendations, setShowRecommendations] = useState(true);

  const selectedAsset = ASSET_CLASSES.find(a => a.id === selectedAssetClass);
  const selectedTimeframeData = TIMEFRAMES.find(t => t.id === selectedTimeframe);

  // Generate strategy recommendations based on asset class and timeframe
  useEffect(() => {
    generateRecommendations();
  }, [selectedAssetClass, selectedTimeframe]);

  const generateRecommendations = () => {
    const asset = ASSET_CLASSES.find(a => a.id === selectedAssetClass);
    const timeframe = TIMEFRAMES.find(t => t.id === selectedTimeframe);
    
    if (!asset || !timeframe) return;

    // Generate recommendations based on asset type and timeframe
    const recommendations: StrategyRecommendation[] = [];

    asset.availableStrategies.forEach((strategy, index) => {
      const confidence = 60 + Math.random() * 35; // 60-95% confidence
      const expectedReturn = (Math.random() * 40 - 10); // -10% to 30%
      const riskLevel = confidence > 80 ? 'low' : confidence > 65 ? 'medium' : 'high';
      
      let reasoning = [];
      
      // Asset-specific reasoning
      if (selectedAssetClass === 'stocks') {
        reasoning.push('Individual stocks offer good liquidity for this strategy');
        reasoning.push('Historical volatility patterns support this approach');
      } else if (selectedAssetClass === 'etfs') {
        reasoning.push('ETFs provide diversification reducing strategy risk');
        reasoning.push('Lower management fees improve net returns');
      } else if (selectedAssetClass === 'options') {
        reasoning.push('Options premium decay creates income opportunities');
        reasoning.push('Implied volatility patterns favor this strategy');
      } else if (selectedAssetClass === 'crypto') {
        reasoning.push('High volatility in crypto markets suits this strategy');
        reasoning.push('24/7 trading allows for continuous strategy execution');
      }

      // Timeframe-specific reasoning
      if (selectedTimeframe === '1m' || selectedTimeframe === '5m') {
        reasoning.push('Short timeframes provide multiple entry opportunities');
        reasoning.push('Quick profit-taking reduces overnight risk');
      } else if (selectedTimeframe === '1d' || selectedTimeframe === '1w') {
        reasoning.push('Longer timeframes reduce noise and false signals');
        reasoning.push('Position holding allows for trend development');
      }

      recommendations.push({
        strategy,
        confidence: Math.round(confidence),
        expectedReturn: Math.round(expectedReturn * 100) / 100,
        riskLevel: riskLevel as 'low' | 'medium' | 'high',
        timeHorizon: timeframe.duration,
        reasoning,
        historicalPerformance: {
          winRate: 0.45 + Math.random() * 0.3, // 45-75%
          avgReturn: expectedReturn,
          maxDrawdown: -(Math.random() * 15 + 5), // -5% to -20%
          sharpeRatio: Math.random() * 2 + 0.5 // 0.5 to 2.5
        }
      });
    });

    // Sort by confidence
    recommendations.sort((a, b) => b.confidence - a.confidence);
    setRecommendations(recommendations);
  };

  const runBacktest = async () => {
    setIsRunning(true);
    
    // Simulate backtest execution
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Generate sample results for different assets
    const sampleResults: AssetSpecificResult[] = selectedAsset?.examples.map(asset => ({
      asset,
      performance: {
        totalReturn: (Math.random() * 60 - 20), // -20% to 40%
        annualizedReturn: (Math.random() * 25 - 5), // -5% to 20%
        volatility: Math.random() * 30 + 10, // 10% to 40%
        sharpeRatio: Math.random() * 2 + 0.2, // 0.2 to 2.2
        maxDrawdown: -(Math.random() * 25 + 5), // -5% to -30%
        winRate: 0.4 + Math.random() * 0.4, // 40% to 80%
        totalTrades: Math.floor(Math.random() * 200 + 50) // 50 to 250 trades
      },
      bestTimeframes: TIMEFRAMES.slice(0, 3).map(t => t.name),
      recommendedStrategies: recommendations.slice(0, 2)
    })) || [];

    setResults(sampleResults);
    setIsRunning(false);
  };

  const toggleStrategy = (strategy: string) => {
    setSelectedStrategies(prev => 
      prev.includes(strategy) 
        ? prev.filter(s => s !== strategy)
        : [...prev, strategy]
    );
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'text-green-400 bg-green-500/10';
      case 'medium': return 'text-yellow-400 bg-yellow-500/10';
      case 'high': return 'text-red-400 bg-red-500/10';
      default: return 'text-slate-400 bg-slate-500/10';
    }
  };

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'percent',
      minimumFractionDigits: 1,
      maximumFractionDigits: 2
    }).format(num / 100);
  };

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
            <span className="text-white">Universal Backtesting</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
                Universal Asset & Timeframe Backtesting
              </h1>
              <p className="text-slate-400">
                Discover the best strategies for any asset class and timeframe with AI-powered recommendations
              </p>
            </div>
            
            <div className="flex items-center gap-4">
              <button
                onClick={() => setShowRecommendations(!showRecommendations)}
                className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
                  showRecommendations ? 'bg-purple-600 hover:bg-purple-700' : 'bg-slate-700 hover:bg-slate-600'
                }`}
              >
                <Brain className="h-4 w-4 mr-2" />
                AI Recommendations
              </button>
              <button
                onClick={runBacktest}
                disabled={isRunning || selectedStrategies.length === 0}
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
            </div>
          </div>

          {/* Configuration Panel */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {/* Asset Class Selection */}
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <h2 className="text-xl font-bold text-white mb-4 flex items-center">
                <Target className="h-5 w-5 mr-2 text-blue-400" />
                Asset Class Selection
              </h2>
              <div className="grid grid-cols-1 gap-3">
                {ASSET_CLASSES.map((asset) => (
                  <button
                    key={asset.id}
                    onClick={() => setSelectedAssetClass(asset.id)}
                    className={`p-4 rounded-xl border-2 text-left transition-all ${
                      selectedAssetClass === asset.id
                        ? 'border-blue-500 bg-blue-500/10'
                        : 'border-slate-700 bg-slate-800 hover:border-slate-600'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">{asset.icon}</span>
                        <div>
                          <h3 className="font-medium text-white">{asset.name}</h3>
                          <p className="text-sm text-slate-400">{asset.availableStrategies.length} strategies available</p>
                        </div>
                      </div>
                      {selectedAssetClass === asset.id && (
                        <CheckCircle className="h-5 w-5 text-blue-400" />
                      )}
                    </div>
                    <div className="text-xs text-slate-400">
                      Examples: {asset.examples.slice(0, 3).join(', ')}
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Timeframe Selection */}
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <h2 className="text-xl font-bold text-white mb-4 flex items-center">
                <Clock className="h-5 w-5 mr-2 text-green-400" />
                Timeframe Selection
              </h2>
              <div className="grid grid-cols-2 gap-3">
                {TIMEFRAMES.map((timeframe) => (
                  <button
                    key={timeframe.id}
                    onClick={() => setSelectedTimeframe(timeframe.id)}
                    className={`p-3 rounded-xl border text-center transition-all ${
                      selectedTimeframe === timeframe.id
                        ? 'border-green-500 bg-green-500/10'
                        : 'border-slate-700 bg-slate-800 hover:border-slate-600'
                    }`}
                  >
                    <div className="font-medium text-white mb-1">{timeframe.name}</div>
                    <div className="text-xs text-slate-400">{timeframe.suitableFor[0]}</div>
                    {selectedTimeframe === timeframe.id && (
                      <CheckCircle className="h-4 w-4 text-green-400 mx-auto mt-2" />
                    )}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* AI Recommendations */}
        {showRecommendations && (
          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800 mb-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-white flex items-center">
                <Lightbulb className="h-5 w-5 mr-2 text-yellow-400" />
                AI-Powered Strategy Recommendations
              </h2>
              <div className="text-sm text-slate-400">
                For {selectedAsset?.name} • {selectedTimeframeData?.name}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {recommendations.map((rec, index) => (
                <div
                  key={index}
                  className={`p-4 rounded-xl border cursor-pointer transition-all ${
                    selectedStrategies.includes(rec.strategy)
                      ? 'border-blue-500 bg-blue-500/10'
                      : 'border-slate-700 bg-slate-800 hover:border-slate-600'
                  }`}
                  onClick={() => toggleStrategy(rec.strategy)}
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-2">
                      {index === 0 && <Crown className="h-4 w-4 text-yellow-400" />}
                      {index === 1 && <Medal className="h-4 w-4 text-gray-400" />}
                      {index === 2 && <Award className="h-4 w-4 text-orange-400" />}
                      <h3 className="font-medium text-white capitalize">
                        {rec.strategy.replace('_', ' ')}
                      </h3>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${getRiskColor(rec.riskLevel)}`}>
                        {rec.riskLevel}
                      </span>
                      <span className="text-sm font-bold text-green-400">
                        {rec.confidence}%
                      </span>
                    </div>
                  </div>

                  <div className="space-y-2 mb-3">
                    <div className="flex justify-between text-sm">
                      <span className="text-slate-400">Expected Return:</span>
                      <span className={`font-medium ${rec.expectedReturn >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {rec.expectedReturn >= 0 ? '+' : ''}{rec.expectedReturn}%
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-slate-400">Win Rate:</span>
                      <span className="text-white">{formatNumber(rec.historicalPerformance.winRate * 100)}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-slate-400">Sharpe Ratio:</span>
                      <span className="text-blue-400">{rec.historicalPerformance.sharpeRatio.toFixed(2)}</span>
                    </div>
                  </div>

                  <div className="text-xs text-slate-400 mb-3">
                    {STRATEGY_DEFINITIONS[rec.strategy as keyof typeof STRATEGY_DEFINITIONS]}
                  </div>

                  <div className="space-y-1">
                    {rec.reasoning.slice(0, 2).map((reason, idx) => (
                      <div key={idx} className="text-xs text-slate-300 flex items-center">
                        <div className="w-1 h-1 bg-blue-400 rounded-full mr-2" />
                        {reason}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {selectedStrategies.length > 0 && (
              <div className="mt-6 p-4 bg-blue-500/10 rounded-lg border border-blue-500/30">
                <div className="flex items-center justify-between">
                  <span className="text-blue-400">
                    <CheckCircle className="h-4 w-4 mr-2 inline" />
                    {selectedStrategies.length} strategies selected for backtesting
                  </span>
                  <button
                    onClick={() => setSelectedStrategies([])}
                    className="text-sm text-slate-400 hover:text-white transition-colors"
                  >
                    Clear Selection
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Backtest Results */}
        {results.length > 0 && (
          <div className="space-y-6">
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                <BarChart3 className="h-5 w-5 mr-2 text-green-400" />
                Backtest Results - {selectedAsset?.name} ({selectedTimeframeData?.name})
              </h2>
              
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-slate-800">
                    <tr>
                      <th className="px-4 py-3 text-left">Asset</th>
                      <th className="px-4 py-3 text-right">Total Return</th>
                      <th className="px-4 py-3 text-right">Annual Return</th>
                      <th className="px-4 py-3 text-right">Volatility</th>
                      <th className="px-4 py-3 text-right">Sharpe Ratio</th>
                      <th className="px-4 py-3 text-right">Max Drawdown</th>
                      <th className="px-4 py-3 text-right">Win Rate</th>
                      <th className="px-4 py-3 text-right">Total Trades</th>
                    </tr>
                  </thead>
                  <tbody>
                    {results.map((result, index) => (
                      <tr key={index} className="border-t border-slate-800 hover:bg-slate-800/50">
                        <td className="px-4 py-3 font-medium text-white">{result.asset}</td>
                        <td className={`px-4 py-3 text-right font-mono font-bold ${
                          result.performance.totalReturn >= 0 ? 'text-green-400' : 'text-red-400'
                        }`}>
                          {formatNumber(result.performance.totalReturn)}
                        </td>
                        <td className={`px-4 py-3 text-right font-mono ${
                          result.performance.annualizedReturn >= 0 ? 'text-green-400' : 'text-red-400'
                        }`}>
                          {formatNumber(result.performance.annualizedReturn)}
                        </td>
                        <td className="px-4 py-3 text-right font-mono text-yellow-400">
                          {formatNumber(result.performance.volatility)}
                        </td>
                        <td className="px-4 py-3 text-right font-mono text-blue-400">
                          {result.performance.sharpeRatio.toFixed(2)}
                        </td>
                        <td className="px-4 py-3 text-right font-mono text-red-400">
                          {formatNumber(result.performance.maxDrawdown)}
                        </td>
                        <td className="px-4 py-3 text-right font-mono text-purple-400">
                          {formatNumber(result.performance.winRate * 100)}
                        </td>
                        <td className="px-4 py-3 text-right font-mono text-slate-300">
                          {result.performance.totalTrades}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Best Performers Summary */}
              <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-slate-800 rounded-xl p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-slate-400">Best Performer</span>
                    <Crown className="h-4 w-4 text-yellow-400" />
                  </div>
                  <div className="text-lg font-bold text-yellow-400">
                    {results.reduce((max, r) => r.performance.totalReturn > max.performance.totalReturn ? r : max).asset}
                  </div>
                  <div className="text-sm text-slate-300">
                    {formatNumber(Math.max(...results.map(r => r.performance.totalReturn)))}
                  </div>
                </div>
                
                <div className="bg-slate-800 rounded-xl p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-slate-400">Best Sharpe Ratio</span>
                    <Target className="h-4 w-4 text-blue-400" />
                  </div>
                  <div className="text-lg font-bold text-blue-400">
                    {results.reduce((max, r) => r.performance.sharpeRatio > max.performance.sharpeRatio ? r : max).asset}
                  </div>
                  <div className="text-sm text-slate-300">
                    {Math.max(...results.map(r => r.performance.sharpeRatio)).toFixed(2)}
                  </div>
                </div>
                
                <div className="bg-slate-800 rounded-xl p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-slate-400">Lowest Drawdown</span>
                    <AlertCircle className="h-4 w-4 text-green-400" />
                  </div>
                  <div className="text-lg font-bold text-green-400">
                    {results.reduce((min, r) => Math.abs(r.performance.maxDrawdown) < Math.abs(min.performance.maxDrawdown) ? r : min).asset}
                  </div>
                  <div className="text-sm text-slate-300">
                    {formatNumber(Math.max(...results.map(r => r.performance.maxDrawdown)))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}