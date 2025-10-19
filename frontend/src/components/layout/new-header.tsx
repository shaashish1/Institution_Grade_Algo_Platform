'use client';

import React, { useState } from 'react';
import { 
  Menu, 
  X, 
  TrendingUp, 
  BarChart3, 
  Wallet, 
  Brain, 
  HelpCircle, 
  Star,
  ChevronDown,
  Play,
  Shield,
  Zap,
  Users,
  BookOpen,
  Phone,
  LogIn,
  UserPlus
} from 'lucide-react';

interface HeaderProps {
  onSidebarToggle?: () => void;
  currentView?: string;
}

const megaMenuData = {
  trading: {
    title: 'Trading',
    items: [
      { name: 'Live Trading', description: 'Real-time crypto & stock trading', icon: TrendingUp, href: '/trading' },
      { name: 'Market Analysis', description: 'Technical & fundamental analysis', icon: BarChart3, href: '/analysis' },
      { name: 'Order Management', description: 'Advanced order types', icon: Zap, href: '/orders' },
      { name: 'Risk Management', description: 'Portfolio protection tools', icon: Shield, href: '/risk' },
    ]
  },
  features: {
    title: 'Features',
    items: [
      { name: 'Portfolio Management', description: 'Track your investments', icon: Wallet, href: '/portfolio' },
      { name: 'Strategy Builder', description: 'Create custom algorithms', icon: Brain, href: '/strategies' },
      { name: 'Backtesting', description: 'Test strategies on historical data', icon: BarChart3, href: '/backtest' },
      { name: 'Analytics', description: 'Performance insights', icon: Star, href: '/analytics' },
    ]
  },
  help: {
    title: 'Help & Support',
    items: [
      { name: 'Getting Started', description: 'Quick start guide', icon: Play, href: '/help/getting-started' },
      { name: 'Documentation', description: 'Complete user manual', icon: BookOpen, href: '/help/docs' },
      { name: 'Video Tutorials', description: 'Learn with videos', icon: Play, href: '/help/videos' },
      { name: 'Contact Support', description: '24/7 customer support', icon: Phone, href: '/help/contact' },
    ]
  }
};

export function Header({ onSidebarToggle, currentView }: HeaderProps = {}) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-slate-900/95 backdrop-blur-sm border-b border-slate-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="relative">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <TrendingUp className="h-6 w-6 text-white" />
              </div>
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">AlgoProject</h1>
              <p className="text-xs text-slate-400">Institution Grade</p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {Object.entries(megaMenuData).map(([key, menu]) => (
              <div
                key={key}
                className="relative group"
                onMouseEnter={() => setActiveDropdown(key)}
                onMouseLeave={() => setActiveDropdown(null)}
              >
                <button className="flex items-center space-x-1 text-slate-300 hover:text-white transition-colors py-2">
                  <span>{menu.title}</span>
                  <ChevronDown className="h-4 w-4" />
                </button>

                {/* Mega Menu Dropdown */}
                {activeDropdown === key && (
                  <div className="absolute top-full left-0 mt-2 w-80 bg-slate-800 border border-slate-700 rounded-lg shadow-xl">
                    <div className="p-6">
                      <h3 className="text-lg font-semibold text-white mb-4">{menu.title}</h3>
                      <div className="grid gap-3">
                        {menu.items.map((item) => {
                          const Icon = item.icon;
                          return (
                            <a
                              key={item.name}
                              href={item.href}
                              className="flex items-start space-x-3 p-3 rounded-lg hover:bg-slate-700 transition-colors group"
                            >
                              <div className="flex-shrink-0 w-10 h-10 bg-blue-500/10 rounded-lg flex items-center justify-center group-hover:bg-blue-500/20 transition-colors">
                                <Icon className="h-5 w-5 text-blue-400" />
                              </div>
                              <div>
                                <h4 className="text-white font-medium">{item.name}</h4>
                                <p className="text-sm text-slate-400">{item.description}</p>
                              </div>
                            </a>
                          );
                        })}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </nav>

          {/* Right side actions */}
          <div className="flex items-center space-x-4">
            <button className="hidden md:flex items-center space-x-2 px-4 py-2 text-slate-300 hover:text-white transition-colors">
              <LogIn className="h-4 w-4" />
              <span>Login</span>
            </button>
            <button className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2 rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-200 flex items-center space-x-2">
              <UserPlus className="h-4 w-4" />
              <span>Get Started</span>
            </button>

            {/* Mobile menu button */}
            <button
              className="md:hidden p-2"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? (
                <X className="h-6 w-6 text-white" />
              ) : (
                <Menu className="h-6 w-6 text-white" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-slate-700">
            <div className="space-y-4">
              {Object.entries(megaMenuData).map(([key, menu]) => (
                <div key={key}>
                  <h3 className="text-white font-semibold mb-2">{menu.title}</h3>
                  <div className="space-y-2 pl-4">
                    {menu.items.map((item) => {
                      const Icon = item.icon;
                      return (
                        <a
                          key={item.name}
                          href={item.href}
                          className="flex items-center space-x-3 text-slate-300 hover:text-white transition-colors"
                        >
                          <Icon className="h-4 w-4" />
                          <span>{item.name}</span>
                        </a>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </header>
  );
}