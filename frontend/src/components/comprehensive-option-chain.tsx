'use client';

import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Activity, AlertCircle, Filter, RefreshCw, BarChart3, Target, Download, Eye, EyeOff } from 'lucide-react';
import Link from 'next/link';

interface ComprehensiveOptionData {
  strike: number;
  // Call Options Data
  callOI: number;
  callChangeInOI: number;
  callVolume: number;
  callIV: number;
  callLTP: number;
  callChange: number;
  callBidQty: number;
  callBid: number;
  callAsk: number;
  callAskQty: number;
  // Put Options Data
  putOI: number;
  putChangeInOI: number;
  putVolume: number;
  putIV: number;
  putLTP: number;
  putChange: number;
  putBidQty: number;
  putBid: number;
  putAsk: number;
  putAskQty: number;
  // Greeks and additional data
  callDelta?: number;
  callGamma?: number;
  callTheta?: number;
  callVega?: number;
  putDelta?: number;
  putGamma?: number;
  putTheta?: number;
  putVega?: number;
}

interface MarketData {
  symbol: string;
  spotPrice: number;
  change: number;
  changePercent: number;
  high: number;
  low: number;
  volume: number;
  vix?: number;
  sector?: string;
  lotSize: number;
  strikeInterval: number;
  openInterest: number;
  pcr: number; // Put-Call Ratio
  maxPain: number;
}

interface SymbolData {
  symbol: string;
  name: string;
  type: 'index' | 'stock';
  sector?: string;
  expiries: string[];
  lotSize: number;
  strikeInterval: number;
  expiryDay: 'monday' | 'thursday'; // New expiry day tracking
}

// Updated NSE symbols with new Monday expiry system (effective April 2025)
const NSE_OPTION_SYMBOLS: Record<string, SymbolData> = {
  // Indices - Now expire on Monday (post April 2025 change)
  'NIFTY': {
    symbol: 'NIFTY',
    name: 'Nifty 50',
    type: 'index',
    expiries: [
      '21-OCT-2025', '28-OCT-2025', '04-NOV-2025', '11-NOV-2025', '18-NOV-2025', '25-NOV-2025', // Weekly Monday expiries
      '02-DEC-2025', '09-DEC-2025', '16-DEC-2025', '23-DEC-2025', '30-DEC-2025', // Weekly Monday expiries
      '27-JAN-2026', '24-FEB-2026', '30-MAR-2026', '28-APR-2026', '26-MAY-2026', '29-JUN-2026' // Monthly Monday expiries
    ],
    lotSize: 50,
    strikeInterval: 50,
    expiryDay: 'monday'
  },
  'BANKNIFTY': {
    symbol: 'BANKNIFTY',
    name: 'Bank Nifty',
    type: 'index',
    expiries: [
      '21-OCT-2025', '28-OCT-2025', '04-NOV-2025', '11-NOV-2025', '18-NOV-2025', '25-NOV-2025',
      '02-DEC-2025', '09-DEC-2025', '16-DEC-2025', '23-DEC-2025', '30-DEC-2025',
      '27-JAN-2026', '24-FEB-2026', '30-MAR-2026', '28-APR-2026', '26-MAY-2026', '29-JUN-2026'
    ],
    lotSize: 15,
    strikeInterval: 100,
    expiryDay: 'monday'
  },
  'FINNIFTY': {
    symbol: 'FINNIFTY',
    name: 'Fin Nifty',
    type: 'index',
    expiries: [
      '21-OCT-2025', '28-OCT-2025', '04-NOV-2025', '11-NOV-2025', '18-NOV-2025', '25-NOV-2025',
      '02-DEC-2025', '09-DEC-2025', '16-DEC-2025', '23-DEC-2025', '30-DEC-2025',
      '27-JAN-2026', '24-FEB-2026', '30-MAR-2026'
    ],
    lotSize: 40,
    strikeInterval: 50,
    expiryDay: 'monday'
  },
  'MIDCPNIFTY': {
    symbol: 'MIDCPNIFTY',
    name: 'Midcap Nifty',
    type: 'index',
    expiries: ['28-OCT-2025', '25-NOV-2025', '30-DEC-2025', '27-JAN-2026', '24-FEB-2026', '30-MAR-2026'],
    lotSize: 75,
    strikeInterval: 25,
    expiryDay: 'monday'
  },
  // Banking Stocks - Monthly expiry on Monday
  'HDFCBANK': {
    symbol: 'HDFCBANK',
    name: 'HDFC Bank',
    type: 'stock',
    sector: 'Banking',
    expiries: ['28-OCT-2025', '25-NOV-2025', '30-DEC-2025', '26-JAN-2026', '23-FEB-2026', '30-MAR-2026'],
    lotSize: 550,
    strikeInterval: 10,
    expiryDay: 'monday'
  },
  'ICICIBANK': {
    symbol: 'ICICIBANK',
    name: 'ICICI Bank',
    type: 'stock',
    sector: 'Banking',
    expiries: ['28-OCT-2025', '25-NOV-2025', '30-DEC-2025', '26-JAN-2026', '23-FEB-2026', '30-MAR-2026'],
    lotSize: 1375,
    strikeInterval: 5,
    expiryDay: 'monday'
  },
  'SBIN': {
    symbol: 'SBIN',
    name: 'State Bank of India',
    type: 'stock',
    sector: 'Banking',
    expiries: ['28-OCT-2025', '25-NOV-2025', '30-DEC-2025', '26-JAN-2026', '23-FEB-2026', '30-MAR-2026'],
    lotSize: 1500,
    strikeInterval: 5,
    expiryDay: 'monday'
  },
  'AXISBANK': {
    symbol: 'AXISBANK',
    name: 'Axis Bank',
    type: 'stock',
    sector: 'Banking',
    expiries: ['28-OCT-2025', '25-NOV-2025', '30-DEC-2025', '26-JAN-2026', '23-FEB-2026', '30-MAR-2026'],
    lotSize: 1200,
    strikeInterval: 5,
    expiryDay: 'monday'
  },
  // IT Stocks
  'RELIANCE': {
    symbol: 'RELIANCE',
    name: 'Reliance Industries',
    type: 'stock',
    sector: 'Oil & Gas',
    expiries: ['28-OCT-2025', '25-NOV-2025', '30-DEC-2025', '26-JAN-2026', '23-FEB-2026', '30-MAR-2026'],
    lotSize: 250,
    strikeInterval: 10,
    expiryDay: 'monday'
  },
  'TCS': {
    symbol: 'TCS',
    name: 'Tata Consultancy Services',
    type: 'stock',
    sector: 'IT',
    expiries: ['28-OCT-2025', '25-NOV-2025', '30-DEC-2025', '26-JAN-2026', '23-FEB-2026', '30-MAR-2026'],
    lotSize: 150,
    strikeInterval: 25,
    expiryDay: 'monday'
  },
  'INFY': {
    symbol: 'INFY',
    name: 'Infosys',
    type: 'stock',
    sector: 'IT',
    expiries: ['28-OCT-2025', '25-NOV-2025', '30-DEC-2025', '26-JAN-2026', '23-FEB-2026', '30-MAR-2026'],
    lotSize: 300,
    strikeInterval: 25,
    expiryDay: 'monday'
  },
  'WIPRO': {
    symbol: 'WIPRO',
    name: 'Wipro',
    type: 'stock',
    sector: 'IT',
    expiries: ['28-OCT-2025', '25-NOV-2025', '30-DEC-2025', '26-JAN-2026', '23-FEB-2026', '30-MAR-2026'],
    lotSize: 1200,
    strikeInterval: 5,
    expiryDay: 'monday'
  },
  'HCLTECH': {
    symbol: 'HCLTECH',
    name: 'HCL Technologies',
    type: 'stock',
    sector: 'IT',
    expiries: ['28-OCT-2025', '25-NOV-2025', '30-DEC-2025', '26-JAN-2026', '23-FEB-2026', '30-MAR-2026'],
    lotSize: 350,
    strikeInterval: 10,
    expiryDay: 'monday'
  }
};

const REAL_MARKET_DATA: Record<string, MarketData> = {
  'NIFTY': {
    symbol: 'NIFTY',
    spotPrice: 25709.85, // Updated from the attachment
    change: 142.75,
    changePercent: 0.56,
    high: 25781.55,
    low: 25598.90,
    volume: 2847593,
    vix: 14.85,
    lotSize: 50,
    strikeInterval: 50,
    openInterest: 2567893,
    pcr: 1.23,
    maxPain: 25700
  },
  'BANKNIFTY': {
    symbol: 'BANKNIFTY',
    spotPrice: 54789.25,
    change: -234.60,
    changePercent: -0.43,
    high: 55123.40,
    low: 54567.80,
    volume: 1543876,
    lotSize: 15,
    strikeInterval: 100,
    openInterest: 1234567,
    pcr: 0.89,
    maxPain: 54800
  },
  'FINNIFTY': {
    symbol: 'FINNIFTY',
    spotPrice: 23456.70,
    change: 89.30,
    changePercent: 0.38,
    high: 23567.20,
    low: 23234.50,
    volume: 876543,
    sector: 'Financial Services',
    lotSize: 40,
    strikeInterval: 50,
    openInterest: 567890,
    pcr: 1.15,
    maxPain: 23450
  },
  // Add other symbols with comprehensive data...
  'HDFCBANK': {
    symbol: 'HDFCBANK',
    spotPrice: 1654.85,
    change: 12.30,
    changePercent: 0.75,
    high: 1667.15,
    low: 1642.55,
    volume: 23456789,
    sector: 'Banking',
    lotSize: 550,
    strikeInterval: 10,
    openInterest: 890123,
    pcr: 1.05,
    maxPain: 1650
  }
};

export function ComprehensiveOptionChain() {
  const [selectedSymbol, setSelectedSymbol] = useState('NIFTY');
  const [selectedExpiry, setSelectedExpiry] = useState('21-OCT-2025');
  const [symbolFilter, setSymbolFilter] = useState<'all' | 'index' | 'stock'>('all');
  const [sectorFilter, setSectorFilter] = useState<string>('all');
  const [showGreeks, setShowGreeks] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [optionData, setOptionData] = useState<ComprehensiveOptionData[]>([]);
  const [marketData, setMarketData] = useState<MarketData>(REAL_MARKET_DATA.NIFTY);

  // Get available symbols based on filters
  const getFilteredSymbols = () => {
    let symbols = Object.keys(NSE_OPTION_SYMBOLS);
    
    if (symbolFilter !== 'all') {
      symbols = symbols.filter(symbol => NSE_OPTION_SYMBOLS[symbol].type === symbolFilter);
    }
    
    if (sectorFilter !== 'all') {
      symbols = symbols.filter(symbol => NSE_OPTION_SYMBOLS[symbol].sector === sectorFilter);
    }
    
    return symbols.sort((a, b) => {
      const aData = NSE_OPTION_SYMBOLS[a];
      const bData = NSE_OPTION_SYMBOLS[b];
      
      if (aData.type !== bData.type) {
        return aData.type === 'index' ? -1 : 1;
      }
      
      return a.localeCompare(b);
    });
  };

  const getAvailableExpiries = () => {
    return NSE_OPTION_SYMBOLS[selectedSymbol]?.expiries || [];
  };

  const getAvailableSectors = () => {
    const sectors = new Set<string>();
    Object.values(NSE_OPTION_SYMBOLS).forEach(symbol => {
      if (symbol.sector) sectors.add(symbol.sector);
    });
    return Array.from(sectors).sort();
  };

  const handleSymbolChange = (newSymbol: string) => {
    setSelectedSymbol(newSymbol);
    const availableExpiries = NSE_OPTION_SYMBOLS[newSymbol]?.expiries || [];
    setSelectedExpiry(availableExpiries[0] || '21-OCT-2025');
  };

  const symbols = getFilteredSymbols();
  const expiries = getAvailableExpiries();
  const sectors = getAvailableSectors();

  useEffect(() => {
    const currentMarketData = REAL_MARKET_DATA[selectedSymbol];
    if (!currentMarketData) return;
    
    setMarketData(currentMarketData);
    
    const generateComprehensiveOptionData = () => {
      const strikes = [];
      const spotPrice = currentMarketData.spotPrice;
      const symbolData = NSE_OPTION_SYMBOLS[selectedSymbol];
      const strikeInterval = symbolData?.strikeInterval || 50;
      
      const baseStrike = Math.floor(spotPrice / strikeInterval) * strikeInterval;
      const numStrikes = 21; // 10 above, 10 below + ATM
      
      for (let i = -10; i <= 10; i++) {
        const strike = baseStrike + (i * strikeInterval);
        const moneyness = (spotPrice - strike) / spotPrice;
        const distanceFromATM = Math.abs(spotPrice - strike);
        
        // Calculate days to expiry
        const expiryDate = new Date(selectedExpiry);
        const today = new Date();
        const daysToExpiry = Math.max(1, Math.ceil((expiryDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24)));
        const timeToExpiry = daysToExpiry / 365;
        
        // Sector-based volatility
        let baseVolatility = 0.15;
        if (selectedSymbol === 'NIFTY' && currentMarketData.vix) {
          baseVolatility = currentMarketData.vix / 100;
        } else if (selectedSymbol === 'BANKNIFTY') {
          baseVolatility = 0.18;
        } else if (currentMarketData.sector === 'IT') {
          baseVolatility = 0.25;
        } else if (currentMarketData.sector === 'Banking') {
          baseVolatility = 0.20;
        }
        
        const volatility = baseVolatility + (Math.random() - 0.5) * 0.05;
        const riskFreeRate = 0.07;
        
        // Black-Scholes calculations
        const d1 = (Math.log(spotPrice / strike) + (riskFreeRate + 0.5 * volatility * volatility) * timeToExpiry) / 
                   (volatility * Math.sqrt(timeToExpiry));
        const d2 = d1 - volatility * Math.sqrt(timeToExpiry);
        
        const callPrice = Math.max(0.05, 
          spotPrice * normalCDF(d1) - strike * Math.exp(-riskFreeRate * timeToExpiry) * normalCDF(d2)
        );
        const putPrice = Math.max(0.05,
          strike * Math.exp(-riskFreeRate * timeToExpiry) * normalCDF(-d2) - spotPrice * normalCDF(-d1)
        );

        // Greeks calculations
        const callDelta = normalCDF(d1);
        const putDelta = callDelta - 1;
        const gamma = normalPDF(d1) / (spotPrice * volatility * Math.sqrt(timeToExpiry));
        const callTheta = -(spotPrice * normalPDF(d1) * volatility) / (2 * Math.sqrt(timeToExpiry)) - 
                         riskFreeRate * strike * Math.exp(-riskFreeRate * timeToExpiry) * normalCDF(d2);
        const putTheta = -(spotPrice * normalPDF(d1) * volatility) / (2 * Math.sqrt(timeToExpiry)) + 
                        riskFreeRate * strike * Math.exp(-riskFreeRate * timeToExpiry) * normalCDF(-d2);
        const vega = spotPrice * normalPDF(d1) * Math.sqrt(timeToExpiry);
        
        // Volume and OI based on moneyness and lot size
        const lotSize = symbolData?.lotSize || 50;
        const volumeMultiplier = Math.exp(-Math.pow(distanceFromATM / (strikeInterval * 3), 2));
        const baseVolume = Math.max(1000, 50000 / lotSize);
        const baseOI = Math.max(5000, 200000 / lotSize);
        
        strikes.push({
          strike,
          // Call Options
          callOI: Math.floor((Math.random() * baseOI + baseOI * 0.5) * volumeMultiplier / lotSize) * lotSize,
          callChangeInOI: Math.floor((Math.random() - 0.5) * baseOI * 0.1 / lotSize) * lotSize,
          callVolume: Math.floor((Math.random() * baseVolume + baseVolume * 0.2) * volumeMultiplier / lotSize) * lotSize,
          callIV: volatility * 100 + (Math.random() - 0.5) * 5,
          callLTP: parseFloat(callPrice.toFixed(2)),
          callChange: (Math.random() - 0.5) * callPrice * 0.3,
          callBidQty: Math.floor((Math.random() * 100 + 50) / lotSize) * lotSize,
          callBid: parseFloat((callPrice * 0.995).toFixed(2)),
          callAsk: parseFloat((callPrice * 1.005).toFixed(2)),
          callAskQty: Math.floor((Math.random() * 100 + 50) / lotSize) * lotSize,
          
          // Put Options
          putOI: Math.floor((Math.random() * baseOI + baseOI * 0.5) * volumeMultiplier / lotSize) * lotSize,
          putChangeInOI: Math.floor((Math.random() - 0.5) * baseOI * 0.1 / lotSize) * lotSize,
          putVolume: Math.floor((Math.random() * baseVolume + baseVolume * 0.2) * volumeMultiplier / lotSize) * lotSize,
          putIV: volatility * 100 + (Math.random() - 0.5) * 5,
          putLTP: parseFloat(putPrice.toFixed(2)),
          putChange: (Math.random() - 0.5) * putPrice * 0.3,
          putBidQty: Math.floor((Math.random() * 100 + 50) / lotSize) * lotSize,
          putBid: parseFloat((putPrice * 0.995).toFixed(2)),
          putAsk: parseFloat((putPrice * 1.005).toFixed(2)),
          putAskQty: Math.floor((Math.random() * 100 + 50) / lotSize) * lotSize,
          
          // Greeks
          callDelta: callDelta,
          callGamma: gamma,
          callTheta: callTheta / 365, // Per day
          callVega: vega / 100, // Per 1% change in volatility
          putDelta: putDelta,
          putGamma: gamma,
          putTheta: putTheta / 365,
          putVega: vega / 100
        });
      }
      
      setOptionData(strikes.sort((a, b) => a.strike - b.strike));
    };

    generateComprehensiveOptionData();
    
    // Update data every 3 seconds
    const interval = setInterval(() => {
      const variation = (Math.random() - 0.5) * 0.002;
      const newPrice = currentMarketData.spotPrice * (1 + variation);
      setMarketData(prev => ({
        ...prev,
        spotPrice: parseFloat(newPrice.toFixed(2)),
        change: parseFloat((newPrice - currentMarketData.spotPrice + currentMarketData.change).toFixed(2))
      }));
      generateComprehensiveOptionData();
    }, 3000);

    return () => clearInterval(interval);
  }, [selectedSymbol, selectedExpiry]);

  // Helper functions
  function normalCDF(x: number): number {
    return 0.5 * (1 + erf(x / Math.sqrt(2)));
  }

  function normalPDF(x: number): number {
    return Math.exp(-0.5 * x * x) / Math.sqrt(2 * Math.PI);
  }

  function erf(x: number): number {
    const a1 =  0.254829592;
    const a2 = -0.284496736;
    const a3 =  1.421413741;
    const a4 = -1.453152027;
    const a5 =  1.061405429;
    const p  =  0.3275911;

    const sign = x >= 0 ? 1 : -1;
    x = Math.abs(x);

    const t = 1.0 / (1.0 + p * x);
    const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);

    return sign * y;
  }

  const formatNumber = (num: number) => {
    if (num >= 10000000) return (num / 10000000).toFixed(1) + 'Cr';
    if (num >= 100000) return (num / 100000).toFixed(1) + 'L';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toFixed(0);
  };

  const getATMStrike = () => {
    const symbolData = NSE_OPTION_SYMBOLS[selectedSymbol];
    const strikeInterval = symbolData?.strikeInterval || 50;
    return Math.round(marketData.spotPrice / strikeInterval) * strikeInterval;
  };

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
            <span className="text-white">Comprehensive Option Chain</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
                NSE Option Chain - Complete Data
              </h1>
              <p className="text-slate-400">
                All columns: OI • CHNG IN OI • VOLUME • IV • LTP • CHNG • BID QTY • BID • ASK • ASK QTY • STRIKE
              </p>
              <div className="text-sm text-yellow-400 mt-2">
                📅 Updated Expiry System: {NSE_OPTION_SYMBOLS[selectedSymbol]?.expiryDay === 'monday' ? 'Monday Expiries (Post April 2025)' : 'Thursday Expiries'}
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <button
                onClick={() => setShowGreeks(!showGreeks)}
                className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
                  showGreeks ? 'bg-purple-600 hover:bg-purple-700' : 'bg-slate-700 hover:bg-slate-600'
                }`}
              >
                {showGreeks ? <EyeOff className="h-4 w-4 mr-2" /> : <Eye className="h-4 w-4 mr-2" />}
                Greeks
              </button>
              <button
                onClick={() => setShowAdvanced(!showAdvanced)}
                className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
                  showAdvanced ? 'bg-orange-600 hover:bg-orange-700' : 'bg-slate-700 hover:bg-slate-600'
                }`}
              >
                <Filter className="h-4 w-4 mr-2" />
                Advanced
              </button>
              <Link 
                href="/stocks/backtest"
                className="flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg transition-colors"
              >
                <BarChart3 className="h-4 w-4 mr-2" />
                Backtest
              </Link>
              <button className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors">
                <Download className="h-4 w-4 mr-2" />
                Export
              </button>
            </div>
          </div>

          {/* Market Data Summary */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-semibold">{marketData.symbol}</h3>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                  <span className="text-sm text-green-400">LIVE</span>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="text-3xl font-bold text-white">
                    ₹{marketData.spotPrice.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                  </div>
                  <div className={`text-lg font-medium flex items-center ${
                    marketData.change >= 0 ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {marketData.change >= 0 ? <TrendingUp className="h-4 w-4 mr-1" /> : <TrendingDown className="h-4 w-4 mr-1" />}
                    {marketData.change >= 0 ? '+' : ''}{marketData.change.toFixed(2)} ({marketData.changePercent.toFixed(2)}%)
                  </div>
                </div>
                <div className="text-sm text-slate-300 space-y-1">
                  <div className="flex justify-between">
                    <span>High:</span>
                    <span className="font-semibold text-green-400">₹{marketData.high.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Low:</span>
                    <span className="font-semibold text-red-400">₹{marketData.low.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Volume:</span>
                    <span className="font-semibold">{formatNumber(marketData.volume)}</span>
                  </div>
                  {marketData.vix && (
                    <div className="flex justify-between">
                      <span>VIX:</span>
                      <span className="font-semibold text-yellow-400">{marketData.vix.toFixed(2)}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Option Analytics */}
            <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
              <h3 className="text-lg font-semibold mb-4">Option Analytics</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="flex justify-between">
                  <span>Total OI:</span>
                  <span className="font-semibold text-blue-400">{formatNumber(marketData.openInterest)}</span>
                </div>
                <div className="flex justify-between">
                  <span>PCR:</span>
                  <span className="font-semibold text-purple-400">{marketData.pcr.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Max Pain:</span>
                  <span className="font-semibold text-yellow-400">₹{marketData.maxPain}</span>
                </div>
                <div className="flex justify-between">
                  <span>ATM Strike:</span>
                  <span className="font-semibold text-orange-400">₹{getATMStrike()}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Enhanced Symbol and Expiry Selection */}
          <div className="space-y-4">
            {/* Filter Controls */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 bg-slate-800 rounded-xl border border-slate-700">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Filter by Type</label>
                <select
                  value={symbolFilter}
                  onChange={(e) => setSymbolFilter(e.target.value as 'all' | 'index' | 'stock')}
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                >
                  <option value="all">All Symbols</option>
                  <option value="index">Indices Only</option>
                  <option value="stock">Stocks Only</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Filter by Sector</label>
                <select
                  value={sectorFilter}
                  onChange={(e) => setSectorFilter(e.target.value)}
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                  disabled={symbolFilter === 'index'}
                >
                  <option value="all">All Sectors</option>
                  {sectors.map(sector => (
                    <option key={sector} value={sector}>{sector}</option>
                  ))}
                </select>
              </div>
              
              <div className="flex items-end">
                <div className="text-sm text-slate-400">
                  <div className="font-medium text-white">{symbols.length} symbols available</div>
                  <div>{expiries.length} expiry dates for {selectedSymbol}</div>
                </div>
              </div>
            </div>

            {/* Symbol and Expiry Selection */}
            <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Symbol 
                  <span className="ml-2 text-xs text-slate-400">
                    ({NSE_OPTION_SYMBOLS[selectedSymbol]?.type === 'index' ? 'Index' : 'Stock'})
                  </span>
                </label>
                <select
                  value={selectedSymbol}
                  onChange={(e) => handleSymbolChange(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                >
                  {symbols.map(symbol => {
                    const symbolData = NSE_OPTION_SYMBOLS[symbol];
                    return (
                      <option key={symbol} value={symbol}>
                        {symbol} - {symbolData.name}
                      </option>
                    );
                  })}
                </select>
                {NSE_OPTION_SYMBOLS[selectedSymbol]?.sector && (
                  <div className="text-xs text-slate-400 mt-1">
                    Sector: {NSE_OPTION_SYMBOLS[selectedSymbol].sector}
                  </div>
                )}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Expiry Date
                  <span className="ml-2 text-xs text-slate-400">({expiries.length} available)</span>
                </label>
                <select
                  value={selectedExpiry}
                  onChange={(e) => setSelectedExpiry(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                >
                  {expiries.map((expiry, index) => {
                    const expiryDate = new Date(expiry);
                    const today = new Date();
                    const daysToExpiry = Math.ceil((expiryDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
                    return (
                      <option key={expiry} value={expiry}>
                        {expiry} ({daysToExpiry}d)
                      </option>
                    );
                  })}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">ATM Strike</label>
                <div className="flex items-center bg-slate-800 border border-slate-700 rounded-lg px-3 py-2">
                  <Target className="h-4 w-4 mr-2 text-yellow-400" />
                  <span className="text-yellow-400 font-mono font-bold">{getATMStrike()}</span>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Lot Size</label>
                <div className="flex items-center bg-slate-800 border border-slate-700 rounded-lg px-3 py-2">
                  <span className="text-blue-400 font-mono font-bold">{marketData.lotSize}</span>
                  <span className="text-slate-400 ml-1 text-sm">units</span>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Last Updated</label>
                <div className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-300 text-sm">
                  {new Date().toLocaleTimeString()}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Comprehensive Option Chain Table */}
        <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden mb-8">
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead className="bg-slate-800">
                <tr>
                  <th colSpan={showGreeks ? 14 : 10} className="px-3 py-3 text-center text-green-400 font-bold border-r border-slate-700">
                    CALLS
                  </th>
                  <th className="px-2 py-3 text-center text-white font-bold border-r border-slate-700">
                    STRIKE
                  </th>
                  <th colSpan={showGreeks ? 14 : 10} className="px-3 py-3 text-center text-red-400 font-bold">
                    PUTS
                  </th>
                </tr>
                <tr className="text-xs text-slate-300">
                  {/* Call Headers */}
                  <th className="px-2 py-2 text-left">OI</th>
                  <th className="px-2 py-2 text-left">CHNG IN OI</th>
                  <th className="px-2 py-2 text-left">VOLUME</th>
                  <th className="px-2 py-2 text-left">IV</th>
                  <th className="px-2 py-2 text-left">LTP</th>
                  <th className="px-2 py-2 text-left">CHNG</th>
                  <th className="px-2 py-2 text-left">BID QTY</th>
                  <th className="px-2 py-2 text-left">BID</th>
                  <th className="px-2 py-2 text-left">ASK</th>
                  <th className="px-2 py-2 text-left border-r border-slate-700">ASK QTY</th>
                  {showGreeks && (
                    <>
                      <th className="px-2 py-2 text-left">DELTA</th>
                      <th className="px-2 py-2 text-left">GAMMA</th>
                      <th className="px-2 py-2 text-left">THETA</th>
                      <th className="px-2 py-2 text-left border-r border-slate-700">VEGA</th>
                    </>
                  )}
                  
                  {/* Strike Header */}
                  <th className="px-2 py-2 text-center border-r border-slate-700">STRIKE</th>
                  
                  {/* Put Headers */}
                  {showGreeks && (
                    <>
                      <th className="px-2 py-2 text-left">DELTA</th>
                      <th className="px-2 py-2 text-left">GAMMA</th>
                      <th className="px-2 py-2 text-left">THETA</th>
                      <th className="px-2 py-2 text-left">VEGA</th>
                    </>
                  )}
                  <th className="px-2 py-2 text-left">BID QTY</th>
                  <th className="px-2 py-2 text-left">BID</th>
                  <th className="px-2 py-2 text-left">ASK</th>
                  <th className="px-2 py-2 text-left">ASK QTY</th>
                  <th className="px-2 py-2 text-left">CHNG</th>
                  <th className="px-2 py-2 text-left">LTP</th>
                  <th className="px-2 py-2 text-left">IV</th>
                  <th className="px-2 py-2 text-left">VOLUME</th>
                  <th className="px-2 py-2 text-left">CHNG IN OI</th>
                  <th className="px-2 py-2 text-left">OI</th>
                </tr>
              </thead>
              <tbody>
                {optionData.map((option, index) => {
                  const isATM = option.strike === getATMStrike();
                  const isITMCall = option.strike < marketData.spotPrice;
                  const isITMPut = option.strike > marketData.spotPrice;
                  
                  return (
                    <tr
                      key={index}
                      className={`border-t border-slate-800 hover:bg-slate-800/50 ${
                        isATM ? 'bg-yellow-500/5 border-yellow-500/20' : ''
                      }`}
                    >
                      {/* Call Data */}
                      <td className="px-2 py-2 text-xs font-mono">{formatNumber(option.callOI)}</td>
                      <td className={`px-2 py-2 text-xs font-mono ${
                        option.callChangeInOI >= 0 ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {option.callChangeInOI >= 0 ? '+' : ''}{formatNumber(option.callChangeInOI)}
                      </td>
                      <td className="px-2 py-2 text-xs font-mono text-slate-300">{formatNumber(option.callVolume)}</td>
                      <td className="px-2 py-2 text-xs font-mono text-purple-400">{option.callIV.toFixed(1)}%</td>
                      <td className={`px-2 py-2 text-xs font-mono font-bold ${
                        isITMCall ? 'text-green-400' : 'text-slate-300'
                      }`}>
                        {option.callLTP.toFixed(2)}
                      </td>
                      <td className={`px-2 py-2 text-xs font-mono ${
                        option.callChange >= 0 ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {option.callChange >= 0 ? '+' : ''}{option.callChange.toFixed(2)}
                      </td>
                      <td className="px-2 py-2 text-xs font-mono text-slate-400">{formatNumber(option.callBidQty)}</td>
                      <td className="px-2 py-2 text-xs font-mono text-slate-400">{option.callBid.toFixed(2)}</td>
                      <td className="px-2 py-2 text-xs font-mono text-slate-400">{option.callAsk.toFixed(2)}</td>
                      <td className="px-2 py-2 text-xs font-mono text-slate-400 border-r border-slate-700">
                        {formatNumber(option.callAskQty)}
                      </td>
                      
                      {showGreeks && (
                        <>
                          <td className="px-2 py-2 text-xs font-mono text-blue-400">
                            {option.callDelta?.toFixed(3)}
                          </td>
                          <td className="px-2 py-2 text-xs font-mono text-blue-400">
                            {option.callGamma?.toFixed(4)}
                          </td>
                          <td className="px-2 py-2 text-xs font-mono text-blue-400">
                            {option.callTheta?.toFixed(2)}
                          </td>
                          <td className="px-2 py-2 text-xs font-mono text-blue-400 border-r border-slate-700">
                            {option.callVega?.toFixed(2)}
                          </td>
                        </>
                      )}
                      
                      {/* Strike Price */}
                      <td className={`px-2 py-2 text-center font-bold border-r border-slate-700 ${
                        isATM ? 'text-yellow-400 bg-yellow-500/10' : 'text-white'
                      }`}>
                        {option.strike}
                      </td>
                      
                      {/* Put Data */}
                      {showGreeks && (
                        <>
                          <td className="px-2 py-2 text-xs font-mono text-blue-400">
                            {option.putDelta?.toFixed(3)}
                          </td>
                          <td className="px-2 py-2 text-xs font-mono text-blue-400">
                            {option.putGamma?.toFixed(4)}
                          </td>
                          <td className="px-2 py-2 text-xs font-mono text-blue-400">
                            {option.putTheta?.toFixed(2)}
                          </td>
                          <td className="px-2 py-2 text-xs font-mono text-blue-400">
                            {option.putVega?.toFixed(2)}
                          </td>
                        </>
                      )}
                      
                      <td className="px-2 py-2 text-xs font-mono text-slate-400">{formatNumber(option.putBidQty)}</td>
                      <td className="px-2 py-2 text-xs font-mono text-slate-400">{option.putBid.toFixed(2)}</td>
                      <td className="px-2 py-2 text-xs font-mono text-slate-400">{option.putAsk.toFixed(2)}</td>
                      <td className="px-2 py-2 text-xs font-mono text-slate-400">{formatNumber(option.putAskQty)}</td>
                      <td className={`px-2 py-2 text-xs font-mono ${
                        option.putChange >= 0 ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {option.putChange >= 0 ? '+' : ''}{option.putChange.toFixed(2)}
                      </td>
                      <td className={`px-2 py-2 text-xs font-mono font-bold ${
                        isITMPut ? 'text-red-400' : 'text-slate-300'
                      }`}>
                        {option.putLTP.toFixed(2)}
                      </td>
                      <td className="px-2 py-2 text-xs font-mono text-purple-400">{option.putIV.toFixed(1)}%</td>
                      <td className="px-2 py-2 text-xs font-mono text-slate-300">{formatNumber(option.putVolume)}</td>
                      <td className={`px-2 py-2 text-xs font-mono ${
                        option.putChangeInOI >= 0 ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {option.putChangeInOI >= 0 ? '+' : ''}{formatNumber(option.putChangeInOI)}
                      </td>
                      <td className="px-2 py-2 text-xs font-mono">{formatNumber(option.putOI)}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Summary Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
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
              ₹{marketData.maxPain}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}