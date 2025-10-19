'use client';

import React from 'react';
import { 
  TrendingUp, 
  Mail, 
  Phone, 
  MapPin, 
  Facebook, 
  Twitter, 
  Linkedin, 
  Instagram,
  Youtube,
  Shield,
  FileText,
  HelpCircle,
  BookOpen,
  Users,
  Zap,
  BarChart3,
  Wallet,
  Brain,
  Globe,
  ArrowRight
} from 'lucide-react';

const footerSections = [
  {
    title: 'Platform',
    links: [
      { name: 'Live Trading', href: '/trading', icon: TrendingUp },
      { name: 'Portfolio', href: '/portfolio', icon: Wallet },
      { name: 'Strategies', href: '/strategies', icon: Brain },
      { name: 'Analytics', href: '/analytics', icon: BarChart3 },
      { name: 'API Access', href: '/api', icon: Zap },
    ]
  },
  {
    title: 'Resources',
    links: [
      { name: 'Documentation', href: '/docs', icon: BookOpen },
      { name: 'Video Tutorials', href: '/tutorials', icon: Youtube },
      { name: 'Community Forum', href: '/community', icon: Users },
      { name: 'Blog', href: '/blog', icon: FileText },
      { name: 'Market News', href: '/news', icon: Globe },
    ]
  },
  {
    title: 'Support',
    links: [
      { name: 'Help Center', href: '/help', icon: HelpCircle },
      { name: 'Contact Us', href: '/contact', icon: Phone },
      { name: 'Live Chat', href: '/chat', icon: Mail },
      { name: 'System Status', href: '/status', icon: Shield },
      { name: 'Report Issue', href: '/report', icon: FileText },
    ]
  },
  {
    title: 'Legal',
    links: [
      { name: 'Terms of Service', href: '/terms', icon: FileText },
      { name: 'Privacy Policy', href: '/privacy', icon: Shield },
      { name: 'Risk Disclosure', href: '/risk', icon: Shield },
      { name: 'SEBI Compliance', href: '/compliance', icon: Shield },
      { name: 'Cookie Policy', href: '/cookies', icon: FileText },
    ]
  }
];

const socialLinks = [
  { name: 'Facebook', icon: Facebook, href: '#', color: 'hover:text-blue-400' },
  { name: 'Twitter', icon: Twitter, href: '#', color: 'hover:text-sky-400' },
  { name: 'LinkedIn', icon: Linkedin, href: '#', color: 'hover:text-blue-600' },
  { name: 'Instagram', icon: Instagram, href: '#', color: 'hover:text-pink-400' },
  { name: 'YouTube', icon: Youtube, href: '#', color: 'hover:text-red-500' },
];

export function Footer() {
  return (
    <footer className="bg-slate-900 border-t border-slate-800">
      {/* Main Footer */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-8">
          {/* Brand Section */}
          <div className="lg:col-span-2">
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <TrendingUp className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-white">AlgoProject</h3>
                <p className="text-sm text-slate-400">Institution Grade</p>
              </div>
            </div>
            
            <p className="text-slate-300 mb-6 leading-relaxed">
              Professional algorithmic trading platform with advanced analytics, 
              real-time market data, and institutional-grade risk management tools.
            </p>

            {/* Contact Info */}
            <div className="space-y-3 mb-6">
              <div className="flex items-center space-x-3 text-slate-300">
                <Mail className="h-4 w-4 text-blue-400" />
                <span className="text-sm">support@algoproject.com</span>
              </div>
              <div className="flex items-center space-x-3 text-slate-300">
                <Phone className="h-4 w-4 text-blue-400" />
                <span className="text-sm">+91 12345 67890</span>
              </div>
              <div className="flex items-center space-x-3 text-slate-300">
                <MapPin className="h-4 w-4 text-blue-400" />
                <span className="text-sm">Mumbai, India</span>
              </div>
            </div>

            {/* Social Links */}
            <div className="flex space-x-4">
              {socialLinks.map((social) => {
                const Icon = social.icon;
                return (
                  <a
                    key={social.name}
                    href={social.href}
                    className={`w-10 h-10 bg-slate-800 hover:bg-slate-700 rounded-lg flex items-center justify-center transition-colors ${social.color}`}
                    aria-label={social.name}
                  >
                    <Icon className="h-5 w-5" />
                  </a>
                );
              })}
            </div>
          </div>

          {/* Footer Sections */}
          {footerSections.map((section) => (
            <div key={section.title}>
              <h4 className="text-white font-semibold mb-4">{section.title}</h4>
              <ul className="space-y-3">
                {section.links.map((link) => {
                  const Icon = link.icon;
                  return (
                    <li key={link.name}>
                      <a
                        href={link.href}
                        className="flex items-center space-x-2 text-slate-400 hover:text-white transition-colors group"
                      >
                        <Icon className="h-4 w-4 group-hover:text-blue-400 transition-colors" />
                        <span className="text-sm">{link.name}</span>
                      </a>
                    </li>
                  );
                })}
              </ul>
            </div>
          ))}
        </div>

        {/* Newsletter Signup */}
        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="bg-slate-800/50 rounded-2xl p-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
              <div>
                <h3 className="text-2xl font-bold text-white mb-2">
                  Stay Updated
                </h3>
                <p className="text-slate-300">
                  Get the latest market insights, trading tips, and platform updates delivered to your inbox.
                </p>
              </div>
              <div className="flex flex-col sm:flex-row gap-4">
                <div className="flex-1">
                  <input
                    type="email"
                    placeholder="Enter your email"
                    className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 transition-colors"
                  />
                </div>
                <button className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-6 py-3 rounded-lg font-semibold transition-all duration-300 flex items-center space-x-2 group">
                  <span>Subscribe</span>
                  <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-slate-800 bg-slate-950">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="flex items-center space-x-6 text-sm text-slate-400">
              <span>© 2024 AlgoProject. All rights reserved.</span>
              <span className="hidden md:block">•</span>
              <span className="flex items-center space-x-1">
                <Shield className="h-4 w-4 text-green-400" />
                <span>SEBI Compliant</span>
              </span>
            </div>
            
            <div className="flex items-center space-x-6 text-sm">
              <div className="flex items-center space-x-2 text-slate-400">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span>All systems operational</span>
              </div>
              <a href="/status" className="text-slate-400 hover:text-white transition-colors">
                System Status
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* SEBI Warning Strip */}
      <div className="bg-gradient-to-r from-orange-600 to-red-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
          <div className="flex items-center justify-center space-x-2 text-sm">
            <Shield className="h-4 w-4" />
            <span>
              <strong>SEBI Risk Disclosure:</strong> Investment in securities market are subject to market risks. 
              Please read all the related documents carefully before investing. 
              AlgoProject is not responsible for your trading decisions.
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}