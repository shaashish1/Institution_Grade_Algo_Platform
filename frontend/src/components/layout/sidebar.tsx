'use client';

import React from 'react';
import { 
  TrendingUp, 
  Wallet, 
  BarChart3, 
  Settings, 
  Brain,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';

interface SidebarProps {
  isOpen: boolean;
  currentView: string;
  onViewChange: (view: string) => void;
  onToggle: () => void;
}

const menuItems = [
  { id: 'trading', label: 'Trading', icon: TrendingUp },
  { id: 'portfolio', label: 'Portfolio', icon: Wallet },
  { id: 'strategies', label: 'Strategies', icon: Brain },
  { id: 'analytics', label: 'Analytics', icon: BarChart3 },
  { id: 'settings', label: 'Settings', icon: Settings },
];

export function Sidebar({ isOpen, currentView, onViewChange, onToggle }: SidebarProps) {
  return (
    <div className={`bg-slate-950 border-r border-slate-700 transition-all duration-300 ${
      isOpen ? 'w-64' : 'w-16'
    }`}>
      <div className="flex flex-col h-full">
        {/* Logo/Brand */}
        <div className="p-4 border-b border-slate-700">
          <div className="flex items-center justify-between">
            {isOpen && (
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <TrendingUp className="h-5 w-5 text-white" />
                </div>
                <span className="font-bold text-white">AlgoProject</span>
              </div>
            )}
            <button
              onClick={onToggle}
              className="p-1 rounded-lg bg-slate-800 hover:bg-slate-700 transition-colors"
            >
              {isOpen ? (
                <ChevronLeft className="h-4 w-4" />
              ) : (
                <ChevronRight className="h-4 w-4" />
              )}
            </button>
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentView === item.id;
              
              return (
                <li key={item.id}>
                  <button
                    onClick={() => onViewChange(item.id)}
                    className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                      isActive
                        ? 'bg-blue-600 text-white'
                        : 'text-slate-400 hover:text-white hover:bg-slate-800'
                    }`}
                  >
                    <Icon className="h-5 w-5" />
                    {isOpen && <span>{item.label}</span>}
                  </button>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-slate-700">
          {isOpen && (
            <div className="text-center">
              <p className="text-xs text-slate-500">Version 1.0.0</p>
              <p className="text-xs text-slate-500">Professional Edition</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}