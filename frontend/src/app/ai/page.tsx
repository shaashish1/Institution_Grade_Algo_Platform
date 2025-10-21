'use client';

import React from 'react';
import Link from 'next/link';
import { 
  Brain, Lightbulb, Search, Shield, Globe, TrendingUp,
  ArrowRight, Zap, Target, Activity, Star, Clock,
  BarChart3, Users, Bot, Cpu, Eye, Rocket
} from 'lucide-react';

interface AITool {
  id: string;
  name: string;
  description: string;
  icon: React.ReactNode;
  href: string;
  status: 'active' | 'beta' | 'coming-soon';
  accuracy?: string;
  features: string[];
}

export default function AIPage() {
  const aiTools: AITool[] = [
    {
      id: 'strategies',
      name: 'Strategy Recommender',
      description: 'AI-powered trading strategy recommendations based on market conditions and your portfolio',
      icon: <Lightbulb className="h-8 w-8" />,
      href: '/ai/strategies',
      status: 'beta',
      accuracy: '87%',
      features: ['Market Analysis', 'Risk Assessment', 'Performance Prediction', 'Custom Optimization']
    },
    {
      id: 'analysis',
      name: 'Trade Analysis',
      description: 'Intelligent analysis of trade opportunities using machine learning algorithms',
      icon: <Search className="h-8 w-8" />,
      href: '/ai/analysis',
      status: 'beta',
      accuracy: '92%',
      features: ['Pattern Recognition', 'Volume Analysis', 'Price Prediction', 'Sentiment Integration']
    },
    {
      id: 'risk',
      name: 'Risk Assessment',
      description: 'Advanced risk evaluation using AI models trained on historical market data',
      icon: <Shield className="h-8 w-8" />,
      href: '/ai/risk',
      status: 'active',
      accuracy: '95%',
      features: ['Portfolio Risk', 'Correlation Analysis', 'Stress Testing', 'VaR Calculation']
    },
    {
      id: 'sentiment',
      name: 'Market Sentiment',
      description: 'Real-time sentiment analysis from news, social media, and market indicators',
      icon: <Globe className="h-8 w-8" />,
      href: '/ai/sentiment',
      status: 'active',
      accuracy: '89%',
      features: ['News Analysis', 'Social Sentiment', 'Market Psychology', 'Fear & Greed Index']
    },
    {
      id: 'optimization',
      name: 'Portfolio Optimizer',
      description: 'AI-driven portfolio optimization for maximum risk-adjusted returns',
      icon: <Target className="h-8 w-8" />,
      href: '/ai/optimization',
      status: 'coming-soon',
      features: ['Mean Reversion', 'Momentum Factors', 'Risk Parity', 'Black-Litterman']
    },
    {
      id: 'prediction',
      name: 'Price Prediction',
      description: 'Advanced machine learning models for price movement forecasting',
      icon: <TrendingUp className="h-8 w-8" />,
      href: '/ai/prediction',
      status: 'coming-soon',
      features: ['LSTM Networks', 'Transformer Models', 'Ensemble Methods', 'Feature Engineering']
    }
  ];

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'active':
        return <span className="px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded-full">Active</span>;
      case 'beta':
        return <span className="px-2 py-1 bg-yellow-500/20 text-yellow-400 text-xs rounded-full">Beta</span>;
      case 'coming-soon':
        return <span className="px-2 py-1 bg-gray-500/20 text-gray-400 text-xs rounded-full">Coming Soon</span>;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-purple-600 via-blue-600 to-cyan-600 py-20">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <div className="flex items-center justify-center space-x-3 mb-6">
            <Brain className="h-12 w-12 text-white" />
            <h1 className="text-5xl font-bold">AI Trading Tools</h1>
          </div>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto mb-8">
            Harness the power of artificial intelligence to enhance your trading decisions, 
            optimize strategies, and manage risk with cutting-edge machine learning algorithms.
          </p>
          <div className="flex items-center justify-center space-x-8 text-sm">
            <div className="flex items-center space-x-2">
              <Cpu className="h-5 w-5" />
              <span>Advanced ML Models</span>
            </div>
            <div className="flex items-center space-x-2">
              <Zap className="h-5 w-5" />
              <span>Real-time Analysis</span>
            </div>
            <div className="flex items-center space-x-2">
              <Shield className="h-5 w-5" />
              <span>Risk Optimized</span>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Breadcrumb */}
        <nav className="mb-8">
          <div className="flex items-center space-x-2 text-sm text-slate-400">
            <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
            <ArrowRight className="h-4 w-4" />
            <span className="text-white">AI Tools</span>
          </div>
        </nav>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <div className="bg-slate-800 rounded-lg p-6 text-center">
            <Bot className="h-8 w-8 text-blue-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-white mb-1">6</div>
            <div className="text-sm text-slate-400">AI Tools</div>
          </div>
          <div className="bg-slate-800 rounded-lg p-6 text-center">
            <Activity className="h-8 w-8 text-green-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-white mb-1">91%</div>
            <div className="text-sm text-slate-400">Avg. Accuracy</div>
          </div>
          <div className="bg-slate-800 rounded-lg p-6 text-center">
            <Clock className="h-8 w-8 text-yellow-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-white mb-1">24/7</div>
            <div className="text-sm text-slate-400">Real-time</div>
          </div>
          <div className="bg-slate-800 rounded-lg p-6 text-center">
            <Users className="h-8 w-8 text-purple-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-white mb-1">1000+</div>
            <div className="text-sm text-slate-400">Active Users</div>
          </div>
        </div>

        {/* AI Tools Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {aiTools.map((tool) => (
            <div key={tool.id} className="bg-slate-800 rounded-lg p-8 border border-slate-700 hover:border-blue-500 transition-all duration-200 group">
              <div className="flex items-start justify-between mb-6">
                <div className="flex items-center space-x-4">
                  <div className="p-3 bg-blue-500/20 rounded-lg text-blue-400 group-hover:bg-blue-500/30 transition-colors">
                    {tool.icon}
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold text-white mb-1">{tool.name}</h3>
                    {tool.accuracy && (
                      <div className="flex items-center space-x-2">
                        <Star className="h-4 w-4 text-yellow-400" />
                        <span className="text-sm text-yellow-400">{tool.accuracy} accuracy</span>
                      </div>
                    )}
                  </div>
                </div>
                {getStatusBadge(tool.status)}
              </div>

              <p className="text-slate-300 mb-6">{tool.description}</p>

              <div className="mb-6">
                <h4 className="text-sm font-medium text-slate-400 mb-3">Key Features:</h4>
                <div className="grid grid-cols-2 gap-2">
                  {tool.features.map((feature, index) => (
                    <div key={index} className="flex items-center space-x-2 text-sm">
                      <div className="w-1.5 h-1.5 bg-blue-400 rounded-full"></div>
                      <span className="text-slate-300">{feature}</span>
                    </div>
                  ))}
                </div>
              </div>

              <Link 
                href={tool.href}
                className={`flex items-center justify-center space-x-2 w-full py-3 rounded-lg font-medium transition-all duration-200 ${
                  tool.status === 'coming-soon' 
                    ? 'bg-slate-700 text-slate-400 cursor-not-allowed' 
                    : 'bg-blue-500 hover:bg-blue-600 text-white group-hover:shadow-lg group-hover:shadow-blue-500/20'
                }`}
                onClick={tool.status === 'coming-soon' ? (e) => e.preventDefault() : undefined}
              >
                {tool.status === 'coming-soon' ? (
                  <>
                    <Clock className="h-4 w-4" />
                    <span>Coming Soon</span>
                  </>
                ) : (
                  <>
                    <Eye className="h-4 w-4" />
                    <span>Launch Tool</span>
                    <ArrowRight className="h-4 w-4" />
                  </>
                )}
              </Link>
            </div>
          ))}
        </div>

        {/* Features Section */}
        <div className="bg-slate-800 rounded-lg p-8 mb-12">
          <h2 className="text-2xl font-bold mb-6 text-center">Why Choose AI-Powered Trading?</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <Rocket className="h-12 w-12 text-blue-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">Enhanced Performance</h3>
              <p className="text-slate-400">AI algorithms can process vast amounts of data and identify patterns humans might miss</p>
            </div>
            <div className="text-center">
              <Shield className="h-12 w-12 text-green-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">Risk Management</h3>
              <p className="text-slate-400">Advanced risk models help protect your portfolio from unexpected market movements</p>
            </div>
            <div className="text-center">
              <Clock className="h-12 w-12 text-yellow-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">24/7 Monitoring</h3>
              <p className="text-slate-400">AI never sleeps - continuous market monitoring and opportunity detection</p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-8">
          <h2 className="text-2xl font-bold mb-4">Ready to Enhance Your Trading?</h2>
          <p className="text-blue-100 mb-6">Join thousands of traders using AI to improve their performance</p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/ai/strategies" className="px-6 py-3 bg-white text-blue-600 rounded-lg font-medium hover:bg-blue-50 transition-colors">
              Start with Strategy Recommender
            </Link>
            <Link href="/ai/analysis" className="px-6 py-3 bg-blue-700 hover:bg-blue-800 text-white rounded-lg font-medium transition-colors">
              Try Trade Analysis
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}