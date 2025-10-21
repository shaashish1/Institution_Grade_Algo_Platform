'use client';

import React, { useState, useEffect } from 'react';
import { 
  Shield, 
  User, 
  Clock, 
  MapPin, 
  AlertTriangle, 
  CheckCircle,
  Eye,
  Download,
  Filter,
  Search,
  RefreshCw
} from 'lucide-react';

interface AuditLog {
  id: string;
  timestamp: string;
  userId: string;
  action: string;
  resource: string;
  ipAddress: string;
  location: string;
  userAgent: string;
  status: 'success' | 'failure' | 'warning';
  risk: 'low' | 'medium' | 'high';
  details: string;
}

interface SecurityMetrics {
  totalLogins: number;
  failedAttempts: number;
  suspiciousActivity: number;
  uniqueUsers: number;
  averageSessionTime: string;
}

export function SecurityAuditLog() {
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([
    {
      id: '1',
      timestamp: '2025-10-20T09:15:23Z',
      userId: 'admin@company.com',
      action: 'LOGIN',
      resource: 'Trading Platform',
      ipAddress: '192.168.1.100',
      location: 'New York Office',
      userAgent: 'Chrome 118.0.0.0',
      status: 'success',
      risk: 'low',
      details: 'Successful login from corporate network'
    },
    {
      id: '2',
      timestamp: '2025-10-20T09:12:45Z',
      userId: 'john.trader@company.com',
      action: 'ACCESS_DENIED',
      resource: 'Admin Panel',
      ipAddress: '192.168.1.150',
      location: 'Trading Floor',
      userAgent: 'Chrome 118.0.0.0',
      status: 'failure',
      risk: 'medium',
      details: 'Attempted access to restricted resource'
    },
    {
      id: '3',
      timestamp: '2025-10-20T09:10:12Z',
      userId: 'analyst@company.com',
      action: 'DATA_EXPORT',
      resource: 'Portfolio Data',
      ipAddress: '192.168.1.125',
      location: 'Analytics Department',
      userAgent: 'Chrome 118.0.0.0',
      status: 'success',
      risk: 'low',
      details: 'Exported quarterly portfolio performance data'
    },
    {
      id: '4',
      timestamp: '2025-10-20T09:08:34Z',
      userId: 'unknown',
      action: 'FAILED_LOGIN',
      resource: 'Trading Platform',
      ipAddress: '203.45.67.89',
      location: 'External',
      userAgent: 'Unknown Bot',
      status: 'failure',
      risk: 'high',
      details: 'Multiple failed login attempts from external IP'
    },
    {
      id: '5',
      timestamp: '2025-10-20T09:05:17Z',
      userId: 'manager@company.com',
      action: 'CONFIG_CHANGE',
      resource: 'Network Settings',
      ipAddress: '192.168.1.50',
      location: 'IT Department',
      userAgent: 'Chrome 118.0.0.0',
      status: 'success',
      risk: 'low',
      details: 'Updated firewall configuration'
    }
  ]);

  const [metrics, setMetrics] = useState<SecurityMetrics>({
    totalLogins: 247,
    failedAttempts: 12,
    suspiciousActivity: 3,
    uniqueUsers: 45,
    averageSessionTime: '2h 34m'
  });

  const [filters, setFilters] = useState({
    status: 'all',
    risk: 'all',
    timeRange: '24h'
  });

  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Simulate real-time updates
    const interval = setInterval(() => {
      setMetrics(prev => ({
        ...prev,
        totalLogins: prev.totalLogins + Math.floor(Math.random() * 3),
        failedAttempts: prev.failedAttempts + Math.floor(Math.random() * 2)
      }));
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success':
        return <CheckCircle className="h-4 w-4 text-green-400" />;
      case 'failure':
        return <AlertTriangle className="h-4 w-4 text-red-400" />;
      case 'warning':
        return <AlertTriangle className="h-4 w-4 text-yellow-400" />;
      default:
        return <Clock className="h-4 w-4 text-slate-400" />;
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'high':
        return 'text-red-400 bg-red-500/10';
      case 'medium':
        return 'text-yellow-400 bg-yellow-500/10';
      case 'low':
        return 'text-green-400 bg-green-500/10';
      default:
        return 'text-slate-400 bg-slate-500/10';
    }
  };

  const refreshLogs = async () => {
    setIsLoading(true);
    await new Promise(resolve => setTimeout(resolve, 1000));
    setIsLoading(false);
  };

  const exportLogs = () => {
    // In a real implementation, this would export to CSV/JSON
    const dataStr = JSON.stringify(auditLogs, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `audit-logs-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
  };

  const filteredLogs = auditLogs.filter(log => {
    const matchesSearch = searchTerm === '' || 
      log.userId.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.action.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.ipAddress.includes(searchTerm);
    
    const matchesStatus = filters.status === 'all' || log.status === filters.status;
    const matchesRisk = filters.risk === 'all' || log.risk === filters.risk;

    return matchesSearch && matchesStatus && matchesRisk;
  });

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-red-400 to-orange-400 bg-clip-text text-transparent mb-2">
            Security Audit Log
          </h1>
          <p className="text-slate-400">
            Monitor and track all security events and user activities
          </p>
        </div>

        {/* Security Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-2">
              <User className="h-8 w-8 text-blue-400" />
              <span className="text-2xl font-bold text-white">{metrics.totalLogins}</span>
            </div>
            <h3 className="text-slate-400 text-sm">Total Logins</h3>
            <div className="mt-2 text-green-400 text-xs">+5% from yesterday</div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-2">
              <AlertTriangle className="h-8 w-8 text-red-400" />
              <span className="text-2xl font-bold text-white">{metrics.failedAttempts}</span>
            </div>
            <h3 className="text-slate-400 text-sm">Failed Attempts</h3>
            <div className="mt-2 text-red-400 text-xs">↑ Needs attention</div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-2">
              <Shield className="h-8 w-8 text-yellow-400" />
              <span className="text-2xl font-bold text-white">{metrics.suspiciousActivity}</span>
            </div>
            <h3 className="text-slate-400 text-sm">Suspicious Activity</h3>
            <div className="mt-2 text-yellow-400 text-xs">Monitor closely</div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-2">
              <User className="h-8 w-8 text-green-400" />
              <span className="text-2xl font-bold text-white">{metrics.uniqueUsers}</span>
            </div>
            <h3 className="text-slate-400 text-sm">Active Users</h3>
            <div className="mt-2 text-green-400 text-xs">Currently online</div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-2">
              <Clock className="h-8 w-8 text-purple-400" />
              <span className="text-lg font-bold text-white">{metrics.averageSessionTime}</span>
            </div>
            <h3 className="text-slate-400 text-sm">Avg Session</h3>
            <div className="mt-2 text-purple-400 text-xs">Per user</div>
          </div>
        </div>

        {/* Controls */}
        <div className="bg-slate-900 rounded-xl p-6 border border-slate-800 mb-8">
          <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
            <div className="flex items-center space-x-4 flex-1">
              <div className="relative">
                <Search className="h-4 w-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search logs..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 w-64"
                />
              </div>

              <select
                value={filters.status}
                onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
                className="px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="all">All Status</option>
                <option value="success">Success</option>
                <option value="failure">Failure</option>
                <option value="warning">Warning</option>
              </select>

              <select
                value={filters.risk}
                onChange={(e) => setFilters(prev => ({ ...prev, risk: e.target.value }))}
                className="px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="all">All Risk</option>
                <option value="low">Low Risk</option>
                <option value="medium">Medium Risk</option>
                <option value="high">High Risk</option>
              </select>
            </div>

            <div className="flex items-center space-x-3">
              <button
                onClick={refreshLogs}
                disabled={isLoading}
                className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 text-white rounded-lg transition-colors"
              >
                <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                Refresh
              </button>
              <button
                onClick={exportLogs}
                className="flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
              >
                <Download className="h-4 w-4 mr-2" />
                Export
              </button>
            </div>
          </div>
        </div>

        {/* Audit Log Table */}
        <div className="bg-slate-900 rounded-xl border border-slate-800 overflow-hidden">
          <div className="p-6 border-b border-slate-800">
            <h2 className="text-xl font-bold text-white">Security Events</h2>
            <p className="text-slate-400 text-sm mt-1">
              Showing {filteredLogs.length} of {auditLogs.length} events
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-800">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                    Timestamp
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                    User
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                    Action
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                    IP Address
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                    Risk
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                    Details
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {filteredLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-800/50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {getStatusIcon(log.status)}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-300">
                      {new Date(log.timestamp).toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-white">{log.userId}</div>
                      <div className="text-xs text-slate-400">{log.location}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-white">{log.action}</div>
                      <div className="text-xs text-slate-400">{log.resource}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-300">
                      {log.ipAddress}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getRiskColor(log.risk)}`}>
                        {log.risk.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-300 max-w-xs truncate">
                      {log.details}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {filteredLogs.length === 0 && (
            <div className="p-8 text-center">
              <Eye className="h-12 w-12 text-slate-600 mx-auto mb-4" />
              <h3 className="text-slate-400 font-medium">No logs found</h3>
              <p className="text-slate-500 text-sm">Try adjusting your search or filters</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}