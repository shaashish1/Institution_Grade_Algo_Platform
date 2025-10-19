'use client';

import React from 'react';
import { FileText, Shield, AlertTriangle, Scale, Clock, Mail } from 'lucide-react';
import Link from 'next/link';

export function TermsOfService() {
  return (
    <div className="min-h-screen bg-slate-950 text-white p-4">
      <div className="max-w-4xl mx-auto">
        {/* Navigation Breadcrumb */}
        <div className="mb-6">
          <nav className="flex items-center space-x-2 text-sm text-slate-400">
            <Link href="/" className="hover:text-blue-400 transition-colors">Home</Link>
            <span>/</span>
            <span className="text-white">Terms of Service</span>
          </nav>
        </div>

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-4">
            Terms of Service
          </h1>
          <div className="flex items-center space-x-4 text-slate-400">
            <div className="flex items-center">
              <Clock className="h-4 w-4 mr-2" />
              <span>Last updated: October 20, 2024</span>
            </div>
            <div className="flex items-center">
              <FileText className="h-4 w-4 mr-2" />
              <span>Version 2.1</span>
            </div>
          </div>
        </div>

        {/* Important Notice */}
        <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-xl p-6 mb-8">
          <div className="flex items-start space-x-3">
            <AlertTriangle className="h-6 w-6 text-yellow-400 mt-1" />
            <div>
              <h2 className="text-lg font-bold text-yellow-400 mb-2">Important Notice</h2>
              <p className="text-yellow-200">
                Trading in financial instruments involves substantial risk of loss and is not suitable for all investors. 
                Please read these terms carefully before using our platform.
              </p>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="prose prose-invert prose-blue max-w-none">
          <div className="bg-slate-900 rounded-xl p-8 border border-slate-800 space-y-8">
            
            <section>
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
                <Scale className="h-6 w-6 mr-3 text-blue-400" />
                1. Acceptance of Terms
              </h2>
              <div className="text-slate-300 space-y-4">
                <p>
                  By accessing and using AlgoProject ("the Platform", "our Service"), you accept and agree to be bound by the terms and provision of this agreement.
                </p>
                <p>
                  These Terms of Service ("Terms") govern your use of our algorithmic trading platform, including but not limited to:
                </p>
                <ul className="list-disc list-inside space-y-2 ml-4">
                  <li>NSE and BSE equity trading services</li>
                  <li>Options chain analysis and trading</li>
                  <li>Cryptocurrency trading integration</li>
                  <li>Backtesting and strategy development tools</li>
                  <li>Portfolio management and analytics</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
                <Shield className="h-6 w-6 mr-3 text-green-400" />
                2. Eligibility and Account Registration
              </h2>
              <div className="text-slate-300 space-y-4">
                <p>
                  <strong>2.1 Age Requirement:</strong> You must be at least 18 years old to use our services.
                </p>
                <p>
                  <strong>2.2 Legal Capacity:</strong> You represent that you have the legal capacity to enter into these Terms.
                </p>
                <p>
                  <strong>2.3 Regulatory Compliance:</strong> You must comply with all applicable laws and regulations in your jurisdiction, including:
                </p>
                <ul className="list-disc list-inside space-y-2 ml-4">
                  <li>Securities and Exchange Board of India (SEBI) regulations</li>
                  <li>Reserve Bank of India (RBI) guidelines for digital payments</li>
                  <li>Income Tax Act requirements for capital gains reporting</li>
                  <li>Foreign Exchange Management Act (FEMA) for international transactions</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">3. Trading Services and Risk Disclosure</h2>
              <div className="text-slate-300 space-y-4">
                <p>
                  <strong>3.1 Risk Warning:</strong> Trading in financial instruments carries inherent risks, including:
                </p>
                <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4">
                  <ul className="list-disc list-inside space-y-2">
                    <li>Substantial risk of loss of capital</li>
                    <li>Market volatility and price fluctuations</li>
                    <li>Liquidity risks in certain instruments</li>
                    <li>Counterparty and settlement risks</li>
                    <li>Technology and system failures</li>
                  </ul>
                </div>
                <p>
                  <strong>3.2 No Investment Advice:</strong> Our platform provides analytical tools and data but does not constitute investment advice. All trading decisions are solely your responsibility.
                </p>
                <p>
                  <strong>3.3 Algorithmic Trading:</strong> Automated strategies may result in rapid losses. You should thoroughly test strategies before live deployment.
                </p>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">4. Data Usage and Market Information</h2>
              <div className="text-slate-300 space-y-4">
                <p>
                  <strong>4.1 Market Data License:</strong> We provide market data under license agreements with NSE, BSE, and other data providers. This data is for your personal use only.
                </p>
                <p>
                  <strong>4.2 Data Accuracy:</strong> While we strive for accuracy, we do not guarantee the completeness or accuracy of market data and are not liable for any losses resulting from data errors.
                </p>
                <p>
                  <strong>4.3 Redistribution:</strong> You may not redistribute, retransmit, or make market data available to third parties without authorization.
                </p>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">5. Fees and Charges</h2>
              <div className="text-slate-300 space-y-4">
                <p>
                  <strong>5.1 Service Fees:</strong> Subscription fees are charged monthly or annually as per your chosen plan.
                </p>
                <p>
                  <strong>5.2 Transaction Charges:</strong> Trading fees, exchange charges, and regulatory fees apply as per current rate cards.
                </p>
                <p>
                  <strong>5.3 Fee Changes:</strong> We reserve the right to modify fees with 30 days advance notice.
                </p>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">6. Intellectual Property</h2>
              <div className="text-slate-300 space-y-4">
                <p>
                  <strong>6.1 Platform Ownership:</strong> All intellectual property rights in the platform, including algorithms, software, and proprietary indicators, belong to AlgoProject.
                </p>
                <p>
                  <strong>6.2 User Content:</strong> You retain ownership of your trading strategies and data, but grant us license to process this data to provide our services.
                </p>
                <p>
                  <strong>6.3 Restrictions:</strong> You may not reverse engineer, decompile, or attempt to extract source code from our platform.
                </p>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">7. Limitation of Liability</h2>
              <div className="text-slate-300 space-y-4">
                <p>
                  <strong>7.1 Disclaimer:</strong> Our platform is provided "as is" without warranties of any kind.
                </p>
                <p>
                  <strong>7.2 Liability Cap:</strong> Our liability is limited to the amount of fees paid by you in the 12 months preceding the claim.
                </p>
                <p>
                  <strong>7.3 Exclusions:</strong> We are not liable for indirect, consequential, or punitive damages.
                </p>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">8. Privacy and Data Protection</h2>
              <div className="text-slate-300 space-y-4">
                <p>
                  Your privacy is important to us. Please review our <Link href="/privacy" className="text-blue-400 hover:text-blue-300">Privacy Policy</Link> to understand how we collect, use, and protect your personal information.
                </p>
                <p>
                  <strong>8.1 Data Security:</strong> We implement industry-standard security measures to protect your data.
                </p>
                <p>
                  <strong>8.2 Data Retention:</strong> We retain your data as required by regulatory obligations and our legitimate business interests.
                </p>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">9. Termination</h2>
              <div className="text-slate-300 space-y-4">
                <p>
                  <strong>9.1 Termination by You:</strong> You may terminate your account at any time by providing written notice.
                </p>
                <p>
                  <strong>9.2 Termination by Us:</strong> We may terminate your access for breach of terms, regulatory requirements, or at our discretion with reasonable notice.
                </p>
                <p>
                  <strong>9.3 Effect of Termination:</strong> Upon termination, your right to use the platform ceases, but these terms remain binding regarding past use.
                </p>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">10. Governing Law and Dispute Resolution</h2>
              <div className="text-slate-300 space-y-4">
                <p>
                  <strong>10.1 Governing Law:</strong> These Terms are governed by the laws of India.
                </p>
                <p>
                  <strong>10.2 Jurisdiction:</strong> Any disputes shall be subject to the exclusive jurisdiction of courts in Mumbai, India.
                </p>
                <p>
                  <strong>10.3 Arbitration:</strong> Disputes may be resolved through arbitration under the Arbitration and Conciliation Act, 2015.
                </p>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">11. Contact Information</h2>
              <div className="text-slate-300 space-y-4">
                <p>
                  For questions about these Terms of Service, please contact us:
                </p>
                <div className="bg-slate-800 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <Mail className="h-4 w-4 mr-2 text-blue-400" />
                    <span>Email: legal@algoproject.com</span>
                  </div>
                  <div className="flex items-center">
                    <FileText className="h-4 w-4 mr-2 text-blue-400" />
                    <span>Address: AlgoProject Legal Department, Mumbai, India</span>
                  </div>
                </div>
              </div>
            </section>

          </div>
        </div>

        {/* Footer Links */}
        <div className="mt-8 pt-8 border-t border-slate-800">
          <div className="flex flex-wrap gap-6 justify-center text-slate-400">
            <Link href="/privacy" className="hover:text-blue-400 transition-colors">Privacy Policy</Link>
            <Link href="/risk-disclosure" className="hover:text-blue-400 transition-colors">Risk Disclosure</Link>
            <Link href="/compliance" className="hover:text-blue-400 transition-colors">Compliance</Link>
            <Link href="/cookies" className="hover:text-blue-400 transition-colors">Cookie Policy</Link>
          </div>
        </div>
      </div>
    </div>
  );
}