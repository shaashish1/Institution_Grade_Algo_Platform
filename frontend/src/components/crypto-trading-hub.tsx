'use client';

import React, { useState, useEffect } from 'react';
import { Bitcoin, TrendingUp, TrendingDown, Activity, RefreshCw, ArrowUpDown, Zap, BarChart3 } from 'lucide-react';
import Link from 'next/link';

interface CryptoPair {
  symbol: string;
  baseAsset: string;
  quoteAsset: string;
  price: number;
  change24h: number;
  volume24h: number;
  high24h: number;
  low24h: number;
  exchange: 'delta' | 'binance';
}

interface OrderBookEntry {
  price: number;
  quantity: number;
  total: number;
}

export function CryptoTradingHub() {
  const [selectedExchange, setSelectedExchange] = useState<'delta' | 'binance'>('delta');
  const [selectedPair, setSelectedPair] = useState('BTC/INR');
  const [cryptoData, setCryptoData] = useState<CryptoPair[]>([]);
  const [orderBook, setOrderBook] = useState<{bids: OrderBookEntry[], asks: OrderBookEntry[]}>({
    bids: [],
    asks: []
  });

  const deltaExchangePairs = [
    'BTC/INR', 'ETH/INR', 'BNB/INR', 'ADA/INR', 'DOT/INR', 'SOL/INR',
    'MATIC/INR', 'LINK/INR', 'UNI/INR', 'AVAX/INR'
  ];

  const binancePairs = [
    'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'DOT/USDT', 'SOL/USDT',
    'ETH/BTC', 'ADA/BTC', 'DOT/BTC', 'LINK/BTC'
  ];

  useEffect(() => {
    const generateCryptoData = () => {
      const pairs = selectedExchange === 'delta' ? deltaExchangePairs : binancePairs;
      const isINR = selectedExchange === 'delta';
      
      const mockData: CryptoPair[] = pairs.map(pair => {
        const [base, quote] = pair.split('/');
        const basePrice = base === 'BTC' ? (isINR ? 3645000 : 43250) :
                         base === 'ETH' ? (isINR ? 178000 : 2156) :
                         base === 'BNB' ? (isINR ? 25000 : 310) :
                         base === 'ADA' ? (isINR ? 28 : 0.34) :
                         (isINR ? 500 : 6.5);
        
        return {
          symbol: pair,
          baseAsset: base,
          quoteAsset: quote,
          price: basePrice * (0.95 + Math.random() * 0.1),
          change24h: (Math.random() - 0.5) * 10,
          volume24h: Math.random() * 1000000000,
          high24h: basePrice * (1.02 + Math.random() * 0.05),
          low24h: basePrice * (0.95 + Math.random() * 0.03),
          exchange: selectedExchange
        };
      });
      
      setCryptoData(mockData);
    };

    const generateOrderBook = () => {
      const bids: OrderBookEntry[] = [];
      const asks: OrderBookEntry[] = [];
      const basePrice = selectedPair.includes('BTC') ? 
        (selectedExchange === 'delta' ? 3645000 : 43250) : 2156;
      
      for (let i = 0; i < 10; i++) {
        const bidPrice = basePrice * (0.999 - i * 0.0001);
        const askPrice = basePrice * (1.001 + i * 0.0001);
        const bidQty = Math.random() * 5 + 0.1;
        const askQty = Math.random() * 5 + 0.1;
        
        bids.push({
          price: bidPrice,
          quantity: bidQty,
          total: bidPrice * bidQty
        });
        
        asks.push({
          price: askPrice,
          quantity: askQty,
          total: askPrice * askQty
        });
      }
      
      setOrderBook({ bids, asks });
    };

    generateCryptoData();
    generateOrderBook();
    
    const interval = setInterval(() => {
      generateCryptoData();
      generateOrderBook();
    }, 3000);

    return () => clearInterval(interval);
  }, [selectedExchange, selectedPair]);

  const formatPrice = (price: number, pair: string) => {
    if (pair.includes('INR')) {
      return `₹${price.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }
    return `$${price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 4 })}`;
  };

  const formatVolume = (volume: number) => {
    if (volume >= 1000000000) return `₹${(volume / 1000000000).toFixed(1)}B`;
    if (volume >= 1000000) return `₹${(volume / 1000000).toFixed(1)}M`;
    if (volume >= 1000) return `₹${(volume / 1000).toFixed(1)}K`;
    return volume.toFixed(2);
  };

  const selectedPairData = cryptoData.find(pair => pair.symbol === selectedPair);

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4">
      <div className="max-w-7xl mx-auto">
        {/* Navigation Breadcrumb */}
        <div className="mb-6">
          <nav className="flex items-center space-x-2 text-sm text-slate-400">
            <Link href="/" className="hover:text-orange-400 transition-colors">Home</Link>
            <span>/</span>
            <span className="text-white">Crypto Trading</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-3xl font-bold flex items-center">
              <Bitcoin className="h-8 w-8 text-orange-400 mr-3" />
              <span className="bg-gradient-to-r from-orange-400 to-purple-400 bg-clip-text text-transparent">
                Crypto Trading Hub
              </span>
            </h1>
            
            <div className="flex items-center gap-4">
              <Link 
                href="/crypto/backtest"
                className="flex items-center px-4 py-2 bg-gradient-to-r from-orange-600 to-yellow-600 hover:from-orange-700 hover:to-yellow-700 rounded-lg transition-colors font-medium"
              >
                <BarChart3 className="h-4 w-4 mr-2" />
                Backtest
              </Link>
              <button className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors">
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh
              </button>
            </div>
          </div>

          {/* Exchange Selector */}
          <div className="flex gap-4 mb-6">
            <button
              onClick={() => {
                setSelectedExchange('delta');
                setSelectedPair('BTC/INR');
              }}
              className={`flex items-center px-6 py-3 rounded-xl font-semibold transition-all ${
                selectedExchange === 'delta'
                  ? 'bg-gradient-to-r from-green-600 to-blue-600 text-white shadow-lg'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center mr-3 text-white font-bold text-sm">
                Δ
              </div>
              <div>
                <div className="text-left">Delta Exchange</div>
                <div className="text-xs opacity-75">Indian Exchange • INR Pairs</div>
              </div>
            </button>
            
            <button
              onClick={() => {
                setSelectedExchange('binance');
                setSelectedPair('BTC/USDT');
              }}
              className={`flex items-center px-6 py-3 rounded-xl font-semibold transition-all ${
                selectedExchange === 'binance'
                  ? 'bg-gradient-to-r from-yellow-600 to-orange-600 text-white shadow-lg'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              <div className="w-8 h-8 bg-yellow-500 rounded-full flex items-center justify-center mr-3 text-black font-bold text-sm">
                B
              </div>
              <div>
                <div className="text-left">Binance</div>
                <div className="text-xs opacity-75">Global Exchange • USD Pairs</div>
              </div>
            </button>
          </div>
        </div>

        {/* Trading Interface */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Market Data & Pairs */}
          <div className="lg:col-span-2">
            {/* Selected Pair Info */}
            {selectedPairData && (
              <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800 mb-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center">
                    <div className="text-3xl mr-4">
                      {selectedPairData.baseAsset === 'BTC' ? '₿' : 
                       selectedPairData.baseAsset === 'ETH' ? 'Ξ' : '🔗'}
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold">{selectedPairData.symbol}</h3>
                      <p className="text-slate-400 capitalize">{selectedExchange} Exchange</p>
                    </div>
                  </div>
                  
                  <div className="text-right">
                    <div className="text-3xl font-bold">
                      {formatPrice(selectedPairData.price, selectedPairData.symbol)}
                    </div>
                    <div className={`text-lg font-medium flex items-center justify-end ${
                      selectedPairData.change24h >= 0 ? 'text-green-400' : 'text-red-400'
                    }`}>
                      {selectedPairData.change24h >= 0 ? 
                        <TrendingUp className="h-5 w-5 mr-1" /> : 
                        <TrendingDown className="h-5 w-5 mr-1" />
                      }
                      {selectedPairData.change24h >= 0 ? '+' : ''}{selectedPairData.change24h.toFixed(2)}%
                    </div>
                  </div>
                </div>
                
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="text-slate-400">24h High</span>
                    <div className="font-semibold text-green-400">
                      {formatPrice(selectedPairData.high24h, selectedPairData.symbol)}
                    </div>
                  </div>
                  <div>
                    <span className="text-slate-400">24h Low</span>
                    <div className="font-semibold text-red-400">
                      {formatPrice(selectedPairData.low24h, selectedPairData.symbol)}
                    </div>
                  </div>
                  <div>
                    <span className="text-slate-400">24h Volume</span>
                    <div className="font-semibold text-blue-400">
                      {formatVolume(selectedPairData.volume24h)}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Pair Selection */}
            <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <Activity className="h-5 w-5 mr-2 text-blue-400" />
                Available Pairs
              </h3>
              
              <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                {(selectedExchange === 'delta' ? deltaExchangePairs : binancePairs).map(pair => (
                  <button
                    key={pair}
                    onClick={() => setSelectedPair(pair)}
                    className={`p-3 rounded-lg text-left transition-all ${
                      selectedPair === pair
                        ? 'bg-blue-600 text-white'
                        : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                    }`}
                  >
                    <div className="font-semibold">{pair}</div>
                    <div className="text-xs opacity-75">
                      {cryptoData.find(c => c.symbol === pair)?.change24h.toFixed(2)}%
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Order Book */}
          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <h3 className="text-xl font-semibold mb-4 flex items-center">
              <ArrowUpDown className="h-5 w-5 mr-2 text-purple-400" />
              Order Book
            </h3>
            
            <div className="space-y-4">
              {/* Asks */}
              <div>
                <div className="text-sm text-red-400 font-medium mb-2">ASKS</div>
                <div className="space-y-1">
                  {orderBook.asks.slice(0, 5).map((ask, index) => (
                    <div key={index} className="flex justify-between text-xs">
                      <span className="text-red-400 font-mono">
                        {formatPrice(ask.price, selectedPair)}
                      </span>
                      <span className="text-slate-400 font-mono">
                        {ask.quantity.toFixed(4)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Spread */}
              <div className="border-t border-slate-700 pt-2">
                <div className="text-center text-slate-400 text-xs">
                  Spread: {selectedPairData && formatPrice(
                    orderBook.asks[0]?.price - orderBook.bids[0]?.price || 0,
                    selectedPair
                  )}
                </div>
              </div>

              {/* Bids */}
              <div>
                <div className="text-sm text-green-400 font-medium mb-2">BIDS</div>
                <div className="space-y-1">
                  {orderBook.bids.slice(0, 5).map((bid, index) => (
                    <div key={index} className="flex justify-between text-xs">
                      <span className="text-green-400 font-mono">
                        {formatPrice(bid.price, selectedPair)}
                      </span>
                      <span className="text-slate-400 font-mono">
                        {bid.quantity.toFixed(4)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Quick Trade */}
            <div className="mt-6 pt-6 border-t border-slate-700">
              <div className="grid grid-cols-2 gap-2">
                <button className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-semibold transition-colors">
                  Quick Buy
                </button>
                <button className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-semibold transition-colors">
                  Quick Sell
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Exchange Features */}
        <div className="grid md:grid-cols-2 gap-8 mt-8">
          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <div className="flex items-center mb-4">
              <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center mr-3 text-white font-bold">
                Δ
              </div>
              <h3 className="text-xl font-semibold">Delta Exchange Features</h3>
            </div>
            <ul className="space-y-2 text-slate-300">
              <li className="flex items-center">
                <Zap className="h-4 w-4 text-green-400 mr-2" />
                INR trading pairs (No conversion needed)
              </li>
              <li className="flex items-center">
                <Zap className="h-4 w-4 text-green-400 mr-2" />
                Indian regulatory compliance
              </li>
              <li className="flex items-center">
                <Zap className="h-4 w-4 text-green-400 mr-2" />
                Low fees for Indian users
              </li>
              <li className="flex items-center">
                <Zap className="h-4 w-4 text-green-400 mr-2" />
                Futures and perpetual contracts
              </li>
            </ul>
          </div>

          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <div className="flex items-center mb-4">
              <div className="w-10 h-10 bg-yellow-500 rounded-full flex items-center justify-center mr-3 text-black font-bold">
                B
              </div>
              <h3 className="text-xl font-semibold">Binance Features</h3>
            </div>
            <ul className="space-y-2 text-slate-300">
              <li className="flex items-center">
                <Zap className="h-4 w-4 text-yellow-400 mr-2" />
                World's largest crypto exchange
              </li>
              <li className="flex items-center">
                <Zap className="h-4 w-4 text-yellow-400 mr-2" />
                Highest liquidity and volume
              </li>
              <li className="flex items-center">
                <Zap className="h-4 w-4 text-yellow-400 mr-2" />
                500+ trading pairs available
              </li>
              <li className="flex items-center">
                <Zap className="h-4 w-4 text-yellow-400 mr-2" />
                Advanced trading features
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}