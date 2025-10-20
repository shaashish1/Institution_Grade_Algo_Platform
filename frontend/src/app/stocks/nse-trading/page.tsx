'use client';

import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Play, Pause, RotateCcw, Download, Upload, BarChart3, Settings, Calendar, DollarSign, Target, Activity, AlertTriangle, CheckCircle, Brain, Clock, Users } from 'lucide-react';
import Link from 'next/link';

interface NSEAsset {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
  marketCap: number;
  sector: string;
  index: 'NIFTY50' | 'NIFTY100' | 'BOTH';
}

interface BacktestParams {
  assets: string[];
  strategy: string;
  timeframe: string;
  startDate: string;
  endDate: string;
  capital: number;
  stopLoss: number;
  takeProfit: number;
  maxPositions: number;
}

interface AIRecommendation {
  strategy: string;
  timeframe: string;
  confidence: number;
  reason: string;
  expectedReturn: number;
  risk: 'LOW' | 'MEDIUM' | 'HIGH';
  suitableFor: string[];
}

export default function NSETradingPage() {
  const [selectedAssets, setSelectedAssets] = useState<string[]>(['RELIANCE', 'TCS', 'HDFCBANK']);
  const [selectedIndex, setSelectedIndex] = useState<'NIFTY50' | 'NIFTY100' | 'BOTH'>('NIFTY50');
  const [params, setParams] = useState<BacktestParams>({
    assets: ['RELIANCE', 'TCS', 'HDFCBANK'],
    strategy: 'momentum',
    timeframe: '1D',
    startDate: '2024-01-01',
    endDate: '2024-10-31',
    capital: 1000000,
    stopLoss: 5,
    takeProfit: 10,
    maxPositions: 5
  });

  const [aiRecommendations, setAIRecommendations] = useState<AIRecommendation[]>([]);
  const [backtestResults, setBacktestResults] = useState<any>(null);
  const [isBacktesting, setIsBacktesting] = useState(false);
  const [aiLoading, setAILoading] = useState(false);

  // Sample NSE assets data
  const nseAssets: NSEAsset[] = [
    // NIFTY 50 Top Holdings
    { symbol: 'RELIANCE', name: 'Reliance Industries Ltd.', price: 2456.75, change: 15.30, changePercent: 0.63, volume: 12453820, marketCap: 16629400000000, sector: 'Energy', index: 'BOTH' },
    { symbol: 'TCS', name: 'Tata Consultancy Services Ltd.', price: 3542.25, change: -8.45, changePercent: -0.24, volume: 2845620, marketCap: 12982300000000, sector: 'Information Technology', index: 'BOTH' },
    { symbol: 'HDFCBANK', name: 'HDFC Bank Ltd.', price: 1654.80, change: 12.90, changePercent: 0.79, volume: 8432110, marketCap: 12567800000000, sector: 'Banking', index: 'BOTH' },
    { symbol: 'INFY', name: 'Infosys Ltd.', price: 1823.45, change: -5.25, changePercent: -0.29, volume: 5643270, marketCap: 7543200000000, sector: 'Information Technology', index: 'BOTH' },
    { symbol: 'ICICIBANK', name: 'ICICI Bank Ltd.', price: 1156.30, change: 8.75, changePercent: 0.76, volume: 9876540, marketCap: 8123400000000, sector: 'Banking', index: 'BOTH' },
    { symbol: 'BHARTIARTL', name: 'Bharti Airtel Ltd.', price: 1543.60, change: 18.25, changePercent: 1.20, volume: 4532180, marketCap: 8987600000000, sector: 'Telecommunications', index: 'BOTH' },
    { symbol: 'SBIN', name: 'State Bank of India', price: 823.45, change: -3.15, changePercent: -0.38, volume: 15432890, marketCap: 7345600000000, sector: 'Banking', index: 'BOTH' },
    { symbol: 'LT', name: 'Larsen & Toubro Ltd.', price: 3456.78, change: 25.40, changePercent: 0.74, volume: 1876543, marketCap: 4876500000000, sector: 'Construction', index: 'BOTH' },
    { symbol: 'AXISBANK', name: 'Axis Bank Ltd.', price: 1098.65, change: 12.35, changePercent: 1.14, volume: 7654321, marketCap: 3456700000000, sector: 'Banking', index: 'BOTH' },
    { symbol: 'MARUTI', name: 'Maruti Suzuki India Ltd.', price: 12345.67, change: -45.32, changePercent: -0.37, volume: 876543, marketCap: 3729400000000, sector: 'Automobile', index: 'BOTH' },
    { symbol: 'HINDUNILVR', name: 'Hindustan Unilever Ltd.', price: 2567.89, change: 8.90, changePercent: 0.35, volume: 1234567, marketCap: 6012300000000, sector: 'FMCG', index: 'BOTH' },
    { symbol: 'KOTAKBANK', name: 'Kotak Mahindra Bank Ltd.', price: 1789.45, change: 15.67, changePercent: 0.88, volume: 3456789, marketCap: 3567800000000, sector: 'Banking', index: 'BOTH' },
    { symbol: 'ASIANPAINT', name: 'Asian Paints Ltd.', price: 3098.76, change: -12.34, changePercent: -0.40, volume: 987654, marketCap: 2987600000000, sector: 'Chemicals', index: 'BOTH' },
    { symbol: 'NESTLEIND', name: 'Nestle India Ltd.', price: 2234.56, change: 23.45, changePercent: 1.06, volume: 456789, marketCap: 2156700000000, sector: 'FMCG', index: 'BOTH' },
    { symbol: 'HCLTECH', name: 'HCL Technologies Ltd.', price: 1567.89, change: -7.89, changePercent: -0.50, volume: 2345678, marketCap: 4234500000000, sector: 'Information Technology', index: 'BOTH' },
    { symbol: 'WIPRO', name: 'Wipro Ltd.', price: 567.89, change: 3.45, changePercent: 0.61, volume: 5678901, marketCap: 3123400000000, sector: 'Information Technology', index: 'BOTH' },
    { symbol: 'NTPC', name: 'NTPC Ltd.', price: 345.67, change: 2.34, changePercent: 0.68, volume: 8901234, marketCap: 3356700000000, sector: 'Power', index: 'BOTH' },
    { symbol: 'POWERGRID', name: 'Power Grid Corporation Ltd.', price: 234.56, change: 1.23, changePercent: 0.53, volume: 12345678, marketCap: 2234500000000, sector: 'Power', index: 'BOTH' },
    { symbol: 'ULTRACEMCO', name: 'UltraTech Cement Ltd.', price: 10234.56, change: 123.45, changePercent: 1.22, volume: 234567, marketCap: 3012300000000, sector: 'Cement', index: 'BOTH' },
    { symbol: 'JSWSTEEL', name: 'JSW Steel Ltd.', price: 876.54, change: -8.76, changePercent: -0.99, volume: 6789012, marketCap: 2167800000000, sector: 'Metals', index: 'BOTH' },
    
    // Additional NIFTY 100 stocks
    { symbol: 'ADANIPORTS', name: 'Adani Ports & SEZ Ltd.', price: 1456.78, change: 23.45, changePercent: 1.64, volume: 3456789, marketCap: 2987600000000, sector: 'Infrastructure', index: 'NIFTY100' },
    { symbol: 'BAJFINANCE', name: 'Bajaj Finance Ltd.', price: 6789.12, change: -34.56, changePercent: -0.51, volume: 1234567, marketCap: 4198700000000, sector: 'Financial Services', index: 'NIFTY100' },
    { symbol: 'GODREJCP', name: 'Godrej Consumer Products Ltd.', price: 1234.56, change: 12.34, changePercent: 1.01, volume: 2345678, marketCap: 1256700000000, sector: 'FMCG', index: 'NIFTY100' },
    { symbol: 'MARICO', name: 'Marico Ltd.', price: 567.89, change: 5.67, changePercent: 1.01, volume: 3456789, marketCap: 738900000000, sector: 'FMCG', index: 'NIFTY100' },
    { symbol: 'PIDILITIND', name: 'Pidilite Industries Ltd.', price: 2789.12, change: 15.67, changePercent: 0.57, volume: 876543, marketCap: 1398700000000, sector: 'Chemicals', index: 'NIFTY100' }
  ];

  const timeframes = [
    { value: '1m', label: '1 Minute', description: 'High-frequency scalping' },
    { value: '5m', label: '5 Minutes', description: 'Day trading' },
    { value: '15m', label: '15 Minutes', description: 'Intraday strategies' },
    { value: '1H', label: '1 Hour', description: 'Short-term swings' },
    { value: '4H', label: '4 Hours', description: 'Medium-term positions' },
    { value: '1D', label: '1 Day', description: 'Daily analysis' },
    { value: '1W', label: '1 Week', description: 'Weekly trends' },
    { value: '1M', label: '1 Month', description: 'Long-term positions' }
  ];

  const strategies = [
    { value: 'momentum', label: 'Momentum Strategy', description: 'Buy high-momentum stocks with strong trends' },
    { value: 'mean-reversion', label: 'Mean Reversion', description: 'Buy oversold, sell overbought' },
    { value: 'breakout', label: 'Breakout Strategy', description: 'Trade breakouts from key levels' },
    { value: 'pairs-trading', label: 'Pairs Trading', description: 'Long-short correlated pairs' },
    { value: 'sector-rotation', label: 'Sector Rotation', description: 'Rotate between sectors based on trends' },
    { value: 'bollinger-bands', label: 'Bollinger Bands', description: 'Trade based on volatility bands' },
    { value: 'rsi-divergence', label: 'RSI Divergence', description: 'Trade RSI divergence signals' },
    { value: 'macd-crossover', label: 'MACD Crossover', description: 'Trade MACD signal line crossovers' }
  ];

  const getFilteredAssets = () => {
    return nseAssets.filter(asset => {
      if (selectedIndex === 'NIFTY50') return asset.index === 'NIFTY50' || asset.index === 'BOTH';
      if (selectedIndex === 'NIFTY100') return asset.index === 'NIFTY100' || asset.index === 'BOTH';
      return true;
    });
  };

  const getAIRecommendations = async () => {
    setAILoading(true);
    
    // Simulate AI analysis
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const recommendations: AIRecommendation[] = [
      {
        strategy: 'momentum',
        timeframe: '1D',
        confidence: 87,
        reason: 'Strong upward momentum in selected assets with high volume confirmation',
        expectedReturn: 12.5,
        risk: 'MEDIUM',
        suitableFor: ['RELIANCE', 'TCS', 'HDFCBANK']
      },
      {
        strategy: 'mean-reversion',
        timeframe: '4H',
        confidence: 73,
        reason: 'Assets showing oversold conditions with RSI < 30',
        expectedReturn: 8.3,
        risk: 'LOW',
        suitableFor: ['INFY', 'WIPRO']
      },
      {
        strategy: 'breakout',
        timeframe: '1H',
        confidence: 91,
        reason: 'Multiple assets approaching key resistance levels with high volume',
        expectedReturn: 15.7,
        risk: 'HIGH',
        suitableFor: ['BHARTIARTL', 'MARUTI']
      }
    ];
    
    setAIRecommendations(recommendations);
    setAILoading(false);
  };

  const runBacktest = async () => {
    setIsBacktesting(true);
    
    // Simulate backtest execution
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Generate mock results
    const mockResults = {
      totalTrades: 156,
      winRate: 67.3,
      totalPnL: 185750,
      maxDrawdown: -8.2,
      sharpeRatio: 2.34,
      calmarRatio: 1.87,
      avgWin: 3450,
      avgLoss: -1820,
      profitFactor: 2.14,
      monthlyReturns: [
        { month: 'Jan', return: 5.2 },
        { month: 'Feb', return: -2.1 },
        { month: 'Mar', return: 8.7 },
        { month: 'Apr', return: 3.4 },
        { month: 'May', return: -1.8 },
        { month: 'Jun', return: 6.9 },
        { month: 'Jul', return: 4.2 },
        { month: 'Aug', return: -3.5 },
        { month: 'Sep', return: 7.8 },
        { month: 'Oct', return: 2.9 }
      ]
    };
    
    setBacktestResults(mockResults);
    setIsBacktesting(false);
  };

  const handleAssetSelection = (symbol: string) => {
    setSelectedAssets(prev => {
      if (prev.includes(symbol)) {
        return prev.filter(s => s !== symbol);
      } else {
        return [...prev, symbol];
      }
    });
  };

  const selectAllFromIndex = () => {
    const filteredAssets = getFilteredAssets();
    setSelectedAssets(filteredAssets.map(asset => asset.symbol));
  };

  const clearSelection = () => {
    setSelectedAssets([]);
  };

  useEffect(() => {
    setParams(prev => ({ ...prev, assets: selectedAssets }));
  }, [selectedAssets]);

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
            <span className="text-white">NSE Trading</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-4">
            NSE Trading & Backtesting Platform
          </h1>
          <p className="text-xl text-slate-300">
            Advanced backtesting for NIFTY 50 & 100 with AI-powered strategy recommendations
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Panel - Asset Selection */}
          <div className="lg:col-span-1 space-y-6">
            {/* Index Selection */}
            <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <Target className="h-5 w-5 mr-2 text-blue-400" />
                Select Index
              </h3>
              <div className="space-y-3">
                {(['NIFTY50', 'NIFTY100', 'BOTH'] as const).map((index) => (
                  <label key={index} className="flex items-center cursor-pointer">
                    <input
                      type="radio"
                      name="index"
                      value={index}
                      checked={selectedIndex === index}
                      onChange={(e) => setSelectedIndex(e.target.value as any)}
                      className="sr-only"
                    />
                    <div className={`w-4 h-4 rounded-full border-2 mr-3 flex items-center justify-center ${
                      selectedIndex === index ? 'border-blue-400 bg-blue-400' : 'border-slate-600'
                    }`}>
                      {selectedIndex === index && <div className="w-2 h-2 rounded-full bg-white"></div>}
                    </div>
                    <span className={selectedIndex === index ? 'text-white' : 'text-slate-400'}>
                      {index === 'BOTH' ? 'All Stocks' : index}
                    </span>
                  </label>
                ))}
              </div>
              
              <div className="mt-4 flex space-x-2">
                <button
                  onClick={selectAllFromIndex}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm transition-colors"
                >
                  Select All
                </button>
                <button
                  onClick={clearSelection}
                  className="bg-slate-700 hover:bg-slate-600 text-white px-3 py-1 rounded text-sm transition-colors"
                >
                  Clear
                </button>
              </div>
            </div>

            {/* Asset Selection */}
            <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <BarChart3 className="h-5 w-5 mr-2 text-green-400" />
                Assets ({selectedAssets.length} selected)
              </h3>
              <div className="max-h-96 overflow-y-auto space-y-2">
                {getFilteredAssets().map((asset) => (
                  <div
                    key={asset.symbol}
                    className={`p-3 rounded-lg border cursor-pointer transition-all ${
                      selectedAssets.includes(asset.symbol)
                        ? 'border-blue-500 bg-blue-500/10'
                        : 'border-slate-700 hover:border-slate-600'
                    }`}
                    onClick={() => handleAssetSelection(asset.symbol)}
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <div className="font-semibold text-sm">{asset.symbol}</div>
                        <div className="text-xs text-slate-400 truncate">{asset.name}</div>
                        <div className="text-xs text-slate-500">{asset.sector}</div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm">₹{asset.price.toLocaleString()}</div>
                        <div className={`text-xs ${asset.change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                          {asset.change >= 0 ? '+' : ''}{asset.changePercent.toFixed(2)}%
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Panel - Configuration & Results */}
          <div className="lg:col-span-2 space-y-6">
            {/* Strategy Configuration */}
            <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <Settings className="h-5 w-5 mr-2 text-purple-400" />
                Backtest Configuration
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Strategy</label>
                  <select
                    value={params.strategy}
                    onChange={(e) => setParams(prev => ({ ...prev, strategy: e.target.value }))}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white"
                  >
                    {strategies.map(strategy => (
                      <option key={strategy.value} value={strategy.value}>
                        {strategy.label}
                      </option>
                    ))}
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Timeframe</label>
                  <select
                    value={params.timeframe}
                    onChange={(e) => setParams(prev => ({ ...prev, timeframe: e.target.value }))}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white"
                  >
                    {timeframes.map(tf => (
                      <option key={tf.value} value={tf.value}>
                        {tf.label}
                      </option>
                    ))}
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Start Date</label>
                  <input
                    type="date"
                    value={params.startDate}
                    onChange={(e) => setParams(prev => ({ ...prev, startDate: e.target.value }))}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">End Date</label>
                  <input
                    type="date"
                    value={params.endDate}
                    onChange={(e) => setParams(prev => ({ ...prev, endDate: e.target.value }))}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Capital (₹)</label>
                  <input
                    type="number"
                    value={params.capital}
                    onChange={(e) => setParams(prev => ({ ...prev, capital: Number(e.target.value) }))}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Max Positions</label>
                  <input
                    type="number"
                    value={params.maxPositions}
                    onChange={(e) => setParams(prev => ({ ...prev, maxPositions: Number(e.target.value) }))}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white"
                  />
                </div>
              </div>

              <div className="mt-6 flex space-x-4">
                <button
                  onClick={runBacktest}
                  disabled={isBacktesting || selectedAssets.length === 0}
                  className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white px-6 py-2 rounded-lg font-semibold transition-colors flex items-center"
                >
                  {isBacktesting ? (
                    <>
                      <Activity className="h-4 w-4 mr-2 animate-spin" />
                      Running Backtest...
                    </>
                  ) : (
                    <>
                      <Play className="h-4 w-4 mr-2" />
                      Run Backtest
                    </>
                  )}
                </button>
                
                <button
                  onClick={getAIRecommendations}
                  disabled={aiLoading}
                  className="bg-purple-600 hover:bg-purple-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white px-6 py-2 rounded-lg font-semibold transition-colors flex items-center"
                >
                  {aiLoading ? (
                    <>
                      <Brain className="h-4 w-4 mr-2 animate-pulse" />
                      AI Analyzing...
                    </>
                  ) : (
                    <>
                      <Brain className="h-4 w-4 mr-2" />
                      Get AI Recommendations
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* AI Recommendations */}
            {aiRecommendations.length > 0 && (
              <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                  <Brain className="h-5 w-5 mr-2 text-purple-400" />
                  AI Strategy Recommendations
                </h3>
                <div className="space-y-4">
                  {aiRecommendations.map((rec, index) => (
                    <div key={index} className="bg-slate-800 rounded-lg p-4 border border-slate-700">
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <h4 className="font-semibold text-white">{strategies.find(s => s.value === rec.strategy)?.label}</h4>
                          <p className="text-sm text-slate-400">Timeframe: {timeframes.find(t => t.value === rec.timeframe)?.label}</p>
                        </div>
                        <div className="text-right">
                          <div className="text-sm font-semibold text-green-400">+{rec.expectedReturn}%</div>
                          <div className={`text-xs px-2 py-1 rounded ${
                            rec.risk === 'LOW' ? 'bg-green-500/20 text-green-400' :
                            rec.risk === 'MEDIUM' ? 'bg-yellow-500/20 text-yellow-400' :
                            'bg-red-500/20 text-red-400'
                          }`}>
                            {rec.risk} RISK
                          </div>
                        </div>
                      </div>
                      <p className="text-sm text-slate-300 mb-2">{rec.reason}</p>
                      <div className="flex justify-between items-center">
                        <div className="text-xs text-slate-500">
                          Best for: {rec.suitableFor.join(', ')}
                        </div>
                        <div className="text-xs text-blue-400">
                          Confidence: {rec.confidence}%
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Backtest Results */}
            {backtestResults && (
              <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                  <CheckCircle className="h-5 w-5 mr-2 text-green-400" />
                  Backtest Results
                </h3>
                
                {/* Key Metrics */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="bg-slate-800 rounded-lg p-4">
                    <div className="text-sm text-slate-400">Total P&L</div>
                    <div className={`text-xl font-bold ${backtestResults.totalPnL >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                      ₹{backtestResults.totalPnL.toLocaleString()}
                    </div>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-4">
                    <div className="text-sm text-slate-400">Win Rate</div>
                    <div className="text-xl font-bold text-blue-400">{backtestResults.winRate}%</div>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-4">
                    <div className="text-sm text-slate-400">Sharpe Ratio</div>
                    <div className="text-xl font-bold text-purple-400">{backtestResults.sharpeRatio}</div>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-4">
                    <div className="text-sm text-slate-400">Max Drawdown</div>
                    <div className="text-xl font-bold text-red-400">{backtestResults.maxDrawdown}%</div>
                  </div>
                </div>

                {/* Monthly Returns */}
                <div className="mb-6">
                  <h4 className="text-sm font-semibold mb-3 text-slate-300">Monthly Returns</h4>
                  <div className="grid grid-cols-5 md:grid-cols-10 gap-2">
                    {backtestResults.monthlyReturns.map((month: any, index: number) => (
                      <div key={index} className={`p-2 rounded text-center text-xs ${
                        month.return >= 0 ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                      }`}>
                        <div className="font-semibold">{month.month}</div>
                        <div>{month.return > 0 ? '+' : ''}{month.return}%</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Additional Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-slate-800 rounded-lg p-4">
                    <div className="text-sm text-slate-400">Total Trades</div>
                    <div className="text-lg font-semibold text-white">{backtestResults.totalTrades}</div>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-4">
                    <div className="text-sm text-slate-400">Profit Factor</div>
                    <div className="text-lg font-semibold text-white">{backtestResults.profitFactor}</div>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-4">
                    <div className="text-sm text-slate-400">Calmar Ratio</div>
                    <div className="text-lg font-semibold text-white">{backtestResults.calmarRatio}</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}