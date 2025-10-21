'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  Settings, Globe, Key, Eye, EyeOff, CheckCircle, AlertCircle, 
  RefreshCw, Save, TestTube, Shield, Clock, Calendar,
  Building2, Coins, TrendingUp, Activity, Bell, Info,
  ChevronRight, ExternalLink, Copy, Trash2, Edit3, Plus,
  Server, XCircle
} from 'lucide-react';

interface ExchangeStatus {
  exchange_id: string;
  initialized: boolean;
  trading_mode: string;
  markets_count: number;
  live_trading_enabled: boolean;
  credentials_required: boolean;
  initialized_at?: number;
}

interface ExchangeConfig {
  id: string;
  name: string;
  type: 'crypto' | 'stocks' | 'options';
  logo: string;
  status: 'connected' | 'disconnected' | 'error' | 'testing';
  credentials: {
    apiKey?: string;
    apiSecret?: string;
    passphrase?: string;
    userId?: string;
    password?: string;
  };
  permissions: string[];
  lastSync: Date | null;
  connectionTest: {
    status: 'pending' | 'success' | 'failed';
    latency?: number;
    lastTest?: Date;
  };
  settings: {
    sandbox: boolean;
    rateLimit: number;
    autoSync: boolean;
    notifications: boolean;
  };
}

interface FyersConfig {
  clientId: string;
  secretKey: string;
  redirectUrl: string;
  accessToken: string;
  refreshToken: string;
  tokenExpiry: Date | null;
  weeklyExpiry: {
    day: 'tuesday' | 'thursday';
    enabled: boolean;
  };
  monthlyExpiry: {
    lastTuesday: boolean;
    enabled: boolean;
  };
  autoRefresh: boolean;
  status: 'connected' | 'disconnected' | 'expired';
}

const initialExchanges: ExchangeConfig[] = [
  {
    id: 'binance',
    name: 'Binance',
    type: 'crypto',
    logo: 'https://cryptologos.cc/logos/binance-coin-bnb-logo.png',
    status: 'disconnected',
    credentials: {},
    permissions: ['spot', 'futures', 'margin'],
    lastSync: null,
    connectionTest: { status: 'pending' },
    settings: { sandbox: false, rateLimit: 1200, autoSync: true, notifications: true }
  },
  {
    id: 'coinbase',
    name: 'Coinbase Pro',
    type: 'crypto',
    logo: 'https://cryptologos.cc/logos/coinbase-coin-logo.png',
    status: 'disconnected',
    credentials: {},
    permissions: ['view', 'trade'],
    lastSync: null,
    connectionTest: { status: 'pending' },
    settings: { sandbox: true, rateLimit: 10, autoSync: false, notifications: true }
  },
  {
    id: 'kraken',
    name: 'Kraken',
    type: 'crypto',
    logo: 'https://cryptologos.cc/logos/kraken-logo.png',
    status: 'disconnected',
    credentials: {},
    permissions: ['query', 'trade'],
    lastSync: null,
    connectionTest: { status: 'pending' },
    settings: { sandbox: false, rateLimit: 20, autoSync: true, notifications: false }
  },
  {
    id: 'fyers',
    name: 'Fyers API',
    type: 'stocks',
    logo: 'https://via.placeholder.com/40x40/1e293b/64748b?text=F',
    status: 'disconnected',
    credentials: {},
    permissions: ['market_data', 'orders', 'funds'],
    lastSync: null,
    connectionTest: { status: 'pending' },
    settings: { sandbox: false, rateLimit: 100, autoSync: true, notifications: true }
  }
];

const initialFyersConfig: FyersConfig = {
  clientId: '',
  secretKey: '',
  redirectUrl: 'http://localhost:3000/auth/fyers/callback',
  accessToken: '',
  refreshToken: '',
  tokenExpiry: null,
  weeklyExpiry: { day: 'tuesday', enabled: true },
  monthlyExpiry: { lastTuesday: true, enabled: true },
  autoRefresh: true,
  status: 'disconnected'
};

export default function ExchangeSettings() {
  const [exchanges, setExchanges] = useState<ExchangeConfig[]>(initialExchanges);
  const [fyersConfig, setFyersConfig] = useState<FyersConfig>(initialFyersConfig);
  const [activeTab, setActiveTab] = useState<'exchanges' | 'fyers' | 'notifications'>('exchanges');
  const [selectedExchange, setSelectedExchange] = useState<string | null>(null);
  const [showApiKey, setShowApiKey] = useState<Record<string, boolean>>({});
  const [testing, setTesting] = useState<string | null>(null);
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'connected': return 'text-green-400 bg-green-500/20 border-green-500/30';
      case 'disconnected': return 'text-slate-400 bg-slate-500/20 border-slate-500/30';
      case 'error': return 'text-red-400 bg-red-500/20 border-red-500/30';
      case 'testing': return 'text-yellow-400 bg-yellow-500/20 border-yellow-500/30';
      default: return 'text-slate-400 bg-slate-500/20 border-slate-500/30';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'connected': return <CheckCircle className="h-4 w-4" />;
      case 'error': return <AlertCircle className="h-4 w-4" />;
      case 'testing': return <RefreshCw className="h-4 w-4 animate-spin" />;
      default: return <Globe className="h-4 w-4" />;
    }
  };

  const testConnection = async (exchangeId: string) => {
    setTesting(exchangeId);
    
    // Simulate API test
    setTimeout(() => {
      setExchanges(prev => prev.map(ex => 
        ex.id === exchangeId 
          ? {
              ...ex, 
              status: Math.random() > 0.3 ? 'connected' : 'error',
              connectionTest: {
                status: Math.random() > 0.3 ? 'success' : 'failed',
                latency: Math.floor(Math.random() * 200) + 50,
                lastTest: new Date()
              },
              lastSync: new Date()
            }
          : ex
      ));
      setTesting(null);
    }, 2000);
  };

  const saveExchangeConfig = (exchangeId: string, config: Partial<ExchangeConfig>) => {
    setSaveStatus('saving');
    
    setTimeout(() => {
      setExchanges(prev => prev.map(ex => 
        ex.id === exchangeId ? { ...ex, ...config } : ex
      ));
      setSaveStatus('saved');
      
      setTimeout(() => setSaveStatus('idle'), 2000);
    }, 1000);
  };

  const updateFyersConfig = (updates: Partial<FyersConfig>) => {
    setFyersConfig(prev => ({ ...prev, ...updates }));
  };

  const authenticateFyers = () => {
    // Implement Fyers OAuth flow
    const authUrl = `https://api.fyers.in/api/v2/generate-authcode?client_id=${fyersConfig.clientId}&redirect_uri=${fyersConfig.redirectUrl}&response_type=code&state=sample_state`;
    window.open(authUrl, '_blank');
  };

  const getWeeklyExpiryDate = () => {
    const today = new Date();
    const currentWeek = new Date(today);
    const day = fyersConfig.weeklyExpiry.day === 'tuesday' ? 2 : 4; // Tuesday = 2, Thursday = 4
    const daysUntilExpiry = (day + 7 - currentWeek.getDay()) % 7;
    currentWeek.setDate(currentWeek.getDate() + daysUntilExpiry);
    return currentWeek;
  };

  const getMonthlyExpiryDate = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth();
    
    // Get last Tuesday of the month
    const lastDay = new Date(year, month + 1, 0);
    const lastTuesday = new Date(lastDay);
    lastTuesday.setDate(lastDay.getDate() - ((lastDay.getDay() + 5) % 7));
    
    return lastTuesday;
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4">
      <div className="max-w-6xl mx-auto">
        {/* Breadcrumb */}
        <div className="mb-6">
          <nav className="flex items-center space-x-2 text-sm text-slate-400">
            <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
            <span>/</span>
            <Link href="/settings" className="hover:text-blue-400 transition-colors">Settings</Link>
            <span>/</span>
            <span className="text-white">Exchanges</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
            Exchange & API Settings
          </h1>
          <p className="text-xl text-slate-300">
            Configure trading APIs, manage connections, and set up option expiry calculations
          </p>
        </div>

        {/* CCXT Authentication Info */}
        <div className="mb-8 bg-slate-900 rounded-2xl p-6 border border-slate-800">
          <div className="flex items-center space-x-3 mb-4">
            <Info className="h-6 w-6 text-blue-400" />
            <h3 className="text-lg font-bold text-white">CCXT Trading Mode Authentication</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-green-900/20 border border-green-700 rounded-lg p-4">
              <div className="flex items-center space-x-2 mb-2">
                <TestTube className="h-5 w-5 text-green-400" />
                <span className="font-medium text-green-400">Backtest Mode</span>
              </div>
              <p className="text-sm text-slate-300 mb-2">
                Historical data analysis with no credentials required. Perfect for strategy testing.
              </p>
              <div className="flex items-center space-x-2 text-xs text-green-400">
                <CheckCircle className="h-3 w-3" />
                <span>No API keys needed</span>
              </div>
            </div>

            <div className="bg-blue-900/20 border border-blue-700 rounded-lg p-4">
              <div className="flex items-center space-x-2 mb-2">
                <Activity className="h-5 w-5 text-blue-400" />
                <span className="font-medium text-blue-400">Paper Trading</span>
              </div>
              <p className="text-sm text-slate-300 mb-2">
                Real-time data with simulated trading. No credentials needed, no real money at risk.
              </p>
              <div className="flex items-center space-x-2 text-xs text-blue-400">
                <CheckCircle className="h-3 w-3" />
                <span>Public market data only</span>
              </div>
            </div>

            <div className="bg-red-900/20 border border-red-700 rounded-lg p-4">
              <div className="flex items-center space-x-2 mb-2">
                <Shield className="h-5 w-5 text-red-400" />
                <span className="font-medium text-red-400">Live Trading</span>
              </div>
              <p className="text-sm text-slate-300 mb-2">
                Real trading with actual funds. Requires API credentials and proper risk management.
              </p>
              <div className="flex items-center space-x-2 text-xs text-red-400">
                <AlertCircle className="h-3 w-3" />
                <span>API credentials required</span>
              </div>
            </div>
          </div>

          <div className="mt-4 p-3 bg-yellow-900/20 border border-yellow-700 rounded-lg">
            <div className="flex items-start space-x-2">
              <Bell className="h-4 w-4 text-yellow-400 mt-0.5" />
              <div>
                <p className="text-sm text-yellow-400 font-medium">Important Security Notice</p>
                <p className="text-xs text-slate-300 mt-1">
                  For live trading, only provide API keys with limited permissions (read + trade only). 
                  Never share API keys with withdrawal permissions. Always start with sandbox/testnet mode.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="mb-8">
          <div className="flex space-x-1 bg-slate-900 p-1 rounded-xl">
            {[
              { id: 'exchanges', label: 'Exchange APIs', icon: Globe },
              { id: 'fyers', label: 'Fyers Configuration', icon: Building2 },
              { id: 'notifications', label: 'Notifications', icon: Bell }
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center px-6 py-3 rounded-lg font-medium transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-600 text-white'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  <Icon className="h-4 w-4 mr-2" />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* Exchange APIs Tab */}
        {activeTab === 'exchanges' && (
          <div className="space-y-6">
            {/* Exchange List */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {exchanges.map((exchange) => (
                <div key={exchange.id} className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden">
                  {/* Exchange Header */}
                  <div className="p-6 border-b border-slate-800">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-3">
                        <img 
                          src={exchange.logo} 
                          alt={exchange.name}
                          className="w-10 h-10 rounded-lg"
                          onError={(e) => {
                            (e.target as HTMLImageElement).src = `https://via.placeholder.com/40x40/1e293b/64748b?text=${exchange.name.charAt(0)}`;
                          }}
                        />
                        <div>
                          <h3 className="font-bold text-white">{exchange.name}</h3>
                          <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs border ${getStatusColor(exchange.status)}`}>
                            {getStatusIcon(exchange.status)}
                            <span className="ml-1">{exchange.status}</span>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => testConnection(exchange.id)}
                          disabled={testing === exchange.id}
                          className="flex items-center px-3 py-1 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 rounded-lg text-sm transition-colors"
                        >
                          {testing === exchange.id ? (
                            <RefreshCw className="h-4 w-4 animate-spin" />
                          ) : (
                            <TestTube className="h-4 w-4" />
                          )}
                          <span className="ml-1">Test</span>
                        </button>
                        
                        <button
                          onClick={() => setSelectedExchange(selectedExchange === exchange.id ? null : exchange.id)}
                          className="p-2 text-slate-400 hover:text-white"
                        >
                          <Settings className="h-4 w-4" />
                        </button>
                      </div>
                    </div>

                    {/* Connection Stats */}
                    {exchange.connectionTest.lastTest && (
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="text-slate-400">Last Test:</span>
                          <div className="text-white">{exchange.connectionTest.lastTest.toLocaleTimeString()}</div>
                        </div>
                        {exchange.connectionTest.latency && (
                          <div>
                            <span className="text-slate-400">Latency:</span>
                            <div className="text-white">{exchange.connectionTest.latency}ms</div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>

                  {/* Exchange Configuration */}
                  {selectedExchange === exchange.id && (
                    <div className="p-6 space-y-4">
                      <h4 className="font-semibold text-white mb-4">API Configuration</h4>
                      
                      {/* API Key */}
                      <div>
                        <label className="block text-sm text-slate-400 mb-2">API Key</label>
                        <div className="relative">
                          <input
                            type={showApiKey[exchange.id] ? 'text' : 'password'}
                            value={exchange.credentials.apiKey || ''}
                            onChange={(e) => saveExchangeConfig(exchange.id, {
                              credentials: { ...exchange.credentials, apiKey: e.target.value }
                            })}
                            className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white pr-10"
                            placeholder="Enter API Key"
                          />
                          <button
                            onClick={() => setShowApiKey(prev => ({ ...prev, [exchange.id]: !prev[exchange.id] }))}
                            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-white"
                          >
                            {showApiKey[exchange.id] ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                          </button>
                        </div>
                      </div>

                      {/* API Secret */}
                      <div>
                        <label className="block text-sm text-slate-400 mb-2">API Secret</label>
                        <input
                          type="password"
                          value={exchange.credentials.apiSecret || ''}
                          onChange={(e) => saveExchangeConfig(exchange.id, {
                            credentials: { ...exchange.credentials, apiSecret: e.target.value }
                          })}
                          className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                          placeholder="Enter API Secret"
                        />
                      </div>

                      {/* Passphrase (for some exchanges) */}
                      {exchange.id === 'coinbase' && (
                        <div>
                          <label className="block text-sm text-slate-400 mb-2">Passphrase</label>
                          <input
                            type="password"
                            value={exchange.credentials.passphrase || ''}
                            onChange={(e) => saveExchangeConfig(exchange.id, {
                              credentials: { ...exchange.credentials, passphrase: e.target.value }
                            })}
                            className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                            placeholder="Enter Passphrase"
                          />
                        </div>
                      )}

                      {/* Settings */}
                      <div className="grid grid-cols-2 gap-4">
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-slate-400">Sandbox Mode</span>
                          <input
                            type="checkbox"
                            checked={exchange.settings.sandbox}
                            onChange={(e) => saveExchangeConfig(exchange.id, {
                              settings: { ...exchange.settings, sandbox: e.target.checked }
                            })}
                            className="text-blue-600"
                          />
                        </div>
                        
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-slate-400">Auto Sync</span>
                          <input
                            type="checkbox"
                            checked={exchange.settings.autoSync}
                            onChange={(e) => saveExchangeConfig(exchange.id, {
                              settings: { ...exchange.settings, autoSync: e.target.checked }
                            })}
                            className="text-blue-600"
                          />
                        </div>
                      </div>

                      {/* Permissions */}
                      <div>
                        <span className="text-sm text-slate-400 mb-2 block">Permissions Required</span>
                        <div className="flex flex-wrap gap-2">
                          {exchange.permissions.map((permission) => (
                            <span key={permission} className="px-2 py-1 bg-slate-800 text-slate-300 text-xs rounded">
                              {permission}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Global Settings */}
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <h3 className="text-lg font-bold text-white mb-4">Global Exchange Settings</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label className="block text-sm text-slate-400 mb-2">Default Rate Limit (req/min)</label>
                  <input
                    type="number"
                    defaultValue={100}
                    className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                  />
                </div>
                
                <div>
                  <label className="block text-sm text-slate-400 mb-2">Connection Timeout (ms)</label>
                  <input
                    type="number"
                    defaultValue={5000}
                    className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                  />
                </div>
                
                <div>
                  <label className="block text-sm text-slate-400 mb-2">Retry Attempts</label>
                  <input
                    type="number"
                    defaultValue={3}
                    className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Fyers Configuration Tab */}
        {activeTab === 'fyers' && (
          <div className="space-y-6">
            {/* Fyers API Setup */}
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h3 className="text-xl font-bold text-white mb-2">Fyers API Configuration</h3>
                  <p className="text-slate-400">Configure Fyers API for Indian stock market data and trading</p>
                </div>
                
                <div className={`flex items-center px-3 py-2 rounded-lg border ${getStatusColor(fyersConfig.status)}`}>
                  {getStatusIcon(fyersConfig.status)}
                  <span className="ml-2">{fyersConfig.status}</span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm text-slate-400 mb-2">Client ID</label>
                  <input
                    type="text"
                    value={fyersConfig.clientId}
                    onChange={(e) => updateFyersConfig({ clientId: e.target.value })}
                    className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                    placeholder="Your Fyers Client ID"
                  />
                </div>

                <div>
                  <label className="block text-sm text-slate-400 mb-2">Secret Key</label>
                  <input
                    type="password"
                    value={fyersConfig.secretKey}
                    onChange={(e) => updateFyersConfig({ secretKey: e.target.value })}
                    className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                    placeholder="Your Fyers Secret Key"
                  />
                </div>

                <div>
                  <label className="block text-sm text-slate-400 mb-2">Redirect URL</label>
                  <input
                    type="url"
                    value={fyersConfig.redirectUrl}
                    onChange={(e) => updateFyersConfig({ redirectUrl: e.target.value })}
                    className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                    placeholder="Redirect URL for OAuth"
                  />
                </div>

                <div className="flex items-center justify-center">
                  <button
                    onClick={authenticateFyers}
                    disabled={!fyersConfig.clientId || !fyersConfig.secretKey}
                    className="flex items-center px-6 py-3 bg-green-600 hover:bg-green-700 disabled:bg-green-800 disabled:cursor-not-allowed rounded-lg font-medium transition-colors"
                  >
                    <Key className="h-5 w-5 mr-2" />
                    Authenticate with Fyers
                  </button>
                </div>
              </div>
            </div>

            {/* Option Expiry Configuration */}
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <div className="flex items-center mb-6">
                <Calendar className="h-6 w-6 text-purple-400 mr-3" />
                <div>
                  <h3 className="text-xl font-bold text-white">Option Expiry Configuration</h3>
                  <p className="text-slate-400">Configure correct expiry dates for weekly and monthly options</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Weekly Expiry */}
                <div className="space-y-4">
                  <h4 className="font-semibold text-white flex items-center">
                    <Clock className="h-4 w-4 mr-2 text-blue-400" />
                    Weekly Options Expiry
                  </h4>
                  
                  <div className="bg-slate-800 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-slate-300">Enable Weekly Expiry</span>
                      <input
                        type="checkbox"
                        checked={fyersConfig.weeklyExpiry.enabled}
                        onChange={(e) => updateFyersConfig({
                          weeklyExpiry: { ...fyersConfig.weeklyExpiry, enabled: e.target.checked }
                        })}
                        className="text-blue-600"
                      />
                    </div>
                    
                    <div className="mb-3">
                      <label className="block text-sm text-slate-400 mb-2">Expiry Day</label>
                      <select
                        value={fyersConfig.weeklyExpiry.day}
                        onChange={(e) => updateFyersConfig({
                          weeklyExpiry: { ...fyersConfig.weeklyExpiry, day: e.target.value as 'tuesday' | 'thursday' }
                        })}
                        className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white"
                      >
                        <option value="tuesday">Tuesday</option>
                        <option value="thursday">Thursday</option>
                      </select>
                    </div>
                    
                    <div className="text-sm text-slate-400">
                      <span className="text-green-400">Next Weekly Expiry:</span>
                      <div className="font-mono text-white mt-1">
                        {getWeeklyExpiryDate().toLocaleDateString('en-IN', {
                          weekday: 'long',
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric'
                        })}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Monthly Expiry */}
                <div className="space-y-4">
                  <h4 className="font-semibold text-white flex items-center">
                    <Calendar className="h-4 w-4 mr-2 text-purple-400" />
                    Monthly Options Expiry
                  </h4>
                  
                  <div className="bg-slate-800 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-slate-300">Enable Monthly Expiry</span>
                      <input
                        type="checkbox"
                        checked={fyersConfig.monthlyExpiry.enabled}
                        onChange={(e) => updateFyersConfig({
                          monthlyExpiry: { ...fyersConfig.monthlyExpiry, enabled: e.target.checked }
                        })}
                        className="text-blue-600"
                      />
                    </div>
                    
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-slate-300">Last Tuesday of Month</span>
                      <input
                        type="checkbox"
                        checked={fyersConfig.monthlyExpiry.lastTuesday}
                        onChange={(e) => updateFyersConfig({
                          monthlyExpiry: { ...fyersConfig.monthlyExpiry, lastTuesday: e.target.checked }
                        })}
                        className="text-blue-600"
                      />
                    </div>
                    
                    <div className="text-sm text-slate-400">
                      <span className="text-purple-400">Next Monthly Expiry:</span>
                      <div className="font-mono text-white mt-1">
                        {getMonthlyExpiryDate().toLocaleDateString('en-IN', {
                          weekday: 'long',
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric'
                        })}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Important Note */}
              <div className="mt-6 p-4 bg-blue-900/20 border border-blue-500/30 rounded-lg">
                <div className="flex items-start space-x-3">
                  <Info className="h-5 w-5 text-blue-400 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-blue-400 mb-2">Important Expiry Information</h4>
                    <ul className="text-sm text-slate-300 space-y-1">
                      <li>• Weekly options expire on Tuesday of the expiry week</li>
                      <li>• Monthly options expire on the last Tuesday of the expiry month</li>
                      <li>• Real-time expiry data is fetched from Fyers API when connected</li>
                      <li>• Auto-refresh ensures accurate expiry calculations</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Notifications Tab */}
        {activeTab === 'notifications' && (
          <div className="space-y-6">
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <h3 className="text-xl font-bold text-white mb-6">Notification Settings</h3>
              
              <div className="space-y-6">
                {[
                  { id: 'connection', label: 'Connection Status', description: 'Notify when exchange connections are lost or restored' },
                  { id: 'errors', label: 'API Errors', description: 'Alert when API calls fail or return errors' },
                  { id: 'limits', label: 'Rate Limits', description: 'Warning when approaching rate limit thresholds' },
                  { id: 'expiry', label: 'Option Expiry', description: 'Reminders about upcoming option expiry dates' },
                  { id: 'trades', label: 'Trade Execution', description: 'Confirmation notifications for executed trades' }
                ].map((notification) => (
                  <div key={notification.id} className="flex items-center justify-between p-4 bg-slate-800 rounded-lg">
                    <div>
                      <h4 className="font-medium text-white">{notification.label}</h4>
                      <p className="text-sm text-slate-400">{notification.description}</p>
                    </div>
                    <input
                      type="checkbox"
                      defaultChecked={true}
                      className="text-blue-600"
                    />
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Save Status */}
        {saveStatus !== 'idle' && (
          <div className="fixed bottom-4 right-4 z-50">
            <div className={`flex items-center px-4 py-2 rounded-lg border ${
              saveStatus === 'saving' ? 'bg-blue-900/20 border-blue-500/30 text-blue-400' :
              saveStatus === 'saved' ? 'bg-green-900/20 border-green-500/30 text-green-400' :
              'bg-red-900/20 border-red-500/30 text-red-400'
            }`}>
              {saveStatus === 'saving' && <RefreshCw className="h-4 w-4 mr-2 animate-spin" />}
              {saveStatus === 'saved' && <CheckCircle className="h-4 w-4 mr-2" />}
              {saveStatus === 'error' && <AlertCircle className="h-4 w-4 mr-2" />}
              
              <span>
                {saveStatus === 'saving' && 'Saving...'}
                {saveStatus === 'saved' && 'Settings saved successfully'}
                {saveStatus === 'error' && 'Failed to save settings'}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}