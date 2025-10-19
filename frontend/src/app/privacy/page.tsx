'use client';

import React from 'react';
import { ArrowLeft, Shield, Eye, Lock, Cookie } from 'lucide-react';
import Link from 'next/link';

export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-slate-900 text-white">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-600 to-blue-600 py-12">
        <div className="max-w-6xl mx-auto px-4">
          <Link href="/" className="inline-flex items-center text-green-200 hover:text-white mb-6 transition-colors">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Home
          </Link>
          <h1 className="text-4xl font-bold mb-4">Privacy Policy</h1>
          <p className="text-xl text-green-100 max-w-3xl">
            Your privacy is our priority. Learn how we collect, use, and protect your personal information.
          </p>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="prose prose-invert prose-blue max-w-none">
          <div className="bg-blue-900/20 border border-blue-500 rounded-lg p-6 mb-8">
            <h2 className="text-xl font-semibold mb-3 flex items-center">
              <Shield className="h-5 w-5 text-blue-400 mr-2" />
              Privacy Commitment
            </h2>
            <p className="text-slate-300 mb-0">
              <strong>Last Updated:</strong> October 19, 2025<br />
              <strong>Effective Date:</strong> October 19, 2025
            </p>
          </div>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6 flex items-center">
              <Eye className="h-6 w-6 text-green-400 mr-3" />
              Information We Collect
            </h2>
            
            <h3 className="text-xl font-semibold mb-4 text-blue-400">Personal Information</h3>
            <ul className="text-slate-300 space-y-2 mb-6">
              <li>• <strong>Account Information:</strong> Name, email address, phone number</li>
              <li>• <strong>Identity Verification:</strong> Government-issued ID, address verification</li>
              <li>• <strong>Financial Information:</strong> Bank account details, trading history</li>
              <li>• <strong>Authentication Data:</strong> Login credentials, API keys</li>
            </ul>

            <h3 className="text-xl font-semibold mb-4 text-purple-400">Technical Information</h3>
            <ul className="text-slate-300 space-y-2 mb-6">
              <li>• <strong>Device Information:</strong> IP address, browser type, operating system</li>
              <li>• <strong>Usage Data:</strong> Platform interactions, feature usage patterns</li>
              <li>• <strong>Trading Data:</strong> Order history, portfolio performance, strategy parameters</li>
              <li>• <strong>Communication Records:</strong> Support tickets, chat logs</li>
            </ul>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6 flex items-center">
              <Lock className="h-6 w-6 text-purple-400 mr-3" />
              How We Use Your Information
            </h2>
            
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-slate-800 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4 text-blue-400">Platform Operations</h3>
                <ul className="text-slate-300 space-y-2 text-sm">
                  <li>✓ Account management and authentication</li>
                  <li>✓ Trade execution and settlement</li>
                  <li>✓ Portfolio tracking and reporting</li>
                  <li>✓ Customer support services</li>
                </ul>
              </div>
              <div className="bg-slate-800 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4 text-green-400">Compliance & Security</h3>
                <ul className="text-slate-300 space-y-2 text-sm">
                  <li>✓ Regulatory compliance (KYC/AML)</li>
                  <li>✓ Fraud prevention and detection</li>
                  <li>✓ Risk management and monitoring</li>
                  <li>✓ Legal obligation fulfillment</li>
                </ul>
              </div>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6 flex items-center">
              <Cookie className="h-6 w-6 text-orange-400 mr-3" />
              Cookies & Tracking
            </h2>
            
            <div className="bg-slate-800 rounded-lg p-6 mb-6">
              <h3 className="text-lg font-semibold mb-4 text-orange-400">Cookie Types</h3>
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold text-blue-400 mb-2">Essential Cookies</h4>
                  <p className="text-slate-300 text-sm">Required for platform functionality, security, and authentication.</p>
                </div>
                <div>
                  <h4 className="font-semibold text-green-400 mb-2">Performance Cookies</h4>
                  <p className="text-slate-300 text-sm">Help us understand how users interact with our platform to improve performance.</p>
                </div>
                <div>
                  <h4 className="font-semibold text-purple-400 mb-2">Preference Cookies</h4>
                  <p className="text-slate-300 text-sm">Remember your settings and preferences for a personalized experience.</p>
                </div>
              </div>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6 text-red-400">Data Sharing & Disclosure</h2>
            
            <div className="bg-red-900/20 border border-red-500 rounded-lg p-6 mb-6">
              <h3 className="text-lg font-semibold mb-4 text-red-400">We DO NOT sell your personal data</h3>
              <p className="text-slate-300 text-sm">
                AlgoProject never sells, rents, or trades your personal information to third parties for marketing purposes.
              </p>
            </div>

            <h3 className="text-xl font-semibold mb-4 text-blue-400">Limited Sharing</h3>
            <ul className="text-slate-300 space-y-2">
              <li>• <strong>Service Providers:</strong> Vetted third-party services (payment processors, data centers)</li>
              <li>• <strong>Regulatory Authorities:</strong> When required by law or regulation</li>
              <li>• <strong>Legal Requirements:</strong> Court orders, government requests</li>
              <li>• <strong>Business Transfers:</strong> In case of merger, acquisition, or sale (with notice)</li>
            </ul>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6 text-green-400">Your Rights</h2>
            
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-slate-800 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4 text-blue-400">Access & Control</h3>
                <ul className="text-slate-300 space-y-2 text-sm">
                  <li>✓ View your personal data</li>
                  <li>✓ Update account information</li>
                  <li>✓ Download your data</li>
                  <li>✓ Delete your account</li>
                </ul>
              </div>
              <div className="bg-slate-800 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4 text-purple-400">Privacy Controls</h3>
                <ul className="text-slate-300 space-y-2 text-sm">
                  <li>✓ Opt-out of marketing emails</li>
                  <li>✓ Manage cookie preferences</li>
                  <li>✓ Restrict data processing</li>
                  <li>✓ Request data correction</li>
                </ul>
              </div>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6 text-purple-400">Data Security</h2>
            
            <div className="bg-slate-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4 text-green-400">Security Measures</h3>
              <div className="grid md:grid-cols-2 gap-4">
                <ul className="text-slate-300 space-y-2 text-sm">
                  <li>🔐 End-to-end encryption</li>
                  <li>🔐 Multi-factor authentication</li>
                  <li>🔐 Regular security audits</li>
                  <li>🔐 Secure data centers</li>
                </ul>
                <ul className="text-slate-300 space-y-2 text-sm">
                  <li>🛡️ Access controls and monitoring</li>
                  <li>🛡️ Data backup and recovery</li>
                  <li>🛡️ Incident response procedures</li>
                  <li>🛡️ Employee security training</li>
                </ul>
              </div>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6 text-orange-400">Contact Us</h2>
            
            <div className="bg-slate-800 rounded-lg p-6">
              <p className="text-slate-300 mb-4">
                For privacy-related questions or to exercise your rights, contact our Data Protection Officer:
              </p>
              <div className="space-y-2 text-slate-300">
                <p><strong>Email:</strong> privacy@algoproject.in</p>
                <p><strong>Phone:</strong> +91-22-1234-5678</p>
                <p><strong>Address:</strong> Data Protection Officer, AlgoProject Technologies Pvt Ltd,<br />
                   BKC, Mumbai, Maharashtra 400051, India</p>
              </div>
            </div>
          </section>

          <div className="bg-blue-900/20 border border-blue-500 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-3 text-blue-400">Policy Updates</h3>
            <p className="text-slate-300 text-sm">
              We may update this privacy policy from time to time. Significant changes will be notified 
              via email and platform notifications. Continued use of our services after updates 
              constitutes acceptance of the revised policy.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}