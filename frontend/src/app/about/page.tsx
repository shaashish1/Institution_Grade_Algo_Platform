'use client';

import React from 'react';
import { ArrowLeft, Users, Target, Award, Globe } from 'lucide-react';
import Link from 'next/link';

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-slate-900 text-white">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 py-12">
        <div className="max-w-6xl mx-auto px-4">
          <Link href="/" className="inline-flex items-center text-blue-200 hover:text-white mb-6 transition-colors">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Home
          </Link>
          <h1 className="text-4xl font-bold mb-4">About AlgoProject</h1>
          <p className="text-xl text-blue-100 max-w-3xl">
            Pioneering the future of algorithmic trading with cutting-edge technology and institutional-grade infrastructure.
          </p>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto px-4 py-12">
        {/* Mission Section */}
        <section className="mb-16">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold mb-6 flex items-center">
                <Target className="h-8 w-8 text-blue-400 mr-3" />
                Our Mission
              </h2>
              <p className="text-slate-300 text-lg leading-relaxed mb-6">
                At AlgoProject, we democratize algorithmic trading by providing institutional-grade 
                tools and infrastructure to individual traders and small funds. Our platform combines 
                advanced AI, real-time data processing, and sophisticated risk management to level 
                the playing field in financial markets.
              </p>
              <p className="text-slate-300 text-lg leading-relaxed">
                We believe that everyone should have access to the same powerful trading technologies 
                that drive the world's largest hedge funds and investment banks.
              </p>
            </div>
            <div className="bg-slate-800 rounded-2xl p-8">
              <h3 className="text-xl font-semibold mb-4 text-blue-400">Key Statistics</h3>
              <div className="space-y-4">
                <div className="flex justify-between">
                  <span className="text-slate-300">Active Users</span>
                  <span className="font-bold text-green-400">10,000+</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-300">Total Trades Executed</span>
                  <span className="font-bold text-blue-400">1M+</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-300">Average Success Rate</span>
                  <span className="font-bold text-purple-400">78.5%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-300">Countries Served</span>
                  <span className="font-bold text-orange-400">45+</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Team Section */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold mb-8 flex items-center">
            <Users className="h-8 w-8 text-green-400 mr-3" />
            Our Team
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-slate-800 rounded-xl p-6 text-center">
              <div className="w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mx-auto mb-4 flex items-center justify-center text-2xl font-bold">
                AB
              </div>
              <h3 className="text-xl font-semibold mb-2">Alex Bennett</h3>
              <p className="text-blue-400 mb-3">CEO & Founder</p>
              <p className="text-slate-300 text-sm">
                Former Goldman Sachs quant with 15+ years in algorithmic trading and risk management.
              </p>
            </div>
            <div className="bg-slate-800 rounded-xl p-6 text-center">
              <div className="w-20 h-20 bg-gradient-to-r from-green-500 to-blue-600 rounded-full mx-auto mb-4 flex items-center justify-center text-2xl font-bold">
                SR
              </div>
              <h3 className="text-xl font-semibold mb-2">Sarah Rodriguez</h3>
              <p className="text-green-400 mb-3">CTO</p>
              <p className="text-slate-300 text-sm">
                Ex-Google engineer specializing in high-frequency trading systems and machine learning.
              </p>
            </div>
            <div className="bg-slate-800 rounded-xl p-6 text-center">
              <div className="w-20 h-20 bg-gradient-to-r from-purple-500 to-pink-600 rounded-full mx-auto mb-4 flex items-center justify-center text-2xl font-bold">
                MK
              </div>
              <h3 className="text-xl font-semibold mb-2">Michael Kim</h3>
              <p className="text-purple-400 mb-3">Head of Research</p>
              <p className="text-slate-300 text-sm">
                PhD in Quantitative Finance from MIT, former JPMorgan researcher in systematic trading.
              </p>
            </div>
          </div>
        </section>

        {/* Values Section */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold mb-8 flex items-center">
            <Award className="h-8 w-8 text-purple-400 mr-3" />
            Our Values
          </h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-slate-800 rounded-xl p-6">
              <h3 className="text-xl font-semibold mb-4 text-blue-400">🚀 Innovation</h3>
              <p className="text-slate-300">
                We continuously push the boundaries of what's possible in algorithmic trading, 
                leveraging cutting-edge AI and machine learning technologies.
              </p>
            </div>
            <div className="bg-slate-800 rounded-xl p-6">
              <h3 className="text-xl font-semibold mb-4 text-green-400">🔒 Security</h3>
              <p className="text-slate-300">
                Bank-grade security protocols protect your data and funds. We employ military-grade 
                encryption and multi-factor authentication across all systems.
              </p>
            </div>
            <div className="bg-slate-800 rounded-xl p-6">
              <h3 className="text-xl font-semibold mb-4 text-purple-400">📊 Transparency</h3>
              <p className="text-slate-300">
                Complete transparency in our algorithms, fees, and performance metrics. 
                You always know exactly how your strategies are performing.
              </p>
            </div>
            <div className="bg-slate-800 rounded-xl p-6">
              <h3 className="text-xl font-semibold mb-4 text-orange-400">🎯 Excellence</h3>
              <p className="text-slate-300">
                We strive for excellence in everything we do, from our technology stack 
                to customer support and educational resources.
              </p>
            </div>
          </div>
        </section>

        {/* Global Presence */}
        <section>
          <h2 className="text-3xl font-bold mb-8 flex items-center">
            <Globe className="h-8 w-8 text-blue-400 mr-3" />
            Global Presence
          </h2>
          <div className="bg-slate-800 rounded-xl p-8">
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center">
                <h3 className="text-xl font-semibold mb-4 text-blue-400">🏢 Headquarters</h3>
                <p className="text-slate-300">
                  Mumbai, India<br />
                  Financial District<br />
                  Bandra Kurla Complex
                </p>
              </div>
              <div className="text-center">
                <h3 className="text-xl font-semibold mb-4 text-green-400">🌍 Regional Offices</h3>
                <p className="text-slate-300">
                  Singapore (APAC)<br />
                  London (Europe)<br />
                  New York (Americas)
                </p>
              </div>
              <div className="text-center">
                <h3 className="text-xl font-semibold mb-4 text-purple-400">📞 24/7 Support</h3>
                <p className="text-slate-300">
                  Round-the-clock support<br />
                  across all time zones<br />
                  in 15+ languages
                </p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}