'use client';

import React, { useState } from 'react';
import { CheckCircle, XCircle, AlertCircle, ExternalLink, Eye, Smartphone, Palette, MessageSquare, Zap, Shield, TrendingUp } from 'lucide-react';

interface ChecklistItem {
  id: string;
  category: string;
  title: string;
  description: string;
  status: 'completed' | 'pending' | 'needs-attention';
  priority: 'high' | 'medium' | 'low';
}

export function LaunchChecklist() {
  const [checklist, setChecklist] = useState<ChecklistItem[]>([
    // Experience & Clarity
    {
      id: 'hero-copy',
      category: 'Experience & Clarity',
      title: 'Hero copy explains platform purpose',
      description: 'Platform purpose clear in one glance',
      status: 'completed',
      priority: 'high'
    },
    {
      id: 'primary-cta',
      category: 'Experience & Clarity', 
      title: 'Primary CTA visible above fold',
      description: '"Start Trading" or similar visible immediately',
      status: 'completed',
      priority: 'high'
    },
    {
      id: 'algobot-meaning',
      category: 'Experience & Clarity',
      title: 'AlgoBot adds meaning, not distraction',
      description: 'Animation pauses gracefully and provides value',
      status: 'completed',
      priority: 'medium'
    },
    {
      id: 'navigation-clarity',
      category: 'Experience & Clarity',
      title: 'Navigation labels clear and consistent',
      description: 'Short, clear labels across all pages',
      status: 'pending',
      priority: 'medium'
    },

    // Performance & Responsiveness
    {
      id: 'optimized-assets',
      category: 'Performance & Responsiveness',
      title: 'Doodle assets optimized',
      description: 'All doodles exported as optimized SVG or Lottie',
      status: 'completed',
      priority: 'high'
    },
    {
      id: 'page-load-speed',
      category: 'Performance & Responsiveness',
      title: 'Page load under 2.5s on 4G',
      description: 'Performance optimization for mobile networks',
      status: 'needs-attention',
      priority: 'high'
    },
    {
      id: 'animation-degradation',
      category: 'Performance & Responsiveness',
      title: 'Animations degrade gracefully',
      description: 'Smooth experience on lower-end devices',
      status: 'completed',
      priority: 'medium'
    },
    {
      id: 'mobile-testing',
      category: 'Performance & Responsiveness',
      title: 'Mobile layout tested on 3+ screen sizes',
      description: 'Responsive design verification',
      status: 'pending',
      priority: 'high'
    },

    // Visual & Brand Consistency
    {
      id: 'color-palette',
      category: 'Visual & Brand Consistency',
      title: 'Color palette matches brand guide',
      description: 'Accent colors used sparingly and consistently',
      status: 'completed',
      priority: 'high'
    },
    {
      id: 'font-rendering',
      category: 'Visual & Brand Consistency',
      title: 'Comic Neue and Poppins render correctly',
      description: 'Cross-browser font compatibility',
      status: 'completed',
      priority: 'medium'
    },
    {
      id: 'stroke-consistency',
      category: 'Visual & Brand Consistency',
      title: 'Line thickness consistent in doodles',
      description: 'Uniform stroke weight across all illustrations',
      status: 'completed',
      priority: 'medium'
    },
    {
      id: 'text-contrast',
      category: 'Visual & Brand Consistency',
      title: 'Background textures don\'t clash with text',
      description: 'AAA readability compliance',
      status: 'completed',
      priority: 'high'
    },

    // Tone & Microcopy
    {
      id: 'witty-balance',
      category: 'Tone & Microcopy',
      title: 'Witty text balanced with professionalism',
      description: 'Avoid sarcasm in trading context',
      status: 'completed',
      priority: 'medium'
    },
    {
      id: 'algobot-voice',
      category: 'Tone & Microcopy',
      title: 'AlgoBot messages align with brand voice',
      description: 'Friendly, not chatty messaging',
      status: 'completed',
      priority: 'medium'
    },
    {
      id: 'trust-statements',
      category: 'Tone & Microcopy',
      title: 'Trust statements present and legible',
      description: 'Regulatory info and data security visible',
      status: 'completed',
      priority: 'high'
    },

    // Functionality & Flow
    {
      id: 'cta-functionality',
      category: 'Functionality & Flow',
      title: 'All CTAs lead to correct destinations',
      description: 'Proper page routing and modal behavior',
      status: 'completed',
      priority: 'high'
    },
    {
      id: 'pricing-cards',
      category: 'Functionality & Flow',
      title: 'Pricing cards show correct info',
      description: 'State changes on hover/click work properly',
      status: 'pending',
      priority: 'medium'
    },
    {
      id: 'community-interactions',
      category: 'Functionality & Flow',
      title: 'Community section doesn\'t obstruct UI',
      description: 'No interference with scrolling or text',
      status: 'pending',
      priority: 'medium'
    },
    {
      id: 'footer-links',
      category: 'Functionality & Flow',
      title: 'Footer links functional',
      description: 'Correct tab behavior and destinations',
      status: 'pending',
      priority: 'low'
    },

    // Trust & Conversion
    {
      id: 'security-badges',
      category: 'Trust & Conversion',
      title: 'Security badges and logos visible',
      description: 'API partner logos and testimonials before pricing',
      status: 'needs-attention',
      priority: 'high'
    },
    {
      id: 'demo-signup',
      category: 'Trust & Conversion',
      title: 'Demo/signup flow minimal steps',
      description: 'Streamlined conversion process',
      status: 'pending',
      priority: 'high'
    },
    {
      id: 'onboarding-tone',
      category: 'Trust & Conversion',
      title: 'Onboarding uses consistent playful tone',
      description: 'Brand voice maintained throughout user journey',
      status: 'pending',
      priority: 'medium'
    }
  ]);

  const toggleStatus = (id: string) => {
    setChecklist(prev => prev.map(item => 
      item.id === id 
        ? { 
            ...item, 
            status: item.status === 'completed' 
              ? 'pending' 
              : item.status === 'pending' 
                ? 'needs-attention' 
                : 'completed' 
          }
        : item
    ));
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'needs-attention':
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      default:
        return <XCircle className="h-5 w-5 text-slate-400" />;
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'Experience & Clarity':
        return <Eye className="h-5 w-5" />;
      case 'Performance & Responsiveness':
        return <Zap className="h-5 w-5" />;
      case 'Visual & Brand Consistency':
        return <Palette className="h-5 w-5" />;
      case 'Tone & Microcopy':
        return <MessageSquare className="h-5 w-5" />;
      case 'Functionality & Flow':
        return <TrendingUp className="h-5 w-5" />;
      case 'Trust & Conversion':
        return <Shield className="h-5 w-5" />;
      default:
        return <CheckCircle className="h-5 w-5" />;
    }
  };

  const categories = Array.from(new Set(checklist.map(item => item.category)));
  const getStatusCounts = () => {
    const completed = checklist.filter(item => item.status === 'completed').length;
    const total = checklist.length;
    const needsAttention = checklist.filter(item => item.status === 'needs-attention').length;
    return { completed, total, needsAttention };
  };

  const { completed, total, needsAttention } = getStatusCounts();
  const completionPercentage = Math.round((completed / total) * 100);

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-xl shadow-xl border border-slate-200 overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-mint-green to-coral-pink p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold" style={{ fontFamily: 'Comic Neue, cursive' }}>
                🚀 Playful Fintech Launch Checklist
              </h1>
              <p className="text-white/90 mt-1">Quality assurance for your trading platform</p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold">{completionPercentage}%</div>
              <div className="text-sm text-white/80">{completed}/{total} completed</div>
              {needsAttention > 0 && (
                <div className="text-sm text-yellow-200 mt-1">
                  ⚠️ {needsAttention} need attention
                </div>
              )}
            </div>
          </div>
          
          {/* Progress Bar */}
          <div className="mt-4 bg-white/20 rounded-full h-3">
            <div 
              className="bg-white rounded-full h-3 transition-all duration-500"
              style={{ width: `${completionPercentage}%` }}
            />
          </div>
        </div>

        {/* Checklist Categories */}
        <div className="p-6 space-y-6">
          {categories.map(category => {
            const categoryItems = checklist.filter(item => item.category === category);
            const categoryCompleted = categoryItems.filter(item => item.status === 'completed').length;
            
            return (
              <div key={category} className="border border-slate-200 rounded-lg overflow-hidden">
                <div className="bg-slate-50 px-4 py-3 border-b border-slate-200">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="text-slate-600">
                        {getCategoryIcon(category)}
                      </div>
                      <h3 className="font-bold text-slate-800">{category}</h3>
                    </div>
                    <div className="text-sm text-slate-600">
                      {categoryCompleted}/{categoryItems.length}
                    </div>
                  </div>
                </div>
                
                <div className="divide-y divide-slate-100">
                  {categoryItems.map(item => (
                    <div 
                      key={item.id} 
                      className="px-4 py-3 hover:bg-slate-50 transition-colors cursor-pointer"
                      onClick={() => toggleStatus(item.id)}
                    >
                      <div className="flex items-start space-x-3">
                        <button className="mt-0.5">
                          {getStatusIcon(item.status)}
                        </button>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between">
                            <h4 className="font-medium text-slate-800">{item.title}</h4>
                            <span className={`text-xs px-2 py-1 rounded-full ${
                              item.priority === 'high' 
                                ? 'bg-red-100 text-red-700' 
                                : item.priority === 'medium'
                                  ? 'bg-yellow-100 text-yellow-700'
                                  : 'bg-blue-100 text-blue-700'
                            }`}>
                              {item.priority}
                            </span>
                          </div>
                          <p className="text-sm text-slate-600 mt-1">{item.description}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        {/* Footer */}
        <div className="bg-slate-50 px-6 py-4 border-t border-slate-200">
          <div className="flex items-center justify-between text-sm text-slate-600">
            <p>Click items to toggle status: Pending → Needs Attention → Completed</p>
            <a 
              href="https://www.sebi.gov.in/" 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center space-x-1 text-blue-600 hover:text-blue-800"
            >
              <span>SEBI Guidelines</span>
              <ExternalLink className="h-4 w-4" />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}