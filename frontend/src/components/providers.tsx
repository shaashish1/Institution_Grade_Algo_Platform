'use client';

import React from 'react';
import { ThemeProvider } from './theme/theme-provider';

// Providers setup with ThemeProvider
export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider>
      <div className="min-h-screen bg-slate-900 text-white">
        {children}
      </div>
    </ThemeProvider>
  );
}