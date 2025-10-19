'use client';

import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Calendar, Target, AlertCircle, DollarSign, Building2, Clock, Users, BarChart3, Download, Eye, Filter, RefreshCw } from 'lucide-react';
import Link from 'next/link';

interface FuturesData {
  symbol: string;
  expiry: string;
  ltp: number;
  change: number;
  changePercent: number;
  openInterest: number;
  volume: number;
  basis: number; // Difference between futures and spot
  lot_size: number;
  margin_required: number;
  delivery_date: string;
}

interface IPOData {
  company_name: string;
  issue_size: string;
  price_band: string;
  open_date: string;
  close_date: string;
  listing_date: string;
  lot_size: number;
  status: 'upcoming' | 'open' | 'closed' | 'listed';
  subscription: number;
  category: 'mainboard' | 'sme';
  sector: string;
  lead_managers: string[];
  gmp: number; // Grey Market Premium
  estimated_listing_price: number;
}

interface DerivativesPortfolio {
  position_id: string;
  symbol: string;
  type: 'futures' | 'options';
  position_type: 'long' | 'short';
  quantity: number;
  entry_price: number;
  current_price: number;
  pnl: number;
  margin_used: number;
  expiry_date: string;
  days_to_expiry: number;
}

// Sample Futures Data
const FUTURES_DATA: FuturesData[] = [
  {
    symbol: 'NIFTY',
    expiry: '28-NOV-2025',
    ltp: 25745.50,
    change: 35.65,
    changePercent: 0.14,
    openInterest: 2847593,
    volume: 156743,
    basis: 35.65,
    lot_size: 50,
    margin_required: 180000,
    delivery_date: '28-NOV-2025'
  },
  {
    symbol: 'BANKNIFTY',
    expiry: '28-NOV-2025',
    ltp: 54823.75,
    change: -45.50,
    changePercent: -0.08,
    openInterest: 1234567,
    volume: 89432,
    basis: 34.50,
    lot_size: 15,
    margin_required: 165000,
    delivery_date: '28-NOV-2025'
  },
  {
    symbol: 'RELIANCE',
    expiry: '28-NOV-2025',
    ltp: 1298.45,
    change: 8.90,
    changePercent: 0.69,
    openInterest: 567890,
    volume: 234567,
    basis: 3.60,
    lot_size: 250,
    margin_required: 48000,
    delivery_date: '28-NOV-2025'
  },
  {
    symbol: 'TCS',
    expiry: '28-NOV-2025',
    ltp: 4156.20,
    change: -23.45,
    changePercent: -0.56,
    openInterest: 345678,
    volume: 123456,
    basis: 6.20,
    lot_size: 150,
    margin_required: 87000,
    delivery_date: '28-NOV-2025'
  },
  {
    symbol: 'HDFCBANK',
    expiry: '28-NOV-2025',
    ltp: 1667.85,
    change: 13.00,
    changePercent: 0.79,
    openInterest: 890123,
    volume: 345678,
    basis: 13.00,
    lot_size: 550,
    margin_required: 125000,
    delivery_date: '28-NOV-2025'
  }
];

// Sample IPO Data
const IPO_DATA: IPOData[] = [
  {
    company_name: 'TechCorp Solutions Ltd',
    issue_size: '₹2,500 Cr',
    price_band: '₹320-350',
    open_date: '25-OCT-2025',
    close_date: '29-OCT-2025',
    listing_date: '05-NOV-2025',
    lot_size: 42,
    status: 'upcoming',
    subscription: 0,
    category: 'mainboard',
    sector: 'Information Technology',
    lead_managers: ['ICICI Securities', 'Kotak Mahindra Capital'],
    gmp: 45,
    estimated_listing_price: 395
  },
  {
    company_name: 'Green Energy Systems',
    issue_size: '₹1,800 Cr',
    price_band: '₹285-310',
    open_date: '22-OCT-2025',
    close_date: '24-OCT-2025',
    listing_date: '30-OCT-2025',
    lot_size: 48,
    status: 'open',
    subscription: 2.34,
    category: 'mainboard',
    sector: 'Renewable Energy',
    lead_managers: ['Axis Capital', 'SBI Capital Markets'],
    gmp: 28,
    estimated_listing_price: 338
  },
  {
    company_name: 'MediPharm Industries',
    issue_size: '₹950 Cr',
    price_band: '₹180-195',
    open_date: '15-OCT-2025',
    close_date: '17-OCT-2025',
    listing_date: '23-OCT-2025',
    lot_size: 76,
    status: 'closed',
    subscription: 12.45,
    category: 'mainboard',
    sector: 'Pharmaceuticals',
    lead_managers: ['Morgan Stanley', 'Goldman Sachs'],
    gmp: 67,
    estimated_listing_price: 262
  },
  {
    company_name: 'Smart Logistics Hub',
    issue_size: '₹45 Cr',
    price_band: '₹92-98',
    open_date: '28-OCT-2025',
    close_date: '30-OCT-2025',
    listing_date: '06-NOV-2025',
    lot_size: 150,
    status: 'upcoming',
    subscription: 0,
    category: 'sme',
    sector: 'Logistics',
    lead_managers: ['Hem Securities'],
    gmp: 12,
    estimated_listing_price: 110
  }
];

// Sample Portfolio Data
const SAMPLE_PORTFOLIO: DerivativesPortfolio[] = [
  {
    position_id: 'FUT001',
    symbol: 'NIFTY',
    type: 'futures',
    position_type: 'long',
    quantity: 50,
    entry_price: 25650.00,
    current_price: 25745.50,
    pnl: 4775.00,
    margin_used: 180000,
    expiry_date: '28-NOV-2025',
    days_to_expiry: 40
  },
  {
    position_id: 'OPT001',
    symbol: 'BANKNIFTY',
    type: 'options',
    position_type: 'short',
    quantity: 15,
    entry_price: 245.50,
    current_price: 189.75,
    pnl: 835.25,
    margin_used: 45000,
    expiry_date: '21-OCT-2025',
    days_to_expiry: 2
  },
  {
    position_id: 'FUT002',
    symbol: 'RELIANCE',
    type: 'futures',
    position_type: 'long',
    quantity: 250,
    entry_price: 1285.20,
    current_price: 1298.45,
    pnl: 3312.50,
    margin_used: 48000,
    expiry_date: '28-NOV-2025',
    days_to_expiry: 40
  }
];

export function DerivativesIPOHub() {
  const [activeTab, setActiveTab] = useState<'futures' | 'ipo' | 'portfolio'>('futures');
  const [selectedCategory, setSelectedCategory] = useState<'all' | 'mainboard' | 'sme'>('all');
  const [selectedStatus, setSelectedStatus] = useState<'all' | 'upcoming' | 'open' | 'closed'>('all');
  const [futuresData, setFuturesData] = useState<FuturesData[]>(FUTURES_DATA);
  const [ipoData, setIpoData] = useState<IPOData[]>(IPO_DATA);
  const [portfolioData] = useState<DerivativesPortfolio[]>(SAMPLE_PORTFOLIO);

  useEffect(() => {
    // Simulate real-time updates for futures data
    const interval = setInterval(() => {
      setFuturesData(prev => prev.map(item => ({
        ...item,
        ltp: item.ltp + (Math.random() - 0.5) * item.ltp * 0.002,
        change: item.change + (Math.random() - 0.5) * 10,
        volume: item.volume + Math.floor(Math.random() * 1000)
      })));
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const formatNumber = (num: number) => {
    if (num >= 10000000) return (num / 10000000).toFixed(1) + 'Cr';
    if (num >= 100000) return (num / 100000).toFixed(1) + 'L';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toFixed(0);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'upcoming': return 'text-blue-400 bg-blue-500/10';
      case 'open': return 'text-green-400 bg-green-500/10';
      case 'closed': return 'text-yellow-400 bg-yellow-500/10';
      case 'listed': return 'text-purple-400 bg-purple-500/10';
      default: return 'text-slate-400 bg-slate-500/10';
    }
  };

  const filteredIPOs = ipoData.filter(ipo => {
    if (selectedCategory !== 'all' && ipo.category !== selectedCategory) return false;
    if (selectedStatus !== 'all' && ipo.status !== selectedStatus) return false;
    return true;
  });

  const totalPortfolioPnL = portfolioData.reduce((sum, position) => sum + position.pnl, 0);
  const totalMarginUsed = portfolioData.reduce((sum, position) => sum + position.margin_used, 0);

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4">
      <div className="max-w-full mx-auto">
        {/* Navigation Breadcrumb */}
        <div className="mb-6">
          <nav className="flex items-center space-x-2 text-sm text-slate-400">
            <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
            <span>/</span>
            <Link href="/stocks" className="hover:text-blue-400 transition-colors">Stocks</Link>
            <span>/</span>
            <span className="text-white">Derivatives & IPO Hub</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
                Derivatives & IPO Trading Hub
              </h1>
              <p className="text-slate-400">
                Futures contracts, IPO applications, and derivatives portfolio management
              </p>
            </div>
            
            <div className="flex items-center gap-4">
              <button className="flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg transition-colors">
                <Download className="h-4 w-4 mr-2" />
                Export Data
              </button>
              <Link 
                href="/stocks/backtest"
                className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
              >
                <BarChart3 className="h-4 w-4 mr-2" />
                Backtest
              </Link>
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="flex space-x-1 bg-slate-800 rounded-lg p-1 mb-6">
            <button
              onClick={() => setActiveTab('futures')}
              className={`flex items-center px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                activeTab === 'futures' 
                  ? 'bg-blue-600 text-white' 
                  : 'text-slate-400 hover:text-white hover:bg-slate-700'
              }`}
            >
              <TrendingUp className="h-4 w-4 mr-2" />
              Futures
            </button>
            <button
              onClick={() => setActiveTab('ipo')}
              className={`flex items-center px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                activeTab === 'ipo' 
                  ? 'bg-purple-600 text-white' 
                  : 'text-slate-400 hover:text-white hover:bg-slate-700'
              }`}
            >
              <Building2 className="h-4 w-4 mr-2" />
              IPO Center
            </button>
            <button
              onClick={() => setActiveTab('portfolio')}
              className={`flex items-center px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                activeTab === 'portfolio' 
                  ? 'bg-green-600 text-white' 
                  : 'text-slate-400 hover:text-white hover:bg-slate-700'
              }`}
            >
              <Target className="h-4 w-4 mr-2" />
              Portfolio
            </button>
          </div>
        </div>

        {/* Futures Tab */}
        {activeTab === 'futures' && (
          <div className="space-y-6">
            {/* Futures Market Overview */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-slate-400">Total Volume</span>
                  <BarChart3 className="h-4 w-4 text-blue-400" />
                </div>
                <div className="text-xl font-bold text-white">
                  {formatNumber(futuresData.reduce((sum, item) => sum + item.volume, 0))}
                </div>
              </div>
              <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-slate-400">Total OI</span>
                  <Target className="h-4 w-4 text-green-400" />
                </div>
                <div className="text-xl font-bold text-white">
                  {formatNumber(futuresData.reduce((sum, item) => sum + item.openInterest, 0))}
                </div>
              </div>
              <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-slate-400">Avg Basis</span>
                  <DollarSign className="h-4 w-4 text-yellow-400" />
                </div>
                <div className="text-xl font-bold text-white">
                  {(futuresData.reduce((sum, item) => sum + item.basis, 0) / futuresData.length).toFixed(2)}
                </div>
              </div>
              <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-slate-400">Active Contracts</span>
                  <Clock className="h-4 w-4 text-purple-400" />
                </div>
                <div className="text-xl font-bold text-white">{futuresData.length}</div>
              </div>
            </div>

            {/* Futures Table */}
            <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden">
              <div className="p-4 border-b border-slate-800">
                <h2 className="text-xl font-bold text-white">NSE Futures Contracts</h2>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-slate-800">
                    <tr>
                      <th className="px-4 py-3 text-left">Symbol</th>
                      <th className="px-4 py-3 text-left">Expiry</th>
                      <th className="px-4 py-3 text-right">LTP</th>
                      <th className="px-4 py-3 text-right">Change</th>
                      <th className="px-4 py-3 text-right">Basis</th>
                      <th className="px-4 py-3 text-right">Volume</th>
                      <th className="px-4 py-3 text-right">OI</th>
                      <th className="px-4 py-3 text-right">Lot Size</th>
                      <th className="px-4 py-3 text-right">Margin</th>
                    </tr>
                  </thead>
                  <tbody>
                    {futuresData.map((future, index) => (
                      <tr key={index} className="border-t border-slate-800 hover:bg-slate-800/50">
                        <td className="px-4 py-3 font-medium text-white">{future.symbol}</td>
                        <td className="px-4 py-3 text-slate-300">{future.expiry}</td>
                        <td className="px-4 py-3 text-right font-mono text-white">
                          ₹{future.ltp.toFixed(2)}
                        </td>
                        <td className={`px-4 py-3 text-right font-mono ${
                          future.change >= 0 ? 'text-green-400' : 'text-red-400'
                        }`}>
                          {future.change >= 0 ? '+' : ''}{future.change.toFixed(2)} ({future.changePercent.toFixed(2)}%)
                        </td>
                        <td className="px-4 py-3 text-right font-mono text-yellow-400">
                          +{future.basis.toFixed(2)}
                        </td>
                        <td className="px-4 py-3 text-right font-mono text-slate-300">
                          {formatNumber(future.volume)}
                        </td>
                        <td className="px-4 py-3 text-right font-mono text-slate-300">
                          {formatNumber(future.openInterest)}
                        </td>
                        <td className="px-4 py-3 text-right font-mono text-blue-400">
                          {future.lot_size}
                        </td>
                        <td className="px-4 py-3 text-right font-mono text-purple-400">
                          ₹{formatNumber(future.margin_required)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* IPO Tab */}
        {activeTab === 'ipo' && (
          <div className="space-y-6">
            {/* IPO Filters */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 bg-slate-800 rounded-xl border border-slate-700">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Category</label>
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value as any)}
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                >
                  <option value="all">All Categories</option>
                  <option value="mainboard">Mainboard</option>
                  <option value="sme">SME</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Status</label>
                <select
                  value={selectedStatus}
                  onChange={(e) => setSelectedStatus(e.target.value as any)}
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                >
                  <option value="all">All Status</option>
                  <option value="upcoming">Upcoming</option>
                  <option value="open">Open</option>
                  <option value="closed">Closed</option>
                </select>
              </div>
              <div className="flex items-end">
                <div className="text-sm text-slate-400">
                  <div className="font-medium text-white">{filteredIPOs.length} IPOs</div>
                  <div>Available for application</div>
                </div>
              </div>
            </div>

            {/* IPO Cards */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {filteredIPOs.map((ipo, index) => (
                <div key={index} className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-lg font-bold text-white mb-1">{ipo.company_name}</h3>
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(ipo.status)}`}>
                          {ipo.status.toUpperCase()}
                        </span>
                        <span className="text-xs text-slate-400">{ipo.category.toUpperCase()}</span>
                      </div>
                    </div>
                    <Building2 className="h-6 w-6 text-blue-400" />
                  </div>

                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div>
                      <span className="text-xs text-slate-400">Issue Size</span>
                      <div className="font-semibold text-white">{ipo.issue_size}</div>
                    </div>
                    <div>
                      <span className="text-xs text-slate-400">Price Band</span>
                      <div className="font-semibold text-white">{ipo.price_band}</div>
                    </div>
                    <div>
                      <span className="text-xs text-slate-400">Lot Size</span>
                      <div className="font-semibold text-white">{ipo.lot_size} shares</div>
                    </div>
                    <div>
                      <span className="text-xs text-slate-400">Sector</span>
                      <div className="font-semibold text-white">{ipo.sector}</div>
                    </div>
                  </div>

                  <div className="space-y-2 mb-4">
                    <div className="flex justify-between text-sm">
                      <span className="text-slate-400">Open Date:</span>
                      <span className="text-white">{ipo.open_date}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-slate-400">Close Date:</span>
                      <span className="text-white">{ipo.close_date}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-slate-400">Listing Date:</span>
                      <span className="text-white">{ipo.listing_date}</span>
                    </div>
                  </div>

                  {ipo.status === 'open' && (
                    <div className="bg-green-500/10 rounded-lg p-3 mb-4">
                      <div className="flex justify-between items-center">
                        <span className="text-green-400 font-medium">Subscription: {ipo.subscription}x</span>
                        <Users className="h-4 w-4 text-green-400" />
                      </div>
                    </div>
                  )}

                  <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
                    <div>
                      <span className="text-slate-400">GMP:</span>
                      <span className="ml-2 font-semibold text-yellow-400">₹{ipo.gmp}</span>
                    </div>
                    <div>
                      <span className="text-slate-400">Est. Listing:</span>
                      <span className="ml-2 font-semibold text-green-400">₹{ipo.estimated_listing_price}</span>
                    </div>
                  </div>

                  <div className="mb-4">
                    <span className="text-xs text-slate-400">Lead Managers:</span>
                    <div className="text-sm text-white mt-1">{ipo.lead_managers.join(', ')}</div>
                  </div>

                  {(ipo.status === 'upcoming' || ipo.status === 'open') && (
                    <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
                      {ipo.status === 'upcoming' ? 'Set Reminder' : 'Apply Now'}
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Portfolio Tab */}
        {activeTab === 'portfolio' && (
          <div className="space-y-6">
            {/* Portfolio Summary */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-slate-400">Total P&L</span>
                  {totalPortfolioPnL >= 0 ? 
                    <TrendingUp className="h-4 w-4 text-green-400" /> : 
                    <TrendingDown className="h-4 w-4 text-red-400" />
                  }
                </div>
                <div className={`text-2xl font-bold ${totalPortfolioPnL >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                  ₹{totalPortfolioPnL.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                </div>
              </div>
              <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-slate-400">Margin Used</span>
                  <DollarSign className="h-4 w-4 text-blue-400" />
                </div>
                <div className="text-xl font-bold text-white">
                  ₹{totalMarginUsed.toLocaleString('en-IN')}
                </div>
              </div>
              <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-slate-400">Positions</span>
                  <Target className="h-4 w-4 text-purple-400" />
                </div>
                <div className="text-xl font-bold text-white">{portfolioData.length}</div>
              </div>
              <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-slate-400">Expiring Soon</span>
                  <AlertCircle className="h-4 w-4 text-yellow-400" />
                </div>
                <div className="text-xl font-bold text-white">
                  {portfolioData.filter(p => p.days_to_expiry <= 7).length}
                </div>
              </div>
            </div>

            {/* Portfolio Positions */}
            <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden">
              <div className="p-4 border-b border-slate-800">
                <h2 className="text-xl font-bold text-white">Active Positions</h2>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-slate-800">
                    <tr>
                      <th className="px-4 py-3 text-left">Symbol</th>
                      <th className="px-4 py-3 text-left">Type</th>
                      <th className="px-4 py-3 text-left">Position</th>
                      <th className="px-4 py-3 text-right">Quantity</th>
                      <th className="px-4 py-3 text-right">Entry Price</th>
                      <th className="px-4 py-3 text-right">Current Price</th>
                      <th className="px-4 py-3 text-right">P&L</th>
                      <th className="px-4 py-3 text-right">Margin</th>
                      <th className="px-4 py-3 text-center">Days to Expiry</th>
                    </tr>
                  </thead>
                  <tbody>
                    {portfolioData.map((position, index) => (
                      <tr key={index} className="border-t border-slate-800 hover:bg-slate-800/50">
                        <td className="px-4 py-3 font-medium text-white">{position.symbol}</td>
                        <td className="px-4 py-3">
                          <span className={`px-2 py-1 rounded text-xs font-medium ${
                            position.type === 'futures' 
                              ? 'text-blue-400 bg-blue-500/10' 
                              : 'text-purple-400 bg-purple-500/10'
                          }`}>
                            {position.type.toUpperCase()}
                          </span>
                        </td>
                        <td className="px-4 py-3">
                          <span className={`px-2 py-1 rounded text-xs font-medium ${
                            position.position_type === 'long' 
                              ? 'text-green-400 bg-green-500/10' 
                              : 'text-red-400 bg-red-500/10'
                          }`}>
                            {position.position_type.toUpperCase()}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-right font-mono text-white">{position.quantity}</td>
                        <td className="px-4 py-3 text-right font-mono text-slate-300">
                          ₹{position.entry_price.toFixed(2)}
                        </td>
                        <td className="px-4 py-3 text-right font-mono text-white">
                          ₹{position.current_price.toFixed(2)}
                        </td>
                        <td className={`px-4 py-3 text-right font-mono font-bold ${
                          position.pnl >= 0 ? 'text-green-400' : 'text-red-400'
                        }`}>
                          ₹{position.pnl.toFixed(2)}
                        </td>
                        <td className="px-4 py-3 text-right font-mono text-blue-400">
                          ₹{formatNumber(position.margin_used)}
                        </td>
                        <td className={`px-4 py-3 text-center font-mono ${
                          position.days_to_expiry <= 7 ? 'text-red-400 font-bold' : 'text-slate-300'
                        }`}>
                          {position.days_to_expiry}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}