'use client';

import React from 'react';
import { Sun, Moon, Sparkles } from 'lucide-react';
import { useTheme } from './theme-provider';

export function ThemeSwitcher() {
  const { theme, setTheme } = useTheme();

  const themes = [
    { id: 'light', name: 'Light', icon: Sun, color: 'bg-yellow-500' },
    { id: 'dark', name: 'Dark', icon: Moon, color: 'bg-slate-700' },
    { id: 'cosmic', name: 'Cosmic', icon: Sparkles, color: 'bg-purple-600' }
  ];

  return (
    <div className="flex items-center space-x-2 p-2 bg-slate-800/50 backdrop-blur-sm rounded-lg border border-slate-700">
      {themes.map(({ id, name, icon: Icon, color }) => (
        <button
          key={id}
          onClick={() => setTheme(id as any)}
          className={`
            flex items-center space-x-2 px-3 py-2 rounded-md transition-all duration-200
            ${theme === id 
              ? 'bg-white/20 text-white shadow-lg scale-105' 
              : 'text-slate-400 hover:text-white hover:bg-white/10'
            }
          `}
          title={`Switch to ${name} theme`}
        >
          <div className={`w-3 h-3 rounded-full ${color}`} />
          <Icon className="h-4 w-4" />
          <span className="text-sm font-medium hidden sm:inline">{name}</span>
        </button>
      ))}
    </div>
  );
}