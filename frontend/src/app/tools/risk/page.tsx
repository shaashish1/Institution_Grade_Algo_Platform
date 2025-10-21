'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Shield, TrendingDown, AlertTriangle, PieChart, BarChart3, DollarSign, Percent, Target, Activity } from 'lucide-react';

interface Position {
  id: string;
  symbol: string;
  type: 'stock' | 'option';
  side: 'long' | 'short';
  quantity: number;
  entryPrice: number;
  currentPrice: number;
  pnl: number;
  pnlPercent: number;
  exposure: number;
  risk: number;
  sector: string;
}

interface RiskMetrics {
  portfolioValue: number;
  totalPnL: number;
  totalPnLPercent: number;
  maxDrawdown: number;
  dailyVaR: number;
  sharpeRatio: number;
  maxRisk: number;
  usedMargin: number;
  availableMargin: number;
  concentrationRisk: number;
}

interface RiskSettings {
  maxPositionSize: number;
  maxPortfolioRisk: number;
  maxDrawdown: number;
  maxSectorExposure: number;
  stopLossPercent: number;
  riskRewardRatio: number;
}

const samplePositions: Position[] = [
  {
    id: '1',
    symbol: 'NIFTY 26000 CE',
    type: 'option',
    side: 'long',
    quantity: 100,
    entryPrice: 150,
    currentPrice: 175,
    pnl: 2500,
    pnlPercent: 16.67,
    exposure: 17500,
    risk: 15000,
    sector: 'Index'
  },
  {
    id: '2',
    symbol: 'RELIANCE',
    type: 'stock',
    side: 'long',
    quantity: 50,
    entryPrice: 2750,
    currentPrice: 2789,
    pnl: 1950,
    pnlPercent: 1.42,
    exposure: 139450,
    risk: 6972,
    sector: 'Energy'
  },
  {
    id: '3',
    symbol: 'BANKNIFTY 55000 PE',
    type: 'option',
    side: 'short',
    quantity: 75,
    entryPrice: 200,
    currentPrice: 180,
    pnl: 1500,
    pnlPercent: 10.0,
    exposure: -13500,
    risk: 20000,
    sector: 'Index'
  },
  {
    id: '4',
    symbol: 'TCS',
    type: 'stock',
    side: 'long',
    quantity: 25,
    entryPrice: 4100,
    currentPrice: 4123,
    pnl: 575,
    pnlPercent: 0.56,
    exposure: 103075,
    risk: 5154,
    sector: 'IT'
  }
];

const defaultRiskSettings: RiskSettings = {
  maxPositionSize: 10, // % of portfolio
  maxPortfolioRisk: 5, // % of portfolio
  maxDrawdown: 15, // %
  maxSectorExposure: 25, // % of portfolio
  stopLossPercent: 5, // %
  riskRewardRatio: 2 // 1:2 risk:reward
};

export default function RiskManager() {
  const [positions, setPositions] = useState<Position[]>(samplePositions);
  const [riskSettings, setRiskSettings] = useState<RiskSettings>(defaultRiskSettings);
  const [selectedView, setSelectedView] = useState<'overview' | 'positions' | 'settings'>('overview');

  const calculateRiskMetrics = (): RiskMetrics => {
    const portfolioValue = 500000; // Mock portfolio value
    const totalPnL = positions.reduce((sum, pos) => sum + pos.pnl, 0);
    const totalExposure = positions.reduce((sum, pos) => sum + Math.abs(pos.exposure), 0);
    const totalRisk = positions.reduce((sum, pos) => sum + pos.risk, 0);

    // Calculate sector concentration
    const sectorExposure: Record<string, number> = {};
    positions.forEach(pos => {
      sectorExposure[pos.sector] = (sectorExposure[pos.sector] || 0) + Math.abs(pos.exposure);
    });
    const maxSectorExposure = Math.max(...Object.values(sectorExposure));
    const concentrationRisk = (maxSectorExposure / totalExposure) * 100;

    return {
      portfolioValue,
      totalPnL,
      totalPnLPercent: (totalPnL / portfolioValue) * 100,
      maxDrawdown: 8.5, // Mock value
      dailyVaR: 15000, // Mock Value at Risk
      sharpeRatio: 1.8, // Mock Sharpe ratio
      maxRisk: totalRisk,
      usedMargin: totalExposure * 0.2, // Mock 20% margin
      availableMargin: portfolioValue - (totalExposure * 0.2),
      concentrationRisk
    };
  };

  const getRiskLevel = (value: number, threshold: number): 'low' | 'medium' | 'high' => {
    if (value <= threshold * 0.5) return 'low';
    if (value <= threshold) return 'medium';
    return 'high';
  };

  const getRiskColor = (level: 'low' | 'medium' | 'high') => {
    switch (level) {
      case 'low': return 'text-green-400 bg-green-900/30 border-green-700';
      case 'medium': return 'text-yellow-400 bg-yellow-900/30 border-yellow-700';
      case 'high': return 'text-red-400 bg-red-900/30 border-red-700';
    }
  };

  const riskMetrics = calculateRiskMetrics();

  const positionRiskLevel = getRiskLevel(
    (riskMetrics.maxRisk / riskMetrics.portfolioValue) * 100,
    riskSettings.maxPortfolioRisk
  );

  const concentrationRiskLevel = getRiskLevel(
    riskMetrics.concentrationRisk,
    riskSettings.maxSectorExposure
  );

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
            <span className="text-white">Risk Manager</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-4">
            <Shield className="h-8 w-8 text-blue-400" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              Portfolio Risk Manager
            </h1>
          </div>
          <p className="text-xl text-slate-300">
            Monitor and manage portfolio risk with advanced analytics and alerts
          </p>
        </div>

        {/* Risk Alert Banner */}
        {(positionRiskLevel === 'high' || concentrationRiskLevel === 'high') && (
          <div className="mb-6 bg-red-900/30 border border-red-700 rounded-xl p-4">
            <div className="flex items-center space-x-2 text-red-400">
              <AlertTriangle className="h-5 w-5" />
              <span className="font-semibold">Risk Alert</span>
            </div>
            <p className="text-red-300 mt-2">
              {positionRiskLevel === 'high' && 'Portfolio risk exceeds maximum threshold. '}
              {concentrationRiskLevel === 'high' && 'High sector concentration detected. '}
              Consider reducing position sizes or diversifying holdings.
            </p>
          </div>
        )}

        {/* Tab Navigation */}
        <div className="mb-6">
          <div className="flex space-x-1 bg-slate-900 p-1 rounded-lg w-fit">
            {[
              { id: 'overview', label: 'Risk Overview', icon: PieChart },
              { id: 'positions', label: 'Position Risk', icon: BarChart3 },
              { id: 'settings', label: 'Risk Settings', icon: Shield }
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setSelectedView(tab.id as any)}
                  className={`flex items-center px-4 py-2 rounded-md font-medium transition-colors ${
                    selectedView === tab.id
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

        {/* Risk Overview */}
        {selectedView === 'overview' && (
          <div className="space-y-6">
            {/* Key Risk Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-slate-400">Portfolio Value</span>
                  <DollarSign className="h-5 w-5 text-blue-400" />
                </div>
                <div className="text-2xl font-bold text-white">
                  ₹{(riskMetrics.portfolioValue / 100000).toFixed(1)}L
                </div>
                <div className={`text-sm mt-1 ${
                  riskMetrics.totalPnL >= 0 ? 'text-green-400' : 'text-red-400'
                }`}>
                  {riskMetrics.totalPnL >= 0 ? '+' : ''}₹{riskMetrics.totalPnL.toLocaleString()} 
                  ({riskMetrics.totalPnLPercent >= 0 ? '+' : ''}{riskMetrics.totalPnLPercent.toFixed(2)}%)
                </div>
              </div>

              <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-slate-400">Daily VaR (95%)</span>
                  <TrendingDown className="h-5 w-5 text-red-400" />
                </div>
                <div className="text-2xl font-bold text-red-400">
                  ₹{(riskMetrics.dailyVaR / 1000).toFixed(0)}K
                </div>
                <div className="text-sm text-slate-400 mt-1">
                  {((riskMetrics.dailyVaR / riskMetrics.portfolioValue) * 100).toFixed(1)}% of portfolio
                </div>
              </div>

              <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-slate-400">Max Drawdown</span>
                  <AlertTriangle className="h-5 w-5 text-yellow-400" />
                </div>
                <div className="text-2xl font-bold text-yellow-400">
                  {riskMetrics.maxDrawdown.toFixed(1)}%
                </div>
                <div className={`text-sm mt-1 ${
                  riskMetrics.maxDrawdown <= riskSettings.maxDrawdown ? 'text-green-400' : 'text-red-400'
                }`}>
                  Limit: {riskSettings.maxDrawdown}%
                </div>
              </div>

              <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-slate-400">Sharpe Ratio</span>
                  <Activity className="h-5 w-5 text-purple-400" />
                </div>
                <div className="text-2xl font-bold text-purple-400">
                  {riskMetrics.sharpeRatio.toFixed(1)}
                </div>
                <div className="text-sm text-slate-400 mt-1">
                  {riskMetrics.sharpeRatio > 1.5 ? 'Excellent' : 
                   riskMetrics.sharpeRatio > 1.0 ? 'Good' : 'Needs improvement'}
                </div>
              </div>
            </div>

            {/* Risk Analysis */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Position Risk Breakdown */}
              <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <h3 className="text-xl font-bold text-white mb-6 flex items-center">
                  <Target className="h-5 w-5 mr-2 text-green-400" />
                  Risk Breakdown
                </h3>
                
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-300">Position Risk</span>
                    <div className="flex items-center space-x-2">
                      <span className="font-mono text-white">
                        {((riskMetrics.maxRisk / riskMetrics.portfolioValue) * 100).toFixed(1)}%
                      </span>
                      <span className={`px-2 py-1 rounded text-xs ${getRiskColor(positionRiskLevel)} border`}>
                        {positionRiskLevel.toUpperCase()}
                      </span>
                    </div>
                  </div>

                  <div className="w-full h-2 bg-slate-700 rounded-full">
                    <div 
                      className={`h-2 rounded-full transition-all duration-300 ${
                        positionRiskLevel === 'high' ? 'bg-red-400' :
                        positionRiskLevel === 'medium' ? 'bg-yellow-400' : 'bg-green-400'
                      }`}
                      style={{ 
                        width: `${Math.min(((riskMetrics.maxRisk / riskMetrics.portfolioValue) * 100) / riskSettings.maxPortfolioRisk * 100, 100)}%` 
                      }}
                    ></div>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-slate-300">Concentration Risk</span>
                    <div className="flex items-center space-x-2">
                      <span className="font-mono text-white">{riskMetrics.concentrationRisk.toFixed(1)}%</span>
                      <span className={`px-2 py-1 rounded text-xs ${getRiskColor(concentrationRiskLevel)} border`}>
                        {concentrationRiskLevel.toUpperCase()}
                      </span>
                    </div>
                  </div>

                  <div className="w-full h-2 bg-slate-700 rounded-full">
                    <div 
                      className={`h-2 rounded-full transition-all duration-300 ${
                        concentrationRiskLevel === 'high' ? 'bg-red-400' :
                        concentrationRiskLevel === 'medium' ? 'bg-yellow-400' : 'bg-green-400'
                      }`}
                      style={{ 
                        width: `${Math.min(riskMetrics.concentrationRisk / riskSettings.maxSectorExposure * 100, 100)}%` 
                      }}
                    ></div>
                  </div>

                  <div className="pt-4 border-t border-slate-800">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-slate-400">Used Margin:</span>
                        <div className="font-mono text-white">₹{(riskMetrics.usedMargin / 100000).toFixed(1)}L</div>
                      </div>
                      <div>
                        <span className="text-slate-400">Available Margin:</span>
                        <div className="font-mono text-green-400">₹{(riskMetrics.availableMargin / 100000).toFixed(1)}L</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Risk Recommendations */}
              <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <h3 className="text-xl font-bold text-white mb-6 flex items-center">
                  <AlertTriangle className="h-5 w-5 mr-2 text-yellow-400" />
                  Risk Recommendations
                </h3>

                <div className="space-y-4">
                  {positionRiskLevel === 'high' && (
                    <div className="p-4 bg-red-900/20 border border-red-700 rounded-lg">
                      <div className="flex items-center space-x-2 mb-2">
                        <AlertTriangle className="h-4 w-4 text-red-400" />
                        <span className="font-semibold text-red-400">High Position Risk</span>
                      </div>
                      <p className="text-red-300 text-sm">
                        Your position risk exceeds the maximum threshold. Consider reducing position sizes or closing some positions.
                      </p>
                    </div>
                  )}

                  {concentrationRiskLevel === 'high' && (
                    <div className="p-4 bg-yellow-900/20 border border-yellow-700 rounded-lg">
                      <div className="flex items-center space-x-2 mb-2">
                        <PieChart className="h-4 w-4 text-yellow-400" />
                        <span className="font-semibold text-yellow-400">High Concentration</span>
                      </div>
                      <p className="text-yellow-300 text-sm">
                        Over-exposure to single sector detected. Diversify across different sectors to reduce concentration risk.
                      </p>
                    </div>
                  )}

                  <div className="p-4 bg-blue-900/20 border border-blue-700 rounded-lg">
                    <div className="flex items-center space-x-2 mb-2">
                      <Shield className="h-4 w-4 text-blue-400" />
                      <span className="font-semibold text-blue-400">Risk Management Tips</span>
                    </div>
                    <ul className="text-blue-300 text-sm space-y-1">
                      <li>• Set stop-losses at {riskSettings.stopLossPercent}% for all positions</li>
                      <li>• Maintain 1:{riskSettings.riskRewardRatio} risk-reward ratio</li>
                      <li>• Keep position size under {riskSettings.maxPositionSize}% of portfolio</li>
                      <li>• Review and rebalance weekly</li>
                    </ul>
                  </div>

                  <div className="p-4 bg-green-900/20 border border-green-700 rounded-lg">
                    <div className="flex items-center space-x-2 mb-2">
                      <Target className="h-4 w-4 text-green-400" />
                      <span className="font-semibold text-green-400">Opportunities</span>
                    </div>
                    <p className="text-green-300 text-sm">
                      Available margin: ₹{(riskMetrics.availableMargin / 100000).toFixed(1)}L. Consider adding defensive positions or hedges.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Position Risk Analysis */}
        {selectedView === 'positions' && (
          <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden">
            <div className="p-6 border-b border-slate-800">
              <h2 className="text-xl font-bold text-white">Position Risk Analysis</h2>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-800">
                  <tr className="text-xs text-slate-300">
                    <th className="px-4 py-3 text-left">Position</th>
                    <th className="px-4 py-3 text-right">Exposure</th>
                    <th className="px-4 py-3 text-right">P&L</th>
                    <th className="px-4 py-3 text-right">Risk</th>
                    <th className="px-4 py-3 text-right">% of Portfolio</th>
                    <th className="px-4 py-3 text-center">Risk Level</th>
                  </tr>
                </thead>
                <tbody>
                  {positions.map((position) => {
                    const portfolioPercent = (Math.abs(position.exposure) / riskMetrics.portfolioValue) * 100;
                    const riskPercent = (position.risk / riskMetrics.portfolioValue) * 100;
                    const riskLevel = getRiskLevel(portfolioPercent, riskSettings.maxPositionSize);

                    return (
                      <tr key={position.id} className="border-t border-slate-800 hover:bg-slate-800/50">
                        <td className="px-4 py-4">
                          <div>
                            <div className="font-medium text-white">{position.symbol}</div>
                            <div className="text-xs text-slate-400">
                              {position.type} • {position.side} • {position.quantity} qty
                            </div>
                            <div className="text-xs text-blue-400">{position.sector}</div>
                          </div>
                        </td>
                        <td className="px-4 py-4 text-right">
                          <div className="font-mono text-white">₹{position.exposure.toLocaleString()}</div>
                        </td>
                        <td className="px-4 py-4 text-right">
                          <div className={`font-mono ${position.pnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                            {position.pnl >= 0 ? '+' : ''}₹{position.pnl.toLocaleString()}
                          </div>
                          <div className={`text-xs ${position.pnlPercent >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                            {position.pnlPercent >= 0 ? '+' : ''}{position.pnlPercent.toFixed(2)}%
                          </div>
                        </td>
                        <td className="px-4 py-4 text-right">
                          <div className="font-mono text-red-400">₹{position.risk.toLocaleString()}</div>
                          <div className="text-xs text-slate-400">{riskPercent.toFixed(1)}% of portfolio</div>
                        </td>
                        <td className="px-4 py-4 text-right">
                          <div className="font-mono text-white">{portfolioPercent.toFixed(1)}%</div>
                        </td>
                        <td className="px-4 py-4 text-center">
                          <span className={`px-2 py-1 rounded text-xs ${getRiskColor(riskLevel)} border`}>
                            {riskLevel.toUpperCase()}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Risk Settings */}
        {selectedView === 'settings' && (
          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <h2 className="text-xl font-bold text-white mb-6">Risk Management Settings</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Maximum Position Size (% of Portfolio)
                </label>
                <input
                  type="number"
                  value={riskSettings.maxPositionSize}
                  onChange={(e) => setRiskSettings(prev => ({ ...prev, maxPositionSize: Number(e.target.value) }))}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                  min="1"
                  max="50"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Maximum Portfolio Risk (%)
                </label>
                <input
                  type="number"
                  value={riskSettings.maxPortfolioRisk}
                  onChange={(e) => setRiskSettings(prev => ({ ...prev, maxPortfolioRisk: Number(e.target.value) }))}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                  min="1"
                  max="20"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Maximum Drawdown (%)
                </label>
                <input
                  type="number"
                  value={riskSettings.maxDrawdown}
                  onChange={(e) => setRiskSettings(prev => ({ ...prev, maxDrawdown: Number(e.target.value) }))}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                  min="5"
                  max="30"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Maximum Sector Exposure (%)
                </label>
                <input
                  type="number"
                  value={riskSettings.maxSectorExposure}
                  onChange={(e) => setRiskSettings(prev => ({ ...prev, maxSectorExposure: Number(e.target.value) }))}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                  min="10"
                  max="50"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Stop Loss Percentage (%)
                </label>
                <input
                  type="number"
                  value={riskSettings.stopLossPercent}
                  onChange={(e) => setRiskSettings(prev => ({ ...prev, stopLossPercent: Number(e.target.value) }))}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                  min="1"
                  max="10"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Risk-Reward Ratio (1:X)
                </label>
                <input
                  type="number"
                  value={riskSettings.riskRewardRatio}
                  onChange={(e) => setRiskSettings(prev => ({ ...prev, riskRewardRatio: Number(e.target.value) }))}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                  min="1"
                  max="5"
                  step="0.5"
                />
              </div>
            </div>

            <div className="mt-6 pt-6 border-t border-slate-800">
              <button className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-semibold transition-colors">
                Save Settings
              </button>
            </div>
          </div>
        )}

        {/* Quick Action Links */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link
            href="/tools/calculator"
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-blue-500 transition-colors group"
          >
            <div className="flex items-center justify-between mb-2">
              <Target className="h-6 w-6 text-blue-400" />
              <div className="text-xs text-slate-400">Calculator</div>
            </div>
            <h3 className="font-semibold text-white group-hover:text-blue-400 transition-colors">
              Position Size Calculator
            </h3>
            <p className="text-sm text-slate-400 mt-1">
              Calculate optimal position sizes
            </p>
          </Link>

          <Link
            href="/tools/alerts"
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-yellow-500 transition-colors group"
          >
            <div className="flex items-center justify-between mb-2">
              <AlertTriangle className="h-6 w-6 text-yellow-400" />
              <div className="text-xs text-slate-400">Alerts</div>
            </div>
            <h3 className="font-semibold text-white group-hover:text-yellow-400 transition-colors">
              Risk Alerts
            </h3>
            <p className="text-sm text-slate-400 mt-1">
              Set up risk threshold alerts
            </p>
          </Link>

          <Link
            href="/portfolio"
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-green-500 transition-colors group"
          >
            <div className="flex items-center justify-between mb-2">
              <PieChart className="h-6 w-6 text-green-400" />
              <div className="text-xs text-slate-400">Portfolio</div>
            </div>
            <h3 className="font-semibold text-white group-hover:text-green-400 transition-colors">
              Portfolio Dashboard
            </h3>
            <p className="text-sm text-slate-400 mt-1">
              View complete portfolio
            </p>
          </Link>
        </div>
      </div>
    </div>
  );
}