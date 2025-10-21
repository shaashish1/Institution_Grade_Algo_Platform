'use client';

import React, { useState } from 'react';
import { Sun, Moon, Sparkles, Palette, Settings } from 'lucide-react';
import { useTheme } from './theme-provider';
import { DoodleShowcase, DoodleThemeEnhancer } from './doodle-showcase';

export function ThemeSwitcher() {
  const { theme, setTheme } = useTheme();
  const [isExpanded, setIsExpanded] = useState(false);

  const themes = [
    { id: 'light', name: 'Light', icon: Sun, color: 'bg-yellow-500' },
    { id: 'dark', name: 'Dark', icon: Moon, color: 'bg-slate-700' },
    { id: 'cosmic', name: 'Cosmic', icon: Sparkles, color: 'bg-purple-600' },
    { id: 'doodle', name: 'Doodle ✨', icon: Palette, color: 'bg-gradient-to-r from-pink-500 to-orange-500' }
  ];

  const currentTheme = themes.find(t => t.id === theme) || themes[1];

  return (
    <div className="relative">
      {/* Compact Mode - Show only current theme */}
      {!isExpanded && (
        <button
          onClick={() => setIsExpanded(true)}
          className="
            flex items-center space-x-2 px-4 py-3 
            bg-white/10 dark:bg-slate-800/80 backdrop-blur-md 
            rounded-xl border border-white/20 dark:border-slate-700
            shadow-xl hover:shadow-2xl transition-all duration-300
            text-slate-800 dark:text-white
            hover:bg-white/20 dark:hover:bg-slate-700/80
            group
          "
          title="Theme Settings"
        >
          <div className={`w-4 h-4 rounded-full ${currentTheme.color} shadow-sm`} />
          <currentTheme.icon className="h-5 w-5" />
          <Settings className="h-4 w-4 opacity-60 group-hover:opacity-100 transition-opacity" />
        </button>
      )}

      {/* Expanded Mode - Show all themes */}
      {isExpanded && (
        <div className="
          flex items-center space-x-2 p-2 
          bg-white/15 dark:bg-slate-800/90 backdrop-blur-md 
          rounded-xl border border-white/30 dark:border-slate-700
          shadow-2xl animate-in fade-in-0 zoom-in-95 duration-200
        ">
          {themes.map(({ id, name, icon: Icon, color }) => (
            <button
              key={id}
              onClick={() => {
                setTheme(id as any);
                setIsExpanded(false);
              }}
              className={`
                flex items-center space-x-2 px-3 py-2 rounded-lg transition-all duration-200
                ${theme === id 
                  ? 'bg-blue-500/20 text-blue-600 dark:text-blue-400 shadow-lg scale-105 ring-2 ring-blue-500/30' 
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-800 dark:hover:text-white hover:bg-white/20 dark:hover:bg-slate-700/50'
                }
              `}
              title={`Switch to ${name} theme`}
            >
              <div className={`w-3 h-3 rounded-full ${color} shadow-sm`} />
              <Icon className="h-4 w-4" />
              <span className="text-sm font-medium hidden md:inline">{name}</span>
            </button>
          ))}
          <button
            onClick={() => setIsExpanded(false)}
            className="
              px-2 py-2 rounded-lg transition-all duration-200
              text-slate-500 hover:text-slate-700 dark:hover:text-slate-300
              hover:bg-white/20 dark:hover:bg-slate-700/50
            "
            title="Close theme selector"
          >
            ✕
          </button>
        </div>
      )}
      
      {/* Enhanced Doodle Theme Components */}
      <DoodleShowcase isActive={theme === 'doodle'} />
      {theme === 'doodle' && <DoodleThemeEnhancer />}
    </div>
  );
}