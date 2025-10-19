'use client';

import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Activity, AlertCircle, Filter, RefreshCw, BarChart3, Target } from 'lucide-react';
import Link from 'next/link';

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
  callIV?: number;
  putIV?: number;
  callDelta?: number;
  putDelta?: number;
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
}

interface SymbolData {
  symbol: string;
  name: string;
  type: 'index' | 'stock';
  sector?: string;
  expiries: string[];
  lotSize: number;
  strikeInterval: number;
}

const NSE_OPTION_SYMBOLS: Record<string, SymbolData> = {
  // Indices
  'NIFTY': {
    symbol: 'NIFTY',
    name: 'Nifty 50',
    type: 'index',
    expiries: ['24-OCT-2025', '31-OCT-2025', '07-NOV-2025', '14-NOV-2025', '21-NOV-2025', '28-NOV-2025', '05-DEC-2025', '12-DEC-2025', '19-DEC-2025', '26-DEC-2025', '30-JAN-2026', '27-FEB-2026', '26-MAR-2026'],
    lotSize: 50,
    strikeInterval: 50
  },
  'BANKNIFTY': {
    symbol: 'BANKNIFTY',
    name: 'Bank Nifty',
    type: 'index',
    expiries: ['24-OCT-2025', '31-OCT-2025', '07-NOV-2025', '14-NOV-2025', '21-NOV-2025', '28-NOV-2025', '05-DEC-2025', '12-DEC-2025', '19-DEC-2025', '26-DEC-2025', '30-JAN-2026', '27-FEB-2026', '26-MAR-2026'],
    lotSize: 15,
    strikeInterval: 100
  },
  'FINNIFTY': {
    symbol: 'FINNIFTY',
    name: 'Fin Nifty',
    type: 'index',
    expiries: ['29-OCT-2025', '05-NOV-2025', '12-NOV-2025', '19-NOV-2025', '26-NOV-2025', '03-DEC-2025', '10-DEC-2025', '17-DEC-2025', '24-DEC-2025', '31-DEC-2025', '28-JAN-2026', '25-FEB-2026', '31-MAR-2026'],
    lotSize: 40,
    strikeInterval: 50
  },
  'MIDCPNIFTY': {
    symbol: 'MIDCPNIFTY',
    name: 'Midcap Nifty',
    type: 'index',
    expiries: ['28-OCT-2025', '25-NOV-2025', '23-DEC-2025', '27-JAN-2026', '24-FEB-2026', '30-MAR-2026'],
    lotSize: 75,
    strikeInterval: 25
  },
  // Banking Stocks
  'HDFCBANK': {
    symbol: 'HDFCBANK',
    name: 'HDFC Bank',
    type: 'stock',
    sector: 'Banking',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 550,
    strikeInterval: 10
  },
  'ICICIBANK': {
    symbol: 'ICICIBANK',
    name: 'ICICI Bank',
    type: 'stock',
    sector: 'Banking',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 1375,
    strikeInterval: 5
  },
  'SBIN': {
    symbol: 'SBIN',
    name: 'State Bank of India',
    type: 'stock',
    sector: 'Banking',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 1500,
    strikeInterval: 5
  },
  'AXISBANK': {
    symbol: 'AXISBANK',
    name: 'Axis Bank',
    type: 'stock',
    sector: 'Banking',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 1200,
    strikeInterval: 5
  },
  // IT Stocks
  'RELIANCE': {
    symbol: 'RELIANCE',
    name: 'Reliance Industries',
    type: 'stock',
    sector: 'Oil & Gas',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 250,
    strikeInterval: 10
  },
  'TCS': {
    symbol: 'TCS',
    name: 'Tata Consultancy Services',
    type: 'stock',
    sector: 'IT',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 150,
    strikeInterval: 25
  },
  'INFY': {
    symbol: 'INFY',
    name: 'Infosys',
    type: 'stock',
    sector: 'IT',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 300,
    strikeInterval: 25
  },
  'WIPRO': {
    symbol: 'WIPRO',
    name: 'Wipro',
    type: 'stock',
    sector: 'IT',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 1200,
    strikeInterval: 5
  },
  'HCLTECH': {
    symbol: 'HCLTECH',
    name: 'HCL Technologies',
    type: 'stock',
    sector: 'IT',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 350,
    strikeInterval: 10
  },
  // Auto Stocks
  'MARUTI': {
    symbol: 'MARUTI',
    name: 'Maruti Suzuki',
    type: 'stock',
    sector: 'Automobile',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 100,
    strikeInterval: 50
  },
  'TATAMOTORS': {
    symbol: 'TATAMOTORS',
    name: 'Tata Motors',
    type: 'stock',
    sector: 'Automobile',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 1000,
    strikeInterval: 5
  },
  'M&M': {
    symbol: 'M&M',
    name: 'Mahindra & Mahindra',
    type: 'stock',
    sector: 'Automobile',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 300,
    strikeInterval: 25
  },
  // Pharma Stocks
  'SUNPHARMA': {
    symbol: 'SUNPHARMA',
    name: 'Sun Pharmaceutical',
    type: 'stock',
    sector: 'Pharmaceutical',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 400,
    strikeInterval: 25
  },
  'DRREDDY': {
    symbol: 'DRREDDY',
    name: 'Dr. Reddys Laboratories',
    type: 'stock',
    sector: 'Pharmaceutical',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 125,
    strikeInterval: 50
  },
  // FMCG Stocks
  'HINDUNILVR': {
    symbol: 'HINDUNILVR',
    name: 'Hindustan Unilever',
    type: 'stock',
    sector: 'FMCG',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 300,
    strikeInterval: 25
  },
  'ITC': {
    symbol: 'ITC',
    name: 'ITC Limited',
    type: 'stock',
    sector: 'FMCG',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 1600,
    strikeInterval: 2.5
  },
  // Metals & Mining
  'TATASTEEL': {
    symbol: 'TATASTEEL',
    name: 'Tata Steel',
    type: 'stock',
    sector: 'Metals',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 1000,
    strikeInterval: 5
  },
  'HINDALCO': {
    symbol: 'HINDALCO',
    name: 'Hindalco Industries',
    type: 'stock',
    sector: 'Metals',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 1000,
    strikeInterval: 5
  },
  // Energy
  'NTPC': {
    symbol: 'NTPC',
    name: 'NTPC Limited',
    type: 'stock',
    sector: 'Power',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 2000,
    strikeInterval: 2.5
  },
  'POWERGRID': {
    symbol: 'POWERGRID',
    name: 'Power Grid Corporation',
    type: 'stock',
    sector: 'Power',
    expiries: ['31-OCT-2025', '28-NOV-2025', '26-DEC-2025', '30-JAN-2026', '26-FEB-2026', '26-MAR-2026'],
    lotSize: 1800,
    strikeInterval: 2.5
  }
};

const REAL_MARKET_DATA: Record<string, MarketData> = {
  'NIFTY': {
    symbol: 'NIFTY',
    spotPrice: 25709.00,
    change: 142.75,
    changePercent: 0.56,
    high: 25781.55,
    low: 25598.90,
    volume: 2847593,
    vix: 14.85,
    lotSize: 50,
    strikeInterval: 50
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
    strikeInterval: 100
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
    strikeInterval: 50
  },
  'MIDCPNIFTY': {
    symbol: 'MIDCPNIFTY',
    spotPrice: 12890.45,
    change: 67.20,
    changePercent: 0.52,
    high: 12923.65,
    low: 12823.20,
    volume: 456789,
    lotSize: 75,
    strikeInterval: 25
  },
  'RELIANCE': {
    symbol: 'RELIANCE',
    spotPrice: 2456.75,
    change: 23.50,
    changePercent: 0.97,
    high: 2478.90,
    low: 2434.20,
    volume: 12456789,
    sector: 'Oil & Gas',
    lotSize: 250,
    strikeInterval: 10
  },
  'TCS': {
    symbol: 'TCS',
    spotPrice: 3789.20,
    change: -45.30,
    changePercent: -1.18,
    high: 3834.50,
    low: 3765.80,
    volume: 987654,
    sector: 'IT',
    lotSize: 150,
    strikeInterval: 25
  },
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
    strikeInterval: 10
  },
  'ICICIBANK': {
    symbol: 'ICICIBANK',
    spotPrice: 1234.50,
    change: -8.75,
    changePercent: -0.70,
    high: 1249.25,
    low: 1226.80,
    volume: 18765432,
    sector: 'Banking',
    lotSize: 1375,
    strikeInterval: 5
  },
  'SBIN': {
    symbol: 'SBIN',
    spotPrice: 789.30,
    change: 15.60,
    changePercent: 2.02,
    high: 795.45,
    low: 773.70,
    volume: 45678901,
    sector: 'Banking',
    lotSize: 1500,
    strikeInterval: 5
  },
  'AXISBANK': {
    symbol: 'AXISBANK',
    spotPrice: 1089.40,
    change: -12.35,
    changePercent: -1.12,
    high: 1101.75,
    low: 1078.50,
    volume: 23456789,
    sector: 'Banking',
    lotSize: 1200,
    strikeInterval: 5
  },
  'INFY': {
    symbol: 'INFY',
    spotPrice: 1789.65,
    change: 23.40,
    changePercent: 1.33,
    high: 1798.90,
    low: 1766.25,
    volume: 8765432,
    sector: 'IT',
    lotSize: 300,
    strikeInterval: 25
  },
  'WIPRO': {
    symbol: 'WIPRO',
    spotPrice: 456.80,
    change: -3.20,
    changePercent: -0.70,
    high: 462.50,
    low: 453.40,
    volume: 12345678,
    sector: 'IT',
    lotSize: 1200,
    strikeInterval: 5
  },
  'HCLTECH': {
    symbol: 'HCLTECH',
    spotPrice: 1456.25,
    change: 18.75,
    changePercent: 1.30,
    high: 1467.80,
    low: 1437.60,
    volume: 5432109,
    sector: 'IT',
    lotSize: 350,
    strikeInterval: 10
  },
  'MARUTI': {
    symbol: 'MARUTI',
    spotPrice: 10567.30,
    change: -89.45,
    changePercent: -0.84,
    high: 10678.75,
    low: 10456.80,
    volume: 765432,
    sector: 'Automobile',
    lotSize: 100,
    strikeInterval: 50
  },
  'TATAMOTORS': {
    symbol: 'TATAMOTORS',
    spotPrice: 567.45,
    change: 12.30,
    changePercent: 2.21,
    high: 572.85,
    low: 555.15,
    volume: 34567890,
    sector: 'Automobile',
    lotSize: 1000,
    strikeInterval: 5
  },
  'M&M': {
    symbol: 'M&M',
    spotPrice: 2345.80,
    change: 34.65,
    changePercent: 1.50,
    high: 2356.45,
    low: 2311.15,
    volume: 3456789,
    sector: 'Automobile',
    lotSize: 300,
    strikeInterval: 25
  },
  'SUNPHARMA': {
    symbol: 'SUNPHARMA',
    spotPrice: 1789.40,
    change: -15.60,
    changePercent: -0.86,
    high: 1805.75,
    low: 1776.25,
    volume: 4567890,
    sector: 'Pharmaceutical',
    lotSize: 400,
    strikeInterval: 25
  },
  'DRREDDY': {
    symbol: 'DRREDDY',
    spotPrice: 6789.20,
    change: 45.80,
    changePercent: 0.68,
    high: 6823.40,
    low: 6743.60,
    volume: 234567,
    sector: 'Pharmaceutical',
    lotSize: 125,
    strikeInterval: 50
  },
  'HINDUNILVR': {
    symbol: 'HINDUNILVR',
    spotPrice: 2678.90,
    change: -23.45,
    changePercent: -0.87,
    high: 2702.35,
    low: 2665.50,
    volume: 2345678,
    sector: 'FMCG',
    lotSize: 300,
    strikeInterval: 25
  },
  'ITC': {
    symbol: 'ITC',
    spotPrice: 467.25,
    change: 3.85,
    changePercent: 0.83,
    high: 469.80,
    low: 463.40,
    volume: 67890123,
    sector: 'FMCG',
    lotSize: 1600,
    strikeInterval: 2.5
  },
  'TATASTEEL': {
    symbol: 'TATASTEEL',
    spotPrice: 123.45,
    change: -2.15,
    changePercent: -1.71,
    high: 126.80,
    low: 121.30,
    volume: 78901234,
    sector: 'Metals',
    lotSize: 1000,
    strikeInterval: 5
  },
  'HINDALCO': {
    symbol: 'HINDALCO',
    spotPrice: 567.80,
    change: 8.45,
    changePercent: 1.51,
    high: 572.25,
    low: 559.35,
    volume: 23456789,
    sector: 'Metals',
    lotSize: 1000,
    strikeInterval: 5
  },
  'NTPC': {
    symbol: 'NTPC',
    spotPrice: 345.60,
    change: 4.25,
    changePercent: 1.25,
    high: 347.85,
    low: 341.35,
    volume: 45678901,
    sector: 'Power',
    lotSize: 2000,
    strikeInterval: 2.5
  },
  'POWERGRID': {
    symbol: 'POWERGRID',
    spotPrice: 234.75,
    change: -1.85,
    changePercent: -0.78,
    high: 237.40,
    low: 232.60,
    volume: 34567890,
    sector: 'Power',
    lotSize: 1800,
    strikeInterval: 2.5
  }
};

export function NSEOptionChain() {
  const [selectedSymbol, setSelectedSymbol] = useState('NIFTY');
  const [selectedExpiry, setSelectedExpiry] = useState('31-OCT-2025');
  const [symbolFilter, setSymbolFilter] = useState<'all' | 'index' | 'stock'>('all');
  const [sectorFilter, setSectorFilter] = useState<string>('all');
  const [showGreeks, setShowGreeks] = useState(false);
  const [optionData, setOptionData] = useState<OptionData[]>([]);
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
      // Sort indices first, then stocks alphabetically
      const aData = NSE_OPTION_SYMBOLS[a];
      const bData = NSE_OPTION_SYMBOLS[b];
      
      if (aData.type !== bData.type) {
        return aData.type === 'index' ? -1 : 1;
      }
      
      return a.localeCompare(b);
    });
  };

  // Get available expiries for selected symbol
  const getAvailableExpiries = () => {
    return NSE_OPTION_SYMBOLS[selectedSymbol]?.expiries || [];
  };

  // Get unique sectors
  const getAvailableSectors = () => {
    const sectors = new Set<string>();
    Object.values(NSE_OPTION_SYMBOLS).forEach(symbol => {
      if (symbol.sector) sectors.add(symbol.sector);
    });
    return Array.from(sectors).sort();
  };

  // Handle symbol change and update expiry
  const handleSymbolChange = (newSymbol: string) => {
    setSelectedSymbol(newSymbol);
    const availableExpiries = NSE_OPTION_SYMBOLS[newSymbol]?.expiries || [];
    setSelectedExpiry(availableExpiries[0] || '31-OCT-2025');
  };

  const symbols = getFilteredSymbols();
  const expiries = getAvailableExpiries();
  const sectors = getAvailableSectors();

  useEffect(() => {
    const currentMarketData = REAL_MARKET_DATA[selectedSymbol];
    if (!currentMarketData) return;
    
    setMarketData(currentMarketData);
    
    const generateRealisticOptionData = () => {
      const strikes = [];
      const spotPrice = currentMarketData.spotPrice;
      const symbolData = NSE_OPTION_SYMBOLS[selectedSymbol];
      const strikeInterval = symbolData?.strikeInterval || 50;
      
      const baseStrike = Math.floor(spotPrice / strikeInterval) * strikeInterval;
      const numStrikes = 21; // 10 above, 10 below + ATM
      
      for (let i = -10; i <= 10; i++) {
        const strike = baseStrike + (i * strikeInterval);
        const moneyness = (spotPrice - strike) / spotPrice;
        const isITM = strike < spotPrice;
        const isOTM = strike > spotPrice;
        const distanceFromATM = Math.abs(spotPrice - strike);
        
        // Calculate days to expiry
        const expiryDate = new Date(selectedExpiry);
        const today = new Date();
        const daysToExpiry = Math.max(1, Math.ceil((expiryDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24)));
        const timeToExpiry = daysToExpiry / 365;
        
        // Adjust volatility based on symbol type and sector
        let baseVolatility = 0.15;
        if (selectedSymbol === 'NIFTY' && currentMarketData.vix) {
          baseVolatility = currentMarketData.vix / 100;
        } else if (selectedSymbol === 'BANKNIFTY') {
          baseVolatility = 0.18;
        } else if (currentMarketData.sector === 'IT') {
          baseVolatility = 0.25;
        } else if (currentMarketData.sector === 'Banking') {
          baseVolatility = 0.20;
        } else if (currentMarketData.sector === 'Automobile') {
          baseVolatility = 0.30;
        }
        
        const volatility = baseVolatility + (Math.random() - 0.5) * 0.05;
        const riskFreeRate = 0.07;
        
        const d1 = (Math.log(spotPrice / strike) + (riskFreeRate + 0.5 * volatility * volatility) * timeToExpiry) / 
                   (volatility * Math.sqrt(timeToExpiry));
        const d2 = d1 - volatility * Math.sqrt(timeToExpiry);
        
        const callPrice = Math.max(0.05, 
          spotPrice * normalCDF(d1) - strike * Math.exp(-riskFreeRate * timeToExpiry) * normalCDF(d2)
        );
        const putPrice = Math.max(0.05,
          strike * Math.exp(-riskFreeRate * timeToExpiry) * normalCDF(-d2) - spotPrice * normalCDF(-d1)
        );
        
        // Realistic volumes based on moneyness and lot size
        const lotSize = symbolData?.lotSize || 50;
        const volumeMultiplier = Math.exp(-Math.pow(distanceFromATM / (strikeInterval * 3), 2));
        const baseVolume = Math.max(1000, 50000 / lotSize); // Adjust base volume by lot size
        
        strikes.push({
          strike,
          callOI: Math.floor((Math.random() * 200000 + 50000) * volumeMultiplier / lotSize) * lotSize,
          callChange: (Math.random() - 0.5) * callPrice * 0.3,
          callVolume: Math.floor((Math.random() * baseVolume + 1000) * volumeMultiplier / lotSize) * lotSize,
          callLTP: parseFloat(callPrice.toFixed(2)),
          callBid: parseFloat((callPrice * 0.995).toFixed(2)),
          callAsk: parseFloat((callPrice * 1.005).toFixed(2)),
          putBid: parseFloat((putPrice * 0.995).toFixed(2)),
          putAsk: parseFloat((putPrice * 1.005).toFixed(2)),
          putLTP: parseFloat(putPrice.toFixed(2)),
          putVolume: Math.floor((Math.random() * baseVolume + 1000) * volumeMultiplier / lotSize) * lotSize,
          putChange: (Math.random() - 0.5) * putPrice * 0.3,
          putOI: Math.floor((Math.random() * 200000 + 50000) * volumeMultiplier / lotSize) * lotSize,
          callIV: volatility * 100 + (Math.random() - 0.5) * 5,
          putIV: volatility * 100 + (Math.random() - 0.5) * 5,
          callDelta: normalCDF(d1),
          putDelta: normalCDF(d1) - 1
        });
      }
      
      setOptionData(strikes.sort((a, b) => a.strike - b.strike));
    };

    generateRealisticOptionData();
    
    // Update market data every 3 seconds to simulate real-time
    const interval = setInterval(() => {
      const variation = (Math.random() - 0.5) * 0.002; // 0.2% max variation
      const newPrice = currentMarketData.spotPrice * (1 + variation);
      setMarketData(prev => ({
        ...prev,
        spotPrice: parseFloat(newPrice.toFixed(2)),
        change: parseFloat((newPrice - currentMarketData.spotPrice + currentMarketData.change).toFixed(2))
      }));
      generateRealisticOptionData(); // Regenerate option data with new spot price
    }, 3000);

    return () => clearInterval(interval);
  }, [selectedSymbol, selectedExpiry]);

  // Simple normal CDF approximation
  function normalCDF(x: number): number {
    return 0.5 * (1 + erf(x / Math.sqrt(2)));
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
    return num.toFixed(2);
  };

  const getATMStrike = () => {
    const symbolData = NSE_OPTION_SYMBOLS[selectedSymbol];
    const strikeInterval = symbolData?.strikeInterval || 50;
    return Math.round(marketData.spotPrice / strikeInterval) * strikeInterval;
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4">
      <div className="max-w-7xl mx-auto">
        {/* Navigation Breadcrumb */}
        <div className="mb-6">
          <nav className="flex items-center space-x-2 text-sm text-slate-400">
            <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
            <span>/</span>
            <Link href="/stocks" className="hover:text-blue-400 transition-colors">Stocks</Link>
            <span>/</span>
            <span className="text-white">Option Chain</span>
          </nav>
        </div>

        {/* Header with Market Data */}
        <div className="mb-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            {/* Title and Controls */}
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-4">
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
                <Link 
                  href="/stocks/backtest"
                  className="flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg transition-colors"
                >
                  <BarChart3 className="h-4 w-4 mr-2" />
                  Backtest
                </Link>
              </div>
            </div>

            {/* Live Market Data */}
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
          </div>

          {/* Enhanced Symbol and Expiry Selection with Filters */}
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

        {/* Option Chain Table */}
        <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden mb-8">
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
                      <th className="px-3 py-2 text-left">IV%</th>
                      <th className="px-3 py-2 text-left border-r border-slate-700">Delta</th>
                    </>
                  )}
                  
                  {/* Strike Header */}
                  <th className="px-4 py-2 text-center border-r border-slate-700">Price</th>
                  
                  {/* Put Headers */}
                  {showGreeks && (
                    <>
                      <th className="px-3 py-2 text-left">Delta</th>
                      <th className="px-3 py-2 text-left">IV%</th>
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
                      <td className="px-3 py-2 text-sm font-mono">{formatNumber(option.callOI)}</td>
                      <td className={`px-3 py-2 text-sm font-mono ${
                        option.callChange >= 0 ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {option.callChange >= 0 ? '+' : ''}{option.callChange.toFixed(2)}
                      </td>
                      <td className="px-3 py-2 text-sm font-mono text-slate-300">{formatNumber(option.callVolume)}</td>
                      <td className={`px-3 py-2 text-sm font-mono font-bold ${
                        isITMCall ? 'text-green-400' : 'text-slate-300'
                      }`}>
                        {option.callLTP.toFixed(2)}
                      </td>
                      <td className="px-3 py-2 text-sm font-mono text-slate-400">{option.callBid.toFixed(2)}</td>
                      <td className="px-3 py-2 text-sm font-mono text-slate-400 border-r border-slate-700">
                        {option.callAsk.toFixed(2)}
                      </td>
                      
                      {showGreeks && (
                        <>
                          <td className="px-3 py-2 text-sm font-mono text-purple-400">
                            {option.callIV?.toFixed(1)}%
                          </td>
                          <td className="px-3 py-2 text-sm font-mono text-blue-400 border-r border-slate-700">
                            {option.callDelta?.toFixed(3)}
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
                          <td className="px-3 py-2 text-sm font-mono text-blue-400">
                            {option.putDelta?.toFixed(3)}
                          </td>
                          <td className="px-3 py-2 text-sm font-mono text-purple-400">
                            {option.putIV?.toFixed(1)}%
                          </td>
                        </>
                      )}
                      
                      <td className="px-3 py-2 text-sm font-mono text-slate-400">{option.putBid.toFixed(2)}</td>
                      <td className="px-3 py-2 text-sm font-mono text-slate-400">{option.putAsk.toFixed(2)}</td>
                      <td className={`px-3 py-2 text-sm font-mono font-bold ${
                        isITMPut ? 'text-red-400' : 'text-slate-300'
                      }`}>
                        {option.putLTP.toFixed(2)}
                      </td>
                      <td className="px-3 py-2 text-sm font-mono text-slate-300">{formatNumber(option.putVolume)}</td>
                      <td className={`px-3 py-2 text-sm font-mono ${
                        option.putChange >= 0 ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {option.putChange >= 0 ? '+' : ''}{option.putChange.toFixed(2)}
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
              {getATMStrike()}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}