'use client';

import React, { useState, useEffect } from 'react';
import { AlertTriangle, X, Shield, FileText, ExternalLink } from 'lucide-react';

export function SEBIWarning() {
  const [isVisible, setIsVisible] = useState(false);
  const [hasAccepted, setHasAccepted] = useState(false);

  useEffect(() => {
    // Check if user has already seen the warning
    const accepted = localStorage.getItem('sebi-warning-accepted');
    if (!accepted) {
      setIsVisible(true);
    } else {
      setHasAccepted(true);
    }
  }, []);

  const handleAccept = () => {
    localStorage.setItem('sebi-warning-accepted', 'true');
    setIsVisible(false);
    setHasAccepted(true);
  };

  const handleReject = () => {
    // Keep user on website but show limited access message
    setIsVisible(false);
    // Don't save acceptance, so warning will show again on refresh
  };

  if (!isVisible && hasAccepted) {
    return (
      <div className="bg-gradient-to-r from-orange-600 to-red-600 text-white px-4 py-2 text-center text-sm">
        <div className="flex items-center justify-center space-x-2">
          <Shield className="h-4 w-4" />
          <span>
            <strong>SEBI Regulatory Notice:</strong> Investment in securities market are subject to market risks. 
            Please read all the related documents carefully before investing.
          </span>
        </div>
      </div>
    );
  }

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 z-[100] bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-red-500 rounded-xl max-w-2xl w-full p-8 shadow-2xl">
        <div className="flex items-start space-x-4 mb-6">
          <div className="flex-shrink-0">
            <div className="w-12 h-12 bg-red-500/20 rounded-lg flex items-center justify-center">
              <AlertTriangle className="h-6 w-6 text-red-400" />
            </div>
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white mb-2">
              SEBI Regulatory Compliance & Risk Disclosure
            </h2>
            <p className="text-slate-300 text-sm">
              Please read and acknowledge the following important disclosures before proceeding
            </p>
          </div>
        </div>

        <div className="space-y-6 mb-8">
          <div className="bg-slate-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-3 flex items-center">
              <Shield className="h-5 w-5 text-blue-400 mr-2" />
              Risk Disclosure Statement
            </h3>
            <div className="space-y-3 text-slate-300 text-sm">
              <p>
                <strong className="text-white">Market Risk:</strong> Trading in stocks, derivatives and commodities involves substantial risk of loss and is not suitable for all investors.
              </p>
              <p>
                <strong className="text-white">Platform Disclaimer:</strong> AlgoProject is a technology platform. We do not provide investment advice and are not responsible for your trading decisions.
              </p>
              <p>
                <strong className="text-white">Regulatory Compliance:</strong> All trading activities must comply with SEBI guidelines and applicable regulations.
              </p>
              <p>
                <strong className="text-white">Capital Risk:</strong> Never invest money you cannot afford to lose. Past performance is not indicative of future results.
              </p>
            </div>
          </div>

          <div className="bg-slate-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-3 flex items-center">
              <FileText className="h-5 w-5 text-green-400 mr-2" />
              Terms & Conditions
            </h3>
            <ul className="space-y-2 text-slate-300 text-sm">
              <li className="flex items-start">
                <span className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                You acknowledge that algorithmic trading involves significant risk
              </li>
              <li className="flex items-start">
                <span className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                Platform owners are not liable for trading losses or system failures
              </li>
              <li className="flex items-start">
                <span className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                You are responsible for tax compliance and regulatory adherence
              </li>
              <li className="flex items-start">
                <span className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                Minimum age requirement: 18 years for trading
              </li>
            </ul>
          </div>

          <div className="bg-orange-900/20 border border-orange-500 rounded-lg p-4">
            <div className="flex items-center space-x-2 text-orange-400 mb-2">
              <AlertTriangle className="h-5 w-5" />
              <span className="font-semibold">Important Notice</span>
            </div>
            <p className="text-orange-200 text-sm">
              This platform is for educational and research purposes. Always consult with a qualified financial advisor before making investment decisions.
            </p>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-4">
          <button
            onClick={handleReject}
            className="flex-1 px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors flex items-center justify-center space-x-2"
          >
            <X className="h-4 w-4" />
            <span>I Do Not Agree</span>
          </button>
          <button
            onClick={handleAccept}
            className="flex-1 px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white rounded-lg transition-all duration-200 flex items-center justify-center space-x-2"
          >
            <Shield className="h-4 w-4" />
            <span>I Understand & Agree</span>
          </button>
        </div>

        <div className="mt-6 pt-6 border-t border-slate-700">
          <div className="flex items-center justify-center space-x-6 text-xs text-slate-400">
            <a href="#" className="hover:text-white transition-colors flex items-center space-x-1">
              <FileText className="h-3 w-3" />
              <span>Terms of Service</span>
            </a>
            <a href="#" className="hover:text-white transition-colors flex items-center space-x-1">
              <Shield className="h-3 w-3" />
              <span>Privacy Policy</span>
            </a>
            <a href="https://www.sebi.gov.in/" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors flex items-center space-x-1">
              <ExternalLink className="h-3 w-3" />
              <span>SEBI Website</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}