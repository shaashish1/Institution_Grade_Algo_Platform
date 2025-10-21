'use client';

import React, { useState, useEffect } from 'react';
import { 
  Upload, Download, Play, Pause, BarChart3, TrendingUp, 
  Code, FileText, Settings, Star, Clock, DollarSign,
  Plus, Search, Filter, Grid, List, Eye
} from 'lucide-react';

interface Strategy {
  id: string;
  name: string;
  type: 'pinescript' | 'python' | 'built-in';
  description: string;
  performance: {
    returns: number;
    sharpe: number;
    maxDrawdown: number;
    winRate: number;
  };
  status: 'active' | 'inactive' | 'backtesting';
  timeframe: string;
  markets: string[];
  lastUpdated: string;
  rating: number;
  tags: string[];
}

export default function StrategiesPage() {
  const [strategies, setStrategies] = useState<Strategy[]>([]);
  const [selectedStrategies, setSelectedStrategies] = useState<string[]>([]);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState<'all' | 'pinescript' | 'python' | 'built-in'>('all');

  useEffect(() => {
    // Load strategies from backend
    loadStrategies();
  }, []);

  const loadStrategies = async () => {
    try {
      // Mock data for now - will connect to backend strategies folder
      const mockStrategies: Strategy[] = [
        {
          id: '1',
          name: 'Moving Average Crossover',
          type: 'built-in',
          description: 'Classic MA crossover strategy with risk management',
          performance: { returns: 24.5, sharpe: 1.8, maxDrawdown: -8.2, winRate: 67 },
          status: 'active',
          timeframe: '1D',
          markets: ['NSE', 'Crypto'],
          lastUpdated: '2025-10-20',
          rating: 4.2,
          tags: ['trend-following', 'beginner-friendly']
        },
        {
          id: '2',
          name: 'RSI Mean Reversion',
          type: 'python',
          description: 'RSI-based mean reversion with dynamic position sizing',
          performance: { returns: 18.3, sharpe: 2.1, maxDrawdown: -5.8, winRate: 73 },
          status: 'active',
          timeframe: '4H',
          markets: ['NSE'],
          lastUpdated: '2025-10-19',
          rating: 4.5,
          tags: ['mean-reversion', 'advanced']
        },
        {
          id: '3',
          name: 'Bollinger Band Breakout',
          type: 'pinescript',
          description: 'TradingView Pine Script for BB breakout signals',
          performance: { returns: 31.2, sharpe: 1.6, maxDrawdown: -12.4, winRate: 59 },
          status: 'backtesting',
          timeframe: '15M',
          markets: ['Crypto'],
          lastUpdated: '2025-10-18',
          rating: 3.8,
          tags: ['breakout', 'volatility']
        }
      ];
      setStrategies(mockStrategies);
    } catch (error) {
      console.error('Failed to load strategies:', error);
    }
  };

  const handleStrategySelect = (strategyId: string) => {
    setSelectedStrategies(prev => 
      prev.includes(strategyId) 
        ? prev.filter(id => id !== strategyId)
        : [...prev, strategyId]
    );
  };

  const handleSelectAll = () => {
    setSelectedStrategies(strategies.map(s => s.id));
  };

  const handleClearSelection = () => {
    setSelectedStrategies([]);
  };

  const filteredStrategies = strategies.filter(strategy => {
    const matchesSearch = strategy.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         strategy.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterType === 'all' || strategy.type === filterType;
    return matchesSearch && matchesFilter;
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-400 bg-green-400/10';
      case 'inactive': return 'text-gray-400 bg-gray-400/10';
      case 'backtesting': return 'text-yellow-400 bg-yellow-400/10';
      default: return 'text-gray-400 bg-gray-400/10';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'pinescript': return <Code className="h-4 w-4" />;
      case 'python': return <FileText className="h-4 w-4" />;
      case 'built-in': return <Settings className="h-4 w-4" />;
      default: return <FileText className="h-4 w-4" />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Trading Strategies</h1>
          <p className="text-slate-400">
            Manage, backtest, and deploy your algorithmic trading strategies
          </p>
        </div>

        {/* Controls */}
        <div className="bg-slate-800 rounded-lg p-6 mb-6">
          <div className="flex flex-col lg:flex-row gap-4 mb-4">
            {/* Search */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
              <input
                type="text"
                placeholder="Search strategies..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-slate-700 border border-slate-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Filter */}
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value as any)}
              className="px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Types</option>
              <option value="built-in">Built-in</option>
              <option value="python">Python</option>
              <option value="pinescript">Pine Script</option>
            </select>

            {/* View Mode */}
            <div className="flex bg-slate-700 rounded-lg p-1">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 rounded ${viewMode === 'grid' ? 'bg-blue-500' : 'hover:bg-slate-600'}`}
              >
                <Grid className="h-4 w-4" />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 rounded ${viewMode === 'list' ? 'bg-blue-500' : 'hover:bg-slate-600'}`}
              >
                <List className="h-4 w-4" />
              </button>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-wrap gap-3">
            <button className="px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg flex items-center space-x-2 transition-colors">
              <Plus className="h-4 w-4" />
              <span>New Strategy</span>
            </button>
            <button className="px-4 py-2 bg-green-500 hover:bg-green-600 rounded-lg flex items-center space-x-2 transition-colors">
              <Upload className="h-4 w-4" />
              <span>Upload Pine Script</span>
            </button>
            <button className="px-4 py-2 bg-purple-500 hover:bg-purple-600 rounded-lg flex items-center space-x-2 transition-colors">
              <Download className="h-4 w-4" />
              <span>Import Strategies</span>
            </button>
            {selectedStrategies.length > 0 && (
              <>
                <button 
                  onClick={handleClearSelection}
                  className="px-4 py-2 bg-slate-600 hover:bg-slate-500 rounded-lg transition-colors"
                >
                  Clear Selection ({selectedStrategies.length})
                </button>
                <button className="px-4 py-2 bg-orange-500 hover:bg-orange-600 rounded-lg flex items-center space-x-2 transition-colors">
                  <Play className="h-4 w-4" />
                  <span>Run Selected</span>
                </button>
              </>
            )}
            <button 
              onClick={handleSelectAll}
              className="px-4 py-2 bg-slate-600 hover:bg-slate-500 rounded-lg transition-colors"
            >
              Select All
            </button>
          </div>
        </div>

        {/* Strategies Grid/List */}
        {viewMode === 'grid' ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredStrategies.map((strategy) => (
              <div 
                key={strategy.id}
                className={`bg-slate-800 rounded-lg p-6 border-2 transition-all duration-200 cursor-pointer
                  ${selectedStrategies.includes(strategy.id) 
                    ? 'border-blue-500 bg-blue-500/10' 
                    : 'border-slate-700 hover:border-slate-600'
                  }`}
                onClick={() => handleStrategySelect(strategy.id)}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-2">
                    {getTypeIcon(strategy.type)}
                    <h3 className="font-semibold text-lg">{strategy.name}</h3>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Star className="h-4 w-4 text-yellow-400" />
                    <span className="text-sm">{strategy.rating}</span>
                  </div>
                </div>

                <p className="text-slate-400 text-sm mb-4">{strategy.description}</p>

                <div className="space-y-2 mb-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-slate-400">Returns:</span>
                    <span className="text-green-400 font-medium">+{strategy.performance.returns}%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-slate-400">Sharpe:</span>
                    <span className="text-white">{strategy.performance.sharpe}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-slate-400">Win Rate:</span>
                    <span className="text-blue-400">{strategy.performance.winRate}%</span>
                  </div>
                </div>

                <div className="flex items-center justify-between mb-4">
                  <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(strategy.status)}`}>
                    {strategy.status}
                  </span>
                  <span className="text-sm text-slate-400">{strategy.timeframe}</span>
                </div>

                <div className="flex flex-wrap gap-1 mb-4">
                  {strategy.tags.map((tag, index) => (
                    <span key={index} className="px-2 py-1 bg-slate-700 text-xs rounded">
                      {tag}
                    </span>
                  ))}
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
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-slate-800 rounded-lg overflow-hidden">
            <table className="w-full">
              <thead className="bg-slate-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Strategy</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Type</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Performance</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700">
                {filteredStrategies.map((strategy) => (
                  <tr 
                    key={strategy.id}
                    className={`hover:bg-slate-700 cursor-pointer ${
                      selectedStrategies.includes(strategy.id) ? 'bg-blue-500/10' : ''
                    }`}
                    onClick={() => handleStrategySelect(strategy.id)}
                  >
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-white">{strategy.name}</div>
                        <div className="text-sm text-slate-400">{strategy.description}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center space-x-2">
                        {getTypeIcon(strategy.type)}
                        <span className="text-sm">{strategy.type}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <div className="text-green-400">+{strategy.performance.returns}%</div>
                      <div className="text-slate-400">Sharpe: {strategy.performance.sharpe}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(strategy.status)}`}>
                        {strategy.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm space-x-2">
                      <button className="p-1 hover:bg-slate-600 rounded">
                        <Eye className="h-4 w-4" />
                      </button>
                      <button className="p-1 hover:bg-slate-600 rounded">
                        <Play className="h-4 w-4" />
                      </button>
                      <button className="p-1 hover:bg-slate-600 rounded">
                        <BarChart3 className="h-4 w-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {filteredStrategies.length === 0 && (
          <div className="text-center py-12">
            <FileText className="h-12 w-12 text-slate-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-slate-300 mb-2">No strategies found</h3>
            <p className="text-slate-400 mb-4">Try adjusting your search or filter criteria</p>
            <button className="px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg flex items-center space-x-2 mx-auto transition-colors">
              <Plus className="h-4 w-4" />
              <span>Create New Strategy</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}