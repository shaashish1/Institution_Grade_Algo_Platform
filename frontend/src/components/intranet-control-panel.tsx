'use client';

import React, { useState, useEffect } from 'react';
import { Shield, Lock, Users, Network, Monitor, Settings } from 'lucide-react';

interface IntranetConfig {
  domain: string;
  adminUsers: string[];
  allowedIPs: string[];
  securityLevel: 'low' | 'medium' | 'high';
  enableSSO: boolean;
  enableAuditLog: boolean;
}

interface NetworkInfo {
  localIP: string;
  serverIP: string;
  networkSpeed: string;
  latency: number;
  isIntranet: boolean;
}

export function IntranetControlPanel() {
  const [config, setConfig] = useState<IntranetConfig>({
    domain: 'corporate.algoproject.local',
    adminUsers: ['admin@company.com', 'it@company.com'],
    allowedIPs: ['192.168.1.0/24', '10.0.0.0/16'],
    securityLevel: 'high',
    enableSSO: true,
    enableAuditLog: true
  });

  const [networkInfo, setNetworkInfo] = useState<NetworkInfo>({
    localIP: '192.168.1.100',
    serverIP: '192.168.1.50',
    networkSpeed: '1 Gbps',
    latency: 2,
    isIntranet: true
  });

  const [activeUsers, setActiveUsers] = useState(45);
  const [securityAlerts, setSecurityAlerts] = useState(0);

  useEffect(() => {
    // Simulate real-time updates
    const interval = setInterval(() => {
      setActiveUsers(Math.floor(Math.random() * 20) + 40);
      setNetworkInfo(prev => ({
        ...prev,
        latency: Math.floor(Math.random() * 5) + 1
      }));
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const handleConfigUpdate = (key: keyof IntranetConfig, value: any) => {
    setConfig(prev => ({
      ...prev,
      [key]: value
    }));
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
            Intranet Control Panel
          </h1>
          <p className="text-slate-400">
            Manage corporate network access and security settings
          </p>
        </div>

        {/* Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <Users className="h-8 w-8 text-blue-400" />
              <span className="text-2xl font-bold text-white">{activeUsers}</span>
            </div>
            <h3 className="text-slate-400 text-sm">Active Users</h3>
            <div className="mt-2 flex items-center">
              <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse" />
              <span className="text-green-400 text-xs">Online</span>
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <Network className="h-8 w-8 text-green-400" />
              <span className="text-2xl font-bold text-white">{networkInfo.latency}ms</span>
            </div>
            <h3 className="text-slate-400 text-sm">Network Latency</h3>
            <div className="mt-2">
              <span className="text-green-400 text-xs">{networkInfo.networkSpeed}</span>
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <Shield className="h-8 w-8 text-purple-400" />
              <span className="text-2xl font-bold text-white">{securityAlerts}</span>
            </div>
            <h3 className="text-slate-400 text-sm">Security Alerts</h3>
            <div className="mt-2">
              <span className="text-green-400 text-xs">All Clear</span>
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <Monitor className="h-8 w-8 text-yellow-400" />
              <span className="text-2xl font-bold text-white">99.9%</span>
            </div>
            <h3 className="text-slate-400 text-sm">Uptime</h3>
            <div className="mt-2">
              <span className="text-green-400 text-xs">Excellent</span>
            </div>
          </div>
        </div>

        {/* Configuration Sections */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Network Configuration */}
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center">
              <Network className="h-5 w-5 mr-2 text-blue-400" />
              Network Configuration
            </h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Intranet Domain
                </label>
                <input
                  type="text"
                  value={config.domain}
                  onChange={(e) => handleConfigUpdate('domain', e.target.value)}
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Local Server IP
                </label>
                <input
                  type="text"
                  value={networkInfo.serverIP}
                  readOnly
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-slate-400"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Allowed IP Ranges
                </label>
                <div className="space-y-2">
                  {config.allowedIPs.map((ip, index) => (
                    <div key={index} className="flex items-center space-x-2">
                      <input
                        type="text"
                        value={ip}
                        onChange={(e) => {
                          const newIPs = [...config.allowedIPs];
                          newIPs[index] = e.target.value;
                          handleConfigUpdate('allowedIPs', newIPs);
                        }}
                        className="flex-1 px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Security Configuration */}
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center">
              <Shield className="h-5 w-5 mr-2 text-purple-400" />
              Security Configuration
            </h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Security Level
                </label>
                <select
                  value={config.securityLevel}
                  onChange={(e) => handleConfigUpdate('securityLevel', e.target.value)}
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                >
                  <option value="low">Low - Basic Authentication</option>
                  <option value="medium">Medium - Enhanced Security</option>
                  <option value="high">High - Maximum Security</option>
                </select>
              </div>

              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-slate-300">
                  Enable Single Sign-On (SSO)
                </label>
                <button
                  onClick={() => handleConfigUpdate('enableSSO', !config.enableSSO)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    config.enableSSO ? 'bg-purple-600' : 'bg-slate-700'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      config.enableSSO ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-slate-300">
                  Enable Audit Logging
                </label>
                <button
                  onClick={() => handleConfigUpdate('enableAuditLog', !config.enableAuditLog)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    config.enableAuditLog ? 'bg-purple-600' : 'bg-slate-700'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      config.enableAuditLog ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Administrator Users
                </label>
                <div className="space-y-2">
                  {config.adminUsers.map((user, index) => (
                    <input
                      key={index}
                      type="email"
                      value={user}
                      onChange={(e) => {
                        const newUsers = [...config.adminUsers];
                        newUsers[index] = e.target.value;
                        handleConfigUpdate('adminUsers', newUsers);
                      }}
                      className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-8 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <span className="text-slate-400 text-sm">
              Last updated: {new Date().toLocaleString()}
            </span>
          </div>
          
          <div className="flex items-center space-x-4">
            <button className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors">
              Export Config
            </button>
            <button className="px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-lg transition-colors">
              Apply Changes
            </button>
          </div>
        </div>

        {/* Network Diagnostics */}
        <div className="mt-8 bg-slate-900 rounded-xl p-6 border border-slate-800">
          <h2 className="text-xl font-bold text-white mb-6 flex items-center">
            <Monitor className="h-5 w-5 mr-2 text-green-400" />
            Network Diagnostics
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-400 mb-2">✓</div>
              <div className="text-sm text-slate-300">DNS Resolution</div>
              <div className="text-xs text-green-400">Operational</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-green-400 mb-2">✓</div>
              <div className="text-sm text-slate-300">Database Connection</div>
              <div className="text-xs text-green-400">Connected</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-green-400 mb-2">✓</div>
              <div className="text-sm text-slate-300">External APIs</div>
              <div className="text-xs text-green-400">Accessible</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}