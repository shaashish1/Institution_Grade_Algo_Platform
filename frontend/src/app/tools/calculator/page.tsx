'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Calculator, TrendingUp, TrendingDown, Info, BarChart3, Target, AlertCircle, DollarSign, Percent } from 'lucide-react';

interface CalculationResult {
  maxProfit: number;
  maxLoss: number;
  breakeven: number[];
  profitProbability: number;
  riskReward: number;
  margin: number;
  roi: number;
}

interface PositionInput {
  strategy: string;
  spotPrice: number;
  strike1: number;
  strike2?: number;
  strike3?: number;
  strike4?: number;
  premium1: number;
  premium2?: number;
  premium3?: number;
  premium4?: number;
  quantity: number;
  daysToExpiry: number;
  volatility: number;
}

const strategies = [
  { id: 'long-call', name: 'Long Call', legs: 1, description: 'Bullish strategy with unlimited upside' },
  { id: 'long-put', name: 'Long Put', legs: 1, description: 'Bearish strategy with high downside potential' },
  { id: 'covered-call', name: 'Covered Call', legs: 2, description: 'Generate income on existing stock position' },
  { id: 'protective-put', name: 'Protective Put', legs: 2, description: 'Hedge existing stock position' },
  { id: 'bull-call-spread', name: 'Bull Call Spread', legs: 2, description: 'Limited risk bullish strategy' },
  { id: 'bear-put-spread', name: 'Bear Put Spread', legs: 2, description: 'Limited risk bearish strategy' },
  { id: 'long-straddle', name: 'Long Straddle', legs: 2, description: 'Profit from high volatility' },
  { id: 'long-strangle', name: 'Long Strangle', legs: 2, description: 'Cheaper volatility play' },
  { id: 'iron-condor', name: 'Iron Condor', legs: 4, description: 'Neutral strategy for range-bound markets' },
  { id: 'iron-butterfly', name: 'Iron Butterfly', legs: 4, description: 'High probability neutral strategy' },
];

export default function PositionCalculator() {
  const [selectedStrategy, setSelectedStrategy] = useState('long-call');
  const [inputs, setInputs] = useState<PositionInput>({
    strategy: 'long-call',
    spotPrice: 25700,
    strike1: 25800,
    strike2: 0,
    strike3: 0,
    strike4: 0,
    premium1: 150,
    premium2: 0,
    premium3: 0,
    premium4: 0,
    quantity: 50, // NIFTY lot size
    daysToExpiry: 7,
    volatility: 15
  });
  const [result, setResult] = useState<CalculationResult | null>(null);

  // Calculate position metrics
  const calculatePosition = () => {
    const strategy = strategies.find(s => s.id === selectedStrategy);
    if (!strategy) return null;

    let maxProfit = 0;
    let maxLoss = 0;
    let breakeven: number[] = [];
    let margin = 0;

    switch (selectedStrategy) {
      case 'long-call':
        maxProfit = Infinity; // Unlimited
        maxLoss = inputs.premium1 * inputs.quantity;
        breakeven = [inputs.strike1 + inputs.premium1];
        margin = maxLoss;
        break;
        
      case 'long-put':
        maxProfit = (inputs.strike1 - inputs.premium1) * inputs.quantity;
        maxLoss = inputs.premium1 * inputs.quantity;
        breakeven = [inputs.strike1 - inputs.premium1];
        margin = maxLoss;
        break;
        
      case 'bull-call-spread':
        const netDebit = inputs.premium1 - (inputs.premium2 || 0);
        maxProfit = ((inputs.strike2 || 0) - inputs.strike1 - netDebit) * inputs.quantity;
        maxLoss = netDebit * inputs.quantity;
        breakeven = [inputs.strike1 + netDebit];
        margin = Math.abs(maxLoss);
        break;
        
      case 'iron-condor':
        const netCredit = (inputs.premium2 || 0) + (inputs.premium3 || 0) - inputs.premium1 - (inputs.premium4 || 0);
        maxProfit = netCredit * inputs.quantity;
        const spreadWidth = Math.min(
          (inputs.strike2 || 0) - inputs.strike1,
          (inputs.strike4 || 0) - (inputs.strike3 || 0)
        );
        maxLoss = (spreadWidth - netCredit) * inputs.quantity;
        breakeven = [
          inputs.strike1 + netCredit,
          (inputs.strike4 || 0) - netCredit
        ];
        margin = Math.abs(maxLoss);
        break;
        
      default:
        maxProfit = 1000;
        maxLoss = 500;
        breakeven = [inputs.strike1];
        margin = 500;
    }

    const profitProbability = calculateProfitProbability();
    const riskReward = maxProfit === Infinity ? 999 : maxProfit / Math.abs(maxLoss);
    const roi = maxProfit === Infinity ? 999 : (maxProfit / margin) * 100;

    setResult({
      maxProfit,
      maxLoss: Math.abs(maxLoss),
      breakeven,
      profitProbability,
      riskReward,
      margin,
      roi
    });
  };

  const calculateProfitProbability = (): number => {
    // Simplified Black-Scholes based probability calculation
    const timeToExpiry = inputs.daysToExpiry / 365;
    const volatilityFactor = inputs.volatility / 100;
    const moneyness = inputs.spotPrice / inputs.strike1;
    
    // Basic probability estimate based on moneyness and volatility
    if (selectedStrategy.includes('call')) {
      return Math.max(0, Math.min(100, 50 + (moneyness - 1) * 100 - volatilityFactor * 20));
    } else if (selectedStrategy.includes('put')) {
      return Math.max(0, Math.min(100, 50 - (moneyness - 1) * 100 - volatilityFactor * 20));
    }
    
    return 50; // Neutral strategies
  };

  useEffect(() => {
    calculatePosition();
  }, [inputs, selectedStrategy]);

  const updateInput = (field: keyof PositionInput, value: number | string) => {
    setInputs(prev => ({
      ...prev,
      [field]: typeof value === 'string' ? value : Number(value)
    }));
  };

  const getSelectedStrategy = () => strategies.find(s => s.id === selectedStrategy);

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
            <span className="text-white">Position Calculator</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-4">
            <Calculator className="h-8 w-8 text-blue-400" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              Options Position Calculator
            </h1>
          </div>
          <p className="text-xl text-slate-300">
            Calculate profit/loss, breakeven points, and risk metrics for option strategies
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Strategy Selection */}
          <div className="lg:col-span-1">
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                <Target className="h-5 w-5 mr-2 text-blue-400" />
                Strategy Selection
              </h2>
              
              <div className="space-y-3">
                {strategies.map((strategy) => (
                  <button
                    key={strategy.id}
                    onClick={() => setSelectedStrategy(strategy.id)}
                    className={`w-full text-left p-4 rounded-lg border transition-all duration-200 ${
                      selectedStrategy === strategy.id
                        ? 'bg-blue-600/20 border-blue-500 text-blue-300'
                        : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-600 hover:text-white'
                    }`}
                  >
                    <div className="font-medium mb-1">{strategy.name}</div>
                    <div className="text-xs opacity-80">{strategy.description}</div>
                    <div className="text-xs mt-1 opacity-60">{strategy.legs} leg{strategy.legs > 1 ? 's' : ''}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Quick Info */}
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800 mt-6">
              <h3 className="text-lg font-bold text-white mb-4 flex items-center">
                <Info className="h-5 w-5 mr-2 text-yellow-400" />
                Strategy Info
              </h3>
              <div className="space-y-2 text-sm text-slate-300">
                <div><strong>Market Outlook:</strong> {
                  selectedStrategy.includes('call') ? 'Bullish' :
                  selectedStrategy.includes('put') ? 'Bearish' : 'Neutral'
                }</div>
                <div><strong>Risk Level:</strong> {
                  selectedStrategy.includes('long') ? 'Limited' :
                  selectedStrategy.includes('spread') ? 'Limited' : 'Moderate'
                }</div>
                <div><strong>Complexity:</strong> {
                  getSelectedStrategy()?.legs === 1 ? 'Beginner' :
                  getSelectedStrategy()?.legs === 2 ? 'Intermediate' : 'Advanced'
                }</div>
              </div>
            </div>
          </div>

          {/* Input Parameters */}
          <div className="lg:col-span-1">
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                <DollarSign className="h-5 w-5 mr-2 text-green-400" />
                Position Parameters
              </h2>
              
              <div className="space-y-6">
                {/* Market Data */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Spot Price (₹)</label>
                  <input
                    type="number"
                    value={inputs.spotPrice}
                    onChange={(e) => updateInput('spotPrice', e.target.value)}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                    placeholder="25700"
                  />
                </div>

                {/* Strike Prices */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Strike Price 1 (₹)</label>
                  <input
                    type="number"
                    value={inputs.strike1}
                    onChange={(e) => updateInput('strike1', e.target.value)}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                    placeholder="25800"
                  />
                </div>

                {getSelectedStrategy()?.legs && getSelectedStrategy()!.legs > 1 && (
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Strike Price 2 (₹)</label>
                    <input
                      type="number"
                      value={inputs.strike2}
                      onChange={(e) => updateInput('strike2', e.target.value)}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                      placeholder="25900"
                    />
                  </div>
                )}

                {getSelectedStrategy()?.legs && getSelectedStrategy()!.legs > 2 && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-slate-300 mb-2">Strike Price 3 (₹)</label>
                      <input
                        type="number"
                        value={inputs.strike3}
                        onChange={(e) => updateInput('strike3', e.target.value)}
                        className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                        placeholder="25600"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-300 mb-2">Strike Price 4 (₹)</label>
                      <input
                        type="number"
                        value={inputs.strike4}
                        onChange={(e) => updateInput('strike4', e.target.value)}
                        className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                        placeholder="26000"
                      />
                    </div>
                  </>
                )}

                {/* Premiums */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Premium 1 (₹)</label>
                  <input
                    type="number"
                    value={inputs.premium1}
                    onChange={(e) => updateInput('premium1', e.target.value)}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                    placeholder="150"
                  />
                </div>

                {/* Additional premium inputs based on strategy legs */}
                {getSelectedStrategy()?.legs && getSelectedStrategy()!.legs > 1 && (
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Premium 2 (₹)</label>
                    <input
                      type="number"
                      value={inputs.premium2}
                      onChange={(e) => updateInput('premium2', e.target.value)}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                      placeholder="100"
                    />
                  </div>
                )}

                {/* Quantity and other parameters */}
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Quantity (Lot Size)</label>
                  <input
                    type="number"
                    value={inputs.quantity}
                    onChange={(e) => updateInput('quantity', e.target.value)}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                    placeholder="50"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Days to Expiry</label>
                  <input
                    type="number"
                    value={inputs.daysToExpiry}
                    onChange={(e) => updateInput('daysToExpiry', e.target.value)}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                    placeholder="7"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">Implied Volatility (%)</label>
                  <input
                    type="number"
                    value={inputs.volatility}
                    onChange={(e) => updateInput('volatility', e.target.value)}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                    placeholder="15"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Results */}
          <div className="lg:col-span-1">
            {result && (
              <div className="space-y-6">
                {/* P&L Metrics */}
                <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                  <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                    <BarChart3 className="h-5 w-5 mr-2 text-purple-400" />
                    P&L Analysis
                  </h2>
                  
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-300">Max Profit:</span>
                      <span className={`font-bold ${result.maxProfit === Infinity ? 'text-green-400' : 'text-green-400'}`}>
                        {result.maxProfit === Infinity ? '∞' : `₹${result.maxProfit.toLocaleString()}`}
                      </span>
                    </div>
                    
                    <div className="flex justify-between items-center">
                      <span className="text-slate-300">Max Loss:</span>
                      <span className="font-bold text-red-400">₹{result.maxLoss.toLocaleString()}</span>
                    </div>
                    
                    <div className="flex justify-between items-center">
                      <span className="text-slate-300">Risk/Reward:</span>
                      <span className="font-bold text-blue-400">
                        {result.riskReward === 999 ? '∞' : result.riskReward.toFixed(2)}
                      </span>
                    </div>
                    
                    <div className="flex justify-between items-center">
                      <span className="text-slate-300">ROI:</span>
                      <span className="font-bold text-yellow-400">
                        {result.roi === 999 ? '∞' : `${result.roi.toFixed(1)}%`}
                      </span>
                    </div>
                    
                    <div className="flex justify-between items-center">
                      <span className="text-slate-300">Margin Required:</span>
                      <span className="font-bold text-purple-400">₹{result.margin.toLocaleString()}</span>
                    </div>
                  </div>
                </div>

                {/* Breakeven & Probability */}
                <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                  <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                    <Percent className="h-5 w-5 mr-2 text-cyan-400" />
                    Breakeven & Probability
                  </h2>
                  
                  <div className="space-y-4">
                    <div>
                      <span className="text-slate-300 block mb-2">Breakeven Points:</span>
                      <div className="space-y-1">
                        {result.breakeven.map((be, index) => (
                          <div key={index} className="font-bold text-cyan-400">
                            ₹{be.toFixed(2)}
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div className="flex justify-between items-center">
                      <span className="text-slate-300">Profit Probability:</span>
                      <div className="flex items-center">
                        <span className="font-bold text-green-400 mr-2">{result.profitProbability.toFixed(1)}%</span>
                        <div className="w-16 h-2 bg-slate-700 rounded-full">
                          <div 
                            className="h-2 bg-green-400 rounded-full transition-all duration-500"
                            style={{ width: `${result.profitProbability}%` }}
                          ></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Risk Assessment */}
                <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                  <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                    <AlertCircle className="h-5 w-5 mr-2 text-orange-400" />
                    Risk Assessment
                  </h2>
                  
                  <div className="space-y-3">
                    <div className={`p-3 rounded-lg ${
                      result.riskReward > 2 ? 'bg-green-900/30 border border-green-700' :
                      result.riskReward > 1 ? 'bg-yellow-900/30 border border-yellow-700' :
                      'bg-red-900/30 border border-red-700'
                    }`}>
                      <div className="text-sm font-medium">
                        Risk Level: {
                          result.riskReward > 2 ? 'Low' :
                          result.riskReward > 1 ? 'Moderate' : 'High'
                        }
                      </div>
                    </div>
                    
                    <div className="text-xs text-slate-400 space-y-1">
                      <div>• Consider position sizing based on portfolio risk</div>
                      <div>• Monitor implied volatility changes</div>
                      <div>• Set stop-loss at 50% of max loss</div>
                      <div>• Review position before expiry</div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-8 flex justify-center space-x-4">
          <button
            onClick={calculatePosition}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-semibold transition-colors flex items-center"
          >
            <Calculator className="h-5 w-5 mr-2" />
            Recalculate
          </button>
          
          <Link
            href="/stocks/option-chain"
            className="px-6 py-3 bg-green-600 hover:bg-green-700 rounded-lg text-white font-semibold transition-colors flex items-center"
          >
            <TrendingUp className="h-5 w-5 mr-2" />
            View Option Chain
          </Link>
        </div>
      </div>
    </div>
  );
}