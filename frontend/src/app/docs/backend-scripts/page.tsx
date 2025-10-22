'use client';

import React, { useState } from 'react';
import { Server, CheckCircle, AlertCircle, Code, Database, Key, DollarSign } from 'lucide-react';

interface Script {
  name: string;
  path: string;
  status: 'operational' | 'optional' | 'pending';
  purpose: string;
  features: string[];
  credentials: boolean;
  cost: 'FREE' | 'Paid';
  primaryUse: string;
  endpoints?: string[];
}

export default function BackendScriptsPage() {
  const [selectedCategory, setSelectedCategory] = useState<'all' | 'api' | 'stocks' | 'crypto'>('all');
  const [expandedScript, setExpandedScript] = useState<string | null>(null);

  const apiScripts: Script[] = [
    {
      name: 'main.py',
      path: 'api/main.py',
      status: 'operational',
      purpose: 'Core FastAPI server with all endpoints',
      features: [
        'Health check endpoint',
        'Portfolio management',
        'Backtesting API',
        'Strategy management',
        'Trading control',
        'WebSocket support',
        'CORS enabled'
      ],
      credentials: false,
      cost: 'FREE',
      primaryUse: 'API Server',
      endpoints: [
        'GET  /health',
        'GET  /portfolio',
        'POST /backtest',
        'GET  /strategies',
        'GET  /positions',
        'POST /orders/create',
        'GET  /orders/history'
      ]
    },
    {
      name: 'market_data_api.py',
      path: 'api/market_data_api.py',
      status: 'operational',
      purpose: 'Real-time market data API (NSE & Crypto)',
      features: [
        'Real-time NSE indices (NIFTY 50, BANK NIFTY)',
        'Stock quotes (NSE/BSE)',
        'Top gainers/losers',
        'Market status (open/closed)',
        'Multiple exchange support'
      ],
      credentials: false,
      cost: 'FREE',
      primaryUse: 'Market Data',
      endpoints: [
        'GET  /api/market/health',
        'GET  /api/market/indices',
        'POST /api/market/quotes',
        'GET  /api/market/data',
        'GET  /api/market/positions',
        'GET  /api/market-data/provider-status'
      ]
    },
    {
      name: 'settings_api.py',
      path: 'api/settings_api.py',
      status: 'operational',
      purpose: 'Manage exchange configurations',
      features: [
        'Store exchange API keys',
        'Manage credentials',
        'Configure trading accounts',
        'Enable/disable exchanges'
      ],
      credentials: false,
      cost: 'FREE',
      primaryUse: 'Configuration',
      endpoints: [
        'GET    /api/settings/exchanges',
        'POST   /api/settings/exchanges',
        'PUT    /api/settings/exchanges/{name}',
        'DELETE /api/settings/exchanges/{name}'
      ]
    },
    {
      name: 'user_preferences_api.py',
      path: 'api/user_preferences_api.py',
      status: 'operational',
      purpose: 'Store user settings (Market, Mode selection)',
      features: [
        'Market preference (NSE/Crypto)',
        'Mode preference (Backtest/Paper/Live)',
        'localStorage sync',
        'Persistence across sessions'
      ],
      credentials: false,
      cost: 'FREE',
      primaryUse: 'User Settings',
      endpoints: [
        'GET  /api/user/preferences',
        'POST /api/user/preferences',
        'GET  /api/user/preferences/status'
      ]
    },
    {
      name: 'ccxt_service.py',
      path: 'api/ccxt_service.py',
      status: 'operational',
      purpose: 'Unified interface for 200+ crypto exchanges',
      features: [
        'Multi-exchange support',
        'Real-time crypto data',
        'Order execution',
        'Balance checking',
        'Historical data'
      ],
      credentials: false,
      cost: 'FREE',
      primaryUse: 'Crypto Data',
      endpoints: []
    },
    {
      name: 'fyers_user_service.py',
      path: 'api/fyers_user_service.py',
      status: 'optional',
      purpose: 'Manage FYERS user accounts (optional)',
      features: [
        'Store FYERS credentials',
        'Generate access tokens',
        'User authentication',
        'Account management'
      ],
      credentials: true,
      cost: 'Paid',
      primaryUse: 'FYERS Auth',
      endpoints: []
    }
  ];

  const stockScripts: Script[] = [
    {
      name: 'nse_free_data_provider.py',
      path: 'stocks/nse_free_data_provider.py',
      status: 'operational',
      purpose: 'FREE real-time NSE data (NO CREDENTIALS NEEDED) ⭐ PRIMARY',
      features: [
        'Real-time NSE indices',
        'Live stock quotes',
        'Top gainers/losers',
        'Market status',
        'Session management',
        'NSE India API + Yahoo Finance backup'
      ],
      credentials: false,
      cost: 'FREE',
      primaryUse: 'NSE Market Data',
      endpoints: []
    },
    {
      name: 'fyers_data_provider.py',
      path: 'stocks/fyers_data_provider.py',
      status: 'optional',
      purpose: 'FYERS API integration for NSE/BSE (optional)',
      features: [
        'Real-time NSE/BSE data',
        'Historical data',
        'Order execution',
        'Position management'
      ],
      credentials: true,
      cost: 'Paid',
      primaryUse: 'Live Trading',
      endpoints: []
    },
    {
      name: 'live_nse_quotes.py',
      path: 'stocks/live_nse_quotes.py',
      status: 'operational',
      purpose: 'Fetch live NSE stock quotes',
      features: [
        'Real-time quotes',
        'Multiple symbols',
        'Fast response'
      ],
      credentials: false,
      cost: 'FREE',
      primaryUse: 'Stock Quotes',
      endpoints: []
    },
    {
      name: 'data_acquisition.py',
      path: 'stocks/data_acquisition.py',
      status: 'operational',
      purpose: 'Unified data fetching interface',
      features: [
        'Multi-source data fetching',
        'Fallback mechanisms',
        'Caching'
      ],
      credentials: false,
      cost: 'FREE',
      primaryUse: 'Data Aggregation',
      endpoints: []
    }
  ];

  const cryptoScripts: Script[] = [
    {
      name: 'crypto_assets_manager.py',
      path: 'crypto/crypto_assets_manager.py',
      status: 'operational',
      purpose: 'Manage crypto asset lists',
      features: [
        'Load crypto symbols',
        'Symbol validation',
        'Asset categorization'
      ],
      credentials: false,
      cost: 'FREE',
      primaryUse: 'Asset Management',
      endpoints: []
    },
    {
      name: 'crypto_symbol_manager.py',
      path: 'crypto/crypto_symbol_manager.py',
      status: 'operational',
      purpose: 'Crypto symbol management',
      features: [
        'Symbol lookup',
        'Market validation'
      ],
      credentials: false,
      cost: 'FREE',
      primaryUse: 'Symbol Management',
      endpoints: []
    },
    {
      name: 'data_acquisition.py',
      path: 'crypto/data_acquisition.py',
      status: 'operational',
      purpose: 'Fetch crypto market data',
      features: [
        'Multi-exchange support',
        'Historical data',
        'Real-time prices'
      ],
      credentials: false,
      cost: 'FREE',
      primaryUse: 'Crypto Data',
      endpoints: []
    }
  ];

  const allScripts = [...apiScripts, ...stockScripts, ...cryptoScripts];
  const filteredScripts = selectedCategory === 'all' 
    ? allScripts 
    : selectedCategory === 'api' 
      ? apiScripts 
      : selectedCategory === 'stocks' 
        ? stockScripts 
        : cryptoScripts;

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'operational': return 'text-green-500';
      case 'optional': return 'text-blue-500';
      case 'pending': return 'text-yellow-500';
      default: return 'text-gray-500';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'operational': return <CheckCircle className="w-5 h-5" />;
      case 'optional': return <AlertCircle className="w-5 h-5" />;
      case 'pending': return <AlertCircle className="w-5 h-5" />;
      default: return <AlertCircle className="w-5 h-5" />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center gap-3">
            <Server className="w-8 h-8 text-blue-600 dark:text-blue-400" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                Backend Scripts Inventory
              </h1>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                Complete documentation of all backend capabilities
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Total Scripts</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{allScripts.length}</p>
              </div>
              <Code className="w-8 h-8 text-blue-500" />
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Operational</p>
                <p className="text-2xl font-bold text-green-600">
                  {allScripts.filter(s => s.status === 'operational').length}
                </p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-500" />
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Free Scripts</p>
                <p className="text-2xl font-bold text-blue-600">
                  {allScripts.filter(s => s.cost === 'FREE').length}
                </p>
              </div>
              <DollarSign className="w-8 h-8 text-blue-500" />
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">No Credentials</p>
                <p className="text-2xl font-bold text-purple-600">
                  {allScripts.filter(s => !s.credentials).length}
                </p>
              </div>
              <Key className="w-8 h-8 text-purple-500" />
            </div>
          </div>
        </div>
      </div>

      {/* Category Filter */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex gap-2">
          {['all', 'api', 'stocks', 'crypto'].map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category as any)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                selectedCategory === category
                  ? 'bg-blue-600 text-white'
                  : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              {category.toUpperCase()}
              {category !== 'all' && (
                <span className="ml-2 text-xs opacity-75">
                  ({category === 'api' ? apiScripts.length : category === 'stocks' ? stockScripts.length : cryptoScripts.length})
                </span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Scripts List */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 pb-12">
        <div className="space-y-4">
          {filteredScripts.map((script) => (
            <div
              key={script.path}
              className="bg-white dark:bg-gray-800 rounded-lg shadow hover:shadow-md transition-shadow"
            >
              {/* Script Header */}
              <div
                className="p-4 cursor-pointer"
                onClick={() => setExpandedScript(expandedScript === script.path ? null : script.path)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <span className={getStatusColor(script.status)}>
                        {getStatusIcon(script.status)}
                      </span>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                          {script.name}
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400 font-mono">
                          {script.path}
                        </p>
                      </div>
                    </div>
                    <p className="text-sm text-gray-700 dark:text-gray-300 mt-2">
                      {script.purpose}
                    </p>
                  </div>

                  {/* Badges */}
                  <div className="flex gap-2 ml-4">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      script.cost === 'FREE' 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                        : 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200'
                    }`}>
                      {script.cost}
                    </span>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      script.credentials
                        ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                        : 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                    }`}>
                      {script.credentials ? 'Credentials' : 'No Creds'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Expanded Details */}
              {expandedScript === script.path && (
                <div className="border-t border-gray-200 dark:border-gray-700 p-4 space-y-4">
                  {/* Features */}
                  <div>
                    <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-2">
                      Features
                    </h4>
                    <ul className="list-disc list-inside space-y-1">
                      {script.features.map((feature, idx) => (
                        <li key={idx} className="text-sm text-gray-700 dark:text-gray-300">
                          {feature}
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Endpoints */}
                  {script.endpoints && script.endpoints.length > 0 && (
                    <div>
                      <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-2">
                        API Endpoints
                      </h4>
                      <div className="bg-gray-900 dark:bg-black rounded p-3 font-mono text-xs text-gray-100 space-y-1">
                        {script.endpoints.map((endpoint, idx) => (
                          <div key={idx}>{endpoint}</div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Primary Use */}
                  <div className="flex items-center gap-2">
                    <Database className="w-4 h-4 text-gray-500" />
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      Primary Use: <span className="font-medium text-gray-900 dark:text-white">{script.primaryUse}</span>
                    </span>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Quick Start */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 pb-12">
        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-3">
            🚀 Quick Start
          </h3>
          <div className="space-y-2 text-sm text-blue-800 dark:text-blue-200">
            <p><strong>1. Start Backend:</strong> <code className="bg-blue-100 dark:bg-blue-900 px-2 py-1 rounded">python start_backend.py</code></p>
            <p><strong>2. API Docs:</strong> <a href="http://localhost:8000/docs" target="_blank" className="underline">http://localhost:8000/docs</a></p>
            <p><strong>3. Health Check:</strong> <code className="bg-blue-100 dark:bg-blue-900 px-2 py-1 rounded">curl http://localhost:8000/health</code></p>
          </div>
        </div>
      </div>
    </div>
  );
}
