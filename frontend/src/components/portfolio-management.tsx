'use client';

import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, TrendingDown, BarChart3, DollarSign, Target, Activity, 
  Crown, Zap, AlertCircle, CheckCircle, Eye, PlayCircle, Settings,
  Calendar, Clock, Bell, RefreshCw, ArrowUpRight, ArrowDownRight,
  PieChart, LineChart, Users, Building2, Coins, Filter, Download,
  Plus, Minus, MoreVertical, Edit, Trash2, Search, SortAsc, SortDesc
} from 'lucide-react';
import Link from 'next/link';

interface Holding {
  id: string;
  symbol: string;
  name: string;
  type: 'stock' | 'option' | 'crypto' | 'etf' | 'futures';
  quantity: number;
  avgPrice: number;
  currentPrice: number;
  pnl: number;
  pnlPercent: number;
  value: number;
  allocation: number;
  dayChange: number;
  dayChangePercent: number;
  strike?: number;
  expiry?: string;
  sector?: string;
  exchange?: string;
}

interface PortfolioStats {
  totalValue: number;
  totalCost: number;
  totalPnL: number;
  totalPnLPercent: number;
  dayChange: number;
  dayChangePercent: number;
  cash: number;
  marginUsed: number;
  marginAvailable: number;
}

interface AssetAllocation {
  type: string;
  value: number;
  percentage: number;
  color: string;
}

interface SectorAllocation {
  sector: string;
  value: number;
  percentage: number;
  color: string;
}

export function PortfolioManagement() {
  const [portfolioStats, setPortfolioStats] = useState<PortfolioStats>({
    totalValue: 12450000,
    totalCost: 10000000,
    totalPnL: 2450000,
    totalPnLPercent: 24.5,
    dayChange: 156000,
    dayChangePercent: 1.27,
    cash: 3200000,
    marginUsed: 2100000,
    marginAvailable: 5400000
  });

  const [holdings, setHoldings] = useState<Holding[]>([
    {
      id: '1',
      symbol: 'NIFTY 25700 CE',
      name: 'Nifty Call Option',
      type: 'option',
      quantity: 100,
      avgPrice: 156,
      currentPrice: 189,
      pnl: 3300,
      pnlPercent: 21.15,
      value: 18900,
      allocation: 1.52,
      dayChange: 450,
      dayChangePercent: 2.44,
      strike: 25700,
      expiry: '28-Nov-24',
      exchange: 'NSE'
    },
    {
      id: '2',
      symbol: 'RELIANCE',
      name: 'Reliance Industries Limited',
      type: 'stock',
      quantity: 50,
      avgPrice: 2450,
      currentPrice: 2478,
      pnl: 1400,
      pnlPercent: 1.14,
      value: 123900,
      allocation: 9.95,
      dayChange: 890,
      dayChangePercent: 0.72,
      sector: 'Energy',
      exchange: 'NSE'
    },
    {
      id: '3',
      symbol: 'BTC/USDT',
      name: 'Bitcoin',
      type: 'crypto',
      quantity: 0.5,
      avgPrice: 96800,
      currentPrice: 98456,
      pnl: 828,
      pnlPercent: 1.71,
      value: 49228,
      allocation: 3.95,
      dayChange: 623,
      dayChangePercent: 1.28,
      exchange: 'Binance'
    },
    {
      id: '4',
      symbol: 'NIFTYBEES',
      name: 'Nippon India ETF Nifty BeES',
      type: 'etf',
      quantity: 1000,
      avgPrice: 257.5,
      currentPrice: 259.2,
      pnl: 1700,
      pnlPercent: 0.66,
      value: 259200,
      allocation: 20.83,
      dayChange: 1040,
      dayChangePercent: 0.40,
      sector: 'Diversified',
      exchange: 'NSE'
    },
    {
      id: '5',
      symbol: 'HDFCBANK',
      name: 'HDFC Bank Limited',
      type: 'stock',
      quantity: 25,
      avgPrice: 1650,
      currentPrice: 1678,
      pnl: 700,
      pnlPercent: 1.70,
      value: 41950,
      allocation: 3.37,
      dayChange: 210,
      dayChangePercent: 0.50,
      sector: 'Banking',
      exchange: 'NSE'
    }
  ]);

  const [assetAllocation] = useState<AssetAllocation[]>([
    { type: 'Stocks', value: 6500000, percentage: 52.2, color: 'bg-blue-500' },
    { type: 'ETFs', value: 2800000, percentage: 22.5, color: 'bg-green-500' },
    { type: 'Options', value: 1850000, percentage: 14.9, color: 'bg-purple-500' },
    { type: 'Crypto', value: 950000, percentage: 7.6, color: 'bg-yellow-500' },
    { type: 'Cash', value: 350000, percentage: 2.8, color: 'bg-slate-500' }
  ]);

  const [sectorAllocation] = useState<SectorAllocation[]>([
    { sector: 'Banking', value: 3200000, percentage: 25.7, color: 'bg-blue-600' },
    { sector: 'Technology', value: 2800000, percentage: 22.5, color: 'bg-purple-600' },
    { sector: 'Energy', value: 1900000, percentage: 15.3, color: 'bg-orange-600' },
    { sector: 'Healthcare', value: 1200000, percentage: 9.6, color: 'bg-green-600' },
    { sector: 'Consumer', value: 950000, percentage: 7.6, color: 'bg-red-600' },
    { sector: 'Others', value: 2400000, percentage: 19.3, color: 'bg-slate-600' }
  ]);

  const [selectedAssetType, setSelectedAssetType] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('value');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [searchTerm, setSearchTerm] = useState('');

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  };

  const formatNumber = (value: number) => {
    if (value >= 10000000) return `₹${(value / 10000000).toFixed(1)}Cr`;
    if (value >= 100000) return `₹${(value / 100000).toFixed(1)}L`;
    if (value >= 1000) return `₹${(value / 1000).toFixed(1)}K`;
    return `₹${value.toFixed(0)}`;
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'stock': return 'text-blue-400 bg-blue-500/10';
      case 'option': return 'text-purple-400 bg-purple-500/10';
      case 'crypto': return 'text-yellow-400 bg-yellow-500/10';
      case 'etf': return 'text-green-400 bg-green-500/10';
      case 'futures': return 'text-orange-400 bg-orange-500/10';
      default: return 'text-slate-400 bg-slate-500/10';
    }
  };

  const filteredHoldings = holdings.filter(holding => {
    const matchesType = selectedAssetType === 'all' || holding.type === selectedAssetType;
    const matchesSearch = holding.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         holding.name.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesType && matchesSearch;
  });

  const sortedHoldings = [...filteredHoldings].sort((a, b) => {
    let aVal, bVal;
    switch (sortBy) {
      case 'symbol':
        aVal = a.symbol;
        bVal = b.symbol;
        break;
      case 'value':
        aVal = a.value;
        bVal = b.value;
        break;
      case 'pnl':
        aVal = a.pnl;
        bVal = b.pnl;
        break;
      case 'allocation':
        aVal = a.allocation;
        bVal = b.allocation;
        break;
      default:
        aVal = a.value;
        bVal = b.value;
    }

    if (typeof aVal === 'string') {
      return sortOrder === 'asc' ? aVal.localeCompare(bVal as string) : (bVal as string).localeCompare(aVal);
    }
    return sortOrder === 'asc' ? (aVal as number) - (bVal as number) : (bVal as number) - (aVal as number);
  });

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4">
      <div className="max-w-full mx-auto">
        {/* Navigation Breadcrumb */}
        <div className="mb-6">
          <nav className="flex items-center space-x-2 text-sm text-slate-400">
            <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
            <span>/</span>
            <Link href="/dashboard" className="hover:text-blue-400 transition-colors">Dashboard</Link>
            <span>/</span>
            <span className="text-white">Portfolio</span>
          </nav>
        </div>

        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
              Portfolio Management
            </h1>
            <p className="text-slate-400">
              Comprehensive view of your holdings, performance, and asset allocation
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            <button className="flex items-center px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors">
              <Download className="h-4 w-4 mr-2" />
              Export
            </button>
            <button className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors">
              <RefreshCw className="h-4 w-4 mr-2" />
              Refresh
            </button>
          </div>
        </div>

        {/* Portfolio Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-slate-400 text-sm font-medium">Total Value</h3>
              <DollarSign className="h-5 w-5 text-blue-400" />
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              {formatCurrency(portfolioStats.totalValue)}
            </div>
            <div className={`flex items-center text-sm ${
              portfolioStats.dayChange >= 0 ? 'text-green-400' : 'text-red-400'
            }`}>
              {portfolioStats.dayChange >= 0 ? (
                <TrendingUp className="h-4 w-4 mr-1" />
              ) : (
                <TrendingDown className="h-4 w-4 mr-1" />
              )}
              {formatNumber(Math.abs(portfolioStats.dayChange))} ({portfolioStats.dayChangePercent.toFixed(2)}%)
            </div>
          </div>

          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-slate-400 text-sm font-medium">Total P&L</h3>
              <Target className="h-5 w-5 text-green-400" />
            </div>
            <div className="text-2xl font-bold text-green-400 mb-1">
              +{formatCurrency(portfolioStats.totalPnL)}
            </div>
            <div className="text-sm text-green-400">
              +{portfolioStats.totalPnLPercent.toFixed(1)}% Overall
            </div>
          </div>

          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-slate-400 text-sm font-medium">Available Cash</h3>
              <Activity className="h-5 w-5 text-purple-400" />
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              {formatCurrency(portfolioStats.cash)}
            </div>
            <div className="text-sm text-slate-400">
              Ready for trading
            </div>
          </div>

          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-slate-400 text-sm font-medium">Margin Used</h3>
              <BarChart3 className="h-5 w-5 text-orange-400" />
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              {formatCurrency(portfolioStats.marginUsed)}
            </div>
            <div className="text-sm text-slate-400">
              Available: {formatNumber(portfolioStats.marginAvailable)}
            </div>
          </div>

          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-slate-400 text-sm font-medium">Total Holdings</h3>
              <Users className="h-5 w-5 text-indigo-400" />
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              {holdings.length}
            </div>
            <div className="text-sm text-slate-400">
              Active positions
            </div>
          </div>
        </div>

        {/* Asset & Sector Allocation */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center">
              <PieChart className="h-5 w-5 mr-2 text-blue-400" />
              Asset Allocation
            </h2>
            
            <div className="space-y-4">
              {assetAllocation.map((asset, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className={`w-4 h-4 rounded ${asset.color}`} />
                    <span className="text-white font-medium">{asset.type}</span>
                  </div>
                  <div className="text-right">
                    <div className="text-white font-mono">{formatNumber(asset.value)}</div>
                    <div className="text-slate-400 text-sm">{asset.percentage.toFixed(1)}%</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center">
              <BarChart3 className="h-5 w-5 mr-2 text-green-400" />
              Sector Allocation
            </h2>
            
            <div className="space-y-4">
              {sectorAllocation.map((sector, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className={`w-4 h-4 rounded ${sector.color}`} />
                    <span className="text-white font-medium">{sector.sector}</span>
                  </div>
                  <div className="text-right">
                    <div className="text-white font-mono">{formatNumber(sector.value)}</div>
                    <div className="text-slate-400 text-sm">{sector.percentage.toFixed(1)}%</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Holdings Table */}
        <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-white">Holdings</h2>
            
            <div className="flex items-center gap-4">
              <div className="relative">
                <Search className="h-4 w-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search holdings..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500"
                />
              </div>
              
              <select
                value={selectedAssetType}
                onChange={(e) => setSelectedAssetType(e.target.value)}
                className="px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
              >
                <option value="all">All Assets</option>
                <option value="stock">Stocks</option>
                <option value="option">Options</option>
                <option value="crypto">Crypto</option>
                <option value="etf">ETFs</option>
                <option value="futures">Futures</option>
              </select>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-800">
                <tr>
                  <th className="px-4 py-3 text-left">
                    <button
                      onClick={() => {
                        setSortBy('symbol');
                        setSortOrder(sortBy === 'symbol' && sortOrder === 'asc' ? 'desc' : 'asc');
                      }}
                      className="flex items-center hover:text-blue-400"
                    >
                      Symbol
                      {sortBy === 'symbol' && (
                        sortOrder === 'asc' ? <SortAsc className="h-3 w-3 ml-1" /> : <SortDesc className="h-3 w-3 ml-1" />
                      )}
                    </button>
                  </th>
                  <th className="px-4 py-3 text-left">Type</th>
                  <th className="px-4 py-3 text-right">Quantity</th>
                  <th className="px-4 py-3 text-right">Avg Price</th>
                  <th className="px-4 py-3 text-right">Current Price</th>
                  <th className="px-4 py-3 text-right">
                    <button
                      onClick={() => {
                        setSortBy('value');
                        setSortOrder(sortBy === 'value' && sortOrder === 'desc' ? 'asc' : 'desc');
                      }}
                      className="flex items-center hover:text-blue-400"
                    >
                      Value
                      {sortBy === 'value' && (
                        sortOrder === 'asc' ? <SortAsc className="h-3 w-3 ml-1" /> : <SortDesc className="h-3 w-3 ml-1" />
                      )}
                    </button>
                  </th>
                  <th className="px-4 py-3 text-right">
                    <button
                      onClick={() => {
                        setSortBy('pnl');
                        setSortOrder(sortBy === 'pnl' && sortOrder === 'desc' ? 'asc' : 'desc');
                      }}
                      className="flex items-center hover:text-blue-400"
                    >
                      P&L
                      {sortBy === 'pnl' && (
                        sortOrder === 'asc' ? <SortAsc className="h-3 w-3 ml-1" /> : <SortDesc className="h-3 w-3 ml-1" />
                      )}
                    </button>
                  </th>
                  <th className="px-4 py-3 text-right">Day Change</th>
                  <th className="px-4 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {sortedHoldings.map((holding) => (
                  <tr key={holding.id} className="border-t border-slate-800 hover:bg-slate-800/50">
                    <td className="px-4 py-3">
                      <div>
                        <div className="font-medium text-white">{holding.symbol}</div>
                        <div className="text-xs text-slate-400">{holding.name}</div>
                        {holding.expiry && (
                          <div className="text-xs text-purple-400">Exp: {holding.expiry}</div>
                        )}
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${getTypeColor(holding.type)}`}>
                        {holding.type.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-right font-mono text-white">
                      {holding.quantity}
                    </td>
                    <td className="px-4 py-3 text-right font-mono text-slate-300">
                      ₹{holding.avgPrice.toFixed(2)}
                    </td>
                    <td className="px-4 py-3 text-right font-mono text-white">
                      ₹{holding.currentPrice.toFixed(2)}
                    </td>
                    <td className="px-4 py-3 text-right font-mono text-white">
                      {formatNumber(holding.value)}
                    </td>
                    <td className={`px-4 py-3 text-right font-mono ${
                      holding.pnl >= 0 ? 'text-green-400' : 'text-red-400'
                    }`}>
                      {holding.pnl >= 0 ? '+' : ''}{formatNumber(holding.pnl)}
                      <div className="text-xs">
                        {holding.pnlPercent >= 0 ? '+' : ''}{holding.pnlPercent.toFixed(2)}%
                      </div>
                    </td>
                    <td className={`px-4 py-3 text-right font-mono ${
                      holding.dayChange >= 0 ? 'text-green-400' : 'text-red-400'
                    }`}>
                      {holding.dayChange >= 0 ? '+' : ''}{formatNumber(holding.dayChange)}
                      <div className="text-xs">
                        {holding.dayChangePercent >= 0 ? '+' : ''}{holding.dayChangePercent.toFixed(2)}%
                      </div>
                    </td>
                    <td className="px-4 py-3 text-right">
                      <div className="flex items-center justify-end space-x-2">
                        <button className="p-1 text-slate-400 hover:text-blue-400 transition-colors">
                          <Edit className="h-4 w-4" />
                        </button>
                        <button className="p-1 text-slate-400 hover:text-red-400 transition-colors">
                          <Trash2 className="h-4 w-4" />
                        </button>
                        <button className="p-1 text-slate-400 hover:text-white transition-colors">
                          <MoreVertical className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}