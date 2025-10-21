'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Brain, TrendingUp, BarChart3, Target, Zap, Activity, Eye, Play, Pause, Upload, Shield } from 'lucide-react';

interface Strategy {
  id: string;
  name: string;
  description: string;
  type: 'momentum' | 'reversal' | 'arbitrage' | 'mean_reversion' | 'breakout';
  timeframe: string;
  winRate: number;
  avgReturn: number;
  maxDrawdown: number;
  sharpeRatio: number;
  totalTrades: number;
  profitFactor: number;
  status: 'active' | 'paused' | 'backtesting';
  risk: 'low' | 'medium' | 'high';
  aiScore: number;
  signals: Signal[];
}

interface Signal {
  id: string;
  symbol: string;
  action: 'buy' | 'sell' | 'hold';
  confidence: number;
  price: number;
  target: number;
  stopLoss: number;
  reason: string;
  timestamp: string;
}

interface AIAnalysis {
  marketTrend: 'bullish' | 'bearish' | 'neutral';
  sentiment: number;
  volatility: 'low' | 'medium' | 'high';
  recommendations: string[];
  riskFactors: string[];
  opportunities: string[];
}

const sampleStrategies: Strategy[] = [
  {
    id: '1',
    name: 'Momentum Alpha',
    description: 'AI-powered momentum strategy using technical indicators and market sentiment',
    type: 'momentum',
    timeframe: '1H',
    winRate: 68.5,
    avgReturn: 2.4,
    maxDrawdown: 8.2,
    sharpeRatio: 1.8,
    totalTrades: 342,
    profitFactor: 2.1,
    status: 'active',
    risk: 'medium',
    aiScore: 85,
    signals: [
      {
        id: '1',
        symbol: 'BTC/USDT',
        action: 'buy',
        confidence: 87,
        price: 43250,
        target: 45100,
        stopLoss: 42000,
        reason: 'Strong momentum with bullish AI sentiment',
        timestamp: new Date().toISOString()
      }
    ]
  },
  {
    id: '2',
    name: 'Volatility Arbitrage',
    description: 'Exploits volatility discrepancies across different market segments',
    type: 'arbitrage',
    timeframe: '5M',
    winRate: 72.1,
    avgReturn: 1.8,
    maxDrawdown: 5.6,
    sharpeRatio: 2.3,
    totalTrades: 892,
    profitFactor: 2.5,
    status: 'active',
    risk: 'low',
    aiScore: 92,
    signals: [
      {
        id: '2',
        symbol: 'ETH/USDT',
        action: 'sell',
        confidence: 78,
        price: 2650,
        target: 2550,
        stopLoss: 2720,
        reason: 'High IV with unusual put activity',
        timestamp: new Date().toISOString()
      }
    ]
  }
];

const sampleAIAnalysis: AIAnalysis = {
  marketTrend: 'bullish',
  sentiment: 72,
  volatility: 'medium',
  recommendations: [
    'Focus on momentum strategies in current bull market',
    'Consider reducing position sizes due to elevated volatility',
    'Monitor DeFi sector for potential breakout opportunities',
    'Implement hedging strategies for crypto positions'
  ],
  riskFactors: [
    'High correlation between major cryptocurrencies',
    'Elevated volatility in altcoin markets',
    'Regulatory news affecting market sentiment',
    'Options expiry this week may increase volatility'
  ],
  opportunities: [
    'Strong momentum in Layer 1 blockchain tokens',
    'Oversold conditions in DeFi protocols',
    'Unusual activity in memecoin sector',
    'Divergence signals in AI/ML crypto tokens'
  ]
};

export default function AIStrategyAnalyzer() {
  const [strategies, setStrategies] = useState<Strategy[]>(sampleStrategies);
  const [selectedStrategy, setSelectedStrategy] = useState<Strategy | null>(null);
  const [aiAnalysis] = useState<AIAnalysis>(sampleAIAnalysis);
  const [selectedView, setSelectedView] = useState<'strategies' | 'signals' | 'analysis'>('strategies');
  const [showCredentialsModal, setShowCredentialsModal] = useState(false);

  const getStrategyTypeColor = (type: Strategy['type']) => {
    switch (type) {
      case 'momentum': return 'text-blue-400 bg-blue-900/30 border-blue-700';
      case 'reversal': return 'text-purple-400 bg-purple-900/30 border-purple-700';
      case 'arbitrage': return 'text-green-400 bg-green-900/30 border-green-700';
      case 'mean_reversion': return 'text-yellow-400 bg-yellow-900/30 border-yellow-700';
      case 'breakout': return 'text-red-400 bg-red-900/30 border-red-700';
    }
  };

  const getRiskColor = (risk: Strategy['risk']) => {
    switch (risk) {
      case 'low': return 'text-green-400 bg-green-900/30 border-green-700';
      case 'medium': return 'text-yellow-400 bg-yellow-900/30 border-yellow-700';
      case 'high': return 'text-red-400 bg-red-900/30 border-red-700';
    }
  };

  const getActionColor = (action: Signal['action']) => {
    switch (action) {
      case 'buy': return 'text-green-400 bg-green-900/30 border-green-700';
      case 'sell': return 'text-red-400 bg-red-900/30 border-red-700';
      case 'hold': return 'text-yellow-400 bg-yellow-900/30 border-yellow-700';
    }
  };

  const toggleStrategyStatus = (strategyId: string) => {
    setStrategies(prev => prev.map(strategy => 
      strategy.id === strategyId 
        ? { 
            ...strategy, 
            status: strategy.status === 'active' ? 'paused' : 'active' 
          }
        : strategy
    ));
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4">
      <div className="max-w-7xl mx-auto">
        {/* Breadcrumb */}
        <div className="mb-6">
          <nav className="flex items-center space-x-2 text-sm text-slate-400">
            <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
            <span>/</span>
            <Link href="/ai" className="hover:text-blue-400 transition-colors">AI</Link>
            <span>/</span>
            <span className="text-white">Strategy Analyzer</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-4">
            <Brain className="h-8 w-8 text-purple-400" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
              AI Strategy Analyzer
            </h1>
          </div>
          <p className="text-xl text-slate-300">
            Advanced AI-powered strategy analysis and signal generation
          </p>
        </div>

        {/* Market Overview */}
        <div className="mb-6 bg-slate-900 rounded-2xl p-6 border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-bold text-white">AI Market Analysis</h3>
            <div className="flex items-center space-x-2">
              <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                aiAnalysis.marketTrend === 'bullish' ? 'text-green-400 bg-green-900/30' :
                aiAnalysis.marketTrend === 'bearish' ? 'text-red-400 bg-red-900/30' :
                'text-yellow-400 bg-yellow-900/30'
              }`}>
                {aiAnalysis.marketTrend.toUpperCase()}
              </div>
              <div className="text-slate-400">•</div>
              <div className="text-white font-mono">{aiAnalysis.sentiment}% Sentiment</div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <div className="text-slate-400 text-sm mb-2">Active Strategies</div>
              <div className="text-2xl font-bold text-white">
                {strategies.filter(s => s.status === 'active').length}
              </div>
              <div className="text-green-400 text-sm">
                +{strategies.filter(s => s.avgReturn > 0).length} profitable
              </div>
            </div>
            <div>
              <div className="text-slate-400 text-sm mb-2">Active Signals</div>
              <div className="text-2xl font-bold text-blue-400">
                {strategies.reduce((sum, s) => sum + s.signals.length, 0)}
              </div>
              <div className="text-blue-400 text-sm">
                {strategies.filter(s => s.signals.some(signal => signal.confidence > 80)).length} high confidence
              </div>
            </div>
            <div>
              <div className="text-slate-400 text-sm mb-2">Average Return</div>
              <div className="text-2xl font-bold text-green-400">
                +{(strategies.reduce((sum, s) => sum + s.avgReturn, 0) / strategies.length).toFixed(1)}%
              </div>
              <div className="text-green-400 text-sm">per strategy</div>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="mb-6">
          <div className="flex space-x-1 bg-slate-900 rounded-lg p-1 border border-slate-800">
            {[
              { id: 'strategies', label: 'Strategies', icon: Target },
              { id: 'signals', label: 'Live Signals', icon: Zap },
              { id: 'analysis', label: 'AI Analysis', icon: Brain }
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setSelectedView(tab.id as any)}
                  className={`flex items-center px-4 py-2 rounded-md font-medium transition-colors ${
                    selectedView === tab.id
                      ? 'bg-purple-600 text-white'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  <Icon className="h-4 w-4 mr-2" />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* Strategies View */}
        {selectedView === 'strategies' && (
          <div className="space-y-6">
            {/* PineScript Upload Section */}
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <div className="flex items-center space-x-3 mb-4">
                <div className="bg-green-500/20 p-2 rounded-lg">
                  <Upload className="h-5 w-5 text-green-400" />
                </div>
                <h3 className="text-xl font-bold text-white">Upload PineScript Strategy</h3>
              </div>
              
              <p className="text-slate-400 mb-6">
                Upload your custom PineScript strategies for backtesting and live trading. 
                Supports TradingView Pine Script v5 syntax.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* File Upload */}
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      PineScript File (.pine)
                    </label>
                    <div className="border-2 border-dashed border-slate-700 rounded-lg p-8 text-center hover:border-green-500 transition-colors cursor-pointer">
                      <div className="flex flex-col items-center">
                        <div className="bg-green-500/20 p-3 rounded-full mb-3">
                          <Upload className="h-6 w-6 text-green-400" />
                        </div>
                        <p className="text-slate-300 font-medium mb-1">Click to upload PineScript</p>
                        <p className="text-slate-500 text-sm">or drag and drop .pine files</p>
                      </div>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      Strategy Name
                    </label>
                    <input
                      type="text"
                      placeholder="My Custom Strategy"
                      className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:border-green-500 focus:outline-none"
                    />
                  </div>
                </div>

                {/* Trading Options */}
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      Trading Mode
                    </label>
                    <div className="grid grid-cols-3 gap-2">
                      <button className="px-4 py-2 bg-blue-600 text-white rounded-lg font-medium text-sm">
                        Backtest
                      </button>
                      <button className="px-4 py-2 bg-slate-700 text-slate-300 rounded-lg font-medium text-sm hover:bg-slate-600">
                        Paper Trade
                      </button>
                      <button 
                        onClick={() => setShowCredentialsModal(true)}
                        className="px-4 py-2 bg-red-700 text-white rounded-lg font-medium text-sm hover:bg-red-600"
                      >
                        Live Trade
                      </button>
                    </div>
                    <p className="text-xs text-slate-500 mt-2">
                      * Live trading requires API credentials
                    </p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      Timeframe
                    </label>
                    <select className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:border-green-500 focus:outline-none">
                      <option>1m</option>
                      <option>5m</option>
                      <option>15m</option>
                      <option>1h</option>
                      <option>4h</option>
                      <option>1d</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      Initial Capital
                    </label>
                    <input
                      type="number"
                      placeholder="10000"
                      className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:border-green-500 focus:outline-none"
                    />
                  </div>

                  <button className="w-full bg-gradient-to-r from-green-600 to-blue-600 text-white font-bold py-3 rounded-lg hover:from-green-700 hover:to-blue-700 transition-all">
                    Deploy Strategy
                  </button>
                </div>
              </div>

              {/* Authentication Info */}
              <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 pt-6 border-t border-slate-800">
                <div className="flex items-center space-x-3">
                  <div className="bg-green-500/20 p-1 rounded">
                    <Target className="h-4 w-4 text-green-400" />
                  </div>
                  <span className="text-slate-300 text-sm">Backtest: No credentials needed</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="bg-blue-500/20 p-1 rounded">
                    <BarChart3 className="h-4 w-4 text-blue-400" />
                  </div>
                  <span className="text-slate-300 text-sm">Paper: No credentials needed</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="bg-red-500/20 p-1 rounded">
                    <Shield className="h-4 w-4 text-red-400" />
                  </div>
                  <span className="text-slate-300 text-sm">Live: API credentials required</span>
                </div>
              </div>
            </div>

            {/* Strategy List */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 space-y-4">
                {strategies.map((strategy) => (
                  <div 
                    key={strategy.id}
                    className={`bg-slate-900 rounded-2xl p-6 border cursor-pointer transition-all ${
                      selectedStrategy?.id === strategy.id 
                        ? 'border-purple-500 bg-purple-900/10' 
                        : 'border-slate-800 hover:border-slate-700'
                    }`}
                    onClick={() => setSelectedStrategy(strategy)}
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <h3 className="text-xl font-bold text-white mb-2">{strategy.name}</h3>
                        <p className="text-slate-400 text-sm">{strategy.description}</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 rounded text-xs ${getStrategyTypeColor(strategy.type)} border`}>
                          {strategy.type.replace('_', ' ').toUpperCase()}
                        </span>
                        <span className={`px-2 py-1 rounded text-xs ${getRiskColor(strategy.risk)} border`}>
                          {strategy.risk.toUpperCase()}
                        </span>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                      <div>
                        <div className="text-slate-400 text-xs">Win Rate</div>
                        <div className="text-green-400 font-bold">{strategy.winRate}%</div>
                      </div>
                      <div>
                        <div className="text-slate-400 text-xs">Avg Return</div>
                        <div className="text-blue-400 font-bold">+{strategy.avgReturn}%</div>
                      </div>
                      <div>
                        <div className="text-slate-400 text-xs">Sharpe</div>
                        <div className="text-purple-400 font-bold">{strategy.sharpeRatio}</div>
                      </div>
                      <div>
                        <div className="text-slate-400 text-xs">AI Score</div>
                        <div className="text-yellow-400 font-bold">{strategy.aiScore}</div>
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          strategy.status === 'active' ? 'bg-green-900/30 text-green-400' :
                          strategy.status === 'paused' ? 'bg-yellow-900/30 text-yellow-400' :
                          'bg-blue-900/30 text-blue-400'
                        }`}>
                          {strategy.status.toUpperCase()}
                        </span>
                        <span className="text-slate-400 text-sm">{strategy.timeframe}</span>
                        <span className="text-slate-400 text-sm">{strategy.totalTrades} trades</span>
                      </div>
                      
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          toggleStrategyStatus(strategy.id);
                        }}
                        className="flex items-center px-3 py-1 rounded bg-slate-800 text-slate-300 hover:bg-slate-700 transition-colors"
                      >
                        {strategy.status === 'active' ? (
                          <>
                            <Pause className="h-3 w-3 mr-1" />
                            Pause
                          </>
                        ) : (
                          <>
                            <Play className="h-3 w-3 mr-1" />
                            Start
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              {/* Strategy Details */}
              <div className="lg:col-span-1">
                {selectedStrategy ? (
                  <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800 sticky top-4">
                    <h3 className="text-lg font-bold text-white mb-4">Strategy Details</h3>
                    
                    <div className="space-y-4">
                      <div>
                        <div className="text-slate-400 text-sm mb-1">Performance</div>
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <span className="text-slate-300">Win Rate</span>
                            <span className="text-green-400">{selectedStrategy.winRate}%</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-300">Avg Return</span>
                            <span className="text-blue-400">+{selectedStrategy.avgReturn}%</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-300">Max Drawdown</span>
                            <span className="text-red-400">-{selectedStrategy.maxDrawdown}%</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-300">Sharpe Ratio</span>
                            <span className="text-purple-400">{selectedStrategy.sharpeRatio}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-300">Profit Factor</span>
                            <span className="text-yellow-400">{selectedStrategy.profitFactor}</span>
                          </div>
                        </div>
                      </div>

                      {selectedStrategy.signals.length > 0 && (
                        <div>
                          <div className="text-slate-400 text-sm mb-2">Active Signals</div>
                          <div className="space-y-2">
                            {selectedStrategy.signals.map((signal) => (
                              <div key={signal.id} className="bg-slate-800 rounded-lg p-3">
                                <div className="flex items-center justify-between mb-2">
                                  <span className="font-medium text-white">{signal.symbol}</span>
                                  <span className={`px-2 py-1 rounded text-xs ${getActionColor(signal.action)}`}>
                                    {signal.action.toUpperCase()}
                                  </span>
                                </div>
                                <div className="text-sm text-slate-400 mb-1">
                                  Confidence: {signal.confidence}%
                                </div>
                                <div className="text-xs text-slate-500">
                                  {signal.reason}
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ) : (
                  <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800 text-center">
                    <Brain className="h-12 w-12 mx-auto mb-4 opacity-50 text-slate-400" />
                    <p className="text-slate-400">Select a strategy to view details</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Live Signals View */}
        {selectedView === 'signals' && (
          <div className="space-y-6">
            {strategies.filter(s => s.signals.length > 0).map((strategy) => (
              <div key={strategy.id} className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden">
                <div className="p-4 border-b border-slate-800 bg-slate-800/50">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-bold text-white">{strategy.name}</h3>
                    <div className="flex items-center space-x-2">
                      <span className={`px-2 py-1 rounded text-xs ${getStrategyTypeColor(strategy.type)} border`}>
                        {strategy.type.replace('_', ' ').toUpperCase()}
                      </span>
                      <span className="text-purple-400 font-mono">AI Score: {strategy.aiScore}</span>
                    </div>
                  </div>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-slate-800">
                      <tr className="text-xs text-slate-300">
                        <th className="px-4 py-3 text-left">Symbol</th>
                        <th className="px-4 py-3 text-center">Action</th>
                        <th className="px-4 py-3 text-right">Price</th>
                        <th className="px-4 py-3 text-right">Target</th>
                        <th className="px-4 py-3 text-right">Stop Loss</th>
                        <th className="px-4 py-3 text-center">Confidence</th>
                        <th className="px-4 py-3 text-left">Reason</th>
                      </tr>
                    </thead>
                    <tbody>
                      {strategy.signals.map((signal) => (
                        <tr key={signal.id} className="border-t border-slate-800 hover:bg-slate-800/30">
                          <td className="px-4 py-4">
                            <div className="font-medium text-white">{signal.symbol}</div>
                          </td>
                          <td className="px-4 py-4 text-center">
                            <span className={`px-2 py-1 rounded text-xs font-medium ${getActionColor(signal.action)}`}>
                              {signal.action.toUpperCase()}
                            </span>
                          </td>
                          <td className="px-4 py-4 text-right font-mono text-white">
                            ${signal.price.toLocaleString()}
                          </td>
                          <td className="px-4 py-4 text-right font-mono text-green-400">
                            ${signal.target.toLocaleString()}
                          </td>
                          <td className="px-4 py-4 text-right font-mono text-red-400">
                            ${signal.stopLoss.toLocaleString()}
                          </td>
                          <td className="px-4 py-4 text-center">
                            <div className="flex items-center justify-center">
                              <div className="w-12 bg-slate-700 rounded-full h-2 mr-2">
                                <div 
                                  className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
                                  style={{ width: `${signal.confidence}%` }}
                                />
                              </div>
                              <span className="text-xs text-slate-300">{signal.confidence}%</span>
                            </div>
                          </td>
                          <td className="px-4 py-4 text-slate-300 text-sm">
                            {signal.reason}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* AI Analysis View */}
        {selectedView === 'analysis' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              {/* Recommendations */}
              <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <h3 className="text-lg font-bold text-green-400 mb-4">AI Recommendations</h3>
                <div className="space-y-3">
                  {aiAnalysis.recommendations.map((rec, index) => (
                    <div key={index} className="flex items-start space-x-3">
                      <div className="bg-green-500/20 rounded-full p-1 mt-1">
                        <div className="w-2 h-2 bg-green-400 rounded-full" />
                      </div>
                      <p className="text-slate-300">{rec}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Risk Factors */}
              <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <h3 className="text-lg font-bold text-red-400 mb-4">Risk Factors</h3>
                <div className="space-y-3">
                  {aiAnalysis.riskFactors.map((risk, index) => (
                    <div key={index} className="flex items-start space-x-3">
                      <div className="bg-red-500/20 rounded-full p-1 mt-1">
                        <div className="w-2 h-2 bg-red-400 rounded-full" />
                      </div>
                      <p className="text-slate-300">{risk}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="space-y-6">
              {/* Market Sentiment */}
              <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <h3 className="text-lg font-bold text-white mb-4">Market Sentiment</h3>
                <div className="text-center mb-4">
                  <div className="text-3xl font-bold text-blue-400 mb-2">{aiAnalysis.sentiment}%</div>
                  <div className="w-full bg-slate-800 rounded-full h-3">
                    <div 
                      className="bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 h-3 rounded-full transition-all duration-300"
                      style={{ width: `${aiAnalysis.sentiment}%` }}
                    />
                  </div>
                  <div className="flex justify-between text-xs text-slate-400 mt-2">
                    <span>Bearish</span>
                    <span>Neutral</span>
                    <span>Bullish</span>
                  </div>
                </div>
              </div>

              {/* Opportunities */}
              <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <h3 className="text-lg font-bold text-yellow-400 mb-4">Opportunities</h3>
                <div className="space-y-3">
                  {aiAnalysis.opportunities.slice(0, 3).map((opp, index) => (
                    <div key={index} className="flex items-start space-x-3">
                      <div className="bg-yellow-500/20 rounded-full p-1 mt-1">
                        <div className="w-2 h-2 bg-yellow-400 rounded-full" />
                      </div>
                      <p className="text-slate-300 text-sm">{opp}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Credentials Modal */}
        {showCredentialsModal && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-slate-900 rounded-xl p-6 border border-slate-800 max-w-md w-full mx-4">
              <div className="flex items-center space-x-3 mb-4">
                <Shield className="h-6 w-6 text-red-400" />
                <h3 className="text-lg font-bold text-white">Live Trading Credentials Required</h3>
              </div>
              
              <p className="text-slate-300 mb-6">
                To enable live trading, you need to configure your exchange API credentials. 
                This is required for executing real trades with your account.
              </p>

              <div className="flex space-x-3">
                <Link 
                  href="/settings/exchanges"
                  className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg font-medium text-center hover:bg-blue-700 transition-colors"
                >
                  Configure API Keys
                </Link>
                <button
                  onClick={() => setShowCredentialsModal(false)}
                  className="flex-1 bg-slate-700 text-slate-300 px-4 py-2 rounded-lg font-medium hover:bg-slate-600 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}