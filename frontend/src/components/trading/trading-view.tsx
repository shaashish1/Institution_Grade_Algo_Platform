'use client';

import React, { useState } from 'react';
import { TradingChart } from './trading-chart';
import { OrderBook } from './order-book';
import { TradingPanel } from './trading-panel';
import { MarketData } from './market-data';
import { RecentTrades } from './recent-trades';

export function TradingView() {
  const [selectedSymbol, setSelectedSymbol] = useState('BTC/USDT');

  return (
    <div className="grid grid-cols-12 gap-6 h-full">
      {/* Market Data Header */}
      <div className="col-span-12">
        <MarketData symbol={selectedSymbol} onSymbolChange={setSelectedSymbol} />
      </div>

      {/* Main Chart */}
      <div className="col-span-8">
        <TradingChart symbol={selectedSymbol} />
      </div>

      {/* Order Book */}
      <div className="col-span-4">
        <OrderBook symbol={selectedSymbol} />
      </div>

      {/* Trading Panel */}
      <div className="col-span-8">
        <TradingPanel symbol={selectedSymbol} />
      </div>

      {/* Recent Trades */}
      <div className="col-span-4">
        <RecentTrades symbol={selectedSymbol} />
      </div>
    </div>
  );
}