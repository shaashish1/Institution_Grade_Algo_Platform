'use client';

import React, { useState } from 'react';
import { 
  Shield, 
  Building2, 
  Users, 
  Lock, 
  Eye, 
  EyeOff,
  CheckCircle,
  AlertCircle,
  Briefcase
} from 'lucide-react';

interface AuthMethod {
  id: string;
  name: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
  available: boolean;
}

interface EmployeeInfo {
  employeeId: string;
  department: string;
  role: string;
  accessLevel: 'basic' | 'advanced' | 'admin';
  permissions: string[];
}

export function CorporateAuth() {
  const [authMethod, setAuthMethod] = useState<string>('credentials');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [credentials, setCredentials] = useState({
    employeeId: '',
    password: '',
    domain: 'CORPORATE'
  });

  const authMethods: AuthMethod[] = [
    {
      id: 'credentials',
      name: 'Domain Credentials',
      description: 'Login with your corporate credentials',
      icon: Lock,
      available: true
    },
    {
      id: 'sso',
      name: 'Single Sign-On',
      description: 'Use your Active Directory account',
      icon: Shield,
      available: true
    },
    {
      id: 'certificate',
      name: 'Smart Card',
      description: 'Hardware certificate authentication',
      icon: Building2,
      available: false
    }
  ];

  const employeeInfo: EmployeeInfo = {
    employeeId: 'EMP001',
    department: 'Information Technology',
    role: 'Senior Software Engineer',
    accessLevel: 'admin',
    permissions: [
      'Trading Platform Access',
      'Admin Panel Access',
      'Network Configuration',
      'User Management',
      'Audit Log Access'
    ]
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    // Simulate authentication
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // For demo purposes, always succeed
    setIsLoading(false);
    // In real implementation, redirect to dashboard
  };

  const handleSSO = () => {
    // Simulate SSO redirect
    window.location.href = '/sso/redirect';
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* Corporate Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <div className="bg-gradient-to-br from-blue-600 to-purple-600 p-3 rounded-xl">
              <Building2 className="h-8 w-8 text-white" />
            </div>
          </div>
          <h1 className="text-2xl font-bold text-white mb-2">Corporate Access</h1>
          <p className="text-slate-400">AlgoProject Trading Platform - Intranet</p>
        </div>

        {/* Authentication Methods */}
        <div className="bg-slate-900 rounded-2xl border border-slate-800 p-6 mb-6">
          <h2 className="text-lg font-semibold text-white mb-4">Authentication Method</h2>
          
          <div className="space-y-3 mb-6">
            {authMethods.map((method) => {
              const IconComponent = method.icon;
              return (
                <button
                  key={method.id}
                  onClick={() => setAuthMethod(method.id)}
                  disabled={!method.available}
                  className={`w-full p-4 rounded-xl border-2 transition-all ${
                    authMethod === method.id
                      ? 'border-blue-500 bg-blue-500/10'
                      : 'border-slate-700 hover:border-slate-600'
                  } ${!method.available ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  <div className="flex items-center">
                    <IconComponent className={`h-5 w-5 mr-3 ${
                      authMethod === method.id ? 'text-blue-400' : 'text-slate-400'
                    }`} />
                    <div className="text-left">
                      <div className={`font-medium ${
                        authMethod === method.id ? 'text-blue-400' : 'text-white'
                      }`}>
                        {method.name}
                        {!method.available && <span className="text-yellow-400 ml-2">(Coming Soon)</span>}
                      </div>
                      <div className="text-slate-400 text-sm">{method.description}</div>
                    </div>
                  </div>
                </button>
              );
            })}
          </div>

          {/* Login Form */}
          {authMethod === 'credentials' && (
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Employee ID
                </label>
                <input
                  type="text"
                  value={credentials.employeeId}
                  onChange={(e) => setCredentials(prev => ({ ...prev, employeeId: e.target.value }))}
                  className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter your employee ID"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Password
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={credentials.password}
                    onChange={(e) => setCredentials(prev => ({ ...prev, password: e.target.value }))}
                    className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 pr-12"
                    placeholder="Enter your password"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-white"
                  >
                    {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Domain
                </label>
                <select
                  value={credentials.domain}
                  onChange={(e) => setCredentials(prev => ({ ...prev, domain: e.target.value }))}
                  className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="CORPORATE">CORPORATE</option>
                  <option value="FINANCE">FINANCE</option>
                  <option value="TRADING">TRADING</option>
                </select>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full px-4 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-slate-600 disabled:to-slate-600 text-white font-semibold rounded-lg transition-colors disabled:cursor-not-allowed"
              >
                {isLoading ? 'Authenticating...' : 'Sign In'}
              </button>
            </form>
          )}

          {/* SSO Option */}
          {authMethod === 'sso' && (
            <div className="text-center">
              <div className="bg-slate-800 rounded-xl p-6 mb-4">
                <Shield className="h-12 w-12 text-blue-400 mx-auto mb-4" />
                <h3 className="text-white font-semibold mb-2">Single Sign-On</h3>
                <p className="text-slate-400 text-sm mb-4">
                  You will be redirected to the corporate authentication portal
                </p>
              </div>
              
              <button
                onClick={handleSSO}
                className="w-full px-4 py-3 bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white font-semibold rounded-lg transition-colors"
              >
                Continue with SSO
              </button>
            </div>
          )}
        </div>

        {/* Employee Info (Demo) */}
        <div className="bg-slate-900 rounded-2xl border border-slate-800 p-6">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
            <Briefcase className="h-5 w-5 mr-2 text-purple-400" />
            Employee Information
          </h3>
          
          <div className="space-y-3 text-sm">
            <div className="flex justify-between">
              <span className="text-slate-400">Employee ID:</span>
              <span className="text-white">{employeeInfo.employeeId}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Department:</span>
              <span className="text-white">{employeeInfo.department}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Role:</span>
              <span className="text-white">{employeeInfo.role}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Access Level:</span>
              <span className={`font-medium ${
                employeeInfo.accessLevel === 'admin' ? 'text-red-400' :
                employeeInfo.accessLevel === 'advanced' ? 'text-yellow-400' : 'text-green-400'
              }`}>
                {employeeInfo.accessLevel.toUpperCase()}
              </span>
            </div>
          </div>

          <div className="mt-4 pt-4 border-t border-slate-800">
            <h4 className="text-white font-medium mb-2">Access Permissions:</h4>
            <div className="space-y-1">
              {employeeInfo.permissions.map((permission, index) => (
                <div key={index} className="flex items-center text-sm">
                  <CheckCircle className="h-4 w-4 text-green-400 mr-2" />
                  <span className="text-slate-300">{permission}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Security Notice */}
        <div className="mt-6 bg-yellow-500/10 border border-yellow-500/20 rounded-xl p-4">
          <div className="flex items-start">
            <AlertCircle className="h-5 w-5 text-yellow-400 mr-3 mt-0.5 flex-shrink-0" />
            <div>
              <h4 className="text-yellow-400 font-medium text-sm">Corporate Security Policy</h4>
              <p className="text-yellow-300/80 text-xs mt-1">
                This system is for authorized personnel only. All activities are monitored and logged for security purposes.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}