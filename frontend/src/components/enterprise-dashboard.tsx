'use client';

import React, { useState, useEffect } from 'react';
import { 
  Shield, 
  Users, 
  Activity, 
  Server, 
  Globe, 
  Lock,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock,
  Settings,
  Eye,
  Zap,
  BarChart3,
  Network,
  Building,
  UserCheck
} from 'lucide-react';

interface SystemStatus {
  cpu: number;
  memory: number;
  network: number;
  storage: number;
}

interface NetworkMetrics {
  bandwidth: string;
  latency: string;
  uptime: string;
  activeConnections: number;
}

interface SecurityAlert {
  id: string;
  type: 'warning' | 'critical' | 'info';
  message: string;
  timestamp: string;
}

export function EnterpriseDashboard() {
  const [systemStatus, setSystemStatus] = useState<SystemStatus>({
    cpu: 45,
    memory: 68,
    network: 23,
    storage: 82
  });

  const [networkMetrics, setNetworkMetrics] = useState<NetworkMetrics>({
    bandwidth: '850 Mbps',
    latency: '2ms',
    uptime: '99.98%',
    activeConnections: 247
  });

  const [securityAlerts, setSecurityAlerts] = useState<SecurityAlert[]>([
    {
      id: '1',
      type: 'warning',
      message: 'Unusual login pattern detected from IT Department',
      timestamp: '2 minutes ago'
    },
    {
      id: '2',
      type: 'info',
      message: 'Security scan completed successfully',
      timestamp: '15 minutes ago'
    },
    {
      id: '3',
      type: 'critical',
      message: 'Failed login attempts from external IP blocked',
      timestamp: '1 hour ago'
    }
  ]);

  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    // Update system metrics
    const metricsInterval = setInterval(() => {
      setSystemStatus(prev => ({
        cpu: Math.max(20, Math.min(90, prev.cpu + (Math.random() - 0.5) * 10)),
        memory: Math.max(30, Math.min(95, prev.memory + (Math.random() - 0.5) * 8)),
        network: Math.max(10, Math.min(80, prev.network + (Math.random() - 0.5) * 15)),
        storage: Math.max(60, Math.min(95, prev.storage + (Math.random() - 0.5) * 3))
      }));

      setNetworkMetrics(prev => ({
        ...prev,
        activeConnections: Math.max(200, Math.min(300, prev.activeConnections + Math.floor((Math.random() - 0.5) * 10)))
      }));
    }, 5000);

    // Update time
    const timeInterval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => {
      clearInterval(metricsInterval);
      clearInterval(timeInterval);
    };
  }, []);

  const getStatusColor = (value: number, thresholds: { warning: number; critical: number }) => {
    if (value >= thresholds.critical) return 'text-red-400';
    if (value >= thresholds.warning) return 'text-yellow-400';
    return 'text-green-400';
  };

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'critical':
        return <AlertTriangle className="h-4 w-4 text-red-400" />;
      case 'warning':
        return <AlertTriangle className="h-4 w-4 text-yellow-400" />;
      case 'info':
        return <CheckCircle className="h-4 w-4 text-blue-400" />;
      default:
        return <Clock className="h-4 w-4 text-slate-400" />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
              Enterprise Dashboard
            </h1>
            <p className="text-slate-400">
              Corporate intranet monitoring and control center
            </p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-mono text-white">
              {currentTime.toLocaleTimeString()}
            </div>
            <div className="text-slate-400 text-sm">
              {currentTime.toLocaleDateString()}
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <Users className="h-8 w-8 text-blue-400" />
              <span className="text-2xl font-bold text-white">247</span>
            </div>
            <h3 className="text-slate-400 text-sm mb-2">Active Users</h3>
            <div className="flex items-center text-green-400 text-xs">
              <TrendingUp className="h-3 w-3 mr-1" />
              +12% from yesterday
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <Shield className="h-8 w-8 text-green-400" />
              <span className="text-2xl font-bold text-white">99.8%</span>
            </div>
            <h3 className="text-slate-400 text-sm mb-2">Security Score</h3>
            <div className="flex items-center text-green-400 text-xs">
              <CheckCircle className="h-3 w-3 mr-1" />
              All systems secure
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <Network className="h-8 w-8 text-purple-400" />
              <span className="text-2xl font-bold text-white">{networkMetrics.bandwidth}</span>
            </div>
            <h3 className="text-slate-400 text-sm mb-2">Network Speed</h3>
            <div className="flex items-center text-green-400 text-xs">
              <Zap className="h-3 w-3 mr-1" />
              Optimal performance
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <Activity className="h-8 w-8 text-orange-400" />
              <span className="text-2xl font-bold text-white">{networkMetrics.uptime}</span>
            </div>
            <h3 className="text-slate-400 text-sm mb-2">System Uptime</h3>
            <div className="flex items-center text-green-400 text-xs">
              <CheckCircle className="h-3 w-3 mr-1" />
              Excellent stability
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* System Performance */}
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-white">System Performance</h2>
              <Server className="h-6 w-6 text-slate-400" />
            </div>

            <div className="space-y-6">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-slate-300">CPU Usage</span>
                  <span className={`text-sm font-medium ${getStatusColor(systemStatus.cpu, { warning: 70, critical: 85 })}`}>
                    {systemStatus.cpu}%
                  </span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full transition-all duration-500 ${
                      systemStatus.cpu >= 85 ? 'bg-red-500' : 
                      systemStatus.cpu >= 70 ? 'bg-yellow-500' : 'bg-green-500'
                    }`}
                    style={{ width: `${systemStatus.cpu}%` }}
                  />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-slate-300">Memory Usage</span>
                  <span className={`text-sm font-medium ${getStatusColor(systemStatus.memory, { warning: 80, critical: 90 })}`}>
                    {systemStatus.memory}%
                  </span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full transition-all duration-500 ${
                      systemStatus.memory >= 90 ? 'bg-red-500' : 
                      systemStatus.memory >= 80 ? 'bg-yellow-500' : 'bg-green-500'
                    }`}
                    style={{ width: `${systemStatus.memory}%` }}
                  />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-slate-300">Network Usage</span>
                  <span className={`text-sm font-medium ${getStatusColor(systemStatus.network, { warning: 60, critical: 80 })}`}>
                    {systemStatus.network}%
                  </span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full transition-all duration-500 ${
                      systemStatus.network >= 80 ? 'bg-red-500' : 
                      systemStatus.network >= 60 ? 'bg-yellow-500' : 'bg-green-500'
                    }`}
                    style={{ width: `${systemStatus.network}%` }}
                  />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-slate-300">Storage Usage</span>
                  <span className={`text-sm font-medium ${getStatusColor(systemStatus.storage, { warning: 85, critical: 95 })}`}>
                    {systemStatus.storage}%
                  </span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full transition-all duration-500 ${
                      systemStatus.storage >= 95 ? 'bg-red-500' : 
                      systemStatus.storage >= 85 ? 'bg-yellow-500' : 'bg-green-500'
                    }`}
                    style={{ width: `${systemStatus.storage}%` }}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Security Alerts */}
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-white">Security Alerts</h2>
              <Shield className="h-6 w-6 text-slate-400" />
            </div>

            <div className="space-y-4">
              {securityAlerts.map((alert) => (
                <div key={alert.id} className="flex items-start space-x-3 p-3 bg-slate-800 rounded-lg">
                  {getAlertIcon(alert.type)}
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-white">{alert.message}</p>
                    <p className="text-xs text-slate-400 mt-1">{alert.timestamp}</p>
                  </div>
                </div>
              ))}
            </div>

            <button className="w-full mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
              View All Alerts
            </button>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center mb-4">
              <Building className="h-8 w-8 text-blue-400 mr-3" />
              <h3 className="text-lg font-semibold text-white">Network Control</h3>
            </div>
            <p className="text-slate-400 text-sm mb-4">
              Manage corporate network settings and optimization
            </p>
            <button className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
              Open Control Panel
            </button>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center mb-4">
              <UserCheck className="h-8 w-8 text-green-400 mr-3" />
              <h3 className="text-lg font-semibold text-white">User Management</h3>
            </div>
            <p className="text-slate-400 text-sm mb-4">
              Manage employee access and authentication
            </p>
            <button className="w-full px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors">
              Manage Users
            </button>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center mb-4">
              <Eye className="h-8 w-8 text-purple-400 mr-3" />
              <h3 className="text-lg font-semibold text-white">Audit Logs</h3>
            </div>
            <p className="text-slate-400 text-sm mb-4">
              Review security events and system activity
            </p>
            <button className="w-full px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors">
              View Logs
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}