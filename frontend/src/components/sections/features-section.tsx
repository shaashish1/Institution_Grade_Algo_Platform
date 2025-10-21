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
  Smartphone,
  LucideIcon
} from 'lucide-react';
import { useTheme } from '../theme/theme-provider';

// Feature interface
interface Feature {
  icon: LucideIcon;
  title: string;
  description: string;
  gradient: string;
  delay: string;
  emoji: string;
}

// Doodle Feature Card Component
interface DoodleFeatureCardProps {
  emoji: string;
  title: string;
  description: string;
}

function DoodleFeatureCard({ emoji, title, description }: DoodleFeatureCardProps) {
  return (
    <div className="group relative bg-white/90 backdrop-blur-sm border-3 border-pink-300 hover:border-orange-400 rounded-2xl p-8 transition-all duration-300 transform hover:scale-105 hover:rotate-1 shadow-lg hover:shadow-2xl">
      {/* Emoji Icon */}
      <div className="text-5xl mb-4 transform group-hover:scale-110 transition-transform duration-300">
        {emoji}
      </div>
      
      {/* Title */}
      <h3 className="text-2xl font-bold text-slate-800 mb-4 font-handwriting">
        {title}
      </h3>
      
      {/* Description */}
      <p className="text-slate-600 leading-relaxed font-handwriting">
        {description}
      </p>
      
      {/* Decorative elements */}
      <div className="absolute top-4 right-4 w-3 h-3 bg-yellow-400 rounded-full animate-bounce"></div>
      <div className="absolute bottom-4 left-4 w-2 h-2 bg-pink-400 rounded-full animate-pulse"></div>
    </div>
  );
}

// Main features configuration
const features: Feature[] = [
  {
    icon: TrendingUp,
    title: 'Real-Time Trading',
    description: 'Execute trades instantly with live market data and advanced order types across multiple exchanges.',
    gradient: 'from-blue-500 to-cyan-500',
    delay: 'delay-0',
    emoji: '📈'
  },
  {
    icon: Brain,
    title: 'AI-Powered Strategies',
    description: 'Create and deploy sophisticated trading algorithms with machine learning capabilities.',
    gradient: 'from-purple-500 to-pink-500',
    delay: 'delay-100',
    emoji: '🧠'
  },
  {
    icon: Shield,
    title: 'Risk Management',
    description: 'Advanced risk controls with position sizing, stop-loss, and portfolio protection features.',
    gradient: 'from-green-500 to-emerald-500',
    delay: 'delay-200',
    emoji: '🛡️'
  },
  {
    icon: BarChart3,
    title: 'Advanced Analytics',
    description: 'Comprehensive performance analytics with detailed reporting and backtesting capabilities.',
    gradient: 'from-orange-500 to-red-500',
    delay: 'delay-300',
    emoji: '📊'
  },
  {
    icon: Wallet,
    title: 'Portfolio Management',
    description: 'Unified portfolio view across all exchanges with automatic rebalancing and optimization.',
    gradient: 'from-indigo-500 to-purple-500',
    delay: 'delay-400',
    emoji: '💼'
  },
  {
    icon: Globe,
    title: 'Multi-Exchange Support',
    description: 'Connect to 100+ cryptocurrency exchanges and major stock markets worldwide.',
    gradient: 'from-teal-500 to-blue-500',
    delay: 'delay-500',
    emoji: '🌍'
  }
];

// Additional features list
const additionalFeatures = [
  { icon: Clock, text: '24/7 Monitoring' },
  { icon: Lock, text: 'Bank-Grade Security' },
  { icon: Smartphone, text: 'Mobile Trading' },
  { icon: Users, text: 'Community Features' },
  { icon: Target, text: 'Precision Execution' }
];

// Theme configuration helper
const themeConfig = {
  light: {
    background: 'bg-gradient-to-br from-blue-50 to-purple-50',
    text: 'text-slate-900',
    subtitle: 'text-slate-600',
    card: 'bg-white/80 backdrop-blur-sm border border-slate-200',
    badge: 'bg-blue-100 border border-blue-200 text-blue-600',
    hoverCard: 'bg-slate-100',
    additionalFeaturesBg: 'bg-slate-200 group-hover:bg-blue-500',
    additionalFeaturesText: 'text-slate-600 group-hover:text-white',
    additionalFeaturesHover: 'text-slate-900'
  },
  doodle: {
    background: 'bg-gradient-to-br from-orange-50 to-pink-50',
    text: 'text-slate-800',
    subtitle: 'text-slate-600',
    card: 'bg-white/90 backdrop-blur-sm border-3 border-pink-300',
    badge: 'bg-pink-200 border-2 border-pink-400 text-pink-600',
    hoverCard: 'bg-pink-50',
    additionalFeaturesBg: 'bg-pink-200 group-hover:bg-orange-500',
    additionalFeaturesText: 'text-pink-600 group-hover:text-white',
    additionalFeaturesHover: 'text-slate-800'
  },
  cosmic: {
    background: 'bg-gradient-to-br from-slate-950 to-purple-950',
    text: 'text-white',
    subtitle: 'text-slate-300',
    card: 'bg-slate-800/50 backdrop-blur-sm border border-slate-700',
    badge: 'bg-blue-500/10 border border-blue-500/20 text-blue-400',
    hoverCard: 'bg-slate-700/50',
    additionalFeaturesBg: 'bg-slate-700 group-hover:bg-blue-500',
    additionalFeaturesText: 'text-slate-300 group-hover:text-white',
    additionalFeaturesHover: 'text-white'
  },
  dark: {
    background: 'bg-slate-900',
    text: 'text-white',
    subtitle: 'text-slate-300',
    card: 'bg-slate-800/50 backdrop-blur-sm border border-slate-700',
    badge: 'bg-blue-500/10 border border-blue-500/20 text-blue-400',
    hoverCard: 'bg-slate-700/50',
    additionalFeaturesBg: 'bg-slate-700 group-hover:bg-blue-500',
    additionalFeaturesText: 'text-slate-300 group-hover:text-white',
    additionalFeaturesHover: 'text-white'
  }
};


export function FeaturesSection() {
  const { theme } = useTheme();
  const config = themeConfig[theme as keyof typeof themeConfig] || themeConfig.dark;

  // Doodle theme has its own unique layout
  if (theme === 'doodle') {
    return (
      <section className={`relative py-24 overflow-hidden ${config.background}`}>
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Section Header */}
          <div className="text-center mb-20">
            <div className={`inline-flex items-center space-x-2 ${config.badge} rounded-full px-6 py-2 mb-6 transform rotate-1`}>
              <Zap className="h-4 w-4" />
              <span className="text-sm font-bold font-handwriting">Awesome Features!</span>
            </div>
            
            <h2 className="text-4xl md:text-6xl font-bold text-slate-800 mb-6 font-handwriting">
              Everything You Need to
              <span className="block bg-gradient-to-r from-pink-500 via-orange-500 to-yellow-500 bg-clip-text text-transparent">
                Trade Like a Pro! 🚀
              </span>
            </h2>
            
            <p className={`text-xl ${config.subtitle} max-w-3xl mx-auto font-handwriting`}>
              Our platform combines fun design with powerful technology to make 
              trading both enjoyable and profitable! ✨
            </p>
          </div>

          {/* Doodle Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature) => (
              <DoodleFeatureCard
                key={feature.title}
                emoji={feature.emoji}
                title={feature.title}
                description={feature.description}
              />
            ))}
          </div>

          {/* Doodle CTA */}
          <div className="text-center mt-16">
            <div className="inline-flex flex-col sm:flex-row gap-6">
              <button className="bg-gradient-to-r from-pink-500 to-orange-500 hover:from-pink-600 hover:to-orange-600 text-white px-8 py-4 rounded-full font-bold text-lg transition-all duration-300 transform hover:scale-105 hover:rotate-2 shadow-lg border-3 border-pink-400">
                🎨 Start Creating!
              </button>
              <button className="bg-white border-3 border-yellow-400 hover:bg-yellow-50 text-slate-800 px-8 py-4 rounded-full font-bold text-lg transition-all duration-300 transform hover:scale-105 hover:-rotate-1 shadow-lg">
                📚 Learn More
              </button>
            </div>
          </div>
        </div>
      </section>
    );
  }

  // Default theme rendering
  return (
    <section className={`relative py-24 overflow-hidden ${config.background}`}>
      {/* Background Effects */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-20">
          <div className={`inline-flex items-center space-x-2 ${config.badge} rounded-full px-6 py-2 mb-6`}>
            <Zap className="h-4 w-4" />
            <span className="text-sm font-medium">Powerful Features</span>
          </div>
          
          <h2 className={`text-4xl md:text-6xl font-bold ${config.text} mb-6`}>
            Everything You Need to
            <span className="block bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              Trade Successfully
            </span>
          </h2>
          
          <p className={`text-xl ${config.subtitle} max-w-3xl mx-auto`}>
            Our platform combines cutting-edge technology with intuitive design to deliver 
            a trading experience that's both powerful and accessible.
          </p>
        </div>

        {/* Main Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <div
                key={feature.title}
                className={`group relative ${config.card} rounded-2xl p-8 hover:border-slate-600 transition-all duration-500 hover:transform hover:scale-105 animate-fade-in ${feature.delay}`}
              >
                {/* Hover Effect */}
                <div className="absolute inset-0 bg-gradient-to-r opacity-0 group-hover:opacity-10 transition-opacity duration-500 rounded-2xl from-blue-500 to-purple-500"></div>
                
                {/* Icon */}
                <div className={`w-14 h-14 rounded-xl bg-gradient-to-r ${feature.gradient} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <Icon className="h-7 w-7 text-white" />
                </div>

                {/* Content */}
                <h3 className={`text-xl font-semibold ${config.text} mb-4 group-hover:text-blue-400 transition-colors`}>
                  {feature.title}
                </h3>
                <p className={`${config.subtitle} leading-relaxed`}>
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
        <div className={`${config.card} rounded-2xl p-8`}>
          <h3 className={`text-2xl font-bold ${config.text} text-center mb-8`}>
            And Much More...
          </h3>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
            {additionalFeatures.map((item) => {
              const Icon = item.icon;
              return (
                <div
                  key={item.text}
                  className={`flex flex-col items-center space-y-3 p-4 rounded-lg hover:${config.hoverCard} transition-colors group`}
                >
                  <div className={`w-12 h-12 ${config.additionalFeaturesBg} rounded-lg flex items-center justify-center transition-colors duration-300`}>
                    <Icon className={`h-6 w-6 ${config.additionalFeaturesText}`} />
                  </div>
                  <span className={`text-sm ${config.subtitle} group-hover:${config.additionalFeaturesHover} text-center transition-colors`}>
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
            <button className={`${theme === 'light' ? 'bg-white hover:bg-slate-50 text-slate-900 border border-slate-300 hover:border-slate-400' : 'bg-slate-800 hover:bg-slate-700 text-white border border-slate-600 hover:border-slate-500'} px-8 py-4 rounded-lg font-semibold transition-colors`}>
              View All Features
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}