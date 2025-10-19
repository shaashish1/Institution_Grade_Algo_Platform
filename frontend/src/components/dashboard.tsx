'use client';

import React, { useState } from 'react';
import { Header } from './layout/header';
import { Sidebar } from './layout/sidebar';
import { TradingView } from './trading/trading-view';
import { Portfolio } from './portfolio/portfolio';
import { Strategies } from './strategies/strategies';
import { Analytics } from './analytics/analytics';
import { Settings } from './settings/settings';

type ViewType = 'trading' | 'portfolio' | 'strategies' | 'analytics' | 'settings';

export function Dashboard() {
  const [currentView, setCurrentView] = useState<ViewType>('trading');
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const renderView = () => {
    switch (currentView) {
      case 'trading':
        return <TradingView />;
      case 'portfolio':
        return <Portfolio />;
      case 'strategies':
        return <Strategies />;
      case 'analytics':
        return <Analytics />;
      case 'settings':
        return <Settings />;
      default:
        return <TradingView />;
    }
  };

  return (
    <div className="flex h-screen bg-slate-900 text-white">
      <Sidebar 
        isOpen={sidebarOpen}
        currentView={currentView}
        onViewChange={(view: string) => setCurrentView(view as ViewType)}
        onToggle={() => setSidebarOpen(!sidebarOpen)}
      />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header 
          onSidebarToggle={() => setSidebarOpen(!sidebarOpen)}
          currentView={currentView}
        />
        
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-slate-800">
          <div className="container mx-auto px-6 py-8">
            {renderView()}
          </div>
        </main>
      </div>
    </div>
  );
}