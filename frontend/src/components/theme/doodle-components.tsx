'use client';

import React, { useState, useEffect } from 'react';

// AlgoBot Mascot Component
export function AlgoBot({ 
  expression = 'happy', 
  size = 'medium', 
  accessories = [] 
}: {
  expression?: 'happy' | 'excited' | 'thinking' | 'cool';
  size?: 'small' | 'medium' | 'large';
  accessories?: string[];
}) {
  const sizeClasses = {
    small: 'text-4xl',
    medium: 'text-6xl',
    large: 'text-8xl'
  };

  const expressions = {
    happy: '😊',
    excited: '🤩', 
    thinking: '🤔',
    cool: '😎'
  };

  return (
    <div className={`${sizeClasses[size]} inline-block animate-doodle-bounce`}>
      <span className="filter drop-shadow-lg">
        {expressions[expression]}
        {accessories.includes('coffee') && '☕'}
        {accessories.includes('rocket') && '🚀'}
      </span>
    </div>
  );
}

// Playful Feature Card Component
export function PlayfulFeatureCard({ 
  icon, 
  title, 
  description, 
  color, 
  doodle 
}: {
  icon: string;
  title: string;
  description: string;
  color: 'mint-green' | 'coral-pink' | 'yellow';
  doodle: string;
}) {
  const colorClasses = {
    'mint-green': 'bg-mint-green/20 border-mint-green backdrop-blur-md',
    'coral-pink': 'bg-coral-pink/20 border-coral-pink backdrop-blur-md',
    'yellow': 'bg-yellow/20 border-yellow backdrop-blur-md'
  };

  return (
    <div className={`relative p-8 rounded-3xl border-4 ${colorClasses[color]} transform hover:scale-105 hover:rotate-1 transition-all duration-300 shadow-lg hover:shadow-xl`}>
      {/* Doodle accent */}
      <div className="absolute -top-4 -right-4 text-3xl animate-doodle-wiggle">
        {doodle}
      </div>
      
      <div className="text-5xl mb-4">{icon}</div>
      <h3 className="text-2xl font-bold text-white mb-3 drop-shadow-lg" style={{ fontFamily: 'Comic Neue, cursive' }}>
        {title}
      </h3>
      <p className="text-white/90 drop-shadow-md" style={{ fontFamily: 'Poppins, sans-serif' }}>
        {description}
      </p>
    </div>
  );
}

// Community Section Component  
export function CommunitySection() {
  return (
    <section className="py-24 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 bg-gradient-to-r from-indigo-900/30 via-purple-900/20 to-pink-900/30"></div>
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-full blur-3xl"></div>
      
      <div className="relative max-w-6xl mx-auto px-6 text-center">
        {/* Section Header */}
        <div className="mb-16">
          <div className="inline-flex items-center gap-2 mb-6 bg-white/10 backdrop-blur-md px-4 py-2 rounded-full border border-white/20">
            <span className="text-sm font-medium text-white/90">👥 Join Our Community</span>
          </div>
          
          <h2 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-white via-blue-100 to-purple-100 bg-clip-text text-transparent mb-6" style={{ fontFamily: 'Comic Neue, cursive' }}>
            Connect with
            <br />
            <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
              Trading Experts
            </span>
          </h2>
          
          <p className="text-xl text-white/70 max-w-3xl mx-auto mb-12" style={{ fontFamily: 'Poppins, sans-serif' }}>
            Join thousands of traders sharing strategies, insights, and success stories. 
            From beginners to professionals, everyone finds their place in our community.
          </p>
        </div>

        {/* Community Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-16">
          <div className="text-center">
            <div className="text-4xl mb-2">👨‍💼</div>
            <div className="text-2xl font-bold text-white mb-1" style={{ fontFamily: 'Comic Neue, cursive' }}>25K+</div>
            <div className="text-white/60 text-sm" style={{ fontFamily: 'Poppins, sans-serif' }}>Professionals</div>
          </div>
          
          <div className="text-center">
            <div className="text-4xl mb-2">👩‍💻</div>
            <div className="text-2xl font-bold text-white mb-1" style={{ fontFamily: 'Comic Neue, cursive' }}>15K+</div>
            <div className="text-white/60 text-sm" style={{ fontFamily: 'Poppins, sans-serif' }}>Developers</div>
          </div>
          
          <div className="text-center">
            <div className="text-4xl mb-2">🎓</div>
            <div className="text-2xl font-bold text-white mb-1" style={{ fontFamily: 'Comic Neue, cursive' }}>10K+</div>
            <div className="text-white/60 text-sm" style={{ fontFamily: 'Poppins, sans-serif' }}>Students</div>
          </div>
          
          <div className="text-center">
            <div className="text-4xl mb-2">🚀</div>
            <div className="text-2xl font-bold text-white mb-1" style={{ fontFamily: 'Comic Neue, cursive' }}>5K+</div>
            <div className="text-white/60 text-sm" style={{ fontFamily: 'Poppins, sans-serif' }}>Entrepreneurs</div>
          </div>
        </div>

        {/* CTA */}
        <div className="bg-white/5 backdrop-blur-md rounded-3xl border border-white/10 p-8 max-w-2xl mx-auto">
          <p className="text-lg text-white/90 mb-6" style={{ fontFamily: 'Comic Neue, cursive' }}>
            "From retail dreamers to data scientists — everyone belongs here! �"
          </p>
          
          <button className="bg-gradient-to-r from-emerald-500 to-cyan-500 text-white px-8 py-4 rounded-2xl text-lg font-bold hover:scale-105 transition-all duration-300 hover:shadow-2xl hover:shadow-emerald-500/25" style={{ fontFamily: 'Comic Neue, cursive' }}>
            Join Community
          </button>
        </div>
      </div>
    </section>
  );
}

// Modern Pricing Card Component
export function PlayfulPricingCard({
  plan,
  price,
  badge,
  features,
  isPopular = false
}: {
  plan: string;
  price: string;
  badge: string;
  features: string[];
  isPopular?: boolean;
}) {
  return (
    <div className={`relative h-full transition-all duration-500 hover:scale-105 ${
      isPopular ? 'z-10' : 'z-0'
    }`}>
      {/* Popular badge */}
      {isPopular && (
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 z-20">
          <div className="bg-gradient-to-r from-emerald-500 to-cyan-500 text-white px-6 py-2 rounded-full text-sm font-bold shadow-lg">
            ⭐ {badge}
          </div>
        </div>
      )}

      <div className={`h-full p-8 rounded-3xl border transition-all duration-500 backdrop-blur-md ${
        isPopular 
          ? 'border-emerald-400/50 bg-gradient-to-b from-emerald-500/10 to-cyan-500/10 shadow-2xl shadow-emerald-500/20' 
          : 'border-white/20 bg-white/5 hover:bg-white/10 hover:border-white/30'
      }`}>
        {/* Plan header */}
        <div className="text-center mb-8">
          <h3 className="text-2xl font-bold text-white mb-2" style={{ fontFamily: 'Comic Neue, cursive' }}>
            {plan}
          </h3>
          {!isPopular && (
            <div className="text-sm text-white/60 mb-4">{badge}</div>
          )}
          <div className="flex items-baseline justify-center">
            <span className="text-5xl font-bold bg-gradient-to-r from-white to-cyan-200 bg-clip-text text-transparent" style={{ fontFamily: 'Comic Neue, cursive' }}>
              {price}
            </span>
            <span className="text-lg text-white/70 ml-1">/month</span>
          </div>
        </div>

        {/* Features list */}
        <ul className="space-y-4 mb-8">
          {features.map((feature, index) => (
            <li key={index} className="flex items-start text-white/80" style={{ fontFamily: 'Poppins, sans-serif' }}>
              <span className={`${isPopular ? 'text-emerald-400' : 'text-cyan-400'} mr-3 mt-1 flex-shrink-0`}>✓</span>
              <span className="leading-relaxed">{feature}</span>
            </li>
          ))}
        </ul>

        {/* CTA Button */}
        <button className={`w-full py-4 px-6 rounded-2xl font-bold text-lg transition-all duration-300 hover:scale-105 hover:shadow-xl ${
          isPopular
            ? 'bg-gradient-to-r from-emerald-500 to-cyan-500 text-white hover:shadow-emerald-500/25'
            : 'bg-white/10 border-2 border-white/30 text-white hover:bg-white/20 hover:border-white/50'
        }`} style={{ fontFamily: 'Comic Neue, cursive' }}>
          {isPopular ? 'Get Started Now' : `Choose ${plan}`}
        </button>
      </div>
    </div>
  );
}

// Doodle Feature Card Component (for features-section.tsx)
export function DoodleFeatureCard({ 
  icon, 
  title, 
  description 
}: {
  icon: string;
  title: string;
  description: string;
}) {
  return (
    <div className="relative p-8 rounded-3xl border-4 border-mint-green bg-mint-green/20 transform hover:scale-105 hover:rotate-1 transition-all duration-300 shadow-lg hover:shadow-xl backdrop-blur-md">
      <div className="text-5xl mb-4 animate-doodle-bounce">{icon}</div>
      <h3 className="text-2xl font-bold text-white mb-3 drop-shadow-lg" style={{ fontFamily: 'Comic Neue, cursive' }}>
        {title}
      </h3>
      <p className="text-white/90 drop-shadow-md" style={{ fontFamily: 'Poppins, sans-serif' }}>
        {description}
      </p>
    </div>
  );
}

// Doodle Background Component
export function DoodleBackground({ theme }: { theme: string }) {
  return (
    <div className="doodle-background fixed inset-0 pointer-events-none z-[-1]">
      <div className="absolute inset-0 bg-gradient-to-br from-off-white via-mint-green/5 to-coral-pink/5" />
      
      {/* Animated doodle elements */}
      <div className="absolute top-20 left-10 text-4xl animate-doodle-float-0">☁️</div>
      <div className="absolute top-40 right-20 text-3xl animate-doodle-float-1">⭐</div>
      <div className="absolute bottom-32 left-20 text-2xl animate-doodle-float-2">🎈</div>
      <div className="absolute bottom-20 right-40 text-3xl animate-doodle-wiggle">✨</div>
      <div className="absolute top-1/2 left-1/4 text-2xl animate-doodle-twinkle">🌟</div>
      <div className="absolute top-3/4 right-1/3 text-4xl animate-doodle-bounce-slow">🎯</div>
    </div>
  );
}

// Doodle Hero Section Component
export function DoodleHeroSection() {
  return (
    <section className="relative py-12 overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-900/10 via-purple-900/10 to-pink-900/10"></div>
      
      <div className="relative max-w-7xl mx-auto px-6 text-center z-10">
        {/* Minimal Hero Content */}
        <div className="py-8">
          <div className="text-2xl font-bold text-white/80" style={{ fontFamily: 'Comic Neue, cursive' }}>
            Welcome to AlgoProject
          </div>
        </div>
      </div>
    </section>
  );
}

// Modern Features Section Component
export function ModernFeaturesSection() {
  const features = [
    {
      icon: "🤖",
      title: "AI-Powered Strategies",
      description: "Advanced machine learning algorithms that adapt to market conditions and optimize your trading performance in real-time.",
      gradient: "from-blue-500 to-cyan-500"
    },
    {
      icon: "📊",
      title: "Advanced Analytics", 
      description: "Comprehensive market analysis with custom indicators, backtesting capabilities, and detailed performance metrics.",
      gradient: "from-emerald-500 to-teal-500"
    },
    {
      icon: "🔒",
      title: "Bank-Grade Security",
      description: "Enterprise-level security with encrypted data, secure API connections, and multi-factor authentication protection.",
      gradient: "from-purple-500 to-pink-500"
    },
    {
      icon: "⚡",
      title: "Lightning Fast Execution",
      description: "Ultra-low latency trading execution with direct market access and optimized order routing algorithms.",
      gradient: "from-yellow-500 to-orange-500"
    },
    {
      icon: "📱",
      title: "Mobile Trading",
      description: "Trade on-the-go with our responsive mobile platform, featuring real-time notifications and portfolio tracking.",
      gradient: "from-indigo-500 to-purple-500"
    },
    {
      icon: "🎓",
      title: "Educational Resources",
      description: "Comprehensive learning center with tutorials, webinars, and market insights to enhance your trading skills.",
      gradient: "from-rose-500 to-pink-500"
    }
  ];

  return (
    <section className="py-24 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-white/5 to-transparent"></div>
      
      <div className="relative max-w-7xl mx-auto px-6">
        {/* Section Header */}
        <div className="text-center mb-20">
          <div className="inline-flex items-center gap-2 mb-6 bg-white/10 backdrop-blur-md px-4 py-2 rounded-full border border-white/20">
            <span className="text-sm font-medium text-white/90">🚀 Platform Features</span>
          </div>
          
          <h2 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-white via-blue-100 to-purple-100 bg-clip-text text-transparent mb-6" style={{ fontFamily: 'Comic Neue, cursive' }}>
            Everything You Need to
            <br />
            <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
              Trade Like a Pro
            </span>
          </h2>
          
          <p className="text-xl text-white/70 max-w-3xl mx-auto" style={{ fontFamily: 'Poppins, sans-serif' }}>
            Our comprehensive trading platform combines cutting-edge technology with intuitive design 
            to deliver an unparalleled trading experience.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="group relative">
              <div className="h-full p-8 bg-white/5 backdrop-blur-md rounded-3xl border border-white/10 hover:bg-white/10 hover:border-white/20 transition-all duration-500 hover:scale-105">
                {/* Icon with gradient background */}
                <div className={`inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-r ${feature.gradient} mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <span className="text-3xl">{feature.icon}</span>
                </div>
                
                <h3 className="text-2xl font-bold text-white mb-4 group-hover:text-cyan-300 transition-colors" style={{ fontFamily: 'Comic Neue, cursive' }}>
                  {feature.title}
                </h3>
                
                <p className="text-white/70 leading-relaxed" style={{ fontFamily: 'Poppins, sans-serif' }}>
                  {feature.description}
                </p>
                
                {/* Hover effect */}
                <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-cyan-500/10 to-blue-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}