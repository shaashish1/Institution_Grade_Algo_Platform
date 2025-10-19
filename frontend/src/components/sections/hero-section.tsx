'use client';

import React, { useEffect, useState } from 'react';
import { 
  TrendingUp, 
  ArrowRight, 
  Play, 
  Star, 
  Users, 
  DollarSign, 
  Zap,
  Shield,
  BarChart3,
  Sparkles
} from 'lucide-react';

export function HeroSection() {
  const [mounted, setMounted] = useState(false);
  const [currentStat, setCurrentStat] = useState(0);

  const stats = [
    { label: 'Active Traders', value: '50,000+', icon: Users },
    { label: 'Trading Volume', value: '$2.5B+', icon: DollarSign },
    { label: 'Success Rate', value: '89%', icon: TrendingUp },
    { label: 'Uptime', value: '99.9%', icon: Shield },
  ];

  useEffect(() => {
    setMounted(true);
    const interval = setInterval(() => {
      setCurrentStat((prev) => (prev + 1) % stats.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  if (!mounted) return null;

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-16">
      {/* Animated Background */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900"></div>
        <div className="absolute inset-0 opacity-30">
          <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-blue-500/20 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-green-500/10 rounded-full blur-3xl animate-pulse delay-2000"></div>
        </div>
      </div>

      {/* Grid Pattern */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute inset-0" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }}></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="space-y-8">
          {/* Animated Badge */}
          <div className="inline-flex items-center space-x-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-6 py-2 text-blue-400 animate-fade-in">
            <Sparkles className="h-4 w-4" />
            <span className="text-sm font-medium">Institution Grade Trading Platform</span>
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          </div>

          {/* Main Heading */}
          <div className="space-y-4">
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-white leading-tight">
              <span className="block">Trade Like a</span>
              <span className="block bg-gradient-to-r from-blue-400 via-purple-500 to-green-400 bg-clip-text text-transparent animate-gradient">
                Professional
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-slate-300 max-w-3xl mx-auto leading-relaxed">
              Advanced algorithmic trading platform with real-time analytics, 
              portfolio management, and institutional-grade risk controls.
            </p>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <button className="group bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-8 py-4 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl flex items-center space-x-2">
              <span>Start Trading Now</span>
              <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
            </button>
            
            <button className="group bg-slate-800/50 hover:bg-slate-700/50 text-white px-8 py-4 rounded-lg font-semibold transition-all duration-300 border border-slate-600 hover:border-slate-500 flex items-center space-x-2">
              <Play className="h-5 w-5" />
              <span>Watch Demo</span>
            </button>
          </div>

          {/* Animated Stats */}
          <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => {
              const Icon = stat.icon;
              const isActive = currentStat === index;
              
              return (
                <div
                  key={stat.label}
                  className={`p-6 rounded-xl border transition-all duration-500 ${
                    isActive 
                      ? 'bg-blue-500/20 border-blue-500/50 scale-105 shadow-lg' 
                      : 'bg-slate-800/30 border-slate-700/50'
                  }`}
                >
                  <div className={`w-12 h-12 mx-auto mb-4 rounded-lg flex items-center justify-center transition-colors ${
                    isActive ? 'bg-blue-500' : 'bg-slate-700'
                  }`}>
                    <Icon className={`h-6 w-6 ${isActive ? 'text-white' : 'text-slate-300'}`} />
                  </div>
                  <div className={`text-2xl font-bold mb-1 transition-colors ${
                    isActive ? 'text-blue-400' : 'text-white'
                  }`}>
                    {stat.value}
                  </div>
                  <div className="text-slate-400 text-sm">{stat.label}</div>
                </div>
              );
            })}
          </div>

          {/* Trust Indicators */}
          <div className="mt-16 flex flex-wrap justify-center items-center gap-8 opacity-60">
            <div className="flex items-center space-x-2 text-slate-400">
              <Shield className="h-5 w-5" />
              <span className="text-sm">SEBI Compliant</span>
            </div>
            <div className="flex items-center space-x-2 text-slate-400">
              <Zap className="h-5 w-5" />
              <span className="text-sm">Real-time Data</span>
            </div>
            <div className="flex items-center space-x-2 text-slate-400">
              <BarChart3 className="h-5 w-5" />
              <span className="text-sm">Advanced Analytics</span>
            </div>
            <div className="flex items-center space-x-2 text-slate-400">
              <Star className="h-5 w-5" />
              <span className="text-sm">5-Star Rated</span>
            </div>
          </div>
        </div>
      </div>

      {/* Floating Elements */}
      <div className="absolute top-20 left-10 animate-float">
        <div className="w-4 h-4 bg-blue-400 rounded-full opacity-60"></div>
      </div>
      <div className="absolute top-40 right-20 animate-float-delay">
        <div className="w-6 h-6 bg-purple-400 rounded-full opacity-40"></div>
      </div>
      <div className="absolute bottom-40 left-20 animate-float-delay-2">
        <div className="w-3 h-3 bg-green-400 rounded-full opacity-50"></div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 border-2 border-slate-400 rounded-full flex justify-center">
          <div className="w-1 h-3 bg-slate-400 rounded-full mt-2 animate-pulse"></div>
        </div>
      </div>
    </section>
  );
}