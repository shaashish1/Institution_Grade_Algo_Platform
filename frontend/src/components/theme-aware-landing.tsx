'use client';

import React, { useState, useEffect } from 'react';
import { useTheme } from './theme/theme-provider';
import { ThemeSwitcher } from './theme/theme-switcher';
import { PricingSection } from './sections/pricing-section';
import { Footer } from './layout/footer';
import { SEBIWarning } from './compliance/sebi-warning';
import { MegaMenu } from './layout/mega-menu';

// Theme-specific imports
import { CosmicBackground } from './theme/cosmic-components';

// Placeholder components
const CosmicHeroSection = () => <div>Cosmic Hero Section</div>;
const HeroSection = () => <div>Hero Section</div>;

export function ThemeAwareLandingPage() {
  const { theme } = useTheme();
  const [activeMarketTab, setActiveMarketTab] = useState<'crypto' | 'nse'>('crypto');
  const [cryptoData, setCryptoData] = useState<any[]>([]);
  const [nseData, setNseData] = useState<any[]>([]);
  const [loadingCrypto, setLoadingCrypto] = useState(false);
  const [loadingNSE, setLoadingNSE] = useState(false);

  // Fetch crypto data
  useEffect(() => {
    const fetchCryptoData = async () => {
      setLoadingCrypto(true);
      try {
        const response = await fetch('https://api.coingecko.com/api/v3/markets?vs_currency=inr&order=market_cap_desc&per_page=8&sparkline=false');
        const data = await response.json();
        // Ensure data is always an array
        setCryptoData(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error('Error fetching crypto data:', error);
        // Fallback data
        setCryptoData([
          { id: 'bitcoin', symbol: 'btc', name: 'Bitcoin', current_price: 5800000, price_change_percentage_24h: 2.5, market_cap_rank: 1 },
          { id: 'ethereum', symbol: 'eth', name: 'Ethereum', current_price: 290000, price_change_percentage_24h: 3.2, market_cap_rank: 2 },
          { id: 'solana', symbol: 'sol', name: 'Solana', current_price: 18000, price_change_percentage_24h: -1.5, market_cap_rank: 5 },
          { id: 'cardano', symbol: 'ada', name: 'Cardano', current_price: 1200, price_change_percentage_24h: 1.8, market_cap_rank: 4 },
          { id: 'ripple', symbol: 'xrp', name: 'Ripple', current_price: 3500, price_change_percentage_24h: -0.5, market_cap_rank: 6 },
          { id: 'polkadot', symbol: 'dot', name: 'Polkadot', current_price: 1850, price_change_percentage_24h: 2.2, market_cap_rank: 11 },
          { id: 'dogecoin', symbol: 'doge', name: 'Dogecoin', current_price: 850, price_change_percentage_24h: 5.1, market_cap_rank: 10 },
          { id: 'litecoin', symbol: 'ltc', name: 'Litecoin', current_price: 12000, price_change_percentage_24h: -1.2, market_cap_rank: 21 },
        ]);
      }
      setLoadingCrypto(false);
    };
    fetchCryptoData();
  }, []);

  // Fetch NSE stock data
  useEffect(() => {
    const fetchNSEData = async () => {
      setLoadingNSE(true);
      try {
        // Using mock data for NSE stocks since real-time NSE API requires authentication
        setNseData([
          { symbol: 'RELIANCE', name: 'Reliance Industries', price: 2850, change: 1.2, changePercent: 0.04 },
          { symbol: 'TCS', name: 'Tata Consultancy Services', price: 3650, change: -25, changePercent: -0.68 },
          { symbol: 'INFY', name: 'Infosys', price: 1520, change: 15, changePercent: 0.99 },
          { symbol: 'HDFC', name: 'HDFC Bank', price: 1880, change: -10, changePercent: -0.53 },
          { symbol: 'MARUTI', name: 'Maruti Suzuki', price: 12450, change: 250, changePercent: 2.05 },
          { symbol: 'WIPRO', name: 'Wipro', price: 485, change: 8, changePercent: 1.67 },
        ]);
      } catch (error) {
        console.error('Error fetching NSE data:', error);
      }
      setLoadingNSE(false);
    };
    fetchNSEData();
  }, []);

  // Theme-specific classes
  const getBackgroundClass = () => {
    switch (theme) {
      case 'light':
        return 'min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50 text-slate-900';
      case 'dark':
        return 'min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-blue-950 text-white';
      case 'cosmic':
        return 'min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-indigo-950 text-white relative overflow-hidden';
      case 'doodle':
        return 'min-h-screen bg-gradient-to-br from-purple-900 via-indigo-900 to-pink-900 text-white relative overflow-hidden';
      default:
        return 'min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-blue-950 text-white';
    }
  };

  const getCardClasses = () => {
    switch (theme) {
      case 'light':
        return 'bg-white/90 border-slate-200 backdrop-blur-sm';
      case 'cosmic':
        return 'bg-slate-900/60 border-purple-500/30 backdrop-blur-md';
      case 'doodle':
        return 'bg-white/10 border-white/20 backdrop-blur-md';
      default:
        return 'bg-slate-800/70 border-slate-700 backdrop-blur-sm';
    }
  };

  const getTextClasses = () => {
    if (theme === 'light') {
      return { primary: 'text-slate-900', secondary: 'text-slate-600', accent: 'text-blue-600' };
    }
    return { primary: 'text-white', secondary: 'text-slate-300', accent: 'text-cyan-400' };
  };

  const textClasses = getTextClasses();

  return (
    <div className={getBackgroundClass()}>
      {/* Theme Background */}
      {theme === 'cosmic' && <CosmicBackground theme={theme} />}
      
      <div className="theme-switcher fixed top-6 right-6 z-[9998] pointer-events-auto">
        <ThemeSwitcher />
      </div>

      <SEBIWarning />
      <MegaMenu />
      
      <main className="relative z-10">
        {/* Professional Hero Section */}
        <section className="pt-20 pb-16 px-6">
          <div className="max-w-6xl mx-auto text-center">
            <h1 className={`text-5xl md:text-7xl font-bold mb-6 ${textClasses.primary}`}>
              Algorithmic Trading
              <br />
              <span className={textClasses.accent}>Reimagined</span>
            </h1>
            <p className={`text-xl md:text-2xl mb-8 ${textClasses.secondary} max-w-3xl mx-auto`}>
              Execute lightning-fast trades. Analyze market trends. Maximize profits. 
              All powered by cutting-edge AI and machine learning algorithms.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
              <button className="bg-gradient-to-r from-cyan-500 to-blue-600 text-white px-8 py-4 rounded-lg font-bold hover:shadow-lg hover:shadow-cyan-500/50 transition-all duration-300 hover:scale-105">
                Start Trading Now →
              </button>
              <button className={`border-2 ${theme === 'light' ? 'border-blue-600 text-blue-600 hover:bg-blue-50' : 'border-cyan-400 text-cyan-400 hover:bg-white/10'} px-8 py-4 rounded-lg font-bold transition-all duration-300 hover:scale-105`}>
                View Demo
              </button>
            </div>

            {/* Key Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
              <div className={`${getCardClasses()} border p-6 rounded-lg`}>
                <div className={`text-3xl font-bold mb-2 ${textClasses.accent}`}>$5.2B</div>
                <div className={textClasses.secondary}>Total Volume</div>
              </div>
              <div className={`${getCardClasses()} border p-6 rounded-lg`}>
                <div className={`text-3xl font-bold mb-2 ${textClasses.accent}`}>50K+</div>
                <div className={textClasses.secondary}>Active Traders</div>
              </div>
              <div className={`${getCardClasses()} border p-6 rounded-lg`}>
                <div className={`text-3xl font-bold mb-2 ${textClasses.accent}`}>99.99%</div>
                <div className={textClasses.secondary}>Uptime</div>
              </div>
              <div className={`${getCardClasses()} border p-6 rounded-lg`}>
                <div className={`text-3xl font-bold mb-2 ${textClasses.accent}`}>24/7</div>
                <div className={textClasses.secondary}>Support</div>
              </div>
            </div>
          </div>
        </section>

        {/* Market Data Section */}
        <section className="py-16 px-6 border-y border-white/10">
          <div className="max-w-6xl mx-auto">
            <h2 className={`text-3xl md:text-4xl font-bold mb-8 text-center ${textClasses.primary}`}>
              Live Market Data
            </h2>
            
            {/* Tab Navigation */}
            <div className="flex justify-center gap-4 mb-8">
              <button
                onClick={() => setActiveMarketTab('crypto')}
                className={`px-6 py-3 rounded-lg font-semibold transition-all duration-300 ${
                  activeMarketTab === 'crypto'
                    ? `${textClasses.accent} border-b-2 border-cyan-500`
                    : `${textClasses.secondary} hover:${textClasses.primary}`
                }`}
              >
                🪙 Cryptocurrency
              </button>
              <button
                onClick={() => setActiveMarketTab('nse')}
                className={`px-6 py-3 rounded-lg font-semibold transition-all duration-300 ${
                  activeMarketTab === 'nse'
                    ? `${textClasses.accent} border-b-2 border-cyan-500`
                    : `${textClasses.secondary} hover:${textClasses.primary}`
                }`}
              >
                📈 NSE Stocks
              </button>
            </div>

            {/* Crypto Data Table */}
            {activeMarketTab === 'crypto' && (
              <div className={`${getCardClasses()} border rounded-lg overflow-hidden`}>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className={theme === 'light' ? 'bg-slate-100' : 'bg-slate-800/50'}>
                      <tr>
                        <th className={`px-6 py-4 text-left font-semibold ${textClasses.secondary}`}>Asset</th>
                        <th className={`px-6 py-4 text-right font-semibold ${textClasses.secondary}`}>Price (INR)</th>
                        <th className={`px-6 py-4 text-right font-semibold ${textClasses.secondary}`}>24h Change</th>
                        <th className={`px-6 py-4 text-right font-semibold ${textClasses.secondary}`}>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Array.isArray(cryptoData) && cryptoData.length > 0 ? (
                        cryptoData.slice(0, 8).map((crypto, idx) => (
                          <tr key={idx} className={`border-t ${theme === 'light' ? 'border-slate-200 hover:bg-slate-50' : 'border-white/10 hover:bg-white/5'} transition-colors`}>
                            <td className={`px-6 py-4 font-semibold ${textClasses.primary}`}>
                              {crypto.name}
                              <span className={`ml-2 text-xs ${textClasses.secondary}`}>({crypto.symbol?.toUpperCase()})</span>
                            </td>
                            <td className={`px-6 py-4 text-right ${textClasses.primary}`}>
                              ₹{(crypto.current_price || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                            </td>
                            <td className={`px-6 py-4 text-right font-semibold ${
                              (crypto.price_change_percentage_24h || 0) >= 0 ? 'text-green-500' : 'text-red-500'
                            }`}>
                              {(crypto.price_change_percentage_24h || 0).toFixed(2)}%
                            </td>
                            <td className="px-6 py-4 text-right">
                              <button className="bg-cyan-600 hover:bg-cyan-700 text-white px-3 py-1 rounded text-xs font-semibold transition-colors">
                                Trade
                              </button>
                            </td>
                          </tr>
                        ))
                      ) : (
                        <tr>
                          <td colSpan={4} className={`px-6 py-4 text-center ${textClasses.secondary}`}>
                            Loading crypto data...
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* NSE Stocks Table */}
            {activeMarketTab === 'nse' && (
              <div className={`${getCardClasses()} border rounded-lg overflow-hidden`}>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className={theme === 'light' ? 'bg-slate-100' : 'bg-slate-800/50'}>
                      <tr>
                        <th className={`px-6 py-4 text-left font-semibold ${textClasses.secondary}`}>Company</th>
                        <th className={`px-6 py-4 text-right font-semibold ${textClasses.secondary}`}>Price (₹)</th>
                        <th className={`px-6 py-4 text-right font-semibold ${textClasses.secondary}`}>Change</th>
                        <th className={`px-6 py-4 text-right font-semibold ${textClasses.secondary}`}>% Change</th>
                        <th className={`px-6 py-4 text-right font-semibold ${textClasses.secondary}`}>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Array.isArray(nseData) && nseData.length > 0 ? (
                        nseData.map((stock, idx) => (
                          <tr key={idx} className={`border-t ${theme === 'light' ? 'border-slate-200 hover:bg-slate-50' : 'border-white/10 hover:bg-white/5'} transition-colors`}>
                            <td className={`px-6 py-4 font-semibold ${textClasses.primary}`}>
                              {stock.name}
                              <span className={`ml-2 text-xs ${textClasses.secondary}`}>{stock.symbol}</span>
                            </td>
                            <td className={`px-6 py-4 text-right ${textClasses.primary}`}>
                              ₹{stock.price.toLocaleString()}
                            </td>
                            <td className={`px-6 py-4 text-right font-semibold ${stock.change >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                              {stock.change >= 0 ? '+' : ''}{stock.change}
                            </td>
                            <td className={`px-6 py-4 text-right font-semibold ${stock.changePercent >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                              {stock.changePercent >= 0 ? '+' : ''}{stock.changePercent.toFixed(2)}%
                            </td>
                            <td className="px-6 py-4 text-right">
                              <button className="bg-cyan-600 hover:bg-cyan-700 text-white px-3 py-1 rounded text-xs font-semibold transition-colors">
                                Trade
                              </button>
                            </td>
                          </tr>
                        ))
                      ) : (
                        <tr>
                          <td colSpan={5} className={`px-6 py-4 text-center ${textClasses.secondary}`}>
                            Loading NSE data...
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        </section>

        {/* Features Section */}
        <section className="py-16 px-6">
          <div className="max-w-6xl mx-auto">
            <h2 className={`text-3xl md:text-4xl font-bold mb-12 text-center ${textClasses.primary}`}>
              Why Choose AlgoProject?
            </h2>
            
            <div className="grid md:grid-cols-3 gap-8">
              {[
                { icon: '⚡', title: 'Sub-Millisecond Execution', desc: 'Trade faster than your competition with our optimized trading engine.' },
                { icon: '🤖', title: 'AI-Powered Strategies', desc: 'Leverage machine learning to identify profitable opportunities 24/7.' },
                { icon: '📊', title: 'Advanced Analytics', desc: 'Real-time charts, technical indicators, and predictive models.' },
                { icon: '🔒', title: 'Bank-Grade Security', desc: 'Enterprise-level encryption and compliance with all regulations.' },
                { icon: '📱', title: 'Desktop & Mobile', desc: 'Trade anywhere with our responsive, professional platforms.' },
                { icon: '🎓', title: 'Expert Education', desc: 'Learn from industry professionals with our comprehensive tutorials.' },
              ].map((feature, idx) => (
                <div key={idx} className={`${getCardClasses()} border p-8 rounded-lg hover:shadow-lg transition-all duration-300 hover:-translate-y-1`}>
                  <div className="text-4xl mb-4">{feature.icon}</div>
                  <h3 className={`text-xl font-bold mb-3 ${textClasses.primary}`}>{feature.title}</h3>
                  <p className={textClasses.secondary}>{feature.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Pricing Section */}
        <PricingSection />
      </main>
      
      <Footer />
    </div>
  );
}