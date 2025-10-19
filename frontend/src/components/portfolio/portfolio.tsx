'use client';

export function Portfolio() {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white">Portfolio Management</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-900 rounded-lg border border-slate-700 p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Total Balance</h3>
          <p className="text-3xl font-bold text-green-400">$12,345.67</p>
        </div>
        <div className="bg-slate-900 rounded-lg border border-slate-700 p-6">
          <h3 className="text-lg font-semibold text-white mb-4">24h P&L</h3>
          <p className="text-3xl font-bold text-green-400">+$234.56</p>
        </div>
        <div className="bg-slate-900 rounded-lg border border-slate-700 p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Active Positions</h3>
          <p className="text-3xl font-bold text-white">5</p>
        </div>
      </div>
    </div>
  );
}