'use client';

import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, TrendingDown, BarChart3, DollarSign, Target, Activity, 
  Crown, Zap, AlertCircle, CheckCircle, Eye, PlayCircle, Settings,
  Calendar, Clock, Bell, RefreshCw, ArrowUpRight, ArrowDownRight,
  PieChart, LineChart, Users, Building2, Coins, Filter, Download,
  Plus, Minus, MoreVertical, Edit, Trash2, Search, SortAsc, SortDesc,
  BarChart2, AreaChart, Percent, Calculator, Globe
} from 'lucide-react';
import Link from 'next/link';

interface PerformanceMetric {
  name: string;
  value: number;
  change: number;
  period: string;
  benchmark?: number;
  format: 'currency' | 'percentage' | 'number' | 'ratio';
}

interface RiskMetric {
  name: string;
  value: number;
  level: 'low' | 'medium' | 'high';
  description: string;
}

interface CorrelationData {
  asset1: string;
  asset2: string;
  correlation: number;
}

interface PerformanceAttribution {
  sector: string;
  allocation: number;
  return: number;
  contribution: number;
  benchmark: number;
}

interface TimeSeriesData {
  date: string;
  portfolio: number;
  benchmark: number;
  drawdown: number;
}

export function AdvancedAnalytics() {
  const [selectedTimeframe, setSelectedTimeframe] = useState<string>('1Y');
  const [selectedBenchmark, setSelectedBenchmark] = useState<string>('NIFTY50');
  const [activeTab, setActiveTab] = useState<string>('performance');

  const [performanceMetrics] = useState<PerformanceMetric[]>([
    { name: 'Total Return', value: 24.5, change: 2.3, period: '1Y', benchmark: 18.2, format: 'percentage' },
    { name: 'Annualized Return', value: 22.8, change: 1.8, period: '3Y', benchmark: 15.4, format: 'percentage' },
    { name: 'Sharpe Ratio', value: 1.45, change: 0.12, period: '1Y', benchmark: 1.08, format: 'ratio' },
    { name: 'Sortino Ratio', value: 1.89, change: 0.15, period: '1Y', benchmark: 1.31, format: 'ratio' },
    { name: 'Maximum Drawdown', value: -8.2, change: 1.1, period: '1Y', benchmark: -12.4, format: 'percentage' },
    { name: 'Beta', value: 0.92, change: -0.05, period: '1Y', benchmark: 1.0, format: 'ratio' },
    { name: 'Alpha', value: 5.8, change: 0.7, period: '1Y', benchmark: 0, format: 'percentage' },
    { name: 'Information Ratio', value: 0.73, change: 0.08, period: '1Y', format: 'ratio' }
  ]);

  const [riskMetrics] = useState<RiskMetric[]>([
    { name: 'Portfolio Volatility', value: 16.2, level: 'medium', description: 'Standard deviation of returns' },
    { name: 'Value at Risk (95%)', value: -2.3, level: 'low', description: 'Maximum expected loss in 1 day' },
    { name: 'Expected Shortfall', value: -3.1, level: 'low', description: 'Average loss beyond VaR' },
    { name: 'Tracking Error', value: 4.2, level: 'medium', description: 'Standard deviation vs benchmark' },
    { name: 'Maximum Leverage', value: 2.1, level: 'medium', description: 'Peak leverage used' },
    { name: 'Concentration Risk', value: 22.5, level: 'medium', description: 'Largest position percentage' }
  ]);

  const [correlationData] = useState<CorrelationData[]>([
    { asset1: 'Stocks', asset2: 'Bonds', correlation: -0.23 },
    { asset1: 'Stocks', asset2: 'Crypto', correlation: 0.45 },
    { asset1: 'Stocks', asset2: 'Gold', correlation: -0.15 },
    { asset1: 'Bonds', asset2: 'Crypto', correlation: -0.08 },
    { asset1: 'Bonds', asset2: 'Gold', correlation: 0.12 },
    { asset1: 'Crypto', asset2: 'Gold', correlation: 0.18 }
  ]);

  const [performanceAttribution] = useState<PerformanceAttribution[]>([
    { sector: 'Banking', allocation: 25.7, return: 28.5, contribution: 7.32, benchmark: 22.1 },
    { sector: 'Technology', allocation: 22.5, return: 31.2, contribution: 7.02, benchmark: 25.8 },
    { sector: 'Energy', allocation: 15.3, return: 18.9, contribution: 2.89, benchmark: 16.4 },
    { sector: 'Healthcare', allocation: 9.6, return: 22.1, contribution: 2.12, benchmark: 19.7 },
    { sector: 'Consumer', allocation: 7.6, return: 15.3, contribution: 1.16, benchmark: 13.8 },
    { sector: 'Others', allocation: 19.3, return: 20.4, contribution: 3.94, benchmark: 17.9 }
  ]);

  const formatValue = (value: number, format: string) => {
    switch (format) {
      case 'currency':
        return new Intl.NumberFormat('en-IN', {
          style: 'currency',
          currency: 'INR',
          minimumFractionDigits: 0,
          maximumFractionDigits: 0
        }).format(value);
      case 'percentage':
        return `${value >= 0 ? '+' : ''}${value.toFixed(1)}%`;
      case 'ratio':
        return value.toFixed(2);
      default:
        return value.toLocaleString();
    }
  };

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'low': return 'text-green-400 bg-green-500/10';
      case 'medium': return 'text-yellow-400 bg-yellow-500/10';
      case 'high': return 'text-red-400 bg-red-500/10';
      default: return 'text-slate-400 bg-slate-500/10';
    }
  };

  const getCorrelationColor = (correlation: number) => {
    if (correlation > 0.5) return 'text-red-400';
    if (correlation > 0.2) return 'text-yellow-400';
    if (correlation > -0.2) return 'text-slate-400';
    if (correlation > -0.5) return 'text-blue-400';
    return 'text-green-400';
  };

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
            <span className="text-white">Analytics</span>
          </nav>
        </div>

        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
              Advanced Analytics
            </h1>
            <p className="text-slate-400">
              Comprehensive portfolio performance attribution, risk analysis, and correlation insights
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            <select
              value={selectedTimeframe}
              onChange={(e) => setSelectedTimeframe(e.target.value)}
              className="px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
            >
              <option value="1M">1 Month</option>
              <option value="3M">3 Months</option>
              <option value="6M">6 Months</option>
              <option value="1Y">1 Year</option>
              <option value="3Y">3 Years</option>
              <option value="5Y">5 Years</option>
            </select>
            
            <select
              value={selectedBenchmark}
              onChange={(e) => setSelectedBenchmark(e.target.value)}
              className="px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
            >
              <option value="NIFTY50">NIFTY 50</option>
              <option value="SENSEX">SENSEX</option>
              <option value="NIFTY500">NIFTY 500</option>
              <option value="CUSTOM">Custom Index</option>
            </select>
            
            <button className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors">
              <Download className="h-4 w-4 mr-2" />
              Export Report
            </button>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex space-x-1 mb-8 bg-slate-900 rounded-xl p-1">
          {[
            { id: 'performance', name: 'Performance', icon: BarChart3 },
            { id: 'risk', name: 'Risk Analysis', icon: AlertCircle },
            { id: 'attribution', name: 'Attribution', icon: PieChart },
            { id: 'correlation', name: 'Correlation', icon: BarChart2 }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center px-6 py-3 rounded-lg font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              <tab.icon className="h-4 w-4 mr-2" />
              {tab.name}
            </button>
          ))}
        </div>

        {/* Performance Tab */}
        {activeTab === 'performance' && (
          <div className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {performanceMetrics.map((metric, index) => (
                <div key={index} className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-slate-400 text-sm font-medium">{metric.name}</h3>
                    <Calculator className="h-4 w-4 text-blue-400" />
                  </div>
                  
                  <div className="text-2xl font-bold text-white mb-2">
                    {formatValue(metric.value, metric.format)}
                  </div>
                  
                  <div className="flex items-center justify-between text-sm">
                    <div className={`flex items-center ${
                      metric.change >= 0 ? 'text-green-400' : 'text-red-400'
                    }`}>
                      {metric.change >= 0 ? (
                        <TrendingUp className="h-3 w-3 mr-1" />
                      ) : (
                        <TrendingDown className="h-3 w-3 mr-1" />
                      )}
                      {formatValue(Math.abs(metric.change), metric.format)}
                    </div>
                    
                    {metric.benchmark && (
                      <div className="text-slate-400">
                        vs {formatValue(metric.benchmark, metric.format)}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* Performance Chart Placeholder */}
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                <LineChart className="h-5 w-5 mr-2 text-blue-400" />
                Portfolio vs Benchmark Performance
              </h2>
              
              <div className="h-80 bg-slate-800 rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <AreaChart className="h-16 w-16 text-slate-600 mx-auto mb-4" />
                  <p className="text-slate-400">Performance chart will be displayed here</p>
                  <p className="text-slate-500 text-sm">Interactive time series visualization</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Risk Analysis Tab */}
        {activeTab === 'risk' && (
          <div className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {riskMetrics.map((metric, index) => (
                <div key={index} className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-white font-medium">{metric.name}</h3>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${getRiskColor(metric.level)}`}>
                      {metric.level}
                    </span>
                  </div>
                  
                  <div className="text-2xl font-bold text-white mb-2">
                    {metric.value >= 0 ? '' : ''}{metric.value.toFixed(1)}
                    {metric.name.includes('VaR') || metric.name.includes('Shortfall') ? '%' : 
                     metric.name.includes('Ratio') || metric.name.includes('Leverage') ? '' : '%'}
                  </div>
                  
                  <p className="text-slate-400 text-sm">{metric.description}</p>
                </div>
              ))}
            </div>

            {/* Risk Chart Placeholder */}
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                <BarChart3 className="h-5 w-5 mr-2 text-red-400" />
                Risk Decomposition
              </h2>
              
              <div className="h-80 bg-slate-800 rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <AlertCircle className="h-16 w-16 text-slate-600 mx-auto mb-4" />
                  <p className="text-slate-400">Risk breakdown chart will be displayed here</p>
                  <p className="text-slate-500 text-sm">VaR, stress testing, and scenario analysis</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Attribution Tab */}
        {activeTab === 'attribution' && (
          <div className="space-y-8">
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                <Target className="h-5 w-5 mr-2 text-green-400" />
                Sector Performance Attribution
              </h2>
              
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-slate-800">
                    <tr>
                      <th className="px-4 py-3 text-left">Sector</th>
                      <th className="px-4 py-3 text-right">Allocation</th>
                      <th className="px-4 py-3 text-right">Return</th>
                      <th className="px-4 py-3 text-right">Contribution</th>
                      <th className="px-4 py-3 text-right">Benchmark</th>
                      <th className="px-4 py-3 text-right">Excess Return</th>
                    </tr>
                  </thead>
                  <tbody>
                    {performanceAttribution.map((sector, index) => (
                      <tr key={index} className="border-t border-slate-800 hover:bg-slate-800/50">
                        <td className="px-4 py-3 font-medium text-white">{sector.sector}</td>
                        <td className="px-4 py-3 text-right font-mono text-blue-400">
                          {sector.allocation.toFixed(1)}%
                        </td>
                        <td className={`px-4 py-3 text-right font-mono ${
                          sector.return >= 0 ? 'text-green-400' : 'text-red-400'
                        }`}>
                          {sector.return >= 0 ? '+' : ''}{sector.return.toFixed(1)}%
                        </td>
                        <td className="px-4 py-3 text-right font-mono text-white">
                          +{sector.contribution.toFixed(2)}%
                        </td>
                        <td className="px-4 py-3 text-right font-mono text-slate-400">
                          {sector.benchmark.toFixed(1)}%
                        </td>
                        <td className={`px-4 py-3 text-right font-mono ${
                          (sector.return - sector.benchmark) >= 0 ? 'text-green-400' : 'text-red-400'
                        }`}>
                          {(sector.return - sector.benchmark) >= 0 ? '+' : ''}
                          {(sector.return - sector.benchmark).toFixed(1)}%
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Attribution Chart Placeholder */}
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                <PieChart className="h-5 w-5 mr-2 text-purple-400" />
                Attribution Breakdown
              </h2>
              
              <div className="h-80 bg-slate-800 rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <PieChart className="h-16 w-16 text-slate-600 mx-auto mb-4" />
                  <p className="text-slate-400">Attribution visualization will be displayed here</p>
                  <p className="text-slate-500 text-sm">Asset allocation and selection effects</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Correlation Tab */}
        {activeTab === 'correlation' && (
          <div className="space-y-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                  <Globe className="h-5 w-5 mr-2 text-yellow-400" />
                  Asset Correlation Matrix
                </h2>
                
                <div className="space-y-4">
                  {correlationData.map((corr, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-slate-800 rounded-lg">
                      <div className="text-white font-medium">
                        {corr.asset1} ↔ {corr.asset2}
                      </div>
                      <div className={`font-mono font-bold ${getCorrelationColor(corr.correlation)}`}>
                        {corr.correlation >= 0 ? '+' : ''}{corr.correlation.toFixed(2)}
                      </div>
                    </div>
                  ))}
                </div>
                
                <div className="mt-6 p-4 bg-slate-800 rounded-lg">
                  <h3 className="text-white font-medium mb-2">Correlation Guide</h3>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div className="flex items-center">
                      <div className="w-3 h-3 bg-green-500 rounded mr-2"></div>
                      <span className="text-slate-400">Strong Negative (-0.5 to -1.0)</span>
                    </div>
                    <div className="flex items-center">
                      <div className="w-3 h-3 bg-blue-500 rounded mr-2"></div>
                      <span className="text-slate-400">Weak Negative (-0.2 to -0.5)</span>
                    </div>
                    <div className="flex items-center">
                      <div className="w-3 h-3 bg-slate-500 rounded mr-2"></div>
                      <span className="text-slate-400">No Correlation (-0.2 to 0.2)</span>
                    </div>
                    <div className="flex items-center">
                      <div className="w-3 h-3 bg-yellow-500 rounded mr-2"></div>
                      <span className="text-slate-400">Weak Positive (0.2 to 0.5)</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                  <BarChart2 className="h-5 w-5 mr-2 text-blue-400" />
                  Correlation Heatmap
                </h2>
                
                <div className="h-80 bg-slate-800 rounded-lg flex items-center justify-center">
                  <div className="text-center">
                    <BarChart2 className="h-16 w-16 text-slate-600 mx-auto mb-4" />
                    <p className="text-slate-400">Correlation heatmap will be displayed here</p>
                    <p className="text-slate-500 text-sm">Interactive correlation matrix visualization</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}