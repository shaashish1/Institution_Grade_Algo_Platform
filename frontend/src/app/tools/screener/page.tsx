'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Search, Filter, TrendingUp, TrendingDown, Eye, BarChart3, Target, DollarSign, Percent, Volume, Clock } from 'lucide-react';

interface StockData {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
  marketCap: number;
  pe: number;
  sector: string;
  iv: number;
  optionVolume: number;
  putCallRatio: number;
}

interface ScreenerFilters {
  priceMin: number;
  priceMax: number;
  changeMin: number;
  changeMax: number;
  volumeMin: number;
  sector: string;
  ivMin: number;
  ivMax: number;
  optionVolumeMin: number;
  putCallRatioMin: number;
  putCallRatioMax: number;
}

const sampleStocks: StockData[] = [
  {
    symbol: 'RELIANCE',
    name: 'Reliance Industries',
    price: 2789.45,
    change: 45.20,
    changePercent: 1.65,
    volume: 2345678,
    marketCap: 1887000,
    pe: 24.5,
    sector: 'Energy',
    iv: 18.5,
    optionVolume: 125000,
    putCallRatio: 0.85
  },
  {
    symbol: 'TCS',
    name: 'Tata Consultancy Services',
    price: 4123.30,
    change: -28.75,
    changePercent: -0.69,
    volume: 1876543,
    marketCap: 1505000,
    pe: 28.2,
    sector: 'IT',
    iv: 22.3,
    optionVolume: 98000,
    putCallRatio: 1.15
  },
  {
    symbol: 'HDFCBANK',
    name: 'HDFC Bank',
    price: 1678.90,
    change: 23.45,
    changePercent: 1.42,
    volume: 3456789,
    marketCap: 1245000,
    pe: 19.8,
    sector: 'Banking',
    iv: 16.7,
    optionVolume: 187000,
    putCallRatio: 0.92
  },
  {
    symbol: 'INFY',
    name: 'Infosys',
    price: 1789.25,
    change: 12.80,
    changePercent: 0.72,
    volume: 2987654,
    marketCap: 756000,
    pe: 26.4,
    sector: 'IT',
    iv: 21.8,
    optionVolume: 76000,
    putCallRatio: 1.08
  },
  {
    symbol: 'ICICIBANK',
    name: 'ICICI Bank',
    price: 1234.56,
    change: -15.60,
    changePercent: -1.25,
    volume: 4567890,
    marketCap: 865000,
    pe: 15.3,
    sector: 'Banking',
    iv: 19.2,
    optionVolume: 145000,
    putCallRatio: 1.22
  },
  {
    symbol: 'SBIN',
    name: 'State Bank of India',
    price: 789.30,
    change: 18.75,
    changePercent: 2.43,
    volume: 6789012,
    marketCap: 705000,
    pe: 12.7,
    sector: 'Banking',
    iv: 25.4,
    optionVolume: 234000,
    putCallRatio: 0.78
  },
  {
    symbol: 'BHARTIARTL',
    name: 'Bharti Airtel',
    price: 1456.78,
    change: 34.20,
    changePercent: 2.40,
    volume: 3456789,
    marketCap: 823000,
    pe: 18.9,
    sector: 'Telecom',
    iv: 28.6,
    optionVolume: 89000,
    putCallRatio: 0.95
  },
  {
    symbol: 'ITC',
    name: 'ITC Limited',
    price: 456.90,
    change: -3.25,
    changePercent: -0.71,
    volume: 5678901,
    marketCap: 568000,
    pe: 22.1,
    sector: 'FMCG',
    iv: 15.8,
    optionVolume: 67000,
    putCallRatio: 1.05
  }
];

const sectors = ['All', 'Banking', 'IT', 'Energy', 'Telecom', 'FMCG', 'Auto', 'Pharma', 'Metals'];

const presetFilters = [
  {
    name: 'High IV Stocks',
    description: 'Stocks with high implied volatility (>25%)',
    filters: { ivMin: 25, ivMax: 100 }
  },
  {
    name: 'High Option Activity',
    description: 'Stocks with high option trading volume',
    filters: { optionVolumeMin: 100000 }
  },
  {
    name: 'Bearish Sentiment',
    description: 'Put/Call ratio > 1.2 (bearish)',
    filters: { putCallRatioMin: 1.2, putCallRatioMax: 5 }
  },
  {
    name: 'Bullish Momentum',
    description: 'Price change > 2% with high volume',
    filters: { changeMin: 2, volumeMin: 3000000 }
  },
  {
    name: 'Value Picks',
    description: 'Low PE ratio stocks',
    filters: { priceMax: 2000 }
  }
];

export default function StockScreener() {
  const [selectedTab, setSelectedTab] = useState<'stocks' | 'options'>('stocks');
  const [filters, setFilters] = useState<ScreenerFilters>({
    priceMin: 0,
    priceMax: 10000,
    changeMin: -10,
    changeMax: 10,
    volumeMin: 0,
    sector: 'All',
    ivMin: 0,
    ivMax: 100,
    optionVolumeMin: 0,
    putCallRatioMin: 0,
    putCallRatioMax: 5
  });
  const [filteredStocks, setFilteredStocks] = useState<StockData[]>(sampleStocks);
  const [searchTerm, setSearchTerm] = useState('');

  const applyFilters = () => {
    let filtered = sampleStocks.filter(stock => {
      const matchesSearch = stock.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           stock.name.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesPrice = stock.price >= filters.priceMin && stock.price <= filters.priceMax;
      const matchesChange = stock.changePercent >= filters.changeMin && stock.changePercent <= filters.changeMax;
      const matchesVolume = stock.volume >= filters.volumeMin;
      const matchesSector = filters.sector === 'All' || stock.sector === filters.sector;
      const matchesIV = stock.iv >= filters.ivMin && stock.iv <= filters.ivMax;
      const matchesOptionVolume = stock.optionVolume >= filters.optionVolumeMin;
      const matchesPCR = stock.putCallRatio >= filters.putCallRatioMin && stock.putCallRatio <= filters.putCallRatioMax;

      return matchesSearch && matchesPrice && matchesChange && matchesVolume && 
             matchesSector && matchesIV && matchesOptionVolume && matchesPCR;
    });

    setFilteredStocks(filtered);
  };

  const applyPresetFilter = (preset: any) => {
    setFilters(prev => ({ ...prev, ...preset.filters }));
  };

  const resetFilters = () => {
    setFilters({
      priceMin: 0,
      priceMax: 10000,
      changeMin: -10,
      changeMax: 10,
      volumeMin: 0,
      sector: 'All',
      ivMin: 0,
      ivMax: 100,
      optionVolumeMin: 0,
      putCallRatioMin: 0,
      putCallRatioMax: 5
    });
    setSearchTerm('');
  };

  useEffect(() => {
    applyFilters();
  }, [filters, searchTerm]);

  const formatNumber = (num: number): string => {
    if (num >= 100000) return (num / 100000).toFixed(1) + 'L';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toFixed(0);
  };

  const formatMarketCap = (num: number): string => {
    if (num >= 100000) return (num / 100000).toFixed(1) + 'L Cr';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K Cr';
    return num.toFixed(0) + ' Cr';
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
            <span className="text-white">Stock Screener</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-4">
            <Search className="h-8 w-8 text-blue-400" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              Stock & Option Screener
            </h1>
          </div>
          <p className="text-xl text-slate-300">
            Find stocks and options with custom filters and technical criteria
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6">
          <div className="flex space-x-1 bg-slate-900 p-1 rounded-lg w-fit">
            <button
              onClick={() => setSelectedTab('stocks')}
              className={`px-6 py-2 rounded-md font-medium transition-colors ${
                selectedTab === 'stocks'
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Stock Screener
            </button>
            <button
              onClick={() => setSelectedTab('options')}
              className={`px-6 py-2 rounded-md font-medium transition-colors ${
                selectedTab === 'options'
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Option Activity
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-4 gap-6">
          {/* Filters Sidebar */}
          <div className="xl:col-span-1">
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800 sticky top-4">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-white flex items-center">
                  <Filter className="h-5 w-5 mr-2 text-purple-400" />
                  Filters
                </h2>
                <button
                  onClick={resetFilters}
                  className="text-sm text-slate-400 hover:text-white transition-colors"
                >
                  Reset
                </button>
              </div>

              {/* Search */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-slate-300 mb-2">Search Symbol</label>
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="RELIANCE, TCS..."
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white placeholder-slate-400 focus:border-blue-500 focus:outline-none"
                />
              </div>

              {/* Preset Filters */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-slate-300 mb-3">Quick Filters</label>
                <div className="space-y-2">
                  {presetFilters.map((preset, index) => (
                    <button
                      key={index}
                      onClick={() => applyPresetFilter(preset)}
                      className="w-full text-left p-3 bg-slate-800 hover:bg-slate-700 rounded-lg border border-slate-700 transition-colors"
                    >
                      <div className="font-medium text-sm text-white">{preset.name}</div>
                      <div className="text-xs text-slate-400 mt-1">{preset.description}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Price Range */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-slate-300 mb-2">Price Range (₹)</label>
                <div className="grid grid-cols-2 gap-2">
                  <input
                    type="number"
                    value={filters.priceMin}
                    onChange={(e) => setFilters(prev => ({ ...prev, priceMin: Number(e.target.value) }))}
                    placeholder="Min"
                    className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                  />
                  <input
                    type="number"
                    value={filters.priceMax}
                    onChange={(e) => setFilters(prev => ({ ...prev, priceMax: Number(e.target.value) }))}
                    placeholder="Max"
                    className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                  />
                </div>
              </div>

              {/* Change % Range */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-slate-300 mb-2">Change % Range</label>
                <div className="grid grid-cols-2 gap-2">
                  <input
                    type="number"
                    value={filters.changeMin}
                    onChange={(e) => setFilters(prev => ({ ...prev, changeMin: Number(e.target.value) }))}
                    placeholder="Min %"
                    className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                  />
                  <input
                    type="number"
                    value={filters.changeMax}
                    onChange={(e) => setFilters(prev => ({ ...prev, changeMax: Number(e.target.value) }))}
                    placeholder="Max %"
                    className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                  />
                </div>
              </div>

              {/* Sector */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-slate-300 mb-2">Sector</label>
                <select
                  value={filters.sector}
                  onChange={(e) => setFilters(prev => ({ ...prev, sector: e.target.value }))}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                >
                  {sectors.map(sector => (
                    <option key={sector} value={sector}>{sector}</option>
                  ))}
                </select>
              </div>

              {/* Option-specific filters */}
              {selectedTab === 'options' && (
                <>
                  <div className="mb-6">
                    <label className="block text-sm font-medium text-slate-300 mb-2">Implied Volatility % Range</label>
                    <div className="grid grid-cols-2 gap-2">
                      <input
                        type="number"
                        value={filters.ivMin}
                        onChange={(e) => setFilters(prev => ({ ...prev, ivMin: Number(e.target.value) }))}
                        placeholder="Min IV%"
                        className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                      />
                      <input
                        type="number"
                        value={filters.ivMax}
                        onChange={(e) => setFilters(prev => ({ ...prev, ivMax: Number(e.target.value) }))}
                        placeholder="Max IV%"
                        className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                      />
                    </div>
                  </div>

                  <div className="mb-6">
                    <label className="block text-sm font-medium text-slate-300 mb-2">Option Volume (Min)</label>
                    <input
                      type="number"
                      value={filters.optionVolumeMin}
                      onChange={(e) => setFilters(prev => ({ ...prev, optionVolumeMin: Number(e.target.value) }))}
                      placeholder="Min volume"
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                    />
                  </div>

                  <div className="mb-6">
                    <label className="block text-sm font-medium text-slate-300 mb-2">Put/Call Ratio Range</label>
                    <div className="grid grid-cols-2 gap-2">
                      <input
                        type="number"
                        step="0.1"
                        value={filters.putCallRatioMin}
                        onChange={(e) => setFilters(prev => ({ ...prev, putCallRatioMin: Number(e.target.value) }))}
                        placeholder="Min"
                        className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                      />
                      <input
                        type="number"
                        step="0.1"
                        value={filters.putCallRatioMax}
                        onChange={(e) => setFilters(prev => ({ ...prev, putCallRatioMax: Number(e.target.value) }))}
                        placeholder="Max"
                        className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                      />
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>

          {/* Results */}
          <div className="xl:col-span-3">
            <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden">
              {/* Results Header */}
              <div className="p-6 border-b border-slate-800">
                <div className="flex justify-between items-center">
                  <h2 className="text-xl font-bold text-white">
                    {selectedTab === 'stocks' ? 'Stock Results' : 'Option Activity Results'}
                  </h2>
                  <div className="text-sm text-slate-400">
                    {filteredStocks.length} stocks found
                  </div>
                </div>
              </div>

              {/* Results Table */}
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-slate-800">
                    <tr className="text-xs text-slate-300">
                      <th className="px-4 py-3 text-left">Symbol</th>
                      <th className="px-4 py-3 text-right">Price</th>
                      <th className="px-4 py-3 text-right">Change %</th>
                      <th className="px-4 py-3 text-right">Volume</th>
                      <th className="px-4 py-3 text-right">Market Cap</th>
                      {selectedTab === 'options' && (
                        <>
                          <th className="px-4 py-3 text-right">IV %</th>
                          <th className="px-4 py-3 text-right">Opt Volume</th>
                          <th className="px-4 py-3 text-right">P/C Ratio</th>
                        </>
                      )}
                      <th className="px-4 py-3 text-center">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredStocks.map((stock, index) => (
                      <tr key={index} className="border-t border-slate-800 hover:bg-slate-800/50">
                        <td className="px-4 py-4">
                          <div>
                            <div className="font-medium text-white">{stock.symbol}</div>
                            <div className="text-xs text-slate-400">{stock.name}</div>
                            <div className="text-xs text-blue-400">{stock.sector}</div>
                          </div>
                        </td>
                        <td className="px-4 py-4 text-right">
                          <div className="font-mono text-white">₹{stock.price.toFixed(2)}</div>
                        </td>
                        <td className="px-4 py-4 text-right">
                          <div className={`font-mono ${stock.change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                            {stock.change >= 0 ? '+' : ''}{stock.changePercent.toFixed(2)}%
                          </div>
                        </td>
                        <td className="px-4 py-4 text-right">
                          <div className="font-mono text-slate-300">{formatNumber(stock.volume)}</div>
                        </td>
                        <td className="px-4 py-4 text-right">
                          <div className="font-mono text-slate-300">{formatMarketCap(stock.marketCap)}</div>
                        </td>
                        {selectedTab === 'options' && (
                          <>
                            <td className="px-4 py-4 text-right">
                              <div className="font-mono text-purple-400">{stock.iv.toFixed(1)}%</div>
                            </td>
                            <td className="px-4 py-4 text-right">
                              <div className="font-mono text-cyan-400">{formatNumber(stock.optionVolume)}</div>
                            </td>
                            <td className="px-4 py-4 text-right">
                              <div className={`font-mono ${
                                stock.putCallRatio > 1.2 ? 'text-red-400' : 
                                stock.putCallRatio < 0.8 ? 'text-green-400' : 'text-yellow-400'
                              }`}>
                                {stock.putCallRatio.toFixed(2)}
                              </div>
                            </td>
                          </>
                        )}
                        <td className="px-4 py-4 text-center">
                          <Link
                            href={`/stocks/option-chain?symbol=${stock.symbol}`}
                            className="inline-flex items-center px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-xs text-white transition-colors"
                          >
                            <Eye className="h-3 w-3 mr-1" />
                            View
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {filteredStocks.length === 0 && (
                <div className="p-12 text-center">
                  <Search className="h-12 w-12 text-slate-600 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-slate-400 mb-2">No stocks found</h3>
                  <p className="text-slate-500">Try adjusting your filter criteria</p>
                </div>
              )}
            </div>

            {/* Quick Actions */}
            <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
              <Link
                href="/stocks/option-chain"
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-blue-500 transition-colors group"
              >
                <div className="flex items-center justify-between mb-2">
                  <Target className="h-6 w-6 text-blue-400" />
                  <div className="text-xs text-slate-400">Trading</div>
                </div>
                <h3 className="font-semibold text-white group-hover:text-blue-400 transition-colors">
                  Option Chain
                </h3>
                <p className="text-sm text-slate-400 mt-1">
                  View detailed option data
                </p>
              </Link>

              <Link
                href="/tools/calculator"
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-green-500 transition-colors group"
              >
                <div className="flex items-center justify-between mb-2">
                  <DollarSign className="h-6 w-6 text-green-400" />
                  <div className="text-xs text-slate-400">Tools</div>
                </div>
                <h3 className="font-semibold text-white group-hover:text-green-400 transition-colors">
                  Position Calculator
                </h3>
                <p className="text-sm text-slate-400 mt-1">
                  Calculate profit/loss
                </p>
              </Link>

              <Link
                href="/stocks/backtest"
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-purple-500 transition-colors group"
              >
                <div className="flex items-center justify-between mb-2">
                  <BarChart3 className="h-6 w-6 text-purple-400" />
                  <div className="text-xs text-slate-400">Analysis</div>
                </div>
                <h3 className="font-semibold text-white group-hover:text-purple-400 transition-colors">
                  Backtesting
                </h3>
                <p className="text-sm text-slate-400 mt-1">
                  Test strategies
                </p>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}