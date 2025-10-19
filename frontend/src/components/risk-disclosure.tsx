'use client';

import React from 'react';
import { AlertTriangle, TrendingDown, DollarSign, Clock, Shield, FileText, Scale, Activity } from 'lucide-react';
import Link from 'next/link';

export function RiskDisclosure() {
  return (
    <div className="min-h-screen bg-slate-950 text-white p-4">
      <div className="max-w-4xl mx-auto">
        {/* Navigation Breadcrumb */}
        <div className="mb-6">
          <nav className="flex items-center space-x-2 text-sm text-slate-400">
            <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
            <span>/</span>
            <span className="text-white">Risk Disclosure</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-red-400 to-orange-400 bg-clip-text text-transparent mb-4">
            Risk Disclosure Statement
          </h1>
          <div className="flex items-center space-x-4 text-slate-400">
            <div className="flex items-center">
              <Clock className="h-4 w-4 mr-2" />
              <span>Last updated: October 20, 2024</span>
            </div>
            <div className="flex items-center">
              <FileText className="h-4 w-4 mr-2" />
              <span>Required Reading</span>
            </div>
          </div>
        </div>

        {/* Critical Warning */}
        <div className="bg-red-500/20 border-2 border-red-500 rounded-xl p-6 mb-8">
          <div className="flex items-start space-x-3">
            <AlertTriangle className="h-8 w-8 text-red-400 mt-1 flex-shrink-0" />
            <div>
              <h2 className="text-xl font-bold text-red-400 mb-3">CRITICAL RISK WARNING</h2>
              <p className="text-red-200 mb-4">
                Trading in financial instruments involves substantial risk of loss and is not suitable for all investors. 
                You should carefully consider whether trading is appropriate for you in light of your experience, objectives, 
                financial resources, and other relevant circumstances.
              </p>
              <p className="text-red-300 font-semibold">
                YOU CAN LOSE MORE THAN YOUR INITIAL INVESTMENT
              </p>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="space-y-8">
          
          {/* General Trading Risks */}
          <div className="bg-slate-900 rounded-xl p-8 border border-slate-800">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <TrendingDown className="h-6 w-6 mr-3 text-red-400" />
              General Trading Risks
            </h2>
            
            <div className="space-y-6">
              <div className="border-l-4 border-red-500 pl-4">
                <h3 className="text-lg font-semibold text-white mb-2">Market Risk</h3>
                <p className="text-slate-300">
                  Financial markets are subject to volatility and can move against your position rapidly and unpredictably. 
                  Economic events, geopolitical tensions, and market sentiment can cause significant price movements.
                </p>
              </div>

              <div className="border-l-4 border-orange-500 pl-4">
                <h3 className="text-lg font-semibold text-white mb-2">Liquidity Risk</h3>
                <p className="text-slate-300">
                  Some instruments may have limited liquidity, making it difficult to execute trades at desired prices. 
                  This is particularly relevant for small-cap stocks and certain derivative instruments.
                </p>
              </div>

              <div className="border-l-4 border-yellow-500 pl-4">
                <h3 className="text-lg font-semibold text-white mb-2">Leverage Risk</h3>
                <p className="text-slate-300">
                  Leveraged trading amplifies both potential profits and losses. A small adverse price movement 
                  can result in substantial losses that may exceed your initial investment.
                </p>
              </div>

              <div className="border-l-4 border-blue-500 pl-4">
                <h3 className="text-lg font-semibold text-white mb-2">Technology Risk</h3>
                <p className="text-slate-300">
                  Electronic trading systems may experience technical failures, connectivity issues, or delays 
                  that could prevent you from executing trades or managing positions effectively.
                </p>
              </div>
            </div>
          </div>

          {/* Equity Trading Risks */}
          <div className="bg-slate-900 rounded-xl p-8 border border-slate-800">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <Activity className="h-6 w-6 mr-3 text-blue-400" />
              Equity Trading Risks
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-lg font-semibold text-white mb-3">Company-Specific Risks</h3>
                <ul className="space-y-2 text-slate-300">
                  <li>• Poor financial performance</li>
                  <li>• Management changes</li>
                  <li>• Regulatory actions</li>
                  <li>• Industry disruption</li>
                  <li>• Corporate governance issues</li>
                </ul>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-white mb-3">Market Risks</h3>
                <ul className="space-y-2 text-slate-300">
                  <li>• Sector rotation</li>
                  <li>• Economic cycles</li>
                  <li>• Interest rate changes</li>
                  <li>• Currency fluctuations</li>
                  <li>• Inflation impact</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Options Trading Risks */}
          <div className="bg-slate-900 rounded-xl p-8 border border-slate-800">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <DollarSign className="h-6 w-6 mr-3 text-purple-400" />
              Options Trading Risks
            </h2>
            
            <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-4 mb-6">
              <p className="text-purple-200 font-semibold">
                Options trading is complex and involves significant risk. Options can expire worthless, 
                resulting in total loss of premium paid.
              </p>
            </div>

            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Time Decay (Theta)</h3>
                <p className="text-slate-300">
                  Options lose value as they approach expiration, even if the underlying asset price remains unchanged.
                </p>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Volatility Risk</h3>
                <p className="text-slate-300">
                  Changes in implied volatility can significantly impact option prices, sometimes more than 
                  underlying price movements.
                </p>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Assignment Risk</h3>
                <p className="text-slate-300">
                  Short option positions may be assigned at any time, potentially resulting in unexpected 
                  obligations to buy or sell the underlying asset.
                </p>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Complex Strategies</h3>
                <p className="text-slate-300">
                  Multi-leg option strategies involve multiple commission costs and complex risk profiles 
                  that may not be suitable for all investors.
                </p>
              </div>
            </div>
          </div>

          {/* Cryptocurrency Risks */}
          <div className="bg-slate-900 rounded-xl p-8 border border-slate-800">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <Shield className="h-6 w-6 mr-3 text-yellow-400" />
              Cryptocurrency Trading Risks
            </h2>
            
            <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4 mb-6">
              <p className="text-yellow-200 font-semibold">
                Cryptocurrency markets are highly volatile and largely unregulated. Digital assets can 
                lose substantial value quickly and may become worthless.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-lg font-semibold text-white mb-3">Market Risks</h3>
                <ul className="space-y-2 text-slate-300">
                  <li>• Extreme volatility</li>
                  <li>• 24/7 trading exposure</li>
                  <li>• Limited liquidity</li>
                  <li>• Market manipulation</li>
                  <li>• Price discovery issues</li>
                </ul>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-white mb-3">Technical Risks</h3>
                <ul className="space-y-2 text-slate-300">
                  <li>• Blockchain forks</li>
                  <li>• Smart contract vulnerabilities</li>
                  <li>• Exchange security breaches</li>
                  <li>• Wallet security issues</li>
                  <li>• Network congestion</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Algorithmic Trading Risks */}
          <div className="bg-slate-900 rounded-xl p-8 border border-slate-800">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <Activity className="h-6 w-6 mr-3 text-green-400" />
              Algorithmic Trading Risks
            </h2>
            
            <div className="space-y-6">
              <div className="border-l-4 border-green-500 pl-4">
                <h3 className="text-lg font-semibold text-white mb-2">Strategy Risk</h3>
                <p className="text-slate-300">
                  Past performance of trading strategies does not guarantee future results. Market conditions 
                  change, and strategies that worked historically may fail in current markets.
                </p>
              </div>

              <div className="border-l-4 border-indigo-500 pl-4">
                <h3 className="text-lg font-semibold text-white mb-2">Over-Optimization Risk</h3>
                <p className="text-slate-300">
                  Backtested strategies may be curve-fitted to historical data and may not perform well 
                  in live trading conditions with different market dynamics.
                </p>
              </div>

              <div className="border-l-4 border-pink-500 pl-4">
                <h3 className="text-lg font-semibold text-white mb-2">Execution Risk</h3>
                <p className="text-slate-300">
                  Slippage, latency, and partial fills can significantly impact algorithmic strategy 
                  performance compared to backtested results.
                </p>
              </div>

              <div className="border-l-4 border-cyan-500 pl-4">
                <h3 className="text-lg font-semibold text-white mb-2">System Risk</h3>
                <p className="text-slate-300">
                  Automated systems may malfunction, execute unintended trades, or fail to execute 
                  protective stops, potentially resulting in substantial losses.
                </p>
              </div>
            </div>
          </div>

          {/* Regulatory and Legal Risks */}
          <div className="bg-slate-900 rounded-xl p-8 border border-slate-800">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <Scale className="h-6 w-6 mr-3 text-indigo-400" />
              Regulatory and Legal Risks
            </h2>
            
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Regulatory Changes</h3>
                <p className="text-slate-300">
                  Changes in laws, regulations, or government policies can adversely affect trading 
                  strategies and market accessibility.
                </p>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Tax Implications</h3>
                <p className="text-slate-300">
                  Trading activities may result in complex tax obligations. Consult with tax professionals 
                  to understand the implications of your trading activities.
                </p>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Compliance Requirements</h3>
                <p className="text-slate-300">
                  Traders must comply with position limits, reporting requirements, and other regulatory 
                  obligations that may limit trading strategies.
                </p>
              </div>
            </div>
          </div>

          {/* Risk Management */}
          <div className="bg-slate-900 rounded-xl p-8 border border-slate-800">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <Shield className="h-6 w-6 mr-3 text-blue-400" />
              Risk Management Recommendations
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-lg font-semibold text-white mb-3">Position Sizing</h3>
                <ul className="space-y-2 text-slate-300">
                  <li>• Never risk more than you can afford to lose</li>
                  <li>• Limit position sizes to a small percentage of capital</li>
                  <li>• Diversify across instruments and strategies</li>
                  <li>• Use stop-loss orders appropriately</li>
                </ul>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-white mb-3">Education and Preparation</h3>
                <ul className="space-y-2 text-slate-300">
                  <li>• Thoroughly understand instruments before trading</li>
                  <li>• Test strategies extensively before live deployment</li>
                  <li>• Stay informed about market conditions</li>
                  <li>• Continuously monitor and adjust strategies</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Acknowledgment */}
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-6">
            <h2 className="text-xl font-bold text-red-400 mb-4">Acknowledgment Required</h2>
            <p className="text-red-200 mb-4">
              By using our platform, you acknowledge that you have read, understood, and accepted all the risks 
              outlined in this disclosure. You understand that:
            </p>
            <ul className="space-y-2 text-red-200">
              <li>• Trading involves substantial risk of loss</li>
              <li>• Past performance does not guarantee future results</li>
              <li>• You are solely responsible for your trading decisions</li>
              <li>• You should seek independent financial advice if needed</li>
              <li>• You will trade within your financial means and risk tolerance</li>
            </ul>
          </div>

        </div>

        {/* Footer Links */}
        <div className="mt-8 pt-8 border-t border-slate-800">
          <div className="flex flex-wrap gap-6 justify-center text-slate-400">
            <Link href="/terms" className="hover:text-blue-400 transition-colors">Terms of Service</Link>
            <Link href="/privacy" className="hover:text-blue-400 transition-colors">Privacy Policy</Link>
            <Link href="/compliance" className="hover:text-blue-400 transition-colors">Compliance</Link>
            <Link href="/cookies" className="hover:text-blue-400 transition-colors">Cookie Policy</Link>
          </div>
        </div>
      </div>
    </div>
  );
}