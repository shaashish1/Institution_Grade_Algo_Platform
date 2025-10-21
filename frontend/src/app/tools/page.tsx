'use client';

import React from 'react';
import Link from 'next/link';
import { 
  Calculator, Target, TrendingUp, Search, AlertTriangle, 
  PieChart, BarChart3, Settings, Zap, Shield, Clock,
  ArrowRight, Star, Activity, DollarSign, Brain, Users
} from 'lucide-react';

interface Tool {
  id: string;
  name: string;
  description: string;
  icon: React.ReactNode;
  href: string;
  category: 'analysis' | 'trading' | 'risk' | 'alerts';
  featured?: boolean;
  status: 'active' | 'beta' | 'coming-soon';
  difficulty: 'beginner' | 'intermediate' | 'advanced';
}

export default function ToolsPage() {
  const tools: Tool[] = [
    {
      id: 'screener',
      name: 'Stock Screener',
      description: 'Advanced stock screening with custom filters and criteria',
      icon: <Search className="h-6 w-6" />,
      href: '/tools/screener',
      category: 'analysis',
      featured: true,
      status: 'active',
      difficulty: 'intermediate'
    },
    {
      id: 'calculator',
      name: 'Options Calculator',
      description: 'Calculate option pricing, Greeks, and profit/loss scenarios',
      icon: <Calculator className="h-6 w-6" />,
      href: '/tools/calculator',
      category: 'trading',
      featured: true,
      status: 'active',
      difficulty: 'beginner'
    },
    {
      id: 'risk',
      name: 'Risk Management',
      description: 'Portfolio risk analysis and position sizing tools',
      icon: <Shield className="h-6 w-6" />,
      href: '/tools/risk',
      category: 'risk',
      featured: true,
      status: 'active',
      difficulty: 'advanced'
    },
    {
      id: 'alerts',
      name: 'Price Alerts',
      description: 'Set custom price alerts and trading notifications',
      icon: <AlertTriangle className="h-6 w-6" />,
      href: '/tools/alerts',
      category: 'alerts',
      status: 'beta',
      difficulty: 'beginner'
    },
    {
      id: 'portfolio-analyzer',
      name: 'Portfolio Analyzer',
      description: 'Comprehensive portfolio performance and allocation analysis',
      icon: <PieChart className="h-6 w-6" />,
      href: '/tools/portfolio',
      category: 'analysis',
      status: 'active',
      difficulty: 'intermediate'
    },
    {
      id: 'volatility-scanner',
      name: 'Volatility Scanner',
      description: 'Identify high volatility stocks and trading opportunities',
      icon: <Activity className="h-6 w-6" />,
      href: '/tools/volatility',
      category: 'analysis',
      status: 'beta',
      difficulty: 'advanced'
    },
    {
      id: 'earnings-calendar',
      name: 'Earnings Calendar',
      description: 'Track upcoming earnings announcements and events',
      icon: <Clock className="h-6 w-6" />,
      href: '/tools/earnings',
      category: 'analysis',
      status: 'active',
      difficulty: 'beginner'
    },
    {
      id: 'correlation-matrix',
      name: 'Correlation Matrix',
      description: 'Analyze correlations between stocks and asset classes',
      icon: <BarChart3 className="h-6 w-6" />,
      href: '/tools/correlation',
      category: 'analysis',
      status: 'coming-soon',
      difficulty: 'advanced'
    },
    {
      id: 'ai-signals',
      name: 'AI Trading Signals',
      description: 'Machine learning powered trading signal generation',
      icon: <Brain className="h-6 w-6" />,
      href: '/tools/ai-signals',
      category: 'trading',
      status: 'coming-soon',
      difficulty: 'advanced'
    },
    {
      id: 'social-sentiment',
      name: 'Social Sentiment',
      description: 'Track social media sentiment and market mood',
      icon: <Users className="h-6 w-6" />,
      href: '/tools/sentiment',
      category: 'analysis',
      status: 'beta',
      difficulty: 'intermediate'
    }
  ];

  const categories = {
    analysis: { name: 'Analysis Tools', color: 'blue' },
    trading: { name: 'Trading Tools', color: 'green' },
    risk: { name: 'Risk Management', color: 'red' },
    alerts: { name: 'Alerts & Notifications', color: 'yellow' }
  };

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

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'text-green-400';
      case 'intermediate': return 'text-yellow-400';
      case 'advanced': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const featuredTools = tools.filter(tool => tool.featured);

  return (
    <div className="min-h-screen bg-slate-900 text-white">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 py-16">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-4">Trading Tools & Analytics</h1>
            <p className="text-xl text-blue-100 max-w-3xl mx-auto">
              Professional-grade tools for market analysis, risk management, and trading optimization
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Breadcrumb */}
        <nav className="mb-8">
          <div className="flex items-center space-x-2 text-sm text-slate-400">
            <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
            <ArrowRight className="h-4 w-4" />
            <span className="text-white">Tools</span>
          </div>
        </nav>

        {/* Featured Tools */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-6 flex items-center">
            <Star className="h-6 w-6 text-yellow-400 mr-2" />
            Featured Tools
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredTools.map((tool) => (
              <Link key={tool.id} href={tool.href} className="group">
                <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 hover:border-blue-500 transition-all duration-200 group-hover:shadow-lg group-hover:shadow-blue-500/10">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="p-2 bg-blue-500/20 rounded-lg text-blue-400">
                        {tool.icon}
                      </div>
                      <div>
                        <h3 className="font-semibold text-lg group-hover:text-blue-400 transition-colors">
                          {tool.name}
                        </h3>
                        <span className={`text-sm ${getDifficultyColor(tool.difficulty)}`}>
                          {tool.difficulty}
                        </span>
                      </div>
                    </div>
                    {getStatusBadge(tool.status)}
                  </div>
                  <p className="text-slate-400 text-sm mb-4">{tool.description}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-slate-500 capitalize">
                      {categories[tool.category].name}
                    </span>
                    <ArrowRight className="h-4 w-4 text-slate-400 group-hover:text-blue-400 transition-colors" />
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </section>

        {/* All Tools by Category */}
        <section>
          <h2 className="text-2xl font-bold mb-8">All Tools</h2>
          
          {Object.entries(categories).map(([categoryKey, categoryInfo]) => {
            const categoryTools = tools.filter(tool => tool.category === categoryKey);
            if (categoryTools.length === 0) return null;

            return (
              <div key={categoryKey} className="mb-8">
                <h3 className="text-xl font-semibold mb-4 flex items-center">
                  <div className={`w-3 h-3 rounded-full bg-${categoryInfo.color}-500 mr-3`}></div>
                  {categoryInfo.name}
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                  {categoryTools.map((tool) => (
                    <Link key={tool.id} href={tool.href} className="group">
                      <div className="bg-slate-800 rounded-lg p-4 border border-slate-700 hover:border-slate-600 transition-all duration-200 group-hover:shadow-md">
                        <div className="flex items-center space-x-3 mb-3">
                          <div className="p-2 bg-slate-700 rounded-lg text-slate-400 group-hover:text-white transition-colors">
                            {tool.icon}
                          </div>
                          <div className="flex-1">
                            <h4 className="font-medium group-hover:text-blue-400 transition-colors">
                              {tool.name}
                            </h4>
                            <span className={`text-xs ${getDifficultyColor(tool.difficulty)}`}>
                              {tool.difficulty}
                            </span>
                          </div>
                          {getStatusBadge(tool.status)}
                        </div>
                        <p className="text-slate-400 text-sm">{tool.description}</p>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>
            );
          })}
        </section>

        {/* Quick Access */}
        <section className="mt-12 bg-slate-800 rounded-lg p-8">
          <h3 className="text-xl font-semibold mb-6">Quick Access</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Link href="/stocks" className="flex items-center space-x-2 p-3 bg-slate-700 rounded-lg hover:bg-slate-600 transition-colors">
              <TrendingUp className="h-5 w-5 text-green-400" />
              <span>Stocks</span>
            </Link>
            <Link href="/crypto" className="flex items-center space-x-2 p-3 bg-slate-700 rounded-lg hover:bg-slate-600 transition-colors">
              <Zap className="h-5 w-5 text-yellow-400" />
              <span>Crypto</span>
            </Link>
            <Link href="/portfolio" className="flex items-center space-x-2 p-3 bg-slate-700 rounded-lg hover:bg-slate-600 transition-colors">
              <PieChart className="h-5 w-5 text-blue-400" />
              <span>Portfolio</span>
            </Link>
            <Link href="/strategies" className="flex items-center space-x-2 p-3 bg-slate-700 rounded-lg hover:bg-slate-600 transition-colors">
              <Target className="h-5 w-5 text-purple-400" />
              <span>Strategies</span>
            </Link>
          </div>
        </section>
      </div>
    </div>
  );
}