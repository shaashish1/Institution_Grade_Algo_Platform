'use client';

import React, { useState, useEffect } from 'react';
import { 
  Wifi, 
  Database, 
  HardDrive, 
  Zap, 
  Settings, 
  RefreshCw,
  CheckCircle,
  AlertTriangle,
  Activity
} from 'lucide-react';

interface CacheMetrics {
  hitRate: number;
  missRate: number;
  totalRequests: number;
  cacheSize: string;
  lastCleared: string;
}

interface NetworkOptimization {
  compressionEnabled: boolean;
  cacheEnabled: boolean;
  cdnEnabled: boolean;
  prefetchEnabled: boolean;
  bandwidthOptimization: boolean;
}

export function NetworkOptimizer() {
  const [cacheMetrics, setCacheMetrics] = useState<CacheMetrics>({
    hitRate: 94.5,
    missRate: 5.5,
    totalRequests: 12450,
    cacheSize: '2.3 GB',
    lastCleared: '2 hours ago'
  });

  const [optimization, setOptimization] = useState<NetworkOptimization>({
    compressionEnabled: true,
    cacheEnabled: true,
    cdnEnabled: false, // Disabled for intranet
    prefetchEnabled: true,
    bandwidthOptimization: true
  });

  const [networkStats, setNetworkStats] = useState({
    bandwidth: '850 Mbps',
    latency: '2ms',
    packetLoss: '0.01%',
    throughput: '78%'
  });

  const [isOptimizing, setIsOptimizing] = useState(false);

  useEffect(() => {
    // Simulate real-time updates
    const interval = setInterval(() => {
      setCacheMetrics(prev => ({
        ...prev,
        hitRate: Math.max(90, Math.min(98, prev.hitRate + (Math.random() - 0.5) * 2)),
        totalRequests: prev.totalRequests + Math.floor(Math.random() * 50)
      }));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const handleOptimizationToggle = (key: keyof NetworkOptimization) => {
    setOptimization(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  const runOptimization = async () => {
    setIsOptimizing(true);
    
    // Simulate optimization process
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    setCacheMetrics(prev => ({
      ...prev,
      hitRate: Math.min(98, prev.hitRate + 2),
      lastCleared: 'just now'
    }));
    
    setIsOptimizing(false);
  };

  const clearCache = () => {
    setCacheMetrics(prev => ({
      ...prev,
      hitRate: 0,
      totalRequests: 0,
      cacheSize: '0 MB',
      lastCleared: 'just now'
    }));
    
    // Simulate cache rebuilding
    setTimeout(() => {
      setCacheMetrics(prev => ({
        ...prev,
        hitRate: 85,
        cacheSize: '150 MB'
      }));
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent mb-2">
            Network Optimizer
          </h1>
          <p className="text-slate-400">
            Optimize intranet performance and local network caching
          </p>
        </div>

        {/* Network Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <Wifi className="h-8 w-8 text-blue-400" />
              <span className="text-2xl font-bold text-white">{networkStats.bandwidth}</span>
            </div>
            <h3 className="text-slate-400 text-sm">Bandwidth</h3>
            <div className="mt-2">
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div className="bg-blue-400 h-2 rounded-full" style={{ width: '85%' }}></div>
              </div>
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <Zap className="h-8 w-8 text-green-400" />
              <span className="text-2xl font-bold text-white">{networkStats.latency}</span>
            </div>
            <h3 className="text-slate-400 text-sm">Latency</h3>
            <div className="mt-2 flex items-center">
              <CheckCircle className="h-4 w-4 text-green-400 mr-1" />
              <span className="text-green-400 text-xs">Excellent</span>
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <Activity className="h-8 w-8 text-purple-400" />
              <span className="text-2xl font-bold text-white">{networkStats.throughput}</span>
            </div>
            <h3 className="text-slate-400 text-sm">Throughput</h3>
            <div className="mt-2">
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div className="bg-purple-400 h-2 rounded-full" style={{ width: networkStats.throughput }}></div>
              </div>
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <AlertTriangle className="h-8 w-8 text-yellow-400" />
              <span className="text-2xl font-bold text-white">{networkStats.packetLoss}</span>
            </div>
            <h3 className="text-slate-400 text-sm">Packet Loss</h3>
            <div className="mt-2 flex items-center">
              <CheckCircle className="h-4 w-4 text-green-400 mr-1" />
              <span className="text-green-400 text-xs">Minimal</span>
            </div>
          </div>
        </div>

        {/* Optimization Controls */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Cache Management */}
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center">
              <Database className="h-5 w-5 mr-2 text-blue-400" />
              Cache Management
            </h2>
            
            <div className="space-y-4 mb-6">
              <div className="flex items-center justify-between">
                <span className="text-slate-300">Hit Rate</span>
                <span className="text-2xl font-bold text-green-400">{cacheMetrics.hitRate.toFixed(1)}%</span>
              </div>
              
              <div className="w-full bg-slate-700 rounded-full h-3">
                <div 
                  className="bg-gradient-to-r from-green-500 to-blue-500 h-3 rounded-full transition-all duration-1000"
                  style={{ width: `${cacheMetrics.hitRate}%` }}
                ></div>
              </div>
              
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-slate-400">Total Requests:</span>
                  <span className="text-white ml-2">{cacheMetrics.totalRequests.toLocaleString()}</span>
                </div>
                <div>
                  <span className="text-slate-400">Cache Size:</span>
                  <span className="text-white ml-2">{cacheMetrics.cacheSize}</span>
                </div>
                <div>
                  <span className="text-slate-400">Last Cleared:</span>
                  <span className="text-white ml-2">{cacheMetrics.lastCleared}</span>
                </div>
                <div>
                  <span className="text-slate-400">Miss Rate:</span>
                  <span className="text-white ml-2">{cacheMetrics.missRate.toFixed(1)}%</span>
                </div>
              </div>
            </div>

            <div className="flex space-x-3">
              <button
                onClick={clearCache}
                className="flex-1 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors flex items-center justify-center"
              >
                <HardDrive className="h-4 w-4 mr-2" />
                Clear Cache
              </button>
              <button
                onClick={runOptimization}
                disabled={isOptimizing}
                className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 text-white rounded-lg transition-colors flex items-center justify-center"
              >
                {isOptimizing ? (
                  <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                ) : (
                  <Zap className="h-4 w-4 mr-2" />
                )}
                {isOptimizing ? 'Optimizing...' : 'Optimize'}
              </button>
            </div>
          </div>

          {/* Network Optimization Settings */}
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center">
              <Settings className="h-5 w-5 mr-2 text-purple-400" />
              Optimization Settings
            </h2>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-slate-300 font-medium">Compression</label>
                  <p className="text-slate-400 text-sm">Reduce data transfer size</p>
                </div>
                <button
                  onClick={() => handleOptimizationToggle('compressionEnabled')}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    optimization.compressionEnabled ? 'bg-green-600' : 'bg-slate-700'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      optimization.compressionEnabled ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <label className="text-slate-300 font-medium">Local Caching</label>
                  <p className="text-slate-400 text-sm">Cache frequently accessed data</p>
                </div>
                <button
                  onClick={() => handleOptimizationToggle('cacheEnabled')}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    optimization.cacheEnabled ? 'bg-green-600' : 'bg-slate-700'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      optimization.cacheEnabled ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <label className="text-slate-300 font-medium">Resource Prefetching</label>
                  <p className="text-slate-400 text-sm">Preload likely needed resources</p>
                </div>
                <button
                  onClick={() => handleOptimizationToggle('prefetchEnabled')}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    optimization.prefetchEnabled ? 'bg-green-600' : 'bg-slate-700'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      optimization.prefetchEnabled ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <label className="text-slate-300 font-medium">Bandwidth Optimization</label>
                  <p className="text-slate-400 text-sm">Optimize for local network speed</p>
                </div>
                <button
                  onClick={() => handleOptimizationToggle('bandwidthOptimization')}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    optimization.bandwidthOptimization ? 'bg-green-600' : 'bg-slate-700'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      optimization.bandwidthOptimization ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>

              <div className="bg-slate-800 rounded-lg p-4 mt-4">
                <div className="flex items-center text-slate-400 text-sm">
                  <AlertTriangle className="h-4 w-4 mr-2 text-yellow-400" />
                  CDN disabled for intranet optimization
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Performance Recommendations */}
        <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
          <h2 className="text-xl font-bold text-white mb-6">Performance Recommendations</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-slate-800 rounded-lg p-4">
              <div className="flex items-center mb-3">
                <CheckCircle className="h-5 w-5 text-green-400 mr-2" />
                <span className="font-medium text-white">Optimal Cache Hit Rate</span>
              </div>
              <p className="text-slate-400 text-sm">
                Current cache hit rate of {cacheMetrics.hitRate.toFixed(1)}% is excellent for intranet operations.
              </p>
            </div>
            
            <div className="bg-slate-800 rounded-lg p-4">
              <div className="flex items-center mb-3">
                <CheckCircle className="h-5 w-5 text-green-400 mr-2" />
                <span className="font-medium text-white">Low Latency Network</span>
              </div>
              <p className="text-slate-400 text-sm">
                {networkStats.latency} latency indicates excellent local network performance.
              </p>
            </div>
            
            <div className="bg-slate-800 rounded-lg p-4">
              <div className="flex items-center mb-3">
                <CheckCircle className="h-5 w-5 text-green-400 mr-2" />
                <span className="font-medium text-white">Compression Active</span>
              </div>
              <p className="text-slate-400 text-sm">
                Data compression is reducing bandwidth usage by approximately 40%.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}