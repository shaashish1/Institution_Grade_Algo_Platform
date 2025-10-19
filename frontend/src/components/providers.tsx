'use client';

import React from 'react';

// Simple providers setup without external dependencies for now
export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-slate-900 text-white">
      {children}
    </div>
  );
}