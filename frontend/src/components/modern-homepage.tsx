'use client';

import React, { useState, useEffect } from 'react';
import { ArrowRight, TrendingUp, BarChart3, Zap, Shield, Target, Play, ChevronRight, Star, Award } from 'lucide-react';
import Link from 'next/link';

interface PricingTier {
  name: string;
  price: string;
  period: string;
  features: string[];
  popular?: boolean;
  cta: string;
}

export default function ModernHomepage() {
  const [activeTab, setActiveTab] = useState<'stocks' | 'crypto'>('stocks');
  const [currentSlide, setCurrentSlide] = useState(0);

  const pricingTiers: PricingTier[] = [
    {
      name: 'Starter',
      price: '₹999',
      period: '/month',
      features: [
        'NSE Real-time Data',
        'Basic Option Chain',
        '5 Active Strategies',
        'Standard Support'
      ],
      cta: 'Start Free Trial'
    },
    {
      name: 'Professional',
      price: '₹2,999',
      period: '/month',
      features: [
        'Full NSE + BSE Access',
        'Advanced Option Chain',
        'Unlimited Strategies',
        'Crypto Integration',
        'Priority Support',
        'Risk Analytics'
      ],
      popular: true,
      cta: 'Get Started'
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      period: '/tailored',
      features: [
        'Everything in Pro',
        'White-label Solution',
        'API Access',
        'Dedicated Manager',
        'Custom Integrations'
      ],
      cta: 'Contact Sales'
    }
  ];

  const testimonials = [
    {
      name: 'Rajesh Kumar',
      role: 'Quantitative Trader',
      company: 'Mumbai',
      rating: 5,
      text: "AlgoProject's NSE option chain analysis helped me increase my success rate by 40%. The platform is incredibly intuitive."
    },
    {
      name: 'Priya Sharma',
      role: 'Portfolio Manager',
      company: 'Delhi',
      rating: 5,
      text: 'The crypto integration with Delta Exchange is seamless. Perfect for diversified algorithmic trading strategies.'
    },
    {
      name: 'Amit Patel',
      role: 'Retail Trader',
      company: 'Bangalore',
      rating: 5,
      text: 'Clean interface, powerful analytics, and excellent support. This platform transformed my trading approach.'
    }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % testimonials.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-white overflow-hidden">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-4">
        {/* Background Effects */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-950/50 via-slate-950 to-purple-950/50" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(59,130,246,0.1),transparent)] opacity-70" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_80%,rgba(139,92,246,0.1),transparent)] opacity-70" />

        <div className="relative z-10 max-w-6xl mx-auto text-center">
          {/* Main Headline */}
          <div className="mb-8">
            <div className="inline-flex items-center px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-full text-blue-400 text-sm font-medium mb-6">
              <Star className="h-4 w-4 mr-2" />
              India's Most Advanced Algorithmic Trading Platform
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold leading-tight mb-6">
              <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-blue-400 bg-clip-text text-transparent">
                Institutional-Grade
              </span>
              <br />
              <span className="text-white">Trading Platform</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-slate-300 max-w-4xl mx-auto leading-relaxed mb-6">
              Advanced cryptocurrency trading platform with comprehensive backtesting, 
              <span className="text-blue-400 font-semibold"> multi-exchange support</span>, 
              <span className="text-purple-400 font-semibold"> AI-powered analytics</span>, and 
              <span className="text-green-400 font-semibold"> professional-grade tools</span> for algorithmic trading.
            </p>

            {/* Value Propositions */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto mb-8">
              <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
                <div className="bg-blue-500/20 w-12 h-12 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <BarChart3 className="h-6 w-6 text-blue-400" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">Professional Analytics</h3>
                <p className="text-slate-400 text-sm">Real-time option Greeks, volatility analysis, and institutional-grade risk metrics</p>
              </div>
              
              <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
                <div className="bg-purple-500/20 w-12 h-12 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <Zap className="h-6 w-6 text-purple-400" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">Multi-Exchange Trading</h3>
                <p className="text-slate-400 text-sm">Trade across top global exchanges including Binance, Coinbase, Kraken, and more with unified APIs</p>
              </div>
              
              <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
                <div className="bg-green-500/20 w-12 h-12 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <Shield className="h-6 w-6 text-green-400" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">Enterprise Security</h3>
                <p className="text-slate-400 text-sm">Bank-grade encryption, multi-factor authentication, and advanced risk controls</p>
              </div>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-6 justify-center items-center mb-16">
            <Link 
              href="/dashboard"
              className="group relative px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl text-white font-semibold text-lg transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-blue-500/25"
            >
              <span className="flex items-center">
                Launch Dashboard
                <ArrowRight className="h-5 w-5 ml-2 group-hover:translate-x-1 transition-transform" />
              </span>
            </Link>
            
            <Link 
              href="#pricing"
              className="group relative px-8 py-4 bg-slate-800/50 border border-slate-700 rounded-xl text-white font-semibold text-lg transition-all duration-300 hover:bg-slate-800 hover:border-slate-600"
            >
              <span className="flex items-center">
                <Play className="h-5 w-5 mr-2" />
                View Pricing
              </span>
            </Link>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-blue-400 mb-2">200+</div>
              <div className="text-slate-400 text-sm">Global Exchanges</div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-purple-400 mb-2">50K+</div>
              <div className="text-slate-400 text-sm">Trading Instruments</div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-green-400 mb-2">99.9%</div>
              <div className="text-slate-400 text-sm">Uptime Guarantee</div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-orange-400 mb-2">&lt;10ms</div>
              <div className="text-slate-400 text-sm">Order Latency</div>
            </div>
          </div>
        </div>

        {/* Scroll Indicator */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
          <div className="w-6 h-10 border-2 border-slate-600 rounded-full flex justify-center">
            <div className="w-1 h-3 bg-blue-400 rounded-full mt-2 animate-pulse" />
          </div>
        </div>
      </section>

      {/* Trading Platforms Tabs */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                Complete Trading Ecosystem
              </span>
            </h2>
            <p className="text-xl text-slate-300 max-w-4xl mx-auto">
              From NSE Options to Global Cryptocurrencies - One platform for all your algorithmic trading needs. 
              Professional tools, institutional data, and enterprise-grade infrastructure.
            </p>
          </div>

          {/* Tab Navigation */}
          <div className="flex justify-center mb-12">
            <div className="bg-slate-900/50 p-2 rounded-2xl border border-slate-800">
              <button
                onClick={() => setActiveTab('stocks')}
                className={`px-8 py-4 rounded-xl font-semibold text-lg transition-all duration-300 ${
                  activeTab === 'stocks'
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800'
                }`}
              >
                Indian Markets (NSE/BSE)
              </button>
              <button
                onClick={() => setActiveTab('crypto')}
                className={`px-8 py-4 rounded-xl font-semibold text-lg transition-all duration-300 ${
                  activeTab === 'crypto'
                    ? 'bg-purple-600 text-white shadow-lg'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800'
                }`}
              >
                Global Exchanges (200+)
              </button>
            </div>
          </div>

          {/* Tab Content */}
          <div className="relative">
            {activeTab === 'stocks' && (
              <div className="grid md:grid-cols-2 gap-12 items-center">
                <div>
                  <h3 className="text-3xl font-bold mb-6 text-blue-400">
                    Indian Stock Markets - NSE & BSE
                  </h3>
                  <p className="text-lg text-slate-300 mb-8 leading-relaxed">
                    Complete ecosystem for Indian markets with real-time NSE/BSE data, advanced option chains, 
                    AI-powered analytics, and institutional-grade backtesting. Fyers API integration ensures 
                    accurate expiry calculations and seamless order execution.
                  </p>
                  
                  <div className="space-y-4 mb-8">
                    <div className="flex items-center text-slate-300">
                      <div className="w-2 h-2 bg-blue-400 rounded-full mr-4"></div>
                      Real-time NSE/BSE option chains with accurate expiry dates
                    </div>
                    <div className="flex items-center text-slate-300">
                      <div className="w-2 h-2 bg-blue-400 rounded-full mr-4"></div>
                      Advanced Greeks, volatility & liquidity analysis
                    </div>
                    <div className="flex items-center text-slate-300">
                      <div className="w-2 h-2 bg-blue-400 rounded-full mr-4"></div>
                      AI-powered strategy recommendations & risk assessment
                    </div>
                    <div className="flex items-center text-slate-300">
                      <div className="w-2 h-2 bg-blue-400 rounded-full mr-4"></div>
                      Fyers API integration for seamless trading
                    </div>
                    <div className="flex items-center text-slate-300">
                      <div className="w-2 h-2 bg-blue-400 rounded-full mr-4"></div>
                      Professional charting with 100+ technical indicators
                    </div>
                  </div>

                  <Link
                    href="/stocks"
                    className="inline-flex items-center px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-xl text-white font-semibold transition-all duration-300 hover:scale-105"
                  >
                    Explore NSE Trading
                    <ChevronRight className="h-5 w-5 ml-2" />
                  </Link>
                </div>

                <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-2xl p-8 border border-slate-700">
                  <div className="mb-6">
                    <h4 className="text-xl font-semibold text-blue-400 mb-4">Live Option Chain</h4>
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div className="text-center">
                        <div className="text-green-400 font-bold">CALLS</div>
                      </div>
                      <div className="text-center">
                        <div className="text-white font-bold">STRIKE</div>
                      </div>
                      <div className="text-center">
                        <div className="text-red-400 font-bold">PUTS</div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    {[
                      { strike: '21000', callPrice: '156.50', putPrice: '45.20' },
                      { strike: '21100', callPrice: '98.75', putPrice: '67.30' },
                      { strike: '21200', callPrice: '67.25', putPrice: '98.45' },
                      { strike: '21300', callPrice: '43.80', putPrice: '145.60' }
                    ].map((option, index) => (
                      <div key={index} className="grid grid-cols-3 gap-4 py-2 px-4 bg-slate-800/50 rounded-lg">
                        <div className="text-green-400 font-mono text-center">{option.callPrice}</div>
                        <div className="text-white font-mono text-center font-bold">{option.strike}</div>
                        <div className="text-red-400 font-mono text-center">{option.putPrice}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'crypto' && (
              <div className="grid md:grid-cols-2 gap-12 items-center">
                <div>
                  <h3 className="text-3xl font-bold mb-6 text-purple-400">
                    Global Multi-Exchange Trading
                  </h3>
                  <p className="text-lg text-slate-300 mb-8 leading-relaxed">
                    Trade across 200+ global exchanges including Binance, Coinbase, Kraken, and regional exchanges. 
                    CCXT integration provides unified APIs, real-time data, and advanced order management 
                    for cryptocurrencies, forex, and international equity markets.
                  </p>
                  
                  <div className="space-y-4 mb-8">
                    <div className="flex items-center text-slate-300">
                      <div className="w-2 h-2 bg-purple-400 rounded-full mr-4"></div>
                      200+ exchanges via CCXT unified API integration
                    </div>
                    <div className="flex items-center text-slate-300">
                      <div className="w-2 h-2 bg-purple-400 rounded-full mr-4"></div>
                      Real-time multi-exchange arbitrage opportunities
                    </div>
                    <div className="flex items-center text-slate-300">
                      <div className="w-2 h-2 bg-purple-400 rounded-full mr-4"></div>
                      Advanced portfolio rebalancing algorithms
                    </div>
                    <div className="flex items-center text-slate-300">
                      <div className="w-2 h-2 bg-purple-400 rounded-full mr-4"></div>
                      Professional charting similar to TradingView
                    </div>
                    <div className="flex items-center text-slate-300">
                      <div className="w-2 h-2 bg-purple-400 rounded-full mr-4"></div>
                      Cross-exchange risk management & reporting
                    </div>
                  </div>

                  <Link
                    href="/exchanges"
                    className="inline-flex items-center px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-xl text-white font-semibold transition-all duration-300 hover:scale-105"
                  >
                    Explore Global Exchanges
                    <ChevronRight className="h-5 w-5 ml-2" />
                  </Link>
                </div>

                <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-2xl p-8 border border-slate-700">
                  <div className="mb-6">
                    <h4 className="text-xl font-semibold text-purple-400 mb-4">Supported Exchanges</h4>
                    <div className="text-sm text-slate-400 mb-4">CCXT Integration - 200+ Exchanges</div>
                  </div>
                  
                  <div className="space-y-4">
                    {[
                      { name: 'Binance', type: 'Global Crypto', assets: '500+', status: 'Active' },
                      { name: 'Coinbase Pro', type: 'US Crypto', assets: '200+', status: 'Active' },
                      { name: 'Kraken', type: 'European Crypto', assets: '190+', status: 'Active' },
                      { name: 'OKX', type: 'Global Crypto', assets: '400+', status: 'Active' }
                    ].map((exchange, index) => (
                      <div key={index} className="flex items-center justify-between py-3 px-4 bg-slate-800/50 rounded-lg">
                        <div>
                          <div className="font-semibold text-white">{exchange.name}</div>
                          <div className="text-xs text-slate-400">{exchange.type}</div>
                        </div>
                        <div className="text-right">
                          <div className="font-mono text-purple-400">{exchange.assets}</div>
                          <div className="text-xs text-green-400">{exchange.status}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Features Slider */}
      <section className="py-20 px-4 bg-slate-950/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                Why Choose AlgoProject
              </span>
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="group p-8 bg-gradient-to-br from-slate-900 to-slate-800 rounded-2xl border border-slate-700 hover:border-blue-500/50 transition-all duration-300 hover:scale-105">
              <div className="p-4 bg-blue-500/10 rounded-xl w-fit mb-6 group-hover:bg-blue-500/20 transition-colors">
                <BarChart3 className="h-8 w-8 text-blue-400" />
              </div>
              <h3 className="text-xl font-bold mb-4 text-white">Advanced Analytics</h3>
              <p className="text-slate-300">
                Real-time option chain analysis, volatility tracking, and risk metrics 
                to make informed trading decisions.
              </p>
            </div>

            <div className="group p-8 bg-gradient-to-br from-slate-900 to-slate-800 rounded-2xl border border-slate-700 hover:border-purple-500/50 transition-all duration-300 hover:scale-105">
              <div className="p-4 bg-purple-500/10 rounded-xl w-fit mb-6 group-hover:bg-purple-500/20 transition-colors">
                <Zap className="h-8 w-8 text-purple-400" />
              </div>
              <h3 className="text-xl font-bold mb-4 text-white">Lightning Fast</h3>
              <p className="text-slate-300">
                Ultra-low latency execution across NSE and crypto exchanges. 
                Never miss a trading opportunity.
              </p>
            </div>

            <div className="group p-8 bg-gradient-to-br from-slate-900 to-slate-800 rounded-2xl border border-slate-700 hover:border-green-500/50 transition-all duration-300 hover:scale-105">
              <div className="p-4 bg-green-500/10 rounded-xl w-fit mb-6 group-hover:bg-green-500/20 transition-colors">
                <Shield className="h-8 w-8 text-green-400" />
              </div>
              <h3 className="text-xl font-bold mb-4 text-white">Bank-Grade Security</h3>
              <p className="text-slate-300">
                Enterprise-level security with encrypted data transmission 
                and SEBI-compliant risk management.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Slider */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-6 text-white">
              Trusted by <span className="text-blue-400">15,000+</span> Traders
            </h2>
          </div>

          <div className="relative">
            <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-2xl p-8 border border-slate-700">
              <div className="text-center">
                <div className="flex justify-center mb-4">
                  {[...Array(testimonials[currentSlide].rating)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                
                <blockquote className="text-xl text-slate-300 mb-6 leading-relaxed">
                  "{testimonials[currentSlide].text}"
                </blockquote>
                
                <div>
                  <div className="font-semibold text-white text-lg">
                    {testimonials[currentSlide].name}
                  </div>
                  <div className="text-slate-400">
                    {testimonials[currentSlide].role} • {testimonials[currentSlide].company}
                  </div>
                </div>
              </div>
            </div>

            {/* Slider Dots */}
            <div className="flex justify-center mt-8 space-x-2">
              {testimonials.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentSlide(index)}
                  className={`w-3 h-3 rounded-full transition-all duration-300 ${
                    index === currentSlide ? 'bg-blue-400' : 'bg-slate-600'
                  }`}
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 px-4 bg-slate-950/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                Choose Your Plan
              </span>
            </h2>
            <p className="text-xl text-slate-300">
              Start your algorithmic trading journey today
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {pricingTiers.map((tier, index) => (
              <div
                key={index}
                className={`relative p-8 rounded-2xl border transition-all duration-300 hover:scale-105 ${
                  tier.popular
                    ? 'bg-gradient-to-br from-blue-900/50 to-purple-900/50 border-blue-500/50'
                    : 'bg-gradient-to-br from-slate-900 to-slate-800 border-slate-700'
                }`}
              >
                {tier.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <div className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-6 py-2 rounded-full text-sm font-semibold">
                      Most Popular
                    </div>
                  </div>
                )}

                <div className="text-center mb-8">
                  <h3 className="text-2xl font-bold text-white mb-4">{tier.name}</h3>
                  <div className="mb-4">
                    <span className="text-4xl font-bold text-blue-400">{tier.price}</span>
                    <span className="text-slate-400">{tier.period}</span>
                  </div>
                </div>

                <ul className="space-y-4 mb-8">
                  {tier.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-center text-slate-300">
                      <div className="w-2 h-2 bg-blue-400 rounded-full mr-3 flex-shrink-0"></div>
                      {feature}
                    </li>
                  ))}
                </ul>

                <button
                  className={`w-full py-4 rounded-xl font-semibold text-lg transition-all duration-300 ${
                    tier.popular
                      ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white hover:scale-105'
                      : 'bg-slate-800 text-white hover:bg-slate-700 border border-slate-600'
                  }`}
                >
                  {tier.cta}
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Ready to <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">Transform</span> Your Trading?
          </h2>
          <p className="text-xl text-slate-300 mb-8 max-w-2xl mx-auto">
            Join thousands of successful traders using AlgoProject's advanced algorithms 
            for NSE and crypto markets.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-6 justify-center">
            <button className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl text-white font-semibold text-lg transition-all duration-300 hover:scale-105 hover:shadow-2xl">
              Start Free Trial Today
            </button>
            <button className="px-8 py-4 bg-slate-800 border border-slate-700 rounded-xl text-white font-semibold text-lg transition-all duration-300 hover:bg-slate-700">
              Schedule Demo Call
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}