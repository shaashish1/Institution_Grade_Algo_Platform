'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  Menu, X, ChevronDown, TrendingUp, BarChart3, Target, Zap, 
  Settings, User, Bell, Search, Activity, DollarSign, Brain,
  PieChart, LineChart, Shield, Coins, Building2, Calculator,
  TrendingDown, Play, Eye, Crown, Award, Lightbulb, Database,
  Globe, Smartphone, Monitor, RefreshCw, Download, Upload
} from 'lucide-react';

interface MenuItem {
  label: string;
  href?: string;
  icon: any;
  description?: string;
  items?: MenuItem[];
  badge?: string;
  isNew?: boolean;
}

interface MegaMenuProps {
  className?: string;
}

const menuItems: MenuItem[] = [
  {
    label: 'Trading',
    icon: TrendingUp,
    items: [
      {
        label: 'NSE Options',
        href: '/stocks/option-chain',
        icon: Target,
        description: 'Real-time option chain data and analysis',
        badge: 'Live'
      },
      {
        label: 'Complete Option Chain',
        href: '/stocks/option-chain/complete',
        icon: Eye,
        description: 'Comprehensive option data with all strikes',
        isNew: true
      },
      {
        label: 'Derivatives & IPO',
        href: '/stocks/derivatives',
        icon: Building2,
        description: 'Futures, options, and IPO hub'
      },
      {
        label: 'Cryptocurrency',
        href: '/crypto',
        icon: Coins,
        description: 'Multi-exchange crypto trading'
      },
      {
        label: 'ETF Trading',
        href: '/stocks/etf',
        icon: PieChart,
        description: 'Exchange-traded fund analysis'
      },
      {
        label: 'Advanced Charts',
        href: '/charts',
        icon: LineChart,
        description: 'Professional charting with indicators',
        badge: 'Pro',
        isNew: true
      }
    ]
  },
  {
    label: 'Backtesting',
    icon: BarChart3,
    items: [
      {
        label: 'Universal Backtesting',
        href: '/stocks/backtest/universal',
        icon: Brain,
        description: 'AI-powered strategy optimization',
        badge: 'AI',
        isNew: true
      },
      {
        label: 'Multi-Strategy Compare',
        href: '/stocks/backtest/multi-strategy',
        icon: Calculator,
        description: 'Compare multiple strategies side-by-side'
      },
      {
        label: 'NSE Backtesting',
        href: '/stocks/backtest',
        icon: Activity,
        description: 'Historical NSE data backtesting'
      },
      {
        label: 'Crypto Backtesting',
        href: '/crypto/backtest',
        icon: TrendingDown,
        description: 'Cryptocurrency strategy testing'
      }
    ]
  },
  {
    label: 'Portfolio',
    icon: DollarSign,
    items: [
      {
        label: 'Dashboard',
        href: '/dashboard',
        icon: Monitor,
        description: 'Unified trading dashboard',
        badge: 'Main'
      },
      {
        label: 'Holdings',
        href: '/portfolio',
        icon: PieChart,
        description: 'Portfolio management and tracking'
      },
      {
        label: 'Analytics',
        href: '/analytics',
        icon: LineChart,
        description: 'Advanced performance analytics'
      },
      {
        label: 'P&L Reports',
        href: '/reports',
        icon: Download,
        description: 'Profit & loss reporting'
      }
    ]
  },
  {
    label: 'AI Tools',
    icon: Brain,
    items: [
      {
        label: 'Strategy Recommender',
        href: '/ai/strategies',
        icon: Lightbulb,
        description: 'AI-powered strategy recommendations',
        isNew: true,
        badge: 'Beta'
      },
      {
        label: 'Trade Analysis',
        href: '/ai/analysis',
        icon: Search,
        description: 'AI trade opportunity analysis',
        isNew: true
      },
      {
        label: 'Risk Assessment',
        href: '/ai/risk',
        icon: Shield,
        description: 'Intelligent risk evaluation'
      },
      {
        label: 'Market Sentiment',
        href: '/ai/sentiment',
        icon: Globe,
        description: 'AI sentiment analysis'
      }
    ]
  },
  {
    label: 'Tools',
    icon: Settings,
    items: [
      {
        label: 'Settings',
        href: '/settings',
        icon: Settings,
        description: 'Application settings and preferences',
        badge: 'New'
      },
      {
        label: 'Position Calculator',
        href: '/tools/calculator',
        icon: Calculator,
        description: 'Options and position size calculator'
      },
      {
        label: 'Risk Manager',
        href: '/tools/risk',
        icon: Shield,
        description: 'Portfolio risk management tools'
      },
      {
        label: 'Screener',
        href: '/tools/screener',
        icon: Search,
        description: 'Stock and option screener'
      },
      {
        label: 'Alerts',
        href: '/tools/alerts',
        icon: Bell,
        description: 'Price and strategy alerts'
      },
      {
        label: 'Enterprise Dashboard',
        href: '/intranet/dashboard',
        icon: Monitor,
        description: 'Corporate intranet control center',
        badge: 'New'
      },
      {
        label: 'Intranet Control',
        href: '/intranet',
        icon: Globe,
        description: 'Corporate network management',
        badge: 'Admin'
      },
      {
        label: 'Network Optimizer',
        href: '/intranet/network',
        icon: Monitor,
        description: 'Local network performance optimization'
      },
      {
        label: 'Corporate Auth',
        href: '/intranet/auth',
        icon: Shield,
        description: 'Enterprise authentication system'
      },
      {
        label: 'Security Audit',
        href: '/intranet/security',
        icon: Shield,
        description: 'Security event monitoring'
      }
    ]
  },
  {
    label: 'Exchanges',
    icon: Globe,
    items: [
      {
        label: 'All Exchanges',
        href: '/exchanges',
        icon: Building2,
        description: 'Browse all supported exchanges',
        badge: 'CCXT'
      },
      {
        label: 'Exchange Settings',
        href: '/settings/exchanges',
        icon: Settings,
        description: 'Configure API keys and settings'
      },
      {
        label: 'Connection Status',
        href: '/exchanges/status',
        icon: Activity,
        description: 'Monitor exchange connectivity'
      },
      {
        label: 'Trading Fees',
        href: '/exchanges/fees',
        icon: DollarSign,
        description: 'Compare trading fees across exchanges'
      }
    ]
  }
];

export function MegaMenu({ className = '' }: MegaMenuProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);
  const pathname = usePathname();

  const toggleMenu = () => {
    setIsOpen(!isOpen);
    setActiveDropdown(null);
  };

  const handleDropdownToggle = (label: string) => {
    setActiveDropdown(activeDropdown === label ? null : label);
  };

  const isActivePath = (href: string) => {
    return pathname === href || pathname.startsWith(href + '/');
  };

  return (
    <nav className={`bg-slate-900 border-b border-slate-800 ${className}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <TrendingUp className="h-8 w-8 text-blue-400" />
              <span className="text-xl font-bold text-white">AlgoProject</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden lg:block">
            <div className="flex items-center space-x-1">
              {menuItems.map((item) => (
                <div
                  key={item.label}
                  className="relative"
                  onMouseEnter={() => setActiveDropdown(item.label)}
                  onMouseLeave={() => setActiveDropdown(null)}
                >
                  {item.href ? (
                    <Link
                      href={item.href}
                      className={`flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                        isActivePath(item.href)
                          ? 'bg-blue-600 text-white'
                          : 'text-slate-300 hover:text-white hover:bg-slate-800'
                      }`}
                    >
                      <item.icon className="h-4 w-4 mr-2" />
                      {item.label}
                    </Link>
                  ) : (
                    <button
                      className={`flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                        activeDropdown === item.label
                          ? 'bg-slate-800 text-white'
                          : 'text-slate-300 hover:text-white hover:bg-slate-800'
                      }`}
                    >
                      <item.icon className="h-4 w-4 mr-2" />
                      {item.label}
                      <ChevronDown className="h-3 w-3 ml-1" />
                    </button>
                  )}

                  {/* Mega Menu Dropdown */}
                  {item.items && activeDropdown === item.label && (
                    <div className="absolute top-full left-0 mt-1 w-80 bg-slate-900 border border-slate-700 rounded-xl shadow-2xl z-50">
                      <div className="p-4">
                        <div className="grid grid-cols-1 gap-2">
                          {item.items.map((subItem) => (
                            <Link
                              key={subItem.label}
                              href={subItem.href || '#'}
                              className={`flex items-start p-3 rounded-lg transition-colors group ${
                                subItem.href && isActivePath(subItem.href)
                                  ? 'bg-blue-600/20 text-blue-300'
                                  : 'hover:bg-slate-800 text-slate-300 hover:text-white'
                              }`}
                              onClick={() => setActiveDropdown(null)}
                            >
                              <subItem.icon className="h-5 w-5 mt-0.5 mr-3 text-blue-400 group-hover:text-blue-300" />
                              <div className="flex-1">
                                <div className="flex items-center">
                                  <span className="font-medium">{subItem.label}</span>
                                  {subItem.badge && (
                                    <span className="ml-2 px-2 py-0.5 bg-blue-600 text-blue-100 text-xs rounded-full">
                                      {subItem.badge}
                                    </span>
                                  )}
                                  {subItem.isNew && (
                                    <span className="ml-2 px-2 py-0.5 bg-green-600 text-green-100 text-xs rounded-full">
                                      New
                                    </span>
                                  )}
                                </div>
                                {subItem.description && (
                                  <p className="text-xs text-slate-400 mt-1 group-hover:text-slate-300">
                                    {subItem.description}
                                  </p>
                                )}
                              </div>
                            </Link>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Right Side Icons */}
          <div className="flex items-center space-x-4">
            {/* Search */}
            <button className="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors">
              <Search className="h-5 w-5" />
            </button>

            {/* Notifications */}
            <button className="relative p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors">
              <Bell className="h-5 w-5" />
              <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></span>
            </button>

            {/* Settings */}
            <Link
              href="/settings"
              className="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors"
            >
              <Settings className="h-5 w-5" />
            </Link>

            {/* Profile */}
            <div className="relative">
              <button className="flex items-center space-x-2 p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors">
                <User className="h-5 w-5" />
                <span className="hidden md:block text-sm">Trader</span>
              </button>
            </div>

            {/* Mobile menu button */}
            <button
              onClick={toggleMenu}
              className="lg:hidden p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors"
            >
              {isOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="lg:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 border-t border-slate-800">
              {menuItems.map((item) => (
                <div key={item.label}>
                  {item.href ? (
                    <Link
                      href={item.href}
                      className={`flex items-center px-3 py-2 rounded-lg text-base font-medium transition-colors ${
                        isActivePath(item.href)
                          ? 'bg-blue-600 text-white'
                          : 'text-slate-300 hover:text-white hover:bg-slate-800'
                      }`}
                      onClick={() => setIsOpen(false)}
                    >
                      <item.icon className="h-5 w-5 mr-3" />
                      {item.label}
                    </Link>
                  ) : (
                    <>
                      <button
                        onClick={() => handleDropdownToggle(item.label)}
                        className="w-full flex items-center justify-between px-3 py-2 rounded-lg text-base font-medium text-slate-300 hover:text-white hover:bg-slate-800 transition-colors"
                      >
                        <div className="flex items-center">
                          <item.icon className="h-5 w-5 mr-3" />
                          {item.label}
                        </div>
                        <ChevronDown 
                          className={`h-4 w-4 transition-transform ${
                            activeDropdown === item.label ? 'rotate-180' : ''
                          }`} 
                        />
                      </button>
                      
                      {item.items && activeDropdown === item.label && (
                        <div className="ml-6 mt-2 space-y-1">
                          {item.items.map((subItem) => (
                            <Link
                              key={subItem.label}
                              href={subItem.href || '#'}
                              className={`flex items-center px-3 py-2 rounded-lg text-sm transition-colors ${
                                subItem.href && isActivePath(subItem.href)
                                  ? 'bg-blue-600/20 text-blue-300'
                                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
                              }`}
                              onClick={() => setIsOpen(false)}
                            >
                              <subItem.icon className="h-4 w-4 mr-3" />
                              <div>
                                <div className="flex items-center">
                                  {subItem.label}
                                  {subItem.badge && (
                                    <span className="ml-2 px-1.5 py-0.5 bg-blue-600 text-blue-100 text-xs rounded">
                                      {subItem.badge}
                                    </span>
                                  )}
                                  {subItem.isNew && (
                                    <span className="ml-2 px-1.5 py-0.5 bg-green-600 text-green-100 text-xs rounded">
                                      New
                                    </span>
                                  )}
                                </div>
                              </div>
                            </Link>
                          ))}
                        </div>
                      )}
                    </>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}