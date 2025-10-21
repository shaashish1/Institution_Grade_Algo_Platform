'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Brain, TrendingUp, TrendingDown, Activity, BarChart3, PieChart, Eye, Zap, AlertTriangle } from 'lucide-react';

interface MarketData {
  symbol: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
  marketCap?: number;
  sector: string;
  aiSignal: 'bullish' | 'bearish' | 'neutral';
  confidence: number;
}

interface SectorAnalysis {
  sector: string;
  performance: number;
  trend: 'bullish' | 'bearish' | 'neutral';
  topStocks: string[];
  sentiment: number;
  aiRecommendation: string;
}

interface AIInsights {
  marketTrend: 'bullish' | 'bearish' | 'neutral';
  sentiment: number;
  volatility: 'low' | 'medium' | 'high';
  keyEvents: string[];
  technicalSignals: {
    signal: string;
    strength: number;
    description: string;
  }[];
  predictions: {
    timeframe: string;
    direction: 'up' | 'down' | 'sideways';
    confidence: number;
    targets: number[];
  }[];
}

const sampleMarketData: MarketData[] = [
  {
    symbol: 'NIFTY 50',
    price: 26247.50,
    change: 185.30,
    changePercent: 0.71,
    volume: 125000000,
    sector: 'Index',
    aiSignal: 'bullish',
    confidence: 78
  },
  {
    symbol: 'RELIANCE',
    price: 2789.45,
    change: 23.85,
    changePercent: 0.86,
    volume: 8500000,
    marketCap: 1885000000000,
    sector: 'Energy',
    aiSignal: 'bullish',
    confidence: 82
  },
  {
    symbol: 'TCS',
    price: 4123.20,
    change: -12.45,
    changePercent: -0.30,
    volume: 3200000,
    marketCap: 1505000000000,
    sector: 'IT',
    aiSignal: 'neutral',
    confidence: 65
  },
  {
    symbol: 'HDFC BANK',
    price: 1875.60,
    change: 8.90,
    changePercent: 0.48,
    volume: 12000000,
    marketCap: 1425000000000,
    sector: 'Banking',
    aiSignal: 'bullish',
    confidence: 75
  },
  {
    symbol: 'INFY',
    price: 1956.30,
    change: -5.70,
    changePercent: -0.29,
    volume: 6800000,
    marketCap: 805000000000,
    sector: 'IT',
    aiSignal: 'bearish',
    confidence: 68
  }
];

const sampleSectorAnalysis: SectorAnalysis[] = [
  {
    sector: 'Banking',
    performance: 1.2,
    trend: 'bullish',
    topStocks: ['HDFC BANK', 'ICICI BANK', 'SBI'],
    sentiment: 78,
    aiRecommendation: 'Strong fundamentals with improving credit growth'
  },
  {
    sector: 'IT',
    performance: -0.5,
    trend: 'neutral',
    topStocks: ['TCS', 'INFY', 'WIPRO'],
    sentiment: 62,
    aiRecommendation: 'Mixed signals due to global economic uncertainty'
  },
  {
    sector: 'Energy',
    performance: 2.1,
    trend: 'bullish',
    topStocks: ['RELIANCE', 'ONGC', 'IOC'],
    sentiment: 85,
    aiRecommendation: 'Benefiting from rising oil prices and refining margins'
  },
  {
    sector: 'Pharmaceuticals',
    performance: 0.8,
    trend: 'bullish',
    topStocks: ['SUN PHARMA', 'CIPLA', 'DR REDDY'],
    sentiment: 71,
    aiRecommendation: 'Stable growth with export opportunities'
  },
  {
    sector: 'Auto',
    performance: -1.3,
    trend: 'bearish',
    topStocks: ['MARUTI', 'TATA MOTORS', 'M&M'],
    sentiment: 45,
    aiRecommendation: 'Facing headwinds from higher input costs'
  }
];

const sampleAIInsights: AIInsights = {
  marketTrend: 'bullish',
  sentiment: 72,
  volatility: 'medium',
  keyEvents: [
    'RBI policy meeting scheduled for next week',
    'Q3 earnings season begins',
    'Global inflation data due Friday',
    'FII inflows continue positively'
  ],
  technicalSignals: [
    {
      signal: 'Golden Cross Formation',
      strength: 85,
      description: 'NIFTY 50 MA crosses above 200 MA, indicating bullish momentum'
    },
    {
      signal: 'RSI Divergence',
      strength: 72,
      description: 'Banking index showing positive RSI divergence'
    },
    {
      signal: 'Volume Breakout',
      strength: 68,
      description: 'Above average volume in large-cap stocks'
    }
  ],
  predictions: [
    {
      timeframe: '1 Week',
      direction: 'up',
      confidence: 78,
      targets: [26500, 26800]
    },
    {
      timeframe: '1 Month',
      direction: 'up',
      confidence: 65,
      targets: [27000, 27500]
    },
    {
      timeframe: '3 Months',
      direction: 'sideways',
      confidence: 55,
      targets: [25500, 28000]
    }
  ]
};

export default function AIMarketAnalysis() {
  const [marketData, setMarketData] = useState<MarketData[]>(sampleMarketData);
  const [sectorAnalysis, setSectorAnalysis] = useState<SectorAnalysis[]>(sampleSectorAnalysis);
  const [aiInsights, setAIInsights] = useState<AIInsights>(sampleAIInsights);
  const [selectedView, setSelectedView] = useState<'overview' | 'sectors' | 'insights' | 'predictions'>('overview');

  const getSignalColor = (signal: 'bullish' | 'bearish' | 'neutral') => {
    switch (signal) {
      case 'bullish': return 'text-green-400 bg-green-900/30 border-green-700';
      case 'bearish': return 'text-red-400 bg-red-900/30 border-red-700';
      case 'neutral': return 'text-yellow-400 bg-yellow-900/30 border-yellow-700';
    }
  };

  const getTrendColor = (trend: 'bullish' | 'bearish' | 'neutral') => {
    switch (trend) {
      case 'bullish': return 'text-green-400';
      case 'bearish': return 'text-red-400';
      case 'neutral': return 'text-yellow-400';
    }
  };

  const getDirectionIcon = (direction: 'up' | 'down' | 'sideways') => {
    switch (direction) {
      case 'up': return <TrendingUp className="h-4 w-4 text-green-400" />;
      case 'down': return <TrendingDown className="h-4 w-4 text-red-400" />;
      case 'sideways': return <Activity className="h-4 w-4 text-yellow-400" />;
    }
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
            <span className="text-white">Market Analysis</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-4">
            <Brain className="h-8 w-8 text-blue-400" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-green-400 bg-clip-text text-transparent">
              AI Market Analysis
            </h1>
          </div>
          <p className="text-xl text-slate-300">
            Advanced AI-powered market insights and predictions
          </p>
        </div>

        {/* Market Overview Dashboard */}
        <div className="mb-6 bg-slate-900 rounded-2xl p-6 border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-bold text-white">Market Pulse</h3>
            <div className="flex items-center space-x-2">
              <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                aiInsights.marketTrend === 'bullish' ? 'text-green-400 bg-green-900/30' :
                aiInsights.marketTrend === 'bearish' ? 'text-red-400 bg-red-900/30' :
                'text-yellow-400 bg-yellow-900/30'
              }`}>
                {aiInsights.marketTrend.toUpperCase()}
              </div>
              <div className="text-slate-400">•</div>
              <div className="text-white font-mono">{aiInsights.sentiment}% Sentiment</div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div>
              <div className="text-slate-400 text-sm mb-2">NIFTY 50</div>
              <div className="text-2xl font-bold text-white">
                {marketData[0]?.price.toLocaleString()}
              </div>
              <div className={`text-sm ${marketData[0]?.change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                {marketData[0]?.change >= 0 ? '+' : ''}{marketData[0]?.change.toFixed(2)} 
                ({marketData[0]?.changePercent >= 0 ? '+' : ''}{marketData[0]?.changePercent.toFixed(2)}%)
              </div>
            </div>
            <div>
              <div className="text-slate-400 text-sm mb-2">Market Sentiment</div>
              <div className="text-2xl font-bold text-blue-400">{aiInsights.sentiment}%</div>
              <div className="text-blue-400 text-sm">
                {aiInsights.sentiment > 70 ? 'Optimistic' : 
                 aiInsights.sentiment > 50 ? 'Neutral' : 'Pessimistic'}
              </div>
            </div>
            <div>
              <div className="text-slate-400 text-sm mb-2">AI Signals</div>
              <div className="text-2xl font-bold text-green-400">
                {marketData.filter(d => d.aiSignal === 'bullish').length}
              </div>
              <div className="text-green-400 text-sm">Bullish signals</div>
            </div>
            <div>
              <div className="text-slate-400 text-sm mb-2">Volatility</div>
              <div className={`text-2xl font-bold ${
                aiInsights.volatility === 'high' ? 'text-red-400' :
                aiInsights.volatility === 'medium' ? 'text-yellow-400' : 'text-green-400'
              }`}>
                {aiInsights.volatility.toUpperCase()}
              </div>
              <div className="text-slate-400 text-sm">Current level</div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6">
          <div className="flex space-x-1 bg-slate-900 p-1 rounded-lg w-fit">
            {[
              { id: 'overview', label: 'Market Overview', icon: BarChart3 },
              { id: 'sectors', label: 'Sector Analysis', icon: PieChart },
              { id: 'insights', label: 'AI Insights', icon: Brain },
              { id: 'predictions', label: 'Predictions', icon: Eye }
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setSelectedView(tab.id as any)}
                  className={`flex items-center px-4 py-2 rounded-md font-medium transition-colors ${
                    selectedView === tab.id
                      ? 'bg-blue-600 text-white'
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

        {/* Market Overview */}
        {selectedView === 'overview' && (
          <div className="space-y-6">
            {/* Key Market Movers */}
            <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden">
              <div className="p-6 border-b border-slate-800">
                <h2 className="text-xl font-bold text-white">Market Movers & AI Signals</h2>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-slate-800">
                    <tr className="text-xs text-slate-300">
                      <th className="px-4 py-3 text-left">Symbol</th>
                      <th className="px-4 py-3 text-right">Price</th>
                      <th className="px-4 py-3 text-right">Change</th>
                      <th className="px-4 py-3 text-right">Volume</th>
                      <th className="px-4 py-3 text-left">Sector</th>
                      <th className="px-4 py-3 text-center">AI Signal</th>
                      <th className="px-4 py-3 text-center">Confidence</th>
                    </tr>
                  </thead>
                  <tbody>
                    {marketData.map((stock, index) => (
                      <tr key={index} className="border-t border-slate-800 hover:bg-slate-800/30">
                        <td className="px-4 py-4">
                          <div className="font-medium text-white">{stock.symbol}</div>
                          {stock.marketCap && (
                            <div className="text-xs text-slate-400">
                              MCap: ₹{(stock.marketCap / 1000000000000).toFixed(1)}T
                            </div>
                          )}
                        </td>
                        <td className="px-4 py-4 text-right">
                          <div className="font-mono text-white">₹{stock.price.toLocaleString()}</div>
                        </td>
                        <td className="px-4 py-4 text-right">
                          <div className={`font-mono ${stock.change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                            {stock.change >= 0 ? '+' : ''}₹{stock.change.toFixed(2)}
                          </div>
                          <div className={`text-xs ${stock.changePercent >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                            {stock.changePercent >= 0 ? '+' : ''}{stock.changePercent.toFixed(2)}%
                          </div>
                        </td>
                        <td className="px-4 py-4 text-right">
                          <div className="font-mono text-slate-300">
                            {(stock.volume / 1000000).toFixed(1)}M
                          </div>
                        </td>
                        <td className="px-4 py-4">
                          <span className="text-slate-300">{stock.sector}</span>
                        </td>
                        <td className="px-4 py-4 text-center">
                          <span className={`px-2 py-1 rounded text-xs ${getSignalColor(stock.aiSignal)} border`}>
                            {stock.aiSignal.toUpperCase()}
                          </span>
                        </td>
                        <td className="px-4 py-4 text-center">
                          <div className="flex items-center justify-center space-x-2">
                            <div className="w-12 h-1 bg-slate-700 rounded-full">
                              <div 
                                className="h-1 bg-blue-400 rounded-full"
                                style={{ width: `${stock.confidence}%` }}
                              ></div>
                            </div>
                            <span className="text-xs text-blue-400 font-medium">{stock.confidence}%</span>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Key Events */}
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <h3 className="text-xl font-bold text-white mb-4 flex items-center">
                <AlertTriangle className="h-5 w-5 mr-2 text-yellow-400" />
                Key Market Events
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {aiInsights.keyEvents.map((event, index) => (
                  <div key={index} className="p-4 bg-yellow-900/20 border border-yellow-700 rounded-lg">
                    <div className="flex items-start space-x-2">
                      <div className="w-2 h-2 bg-yellow-400 rounded-full mt-2"></div>
                      <p className="text-yellow-300 text-sm">{event}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Sector Analysis */}
        {selectedView === 'sectors' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {sectorAnalysis.map((sector, index) => (
              <div key={index} className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold text-white">{sector.sector}</h3>
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-1 rounded text-xs ${getSignalColor(sector.trend)} border`}>
                      {sector.trend.toUpperCase()}
                    </span>
                    <span className={`font-mono text-lg ${sector.performance >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                      {sector.performance >= 0 ? '+' : ''}{sector.performance.toFixed(1)}%
                    </span>
                  </div>
                </div>

                <div className="space-y-4">
                  <div>
                    <div className="text-slate-400 text-sm mb-2">Sentiment Score</div>
                    <div className="flex items-center space-x-3">
                      <div className="flex-1 h-2 bg-slate-700 rounded-full">
                        <div 
                          className={`h-2 rounded-full transition-all duration-300 ${
                            sector.sentiment > 70 ? 'bg-green-400' :
                            sector.sentiment > 50 ? 'bg-yellow-400' : 'bg-red-400'
                          }`}
                          style={{ width: `${sector.sentiment}%` }}
                        ></div>
                      </div>
                      <span className="text-white font-mono">{sector.sentiment}%</span>
                    </div>
                  </div>

                  <div>
                    <div className="text-slate-400 text-sm mb-2">Top Performers</div>
                    <div className="flex flex-wrap gap-2">
                      {sector.topStocks.map((stock, stockIndex) => (
                        <span key={stockIndex} className="px-2 py-1 bg-slate-800 text-blue-400 text-xs rounded">
                          {stock}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div>
                    <div className="text-slate-400 text-sm mb-2">AI Recommendation</div>
                    <p className="text-slate-300 text-sm">{sector.aiRecommendation}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* AI Insights */}
        {selectedView === 'insights' && (
          <div className="space-y-6">
            {/* Technical Signals */}
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <h3 className="text-xl font-bold text-white mb-6 flex items-center">
                <Zap className="h-5 w-5 mr-2 text-purple-400" />
                Technical Signals
              </h3>
              
              <div className="space-y-4">
                {aiInsights.technicalSignals.map((signal, index) => (
                  <div key={index} className="p-4 bg-purple-900/20 border border-purple-700 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-semibold text-purple-400">{signal.signal}</h4>
                      <div className="flex items-center space-x-2">
                        <div className="w-16 h-2 bg-slate-700 rounded-full">
                          <div 
                            className="h-2 bg-purple-400 rounded-full"
                            style={{ width: `${signal.strength}%` }}
                          ></div>
                        </div>
                        <span className="text-xs text-purple-400 font-medium">{signal.strength}%</span>
                      </div>
                    </div>
                    <p className="text-purple-300 text-sm">{signal.description}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Market Analysis Summary */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <h4 className="text-lg font-bold text-white mb-4">Market Trend</h4>
                <div className={`text-3xl font-bold mb-2 ${getTrendColor(aiInsights.marketTrend)}`}>
                  {aiInsights.marketTrend.toUpperCase()}
                </div>
                <p className="text-slate-400 text-sm">
                  {aiInsights.marketTrend === 'bullish' ? 'Strong upward momentum detected' :
                   aiInsights.marketTrend === 'bearish' ? 'Downward pressure observed' :
                   'Sideways consolidation phase'}
                </p>
              </div>

              <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <h4 className="text-lg font-bold text-white mb-4">Volatility Index</h4>
                <div className={`text-3xl font-bold mb-2 ${
                  aiInsights.volatility === 'high' ? 'text-red-400' :
                  aiInsights.volatility === 'medium' ? 'text-yellow-400' : 'text-green-400'
                }`}>
                  {aiInsights.volatility.toUpperCase()}
                </div>
                <p className="text-slate-400 text-sm">
                  {aiInsights.volatility === 'high' ? 'High volatility - exercise caution' :
                   aiInsights.volatility === 'medium' ? 'Moderate volatility - normal range' :
                   'Low volatility - stable market conditions'}
                </p>
              </div>

              <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <h4 className="text-lg font-bold text-white mb-4">Sentiment Score</h4>
                <div className="text-3xl font-bold text-blue-400 mb-2">{aiInsights.sentiment}%</div>
                <div className="w-full h-2 bg-slate-700 rounded-full">
                  <div 
                    className="h-2 bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 rounded-full"
                    style={{ width: `${aiInsights.sentiment}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Predictions */}
        {selectedView === 'predictions' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {aiInsights.predictions.map((prediction, index) => (
                <div key={index} className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-bold text-white">{prediction.timeframe}</h3>
                    <div className="flex items-center space-x-2">
                      {getDirectionIcon(prediction.direction)}
                      <span className={`font-bold ${
                        prediction.direction === 'up' ? 'text-green-400' :
                        prediction.direction === 'down' ? 'text-red-400' : 'text-yellow-400'
                      }`}>
                        {prediction.direction.toUpperCase()}
                      </span>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <div className="text-slate-400 text-sm mb-2">AI Confidence</div>
                      <div className="flex items-center space-x-3">
                        <div className="flex-1 h-2 bg-slate-700 rounded-full">
                          <div 
                            className="h-2 bg-blue-400 rounded-full transition-all duration-300"
                            style={{ width: `${prediction.confidence}%` }}
                          ></div>
                        </div>
                        <span className="text-blue-400 font-bold">{prediction.confidence}%</span>
                      </div>
                    </div>

                    <div>
                      <div className="text-slate-400 text-sm mb-2">Target Levels</div>
                      <div className="space-y-1">
                        {prediction.targets.map((target, targetIndex) => (
                          <div key={targetIndex} className="flex justify-between items-center">
                            <span className="text-slate-300">Target {targetIndex + 1}:</span>
                            <span className="font-mono text-white">{target.toLocaleString()}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Prediction Disclaimer */}
            <div className="bg-yellow-900/20 border border-yellow-700 rounded-2xl p-6">
              <div className="flex items-start space-x-3">
                <AlertTriangle className="h-6 w-6 text-yellow-400 mt-1" />
                <div>
                  <h3 className="text-lg font-bold text-yellow-400 mb-2">Prediction Disclaimer</h3>
                  <p className="text-yellow-300 text-sm">
                    These predictions are generated by AI models based on historical data and current market conditions. 
                    Market movements can be unpredictable and influenced by various factors not captured in the model. 
                    Always conduct your own research and consider consulting with financial advisors before making investment decisions.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Quick Action Links */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link
            href="/ai/strategies"
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-purple-500 transition-colors group"
          >
            <div className="flex items-center justify-between mb-2">
              <Brain className="h-6 w-6 text-purple-400" />
              <div className="text-xs text-slate-400">AI</div>
            </div>
            <h3 className="font-semibold text-white group-hover:text-purple-400 transition-colors">
              Strategy Analyzer
            </h3>
            <p className="text-sm text-slate-400 mt-1">
              Explore AI trading strategies
            </p>
          </Link>

          <Link
            href="/tools/screener"
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-blue-500 transition-colors group"
          >
            <div className="flex items-center justify-between mb-2">
              <BarChart3 className="h-6 w-6 text-blue-400" />
              <div className="text-xs text-slate-400">Tools</div>
            </div>
            <h3 className="font-semibold text-white group-hover:text-blue-400 transition-colors">
              Stock Screener
            </h3>
            <p className="text-sm text-slate-400 mt-1">
              Filter stocks by AI signals
            </p>
          </Link>

          <Link
            href="/tools/alerts"
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-yellow-500 transition-colors group"
          >
            <div className="flex items-center justify-between mb-2">
              <AlertTriangle className="h-6 w-6 text-yellow-400" />
              <div className="text-xs text-slate-400">Alerts</div>
            </div>
            <h3 className="font-semibold text-white group-hover:text-yellow-400 transition-colors">
              Market Alerts
            </h3>
            <p className="text-sm text-slate-400 mt-1">
              Get notified of AI insights
            </p>
          </Link>
        </div>
      </div>
    </div>
  );
}