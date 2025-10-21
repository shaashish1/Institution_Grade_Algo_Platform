'use client';

import React, { useState, useEffect } from 'react';
import { 
  Key, Shield, CheckCircle, AlertTriangle, 
  Eye, EyeOff, Save, Trash2, TestTube, RefreshCw,
  Info, Lock, Smartphone, User
} from 'lucide-react';

interface FyersCredentials {
  user_id: string;
  client_id: string;
  secret_key: string;
  redirect_uri: string;
  user_name: string;
  totp_key?: string;
  pin: string;
  is_active: boolean;
}

interface FyersStatus {
  user_id: string;
  is_connected: boolean;
  has_credentials: boolean;
  token_valid: boolean;
  token_expires?: string;
  last_updated?: string;
  error_message?: string;
}

interface Props {
  userId: string;
}

export function FyersCredentialsManager({ userId }: Props) {
  const [credentials, setCredentials] = useState<FyersCredentials>({
    user_id: userId,
    client_id: '',
    secret_key: '',
    redirect_uri: 'https://www.google.com',
    user_name: '',
    totp_key: '',
    pin: '',
    is_active: true
  });

  const [status, setStatus] = useState<FyersStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [testing, setTesting] = useState(false);
  const [showSecrets, setShowSecrets] = useState(false);
  const [showPin, setShowPin] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    loadCredentials();
    loadStatus();
  }, [userId]);

  const loadCredentials = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/fyers/credentials/${userId}`);
      
      if (response.ok) {
        const data = await response.json();
        setCredentials(prev => ({
          ...prev,
          client_id: data.client_id || '',
          user_name: data.user_name || '',
          redirect_uri: data.redirect_uri || 'https://www.google.com',
          is_active: data.is_active ?? true
        }));
      }
    } catch (error) {
      console.error('Failed to load credentials:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadStatus = async () => {
    try {
      const response = await fetch(`/api/fyers/status/${userId}`);
      if (response.ok) {
        const statusData = await response.json();
        setStatus(statusData);
      }
    } catch (error) {
      console.error('Failed to load status:', error);
    }
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      setError(null);
      setSuccess(null);

      // Validate required fields
      if (!credentials.client_id || !credentials.secret_key || !credentials.user_name || !credentials.pin) {
        setError('Please fill in all required fields');
        return;
      }

      if (credentials.pin.length !== 4 || !/^\d{4}$/.test(credentials.pin)) {
        setError('PIN must be exactly 4 digits');
        return;
      }

      const response = await fetch('/api/fyers/credentials', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      if (response.ok) {
        setSuccess('Fyers credentials saved successfully!');
        await loadStatus();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to save credentials');
      }
    } catch (error) {
      setError('Failed to save credentials. Please try again.');
      console.error('Save error:', error);
    } finally {
      setSaving(false);
    }
  };

  const handleTestConnection = async () => {
    try {
      setTesting(true);
      setError(null);
      setSuccess(null);

      const response = await fetch(`/api/fyers/test-connection/${userId}`, {
        method: 'POST',
      });

      const result = await response.json();
      
      if (result.success) {
        setSuccess('Connection test successful! Credentials are valid.');
        await loadStatus();
      } else {
        setError(`Connection test failed: ${result.message}`);
      }
    } catch (error) {
      setError('Failed to test connection. Please try again.');
      console.error('Test error:', error);
    } finally {
      setTesting(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete your Fyers credentials? This action cannot be undone.')) {
      return;
    }

    try {
      setLoading(true);
      const response = await fetch(`/api/fyers/credentials/${userId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setSuccess('Fyers credentials deleted successfully');
        setCredentials({
          user_id: userId,
          client_id: '',
          secret_key: '',
          redirect_uri: 'https://www.google.com',
          user_name: '',
          totp_key: '',
          pin: '',
          is_active: true
        });
        setStatus(null);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to delete credentials');
      }
    } catch (error) {
      setError('Failed to delete credentials. Please try again.');
      console.error('Delete error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center">
            <Key className="h-5 w-5 mr-2 text-orange-400" />
            Fyers API Credentials
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Configure your personal Fyers API credentials for stock trading
          </p>
        </div>
        
        {status && (
          <div className={`flex items-center px-3 py-1 rounded-full text-xs font-medium ${
            status.is_connected 
              ? 'bg-green-500/20 text-green-400' 
              : status.has_credentials 
                ? 'bg-yellow-500/20 text-yellow-400'
                : 'bg-slate-500/20 text-slate-400'
          }`}>
            {status.is_connected ? (
              <>
                <CheckCircle className="h-3 w-3 mr-1" />
                Connected
              </>
            ) : status.has_credentials ? (
              <>
                <AlertTriangle className="h-3 w-3 mr-1" />
                Token Required
              </>
            ) : (
              <>
                <Shield className="h-3 w-3 mr-1" />
                Not Configured
              </>
            )}
          </div>
        )}
      </div>

      {/* Information Panel */}
      <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-4">
        <div className="flex items-start">
          <Info className="h-5 w-5 text-blue-400 mt-0.5 mr-3 flex-shrink-0" />
          <div className="text-sm text-blue-200">
            <p className="font-medium mb-2">How to get your Fyers API credentials:</p>
            <ol className="list-decimal list-inside space-y-1 text-blue-300">
              <li>Login to <a href="https://api-portal.fyers.in/" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">Fyers API Portal</a></li>
              <li>Create a new app and note down your Client ID and Secret Key</li>
              <li>Get your TOTP key from the Fyers mobile app (Settings → API → TOTP)</li>
              <li>Enter your 4-digit trading PIN</li>
            </ol>
          </div>
        </div>
      </div>

      {/* Error/Success Messages */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4">
          <div className="flex items-center">
            <AlertTriangle className="h-5 w-5 text-red-400 mr-2" />
            <span className="text-red-200">{error}</span>
          </div>
        </div>
      )}

      {success && (
        <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4">
          <div className="flex items-center">
            <CheckCircle className="h-5 w-5 text-green-400 mr-2" />
            <span className="text-green-200">{success}</span>
          </div>
        </div>
      )}

      {/* Credentials Form */}
      <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Client ID */}
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Client ID *
            </label>
            <input
              type="text"
              value={credentials.client_id}
              onChange={(e) => setCredentials(prev => ({ ...prev, client_id: e.target.value }))}
              placeholder="e.g., XA12345-100"
              className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-orange-500"
            />
            <p className="text-xs text-slate-500 mt-1">Format: [UserID]-100</p>
          </div>

          {/* User Name */}
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Fyers User ID *
            </label>
            <div className="relative">
              <User className="h-4 w-4 text-slate-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
              <input
                type="text"
                value={credentials.user_name}
                onChange={(e) => setCredentials(prev => ({ ...prev, user_name: e.target.value }))}
                placeholder="e.g., XA00330"
                className="w-full pl-10 pr-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-orange-500"
              />
            </div>
          </div>

          {/* Secret Key */}
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Secret Key *
            </label>
            <div className="relative">
              <input
                type={showSecrets ? 'text' : 'password'}
                value={credentials.secret_key}
                onChange={(e) => setCredentials(prev => ({ ...prev, secret_key: e.target.value }))}
                placeholder="Enter your secret key"
                className="w-full px-4 py-2 pr-10 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-orange-500"
              />
              <button
                type="button"
                onClick={() => setShowSecrets(!showSecrets)}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-white"
              >
                {showSecrets ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
          </div>

          {/* Trading PIN */}
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Trading PIN *
            </label>
            <div className="relative">
              <Lock className="h-4 w-4 text-slate-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
              <input
                type={showPin ? 'text' : 'password'}
                value={credentials.pin}
                onChange={(e) => setCredentials(prev => ({ ...prev, pin: e.target.value.replace(/\D/g, '').slice(0, 4) }))}
                placeholder="4-digit PIN"
                maxLength={4}
                className="w-full pl-10 pr-10 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-orange-500"
              />
              <button
                type="button"
                onClick={() => setShowPin(!showPin)}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-white"
              >
                {showPin ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
          </div>

          {/* TOTP Key */}
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-slate-300 mb-2">
              TOTP Secret Key (Optional)
            </label>
            <div className="relative">
              <Smartphone className="h-4 w-4 text-slate-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
              <input
                type={showSecrets ? 'text' : 'password'}
                value={credentials.totp_key || ''}
                onChange={(e) => setCredentials(prev => ({ ...prev, totp_key: e.target.value }))}
                placeholder="TOTP secret from Fyers mobile app"
                className="w-full pl-10 pr-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-orange-500"
              />
            </div>
            <p className="text-xs text-slate-500 mt-1">Required for automated token generation</p>
          </div>

          {/* Redirect URI */}
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Redirect URI
            </label>
            <input
              type="url"
              value={credentials.redirect_uri}
              onChange={(e) => setCredentials(prev => ({ ...prev, redirect_uri: e.target.value }))}
              className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-orange-500"
            />
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-6 flex flex-wrap gap-3">
          <button
            onClick={handleSave}
            disabled={saving || loading}
            className="flex items-center px-4 py-2 bg-orange-600 hover:bg-orange-700 disabled:bg-orange-800 text-white rounded-lg transition-colors"
          >
            {saving ? (
              <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
            ) : (
              <Save className="h-4 w-4 mr-2" />
            )}
            {saving ? 'Saving...' : 'Save Credentials'}
          </button>

          <button
            onClick={handleTestConnection}
            disabled={testing || loading || !credentials.client_id}
            className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 text-white rounded-lg transition-colors"
          >
            {testing ? (
              <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
            ) : (
              <TestTube className="h-4 w-4 mr-2" />
            )}
            {testing ? 'Testing...' : 'Test Connection'}
          </button>

          {status?.has_credentials && (
            <button
              onClick={handleDelete}
              disabled={loading}
              className="flex items-center px-4 py-2 bg-red-600 hover:bg-red-700 disabled:bg-red-800 text-white rounded-lg transition-colors"
            >
              <Trash2 className="h-4 w-4 mr-2" />
              Delete Credentials
            </button>
          )}
        </div>
      </div>

      {/* Status Information */}
      {status && (
        <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
          <h3 className="text-lg font-medium text-white mb-4">Connection Status</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-slate-400">Credentials:</span>
                <span className={status.has_credentials ? 'text-green-400' : 'text-red-400'}>
                  {status.has_credentials ? 'Configured' : 'Not Configured'}
                </span>
              </div>
              
              <div className="flex justify-between">
                <span className="text-slate-400">Connection:</span>
                <span className={status.is_connected ? 'text-green-400' : 'text-yellow-400'}>
                  {status.is_connected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
              
              <div className="flex justify-between">
                <span className="text-slate-400">Token Valid:</span>
                <span className={status.token_valid ? 'text-green-400' : 'text-red-400'}>
                  {status.token_valid ? 'Yes' : 'No'}
                </span>
              </div>
            </div>
            
            <div className="space-y-3">
              {status.token_expires && (
                <div className="flex justify-between">
                  <span className="text-slate-400">Token Expires:</span>
                  <span className="text-white text-sm">
                    {new Date(status.token_expires).toLocaleString()}
                  </span>
                </div>
              )}
              
              {status.last_updated && (
                <div className="flex justify-between">
                  <span className="text-slate-400">Last Updated:</span>
                  <span className="text-white text-sm">
                    {new Date(status.last_updated).toLocaleString()}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}