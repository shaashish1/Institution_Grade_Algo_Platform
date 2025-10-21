'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { 
  ArrowRight, FileCode, Upload, Zap, Code, Brain, 
  TrendingUp, BarChart3, Target, Settings, Eye, Play,
  Download, Plus, Search, Filter, Star, Clock
} from 'lucide-react';
import { PineScriptUpload } from '@/components/trading/pine-script-upload';

interface Strategy {
  id: string;
  name: string;
  fileName: string;
  description: string;
  author: string;
  version: string;
  status: 'active' | 'paused' | 'testing' | 'archived';
  performance: {
    return: number;
    sharpe: number;
    maxDrawdown: number;
    trades: number;
  };
  timeframe: string;
  lastUpdated: string;
  category: 'trend' | 'reversal' | 'scalping' | 'swing';
  rating: number;
}

export default function PineScriptPage() {
  const [view, setView] = useState<'upload' | 'library' | 'templates'>('upload');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState<'all' | string>('all');

  const strategies: Strategy[] = [
    {
      id: '1',
      name: 'Advanced RSI Divergence',
      fileName: 'rsi_divergence_v2.pine',
      description: 'Advanced RSI divergence strategy with multi-timeframe analysis',
      author: 'TradingPro',
      version: '2.0',
      status: 'active',
      performance: { return: 23.5, sharpe: 1.8, maxDrawdown: -8.2, trades: 156 },
      timeframe: '1H',
      lastUpdated: '2024-01-15',
      category: 'reversal',
      rating: 4.5
    },
    {
      id: '2',
      name: 'Bollinger Breakout System',
      fileName: 'bb_breakout.pine',
      description: 'Bollinger Band breakout strategy with volume confirmation',
      author: 'AlgoMaster',
      version: '1.3',
      status: 'testing',
      performance: { return: 31.2, sharpe: 2.1, maxDrawdown: -12.4, trades: 89 },
      timeframe: '15M',
      lastUpdated: '2024-01-10',
      category: 'trend',
      rating: 4.2
    },
    {
      id: '3',
      name: 'EMA Crossover Plus',
      fileName: 'ema_cross_enhanced.pine',
      description: 'Enhanced EMA crossover with momentum filters',
      author: 'QuantTrader',
      version: '1.0',
      status: 'paused',
      performance: { return: 18.7, sharpe: 1.6, maxDrawdown: -6.8, trades: 203 },
      timeframe: '4H',
      lastUpdated: '2024-01-08',
      category: 'trend',
      rating: 3.9
    }
  ];

  const templates = [
    { id: '1', name: 'Basic Strategy Template', description: 'Simple strategy framework with entry/exit logic' },
    { id: '2', name: 'Indicator Template', description: 'Custom indicator with plotting and alerts' },
    { id: '3', name: 'Multi-Timeframe Template', description: 'Strategy using multiple timeframes' },
    { id: '4', name: 'Risk Management Template', description: 'Advanced risk and money management' }
  ];

  const filteredStrategies = strategies.filter(strategy => {
    const matchesSearch = strategy.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         strategy.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterCategory === 'all' || strategy.category === filterCategory;
    return matchesSearch && matchesFilter;
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-400 bg-green-400/10';
      case 'testing': return 'text-yellow-400 bg-yellow-400/10';
      case 'paused': return 'text-gray-400 bg-gray-400/10';
      case 'archived': return 'text-red-400 bg-red-400/10';
      default: return 'text-gray-400 bg-gray-400/10';
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'trend': return 'text-blue-400 bg-blue-400/10';
      case 'reversal': return 'text-purple-400 bg-purple-400/10';
      case 'scalping': return 'text-orange-400 bg-orange-400/10';
      case 'swing': return 'text-green-400 bg-green-400/10';
      default: return 'text-gray-400 bg-gray-400/10';
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 py-12">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center space-x-3 mb-4">
            <FileCode className="h-8 w-8 text-white" />
            <h1 className="text-3xl font-bold">Pine Script Manager</h1>
          </div>
          <p className="text-lg text-blue-100 max-w-3xl">
            Upload, manage, and deploy your TradingView Pine Script strategies. 
            Validate scripts automatically and integrate with our backtesting engine.
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Breadcrumb */}
        <nav className="mb-6">
          <div className="flex items-center space-x-2 text-sm text-slate-400">
            <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
            <ArrowRight className="h-4 w-4" />
            <Link href="/strategies" className="hover:text-blue-400 transition-colors">Strategies</Link>
            <ArrowRight className="h-4 w-4" />
            <span className="text-white">Pine Script</span>
          </div>
        </nav>

        {/* Navigation Tabs */}
        <div className="bg-slate-800 rounded-lg p-1 mb-8">
          <div className="flex space-x-1">
            {[
              { id: 'upload', label: 'Upload Scripts', icon: Upload },
              { id: 'library', label: 'Script Library', icon: FileCode },
              { id: 'templates', label: 'Templates', icon: Code }
            ].map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                onClick={() => setView(id as any)}
                className={`flex-1 flex items-center justify-center space-x-2 px-4 py-3 rounded-lg transition-all duration-200 ${
                  view === id 
                    ? 'bg-blue-500 text-white shadow-lg' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-700'
                }`}
              >
                <Icon className="h-5 w-5" />
                <span>{label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        {view === 'upload' && (
          <div>
            <div className="mb-8">
              <h2 className="text-2xl font-bold mb-4">Upload Pine Script Files</h2>
              <p className="text-slate-400 mb-6">
                Upload your Pine Script (.pine) files to validate syntax, extract metadata, 
                and deploy as trading strategies.
              </p>
            </div>
            
            <PineScriptUpload 
              onFileUpload={(file) => console.log('File uploaded:', file)}
              onFileDelete={(id) => console.log('File deleted:', id)}
              onFileDeploy={(id) => console.log('File deployed:', id)}
            />
          </div>
        )}

        {view === 'library' && (
          <div>
            <div className="flex flex-col lg:flex-row gap-4 items-center justify-between mb-8">
              <div>
                <h2 className="text-2xl font-bold mb-2">Script Library</h2>
                <p className="text-slate-400">Manage and monitor your deployed Pine Script strategies</p>
              </div>
              
              <div className="flex gap-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                  <input
                    type="text"
                    placeholder="Search strategies..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10 pr-4 py-2 bg-slate-700 border border-slate-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                
                <select
                  value={filterCategory}
                  onChange={(e) => setFilterCategory(e.target.value)}
                  className="px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">All Categories</option>
                  <option value="trend">Trend Following</option>
                  <option value="reversal">Mean Reversion</option>
                  <option value="scalping">Scalping</option>
                  <option value="swing">Swing Trading</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
              {filteredStrategies.map((strategy) => (
                <div key={strategy.id} className="bg-slate-800 rounded-lg p-6 border border-slate-700 hover:border-blue-500 transition-all duration-200">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="font-semibold text-lg text-white mb-1">{strategy.name}</h3>
                      <p className="text-sm text-slate-400">{strategy.fileName}</p>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Star className="h-4 w-4 text-yellow-400" />
                      <span className="text-sm text-white">{strategy.rating}</span>
                    </div>
                  </div>

                  <p className="text-slate-300 text-sm mb-4">{strategy.description}</p>

                  <div className="space-y-2 mb-4">
                    <div className="flex justify-between">
                      <span className="text-slate-400 text-sm">Return:</span>
                      <span className="text-green-400 font-medium">+{strategy.performance.return}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400 text-sm">Sharpe Ratio:</span>
                      <span className="text-white">{strategy.performance.sharpe}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400 text-sm">Max Drawdown:</span>
                      <span className="text-red-400">{strategy.performance.maxDrawdown}%</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between mb-4">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(strategy.status)}`}>
                      {strategy.status}
                    </span>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${getCategoryColor(strategy.category)}`}>
                      {strategy.category}
                    </span>
                  </div>

                  <div className="flex space-x-2">
                    <button className="flex-1 px-3 py-2 bg-blue-500 hover:bg-blue-600 rounded text-sm transition-colors">
                      <Eye className="h-4 w-4 mx-auto" />
                    </button>
                    <button className="flex-1 px-3 py-2 bg-green-500 hover:bg-green-600 rounded text-sm transition-colors">
                      <Play className="h-4 w-4 mx-auto" />
                    </button>
                    <button className="flex-1 px-3 py-2 bg-purple-500 hover:bg-purple-600 rounded text-sm transition-colors">
                      <BarChart3 className="h-4 w-4 mx-auto" />
                    </button>
                    <button className="flex-1 px-3 py-2 bg-slate-600 hover:bg-slate-500 rounded text-sm transition-colors">
                      <Settings className="h-4 w-4 mx-auto" />
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {filteredStrategies.length === 0 && (
              <div className="text-center py-12">
                <FileCode className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-slate-300 mb-2">No strategies found</h3>
                <p className="text-slate-400 mb-4">Try adjusting your search or upload some Pine Scripts</p>
                <button 
                  onClick={() => setView('upload')}
                  className="px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg transition-colors"
                >
                  Upload Scripts
                </button>
              </div>
            )}
          </div>
        )}

        {view === 'templates' && (
          <div>
            <div className="mb-8">
              <h2 className="text-2xl font-bold mb-4">Pine Script Templates</h2>
              <p className="text-slate-400 mb-6">
                Start with pre-built templates to accelerate your Pine Script development
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              {templates.map((template) => (
                <div key={template.id} className="bg-slate-800 rounded-lg p-6 border border-slate-700 hover:border-blue-500 transition-all duration-200">
                  <h3 className="font-semibold text-lg text-white mb-2">{template.name}</h3>
                  <p className="text-slate-300 mb-4">{template.description}</p>
                  <div className="flex space-x-3">
                    <button className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg text-sm transition-colors">
                      <Download className="h-4 w-4 inline mr-2" />
                      Download
                    </button>
                    <button className="px-4 py-2 bg-slate-600 hover:bg-slate-500 text-white rounded-lg text-sm transition-colors">
                      <Eye className="h-4 w-4 inline mr-2" />
                      Preview
                    </button>
                  </div>
                </div>
              ))}
            </div>

            <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
              <h3 className="font-semibold text-lg text-white mb-4">AI Script Generator</h3>
              <p className="text-slate-300 mb-4">
                Use our AI to generate custom Pine Script code based on your requirements
              </p>
              <button className="px-6 py-3 bg-purple-500 hover:bg-purple-600 text-white rounded-lg transition-colors">
                <Brain className="h-5 w-5 inline mr-2" />
                Generate AI Script
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}