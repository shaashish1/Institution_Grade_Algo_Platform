import ComingSoon from '@/components/ComingSoon';
import { PieChart } from 'lucide-react';

export default function ETFPage() {
  return (
    <ComingSoon
      title="ETF Trading"
      description="Trade and analyze Exchange Traded Funds"
      expectedLaunch="November 2025"
      icon={<PieChart className="w-10 h-10 text-blue-600 dark:text-blue-400" />}
      features={[
        'ETF screener and comparison',
        'Holdings analysis',
        'Performance tracking',
        'Sector allocation',
        'Expense ratio comparison'
      ]}
    />
  );
}
