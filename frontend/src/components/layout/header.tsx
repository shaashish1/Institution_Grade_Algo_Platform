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
  Bell,
  Settings,
  User
} from 'lucide-react';

interface HeaderProps {
  onSidebarToggle?: () => void;
  currentView?: string;
}

export function Header({ onSidebarToggle, currentView }: HeaderProps = {}) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);
  const getPageTitle = () => {
    switch (currentView) {
      case 'trading':
        return 'Trading Dashboard';
      case 'portfolio':
        return 'Portfolio Management';
      case 'strategies':
        return 'Trading Strategies';
      case 'analytics':
        return 'Analytics & Reports';
      case 'settings':
        return 'Settings';
      default:
        return 'AlgoProject';
    }
  };

  return (
    <header className="bg-slate-900 border-b border-slate-700 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={onSidebarToggle}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 transition-colors"
          >
            <Menu className="h-5 w-5" />
          </button>
          
          <div className="flex items-center space-x-3">
            <TrendingUp className="h-8 w-8 text-blue-400" />
            <div>
              <h1 className="text-xl font-bold text-white">AlgoProject</h1>
              <p className="text-sm text-slate-400">{getPageTitle()}</p>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          {/* Real-time status */}
          <div className="flex items-center space-x-2 px-3 py-1 bg-green-900/30 border border-green-700 rounded-full">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-sm text-green-400">Live</span>
          </div>

          {/* Portfolio value */}
          <div className="flex items-center space-x-2 px-3 py-1 bg-slate-800 rounded-lg">
            <Wallet className="h-4 w-4 text-blue-400" />
            <span className="text-sm text-white font-medium">$12,345.67</span>
          </div>

          {/* Notifications */}
          <button className="relative p-2 rounded-lg bg-slate-800 hover:bg-slate-700 transition-colors">
            <Bell className="h-5 w-5" />
            <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></span>
          </button>

          {/* Settings */}
          <button className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 transition-colors">
            <Settings className="h-5 w-5" />
          </button>

          {/* User profile */}
          <button className="flex items-center space-x-2 p-2 rounded-lg bg-slate-800 hover:bg-slate-700 transition-colors">
            <User className="h-5 w-5" />
            <span className="text-sm hidden md:block">Trader</span>
          </button>
        </div>
      </div>
    </header>
  );
}