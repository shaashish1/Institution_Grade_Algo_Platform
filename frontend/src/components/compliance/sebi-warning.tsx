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

    // Add escape key handler
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isVisible) {
        handleAccept();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isVisible]);

  const handleAccept = () => {
    localStorage.setItem('sebi-warning-accepted', 'true');
    setIsVisible(false);
    setHasAccepted(true);
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
    <div className="overlay-modal overlay-backdrop fixed inset-0 z-[9999] bg-black/90 backdrop-blur-md flex items-center justify-center p-4 pointer-events-auto modal-fade-in">
      <div className="modal-content bg-slate-900 border border-red-500 rounded-xl max-w-md w-full p-6 shadow-2xl relative" tabIndex={0}>
        {/* Close button */}
        <button
          onClick={handleAccept}
          className="modal-close absolute top-4 right-4 text-slate-400 hover:text-white transition-colors p-1 hover:bg-slate-800 rounded-full"
          aria-label="Close disclaimer"
        >
          <X className="h-5 w-5" />
        </button>
        
        <div className="flex items-start space-x-3 mb-4">
          <div className="flex-shrink-0">
            <div className="w-10 h-10 bg-red-500/20 rounded-lg flex items-center justify-center">
              <AlertTriangle className="h-5 w-5 text-red-400" />
            </div>
          </div>
          <div>
            <h2 className="text-xl font-bold text-white mb-1 drop-shadow-sm">
              Risk Disclosure
            </h2>
            <p className="text-slate-300 text-xs">
              Please acknowledge before proceeding
            </p>
          </div>
        </div>

        <div className="space-y-4 mb-6">
          <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
            <div className="space-y-2 text-slate-300 text-sm">
              <p className="text-white font-medium">
                • <strong className="text-red-400">9 out of 10</strong> individual traders in equity F&O incur losses
              </p>
              <p className="text-white font-medium">
                • <strong className="text-orange-400">Average loss:</strong> ₹50,000 per trader
              </p>
              <p className="text-white font-medium">
                • <strong className="text-yellow-400">Transaction costs:</strong> 15-50% of trading profits
              </p>
              <p className="text-white font-medium">
                • <strong className="text-purple-400">Market risk:</strong> Investment subject to market risks
              </p>
            </div>
          </div>

          <div className="bg-orange-900/30 border-2 border-orange-500 rounded-lg p-3">
            <div className="flex items-center space-x-2 text-orange-300 mb-2">
              <Shield className="h-5 w-5" />
              <span className="font-bold text-sm">SEBI Notice</span>
            </div>
            <p className="text-orange-100 text-sm font-medium">
              Please read all documents carefully before investing. 
              <a href="https://www.sebi.gov.in/" target="_blank" rel="noopener noreferrer" className="underline ml-1 text-orange-200 hover:text-white">
                Learn more at SEBI.gov.in
              </a>
            </p>
          </div>
        </div>

        <div className="flex justify-center">
          <button
            onClick={handleAccept}
            className="modal-button w-full px-6 py-4 bg-gradient-to-r from-blue-600 to-purple-700 hover:from-blue-700 hover:to-purple-800 text-white rounded-lg transition-all duration-200 flex items-center justify-center space-x-2 text-base font-bold shadow-lg hover:shadow-xl transform hover:scale-[1.02]"
          >
            <Shield className="h-5 w-5" />
            <span>I Understand & Acknowledge</span>
          </button>
        </div>

        <div className="mt-4 pt-4 border-t border-slate-700">
          <div className="flex items-center justify-center space-x-4 text-sm text-slate-400">
            <a href="#" className="hover:text-white transition-colors font-medium">Terms</a>
            <a href="#" className="hover:text-white transition-colors font-medium">Privacy</a>
            <a href="https://www.sebi.gov.in/" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors font-medium">
              SEBI
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}