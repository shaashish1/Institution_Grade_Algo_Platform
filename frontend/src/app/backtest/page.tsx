import ComingSoon from '@/components/ComingSoon';
import { Activity } from 'lucide-react';

export default function BacktestPage() {
  return (
    <ComingSoon
      title="Backtesting Hub"
      description="Central hub for all your backtesting needs - stocks, crypto, and multi-strategy testing"
      expectedLaunch="November 2025"
      icon={<Activity className="w-10 h-10 text-blue-600 dark:text-blue-400" />}
      features={[
        'Historical strategy testing',
        'Performance metrics and reports',
        'Multi-timeframe analysis',
        'Strategy comparison tools',
        'Walk-forward optimization'
      ]}
    />
  );
}
