'use client';

import React, { useEffect, useState } from 'react';
import { Sparkles, Zap, Rocket, Star, Moon, Sun } from 'lucide-react';

interface CosmicBackgroundProps {
  theme: 'light' | 'dark' | 'cosmic';
}

export function CosmicBackground({ theme }: CosmicBackgroundProps) {
  const [stars, setStars] = useState<Array<{ id: number; x: number; y: number; size: number; delay: number }>>([]);

  useEffect(() => {
    // Generate random stars for cosmic background
    const generateStars = () => {
      const newStars = Array.from({ length: 50 }, (_, i) => ({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: Math.random() * 3 + 1,
        delay: Math.random() * 3
      }));
      setStars(newStars);
    };

    if (theme === 'cosmic') {
      generateStars();
    }
  }, [theme]);

  if (theme !== 'cosmic') {
    return null;
  }

  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden">
      {/* Cosmic Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900 via-blue-900 to-black opacity-90" />
      
      {/* Animated Stars */}
      {stars.map((star) => (
        <div
          key={star.id}
          className="absolute rounded-full bg-white animate-sparkle"
          style={{
            left: `${star.x}%`,
            top: `${star.y}%`,
            width: `${star.size}px`,
            height: `${star.size}px`,
            animationDelay: `${star.delay}s`
          }}
        />
      ))}

      {/* Shooting Stars */}
      <div className="absolute top-20 left-20 w-1 h-1 bg-yellow-400 animate-shooting-star opacity-70" />
      <div className="absolute top-40 right-32 w-1 h-1 bg-blue-400 animate-shooting-star opacity-70" style={{ animationDelay: '1s' }} />
      <div className="absolute bottom-32 left-1/4 w-1 h-1 bg-purple-400 animate-shooting-star opacity-70" style={{ animationDelay: '2s' }} />

      {/* Floating Cosmic Elements */}
      <div className="absolute top-1/4 left-1/4 text-4xl animate-float opacity-20">🌟</div>
      <div className="absolute top-3/4 right-1/4 text-3xl animate-float opacity-20" style={{ animationDelay: '1s' }}>🌙</div>
      <div className="absolute bottom-1/4 left-3/4 text-2xl animate-float opacity-20" style={{ animationDelay: '2s' }}>✨</div>
      <div className="absolute top-1/2 right-1/3 text-3xl animate-float opacity-20" style={{ animationDelay: '3s' }}>🚀</div>

      {/* Cosmic Nebula Effects */}
      <div className="absolute top-0 left-0 w-96 h-96 bg-gradient-radial from-purple-500/20 to-transparent rounded-full blur-3xl animate-pulse-slow" />
      <div className="absolute bottom-0 right-0 w-80 h-80 bg-gradient-radial from-blue-500/20 to-transparent rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }} />
      <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-gradient-radial from-pink-500/20 to-transparent rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '2s' }} />
    </div>
  );
}

export function CosmicHeroSection() {
  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden">
      <CosmicBackground theme="cosmic" />
      
      <div className="relative z-10 text-center px-4 max-w-4xl mx-auto">
        {/* Animated Title */}
        <h1 className="text-6xl md:text-8xl font-bold mb-8 bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent animate-cosmic-glow">
          AlgoProject 🚀
        </h1>
        
        {/* Subtitle with emojis */}
        <p className="text-xl md:text-2xl text-purple-200 mb-12 leading-relaxed">
          ✨ Experience the <span className="text-yellow-400 font-semibold">cosmic</span> future of trading ✨<br />
          🌟 Where <span className="text-pink-400 font-semibold">algorithms</span> meet the <span className="text-blue-400 font-semibold">universe</span> 🌟
        </p>

        {/* Animated Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-6 justify-center items-center mb-16">
          <button className="group relative px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full text-white font-semibold text-lg transition-all duration-300 hover:scale-105 hover:shadow-2xl animate-cosmic-glow">
            <span className="flex items-center">
              <Rocket className="h-6 w-6 mr-2 group-hover:animate-bounce" />
              Launch Trading 🚀
            </span>
          </button>
          
          <button className="group relative px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full text-white font-semibold text-lg transition-all duration-300 hover:scale-105 hover:shadow-2xl">
            <span className="flex items-center">
              <Sparkles className="h-6 w-6 mr-2 group-hover:animate-spin" />
              Explore Universe 🌌
            </span>
          </button>
        </div>

        {/* Floating Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div className="text-center p-6 bg-white/10 backdrop-blur-md rounded-2xl border border-purple-400/30 animate-float">
            <div className="text-3xl mb-2">💎</div>
            <div className="text-2xl font-bold text-purple-400">₹50M+</div>
            <div className="text-sm text-purple-200">Portfolio Value</div>
          </div>
          
          <div className="text-center p-6 bg-white/10 backdrop-blur-md rounded-2xl border border-blue-400/30 animate-float" style={{ animationDelay: '0.5s' }}>
            <div className="text-3xl mb-2">⚡</div>
            <div className="text-2xl font-bold text-blue-400">10K+</div>
            <div className="text-sm text-blue-200">Active Trades</div>
          </div>
          
          <div className="text-center p-6 bg-white/10 backdrop-blur-md rounded-2xl border border-pink-400/30 animate-float" style={{ animationDelay: '1s' }}>
            <div className="text-3xl mb-2">🎯</div>
            <div className="text-2xl font-bold text-pink-400">85.2%</div>
            <div className="text-sm text-pink-200">Success Rate</div>
          </div>
          
          <div className="text-center p-6 bg-white/10 backdrop-blur-md rounded-2xl border border-yellow-400/30 animate-float" style={{ animationDelay: '1.5s' }}>
            <div className="text-3xl mb-2">🌟</div>
            <div className="text-2xl font-bold text-yellow-400">24/7</div>
            <div className="text-sm text-yellow-200">Cosmic Trading</div>
          </div>
        </div>
      </div>

      {/* Interactive Cosmic Elements */}
      <div className="absolute bottom-10 left-10 text-6xl animate-bounce cursor-pointer hover:scale-110 transition-transform">
        🛸
      </div>
      <div className="absolute top-20 right-20 text-4xl animate-spin cursor-pointer hover:scale-110 transition-transform" style={{ animationDuration: '10s' }}>
        🌌
      </div>
      <div className="absolute bottom-20 right-20 text-5xl animate-pulse cursor-pointer hover:scale-110 transition-transform">
        👨‍🚀
      </div>
    </div>
  );
}

export function CosmicFeatureCard({ 
  icon, 
  title, 
  description, 
  emoji 
}: { 
  icon: React.ReactNode; 
  title: string; 
  description: string; 
  emoji: string;
}) {
  return (
    <div className="group relative p-8 bg-gradient-to-br from-purple-900/50 to-blue-900/50 backdrop-blur-md rounded-2xl border border-purple-400/30 hover:border-purple-400/60 transition-all duration-300 hover:scale-105 hover:shadow-2xl animate-cosmic-glow">
      {/* Background cosmic effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-500/10 to-pink-500/10 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      
      <div className="relative z-10">
        <div className="flex items-center justify-between mb-6">
          <div className="p-3 bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl group-hover:animate-pulse">
            {icon}
          </div>
          <div className="text-4xl group-hover:animate-bounce">{emoji}</div>
        </div>
        
        <h3 className="text-xl font-bold text-white mb-4 group-hover:text-purple-300 transition-colors">
          {title}
        </h3>
        
        <p className="text-purple-200 group-hover:text-white transition-colors">
          {description}
        </p>

        {/* Sparkle effect on hover */}
        <div className="absolute top-2 right-2 text-yellow-400 opacity-0 group-hover:opacity-100 transition-opacity animate-sparkle">
          ✨
        </div>
      </div>
    </div>
  );
}