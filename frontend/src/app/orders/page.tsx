'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { 
  ShoppingCart, Clock, CheckCircle, XCircle, Filter,
  Download, Search, Calendar, TrendingUp, Activity,
  ArrowUp, ArrowDown, Info, RefreshCw, Eye
} from 'lucide-react';

type OrderStatus = 'pending' | 'executed' | 'cancelled' | 'rejected';
type OrderType = 'market' | 'limit' | 'stop_loss' | 'bracket';

interface Order {
  id: string;
  symbol: string;
  type: OrderType;
  side: 'buy' | 'sell';
  quantity: number;
  price: number;
  status: OrderStatus;
  timestamp: string;
  filledQty?: number;
  averagePrice?: number;
}

export default function OrdersPage() {
  const [filterStatus, setFilterStatus] = useState<OrderStatus | 'all'>('all');
  const [searchQuery, setSearchQuery] = useState('');

  const orders: Order[] = [
    {
      id: 'ORD001234',
      symbol: 'RELIANCE',
      type: 'limit',
      side: 'buy',
      quantity: 50,
      price: 2450.00,
      status: 'executed',
      timestamp: '2025-10-21 09:35:24',
      filledQty: 50,
      averagePrice: 2448.50
    },
    {
      id: 'ORD001235',
      symbol: 'TCS',
      type: 'market',
      side: 'sell',
      quantity: 30,
      price: 3625.00,
      status: 'executed',
      timestamp: '2025-10-21 10:15:42',
      filledQty: 30,
      averagePrice: 3626.20
    },
    {
      id: 'ORD001236',
      symbol: 'INFY',
      type: 'limit',
      side: 'buy',
      quantity: 100,
      price: 1550.00,
      status: 'pending',
      timestamp: '2025-10-21 11:22:15'
    },
    {
      id: 'ORD001237',
      symbol: 'HDFC',
      type: 'stop_loss',
      side: 'sell',
      quantity: 25,
      price: 1650.00,
      status: 'cancelled',
      timestamp: '2025-10-21 12:05:33'
    },
    {
      id: 'ORD001238',
      symbol: 'ICICI',
      type: 'bracket',
      side: 'buy',
      quantity: 75,
      price: 975.00,
      status: 'rejected',
      timestamp: '2025-10-21 13:18:47'
    },
  ];

  const getStatusIcon = (status: OrderStatus) => {
    switch (status) {
      case 'executed':
        return <CheckCircle className="h-5 w-5 text-green-400" />;
      case 'pending':
        return <Clock className="h-5 w-5 text-yellow-400" />;
      case 'cancelled':
      case 'rejected':
        return <XCircle className="h-5 w-5 text-red-400" />;
    }
  };

  const getStatusColor = (status: OrderStatus) => {
    switch (status) {
      case 'executed':
        return 'bg-green-500/10 text-green-400 border-green-500/20';
      case 'pending':
        return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20';
      case 'cancelled':
      case 'rejected':
        return 'bg-red-500/10 text-red-400 border-red-500/20';
    }
  };

  const getTypeColor = (type: OrderType) => {
    switch (type) {
      case 'market':
        return 'bg-blue-500/10 text-blue-400';
      case 'limit':
        return 'bg-purple-500/10 text-purple-400';
      case 'stop_loss':
        return 'bg-orange-500/10 text-orange-400';
      case 'bracket':
        return 'bg-pink-500/10 text-pink-400';
    }
  };

  const filteredOrders = orders.filter(order => {
    const matchesStatus = filterStatus === 'all' || order.status === filterStatus;
    const matchesSearch = order.symbol.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          order.id.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesStatus && matchesSearch;
  });

  const orderStats = {
    total: orders.length,
    executed: orders.filter(o => o.status === 'executed').length,
    pending: orders.filter(o => o.status === 'pending').length,
    cancelled: orders.filter(o => o.status === 'cancelled' || o.status === 'rejected').length
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Breadcrumb */}
      <div className="bg-slate-900 border-b border-slate-800 px-6 py-4">
        <nav className="flex items-center space-x-2 text-sm text-slate-400">
          <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
          <span>/</span>
          <span className="text-white">Order Management</span>
        </nav>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
                Order Management
              </h1>
              <p className="text-xl text-slate-300">
                Track and manage your trading orders
              </p>
            </div>
            
            <div className="flex items-center space-x-4">
              <button className="flex items-center space-x-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors">
                <RefreshCw className="h-4 w-4" />
                <span>Refresh</span>
              </button>
              <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors">
                <Download className="h-4 w-4" />
                <span>Export</span>
              </button>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-slate-400">Total Orders</span>
              <ShoppingCart className="h-5 w-5 text-blue-400" />
            </div>
            <div className="text-2xl font-bold text-white">{orderStats.total}</div>
            <div className="text-sm text-slate-400 mt-1">All time</div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-slate-400">Executed</span>
              <CheckCircle className="h-5 w-5 text-green-400" />
            </div>
            <div className="text-2xl font-bold text-green-400">{orderStats.executed}</div>
            <div className="text-sm text-slate-400 mt-1">
              {((orderStats.executed / orderStats.total) * 100).toFixed(0)}% success rate
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-slate-400">Pending</span>
              <Clock className="h-5 w-5 text-yellow-400" />
            </div>
            <div className="text-2xl font-bold text-yellow-400">{orderStats.pending}</div>
            <div className="text-sm text-slate-400 mt-1">Awaiting execution</div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-slate-400">Cancelled/Rejected</span>
              <XCircle className="h-5 w-5 text-red-400" />
            </div>
            <div className="text-2xl font-bold text-red-400">{orderStats.cancelled}</div>
            <div className="text-sm text-slate-400 mt-1">Failed orders</div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Search */}
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-2">Search Orders</label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search by symbol or order ID..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg pl-10 pr-4 py-2 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            {/* Status Filter */}
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-2">Filter by Status</label>
              <div className="flex space-x-2">
                {['all', 'executed', 'pending', 'cancelled'].map((status) => (
                  <button
                    key={status}
                    onClick={() => setFilterStatus(status as OrderStatus | 'all')}
                    className={`flex-1 px-4 py-2 rounded-lg font-medium capitalize transition-colors ${
                      filterStatus === status
                        ? 'bg-blue-600 text-white'
                        : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                    }`}
                  >
                    {status}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Orders Table */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-slate-800/50 border-b border-slate-700">
                  <th className="text-left py-4 px-6 text-sm font-medium text-slate-400">Order ID</th>
                  <th className="text-left py-4 px-6 text-sm font-medium text-slate-400">Symbol</th>
                  <th className="text-left py-4 px-6 text-sm font-medium text-slate-400">Type</th>
                  <th className="text-left py-4 px-6 text-sm font-medium text-slate-400">Side</th>
                  <th className="text-right py-4 px-6 text-sm font-medium text-slate-400">Quantity</th>
                  <th className="text-right py-4 px-6 text-sm font-medium text-slate-400">Price</th>
                  <th className="text-left py-4 px-6 text-sm font-medium text-slate-400">Status</th>
                  <th className="text-left py-4 px-6 text-sm font-medium text-slate-400">Timestamp</th>
                  <th className="text-center py-4 px-6 text-sm font-medium text-slate-400">Action</th>
                </tr>
              </thead>
              <tbody>
                {filteredOrders.map((order, index) => (
                  <tr key={order.id} className="border-b border-slate-800 hover:bg-slate-800/50 transition-colors">
                    <td className="py-4 px-6">
                      <div className="font-mono text-sm text-blue-400">{order.id}</div>
                    </td>
                    <td className="py-4 px-6">
                      <div className="font-medium text-white">{order.symbol}</div>
                    </td>
                    <td className="py-4 px-6">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium uppercase ${getTypeColor(order.type)}`}>
                        {order.type.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="py-4 px-6">
                      <div className={`flex items-center space-x-1 ${
                        order.side === 'buy' ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {order.side === 'buy' ? <ArrowUp className="h-4 w-4" /> : <ArrowDown className="h-4 w-4" />}
                        <span className="font-medium uppercase">{order.side}</span>
                      </div>
                    </td>
                    <td className="py-4 px-6 text-right">
                      <div className="font-mono text-white">{order.quantity}</div>
                      {order.filledQty && (
                        <div className="text-xs text-slate-400">Filled: {order.filledQty}</div>
                      )}
                    </td>
                    <td className="py-4 px-6 text-right">
                      <div className="font-mono text-white">₹{order.price.toFixed(2)}</div>
                      {order.averagePrice && (
                        <div className="text-xs text-slate-400">Avg: ₹{order.averagePrice.toFixed(2)}</div>
                      )}
                    </td>
                    <td className="py-4 px-6">
                      <div className={`flex items-center space-x-2 px-3 py-1 rounded-lg border w-fit ${getStatusColor(order.status)}`}>
                        {getStatusIcon(order.status)}
                        <span className="text-sm font-medium capitalize">{order.status}</span>
                      </div>
                    </td>
                    <td className="py-4 px-6">
                      <div className="text-sm text-slate-300">{order.timestamp}</div>
                    </td>
                    <td className="py-4 px-6">
                      <div className="flex items-center justify-center space-x-2">
                        <button className="p-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors">
                          <Eye className="h-4 w-4 text-slate-300" />
                        </button>
                        {order.status === 'pending' && (
                          <button className="p-2 bg-red-600/10 hover:bg-red-600/20 rounded-lg transition-colors">
                            <XCircle className="h-4 w-4 text-red-400" />
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {filteredOrders.length === 0 && (
            <div className="text-center py-12">
              <ShoppingCart className="h-12 w-12 text-slate-600 mx-auto mb-4" />
              <p className="text-slate-400">No orders found matching your criteria</p>
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          <Link href="/trading" className="bg-slate-900 border border-slate-800 rounded-xl p-6 hover:border-green-500 transition-colors group">
            <TrendingUp className="h-8 w-8 text-green-400 mb-4" />
            <h3 className="text-lg font-bold text-white mb-2">Place New Order</h3>
            <p className="text-sm text-slate-400">Start live trading</p>
          </Link>

          <Link href="/portfolio" className="bg-slate-900 border border-slate-800 rounded-xl p-6 hover:border-blue-500 transition-colors group">
            <Activity className="h-8 w-8 text-blue-400 mb-4" />
            <h3 className="text-lg font-bold text-white mb-2">View Positions</h3>
            <p className="text-sm text-slate-400">Check active positions</p>
          </Link>

          <Link href="/analytics" className="bg-slate-900 border border-slate-800 rounded-xl p-6 hover:border-purple-500 transition-colors group">
            <ShoppingCart className="h-8 w-8 text-purple-400 mb-4" />
            <h3 className="text-lg font-bold text-white mb-2">Order History</h3>
            <p className="text-sm text-slate-400">View detailed order history</p>
          </Link>
        </div>

        {/* Info Banner */}
        <div className="mt-8 bg-blue-500/10 border border-blue-500/20 rounded-xl p-4">
          <div className="flex items-start space-x-3">
            <Info className="h-5 w-5 text-blue-400 mt-0.5 flex-shrink-0" />
            <div className="flex-1">
              <p className="text-sm text-blue-200">
                <strong>Order Management:</strong> You can modify or cancel pending orders at any time. 
                Executed orders cannot be reversed. For support, contact our 24/7 trading desk.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
