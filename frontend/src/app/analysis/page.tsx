'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { 
  BarChart3, LineChart, TrendingUp, TrendingDown, Activity,
  Target, DollarSign, Eye, Filter, Download, Calendar,
  ArrowUp, ArrowDown, Info, Zap
} from 'lucide-react';

export default function AnalysisPage() {
  const [timeframe, setTimeframe] = useState('1D');
  const [selectedSymbol, setSelectedSymbol] = useState('NIFTY 50');

  const timeframes = ['1D', '1W', '1M', '3M', '1Y', 'ALL'];
  
  const symbols = ['NIFTY 50', 'BANK NIFTY', 'SENSEX', 'FINNIFTY'];

  const technicalIndicators = [
    { name: 'RSI (14)', value: 64.5, signal: 'Neutral', color: 'text-yellow-400' },
    { name: 'MACD', value: '+125.3', signal: 'Bullish', color: 'text-green-400' },
    { name: 'MA (50)', value: '21,350', signal: 'Above', color: 'text-green-400' },
    { name: 'MA (200)', value: '20,890', signal: 'Above', color: 'text-green-400' },
    { name: 'Bollinger Bands', value: 'Upper', signal: 'Overbought', color: 'text-yellow-400' },
    { name: 'ADX', value: 35.2, signal: 'Strong Trend', color: 'text-green-400' },
  ];

  const supportResistance = [
    { type: 'Resistance 3', level: 21800, distance: '+1.6%' },
    { type: 'Resistance 2', level: 21650, distance: '+0.9%' },
    { type: 'Resistance 1', level: 21520, distance: '+0.3%' },
    { type: 'Current Price', level: 21450, distance: '0.0%' },
    { type: 'Support 1', level: 21350, distance: '-0.5%' },
    { type: 'Support 2', level: 21200, distance: '-1.2%' },
    { type: 'Support 3', level: 21050, distance: '-1.9%' },
  ];

  const marketSentiment = [
    { category: 'Bullish', percentage: 62, color: 'bg-green-500' },
    { category: 'Neutral', percentage: 23, color: 'bg-yellow-500' },
    { category: 'Bearish', percentage: 15, color: 'bg-red-500' },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Breadcrumb */}
      <div className="bg-slate-900 border-b border-slate-800 px-6 py-4">
        <nav className="flex items-center space-x-2 text-sm text-slate-400">
          <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
          <span>/</span>
          <span className="text-white">Market Analysis</span>
        </nav>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
            Market Analysis
          </h1>
          <p className="text-xl text-slate-300">
            Technical & fundamental analysis with AI insights
          </p>
        </div>

        {/* Controls */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Symbol Selector */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <label className="block text-sm font-medium text-slate-400 mb-2">Select Symbol</label>
            <select
              value={selectedSymbol}
              onChange={(e) => setSelectedSymbol(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {symbols.map((symbol) => (
                <option key={symbol} value={symbol}>{symbol}</option>
              ))}
            </select>
          </div>

          {/* Timeframe Selector */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <label className="block text-sm font-medium text-slate-400 mb-2">Timeframe</label>
            <div className="flex space-x-2">
              {timeframes.map((tf) => (
                <button
                  key={tf}
                  onClick={() => setTimeframe(tf)}
                  className={`flex-1 px-3 py-2 rounded-lg font-medium transition-colors ${
                    timeframe === tf
                      ? 'bg-blue-600 text-white'
                      : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                  }`}
                >
                  {tf}
                </button>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <label className="block text-sm font-medium text-slate-400 mb-2">Actions</label>
            <div className="flex space-x-2">
              <button className="flex-1 flex items-center justify-center space-x-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors">
                <Filter className="h-4 w-4" />
                <span>Filter</span>
              </button>
              <button className="flex-1 flex items-center justify-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors">
                <Download className="h-4 w-4" />
                <span>Export</span>
              </button>
            </div>
          </div>
        </div>

        {/* Chart Placeholder */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-white">{selectedSymbol} Price Chart</h2>
            <div className="flex items-center space-x-2">
              <span className="text-2xl font-bold text-white">₹21,450.30</span>
              <div className="flex items-center space-x-1 text-green-400">
                <ArrowUp className="h-5 w-5" />
                <span className="font-medium">+0.74%</span>
              </div>
            </div>
          </div>
          
          <div className="bg-slate-800 rounded-lg p-8 h-96 flex items-center justify-center">
            <div className="text-center">
              <LineChart className="h-16 w-16 text-slate-600 mx-auto mb-4" />
              <p className="text-slate-400">Advanced charting coming soon</p>
              <p className="text-sm text-slate-500 mt-2">
                Visit <Link href="/charts" className="text-blue-400 hover:underline">Advanced Charts</Link> for TradingView integration
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Technical Indicators */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-white">Technical Indicators</h2>
              <Zap className="h-5 w-5 text-yellow-400" />
            </div>

            <div className="space-y-4">
              {technicalIndicators.map((indicator, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-slate-800 rounded-lg">
                  <div>
                    <div className="font-medium text-white">{indicator.name}</div>
                    <div className="text-sm text-slate-400">Value: {indicator.value}</div>
                  </div>
                  <div className={`px-3 py-1 rounded-full text-sm font-medium ${indicator.color} bg-slate-700`}>
                    {indicator.signal}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Support & Resistance */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-white">Support & Resistance</h2>
              <Target className="h-5 w-5 text-purple-400" />
            </div>

            <div className="space-y-2">
              {supportResistance.map((level, index) => (
                <div 
                  key={index} 
                  className={`flex items-center justify-between p-3 rounded-lg ${
                    level.type === 'Current Price' 
                      ? 'bg-blue-500/20 border border-blue-500/50' 
                      : 'bg-slate-800'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    {level.type.includes('Resistance') && <ArrowUp className="h-4 w-4 text-red-400" />}
                    {level.type.includes('Support') && <ArrowDown className="h-4 w-4 text-green-400" />}
                    {level.type === 'Current Price' && <Activity className="h-4 w-4 text-blue-400" />}
                    <span className={`font-medium ${
                      level.type === 'Current Price' ? 'text-blue-400' : 'text-white'
                    }`}>
                      {level.type}
                    </span>
                  </div>
                  <div className="text-right">
                    <div className="font-mono text-white">₹{level.level.toLocaleString()}</div>
                    <div className={`text-xs ${
                      level.distance.startsWith('+') ? 'text-red-400' : 
                      level.distance === '0.0%' ? 'text-blue-400' : 'text-green-400'
                    }`}>
                      {level.distance}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Market Sentiment */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-white">Market Sentiment</h2>
            <BarChart3 className="h-5 w-5 text-blue-400" />
          </div>

          <div className="space-y-4">
            {marketSentiment.map((sentiment, index) => (
              <div key={index}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-slate-300 font-medium">{sentiment.category}</span>
                  <span className="text-white font-bold">{sentiment.percentage}%</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-3">
                  <div 
                    className={`${sentiment.color} h-3 rounded-full transition-all duration-500`}
                    style={{ width: `${sentiment.percentage}%` }}
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6 p-4 bg-slate-800 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm text-slate-400">Overall Sentiment</div>
                <div className="text-2xl font-bold text-green-400">Bullish</div>
              </div>
              <div className="text-right">
                <div className="text-sm text-slate-400">Confidence Score</div>
                <div className="text-2xl font-bold text-white">7.8/10</div>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Links */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link href="/stocks/option-chain" className="bg-slate-900 border border-slate-800 rounded-xl p-6 hover:border-blue-500 transition-colors group">
            <Target className="h-8 w-8 text-blue-400 mb-4" />
            <h3 className="text-lg font-bold text-white mb-2">Option Chain</h3>
            <p className="text-sm text-slate-400">View real-time option chain data</p>
          </Link>

          <Link href="/stocks/backtest" className="bg-slate-900 border border-slate-800 rounded-xl p-6 hover:border-purple-500 transition-colors group">
            <Activity className="h-8 w-8 text-purple-400 mb-4" />
            <h3 className="text-lg font-bold text-white mb-2">Backtest Strategies</h3>
            <p className="text-sm text-slate-400">Test strategies on historical data</p>
          </Link>

          <Link href="/ai/strategies" className="bg-slate-900 border border-slate-800 rounded-xl p-6 hover:border-yellow-500 transition-colors group">
            <Zap className="h-8 w-8 text-yellow-400 mb-4" />
            <h3 className="text-lg font-bold text-white mb-2">AI Recommendations</h3>
            <p className="text-sm text-slate-400">Get AI-powered strategy suggestions</p>
          </Link>
        </div>

        {/* Info Banner */}
        <div className="mt-8 bg-blue-500/10 border border-blue-500/20 rounded-xl p-4">
          <div className="flex items-start space-x-3">
            <Info className="h-5 w-5 text-blue-400 mt-0.5 flex-shrink-0" />
            <div className="flex-1">
              <p className="text-sm text-blue-200">
                <strong>Educational Purpose:</strong> These analyses are for educational purposes only 
                and should not be considered as financial advice. Always do your own research before trading.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
