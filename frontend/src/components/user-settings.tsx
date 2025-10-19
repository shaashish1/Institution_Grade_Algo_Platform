'use client';

import React, { useState } from 'react';
import { 
  Settings, User, Bell, Shield, Globe, Monitor, Palette, 
  Database, Key, CreditCard, FileText, HelpCircle, 
  CheckCircle, AlertCircle, Save, RefreshCw, Download,
  Eye, EyeOff, Smartphone, Mail, Lock, Users
} from 'lucide-react';
import Link from 'next/link';

interface SettingsSection {
  id: string;
  name: string;
  icon: any;
  description: string;
}

interface NotificationSetting {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
  type: 'email' | 'push' | 'sms';
}

interface SecuritySetting {
  name: string;
  status: 'enabled' | 'disabled' | 'pending';
  description: string;
}

export function UserSettings() {
  const [activeSection, setActiveSection] = useState<string>('profile');
  const [showPassword, setShowPassword] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  const [profileData, setProfileData] = useState({
    firstName: 'John',
    lastName: 'Trader',
    email: 'john.trader@example.com',
    phone: '+91 98765 43210',
    timezone: 'Asia/Kolkata',
    language: 'English',
    dateFormat: 'DD/MM/YYYY',
    currency: 'INR'
  });

  const [notificationSettings, setNotificationSettings] = useState<NotificationSetting[]>([
    { id: 'trade_alerts', name: 'Trade Alerts', description: 'Get notified when trades are executed', enabled: true, type: 'push' },
    { id: 'price_alerts', name: 'Price Alerts', description: 'Notifications for price movements', enabled: true, type: 'email' },
    { id: 'portfolio_summary', name: 'Portfolio Summary', description: 'Daily portfolio performance updates', enabled: false, type: 'email' },
    { id: 'margin_alerts', name: 'Margin Alerts', description: 'Warnings for margin requirements', enabled: true, type: 'sms' },
    { id: 'news_updates', name: 'Market News', description: 'Important market news and updates', enabled: false, type: 'push' },
    { id: 'system_maintenance', name: 'System Updates', description: 'Platform maintenance notifications', enabled: true, type: 'email' }
  ]);

  const [securitySettings] = useState<SecuritySetting[]>([
    { name: 'Two-Factor Authentication', status: 'enabled', description: 'SMS and authenticator app' },
    { name: 'Login Notifications', status: 'enabled', description: 'Alert on new device login' },
    { name: 'Session Timeout', status: 'enabled', description: 'Auto logout after 30 minutes' },
    { name: 'IP Whitelist', status: 'disabled', description: 'Restrict access to specific IPs' },
    { name: 'API Access', status: 'pending', description: 'Third-party API integrations' }
  ]);

  const [tradingPreferences, setTradingPreferences] = useState({
    defaultOrderType: 'LIMIT',
    defaultQuantity: 1,
    confirmBeforeOrder: true,
    showAdvancedOptions: false,
    autoSquareOff: true,
    riskWarnings: true,
    maxPositionSize: 100000,
    stopLossDefault: 5
  });

  const settingsSections: SettingsSection[] = [
    { id: 'profile', name: 'Profile', icon: User, description: 'Personal information and preferences' },
    { id: 'notifications', name: 'Notifications', icon: Bell, description: 'Alert preferences and delivery methods' },
    { id: 'security', name: 'Security', icon: Shield, description: 'Password, 2FA, and access control' },
    { id: 'trading', name: 'Trading', icon: Settings, description: 'Default trading settings and risk controls' },
    { id: 'appearance', name: 'Appearance', icon: Palette, description: 'Theme and display preferences' },
    { id: 'data', name: 'Data & Privacy', icon: Database, description: 'Data export and privacy settings' }
  ];

  const handleSave = async () => {
    setIsSaving(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    setIsSaving(false);
  };

  const toggleNotification = (id: string) => {
    setNotificationSettings(prev =>
      prev.map(setting =>
        setting.id === id ? { ...setting, enabled: !setting.enabled } : setting
      )
    );
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'enabled': return 'text-green-400 bg-green-500/10';
      case 'disabled': return 'text-slate-400 bg-slate-500/10';
      case 'pending': return 'text-yellow-400 bg-yellow-500/10';
      default: return 'text-slate-400 bg-slate-500/10';
    }
  };

  const getNotificationTypeIcon = (type: string) => {
    switch (type) {
      case 'email': return Mail;
      case 'push': return Bell;
      case 'sms': return Smartphone;
      default: return Bell;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4">
      <div className="max-w-full mx-auto">
        {/* Navigation Breadcrumb */}
        <div className="mb-6">
          <nav className="flex items-center space-x-2 text-sm text-slate-400">
            <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
            <span>/</span>
            <Link href="/dashboard" className="hover:text-blue-400 transition-colors">Dashboard</Link>
            <span>/</span>
            <span className="text-white">Settings</span>
          </nav>
        </div>

        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
              Account Settings
            </h1>
            <p className="text-slate-400">
              Manage your account preferences, security, and trading settings
            </p>
          </div>
          
          <button
            onClick={handleSave}
            disabled={isSaving}
            className="flex items-center px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:cursor-not-allowed rounded-lg transition-colors"
          >
            {isSaving ? (
              <>
                <div className="animate-spin h-4 w-4 mr-2 border-2 border-white border-t-transparent rounded-full" />
                Saving...
              </>
            ) : (
              <>
                <Save className="h-4 w-4 mr-2" />
                Save Changes
              </>
            )}
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Settings Navigation */}
          <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800 h-fit">
            <h2 className="text-lg font-bold text-white mb-4">Settings</h2>
            <nav className="space-y-2">
              {settingsSections.map((section) => (
                <button
                  key={section.id}
                  onClick={() => setActiveSection(section.id)}
                  className={`w-full flex items-center px-4 py-3 rounded-lg text-left transition-all ${
                    activeSection === section.id
                      ? 'bg-blue-600 text-white'
                      : 'text-slate-400 hover:text-white hover:bg-slate-800'
                  }`}
                >
                  <section.icon className="h-5 w-5 mr-3" />
                  <div>
                    <div className="font-medium">{section.name}</div>
                    <div className="text-xs opacity-75">{section.description}</div>
                  </div>
                </button>
              ))}
            </nav>
          </div>

          {/* Settings Content */}
          <div className="lg:col-span-3 space-y-6">
            {/* Profile Settings */}
            {activeSection === 'profile' && (
              <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                  <User className="h-5 w-5 mr-2 text-blue-400" />
                  Profile Information
                </h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">First Name</label>
                    <input
                      type="text"
                      value={profileData.firstName}
                      onChange={(e) => setProfileData(prev => ({ ...prev, firstName: e.target.value }))}
                      className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Last Name</label>
                    <input
                      type="text"
                      value={profileData.lastName}
                      onChange={(e) => setProfileData(prev => ({ ...prev, lastName: e.target.value }))}
                      className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Email</label>
                    <input
                      type="email"
                      value={profileData.email}
                      onChange={(e) => setProfileData(prev => ({ ...prev, email: e.target.value }))}
                      className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Phone</label>
                    <input
                      type="tel"
                      value={profileData.phone}
                      onChange={(e) => setProfileData(prev => ({ ...prev, phone: e.target.value }))}
                      className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Timezone</label>
                    <select
                      value={profileData.timezone}
                      onChange={(e) => setProfileData(prev => ({ ...prev, timezone: e.target.value }))}
                      className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    >
                      <option value="Asia/Kolkata">Asia/Kolkata (IST)</option>
                      <option value="America/New_York">America/New_York (EST)</option>
                      <option value="Europe/London">Europe/London (GMT)</option>
                      <option value="Asia/Tokyo">Asia/Tokyo (JST)</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Language</label>
                    <select
                      value={profileData.language}
                      onChange={(e) => setProfileData(prev => ({ ...prev, language: e.target.value }))}
                      className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    >
                      <option value="English">English</option>
                      <option value="Hindi">हिंदी</option>
                      <option value="Bengali">বাংলা</option>
                      <option value="Tamil">தமிழ்</option>
                    </select>
                  </div>
                </div>
              </div>
            )}

            {/* Notification Settings */}
            {activeSection === 'notifications' && (
              <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                  <Bell className="h-5 w-5 mr-2 text-green-400" />
                  Notification Preferences
                </h2>
                
                <div className="space-y-4">
                  {notificationSettings.map((setting) => {
                    const IconComponent = getNotificationTypeIcon(setting.type);
                    return (
                      <div key={setting.id} className="flex items-center justify-between p-4 bg-slate-800 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <IconComponent className="h-5 w-5 text-blue-400" />
                          <div>
                            <h3 className="font-medium text-white">{setting.name}</h3>
                            <p className="text-sm text-slate-400">{setting.description}</p>
                            <span className="text-xs text-purple-400 capitalize">{setting.type}</span>
                          </div>
                        </div>
                        
                        <button
                          onClick={() => toggleNotification(setting.id)}
                          className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                            setting.enabled ? 'bg-blue-600' : 'bg-slate-700'
                          }`}
                        >
                          <span
                            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                              setting.enabled ? 'translate-x-6' : 'translate-x-1'
                            }`}
                          />
                        </button>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Security Settings */}
            {activeSection === 'security' && (
              <div className="space-y-6">
                <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                  <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                    <Shield className="h-5 w-5 mr-2 text-red-400" />
                    Security Features
                  </h2>
                  
                  <div className="space-y-4">
                    {securitySettings.map((setting, index) => (
                      <div key={index} className="flex items-center justify-between p-4 bg-slate-800 rounded-lg">
                        <div>
                          <h3 className="font-medium text-white">{setting.name}</h3>
                          <p className="text-sm text-slate-400">{setting.description}</p>
                        </div>
                        
                        <div className="flex items-center space-x-3">
                          <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(setting.status)}`}>
                            {setting.status}
                          </span>
                          <button className="text-blue-400 hover:text-blue-300 text-sm">
                            Configure
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                  <h2 className="text-lg font-bold text-white mb-4 flex items-center">
                    <Lock className="h-5 w-5 mr-2 text-yellow-400" />
                    Change Password
                  </h2>
                  
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-300 mb-2">Current Password</label>
                      <div className="relative">
                        <input
                          type={showPassword ? 'text' : 'password'}
                          className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500 pr-10"
                          placeholder="Enter current password"
                        />
                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-white"
                        >
                          {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                        </button>
                      </div>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-slate-300 mb-2">New Password</label>
                      <input
                        type="password"
                        className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
                        placeholder="Enter new password"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-slate-300 mb-2">Confirm New Password</label>
                      <input
                        type="password"
                        className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
                        placeholder="Confirm new password"
                      />
                    </div>
                    
                    <button className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors">
                      Update Password
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Trading Settings */}
            {activeSection === 'trading' && (
              <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                  <Settings className="h-5 w-5 mr-2 text-purple-400" />
                  Trading Preferences
                </h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Default Order Type</label>
                    <select
                      value={tradingPreferences.defaultOrderType}
                      onChange={(e) => setTradingPreferences(prev => ({ ...prev, defaultOrderType: e.target.value }))}
                      className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    >
                      <option value="MARKET">Market Order</option>
                      <option value="LIMIT">Limit Order</option>
                      <option value="STOP_LOSS">Stop Loss</option>
                      <option value="STOP_LIMIT">Stop Limit</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Default Quantity</label>
                    <input
                      type="number"
                      value={tradingPreferences.defaultQuantity}
                      onChange={(e) => setTradingPreferences(prev => ({ ...prev, defaultQuantity: parseInt(e.target.value) }))}
                      className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Max Position Size (₹)</label>
                    <input
                      type="number"
                      value={tradingPreferences.maxPositionSize}
                      onChange={(e) => setTradingPreferences(prev => ({ ...prev, maxPositionSize: parseInt(e.target.value) }))}
                      className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Default Stop Loss (%)</label>
                    <input
                      type="number"
                      step="0.1"
                      value={tradingPreferences.stopLossDefault}
                      onChange={(e) => setTradingPreferences(prev => ({ ...prev, stopLossDefault: parseFloat(e.target.value) }))}
                      className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>
                </div>
                
                <div className="mt-6 space-y-4">
                  <h3 className="text-lg font-medium text-white">Risk Management</h3>
                  
                  {[
                    { key: 'confirmBeforeOrder', label: 'Confirm Before Order', description: 'Show confirmation dialog before placing orders' },
                    { key: 'showAdvancedOptions', label: 'Show Advanced Options', description: 'Display advanced trading options by default' },
                    { key: 'autoSquareOff', label: 'Auto Square Off', description: 'Automatically close positions at market close' },
                    { key: 'riskWarnings', label: 'Risk Warnings', description: 'Show risk warnings for high-risk trades' }
                  ].map((setting) => (
                    <div key={setting.key} className="flex items-center justify-between p-3 bg-slate-800 rounded-lg">
                      <div>
                        <h4 className="font-medium text-white">{setting.label}</h4>
                        <p className="text-sm text-slate-400">{setting.description}</p>
                      </div>
                      
                      <button
                        onClick={() => setTradingPreferences(prev => ({ 
                          ...prev, 
                          [setting.key]: !prev[setting.key as keyof typeof prev] 
                        }))}
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                          tradingPreferences[setting.key as keyof typeof tradingPreferences] ? 'bg-blue-600' : 'bg-slate-700'
                        }`}
                      >
                        <span
                          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                            tradingPreferences[setting.key as keyof typeof tradingPreferences] ? 'translate-x-6' : 'translate-x-1'
                          }`}
                        />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Appearance Settings */}
            {activeSection === 'appearance' && (
              <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                  <Palette className="h-5 w-5 mr-2 text-pink-400" />
                  Appearance & Display
                </h2>
                
                <div className="space-y-6">
                  <div>
                    <h3 className="text-lg font-medium text-white mb-4">Theme</h3>
                    <div className="grid grid-cols-3 gap-4">
                      {['Dark', 'Light', 'Auto'].map((theme) => (
                        <button
                          key={theme}
                          className={`p-4 rounded-lg border-2 transition-all ${
                            theme === 'Dark' 
                              ? 'border-blue-500 bg-blue-500/10' 
                              : 'border-slate-700 bg-slate-800 hover:border-slate-600'
                          }`}
                        >
                          <Monitor className="h-6 w-6 mx-auto mb-2 text-blue-400" />
                          <div className="font-medium text-white">{theme}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="text-lg font-medium text-white mb-4">Chart Colors</h3>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="p-3 bg-slate-800 rounded-lg">
                        <label className="block text-sm font-medium text-slate-300 mb-2">Positive Color</label>
                        <div className="flex items-center space-x-2">
                          <div className="w-8 h-8 bg-green-500 rounded"></div>
                          <span className="text-white">#10B981</span>
                        </div>
                      </div>
                      <div className="p-3 bg-slate-800 rounded-lg">
                        <label className="block text-sm font-medium text-slate-300 mb-2">Negative Color</label>
                        <div className="flex items-center space-x-2">
                          <div className="w-8 h-8 bg-red-500 rounded"></div>
                          <span className="text-white">#EF4444</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Data & Privacy */}
            {activeSection === 'data' && (
              <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">
                <h2 className="text-xl font-bold text-white mb-6 flex items-center">
                  <Database className="h-5 w-5 mr-2 text-indigo-400" />
                  Data & Privacy
                </h2>
                
                <div className="space-y-6">
                  <div>
                    <h3 className="text-lg font-medium text-white mb-4">Data Export</h3>
                    <div className="space-y-3">
                      <button className="w-full flex items-center justify-between p-3 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors">
                        <div className="flex items-center">
                          <Download className="h-5 w-5 mr-3 text-blue-400" />
                          <span className="text-white">Export Trading Data</span>
                        </div>
                        <span className="text-slate-400">CSV, JSON</span>
                      </button>
                      
                      <button className="w-full flex items-center justify-between p-3 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors">
                        <div className="flex items-center">
                          <Download className="h-5 w-5 mr-3 text-green-400" />
                          <span className="text-white">Export Portfolio Data</span>
                        </div>
                        <span className="text-slate-400">PDF, Excel</span>
                      </button>
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="text-lg font-medium text-white mb-4">Privacy Controls</h3>
                    <div className="space-y-3">
                      <div className="flex items-center justify-between p-3 bg-slate-800 rounded-lg">
                        <span className="text-white">Data Analytics</span>
                        <button className="relative inline-flex h-6 w-11 items-center rounded-full bg-blue-600">
                          <span className="inline-block h-4 w-4 transform rounded-full bg-white translate-x-6" />
                        </button>
                      </div>
                      
                      <div className="flex items-center justify-between p-3 bg-slate-800 rounded-lg">
                        <span className="text-white">Usage Statistics</span>
                        <button className="relative inline-flex h-6 w-11 items-center rounded-full bg-slate-700">
                          <span className="inline-block h-4 w-4 transform rounded-full bg-white translate-x-1" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}