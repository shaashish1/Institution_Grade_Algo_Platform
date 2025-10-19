'use client';

import React, { useState, useEffect } from 'react';
import { 
  Brain, Lightbulb, Target, Star, Crown, Award, Shield, Zap,
  TrendingUp, TrendingDown, BarChart3, PieChart, Calculator,
  AlertCircle, CheckCircle, Play, RefreshCw, Settings, Filter,
  ArrowRight, ArrowUpRight, Clock, DollarSign, Activity
} from 'lucide-react';
import Link from 'next/link';

interface StrategyRecommendation {
  id: string;
  name: string;
  type: 'momentum' | 'mean_reversion' | 'volatility' | 'arbitrage' | 'trend_following';
  assetClass: string;
  timeframe: string;
  aiScore: number;
  confidence: number;
  expectedReturn: number;
  riskLevel: 'low' | 'medium' | 'high';
  marketSuitability: number;
  complexity: 'beginner' | 'intermediate' | 'advanced';
  description: string;
  keyFeatures: string[];
  marketConditions: string[];
  pros: string[];
  cons: string[];
  historicalPerformance: {
    winRate: number;
    avgReturn: number;
    maxDrawdown: number;
    sharpeRatio: number;
    trades: number;
  };
  implementation: {
    minCapital: number;
    timeCommitment: string;
    tools: string[];
    difficulty: number;
  };
}

interface MarketCondition {
  name: string;
  current: number;
  optimal: number;
  impact: 'positive' | 'negative' | 'neutral';
}

interface PersonalizedProfile {
  riskTolerance: 'conservative' | 'moderate' | 'aggressive';
  experience: 'beginner' | 'intermediate' | 'expert';
  capital: number;
  timeHorizon: 'short' | 'medium' | 'long';
  preferredAssets: string[];
  goals: string[];
}

export function StrategyRecommendationEngine() {
  const [userProfile, setUserProfile] = useState<PersonalizedProfile>({
    riskTolerance: 'moderate',
    experience: 'intermediate',
    capital: 500000,
    timeHorizon: 'medium',
    preferredAssets: ['stocks', 'options'],
    goals: ['consistent_returns', 'capital_growth']
  });

  const [recommendations, setRecommendations] = useState<StrategyRecommendation[]>([
    {
      id: '1',
      name: 'AI Enhanced Iron Condor',
      type: 'volatility',
      assetClass: 'Options',
      timeframe: 'Weekly',
      aiScore: 94,
      confidence: 87,
      expectedReturn: 15.8,
      riskLevel: 'medium',
      marketSuitability: 92,
      complexity: 'intermediate',
      description: 'AI-optimized iron condor strategy that adapts strike selection based on volatility forecasts and market sentiment analysis.',
      keyFeatures: [
        'Dynamic strike selection using ML models',
        'Volatility forecasting for entry timing',
        'Automated position sizing',
        'Risk-adjusted profit taking'
      ],
      marketConditions: [
        'Low to medium volatility environments',
        'Range-bound markets',
        'High implied volatility premiums'
      ],
      pros: [
        'High probability of profit (70-80%)',
        'Limited risk exposure',
        'Generates consistent income',
        'AI optimization improves traditional strategy'
      ],
      cons: [
        'Limited profit potential',
        'Requires active monitoring',
        'Commission intensive',
        'Vulnerable to gap moves'
      ],
      historicalPerformance: {
        winRate: 78,
        avgReturn: 12.4,
        maxDrawdown: -8.2,
        sharpeRatio: 1.85,
        trades: 156
      },
      implementation: {
        minCapital: 100000,
        timeCommitment: '2-3 hours/week',
        tools: ['Options scanner', 'Volatility analysis', 'Position tracker'],
        difficulty: 7
      }
    },
    {
      id: '2',
      name: 'Momentum Breakout AI',
      type: 'momentum',
      assetClass: 'Stocks',
      timeframe: 'Daily',
      aiScore: 91,
      confidence: 83,
      expectedReturn: 28.5,
      riskLevel: 'high',
      marketSuitability: 88,
      complexity: 'advanced',
      description: 'Machine learning model identifies momentum breakouts with high probability using price action, volume, and sentiment data.',
      keyFeatures: [
        'Multi-factor momentum scoring',
        'Volume surge detection',
        'Sentiment analysis integration',
        'Dynamic stop-loss positioning'
      ],
      marketConditions: [
        'Strong trending markets',
        'High volume environments',
        'Clear directional moves'
      ],
      pros: [
        'High return potential',
        'Captures major moves early',
        'Scalable across sectors',
        'AI reduces false signals'
      ],
      cons: [
        'Higher volatility',
        'Requires quick execution',
        'Can face sudden reversals',
        'Higher transaction costs'
      ],
      historicalPerformance: {
        winRate: 64,
        avgReturn: 18.7,
        maxDrawdown: -15.3,
        sharpeRatio: 1.42,
        trades: 89
      },
      implementation: {
        minCapital: 200000,
        timeCommitment: '1-2 hours/day',
        tools: ['Real-time scanner', 'Technical analysis', 'News sentiment'],
        difficulty: 8
      }
    },
    {
      id: '3',
      name: 'Smart Mean Reversion',
      type: 'mean_reversion',
      assetClass: 'ETFs',
      timeframe: '4-Hour',
      aiScore: 89,
      confidence: 90,
      expectedReturn: 18.2,
      riskLevel: 'low',
      marketSuitability: 95,
      complexity: 'beginner',
      description: 'AI-powered mean reversion strategy for ETFs that identifies oversold/overbought conditions with high accuracy.',
      keyFeatures: [
        'Multi-timeframe analysis',
        'Sector rotation optimization',
        'Risk parity position sizing',
        'Automated rebalancing'
      ],
      marketConditions: [
        'Range-bound markets',
        'Low volatility periods',
        'Stable economic conditions'
      ],
      pros: [
        'Lower risk profile',
        'Consistent returns',
        'Good for beginners',
        'Diversification benefits'
      ],
      cons: [
        'Lower return potential',
        'Slower profit realization',
        'May underperform in trends',
        'Requires patience'
      ],
      historicalPerformance: {
        winRate: 82,
        avgReturn: 14.6,
        maxDrawdown: -5.8,
        sharpeRatio: 2.15,
        trades: 124
      },
      implementation: {
        minCapital: 50000,
        timeCommitment: '30 minutes/day',
        tools: ['ETF screener', 'Rebalancing alerts', 'Risk monitor'],
        difficulty: 4
      }
    }
  ]);

  const [marketConditions, setMarketConditions] = useState<MarketCondition[]>([
    { name: 'Market Volatility', current: 16.8, optimal: 18.5, impact: 'positive' },
    { name: 'Trend Strength', current: 0.72, optimal: 0.65, impact: 'neutral' },
    { name: 'Volume Profile', current: 85, optimal: 80, impact: 'positive' },
    { name: 'Sentiment Score', current: 68, optimal: 70, impact: 'neutral' }
  ]);

  const [isGenerating, setIsGenerating] = useState(false);
  const [selectedStrategy, setSelectedStrategy] = useState<string | null>(null);

  const generateRecommendations = async () => {
    setIsGenerating(true);
    // Simulate AI processing
    await new Promise(resolve => setTimeout(resolve, 2500));
    
    // Update recommendations based on user profile
    const updatedRecs = recommendations.map(rec => ({
      ...rec,
      aiScore: Math.max(75, Math.min(98, rec.aiScore + (Math.random() - 0.5) * 10)),
      confidence: Math.max(70, Math.min(95, rec.confidence + (Math.random() - 0.5) * 8))
    }));
    
    setRecommendations(updatedRecs);
    setIsGenerating(false);
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'momentum': return TrendingUp;
      case 'mean_reversion': return Target;
      case 'volatility': return Activity;
      case 'arbitrage': return Calculator;
      case 'trend_following': return BarChart3;
      default: return Brain;
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

  const getComplexityColor = (complexity: string) => {
    switch (complexity) {
      case 'beginner': return 'text-green-400 bg-green-500/10';
      case 'intermediate': return 'text-yellow-400 bg-yellow-500/10';
      case 'advanced': return 'text-red-400 bg-red-500/10';
      default: return 'text-slate-400 bg-slate-500/10';
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
            <Link href="/ai" className="hover:text-blue-400 transition-colors">AI Tools</Link>
            <span>/</span>
            <span className="text-white">Strategy Recommender</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">
                AI Strategy Recommendation Engine
              </h1>
              <p className="text-slate-400">
                Personalized trading strategy recommendations powered by machine learning
              </p>
            </div>
            
            <div className="flex items-center gap-4">
              <button className="flex items-center px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors">
                <Settings className="h-4 w-4 mr-2" />
                Customize Profile
              </button>
              <button
                onClick={generateRecommendations}
                disabled={isGenerating}
                className="flex items-center px-6 py-2 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:from-slate-600 disabled:to-slate-600 disabled:cursor-not-allowed rounded-lg transition-colors"
              >
                {isGenerating ? (
                  <>
                    <div className="animate-spin h-4 w-4 mr-2 border-2 border-white border-t-transparent rounded-full" />
                    Generating...
                  </>
                ) : (
                  <>
                    <Brain className="h-4 w-4 mr-2" />
                    Generate New Recommendations
                  </>
                )}
              </button>
            </div>
          </div>

          {/* User Profile Summary */}
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
            <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
              <div className="text-slate-400 text-sm mb-1">Risk Tolerance</div>
              <div className="text-white font-semibold capitalize">{userProfile.riskTolerance}</div>
            </div>
            <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
              <div className="text-slate-400 text-sm mb-1">Experience</div>
              <div className="text-white font-semibold capitalize">{userProfile.experience}</div>
            </div>
            <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
              <div className="text-slate-400 text-sm mb-1">Capital</div>
              <div className="text-white font-semibold">₹{(userProfile.capital / 100000).toFixed(1)}L</div>
            </div>
            <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
              <div className="text-slate-400 text-sm mb-1">Time Horizon</div>
              <div className="text-white font-semibold capitalize">{userProfile.timeHorizon}-term</div>
            </div>
            <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
              <div className="text-slate-400 text-sm mb-1">Preferred Assets</div>
              <div className="text-white font-semibold">{userProfile.preferredAssets.join(', ')}</div>
            </div>
          </div>

          {/* Market Conditions */}
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800 mb-8">
            <h2 className="text-lg font-bold text-white mb-4 flex items-center">
              <Activity className="h-5 w-5 mr-2 text-blue-400" />
              Current Market Conditions
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {marketConditions.map((condition, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-slate-800 rounded-lg">
                  <div>
                    <div className="text-white font-medium">{condition.name}</div>
                    <div className="text-slate-400 text-sm">Optimal: {condition.optimal}</div>
                  </div>
                  <div className="text-right">
                    <div className={`font-bold ${
                      condition.impact === 'positive' ? 'text-green-400' :
                      condition.impact === 'negative' ? 'text-red-400' : 'text-yellow-400'
                    }`}>
                      {condition.current}
                    </div>
                    <div className={`text-xs ${
                      condition.impact === 'positive' ? 'text-green-400' :
                      condition.impact === 'negative' ? 'text-red-400' : 'text-yellow-400'
                    }`}>
                      {condition.impact}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Strategy Recommendations */}
        <div className="space-y-6">
          {recommendations.map((strategy, index) => {
            const TypeIcon = getTypeIcon(strategy.type);
            const isExpanded = selectedStrategy === strategy.id;
            
            return (
              <div
                key={strategy.id}
                className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden hover:border-purple-500/50 transition-all"
              >
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-start space-x-4">
                      <div className="flex items-center justify-center w-12 h-12 bg-purple-600/20 rounded-xl">
                        {index === 0 && <Crown className="h-6 w-6 text-yellow-400" />}
                        {index === 1 && <Award className="h-6 w-6 text-silver-400" />}
                        {index === 2 && <Star className="h-6 w-6 text-orange-400" />}
                        {index > 2 && <TypeIcon className="h-6 w-6 text-purple-400" />}
                      </div>
                      <div>
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="text-xl font-bold text-white">{strategy.name}</h3>
                          {index === 0 && (
                            <span className="px-3 py-1 bg-gradient-to-r from-yellow-500 to-orange-500 text-yellow-100 text-sm font-medium rounded-full">
                              #1 Recommended
                            </span>
                          )}
                          {strategy.aiScore > 90 && (
                            <span className="px-2 py-1 bg-purple-600 text-purple-100 text-xs font-medium rounded-full">
                              AI Optimized
                            </span>
                          )}
                        </div>
                        <p className="text-slate-300 mb-3">{strategy.description}</p>
                        <div className="flex items-center space-x-4 text-sm">
                          <span className="text-slate-400">{strategy.assetClass} • {strategy.timeframe}</span>
                          <span className={`px-2 py-1 rounded font-medium ${getRiskColor(strategy.riskLevel)}`}>
                            {strategy.riskLevel} risk
                          </span>
                          <span className={`px-2 py-1 rounded font-medium ${getComplexityColor(strategy.complexity)}`}>
                            {strategy.complexity}
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="text-right">
                      <div className="flex items-center space-x-4 mb-2">
                        <div className="text-center">
                          <div className="text-2xl font-bold text-purple-400">{strategy.aiScore}</div>
                          <div className="text-xs text-slate-400">AI Score</div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-green-400">+{strategy.expectedReturn}%</div>
                          <div className="text-xs text-slate-400">Expected Return</div>
                        </div>
                      </div>
                      <div className="text-sm text-slate-400">
                        Confidence: {strategy.confidence}%
                      </div>
                    </div>
                  </div>

                  {/* Quick Stats */}
                  <div className="grid grid-cols-4 gap-4 mb-6">
                    <div className="text-center p-3 bg-slate-800 rounded-lg">
                      <div className="text-blue-400 font-bold">{strategy.historicalPerformance.winRate}%</div>
                      <div className="text-xs text-slate-400">Win Rate</div>
                    </div>
                    <div className="text-center p-3 bg-slate-800 rounded-lg">
                      <div className="text-green-400 font-bold">{strategy.historicalPerformance.sharpeRatio}</div>
                      <div className="text-xs text-slate-400">Sharpe Ratio</div>
                    </div>
                    <div className="text-center p-3 bg-slate-800 rounded-lg">
                      <div className="text-red-400 font-bold">{strategy.historicalPerformance.maxDrawdown}%</div>
                      <div className="text-xs text-slate-400">Max Drawdown</div>
                    </div>
                    <div className="text-center p-3 bg-slate-800 rounded-lg">
                      <div className="text-purple-400 font-bold">₹{(strategy.implementation.minCapital / 100000).toFixed(0)}L</div>
                      <div className="text-xs text-slate-400">Min Capital</div>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex items-center justify-between">
                    <button
                      onClick={() => setSelectedStrategy(isExpanded ? null : strategy.id)}
                      className="flex items-center px-4 py-2 text-purple-400 hover:text-purple-300 transition-colors"
                    >
                      {isExpanded ? 'Show Less' : 'View Details'}
                      <ArrowRight className={`h-4 w-4 ml-2 transition-transform ${isExpanded ? 'rotate-90' : ''}`} />
                    </button>
                    
                    <div className="flex items-center space-x-3">
                      <Link
                        href="/stocks/backtest/universal"
                        className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                      >
                        <Play className="h-4 w-4 mr-2" />
                        Backtest Strategy
                      </Link>
                      <button className="flex items-center px-4 py-2 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-lg transition-colors">
                        <Zap className="h-4 w-4 mr-2" />
                        Deploy Live
                      </button>
                    </div>
                  </div>
                </div>

                {/* Expanded Details */}
                {isExpanded && (
                  <div className="border-t border-slate-800 p-6 bg-slate-800/50">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                      {/* Key Features */}
                      <div>
                        <h4 className="font-semibold text-white mb-3 flex items-center">
                          <CheckCircle className="h-4 w-4 mr-2 text-green-400" />
                          Key Features
                        </h4>
                        <ul className="space-y-2">
                          {strategy.keyFeatures.map((feature, idx) => (
                            <li key={idx} className="text-sm text-slate-300 flex items-start">
                              <div className="w-1 h-1 bg-purple-400 rounded-full mr-2 mt-2 flex-shrink-0" />
                              {feature}
                            </li>
                          ))}
                        </ul>
                      </div>

                      {/* Pros & Cons */}
                      <div>
                        <h4 className="font-semibold text-white mb-3 flex items-center">
                          <Shield className="h-4 w-4 mr-2 text-blue-400" />
                          Pros & Cons
                        </h4>
                        <div className="space-y-3">
                          <div>
                            <div className="text-green-400 text-sm font-medium mb-1">Advantages:</div>
                            <ul className="space-y-1">
                              {strategy.pros.slice(0, 2).map((pro, idx) => (
                                <li key={idx} className="text-xs text-slate-300">• {pro}</li>
                              ))}
                            </ul>
                          </div>
                          <div>
                            <div className="text-red-400 text-sm font-medium mb-1">Considerations:</div>
                            <ul className="space-y-1">
                              {strategy.cons.slice(0, 2).map((con, idx) => (
                                <li key={idx} className="text-xs text-slate-300">• {con}</li>
                              ))}
                            </ul>
                          </div>
                        </div>
                      </div>

                      {/* Implementation */}
                      <div>
                        <h4 className="font-semibold text-white mb-3 flex items-center">
                          <Settings className="h-4 w-4 mr-2 text-yellow-400" />
                          Implementation
                        </h4>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span className="text-slate-400">Time Commitment:</span>
                            <span className="text-white">{strategy.implementation.timeCommitment}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-400">Difficulty:</span>
                            <span className="text-white">{strategy.implementation.difficulty}/10</span>
                          </div>
                          <div>
                            <span className="text-slate-400">Required Tools:</span>
                            <div className="mt-1">
                              {strategy.implementation.tools.map((tool, idx) => (
                                <span key={idx} className="inline-block px-2 py-1 bg-slate-700 text-xs rounded mr-1 mb-1">
                                  {tool}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}