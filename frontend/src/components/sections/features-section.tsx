'use client';

import React from 'react';
import { 
  TrendingUp, 
  Brain, 
  Shield, 
  Zap, 
  BarChart3, 
  Wallet, 
  Users, 
  Target,
  Globe,
  Clock,
  Lock,
  Smartphone
} from 'lucide-react';

const features = [
  {
    icon: TrendingUp,
    title: 'Real-Time Trading',
    description: 'Execute trades instantly with live market data and advanced order types across multiple exchanges.',
    gradient: 'from-blue-500 to-cyan-500',
    delay: 'delay-0'
  },
  {
    icon: Brain,
    title: 'AI-Powered Strategies',
    description: 'Create and deploy sophisticated trading algorithms with machine learning capabilities.',
    gradient: 'from-purple-500 to-pink-500',
    delay: 'delay-100'
  },
  {
    icon: Shield,
    title: 'Risk Management',
    description: 'Advanced risk controls with position sizing, stop-loss, and portfolio protection features.',
    gradient: 'from-green-500 to-emerald-500',
    delay: 'delay-200'
  },
  {
    icon: BarChart3,
    title: 'Advanced Analytics',
    description: 'Comprehensive performance analytics with detailed reporting and backtesting capabilities.',
    gradient: 'from-orange-500 to-red-500',
    delay: 'delay-300'
  },
  {
    icon: Wallet,
    title: 'Portfolio Management',
    description: 'Track your investments across multiple asset classes with real-time P&L monitoring.',
    gradient: 'from-indigo-500 to-blue-500',
    delay: 'delay-400'
  },
  {
    icon: Zap,
    title: 'Lightning Fast',
    description: 'Ultra-low latency execution with high-frequency trading capabilities and instant notifications.',
    gradient: 'from-yellow-500 to-orange-500',
    delay: 'delay-500'
  }
];

const additionalFeatures = [
  { icon: Globe, text: 'Multi-Exchange Support' },
  { icon: Clock, text: '24/7 Trading' },
  { icon: Lock, text: 'Bank-Grade Security' },
  { icon: Smartphone, text: 'Mobile Trading' },
  { icon: Users, text: 'Community Features' },
  { icon: Target, text: 'Precision Execution' }
];

export function FeaturesSection() {
  return (
    <section className="py-24 relative">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-gradient-to-b from-slate-900 to-slate-800"></div>
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-20">
          <div className="inline-flex items-center space-x-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-6 py-2 text-blue-400 mb-6">
            <Zap className="h-4 w-4" />
            <span className="text-sm font-medium">Powerful Features</span>
          </div>
          
          <h2 className="text-4xl md:text-6xl font-bold text-white mb-6">
            Everything You Need to
            <span className="block bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              Trade Successfully
            </span>
          </h2>
          
          <p className="text-xl text-slate-300 max-w-3xl mx-auto">
            Our platform combines cutting-edge technology with intuitive design to deliver 
            a trading experience that's both powerful and accessible.
          </p>
        </div>

        {/* Main Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div
                key={feature.title}
                className={`group relative bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-8 hover:border-slate-600 transition-all duration-500 hover:transform hover:scale-105 animate-fade-in ${feature.delay}`}
              >
                {/* Hover Effect */}
                <div className="absolute inset-0 bg-gradient-to-r opacity-0 group-hover:opacity-10 transition-opacity duration-500 rounded-2xl from-blue-500 to-purple-500"></div>
                
                {/* Icon */}
                <div className={`w-14 h-14 rounded-xl bg-gradient-to-r ${feature.gradient} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <Icon className="h-7 w-7 text-white" />
                </div>

                {/* Content */}
                <h3 className="text-xl font-semibold text-white mb-4 group-hover:text-blue-400 transition-colors">
                  {feature.title}
                </h3>
                <p className="text-slate-300 leading-relaxed">
                  {feature.description}
                </p>

                {/* Floating Animation */}
                <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Additional Features */}
        <div className="bg-slate-800/30 backdrop-blur-sm border border-slate-700 rounded-2xl p-8">
          <h3 className="text-2xl font-bold text-white text-center mb-8">
            And Much More...
          </h3>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {additionalFeatures.map((item, index) => {
              const Icon = item.icon;
              return (
                <div
                  key={item.text}
                  className="flex flex-col items-center space-y-3 p-4 rounded-lg hover:bg-slate-700/50 transition-colors group"
                >
                  <div className="w-12 h-12 bg-slate-700 group-hover:bg-blue-500 rounded-lg flex items-center justify-center transition-colors duration-300">
                    <Icon className="h-6 w-6 text-slate-300 group-hover:text-white" />
                  </div>
                  <span className="text-sm text-slate-300 group-hover:text-white text-center transition-colors">
                    {item.text}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center mt-16">
          <div className="inline-flex flex-col sm:flex-row gap-4">
            <button className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-8 py-4 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl">
              Start Free Trial
            </button>
            <button className="bg-slate-800 hover:bg-slate-700 text-white px-8 py-4 rounded-lg font-semibold transition-colors border border-slate-600 hover:border-slate-500">
              View All Features
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}