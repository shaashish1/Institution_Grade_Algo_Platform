'use client';

import React from 'react';
import { Check, Star, Zap, Crown } from 'lucide-react';

const plans = [
  {
    name: 'Starter',
    price: 'Free',
    period: '',
    description: 'Perfect for beginners to get started',
    icon: Star,
    gradient: 'from-gray-500 to-gray-600',
    features: [
      'Paper trading',
      'Basic market data',
      'Simple strategies',
      '5 active positions',
      'Email support',
      'Basic analytics'
    ],
    limitations: [
      'No live trading',
      'Limited to 3 exchanges'
    ]
  },
  {
    name: 'Professional',
    price: '₹2,999',
    period: '/month',
    description: 'Advanced tools for serious traders',
    icon: Zap,
    gradient: 'from-blue-500 to-purple-600',
    popular: true,
    features: [
      'Live trading',
      'Real-time market data',
      'Advanced strategies',
      'Unlimited positions',
      'Priority support',
      'Advanced analytics',
      'Risk management tools',
      'Multi-exchange support',
      'Custom indicators',
      'API access'
    ],
    limitations: []
  },
  {
    name: 'Institution',
    price: 'Custom',
    period: '',
    description: 'Enterprise-grade solutions',
    icon: Crown,
    gradient: 'from-yellow-500 to-orange-600',
    features: [
      'Everything in Professional',
      'Dedicated support',
      'Custom integrations',
      'White-label solutions',
      'Advanced reporting',
      'Compliance tools',
      'Multi-user management',
      'SLA guarantees'
    ],
    limitations: []
  }
];

export function PricingSection() {
  return (
    <section className="py-24 relative">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-slate-900 to-slate-800"></div>
      
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-20">
          <div className="inline-flex items-center space-x-2 bg-green-500/10 border border-green-500/20 rounded-full px-6 py-2 text-green-400 mb-6">
            <Star className="h-4 w-4" />
            <span className="text-sm font-medium">Pricing Plans</span>
          </div>
          
          <h2 className="text-4xl md:text-6xl font-bold text-white mb-6">
            Choose Your
            <span className="block bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent">
              Trading Plan
            </span>
          </h2>
          
          <p className="text-xl text-slate-300 max-w-3xl mx-auto">
            Start free and upgrade as you grow. All plans include our core features 
            with advanced tools available for professional and institutional traders.
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {plans.map((plan, index) => {
            const Icon = plan.icon;
            return (
              <div
                key={plan.name}
                className={`relative bg-slate-800/50 backdrop-blur-sm border rounded-2xl p-8 transition-all duration-500 hover:transform hover:scale-105 ${
                  plan.popular 
                    ? 'border-blue-500 shadow-2xl shadow-blue-500/20' 
                    : 'border-slate-700 hover:border-slate-600'
                }`}
              >
                {/* Popular Badge */}
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-2 rounded-full text-sm font-semibold">
                      Most Popular
                    </div>
                  </div>
                )}

                {/* Plan Header */}
                <div className="text-center mb-8">
                  <div className={`w-16 h-16 mx-auto mb-4 rounded-xl bg-gradient-to-r ${plan.gradient} flex items-center justify-center`}>
                    <Icon className="h-8 w-8 text-white" />
                  </div>
                  
                  <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
                  <p className="text-slate-400 text-sm mb-4">{plan.description}</p>
                  
                  <div className="flex items-baseline justify-center">
                    <span className="text-4xl font-bold text-white">{plan.price}</span>
                    {plan.period && (
                      <span className="text-slate-400 ml-1">{plan.period}</span>
                    )}
                  </div>
                </div>

                {/* Features */}
                <div className="space-y-4 mb-8">
                  {plan.features.map((feature, idx) => (
                    <div key={idx} className="flex items-center space-x-3">
                      <div className="flex-shrink-0 w-5 h-5 bg-green-500 rounded-full flex items-center justify-center">
                        <Check className="h-3 w-3 text-white" />
                      </div>
                      <span className="text-slate-300">{feature}</span>
                    </div>
                  ))}
                  
                  {plan.limitations.map((limitation, idx) => (
                    <div key={idx} className="flex items-center space-x-3">
                      <div className="flex-shrink-0 w-5 h-5 bg-slate-600 rounded-full flex items-center justify-center">
                        <span className="text-slate-400 text-xs">×</span>
                      </div>
                      <span className="text-slate-500">{limitation}</span>
                    </div>
                  ))}
                </div>

                {/* CTA Button */}
                <button className={`w-full py-4 rounded-lg font-semibold transition-all duration-300 ${
                  plan.popular
                    ? 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white transform hover:scale-105 shadow-lg hover:shadow-xl'
                    : 'bg-slate-700 hover:bg-slate-600 text-white'
                }`}>
                  {plan.name === 'Institution' ? 'Contact Sales' : plan.name === 'Starter' ? 'Get Started Free' : 'Start Free Trial'}
                </button>

                {/* Additional Info */}
                {plan.name === 'Professional' && (
                  <p className="text-center text-slate-400 text-sm mt-4">
                    ✨ 14-day free trial • Cancel anytime
                  </p>
                )}
              </div>
            );
          })}
        </div>

        {/* Additional Information */}
        <div className="mt-20 text-center">
          <div className="bg-slate-800/30 backdrop-blur-sm border border-slate-700 rounded-2xl p-8">
            <h3 className="text-2xl font-bold text-white mb-4">
              Need Something Different?
            </h3>
            <p className="text-slate-300 mb-6 max-w-2xl mx-auto">
              We offer custom solutions for institutional clients, including dedicated infrastructure, 
              compliance tools, and specialized support.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-8 py-3 rounded-lg font-semibold transition-all duration-300">
                Contact Sales
              </button>
              <button className="bg-slate-700 hover:bg-slate-600 text-white px-8 py-3 rounded-lg font-semibold transition-colors">
                Schedule Demo
              </button>
            </div>
          </div>
        </div>

        {/* Trust Indicators */}
        <div className="mt-16 text-center">
          <p className="text-slate-400 mb-8">Trusted by 50,000+ traders worldwide</p>
          <div className="flex justify-center items-center space-x-8 opacity-60">
            <div className="text-slate-500">🔒 Bank-grade security</div>
            <div className="text-slate-500">📊 SEBI compliant</div>
            <div className="text-slate-500">⚡ 99.9% uptime</div>
            <div className="text-slate-500">🛡️ Insured funds</div>
          </div>
        </div>
      </div>
    </section>
  );
}