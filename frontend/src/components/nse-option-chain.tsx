'use client';

import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Activity, AlertCircle, Filter, RefreshCw } from 'lucide-react';

interface OptionData {
  strike: number;
  callOI: number;
  callChange: number;
  callVolume: number;
  callLTP: number;
  callBid: number;
  callAsk: number;
  putBid: number;
  putAsk: number;
  putLTP: number;
  putVolume: number;
  putChange: number;
  putOI: number;
}

interface GreeksData {
  delta: number;
  gamma: number;
  theta: number;
  vega: number;
  iv: number;
}

export function NSEOptionChain() {
  const [selectedSymbol, setSelectedSymbol] = useState('NIFTY');
  const [selectedExpiry, setSelectedExpiry] = useState('30-OCT-2025');
  const [spotPrice, setSpotPrice] = useState(21150.75);
  const [showGreeks, setShowGreeks] = useState(false);
  const [optionData, setOptionData] = useState<OptionData[]>([]);

  const symbols = ['NIFTY', 'BANKNIFTY', 'FINNIFTY', 'RELIANCE', 'TCS', 'HDFCBANK'];
  const expiries = ['30-OCT-2025', '06-NOV-2025', '13-NOV-2025', '20-NOV-2025', '27-NOV-2025'];

  useEffect(() => {
    // Mock option chain data
    const generateOptionData = () => {
      const strikes = [];
      const baseStrike = Math.floor(spotPrice / 100) * 100;
      
      for (let i = -10; i <= 10; i++) {
        const strike = baseStrike + (i * 100);
        const isITM = selectedSymbol.includes('NIFTY') ? strike < spotPrice : strike > spotPrice;
        
        strikes.push({
          strike,
          callOI: Math.floor(Math.random() * 50000) + 10000,
          callChange: (Math.random() - 0.5) * 1000,
          callVolume: Math.floor(Math.random() * 100000),
          callLTP: Math.max(0.05, (spotPrice - strike + Math.random() * 100)),
          callBid: Math.max(0.05, (spotPrice - strike + Math.random() * 90)),
          callAsk: Math.max(0.05, (spotPrice - strike + Math.random() * 110)),
          putBid: Math.max(0.05, (strike - spotPrice + Math.random() * 90)),
          putAsk: Math.max(0.05, (strike - spotPrice + Math.random() * 110)),
          putLTP: Math.max(0.05, (strike - spotPrice + Math.random() * 100)),
          putVolume: Math.floor(Math.random() * 100000),
          putChange: (Math.random() - 0.5) * 1000,
          putOI: Math.floor(Math.random() * 50000) + 10000,
        });
      }
      
      setOptionData(strikes);
    };

    generateOptionData();
    
    // Update spot price every 5 seconds
    const interval = setInterval(() => {
      setSpotPrice(prev => prev + (Math.random() - 0.5) * 20);
    }, 5000);

    return () => clearInterval(interval);
  }, [selectedSymbol, selectedExpiry, spotPrice]);

  const formatNumber = (num: number) => {
    if (num >= 10000000) return (num / 10000000).toFixed(1) + 'Cr';
    if (num >= 100000) return (num / 100000).toFixed(1) + 'L';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toFixed(2);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header Controls */}
        <div className="mb-8">
          <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              NSE Option Chain
            </h1>
            
            <div className="flex items-center gap-4">
              <button className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors">
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh
              </button>
              
              <button
                onClick={() => setShowGreeks(!showGreeks)}
                className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
                  showGreeks ? 'bg-purple-600 hover:bg-purple-700' : 'bg-slate-700 hover:bg-slate-600'
                }`}
              >
                <Filter className="h-4 w-4 mr-2" />
                Greeks
              </button>
            </div>
          </div>

          {/* Symbol and Expiry Selection */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Symbol</label>
              <select
                value={selectedSymbol}
                onChange={(e) => setSelectedSymbol(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
              >
                {symbols.map(symbol => (
                  <option key={symbol} value={symbol}>{symbol}</option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Expiry</label>
              <select
                value={selectedExpiry}
                onChange={(e) => setSelectedExpiry(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
              >
                {expiries.map(expiry => (
                  <option key={expiry} value={expiry}>{expiry}</option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Spot Price</label>
              <div className="flex items-center bg-slate-800 border border-slate-700 rounded-lg px-3 py-2">
                <span className="text-green-400 font-mono font-bold">₹{spotPrice.toFixed(2)}</span>
                <Activity className="h-4 w-4 ml-2 text-green-400 animate-pulse" />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Last Updated</label>
              <div className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-300">
                {new Date().toLocaleTimeString()}
              </div>
            </div>
          </div>
        </div>

        {/* Option Chain Table */}
        <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-800">
                <tr>
                  <th colSpan={showGreeks ? 8 : 6} className="px-6 py-4 text-center text-green-400 font-bold border-r border-slate-700">
                    CALLS
                  </th>
                  <th className="px-4 py-4 text-center text-white font-bold border-r border-slate-700">
                    STRIKE
                  </th>
                  <th colSpan={showGreeks ? 8 : 6} className="px-6 py-4 text-center text-red-400 font-bold">
                    PUTS
                  </th>
                </tr>
                <tr className="text-xs text-slate-300">
                  {/* Call Headers */}
                  <th className="px-3 py-2 text-left">OI</th>
                  <th className="px-3 py-2 text-left">Chng</th>
                  <th className="px-3 py-2 text-left">Volume</th>
                  <th className="px-3 py-2 text-left">LTP</th>
                  <th className="px-3 py-2 text-left">Bid</th>
                  <th className="px-3 py-2 text-left border-r border-slate-700">Ask</th>
                  {showGreeks && (
                    <>
                      <th className="px-3 py-2 text-left">Delta</th>
                      <th className="px-3 py-2 text-left border-r border-slate-700">IV%</th>
                    </>
                  )}
                  
                  {/* Strike Header */}
                  <th className="px-4 py-2 text-center border-r border-slate-700">Price</th>
                  
                  {/* Put Headers */}
                  {showGreeks && (
                    <>
                      <th className="px-3 py-2 text-left">IV%</th>
                      <th className="px-3 py-2 text-left">Delta</th>
                    </>
                  )}
                  <th className="px-3 py-2 text-left">Bid</th>
                  <th className="px-3 py-2 text-left">Ask</th>
                  <th className="px-3 py-2 text-left">LTP</th>
                  <th className="px-3 py-2 text-left">Volume</th>
                  <th className="px-3 py-2 text-left">Chng</th>
                  <th className="px-3 py-2 text-left">OI</th>
                </tr>
              </thead>
              <tbody>
                {optionData.map((option, index) => {
                  const isATM = Math.abs(option.strike - spotPrice) < 50;
                  
                  return (
                    <tr
                      key={index}
                      className={`border-t border-slate-800 hover:bg-slate-800/50 ${
                        isATM ? 'bg-yellow-500/5 border-yellow-500/20' : ''
                      }`}
                    >
                      {/* Call Data */}
                      <td className="px-3 py-2 text-sm font-mono">{formatNumber(option.callOI)}</td>
                      <td className={`px-3 py-2 text-sm font-mono ${
                        option.callChange >= 0 ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {option.callChange >= 0 ? '+' : ''}{formatNumber(option.callChange)}
                      </td>
                      <td className="px-3 py-2 text-sm font-mono text-slate-300">{formatNumber(option.callVolume)}</td>
                      <td className="px-3 py-2 text-sm font-mono font-bold text-green-400">
                        {option.callLTP.toFixed(2)}
                      </td>
                      <td className="px-3 py-2 text-sm font-mono text-slate-300">{option.callBid.toFixed(2)}</td>
                      <td className="px-3 py-2 text-sm font-mono text-slate-300 border-r border-slate-700">
                        {option.callAsk.toFixed(2)}
                      </td>
                      
                      {showGreeks && (
                        <>
                          <td className="px-3 py-2 text-sm font-mono text-blue-400">
                            {(Math.random() * 0.8 + 0.1).toFixed(3)}
                          </td>
                          <td className="px-3 py-2 text-sm font-mono text-purple-400 border-r border-slate-700">
                            {(Math.random() * 50 + 10).toFixed(1)}%
                          </td>
                        </>
                      )}
                      
                      {/* Strike Price */}
                      <td className={`px-4 py-2 text-center font-bold border-r border-slate-700 ${
                        isATM ? 'text-yellow-400 bg-yellow-500/10' : 'text-white'
                      }`}>
                        {option.strike}
                      </td>
                      
                      {/* Put Data */}
                      {showGreeks && (
                        <>
                          <td className="px-3 py-2 text-sm font-mono text-purple-400">
                            {(Math.random() * 50 + 10).toFixed(1)}%
                          </td>
                          <td className="px-3 py-2 text-sm font-mono text-blue-400">
                            -{(Math.random() * 0.8 + 0.1).toFixed(3)}
                          </td>
                        </>
                      )}
                      
                      <td className="px-3 py-2 text-sm font-mono text-slate-300">{option.putBid.toFixed(2)}</td>
                      <td className="px-3 py-2 text-sm font-mono text-slate-300">{option.putAsk.toFixed(2)}</td>
                      <td className="px-3 py-2 text-sm font-mono font-bold text-red-400">
                        {option.putLTP.toFixed(2)}
                      </td>
                      <td className="px-3 py-2 text-sm font-mono text-slate-300">{formatNumber(option.putVolume)}</td>
                      <td className={`px-3 py-2 text-sm font-mono ${
                        option.putChange >= 0 ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {option.putChange >= 0 ? '+' : ''}{formatNumber(option.putChange)}
                      </td>
                      <td className="px-3 py-2 text-sm font-mono">{formatNumber(option.putOI)}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Summary Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-8">
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400">Total Call OI</span>
              <TrendingUp className="h-5 w-5 text-green-400" />
            </div>
            <div className="text-2xl font-bold text-green-400">
              {formatNumber(optionData.reduce((sum, opt) => sum + opt.callOI, 0))}
            </div>
          </div>
          
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400">Total Put OI</span>
              <TrendingDown className="h-5 w-5 text-red-400" />
            </div>
            <div className="text-2xl font-bold text-red-400">
              {formatNumber(optionData.reduce((sum, opt) => sum + opt.putOI, 0))}
            </div>
          </div>
          
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400">PCR (OI)</span>
              <Activity className="h-5 w-5 text-blue-400" />
            </div>
            <div className="text-2xl font-bold text-blue-400">
              {(optionData.reduce((sum, opt) => sum + opt.putOI, 0) / 
                optionData.reduce((sum, opt) => sum + opt.callOI, 0)).toFixed(2)}
            </div>
          </div>
          
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400">Max Pain</span>
              <AlertCircle className="h-5 w-5 text-yellow-400" />
            </div>
            <div className="text-2xl font-bold text-yellow-400">
              {Math.floor(spotPrice / 100) * 100}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}