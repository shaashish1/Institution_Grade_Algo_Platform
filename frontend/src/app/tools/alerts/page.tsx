'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Bell, Plus, TrendingUp, TrendingDown, Target, Volume, Clock, Trash2, Edit, Play, Pause, AlertTriangle } from 'lucide-react';

interface Alert {
  id: string;
  symbol: string;
  type: 'price' | 'volume' | 'iv' | 'strategy';
  condition: 'above' | 'below' | 'crosses';
  value: number;
  currentValue: number;
  isActive: boolean;
  createdAt: Date;
  triggeredAt?: Date;
  description: string;
  urgency: 'low' | 'medium' | 'high';
}

interface NewAlert {
  symbol: string;
  type: 'price' | 'volume' | 'iv' | 'strategy';
  condition: 'above' | 'below' | 'crosses';
  value: number;
  description: string;
}

const sampleAlerts: Alert[] = [
  {
    id: '1',
    symbol: 'NIFTY',
    type: 'price',
    condition: 'above',
    value: 26000,
    currentValue: 25709,
    isActive: true,
    createdAt: new Date('2025-10-18'),
    description: 'NIFTY breaks 26000 resistance',
    urgency: 'high'
  },
  {
    id: '2',
    symbol: 'RELIANCE',
    type: 'volume',
    condition: 'above',
    value: 5000000,
    currentValue: 2345678,
    isActive: true,
    createdAt: new Date('2025-10-19'),
    description: 'Unusual volume spike in RELIANCE',
    urgency: 'medium'
  },
  {
    id: '3',
    symbol: 'BANKNIFTY',
    type: 'iv',
    condition: 'above',
    value: 20,
    currentValue: 18.5,
    isActive: false,
    createdAt: new Date('2025-10-17'),
    triggeredAt: new Date('2025-10-18'),
    description: 'BANKNIFTY IV spike above 20%',
    urgency: 'low'
  },
  {
    id: '4',
    symbol: 'TCS',
    type: 'price',
    condition: 'below',
    value: 4000,
    currentValue: 4123.30,
    isActive: true,
    createdAt: new Date('2025-10-19'),
    description: 'TCS support break at 4000',
    urgency: 'high'
  }
];

const alertTypes = [
  { value: 'price', label: 'Price Alert', icon: TrendingUp, description: 'Get notified when price crosses a level' },
  { value: 'volume', label: 'Volume Alert', icon: Volume, description: 'Alert on unusual volume activity' },
  { value: 'iv', label: 'IV Alert', icon: Target, description: 'Implied volatility threshold alerts' },
  { value: 'strategy', label: 'Strategy Alert', icon: Bell, description: 'Custom strategy-based alerts' }
];

const conditions = [
  { value: 'above', label: 'Above', description: 'Trigger when value goes above threshold' },
  { value: 'below', label: 'Below', description: 'Trigger when value goes below threshold' },
  { value: 'crosses', label: 'Crosses', description: 'Trigger when value crosses threshold (either direction)' }
];

const symbols = ['NIFTY', 'BANKNIFTY', 'FINNIFTY', 'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK', 'SBIN', 'ITC'];

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>(sampleAlerts);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newAlert, setNewAlert] = useState<NewAlert>({
    symbol: 'NIFTY',
    type: 'price',
    condition: 'above',
    value: 0,
    description: ''
  });
  const [selectedTab, setSelectedTab] = useState<'active' | 'triggered' | 'all'>('active');

  const createAlert = () => {
    const alert: Alert = {
      id: Date.now().toString(),
      ...newAlert,
      currentValue: getCurrentValue(newAlert.symbol, newAlert.type),
      isActive: true,
      createdAt: new Date(),
      urgency: determineUrgency(newAlert)
    };

    setAlerts(prev => [...prev, alert]);
    setNewAlert({
      symbol: 'NIFTY',
      type: 'price',
      condition: 'above',
      value: 0,
      description: ''
    });
    setShowCreateForm(false);
  };

  const getCurrentValue = (symbol: string, type: string): number => {
    // Mock current values - in real app, fetch from API
    const mockValues: Record<string, Record<string, number>> = {
      'NIFTY': { price: 25709, volume: 2847593, iv: 14.85 },
      'BANKNIFTY': { price: 54789, volume: 1543876, iv: 18.5 },
      'RELIANCE': { price: 2789, volume: 2345678, iv: 18.5 },
      'TCS': { price: 4123, volume: 1876543, iv: 22.3 }
    };
    return mockValues[symbol]?.[type] || 0;
  };

  const determineUrgency = (alert: NewAlert): 'low' | 'medium' | 'high' => {
    if (alert.type === 'price') return 'high';
    if (alert.type === 'volume') return 'medium';
    return 'low';
  };

  const toggleAlert = (id: string) => {
    setAlerts(prev => prev.map(alert => 
      alert.id === id ? { ...alert, isActive: !alert.isActive } : alert
    ));
  };

  const deleteAlert = (id: string) => {
    setAlerts(prev => prev.filter(alert => alert.id !== id));
  };

  const getFilteredAlerts = () => {
    switch (selectedTab) {
      case 'active':
        return alerts.filter(alert => alert.isActive);
      case 'triggered':
        return alerts.filter(alert => alert.triggeredAt);
      default:
        return alerts;
    }
  };

  const getUrgencyColor = (urgency: string) => {
    switch (urgency) {
      case 'high': return 'text-red-400 bg-red-900/30 border-red-700';
      case 'medium': return 'text-yellow-400 bg-yellow-900/30 border-yellow-700';
      default: return 'text-blue-400 bg-blue-900/30 border-blue-700';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'price': return TrendingUp;
      case 'volume': return Volume;
      case 'iv': return Target;
      default: return Bell;
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
            <Link href="/tools" className="hover:text-blue-400 transition-colors">Tools</Link>
            <span>/</span>
            <span className="text-white">Alerts</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Bell className="h-8 w-8 text-blue-400" />
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                  Price & Strategy Alerts
                </h1>
                <p className="text-xl text-slate-300 mt-2">
                  Stay informed with real-time market notifications
                </p>
              </div>
            </div>
            <button
              onClick={() => setShowCreateForm(true)}
              className="flex items-center px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-semibold transition-colors"
            >
              <Plus className="h-5 w-5 mr-2" />
              Create Alert
            </button>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400">Active Alerts</span>
              <Bell className="h-5 w-5 text-green-400" />
            </div>
            <div className="text-2xl font-bold text-green-400">
              {alerts.filter(a => a.isActive).length}
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400">Triggered Today</span>
              <AlertTriangle className="h-5 w-5 text-yellow-400" />
            </div>
            <div className="text-2xl font-bold text-yellow-400">
              {alerts.filter(a => a.triggeredAt && 
                new Date(a.triggeredAt).toDateString() === new Date().toDateString()).length}
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400">High Priority</span>
              <TrendingUp className="h-5 w-5 text-red-400" />
            </div>
            <div className="text-2xl font-bold text-red-400">
              {alerts.filter(a => a.urgency === 'high' && a.isActive).length}
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400">Total Alerts</span>
              <Target className="h-5 w-5 text-blue-400" />
            </div>
            <div className="text-2xl font-bold text-blue-400">{alerts.length}</div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6">
          <div className="flex space-x-1 bg-slate-900 p-1 rounded-lg w-fit">
            {(['active', 'triggered', 'all'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setSelectedTab(tab)}
                className={`px-6 py-2 rounded-md font-medium transition-colors capitalize ${
                  selectedTab === tab
                    ? 'bg-blue-600 text-white'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {tab} ({tab === 'active' ? alerts.filter(a => a.isActive).length : 
                       tab === 'triggered' ? alerts.filter(a => a.triggeredAt).length : 
                       alerts.length})
              </button>
            ))}
          </div>
        </div>

        {/* Alerts List */}
        <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden">
          <div className="p-6 border-b border-slate-800">
            <h2 className="text-xl font-bold text-white">Your Alerts</h2>
          </div>

          <div className="divide-y divide-slate-800">
            {getFilteredAlerts().map((alert) => {
              const Icon = getTypeIcon(alert.type);
              const progress = alert.condition === 'above' 
                ? (alert.currentValue / alert.value) * 100
                : alert.condition === 'below'
                ? ((alert.value - alert.currentValue) / alert.value) * 100
                : 50;

              return (
                <div key={alert.id} className="p-6 hover:bg-slate-800/50 transition-colors">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-4">
                      <div className={`p-2 rounded-lg ${getUrgencyColor(alert.urgency)} border`}>
                        <Icon className="h-5 w-5" />
                      </div>
                      
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <h3 className="font-semibold text-white">{alert.symbol}</h3>
                          <span className="px-2 py-1 bg-slate-800 rounded text-xs text-slate-300 capitalize">
                            {alert.type}
                          </span>
                          <span className={`px-2 py-1 rounded text-xs ${
                            alert.isActive ? 'bg-green-900/30 text-green-400' : 'bg-slate-700 text-slate-400'
                          }`}>
                            {alert.isActive ? 'Active' : 'Paused'}
                          </span>
                        </div>
                        
                        <p className="text-slate-300 mb-3">{alert.description}</p>
                        
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                          <div>
                            <span className="text-slate-400">Condition:</span>
                            <div className="font-mono text-white capitalize">{alert.condition} {alert.value}</div>
                          </div>
                          <div>
                            <span className="text-slate-400">Current:</span>
                            <div className="font-mono text-blue-400">{alert.currentValue.toLocaleString()}</div>
                          </div>
                          <div>
                            <span className="text-slate-400">Created:</span>
                            <div className="text-slate-300">{alert.createdAt.toLocaleDateString()}</div>
                          </div>
                          {alert.triggeredAt && (
                            <div>
                              <span className="text-slate-400">Triggered:</span>
                              <div className="text-green-400">{alert.triggeredAt.toLocaleDateString()}</div>
                            </div>
                          )}
                        </div>

                        {alert.isActive && (
                          <div className="mt-3">
                            <div className="flex justify-between text-xs text-slate-400 mb-1">
                              <span>Progress to target</span>
                              <span>{Math.min(progress, 100).toFixed(1)}%</span>
                            </div>
                            <div className="w-full h-2 bg-slate-700 rounded-full">
                              <div 
                                className={`h-2 rounded-full transition-all duration-300 ${
                                  progress >= 100 ? 'bg-green-400' : 
                                  progress >= 80 ? 'bg-yellow-400' : 'bg-blue-400'
                                }`}
                                style={{ width: `${Math.min(progress, 100)}%` }}
                              ></div>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => toggleAlert(alert.id)}
                        className={`p-2 rounded-lg transition-colors ${
                          alert.isActive 
                            ? 'bg-yellow-600 hover:bg-yellow-700 text-white' 
                            : 'bg-green-600 hover:bg-green-700 text-white'
                        }`}
                        title={alert.isActive ? 'Pause Alert' : 'Activate Alert'}
                      >
                        {alert.isActive ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
                      </button>
                      <button
                        className="p-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-slate-300 hover:text-white transition-colors"
                        title="Edit Alert"
                      >
                        <Edit className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => deleteAlert(alert.id)}
                        className="p-2 bg-red-600 hover:bg-red-700 rounded-lg text-white transition-colors"
                        title="Delete Alert"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {getFilteredAlerts().length === 0 && (
            <div className="p-12 text-center">
              <Bell className="h-12 w-12 text-slate-600 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-slate-400 mb-2">No alerts found</h3>
              <p className="text-slate-500 mb-4">
                {selectedTab === 'active' ? 'No active alerts' : 
                 selectedTab === 'triggered' ? 'No triggered alerts' : 'No alerts created yet'}
              </p>
              <button
                onClick={() => setShowCreateForm(true)}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white transition-colors"
              >
                Create Your First Alert
              </button>
            </div>
          )}
        </div>

        {/* Create Alert Modal */}
        {showCreateForm && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div className="bg-slate-900 rounded-2xl border border-slate-800 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
              <div className="p-6 border-b border-slate-800">
                <h2 className="text-xl font-bold text-white">Create New Alert</h2>
              </div>

              <div className="p-6 space-y-6">
                {/* Alert Type Selection */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-3">Alert Type</label>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {alertTypes.map((type) => {
                      const Icon = type.icon;
                      return (
                        <button
                          key={type.value}
                          onClick={() => setNewAlert(prev => ({ ...prev, type: type.value as any }))}
                          className={`p-4 rounded-lg border text-left transition-colors ${
                            newAlert.type === type.value
                              ? 'bg-blue-600/20 border-blue-500 text-blue-300'
                              : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-600'
                          }`}
                        >
                          <div className="flex items-center space-x-3 mb-2">
                            <Icon className="h-5 w-5" />
                            <span className="font-medium">{type.label}</span>
                          </div>
                          <p className="text-xs opacity-80">{type.description}</p>
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* Symbol Selection */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Symbol</label>
                  <select
                    value={newAlert.symbol}
                    onChange={(e) => setNewAlert(prev => ({ ...prev, symbol: e.target.value }))}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                  >
                    {symbols.map(symbol => (
                      <option key={symbol} value={symbol}>{symbol}</option>
                    ))}
                  </select>
                </div>

                {/* Condition */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Condition</label>
                  <select
                    value={newAlert.condition}
                    onChange={(e) => setNewAlert(prev => ({ ...prev, condition: e.target.value as any }))}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                  >
                    {conditions.map(condition => (
                      <option key={condition.value} value={condition.value}>
                        {condition.label} - {condition.description}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Value */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Target Value ({newAlert.type === 'price' ? '₹' : newAlert.type === 'iv' ? '%' : ''})
                  </label>
                  <input
                    type="number"
                    value={newAlert.value}
                    onChange={(e) => setNewAlert(prev => ({ ...prev, value: Number(e.target.value) }))}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                    placeholder="Enter target value"
                  />
                </div>

                {/* Description */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Description</label>
                  <input
                    type="text"
                    value={newAlert.description}
                    onChange={(e) => setNewAlert(prev => ({ ...prev, description: e.target.value }))}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                    placeholder="Brief description of this alert"
                  />
                </div>
              </div>

              <div className="p-6 border-t border-slate-800 flex justify-end space-x-3">
                <button
                  onClick={() => setShowCreateForm(false)}
                  className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-white transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={createAlert}
                  disabled={!newAlert.value || !newAlert.description}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:cursor-not-allowed rounded-lg text-white transition-colors"
                >
                  Create Alert
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}