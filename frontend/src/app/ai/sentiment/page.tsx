'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Globe, TrendingUp, TrendingDown, Activity, MessageCircle, Users, Eye, BarChart3, Zap, Calendar } from 'lucide-react';

interface SentimentData {
  symbol: string;
  sentiment: number;
  news_sentiment: number;
  social_sentiment: number;
  technical_sentiment: number;
  volume_sentiment: number;
  change: number;
  price: number;
  recommendation: 'bullish' | 'bearish' | 'neutral';
}

interface NewsItem {
  id: string;
  title: string;
  summary: string;
  sentiment: number;
  source: string;
  timestamp: string;
  symbols: string[];
}

interface SocialMetrics {
  platform: string;
  mentions: number;
  sentiment: number;
  trending_symbols: string[];
  volume_change: number;
}

const sampleSentimentData: SentimentData[] = [
  {
    symbol: 'NIFTY 50',
    sentiment: 78,
    news_sentiment: 82,
    social_sentiment: 75,
    technical_sentiment: 80,
    volume_sentiment: 85,
    change: 1.2,
    price: 26247.50,
    recommendation: 'bullish'
  },
  {
    symbol: 'RELIANCE',
    sentiment: 72,
    news_sentiment: 70,
    social_sentiment: 68,
    technical_sentiment: 75,
    volume_sentiment: 80,
    change: 0.9,
    price: 2789.45,
    recommendation: 'bullish'
  },
  {
    symbol: 'TCS',
    sentiment: 45,
    news_sentiment: 40,
    social_sentiment: 50,
    technical_sentiment: 45,
    volume_sentiment: 42,
    change: -0.8,
    price: 4123.20,
    recommendation: 'bearish'
  },
  {
    symbol: 'HDFC BANK',
    sentiment: 68,
    news_sentiment: 65,
    social_sentiment: 70,
    technical_sentiment: 72,
    volume_sentiment: 65,
    change: 0.5,
    price: 1875.60,
    recommendation: 'bullish'
  }
];

const sampleNewsData: NewsItem[] = [
  {
    id: '1',
    title: 'Market rallies on positive FII inflows',
    summary: 'Strong foreign institutional investor inflows boost market sentiment across all sectors.',
    sentiment: 85,
    source: 'Economic Times',
    timestamp: '2024-01-15T10:30:00Z',
    symbols: ['NIFTY 50', 'RELIANCE', 'HDFC BANK']
  },
  {
    id: '2', 
    title: 'IT sector faces headwinds from global slowdown',
    summary: 'Technology companies report cautious outlook due to global economic uncertainties.',
    sentiment: 25,
    source: 'Business Standard',
    timestamp: '2024-01-15T08:15:00Z',
    symbols: ['TCS', 'INFY', 'WIPRO']
  },
  {
    id: '3',
    title: 'Banking sector shows resilience',
    summary: 'Strong credit growth and improving asset quality boost banking stocks.',
    sentiment: 78,
    source: 'Mint',
    timestamp: '2024-01-14T16:45:00Z',
    symbols: ['HDFC BANK', 'ICICI BANK', 'SBI']
  }
];

const sampleSocialMetrics: SocialMetrics[] = [
  {
    platform: 'Twitter',
    mentions: 45600,
    sentiment: 72,
    trending_symbols: ['RELIANCE', 'NIFTY 50', 'ADANI'],
    volume_change: 15.6
  },
  {
    platform: 'Reddit',
    mentions: 12400,
    sentiment: 68,
    trending_symbols: ['TCS', 'INFY', 'HDFC BANK'],
    volume_change: 8.2
  },
  {
    platform: 'Discord',
    mentions: 8700,
    sentiment: 80,
    trending_symbols: ['NIFTY 50', 'RELIANCE'],
    volume_change: 22.4
  }
];

export default function AIMarketSentiment() {
  const [sentimentData, setSentimentData] = useState<SentimentData[]>(sampleSentimentData);
  const [newsData, setNewsData] = useState<NewsItem[]>(sampleNewsData);
  const [socialData, setSocialData] = useState<SocialMetrics[]>(sampleSocialMetrics);
  const [selectedView, setSelectedView] = useState<'overview' | 'news' | 'social' | 'technical'>('overview');

  const getSentimentColor = (sentiment: number) => {
    if (sentiment >= 70) return 'text-green-400 bg-green-900/30';
    if (sentiment >= 50) return 'text-yellow-400 bg-yellow-900/30';
    return 'text-red-400 bg-red-900/30';
  };

  const getSentimentLabel = (sentiment: number) => {
    if (sentiment >= 80) return 'Very Bullish';
    if (sentiment >= 70) return 'Bullish';
    if (sentiment >= 50) return 'Neutral';
    if (sentiment >= 30) return 'Bearish';
    return 'Very Bearish';
  };

  const getRecommendationColor = (rec: string) => {
    switch (rec) {
      case 'bullish': return 'text-green-400 bg-green-900/30 border-green-700';
      case 'bearish': return 'text-red-400 bg-red-900/30 border-red-700';
      case 'neutral': return 'text-yellow-400 bg-yellow-900/30 border-yellow-700';
      default: return 'text-slate-400 bg-slate-900/30 border-slate-700';
    }
  };

  const overallSentiment = sentimentData.reduce((sum, item) => sum + item.sentiment, 0) / sentimentData.length;
  const newsSentiment = newsData.reduce((sum, item) => sum + item.sentiment, 0) / newsData.length;
  const socialSentiment = socialData.reduce((sum, item) => sum + item.sentiment, 0) / socialData.length;

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
            <span className="text-white">Market Sentiment</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-4">
            <Globe className="h-8 w-8 text-blue-400" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              AI Market Sentiment
            </h1>
          </div>
          <p className="text-xl text-slate-300">
            Real-time sentiment analysis from news, social media, and technical indicators
          </p>
        </div>

        {/* Sentiment Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <span className="text-slate-400">Overall Sentiment</span>
              <Activity className="h-5 w-5 text-blue-400" />
            </div>
            <div className="text-3xl font-bold text-blue-400 mb-2">
              {overallSentiment.toFixed(0)}%
            </div>
            <div className={`text-sm px-2 py-1 rounded ${getSentimentColor(overallSentiment)}`}>
              {getSentimentLabel(overallSentiment)}
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <span className="text-slate-400">News Sentiment</span>
              <MessageCircle className="h-5 w-5 text-green-400" />
            </div>
            <div className="text-3xl font-bold text-green-400 mb-2">
              {newsSentiment.toFixed(0)}%
            </div>
            <div className="text-sm text-slate-400">
              {newsData.length} articles analyzed
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <span className="text-slate-400">Social Sentiment</span>
              <Users className="h-5 w-5 text-purple-400" />
            </div>
            <div className="text-3xl font-bold text-purple-400 mb-2">
              {socialSentiment.toFixed(0)}%
            </div>
            <div className="text-sm text-slate-400">
              {socialData.reduce((sum, item) => sum + item.mentions, 0).toLocaleString()} mentions
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <span className="text-slate-400">Market Trend</span>
              {overallSentiment >= 60 ? 
                <TrendingUp className="h-5 w-5 text-green-400" /> :
                overallSentiment >= 40 ?
                <Activity className="h-5 w-5 text-yellow-400" /> :
                <TrendingDown className="h-5 w-5 text-red-400" />
              }
            </div>
            <div className={`text-2xl font-bold mb-2 ${
              overallSentiment >= 60 ? 'text-green-400' :
              overallSentiment >= 40 ? 'text-yellow-400' : 'text-red-400'
            }`}>
              {overallSentiment >= 60 ? 'BULLISH' :
               overallSentiment >= 40 ? 'NEUTRAL' : 'BEARISH'}
            </div>
            <div className="text-sm text-slate-400">
              Based on AI analysis
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6">
          <div className="flex space-x-1 bg-slate-900 p-1 rounded-lg w-fit">
            {[
              { id: 'overview', label: 'Overview', icon: BarChart3 },
              { id: 'news', label: 'News Analysis', icon: MessageCircle },
              { id: 'social', label: 'Social Media', icon: Users },
              { id: 'technical', label: 'Technical', icon: Activity }
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

        {/* Overview Tab */}
        {selectedView === 'overview' && (
          <div className="space-y-6">
            <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden">
              <div className="p-6 border-b border-slate-800">
                <h2 className="text-xl font-bold text-white">Stock Sentiment Analysis</h2>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-slate-800">
                    <tr className="text-xs text-slate-300">
                      <th className="px-4 py-3 text-left">Symbol</th>
                      <th className="px-4 py-3 text-right">Price</th>
                      <th className="px-4 py-3 text-right">Change</th>
                      <th className="px-4 py-3 text-center">Overall</th>
                      <th className="px-4 py-3 text-center">News</th>
                      <th className="px-4 py-3 text-center">Social</th>
                      <th className="px-4 py-3 text-center">Technical</th>
                      <th className="px-4 py-3 text-center">Recommendation</th>
                    </tr>
                  </thead>
                  <tbody>
                    {sentimentData.map((item, index) => (
                      <tr key={index} className="border-t border-slate-800 hover:bg-slate-800/30">
                        <td className="px-4 py-4">
                          <div className="font-medium text-white">{item.symbol}</div>
                        </td>
                        <td className="px-4 py-4 text-right">
                          <div className="font-mono text-white">₹{item.price.toLocaleString()}</div>
                        </td>
                        <td className="px-4 py-4 text-right">
                          <div className={`font-mono ${item.change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                            {item.change >= 0 ? '+' : ''}{item.change.toFixed(2)}%
                          </div>
                        </td>
                        <td className="px-4 py-4 text-center">
                          <div className="flex items-center justify-center space-x-2">
                            <div className="w-12 h-2 bg-slate-700 rounded-full">
                              <div 
                                className={`h-2 rounded-full ${
                                  item.sentiment >= 70 ? 'bg-green-400' :
                                  item.sentiment >= 50 ? 'bg-yellow-400' : 'bg-red-400'
                                }`}
                                style={{ width: `${item.sentiment}%` }}
                              ></div>
                            </div>
                            <span className="text-xs text-white font-medium">{item.sentiment}%</span>
                          </div>
                        </td>
                        <td className="px-4 py-4 text-center">
                          <span className={`text-xs font-medium ${getSentimentColor(item.news_sentiment)}`}>
                            {item.news_sentiment}%
                          </span>
                        </td>
                        <td className="px-4 py-4 text-center">
                          <span className={`text-xs font-medium ${getSentimentColor(item.social_sentiment)}`}>
                            {item.social_sentiment}%
                          </span>
                        </td>
                        <td className="px-4 py-4 text-center">
                          <span className={`text-xs font-medium ${getSentimentColor(item.technical_sentiment)}`}>
                            {item.technical_sentiment}%
                          </span>
                        </td>
                        <td className="px-4 py-4 text-center">
                          <span className={`px-2 py-1 rounded text-xs ${getRecommendationColor(item.recommendation)} border`}>
                            {item.recommendation.toUpperCase()}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* News Analysis Tab */}
        {selectedView === 'news' && (
          <div className="space-y-6">
            {newsData.map((news) => (
              <div key={news.id} className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-white mb-2">{news.title}</h3>
                    <p className="text-slate-300 text-sm mb-3">{news.summary}</p>
                    <div className="flex items-center space-x-4 text-xs text-slate-400">
                      <span>{news.source}</span>
                      <span>•</span>
                      <span>{new Date(news.timestamp).toLocaleString()}</span>
                    </div>
                  </div>
                  <div className="ml-6">
                    <div className={`px-3 py-1 rounded-full text-sm font-medium ${getSentimentColor(news.sentiment)}`}>
                      {news.sentiment}% {getSentimentLabel(news.sentiment)}
                    </div>
                  </div>
                </div>
                <div className="flex flex-wrap gap-2">
                  {news.symbols.map((symbol) => (
                    <span key={symbol} className="px-2 py-1 bg-blue-900/30 text-blue-400 text-xs rounded">
                      {symbol}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Social Media Tab */}
        {selectedView === 'social' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {socialData.map((platform) => (
              <div key={platform.platform} className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold text-white">{platform.platform}</h3>
                  <div className={`px-3 py-1 rounded-full text-sm font-medium ${getSentimentColor(platform.sentiment)}`}>
                    {platform.sentiment}%
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-300">Total Mentions:</span>
                    <span className="font-mono text-white">{platform.mentions.toLocaleString()}</span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-slate-300">Volume Change:</span>
                    <span className={`font-mono ${platform.volume_change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                      {platform.volume_change >= 0 ? '+' : ''}{platform.volume_change.toFixed(1)}%
                    </span>
                  </div>

                  <div>
                    <div className="text-slate-300 mb-2">Trending Symbols:</div>
                    <div className="flex flex-wrap gap-2">
                      {platform.trending_symbols.map((symbol) => (
                        <span key={symbol} className="px-2 py-1 bg-purple-900/30 text-purple-400 text-xs rounded">
                          {symbol}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Technical Tab */}
        {selectedView === 'technical' && (
          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
            <h2 className="text-xl font-bold text-white mb-6">Technical Sentiment Indicators</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {sentimentData.map((item) => (
                <div key={item.symbol} className="p-4 bg-slate-800 rounded-lg">
                  <h3 className="font-bold text-white mb-4">{item.symbol}</h3>
                  
                  <div className="space-y-3">
                    <div>
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-slate-300">Technical Score</span>
                        <span className="text-white">{item.technical_sentiment}%</span>
                      </div>
                      <div className="w-full h-2 bg-slate-700 rounded-full">
                        <div 
                          className={`h-2 rounded-full ${
                            item.technical_sentiment >= 70 ? 'bg-green-400' :
                            item.technical_sentiment >= 50 ? 'bg-yellow-400' : 'bg-red-400'
                          }`}
                          style={{ width: `${item.technical_sentiment}%` }}
                        ></div>
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-slate-300">Volume Sentiment</span>
                        <span className="text-white">{item.volume_sentiment}%</span>
                      </div>
                      <div className="w-full h-2 bg-slate-700 rounded-full">
                        <div 
                          className={`h-2 rounded-full ${
                            item.volume_sentiment >= 70 ? 'bg-green-400' :
                            item.volume_sentiment >= 50 ? 'bg-yellow-400' : 'bg-red-400'
                          }`}
                          style={{ width: `${item.volume_sentiment}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Quick Action Links */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link
            href="/ai/strategies"
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-purple-500 transition-colors group"
          >
            <div className="flex items-center justify-between mb-2">
              <Zap className="h-6 w-6 text-purple-400" />
              <div className="text-xs text-slate-400">AI Strategies</div>
            </div>
            <h3 className="font-semibold text-white group-hover:text-purple-400 transition-colors">
              Strategy Analyzer
            </h3>
            <p className="text-sm text-slate-400 mt-1">
              AI-powered trading strategies
            </p>
          </Link>

          <Link
            href="/ai/analysis"
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-blue-500 transition-colors group"
          >
            <div className="flex items-center justify-between mb-2">
              <Eye className="h-6 w-6 text-blue-400" />
              <div className="text-xs text-slate-400">Market Analysis</div>
            </div>
            <h3 className="font-semibold text-white group-hover:text-blue-400 transition-colors">
              AI Market Analysis
            </h3>
            <p className="text-sm text-slate-400 mt-1">
              Advanced market insights
            </p>
          </Link>

          <Link
            href="/tools/alerts"
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-yellow-500 transition-colors group"
          >
            <div className="flex items-center justify-between mb-2">
              <MessageCircle className="h-6 w-6 text-yellow-400" />
              <div className="text-xs text-slate-400">Alerts</div>
            </div>
            <h3 className="font-semibold text-white group-hover:text-yellow-400 transition-colors">
              Sentiment Alerts
            </h3>
            <p className="text-sm text-slate-400 mt-1">
              Get notified of sentiment changes
            </p>
          </Link>
        </div>
      </div>
    </div>
  );
}