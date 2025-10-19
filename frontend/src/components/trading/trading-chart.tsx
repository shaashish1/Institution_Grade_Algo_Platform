'use client';

import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface TradingChartProps {
  symbol: string;
}

// Mock data for demonstration
const generateMockData = () => {
  const data = [];
  const now = Date.now();
  let price = 45000 + Math.random() * 10000;
  
  for (let i = 100; i >= 0; i--) {
    const timestamp = now - i * 60000; // 1 minute intervals
    price += (Math.random() - 0.5) * 1000;
    data.push({
      time: new Date(timestamp).toLocaleTimeString(),
      price: Math.max(price, 30000),
      volume: Math.random() * 1000,
    });
  }
  return data;
};

export function TradingChart({ symbol }: TradingChartProps) {
  const [data, setData] = useState(generateMockData());
  const [timeframe, setTimeframe] = useState('1m');

  useEffect(() => {
    const interval = setInterval(() => {
      setData(generateMockData());
    }, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  const currentPrice = data[data.length - 1]?.price || 0;
  const previousPrice = data[data.length - 2]?.price || 0;
  const priceChange = currentPrice - previousPrice;
  const priceChangePercent = ((priceChange / previousPrice) * 100).toFixed(2);

  return (
    <div className="bg-slate-900 rounded-lg border border-slate-700 p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-xl font-bold text-white">{symbol} Chart</h3>
          <div className="flex items-center space-x-4 mt-2">
            <span className="text-2xl font-bold text-white">
              ${currentPrice.toLocaleString(undefined, { minimumFractionDigits: 2 })}
            </span>
            <span className={`text-sm font-medium ${
              priceChange >= 0 ? 'text-green-400' : 'text-red-400'
            }`}>
              {priceChange >= 0 ? '+' : ''}${priceChange.toFixed(2)} ({priceChangePercent}%)
            </span>
          </div>
        </div>
        
        <div className="flex space-x-2">
          {['1m', '5m', '15m', '1h', '4h', '1d'].map((tf) => (
            <button
              key={tf}
              onClick={() => setTimeframe(tf)}
              className={`px-3 py-1 rounded text-sm transition-colors ${
                timeframe === tf
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-800 text-slate-400 hover:text-white'
              }`}
            >
              {tf}
            </button>
          ))}
        </div>
      </div>

      <div className="h-96">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis 
              dataKey="time" 
              stroke="#9ca3af"
              fontSize={12}
            />
            <YAxis 
              stroke="#9ca3af"
              fontSize={12}
              domain={['dataMin - 1000', 'dataMax + 1000']}
              tickFormatter={(value: number) => `$${value.toLocaleString()}`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #475569',
                borderRadius: '8px',
                color: '#ffffff'
              }}
              formatter={(value: number) => [`$${value.toFixed(2)}`, 'Price']}
            />
            <Line
              type="monotone"
              dataKey="price"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4, fill: '#3b82f6' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}