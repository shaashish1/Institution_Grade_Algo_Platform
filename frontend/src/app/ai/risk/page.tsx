'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Shield, AlertTriangle, TrendingDown, Activity, Brain, BarChart3, Target, Zap, PieChart } from 'lucide-react';

interface RiskAssessment {
  symbol: string;
  riskScore: number;
  volatility: number;
  beta: number;
  maxDrawdown: number;
  valueAtRisk: number;
  sharpeRatio: number;
  riskLevel: 'low' | 'medium' | 'high' | 'extreme';
  factors: RiskFactor[];
  recommendations: string[];
}

interface RiskFactor {
  factor: string;
  impact: number;
  description: string;
  severity: 'low' | 'medium' | 'high';
}

interface PortfolioRisk {
  totalValue: number;
  totalRisk: number;
  diversificationScore: number;
  correlationRisk: number;
  concentrationRisk: number;
  liquidityRisk: number;
  overallRiskGrade: 'A' | 'B' | 'C' | 'D' | 'F';
}

const sampleRiskData: RiskAssessment[] = [
  {
    symbol: 'RELIANCE',
    riskScore: 65,
    volatility: 25.4,
    beta: 1.2,
    maxDrawdown: 18.5,
    valueAtRisk: 12500,
    sharpeRatio: 1.4,
    riskLevel: 'medium',
    factors: [
      {
        factor: 'Market Risk',
        impact: 70,
        description: 'Exposure to overall market movements',
        severity: 'medium'
      },
      {
        factor: 'Sector Risk',
        impact: 45,
        description: 'Energy sector volatility',
        severity: 'low'
      },
      {
        factor: 'Liquidity Risk',
        impact: 20,
        description: 'High trading volume ensures liquidity',
        severity: 'low'
      }
    ],
    recommendations: [
      'Consider hedging with index puts',
      'Monitor oil price volatility',
      'Maintain stop-loss at 5% below entry'
    ]
  },
  {
    symbol: 'TCS',
    riskScore: 45,
    volatility: 18.2,
    beta: 0.8,
    maxDrawdown: 12.3,
    valueAtRisk: 8500,
    sharpeRatio: 2.1,
    riskLevel: 'low',
    factors: [
      {
        factor: 'Currency Risk',
        impact: 60,
        description: 'USD exposure from exports',
        severity: 'medium'
      },
      {
        factor: 'Client Risk',
        impact: 35,
        description: 'Dependence on key clients',
        severity: 'low'
      },
      {
        factor: 'Technology Risk',
        impact: 40,
        description: 'Rapid technology changes',
        severity: 'low'
      }
    ],
    recommendations: [
      'Monitor USD/INR movements',
      'Diversify IT sector exposure',
      'Consider covered call strategies'
    ]
  },
  {
    symbol: 'NIFTY 26000 CE',
    riskScore: 85,
    volatility: 45.8,
    beta: 1.8,
    maxDrawdown: 75.0,
    valueAtRisk: 25000,
    sharpeRatio: 0.6,
    riskLevel: 'high',
    factors: [
      {
        factor: 'Time Decay',
        impact: 90,
        description: 'Theta decay accelerates near expiry',
        severity: 'high'
      },
      {
        factor: 'IV Crush',
        impact: 80,
        description: 'Post-event volatility collapse',
        severity: 'high'
      },
      {
        factor: 'Liquidity Risk',
        impact: 30,
        description: 'Good liquidity in near months',
        severity: 'low'
      }
    ],
    recommendations: [
      'Exit before 15 days to expiry',
      'Monitor implied volatility closely',
      'Use tight stop-losses',
      'Consider profit booking at 20% gains'
    ]
  }
];

const samplePortfolioRisk: PortfolioRisk = {
  totalValue: 500000,
  totalRisk: 75000,
  diversificationScore: 72,
  correlationRisk: 65,
  concentrationRisk: 58,
  liquidityRisk: 25,
  overallRiskGrade: 'B'
};

export default function AIRiskAssessment() {
  const [riskData, setRiskData] = useState<RiskAssessment[]>(sampleRiskData);
  const [portfolioRisk, setPortfolioRisk] = useState<PortfolioRisk>(samplePortfolioRisk);
  const [selectedView, setSelectedView] = useState<'individual' | 'portfolio' | 'scenarios'>('individual');
  const [selectedSymbol, setSelectedSymbol] = useState<RiskAssessment | null>(null);

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'low': return 'text-green-400 bg-green-900/30 border-green-700';
      case 'medium': return 'text-yellow-400 bg-yellow-900/30 border-yellow-700';
      case 'high': return 'text-red-400 bg-red-900/30 border-red-700';
      case 'extreme': return 'text-red-600 bg-red-900/50 border-red-600';
      default: return 'text-slate-400 bg-slate-900/30 border-slate-700';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'low': return 'text-green-400';
      case 'medium': return 'text-yellow-400';
      case 'high': return 'text-red-400';
      default: return 'text-slate-400';
    }
  };

  const getGradeColor = (grade: string) => {
    switch (grade) {
      case 'A': return 'text-green-400 bg-green-900/30';
      case 'B': return 'text-blue-400 bg-blue-900/30';
      case 'C': return 'text-yellow-400 bg-yellow-900/30';
      case 'D': return 'text-orange-400 bg-orange-900/30';
      case 'F': return 'text-red-400 bg-red-900/30';
      default: return 'text-slate-400 bg-slate-900/30';
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
            <Link href="/ai" className="hover:text-blue-400 transition-colors">AI</Link>
            <span>/</span>
            <span className="text-white">Risk Assessment</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-4">
            <Shield className="h-8 w-8 text-red-400" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-red-400 to-orange-400 bg-clip-text text-transparent">
              AI Risk Assessment
            </h1>
          </div>
          <p className="text-xl text-slate-300">
            Intelligent risk evaluation using advanced AI models
          </p>
        </div>

        {/* Portfolio Risk Overview */}
        <div className="mb-8 bg-slate-900 rounded-2xl p-6 border border-slate-800">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-bold text-white">Portfolio Risk Overview</h3>
            <div className={`px-4 py-2 rounded-full text-lg font-bold ${getGradeColor(portfolioRisk.overallRiskGrade)}`}>
              Grade: {portfolioRisk.overallRiskGrade}
            </div>
          </div>

          <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
            <div>
              <div className="text-slate-400 text-sm mb-2">Total Value</div>
              <div className="text-2xl font-bold text-white">₹{(portfolioRisk.totalValue / 100000).toFixed(1)}L</div>
              <div className="text-sm text-red-400">Risk: ₹{(portfolioRisk.totalRisk / 100000).toFixed(1)}L</div>
            </div>
            <div>
              <div className="text-slate-400 text-sm mb-2">Diversification</div>
              <div className="text-2xl font-bold text-blue-400">{portfolioRisk.diversificationScore}%</div>
              <div className="text-sm text-slate-400">Well diversified</div>
            </div>
            <div>
              <div className="text-slate-400 text-sm mb-2">Correlation Risk</div>
              <div className="text-2xl font-bold text-yellow-400">{portfolioRisk.correlationRisk}%</div>
              <div className="text-sm text-slate-400">Moderate correlation</div>
            </div>
            <div>
              <div className="text-slate-400 text-sm mb-2">Liquidity Risk</div>
              <div className="text-2xl font-bold text-green-400">{portfolioRisk.liquidityRisk}%</div>
              <div className="text-sm text-slate-400">High liquidity</div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6">
          <div className="flex space-x-1 bg-slate-900 p-1 rounded-lg w-fit">
            {[
              { id: 'individual', label: 'Individual Risk', icon: Target },
              { id: 'portfolio', label: 'Portfolio Risk', icon: PieChart },
              { id: 'scenarios', label: 'Stress Tests', icon: Activity }
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setSelectedView(tab.id as any)}
                  className={`flex items-center px-4 py-2 rounded-md font-medium transition-colors ${
                    selectedView === tab.id
                      ? 'bg-red-600 text-white'
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

        {/* Individual Risk Assessment */}
        {selectedView === 'individual' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Risk List */}
            <div className="lg:col-span-2 space-y-4">
              {riskData.map((assessment) => (
                <div 
                  key={assessment.symbol}
                  className={`bg-slate-900 rounded-2xl p-6 border cursor-pointer transition-all ${
                    selectedSymbol?.symbol === assessment.symbol 
                      ? 'border-red-500 bg-red-900/10' 
                      : 'border-slate-800 hover:border-slate-700'
                  }`}
                  onClick={() => setSelectedSymbol(assessment)}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-xl font-bold text-white mb-2">{assessment.symbol}</h3>
                      <div className="flex items-center space-x-4">
                        <span className={`px-2 py-1 rounded text-xs ${getRiskColor(assessment.riskLevel)} border`}>
                          {assessment.riskLevel.toUpperCase()} RISK
                        </span>
                        <span className="text-slate-400 text-sm">Score: {assessment.riskScore}/100</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-red-400">{assessment.riskScore}</div>
                      <div className="text-xs text-slate-400">Risk Score</div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div>
                      <div className="text-slate-400 text-xs">Volatility</div>
                      <div className="text-white font-bold">{assessment.volatility}%</div>
                    </div>
                    <div>
                      <div className="text-slate-400 text-xs">Beta</div>
                      <div className="text-blue-400 font-bold">{assessment.beta}</div>
                    </div>
                    <div>
                      <div className="text-slate-400 text-xs">Max DD</div>
                      <div className="text-red-400 font-bold">{assessment.maxDrawdown}%</div>
                    </div>
                    <div>
                      <div className="text-slate-400 text-xs">VaR (95%)</div>
                      <div className="text-purple-400 font-bold">₹{(assessment.valueAtRisk / 1000).toFixed(0)}K</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Risk Details */}
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800 h-fit">
              {selectedSymbol ? (
                <div>
                  <h3 className="text-lg font-bold text-white mb-4">Risk Breakdown</h3>
                  
                  <div className="space-y-4">
                    <div>
                      <div className="text-slate-400 text-sm mb-2">Risk Factors</div>
                      <div className="space-y-2">
                        {selectedSymbol.factors.map((factor, index) => (
                          <div key={index} className="p-3 bg-slate-800 rounded-lg">
                            <div className="flex items-center justify-between mb-1">
                              <span className="font-medium text-white">{factor.factor}</span>
                              <span className={`text-xs font-medium ${getSeverityColor(factor.severity)}`}>
                                {factor.severity.toUpperCase()}
                              </span>
                            </div>
                            <div className="flex items-center space-x-2 mb-2">
                              <div className="flex-1 h-1 bg-slate-700 rounded-full">
                                <div 
                                  className={`h-1 rounded-full ${
                                    factor.impact >= 70 ? 'bg-red-400' :
                                    factor.impact >= 50 ? 'bg-yellow-400' : 'bg-green-400'
                                  }`}
                                  style={{ width: `${factor.impact}%` }}
                                ></div>
                              </div>
                              <span className="text-xs text-white">{factor.impact}%</span>
                            </div>
                            <p className="text-xs text-slate-300">{factor.description}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="pt-4 border-t border-slate-800">
                      <div className="text-slate-400 text-sm mb-2">AI Recommendations</div>
                      <div className="space-y-2">
                        {selectedSymbol.recommendations.map((rec, index) => (
                          <div key={index} className="p-2 bg-blue-900/20 border border-blue-700 rounded">
                            <p className="text-blue-300 text-xs">{rec}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center text-slate-400">
                  <Shield className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>Select a position to view risk details</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Portfolio Risk Tab */}
        {selectedView === 'portfolio' && (
          <div className="space-y-6">
            {/* Risk Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                <h4 className="text-lg font-bold text-white mb-4">Value at Risk</h4>
                <div className="text-3xl font-bold text-red-400 mb-2">
                  ₹{(portfolioRisk.totalRisk / 1000).toFixed(0)}K
                </div>
                <div className="text-sm text-slate-400">
                  95% confidence, 1-day horizon
                </div>
                <div className="mt-4 h-2 bg-slate-700 rounded-full">
                  <div 
                    className="h-2 bg-red-400 rounded-full"
                    style={{ width: `${(portfolioRisk.totalRisk / portfolioRisk.totalValue) * 100}%` }}
                  ></div>
                </div>
              </div>

              <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                <h4 className="text-lg font-bold text-white mb-4">Concentration Risk</h4>
                <div className="text-3xl font-bold text-yellow-400 mb-2">
                  {portfolioRisk.concentrationRisk}%
                </div>
                <div className="text-sm text-slate-400">
                  Largest position exposure
                </div>
                <div className="mt-4 h-2 bg-slate-700 rounded-full">
                  <div 
                    className="h-2 bg-yellow-400 rounded-full"
                    style={{ width: `${portfolioRisk.concentrationRisk}%` }}
                  ></div>
                </div>
              </div>

              <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                <h4 className="text-lg font-bold text-white mb-4">Correlation Matrix</h4>
                <div className="text-3xl font-bold text-blue-400 mb-2">
                  {portfolioRisk.correlationRisk}%
                </div>
                <div className="text-sm text-slate-400">
                  Average correlation
                </div>
                <div className="mt-4 h-2 bg-slate-700 rounded-full">
                  <div 
                    className="h-2 bg-blue-400 rounded-full"
                    style={{ width: `${portfolioRisk.correlationRisk}%` }}
                  ></div>
                </div>
              </div>
            </div>

            {/* Risk Distribution Chart Placeholder */}
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <h3 className="text-xl font-bold text-white mb-6">Risk Distribution by Asset</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {riskData.map((item) => (
                  <div key={item.symbol} className="p-4 bg-slate-800 rounded-lg">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-medium text-white">{item.symbol}</span>
                      <span className={`px-2 py-1 rounded text-xs ${getRiskColor(item.riskLevel)}`}>
                        {item.riskLevel.toUpperCase()}
                      </span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="flex-1 h-3 bg-slate-700 rounded-full">
                        <div 
                          className={`h-3 rounded-full ${
                            item.riskScore >= 80 ? 'bg-red-400' :
                            item.riskScore >= 60 ? 'bg-yellow-400' : 'bg-green-400'
                          }`}
                          style={{ width: `${item.riskScore}%` }}
                        ></div>
                      </div>
                      <span className="text-white font-mono text-sm">{item.riskScore}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Stress Test Scenarios */}
        {selectedView === 'scenarios' && (
          <div className="space-y-6">
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <h3 className="text-xl font-bold text-white mb-6">Stress Test Scenarios</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className="p-4 bg-red-900/20 border border-red-700 rounded-lg">
                  <h4 className="font-bold text-red-400 mb-3">Market Crash (-20%)</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Portfolio Impact:</span>
                      <span className="text-red-400 font-mono">-₹95,000</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Worst Position:</span>
                      <span className="text-red-400 font-mono">-₹45,000</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Recovery Time:</span>
                      <span className="text-white">8-12 months</span>
                    </div>
                  </div>
                </div>

                <div className="p-4 bg-yellow-900/20 border border-yellow-700 rounded-lg">
                  <h4 className="font-bold text-yellow-400 mb-3">High Volatility (+50% VIX)</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Option Positions:</span>
                      <span className="text-yellow-400 font-mono">-₹35,000</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Stock Positions:</span>
                      <span className="text-yellow-400 font-mono">-₹15,000</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Risk Increase:</span>
                      <span className="text-white">+75%</span>
                    </div>
                  </div>
                </div>

                <div className="p-4 bg-blue-900/20 border border-blue-700 rounded-lg">
                  <h4 className="font-bold text-blue-400 mb-3">Interest Rate Shock (+200bps)</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-300">Bank Stocks:</span>
                      <span className="text-green-400 font-mono">+₹12,000</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">REITs/Utilities:</span>
                      <span className="text-red-400 font-mono">-₹8,000</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-300">Net Impact:</span>
                      <span className="text-green-400 font-mono">+₹4,000</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Risk Mitigation Suggestions */}
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <h3 className="text-xl font-bold text-white mb-6">AI Risk Mitigation Suggestions</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h4 className="font-semibold text-green-400">Immediate Actions</h4>
                  <div className="space-y-2">
                    <div className="p-3 bg-green-900/20 border border-green-700 rounded">
                      <p className="text-green-300 text-sm">Reduce options exposure by 25% before expiry</p>
                    </div>
                    <div className="p-3 bg-green-900/20 border border-green-700 rounded">
                      <p className="text-green-300 text-sm">Add defensive stocks to reduce beta</p>
                    </div>
                    <div className="p-3 bg-green-900/20 border border-green-700 rounded">
                      <p className="text-green-300 text-sm">Implement stop-losses at 5% levels</p>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <h4 className="font-semibold text-blue-400">Long-term Strategy</h4>
                  <div className="space-y-2">
                    <div className="p-3 bg-blue-900/20 border border-blue-700 rounded">
                      <p className="text-blue-300 text-sm">Diversify across uncorrelated sectors</p>
                    </div>
                    <div className="p-3 bg-blue-900/20 border border-blue-700 rounded">
                      <p className="text-blue-300 text-sm">Consider portfolio hedging with index puts</p>
                    </div>
                    <div className="p-3 bg-blue-900/20 border border-blue-700 rounded">
                      <p className="text-blue-300 text-sm">Gradually reduce position concentration</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Quick Action Links */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link
            href="/tools/risk"
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-red-500 transition-colors group"
          >
            <div className="flex items-center justify-between mb-2">
              <Shield className="h-6 w-6 text-red-400" />
              <div className="text-xs text-slate-400">Tools</div>
            </div>
            <h3 className="font-semibold text-white group-hover:text-red-400 transition-colors">
              Risk Manager
            </h3>
            <p className="text-sm text-slate-400 mt-1">
              Portfolio risk management
            </p>
          </Link>

          <Link
            href="/ai/strategies"
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-purple-500 transition-colors group"
          >
            <div className="flex items-center justify-between mb-2">
              <Brain className="h-6 w-6 text-purple-400" />
              <div className="text-xs text-slate-400">AI</div>
            </div>
            <h3 className="font-semibold text-white group-hover:text-purple-400 transition-colors">
              Strategy Analyzer
            </h3>
            <p className="text-sm text-slate-400 mt-1">
              Risk-adjusted strategies
            </p>
          </Link>

          <Link
            href="/portfolio"
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-green-500 transition-colors group"
          >
            <div className="flex items-center justify-between mb-2">
              <BarChart3 className="h-6 w-6 text-green-400" />
              <div className="text-xs text-slate-400">Portfolio</div>
            </div>
            <h3 className="font-semibold text-white group-hover:text-green-400 transition-colors">
              Portfolio Dashboard
            </h3>
            <p className="text-sm text-slate-400 mt-1">
              Monitor your positions
            </p>
          </Link>
        </div>
      </div>
    </div>
  );
}