'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { 
  TrendingUp, BarChart3, Target, Zap, Settings, Activity,
  DollarSign, Brain, PieChart, LineChart, Shield, Coins,
  Building2, Globe, Monitor, Eye, Search, ChevronRight
} from 'lucide-react';

interface SitemapLink {
  name: string;
  href: string;
  description: string;
  icon: any;
  badge?: string;
}

interface SitemapCategory {
  title: string;
  description: string;
  icon: any;
  color: string;
  links: SitemapLink[];
}

export default function SitemapPage() {
  const [searchQuery, setSearchQuery] = useState('');

  const categories: SitemapCategory[] = [
    {
      title: 'Core Platform',
      description: 'Essential trading and management tools',
      icon: TrendingUp,
      color: 'from-blue-500 to-purple-600',
      links: [
        { name: 'Home', href: '/', description: 'Platform homepage with overview', icon: Globe },
        { name: 'Dashboard', href: '/dashboard', description: 'Unified trading dashboard', icon: Monitor },
        { name: 'Live Trading', href: '/trading', description: 'Real-time trading interface', icon: TrendingUp, badge: 'Live' },
        { name: 'Market Analysis', href: '/analysis', description: 'Technical & fundamental analysis', icon: BarChart3 },
        { name: 'Order Management', href: '/orders', description: 'Track and manage all orders', icon: Zap },
        { name: 'Portfolio', href: '/portfolio', description: 'Portfolio tracking and management', icon: DollarSign },
        { name: 'Settings', href: '/settings', description: 'Configure platform preferences', icon: Settings },
      ]
    },
    {
      title: 'Stock Trading (NSE)',
      description: 'Indian stock market trading tools',
      icon: Target,
      color: 'from-green-500 to-emerald-600',
      links: [
        { name: 'Stock Markets', href: '/stocks', description: 'Browse NSE listed stocks', icon: Building2 },
        { name: 'Option Chain', href: '/stocks/option-chain', description: 'Real-time NSE option chain', icon: Target, badge: 'Live' },
        { name: 'Complete Option Chain', href: '/stocks/option-chain/complete', description: 'All strikes option analysis', icon: Eye, badge: 'New' },
        { name: 'Derivatives & IPO', href: '/stocks/derivatives', description: 'Futures, options, and IPO hub', icon: LineChart },
        { name: 'NSE Trading', href: '/stocks/nse-trading', description: 'NIFTY 50 & 100 trading', icon: TrendingUp },
        { name: 'ETF Trading', href: '/stocks/etf', description: 'Exchange-traded funds', icon: PieChart },
      ]
    },
    {
      title: 'Backtesting & Strategies',
      description: 'Test and optimize trading strategies',
      icon: BarChart3,
      color: 'from-purple-500 to-pink-600',
      links: [
        { name: 'Strategies', href: '/strategies', description: 'Browse all trading strategies', icon: Brain },
        { name: 'Universal Backtesting', href: '/stocks/backtest/universal', description: 'AI-powered strategy optimizer', icon: Brain, badge: 'AI' },
        { name: 'Multi-Strategy Compare', href: '/stocks/backtest/multi-strategy', description: 'Compare multiple strategies', icon: BarChart3 },
        { name: 'NSE Backtesting', href: '/stocks/backtest', description: 'Historical NSE data testing', icon: Activity },
        { name: 'Crypto Backtesting', href: '/crypto/backtest', description: 'Cryptocurrency strategy testing', icon: Coins },
      ]
    },
    {
      title: 'Cryptocurrency',
      description: 'Multi-exchange crypto trading',
      icon: Coins,
      color: 'from-yellow-500 to-orange-600',
      links: [
        { name: 'Crypto Markets', href: '/crypto', description: 'Multi-exchange crypto trading', icon: Coins },
        { name: 'Crypto Backtesting', href: '/crypto/backtest', description: 'Test crypto strategies', icon: Activity },
        { name: 'Exchanges', href: '/exchanges', description: 'View all supported exchanges', icon: Building2 },
      ]
    },
    {
      title: 'AI & Analytics',
      description: 'Artificial intelligence powered tools',
      icon: Brain,
      color: 'from-indigo-500 to-blue-600',
      links: [
        { name: 'AI Tools', href: '/ai', description: 'AI-powered trading tools', icon: Brain, badge: 'AI' },
        { name: 'Strategy Recommender', href: '/ai/strategies', description: 'AI strategy recommendations', icon: Brain, badge: 'Beta' },
        { name: 'Analytics', href: '/analytics', description: 'Performance analytics dashboard', icon: LineChart },
        { name: 'Reports', href: '/reports', description: 'Generate detailed reports', icon: BarChart3 },
        { name: 'Advanced Charts', href: '/charts', description: 'Professional charting tools', icon: LineChart, badge: 'Pro' },
      ]
    },
    {
      title: 'Tools & Utilities',
      description: 'Additional platform features',
      icon: Zap,
      color: 'from-pink-500 to-rose-600',
      links: [
        { name: 'Tools Hub', href: '/tools', description: 'All platform tools', icon: Zap },
        { name: 'Theme Customization', href: '/theme', description: 'Customize platform appearance', icon: Settings },
        { name: 'QA & Testing', href: '/qa', description: 'Quality assurance tools', icon: Shield },
        { name: 'Intranet', href: '/intranet', description: 'Corporate network management', icon: Globe, badge: 'Admin' },
      ]
    },
    {
      title: 'Information & Support',
      description: 'Learn about the platform',
      icon: Shield,
      color: 'from-slate-500 to-slate-600',
      links: [
        { name: 'About Us', href: '/about', description: 'Learn about AlgoProject', icon: Building2 },
        { name: 'Terms of Service', href: '/terms', description: 'Platform terms and conditions', icon: Shield },
        { name: 'Privacy Policy', href: '/privacy', description: 'How we protect your data', icon: Shield },
        { name: 'Risk Disclosure', href: '/risk-disclosure', description: 'Trading risk warnings', icon: Shield },
        { name: 'API Health', href: '/api/health', description: 'Check API status', icon: Activity },
      ]
    },
  ];

  // Flatten all links for search
  const allLinks = categories.flatMap(cat => 
    cat.links.map(link => ({
      ...link,
      category: cat.title
    }))
  );

  // Filter based on search
  const filteredCategories = searchQuery
    ? categories.map(cat => ({
        ...cat,
        links: cat.links.filter(link =>
          link.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
          link.description.toLowerCase().includes(searchQuery.toLowerCase())
        )
      })).filter(cat => cat.links.length > 0)
    : categories;

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Breadcrumb */}
      <div className="bg-slate-900 border-b border-slate-800 px-6 py-4">
        <nav className="flex items-center space-x-2 text-sm text-slate-400">
          <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
          <span>/</span>
          <span className="text-white">Sitemap</span>
        </nav>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-4">
            Platform Sitemap
          </h1>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto mb-8">
            Navigate through all available pages and features on AlgoProject trading platform
          </p>

          {/* Search */}
          <div className="max-w-2xl mx-auto">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-slate-400" />
              <input
                type="text"
                placeholder="Search for pages, features, or tools..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-12 pr-4 py-4 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>

        {/* Stats Bar */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-center">
            <div className="text-3xl font-bold text-blue-400 mb-2">{categories.length}</div>
            <div className="text-sm text-slate-400">Categories</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-center">
            <div className="text-3xl font-bold text-purple-400 mb-2">{allLinks.length}</div>
            <div className="text-sm text-slate-400">Total Pages</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-center">
            <div className="text-3xl font-bold text-green-400 mb-2">
              {allLinks.filter(l => l.badge === 'Live').length}
            </div>
            <div className="text-sm text-slate-400">Live Features</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-center">
            <div className="text-3xl font-bold text-yellow-400 mb-2">
              {allLinks.filter(l => l.badge === 'AI' || l.badge === 'Beta').length}
            </div>
            <div className="text-sm text-slate-400">AI Tools</div>
          </div>
        </div>

        {/* Categories */}
        <div className="space-y-8">
          {filteredCategories.map((category, index) => {
            const CategoryIcon = category.icon;
            return (
              <div key={index} className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
                {/* Category Header */}
                <div className={`bg-gradient-to-r ${category.color} p-6`}>
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center">
                      <CategoryIcon className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <h2 className="text-2xl font-bold text-white">{category.title}</h2>
                      <p className="text-white/80 mt-1">{category.description}</p>
                    </div>
                  </div>
                </div>

                {/* Links Grid */}
                <div className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {category.links.map((link, linkIndex) => {
                      const LinkIcon = link.icon;
                      return (
                        <Link
                          key={linkIndex}
                          href={link.href}
                          className="group bg-slate-800/50 hover:bg-slate-800 border border-slate-700 hover:border-blue-500 rounded-xl p-4 transition-all duration-200"
                        >
                          <div className="flex items-start space-x-3">
                            <div className="w-10 h-10 bg-blue-500/10 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:bg-blue-500/20 transition-colors">
                              <LinkIcon className="h-5 w-5 text-blue-400" />
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center space-x-2 mb-1">
                                <h3 className="font-semibold text-white group-hover:text-blue-400 transition-colors">
                                  {link.name}
                                </h3>
                                {link.badge && (
                                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                                    link.badge === 'Live' ? 'bg-green-500/20 text-green-400' :
                                    link.badge === 'AI' || link.badge === 'Beta' ? 'bg-purple-500/20 text-purple-400' :
                                    link.badge === 'New' ? 'bg-blue-500/20 text-blue-400' :
                                    link.badge === 'Pro' ? 'bg-yellow-500/20 text-yellow-400' :
                                    'bg-slate-500/20 text-slate-400'
                                  }`}>
                                    {link.badge}
                                  </span>
                                )}
                              </div>
                              <p className="text-sm text-slate-400 group-hover:text-slate-300 transition-colors line-clamp-2">
                                {link.description}
                              </p>
                              <div className="flex items-center space-x-1 mt-2 text-xs text-blue-400 opacity-0 group-hover:opacity-100 transition-opacity">
                                <span>Visit page</span>
                                <ChevronRight className="h-3 w-3" />
                              </div>
                            </div>
                          </div>
                        </Link>
                      );
                    })}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* No Results */}
        {filteredCategories.length === 0 && (
          <div className="text-center py-12">
            <Search className="h-16 w-16 text-slate-600 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-slate-300 mb-2">No pages found</h3>
            <p className="text-slate-400">Try adjusting your search terms</p>
          </div>
        )}

        {/* Quick Stats */}
        <div className="mt-12 bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-2xl p-8">
          <div className="text-center">
            <h3 className="text-2xl font-bold text-white mb-4">Can't find what you're looking for?</h3>
            <p className="text-slate-300 mb-6 max-w-2xl mx-auto">
              Our platform is constantly growing with new features. If you need help or have suggestions, 
              our support team is here to assist you 24/7.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
              <Link
                href="/api/health"
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
              >
                Check System Status
              </Link>
              <Link
                href="/"
                className="px-6 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-medium transition-colors"
              >
                Back to Home
              </Link>
            </div>
          </div>
        </div>

        {/* Footer Info */}
        <div className="mt-8 text-center text-sm text-slate-400">
          <p>
            Last updated: {new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
          </p>
          <p className="mt-2">
            Showing {filteredCategories.reduce((acc, cat) => acc + cat.links.length, 0)} of {allLinks.length} pages
          </p>
        </div>
      </div>
    </div>
  );
}
