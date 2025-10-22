import ComingSoon from '@/components/ComingSoon';
import { Shield } from 'lucide-react';

export default function RiskPage() {
  return (
    <ComingSoon
      title="Risk Management"
      description="Advanced risk assessment and portfolio protection tools"
      expectedLaunch="November 2025"
      icon={<Shield className="w-10 h-10 text-blue-600 dark:text-blue-400" />}
      features={[
        'Portfolio risk analysis',
        'Position sizing calculator',
        'Stop-loss recommendations',
        'Risk/reward ratio calculator',
        'Portfolio diversification metrics'
      ]}
    />
  );
}
