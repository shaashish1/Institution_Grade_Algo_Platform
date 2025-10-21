'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  Globe, ArrowUpRight, Activity, TrendingUp, Shield, 
  Star, Clock, Users, BarChart3, Zap, CheckCircle,
  Filter, Search, RefreshCw, ExternalLink, AlertCircle,
  Building2, Coins, DollarSign, Target, Eye, Settings
} from 'lucide-react';
import { mcpService, ExchangeInfo } from '@/services/mcpService';

interface Exchange {
  id: string;
  name: string;
  logo: string;
  url: string;
  description: string;
  status: 'active' | 'maintenance' | 'inactive';
  fees: {
    maker: number;
    taker: number;
  };
  features: string[];
  volume24h: number;
  pairs: number;
  countries: string[];
  established: number;
  rating: number;
  apis: {
    rest: boolean;
    websocket: boolean;
    sandbox: boolean;
  };
  supportedAssets: string[];
  categories: string[];
}

// Top 10 supported exchanges with working logos
const exchanges: Exchange[] = [
  {
    id: 'binance',
    name: 'Binance',
    logo: 'https://logo.clearbit.com/binance.com',
    url: 'https://binance.com',
    description: 'World\'s largest cryptocurrency exchange by trading volume',
    status: 'active',
    fees: { maker: 0.1, taker: 0.1 },
    features: ['Spot Trading', 'Futures', 'Options', 'Margin', 'Staking', 'NFT'],
    volume24h: 15800000000,
    pairs: 1500,
    countries: ['Global'],
    established: 2017,
    rating: 4.8,
    apis: { rest: true, websocket: true, sandbox: true },
    supportedAssets: ['BTC', 'ETH', 'BNB', 'ADA', 'DOT', 'SOL'],
    categories: ['Crypto', 'Spot', 'Derivatives']
  },
  {
    id: 'coinbase',
    name: 'Coinbase Advanced',
    logo: 'https://logo.clearbit.com/coinbase.com',
    url: 'https://coinbase.com',
    description: 'Leading US-based cryptocurrency exchange with high security',
    status: 'active',
    fees: { maker: 0.5, taker: 0.5 },
    features: ['Spot Trading', 'Institutional', 'Custody', 'Vault', 'Advanced API'],
    volume24h: 2800000000,
    pairs: 280,
    countries: ['US', 'EU', 'UK', 'Canada'],
    established: 2012,
    rating: 4.5,
    apis: { rest: true, websocket: true, sandbox: true },
    supportedAssets: ['BTC', 'ETH', 'LTC', 'BCH', 'ADA', 'DOT'],
    categories: ['Crypto', 'Spot', 'Institutional']
  },
  {
    id: 'kraken',
    name: 'Kraken',
    logo: 'https://logo.clearbit.com/kraken.com',
    url: 'https://kraken.com',
    description: 'Secure and reliable crypto exchange with advanced trading features',
    status: 'active',
    fees: { maker: 0.16, taker: 0.26 },
    features: ['Spot Trading', 'Futures', 'Margin', 'Staking', 'OTC', 'Bank Funding'],
    volume24h: 1200000000,
    pairs: 400,
    countries: ['US', 'EU', 'Canada', 'Japan'],
    established: 2011,
    rating: 4.6,
    apis: { rest: true, websocket: true, sandbox: false },
    supportedAssets: ['BTC', 'ETH', 'XRP', 'LTC', 'ADA', 'USDT'],
    categories: ['Crypto', 'Spot', 'Derivatives']
  },
  {
    id: 'okx',
    name: 'OKX',
    logo: 'https://logo.clearbit.com/okx.com',
    url: 'https://okx.com',
    description: 'Global crypto exchange with comprehensive trading products',
    status: 'active',
    fees: { maker: 0.08, taker: 0.1 },
    features: ['Spot Trading', 'Futures', 'Options', 'Copy Trading', 'DeFi', 'NFT'],
    volume24h: 8900000000,
    pairs: 800,
    countries: ['Global'],
    established: 2017,
    rating: 4.4,
    apis: { rest: true, websocket: true, sandbox: true },
    supportedAssets: ['BTC', 'ETH', 'OKB', 'LTC', 'DOT', 'LINK'],
    categories: ['Crypto', 'Spot', 'Derivatives']
  },
  {
    id: 'bybit',
    name: 'Bybit',
    logo: 'https://logo.clearbit.com/bybit.com',
    url: 'https://bybit.com',
    description: 'Derivatives-focused exchange with high leverage trading',
    status: 'active',
    fees: { maker: -0.025, taker: 0.075 },
    features: ['Derivatives', 'Spot Trading', 'Copy Trading', 'Launchpad', 'Earn'],
    volume24h: 4200000000,
    pairs: 600,
    countries: ['Global'],
    established: 2018,
    rating: 4.3,
    apis: { rest: true, websocket: true, sandbox: true },
    supportedAssets: ['BTC', 'ETH', 'BIT', 'SOL', 'AVAX', 'MATIC'],
    categories: ['Crypto', 'Derivatives']
  },
  {
    id: 'kucoin',
    name: 'KuCoin',
    logo: 'https://logo.clearbit.com/kucoin.com',
    url: 'https://kucoin.com',
    description: 'People\'s exchange with extensive altcoin selection',
    status: 'active',
    fees: { maker: 0.1, taker: 0.1 },
    features: ['Spot Trading', 'Futures', 'Margin', 'Pool-X', 'Lending', 'Bot Trading'],
    volume24h: 1800000000,
    pairs: 1200,
    countries: ['Global'],
    established: 2017,
    rating: 4.2,
    apis: { rest: true, websocket: true, sandbox: true },
    supportedAssets: ['BTC', 'ETH', 'KCS', 'USDT', 'LTC', 'ADA'],
    categories: ['Crypto', 'Spot', 'Derivatives']
  },
  {
    id: 'huobi',
    name: 'HTX (Huobi)',
    logo: 'https://logo.clearbit.com/htx.com',
    url: 'https://htx.com',
    description: 'Global leading digital asset exchange',
    status: 'active',
    fees: { maker: 0.2, taker: 0.2 },
    features: ['Spot Trading', 'Futures', 'Options', 'ETF', 'Staking', 'Earn'],
    volume24h: 3100000000,
    pairs: 900,
    countries: ['Global'],
    established: 2013,
    rating: 4.1,
    apis: { rest: true, websocket: true, sandbox: true },
    supportedAssets: ['BTC', 'ETH', 'HT', 'USDT', 'LTC', 'EOS'],
    categories: ['Crypto', 'Spot', 'Derivatives']
  },
  {
    id: 'gate',
    name: 'Gate.io',
    logo: 'https://logo.clearbit.com/gate.io',
    url: 'https://gate.io',
    description: 'Comprehensive crypto trading platform with DeFi integration',
    status: 'active',
    fees: { maker: 0.2, taker: 0.2 },
    features: ['Spot Trading', 'Futures', 'Options', 'Copy Trading', 'DeFi', 'Startup'],
    volume24h: 2400000000,
    pairs: 1800,
    countries: ['Global'],
    established: 2013,
    rating: 4.0,
    apis: { rest: true, websocket: true, sandbox: false },
    supportedAssets: ['BTC', 'ETH', 'GT', 'USDT', 'TRX', 'LTC'],
    categories: ['Crypto', 'Spot', 'Derivatives']
  },
  {
    id: 'bitget',
    name: 'Bitget',
    logo: 'https://logo.clearbit.com/bitget.com',
    url: 'https://bitget.com',
    description: 'Social trading platform with copy trading features',
    status: 'active',
    fees: { maker: 0.1, taker: 0.1 },
    features: ['Spot Trading', 'Futures', 'Copy Trading', 'Launchpad', 'Earn', 'P2P'],
    volume24h: 3500000000,
    pairs: 700,
    countries: ['Global'],
    established: 2018,
    rating: 4.2,
    apis: { rest: true, websocket: true, sandbox: true },
    supportedAssets: ['BTC', 'ETH', 'BGB', 'USDT', 'SOL', 'AVAX'],
    categories: ['Crypto', 'Spot', 'Derivatives']
  },
  {
    id: 'mexc',
    name: 'MEXC',
    logo: 'https://logo.clearbit.com/mexc.com',
    url: 'https://mexc.com',
    description: 'High-performance digital asset trading platform',
    status: 'active',
    fees: { maker: 0.2, taker: 0.2 },
    features: ['Spot Trading', 'Futures', 'ETF', 'Launchpad', 'Savings', 'Kickstarter'],
    volume24h: 2200000000,
    pairs: 1500,
    countries: ['Global'],
    established: 2018,
    rating: 4.0,
    apis: { rest: true, websocket: true, sandbox: true },
    supportedAssets: ['BTC', 'ETH', 'MX', 'USDT', 'BNB', 'LTC'],
    categories: ['Crypto', 'Spot', 'Derivatives']
  }
];

export default function Exchanges() {
  const [filteredExchanges, setFilteredExchanges] = useState<Exchange[]>(exchanges);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'volume' | 'rating' | 'pairs' | 'fees'>('volume');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  const categories = ['all', 'crypto', 'spot', 'derivatives', 'institutional'];

  useEffect(() => {
    let filtered = exchanges.filter(exchange => {
      const matchesSearch = exchange.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           exchange.description.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesCategory = selectedCategory === 'all' || 
                             exchange.categories.some(cat => 
                               cat.toLowerCase() === selectedCategory.toLowerCase()
                             );
      
      return matchesSearch && matchesCategory;
    });

    // Sort exchanges
    filtered.sort((a, b) => {
      let comparison = 0;
      switch (sortBy) {
        case 'volume':
          comparison = a.volume24h - b.volume24h;
          break;
        case 'rating':
          comparison = a.rating - b.rating;
          break;
        case 'pairs':
          comparison = a.pairs - b.pairs;
          break;
        case 'fees':
          comparison = a.fees.taker - b.fees.taker;
          break;
      }
      return sortOrder === 'desc' ? -comparison : comparison;
    });

    setFilteredExchanges(filtered);
  }, [searchTerm, selectedCategory, sortBy, sortOrder]);

  const formatVolume = (volume: number) => {
    if (volume >= 1e9) return `$${(volume / 1e9).toFixed(1)}B`;
    if (volume >= 1e6) return `$${(volume / 1e6).toFixed(1)}M`;
    return `$${volume.toLocaleString()}`;
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'maintenance': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'inactive': return 'bg-red-500/20 text-red-400 border-red-500/30';
      default: return 'bg-slate-500/20 text-slate-400 border-slate-500/30';
    }
  };

  const getRatingStars = (rating: number) => {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    
    return (
      <div className="flex items-center">
        {[...Array(5)].map((_, i) => (
          <Star
            key={i}
            className={`h-4 w-4 ${
              i < fullStars 
                ? 'text-yellow-400 fill-yellow-400'
                : i === fullStars && hasHalfStar
                ? 'text-yellow-400 fill-yellow-400/50'
                : 'text-slate-600'
            }`}
          />
        ))}
        <span className="ml-1 text-sm text-slate-400">{rating.toFixed(1)}</span>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4">
      <div className="max-w-7xl mx-auto">
        {/* Breadcrumb */}
        <div className="mb-6">
          <nav className="flex items-center space-x-2 text-sm text-slate-400">
            <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
            <span>/</span>
            <span className="text-white">Exchanges</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
                Supported Exchanges
              </h1>
              <p className="text-xl text-slate-300">
                Trade across {exchanges.length} top-tier global cryptocurrency exchanges
              </p>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="bg-slate-900 rounded-lg p-4 border border-slate-800">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-400">{exchanges.length}</div>
                  <div className="text-sm text-slate-400">Exchanges</div>
                </div>
              </div>
              <div className="bg-slate-900 rounded-lg p-4 border border-slate-800">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-400">
                    {exchanges.reduce((sum, ex) => sum + ex.pairs, 0).toLocaleString()}
                  </div>
                  <div className="text-sm text-slate-400">Trading Pairs</div>
                </div>
              </div>
            </div>
          </div>

          {/* Platform Integration Info */}
          <div className="bg-blue-900/20 border border-blue-500/30 rounded-xl p-6 mb-6">
            <div className="flex items-start space-x-4">
              <div className="bg-blue-500/20 rounded-lg p-3">
                <Zap className="h-6 w-6 text-blue-400" />
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-blue-400 mb-2">
                  Unified Trading Platform
                </h3>
                <p className="text-slate-300 mb-3">
                  Our institutional-grade platform provides unified access to the world's leading cryptocurrency exchanges. 
                  Trade seamlessly across multiple exchanges with consistent APIs, real-time data, and advanced order management.
                </p>
                <div className="flex items-center space-x-4">
                  <Link 
                    href="/settings/exchanges"
                    className="flex items-center text-blue-400 hover:text-blue-300 transition-colors"
                  >
                    <Settings className="h-4 w-4 mr-1" />
                    Configure API Keys
                  </Link>
                  <Link 
                    href="/charts"
                    className="flex items-center text-blue-400 hover:text-blue-300 transition-colors"
                  >
                    <BarChart3 className="h-4 w-4 mr-1" />
                    Live Charts
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Search */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
              <input
                type="text"
                placeholder="Search exchanges..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:border-blue-500 focus:outline-none"
              />
            </div>

            {/* Category Filter */}
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:border-blue-500 focus:outline-none"
            >
              {categories.map(category => (
                <option key={category} value={category}>
                  {category.charAt(0).toUpperCase() + category.slice(1)}
                </option>
              ))}
            </select>

            {/* Sort By */}
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:border-blue-500 focus:outline-none"
            >
              <option value="volume">Volume</option>
              <option value="rating">Rating</option>
              <option value="pairs">Trading Pairs</option>
              <option value="fees">Fees</option>
            </select>

            {/* Sort Order */}
            <button
              onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
              className="flex items-center justify-center px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white hover:bg-slate-700 transition-colors"
            >
              {sortOrder === 'desc' ? (
                <>
                  <BarChart3 className="h-4 w-4 mr-2" />
                  High to Low
                </>
              ) : (
                <>
                  <BarChart3 className="h-4 w-4 mr-2 transform rotate-180" />
                  Low to High
                </>
              )}
            </button>
          </div>
        </div>

        {/* Exchange Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {filteredExchanges.map((exchange) => (
            <div key={exchange.id} className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden hover:border-blue-500/50 transition-all duration-300 group">
              {/* Header */}
              <div className="p-6 pb-4">
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
                      <h3 className="font-bold text-white group-hover:text-blue-400 transition-colors">
                        {exchange.name}
                      </h3>
                      <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs border ${getStatusColor(exchange.status)}`}>
                        <div className="w-1.5 h-1.5 rounded-full bg-current mr-1"></div>
                        {exchange.status}
                      </div>
                    </div>
                  </div>
                  
                  <a
                    href={exchange.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-slate-400 hover:text-blue-400 transition-colors"
                  >
                    <ExternalLink className="h-4 w-4" />
                  </a>
                </div>

                <p className="text-slate-400 text-sm mb-4 line-clamp-2">
                  {exchange.description}
                </p>

                {/* Rating */}
                <div className="mb-4">
                  {getRatingStars(exchange.rating)}
                </div>
              </div>

              {/* Stats */}
              <div className="px-6 pb-4">
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <div className="text-xs text-slate-400 mb-1">24h Volume</div>
                    <div className="font-mono text-green-400 font-semibold">
                      {formatVolume(exchange.volume24h)}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-slate-400 mb-1">Trading Pairs</div>
                    <div className="font-mono text-blue-400 font-semibold">
                      {exchange.pairs.toLocaleString()}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-slate-400 mb-1">Maker Fee</div>
                    <div className="font-mono text-yellow-400 font-semibold">
                      {exchange.fees.maker}%
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-slate-400 mb-1">Taker Fee</div>
                    <div className="font-mono text-orange-400 font-semibold">
                      {exchange.fees.taker}%
                    </div>
                  </div>
                </div>

                {/* Features */}
                <div className="mb-4">
                  <div className="text-xs text-slate-400 mb-2">Features</div>
                  <div className="flex flex-wrap gap-1">
                    {exchange.features.slice(0, 4).map((feature, idx) => (
                      <span key={idx} className="px-2 py-1 bg-slate-800 text-slate-300 text-xs rounded">
                        {feature}
                      </span>
                    ))}
                    {exchange.features.length > 4 && (
                      <span className="px-2 py-1 bg-slate-800 text-slate-400 text-xs rounded">
                        +{exchange.features.length - 4} more
                      </span>
                    )}
                  </div>
                </div>

                {/* API Support */}
                <div className="mb-4">
                  <div className="text-xs text-slate-400 mb-2">API Support</div>
                  <div className="flex space-x-2">
                    {exchange.apis.rest && (
                      <span className="flex items-center px-2 py-1 bg-green-900/30 text-green-400 text-xs rounded border border-green-500/30">
                        <CheckCircle className="h-3 w-3 mr-1" />
                        REST
                      </span>
                    )}
                    {exchange.apis.websocket && (
                      <span className="flex items-center px-2 py-1 bg-blue-900/30 text-blue-400 text-xs rounded border border-blue-500/30">
                        <Zap className="h-3 w-3 mr-1" />
                        WebSocket
                      </span>
                    )}
                    {exchange.apis.sandbox && (
                      <span className="flex items-center px-2 py-1 bg-purple-900/30 text-purple-400 text-xs rounded border border-purple-500/30">
                        <Settings className="h-3 w-3 mr-1" />
                        Sandbox
                      </span>
                    )}
                  </div>
                </div>

                {/* Assets */}
                <div>
                  <div className="text-xs text-slate-400 mb-2">Top Assets</div>
                  <div className="flex flex-wrap gap-1">
                    {exchange.supportedAssets.slice(0, 6).map((asset, idx) => (
                      <span key={idx} className="px-2 py-1 bg-slate-800 text-blue-400 text-xs rounded font-mono">
                        {asset}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Footer */}
              <div className="px-6 py-4 bg-slate-800/50 border-t border-slate-700">
                <div className="flex items-center justify-between text-xs text-slate-400">
                  <span>Est. {exchange.established}</span>
                  <span>{exchange.countries.join(', ')}</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Integration Instructions */}
        <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center">
            <Settings className="h-5 w-5 mr-2 text-blue-400" />
            Integration Guide
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-3">
              <h3 className="font-semibold text-green-400">1. API Configuration</h3>
              <p className="text-slate-400 text-sm">
                Set up API keys for your chosen exchanges in the platform settings. 
                We securely store and encrypt all credentials.
              </p>
            </div>
            
            <div className="space-y-3">
              <h3 className="font-semibold text-blue-400">2. Test Connection</h3>
              <p className="text-slate-400 text-sm">
                Use our built-in connection tester to verify API access and 
                ensure proper configuration before live trading.
              </p>
            </div>
            
            <div className="space-y-3">
              <h3 className="font-semibold text-purple-400">3. Start Trading</h3>
              <p className="text-slate-400 text-sm">
                Execute strategies across multiple exchanges simultaneously 
                with unified risk management and portfolio tracking.
              </p>
            </div>
          </div>
          
          <div className="mt-6 flex flex-wrap gap-4">
            <Link
              href="/settings/exchanges"
              className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
            >
              <Settings className="h-4 w-4 mr-2" />
              Configure Exchanges
            </Link>
            <Link
              href="/docs/exchanges"
              className="flex items-center px-4 py-2 bg-slate-800 border border-slate-700 hover:bg-slate-700 rounded-lg transition-colors"
            >
              <Eye className="h-4 w-4 mr-2" />
              View Documentation
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}