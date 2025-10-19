'use client';

import React from 'react';
import Link from 'next/link';
import { BarChart3, TrendingUp, Target, Database, Eye, Calendar, Activity } from 'lucide-react';

export default function IndianStocksPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-white p-4">
      <div className="max-w-7xl mx-auto">
        {/* Navigation Breadcrumb */}
        <div className="mb-6">
          <nav className="flex items-center space-x-2 text-sm text-slate-400">
            <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
            <span>/</span>
            <span className="text-white">Stocks</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-4">
            NSE Stock Options & Analytics
          </h1>
          <p className="text-xl text-slate-300 mb-6">
            Professional option chain analysis with real-time data, Greeks, and advanced strategies
          </p>
        </div>

        {/* Option Chain Variants */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <Link 
            href="/stocks/option-chain"
            className="group bg-slate-900 rounded-2xl p-6 border border-slate-800 hover:border-blue-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/10"
          >
            <div className="flex items-center justify-between mb-4">
              <Eye className="h-8 w-8 text-blue-400" />
              <span className="text-xs text-slate-400 bg-slate-800 px-2 py-1 rounded">Classic</span>
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Standard Option Chain</h3>
            <p className="text-slate-400 mb-4">
              Traditional option chain view with essential data points and easy navigation
            </p>
            <div className="text-sm text-blue-400 font-medium group-hover:text-blue-300">
              25+ symbols • Real-time updates →
            </div>
          </Link>

          <Link 
            href="/stocks/option-chain/complete"
            className="group bg-slate-900 rounded-2xl p-6 border border-slate-800 hover:border-purple-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/10"
          >
            <div className="flex items-center justify-between mb-4">
              <Database className="h-8 w-8 text-purple-400" />
              <span className="text-xs text-slate-400 bg-purple-900/30 px-2 py-1 rounded">Complete</span>
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Comprehensive Data</h3>
            <p className="text-slate-400 mb-4">
              All columns: OI, Volume, IV, LTP, Greeks, Bid/Ask spreads with Monday expiries
            </p>
            <div className="text-sm text-purple-400 font-medium group-hover:text-purple-300">
              Full data set • NSE 2025 changes →
            </div>
          </Link>

          <Link 
            href="/stocks/derivatives"
            className="group bg-slate-900 rounded-2xl p-6 border border-slate-800 hover:border-orange-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-orange-500/10"
          >
            <div className="flex items-center justify-between mb-4">
              <TrendingUp className="h-8 w-8 text-orange-400" />
              <span className="text-xs text-slate-400 bg-orange-900/30 px-2 py-1 rounded">New</span>
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Derivatives & IPO Hub</h3>
            <p className="text-slate-400 mb-4">
              Futures contracts, IPO applications, and derivatives portfolio management
            </p>
            <div className="text-sm text-orange-400 font-medium group-hover:text-orange-300">
              Futures • IPO Center • Portfolio →
            </div>
          </Link>

          <Link 
            href="/stocks/backtest"
            className="group bg-slate-900 rounded-2xl p-6 border border-slate-800 hover:border-green-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-green-500/10"
          >
            <div className="flex items-center justify-between mb-4">
              <BarChart3 className="h-8 w-8 text-green-400" />
              <span className="text-xs text-slate-400 bg-green-900/30 px-2 py-1 rounded">Strategy</span>
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Option Backtesting</h3>
            <p className="text-slate-400 mb-4">
              Test option strategies with historical data and performance metrics
            </p>
            <div className="text-sm text-green-400 font-medium group-hover:text-green-300">
              Multiple strategies • Risk analysis →
            </div>
          </Link>

          <Link 
            href="/stocks/backtest/multi-strategy"
            className="group bg-slate-900 rounded-2xl p-6 border border-slate-800 hover:border-cyan-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-cyan-500/10"
          >
            <div className="flex items-center justify-between mb-4">
              <Target className="h-8 w-8 text-cyan-400" />
              <span className="text-xs text-slate-400 bg-cyan-900/30 px-2 py-1 rounded">Advanced</span>
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Multi-Strategy Compare</h3>
            <p className="text-slate-400 mb-4">
              Compare multiple option strategies side-by-side with performance analytics
            </p>
            <div className="text-sm text-cyan-400 font-medium group-hover:text-cyan-300">
              Parallel testing • Performance charts →
            </div>
          </Link>

          <div className="group bg-slate-900 rounded-2xl p-6 border border-slate-800 hover:border-yellow-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-yellow-500/10 opacity-75">
            <div className="flex items-center justify-between mb-4">
              <Activity className="h-8 w-8 text-yellow-400" />
              <span className="text-xs text-slate-400 bg-yellow-900/30 px-2 py-1 rounded">Coming Soon</span>
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Advanced Analytics</h3>
            <p className="text-slate-400 mb-4">
              Option flow analysis, unusual activity detection, and volatility surface
            </p>
            <div className="text-sm text-yellow-400 font-medium">
              Flow analysis • Volatility surface →
            </div>
          </div>
        </div>

        {/* Feature Highlights */}
        <div className="bg-slate-900 rounded-2xl p-8 border border-slate-800 mb-8">
          <h2 className="text-2xl font-bold text-white mb-6">Platform Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="text-center">
              <Target className="h-12 w-12 text-yellow-400 mx-auto mb-3" />
              <h3 className="font-semibold text-white mb-2">ATM Detection</h3>
              <p className="text-sm text-slate-400">Automatic at-the-money strike identification</p>
            </div>
            <div className="text-center">
              <TrendingUp className="h-12 w-12 text-green-400 mx-auto mb-3" />
              <h3 className="font-semibold text-white mb-2">Live Data</h3>
              <p className="text-sm text-slate-400">Real-time option prices and analytics</p>
            </div>
            <div className="text-center">
              <Calendar className="h-12 w-12 text-blue-400 mx-auto mb-3" />
              <h3 className="font-semibold text-white mb-2">Monday Expiries</h3>
              <p className="text-sm text-slate-400">Updated NSE expiry calendar (April 2025)</p>
            </div>
            <div className="text-center">
              <BarChart3 className="h-12 w-12 text-purple-400 mx-auto mb-3" />
              <h3 className="font-semibold text-white mb-2">Greeks & Analytics</h3>
              <p className="text-sm text-slate-400">Delta, Gamma, Theta, Vega calculations</p>
            </div>
          </div>
        </div>

        {/* Quick Access Market Overview */}
        <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
          <h2 className="text-xl font-bold text-white mb-4">Market Overview</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="bg-slate-800 rounded-lg p-4">
              <div className="flex justify-between items-center">
                <span className="text-slate-400">NIFTY 50</span>
                <span className="text-green-400">+0.56%</span>
              </div>
              <div className="text-2xl font-bold text-white mt-1">25,709.85</div>
              <div className="text-xs text-slate-400 mt-1">Monday expiries active</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-4">
              <div className="flex justify-between items-center">
                <span className="text-slate-400">BANKNIFTY</span>
                <span className="text-red-400">-0.43%</span>
              </div>
              <div className="text-2xl font-bold text-white mt-1">54,789.25</div>
              <div className="text-xs text-slate-400 mt-1">Weekly + Monthly</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-4">
              <div className="flex justify-between items-center">
                <span className="text-slate-400">India VIX</span>
                <span className="text-yellow-400">14.85</span>
              </div>
              <div className="text-lg font-bold text-white mt-1">Low Volatility</div>
              <div className="text-xs text-slate-400 mt-1">Favorable for strategies</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}