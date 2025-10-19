'use client';

import React, { useState, useEffect } from 'react';
import { 
  Brain, TrendingUp, TrendingDown, BarChart3, Target, Zap, 
  Crown, Medal, Award, AlertCircle, CheckCircle, Eye, Play,
  Lightbulb, Calculator, Activity, DollarSign, Shield, RefreshCw,
  Download, Settings, Filter, Search, Calendar, Clock, Star,
  ArrowUpRight, ArrowDownRight, PieChart, LineChart
} from 'lucide-react';
import Link from 'next/link';

interface AIRecommendation {
  id: string;
  symbol: string;
  strategy: string;
  action: 'BUY' | 'SELL' | 'HOLD';
  confidence: number;
  aiScore: number;
  targetPrice: number;
  stopLoss: number;
  timeframe: string;
  reasoning: string[];
  marketFactors: {
    technical: number;
    fundamental: number;
    sentiment: number;
    volume: number;
  };
  riskLevel: 'low' | 'medium' | 'high';
  expectedReturn: number;
  probability: number;
}

interface BacktestResult {
  strategy: string;
  symbol: string;
  timeframe: string;
  performance: {
    totalReturn: number;
    winRate: number;
    sharpeRatio: number;
    maxDrawdown: number;
    trades: number;
  };
  aiAnalysis: {
    marketRegime: string;
    volatilityForecast: number;
    trendStrength: number;
    recommendation: string;
  };
}

interface MarketInsight {
  type: 'opportunity' | 'warning' | 'neutral';
  title: string;
  description: string;
  impact: 'high' | 'medium' | 'low';
  timeRelevant: string;
}

export function AIBacktestingHub() {
  const [selectedTimeframe, setSelectedTimeframe] = useState<string>('1D');
  const [selectedStrategy, setSelectedStrategy] = useState<string>('momentum');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showRecommendations, setShowRecommendations] = useState(true);

  const [aiRecommendations, setAiRecommendations] = useState<AIRecommendation[]>([
    {
      id: '1',
      symbol: 'NIFTY 25800 CE',
      strategy: 'Volatility Breakout',
      action: 'BUY',
      confidence: 87,
      aiScore: 92,
      targetPrice: 185,
      stopLoss: 145,
      timeframe: '2-3 days',
      reasoning: [
        'Strong momentum breakout above key resistance',
        'Implied volatility below historical average',
        'Bullish sentiment in banking sector',
        'Options volume spike indicates institutional interest'
      ],
      marketFactors: {
        technical: 88,
        fundamental: 75,
        sentiment: 82,
        volume: 91
      },
      riskLevel: 'medium',
      expectedReturn: 23.5,
      probability: 0.74
    },
    {
      id: '2',
      symbol: 'RELIANCE',
      strategy: 'Mean Reversion',
      action: 'BUY',
      confidence: 91,
      aiScore: 89,
      targetPrice: 2580,
      stopLoss: 2420,
      timeframe: '1-2 weeks',
      reasoning: [
        'Stock oversold after recent correction',
        'Strong quarterly results expected',
        'Oil price stability supports energy sector',
        'Technical indicators showing reversal signals'
      ],
      marketFactors: {
        technical: 85,
        fundamental: 92,
        sentiment: 78,
        volume: 87
      },
      riskLevel: 'low',
      expectedReturn: 18.2,
      probability: 0.81
    },
    {
      id: '3',
      symbol: 'BTC/USDT',
      strategy: 'Trend Following',
      action: 'HOLD',
      confidence: 73,
      aiScore: 76,
      targetPrice: 102000,
      stopLoss: 94000,
      timeframe: '1-3 weeks',
      reasoning: [
        'Consolidation phase near resistance',
        'Institutional adoption continues',
        'Regulatory clarity improving globally',
        'Wait for clear breakout signal'
      ],
      marketFactors: {
        technical: 72,
        fundamental: 84,
        sentiment: 69,
        volume: 76
      },
      riskLevel: 'high',
      expectedReturn: 15.8,
      probability: 0.68
    }
  ]);

  const [backtestResults, setBacktestResults] = useState<BacktestResult[]>([
    {
      strategy: 'AI Momentum',
      symbol: 'NIFTY',
      timeframe: '1D',
      performance: {
        totalReturn: 34.2,
        winRate: 68.5,
        sharpeRatio: 1.84,
        maxDrawdown: -8.3,
        trades: 127
      },
      aiAnalysis: {
        marketRegime: 'Trending Bull',
        volatilityForecast: 16.8,
        trendStrength: 0.72,
        recommendation: 'Increase position size in trending markets'
      }
    },
    {
      strategy: 'AI Mean Reversion',
      symbol: 'BANKNIFTY',
      timeframe: '4H',
      performance: {
        totalReturn: 28.7,
        winRate: 72.1,
        sharpeRatio: 1.91,
        maxDrawdown: -6.2,
        trades: 89
      },
      aiAnalysis: {
        marketRegime: 'Range Bound',
        volatilityForecast: 22.4,
        trendStrength: 0.31,
        recommendation: 'Optimal for range-bound conditions'
      }
    }
  ]);

  const [marketInsights, setMarketInsights] = useState<MarketInsight[]>([
    {
      type: 'opportunity',
      title: 'High Volatility Setup in Banking Sector',
      description: 'AI detects increased volatility patterns in banking stocks, ideal for option strategies',
      impact: 'high',
      timeRelevant: 'Next 2-3 days'
    },
    {
      type: 'warning',
      title: 'Crypto Market Correlation Risk',
      description: 'Rising correlation between crypto and equity markets may amplify portfolio risk',
      impact: 'medium',
      timeRelevant: 'Current week'
    },
    {
      type: 'opportunity',
      title: 'Earnings Season Alpha Opportunity',
      description: 'ML models identify potential earnings surprises in IT sector stocks',
      impact: 'high',
      timeRelevant: 'Next 2 weeks'
    }
  ]);

  const runAIAnalysis = async () => {
    setIsAnalyzing(true);
    // Simulate AI analysis
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Generate new recommendations
    const newRecommendations = [...aiRecommendations];
    newRecommendations.forEach(rec => {
      rec.confidence = Math.max(60, Math.min(95, rec.confidence + (Math.random() - 0.5) * 10));
      rec.aiScore = Math.max(65, Math.min(98, rec.aiScore + (Math.random() - 0.5) * 8));
    });
    
    setAiRecommendations(newRecommendations);
    setIsAnalyzing(false);
  };

  const getActionColor = (action: string) => {
    switch (action) {
      case 'BUY': return 'text-green-400 bg-green-500/10';
      case 'SELL': return 'text-red-400 bg-red-500/10';
      case 'HOLD': return 'text-yellow-400 bg-yellow-500/10';
      default: return 'text-slate-400 bg-slate-500/10';
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'text-green-400 bg-green-500/10';
      case 'medium': return 'text-yellow-400 bg-yellow-500/10';
      case 'high': return 'text-red-400 bg-red-500/10';
      default: return 'text-slate-400 bg-slate-500/10';
    }
  };

  const getInsightColor = (type: string) => {
    switch (type) {
      case 'opportunity': return 'text-green-400 bg-green-500/10 border-green-500/30';
      case 'warning': return 'text-red-400 bg-red-500/10 border-red-500/30';
      case 'neutral': return 'text-blue-400 bg-blue-500/10 border-blue-500/30';
      default: return 'text-slate-400 bg-slate-500/10 border-slate-500/30';
    }
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
            <span className="text-white">AI Backtesting Hub</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">
                AI-Powered Backtesting & Trade Analysis
              </h1>
              <p className="text-slate-400">
                Advanced AI algorithms analyze market conditions and recommend optimal trading strategies
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
                AI Insights
              </button>
              <button
                onClick={runAIAnalysis}
                disabled={isAnalyzing}
                className="flex items-center px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-slate-600 disabled:to-slate-600 disabled:cursor-not-allowed rounded-lg transition-colors"
              >
                {isAnalyzing ? (
                  <>
                    <div className="animate-spin h-4 w-4 mr-2 border-2 border-white border-t-transparent rounded-full" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Brain className="h-4 w-4 mr-2" />
                    Run AI Analysis
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
              <div className="flex items-center justify-between mb-2">
                <span className="text-slate-400 text-sm">AI Accuracy</span>
                <Brain className="h-4 w-4 text-purple-400" />
              </div>
              <div className="text-2xl font-bold text-white">87.3%</div>
              <div className="text-sm text-green-400">+2.1% this week</div>
            </div>
            
            <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
              <div className="flex items-center justify-between mb-2">
                <span className="text-slate-400 text-sm">Active Signals</span>
                <Zap className="h-4 w-4 text-yellow-400" />
              </div>
              <div className="text-2xl font-bold text-white">24</div>
              <div className="text-sm text-blue-400">12 high confidence</div>
            </div>
            
            <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
              <div className="flex items-center justify-between mb-2">
                <span className="text-slate-400 text-sm">Avg Return</span>
                <TrendingUp className="h-4 w-4 text-green-400" />
              </div>
              <div className="text-2xl font-bold text-green-400">+31.4%</div>
              <div className="text-sm text-slate-400">Last 30 days</div>
            </div>
            
            <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
              <div className="flex items-center justify-between mb-2">
                <span className="text-slate-400 text-sm">Risk Score</span>
                <Shield className="h-4 w-4 text-blue-400" />
              </div>
              <div className="text-2xl font-bold text-yellow-400">6.2/10</div>
              <div className="text-sm text-slate-400">Moderate risk</div>
            </div>
          </div>
        </div>

        {/* AI Recommendations */}
        {showRecommendations && (
          <div className="mb-8">
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-white flex items-center">
                  <Lightbulb className="h-5 w-5 mr-2 text-yellow-400" />
                  AI Trade Recommendations
                </h2>
                <div className="text-sm text-slate-400">
                  Updated {new Date().toLocaleTimeString()}
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                {aiRecommendations.map((rec) => (
                  <div
                    key={rec.id}
                    className="bg-slate-800 rounded-xl p-6 border border-slate-700 hover:border-purple-500/50 transition-all"
                  >
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <h3 className="font-bold text-white">{rec.symbol}</h3>
                        <p className="text-sm text-slate-400">{rec.strategy}</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getActionColor(rec.action)}`}>
                          {rec.action}
                        </span>
                        <div className="text-right">
                          <div className="text-sm text-slate-400">AI Score</div>
                          <div className="text-lg font-bold text-purple-400">{rec.aiScore}</div>
                        </div>
                      </div>
                    </div>

                    <div className="space-y-3 mb-4">
                      <div className="flex justify-between">
                        <span className="text-slate-400">Confidence:</span>
                        <span className="text-white font-semibold">{rec.confidence}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Target:</span>
                        <span className="text-green-400">₹{rec.targetPrice}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Stop Loss:</span>
                        <span className="text-red-400">₹{rec.stopLoss}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Expected Return:</span>
                        <span className="text-purple-400">+{rec.expectedReturn}%</span>
                      </div>
                    </div>

                    <div className="mb-4">
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm text-slate-400">Market Factors</span>
                        <span className={`px-2 py-1 rounded text-xs font-medium ${getRiskColor(rec.riskLevel)}`}>
                          {rec.riskLevel} risk
                        </span>
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div className="flex justify-between">
                          <span className="text-slate-400">Technical:</span>
                          <span className="text-blue-400">{rec.marketFactors.technical}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Fundamental:</span>
                          <span className="text-green-400">{rec.marketFactors.fundamental}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Sentiment:</span>
                          <span className="text-yellow-400">{rec.marketFactors.sentiment}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Volume:</span>
                          <span className="text-purple-400">{rec.marketFactors.volume}%</span>
                        </div>
                      </div>
                    </div>

                    <div className="mb-4">
                      <h4 className="text-sm font-medium text-white mb-2">AI Reasoning:</h4>
                      <ul className="space-y-1">
                        {rec.reasoning.slice(0, 2).map((reason, idx) => (
                          <li key={idx} className="text-xs text-slate-300 flex items-start">
                            <div className="w-1 h-1 bg-blue-400 rounded-full mr-2 mt-2 flex-shrink-0" />
                            {reason}
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="text-xs text-slate-400">
                        Timeframe: {rec.timeframe}
                      </div>
                      <div className="text-xs text-slate-300">
                        Success Probability: {(rec.probability * 100).toFixed(0)}%
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Market Insights */}
        <div className="mb-8">
          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center">
              <Eye className="h-5 w-5 mr-2 text-blue-400" />
              AI Market Insights
            </h2>
            
            <div className="space-y-4">
              {marketInsights.map((insight, index) => (
                <div
                  key={index}
                  className={`p-4 rounded-lg border ${getInsightColor(insight.type)}`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-white">{insight.title}</h3>
                    <div className="flex items-center space-x-2">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        insight.impact === 'high' ? 'bg-red-500/20 text-red-400' :
                        insight.impact === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                        'bg-green-500/20 text-green-400'
                      }`}>
                        {insight.impact} impact
                      </span>
                      <Clock className="h-3 w-3 text-slate-400" />
                      <span className="text-xs text-slate-400">{insight.timeRelevant}</span>
                    </div>
                  </div>
                  <p className="text-slate-300 text-sm">{insight.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Backtest Results */}
        <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-white flex items-center">
              <BarChart3 className="h-5 w-5 mr-2 text-green-400" />
              AI Strategy Performance
            </h2>
            <Link href="/stocks/backtest/universal" className="text-blue-400 hover:text-blue-300 text-sm">
              Run Full Backtest
            </Link>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {backtestResults.map((result, index) => (
              <div key={index} className="bg-slate-800 rounded-xl p-6 border border-slate-700">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="font-bold text-white">{result.strategy}</h3>
                    <p className="text-sm text-slate-400">{result.symbol} • {result.timeframe}</p>
                  </div>
                  {index === 0 && <Crown className="h-5 w-5 text-yellow-400" />}
                </div>

                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <div className="text-slate-400 text-sm">Total Return</div>
                    <div className="text-green-400 font-bold">+{result.performance.totalReturn}%</div>
                  </div>
                  <div>
                    <div className="text-slate-400 text-sm">Win Rate</div>
                    <div className="text-blue-400 font-bold">{result.performance.winRate}%</div>
                  </div>
                  <div>
                    <div className="text-slate-400 text-sm">Sharpe Ratio</div>
                    <div className="text-purple-400 font-bold">{result.performance.sharpeRatio}</div>
                  </div>
                  <div>
                    <div className="text-slate-400 text-sm">Max Drawdown</div>
                    <div className="text-red-400 font-bold">{result.performance.maxDrawdown}%</div>
                  </div>
                </div>

                <div className="border-t border-slate-700 pt-4">
                  <h4 className="text-sm font-medium text-white mb-2">AI Analysis:</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Market Regime:</span>
                      <span className="text-white">{result.aiAnalysis.marketRegime}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Volatility Forecast:</span>
                      <span className="text-yellow-400">{result.aiAnalysis.volatilityForecast}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Trend Strength:</span>
                      <span className="text-green-400">{result.aiAnalysis.trendStrength}</span>
                    </div>
                  </div>
                  <p className="text-xs text-slate-300 mt-3 p-2 bg-slate-900 rounded">
                    {result.aiAnalysis.recommendation}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}