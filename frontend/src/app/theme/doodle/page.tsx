'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowRight, Palette, Sparkles, Heart, Star, Download, Play } from 'lucide-react';
import { CreativeDoodleButton, DoodleCard } from '@/components/theme/doodle-showcase';

export default function DoodleThemePage() {
  return (
    <div className="min-h-screen bg-slate-900 text-white relative overflow-hidden">
      {/* Enhanced Background for Doodle Theme Demo */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900/50 via-pink-900/30 to-orange-900/50" />
      
      <div className="relative z-10 max-w-7xl mx-auto px-6 py-12">
        {/* Breadcrumb */}
        <nav className="mb-8">
          <div className="flex items-center space-x-2 text-sm text-slate-400">
            <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
            <ArrowRight className="h-4 w-4" />
            <span className="text-white">Doodle Theme Showcase</span>
          </div>
        </nav>

        {/* Hero Section */}
        <section className="text-center mb-16">
          <div className="flex items-center justify-center space-x-3 mb-6">
            <Palette className="h-12 w-12 text-pink-400" />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-pink-500 via-purple-500 to-orange-500 bg-clip-text text-transparent">
              Doodle Theme Enhanced
            </h1>
            <Sparkles className="h-12 w-12 text-orange-400 animate-spin" style={{ animationDuration: '3s' }} />
          </div>
          <p className="text-xl text-slate-300 max-w-4xl mx-auto mb-8">
            Experience the most creative and visually stunning theme for your trading platform. 
            Enhanced with Figma-inspired design patterns, smooth animations, and glassmorphism effects.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <CreativeDoodleButton variant="primary">
              <Sparkles className="h-5 w-5" />
              <span>Try Doodle Theme</span>
            </CreativeDoodleButton>
            <CreativeDoodleButton variant="secondary">
              <Download className="h-5 w-5" />
              <span>Download Assets</span>
            </CreativeDoodleButton>
          </div>
        </section>

        {/* Features Grid */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-center mb-12 bg-gradient-to-r from-cyan-400 to-pink-400 bg-clip-text text-transparent">
            Enhanced Features
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <DoodleCard>
              <div className="text-center">
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-pink-500 to-orange-500 flex items-center justify-center">
                  <Sparkles className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Glassmorphism Design</h3>
                <p className="text-slate-300">Beautiful glass-like cards with backdrop blur effects and subtle transparency</p>
              </div>
            </DoodleCard>

            <DoodleCard>
              <div className="text-center">
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center">
                  <Heart className="h-8 w-8 text-white animate-pulse" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Smooth Animations</h3>
                <p className="text-slate-300">Buttery smooth transitions and micro-interactions for delightful user experience</p>
              </div>
            </DoodleCard>

            <DoodleCard>
              <div className="text-center">
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-yellow-400 to-pink-500 flex items-center justify-center">
                  <Star className="h-8 w-8 text-white animate-spin" style={{ animationDuration: '2s' }} />
                </div>
                <h3 className="text-xl font-semibold mb-2">Creative Gradients</h3>
                <p className="text-slate-300">Vibrant gradient combinations that bring energy and life to your interface</p>
              </div>
            </DoodleCard>

            <DoodleCard>
              <div className="text-center">
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-cyan-400 to-purple-500 flex items-center justify-center">
                  <Palette className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Figma Integration</h3>
                <p className="text-slate-300">Designed with Figma MCP integration for seamless design-to-code workflow</p>
              </div>
            </DoodleCard>

            <DoodleCard>
              <div className="text-center">
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-orange-400 to-red-500 flex items-center justify-center">
                  <Play className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Interactive Elements</h3>
                <p className="text-slate-300">Hover effects, particle systems, and dynamic visual feedback</p>
              </div>
            </DoodleCard>

            <DoodleCard>
              <div className="text-center">
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-green-400 to-blue-500 flex items-center justify-center">
                  <ArrowRight className="h-8 w-8 text-white animate-bounce" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Performance Optimized</h3>
                <p className="text-slate-300">Lightweight CSS animations and efficient rendering for smooth performance</p>
              </div>
            </DoodleCard>
          </div>
        </section>

        {/* Demo Components */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-center mb-12 bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent">
            Interactive Demo
          </h2>
          
          <div className="space-y-8">
            {/* Button Showcase */}
            <DoodleCard className="text-center">
              <h3 className="text-xl font-semibold mb-6">Creative Buttons</h3>
              <div className="flex flex-wrap gap-4 justify-center">
                <CreativeDoodleButton variant="primary">Primary Action</CreativeDoodleButton>
                <CreativeDoodleButton variant="secondary">Secondary</CreativeDoodleButton>
                <CreativeDoodleButton variant="accent">Accent Style</CreativeDoodleButton>
              </div>
            </DoodleCard>

            {/* Form Elements */}
            <DoodleCard>
              <h3 className="text-xl font-semibold mb-6">Enhanced Form Elements</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium mb-2">Enhanced Input</label>
                  <input 
                    type="text" 
                    placeholder="Type something magical..." 
                    className="w-full px-4 py-3 rounded-xl bg-white/10 border border-white/20 backdrop-blur-sm focus:border-pink-400 transition-all"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Themed Select</label>
                  <select className="w-full px-4 py-3 rounded-xl bg-white/10 border border-white/20 backdrop-blur-sm focus:border-purple-400 transition-all">
                    <option value="">Choose option...</option>
                    <option value="1">Option 1</option>
                    <option value="2">Option 2</option>
                  </select>
                </div>
              </div>
            </DoodleCard>

            {/* Chart Placeholder */}
            <DoodleCard className="chart-container particle-bg">
              <h3 className="text-xl font-semibold mb-6">Enhanced Chart Visualization</h3>
              <div className="h-64 bg-gradient-to-br from-purple-500/10 to-pink-500/10 rounded-xl flex items-center justify-center border border-white/10">
                <div className="text-center">
                  <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-cyan-400 to-purple-500 flex items-center justify-center animate-pulse">
                    <Sparkles className="h-10 w-10 text-white" />
                  </div>
                  <p className="text-slate-300">Beautiful charts with glassmorphism effects</p>
                </div>
              </div>
            </DoodleCard>
          </div>
        </section>

        {/* How to Enable */}
        <section className="text-center">
          <DoodleCard className="max-w-2xl mx-auto">
            <h2 className="text-2xl font-bold mb-4 bg-gradient-to-r from-pink-400 to-orange-400 bg-clip-text text-transparent">
              How to Enable Doodle Theme
            </h2>
            <div className="space-y-4 text-left">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 rounded-full bg-gradient-to-r from-pink-500 to-orange-500 flex items-center justify-center text-sm font-bold">1</div>
                <p>Click the theme switcher in the top-right corner</p>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 rounded-full bg-gradient-to-r from-purple-500 to-cyan-500 flex items-center justify-center text-sm font-bold">2</div>
                <p>Select "Doodle ✨" from the theme options</p>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 rounded-full bg-gradient-to-r from-cyan-500 to-pink-500 flex items-center justify-center text-sm font-bold">3</div>
                <p>Enjoy the enhanced creative experience!</p>
              </div>
            </div>
            
            <div className="mt-6">
              <CreativeDoodleButton variant="accent">
                <Palette className="h-5 w-5" />
                <span>Switch to Doodle Theme Now</span>
              </CreativeDoodleButton>
            </div>
          </DoodleCard>
        </section>
      </div>
    </div>
  );
}