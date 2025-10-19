'use client';

import React, { useState } from 'react';
import { Chrome, Shield, CheckCircle } from 'lucide-react';

interface GoogleAuthProps {
  onAuthComplete?: (user: any) => void;
}

export function GoogleAuth({ onAuthComplete }: GoogleAuthProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [showTerms, setShowTerms] = useState(false);
  const [termsAccepted, setTermsAccepted] = useState(false);
  const [riskDisclosureAccepted, setRiskDisclosureAccepted] = useState(false);

  const handleGoogleSignIn = async () => {
    if (!termsAccepted || !riskDisclosureAccepted) {
      setShowTerms(true);
      return;
    }

    setIsLoading(true);
    
    try {
      // Simulate Google OAuth flow
      // In production, integrate with Google OAuth 2.0
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const mockUser = {
        id: '1',
        name: 'Trading User',
        email: 'user@example.com',
        picture: 'https://via.placeholder.com/40'
      };
      
      localStorage.setItem('user', JSON.stringify(mockUser));
      localStorage.setItem('auth-token', 'mock-jwt-token');
      
      if (onAuthComplete) {
        onAuthComplete(mockUser);
      }
    } catch (error) {
      console.error('Authentication failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTermsAcceptance = () => {
    if (termsAccepted && riskDisclosureAccepted) {
      setShowTerms(false);
      handleGoogleSignIn();
    }
  };

  if (showTerms) {
    return (
      <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
        <div className="bg-slate-900 border border-blue-500 rounded-xl max-w-2xl w-full p-8 shadow-2xl">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
            <Shield className="h-6 w-6 text-blue-400 mr-2" />
            Terms & Risk Acknowledgment
          </h2>

          <div className="space-y-6 mb-8">
            <div className="bg-slate-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Terms of Service</h3>
              <div className="space-y-3 text-slate-300 text-sm max-h-40 overflow-y-auto">
                <p>• You must be 18+ years old to use this platform</p>
                <p>• Platform owners are not responsible for trading losses</p>
                <p>• All trading decisions are your own responsibility</p>
                <p>• You agree to comply with all applicable laws and regulations</p>
                <p>• Platform may be discontinued or modified at any time</p>
                <p>• Your account may be suspended for violations</p>
              </div>
              <label className="flex items-center mt-4 cursor-pointer">
                <input
                  type="checkbox"
                  checked={termsAccepted}
                  onChange={(e) => setTermsAccepted(e.target.checked)}
                  className="sr-only"
                />
                <div className={`w-5 h-5 rounded border-2 mr-3 flex items-center justify-center ${
                  termsAccepted ? 'bg-blue-500 border-blue-500' : 'border-slate-400'
                }`}>
                  {termsAccepted && <CheckCircle className="h-3 w-3 text-white" />}
                </div>
                <span className="text-sm text-slate-300">I accept the Terms of Service</span>
              </label>
            </div>

            <div className="bg-slate-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Risk Disclosure</h3>
              <div className="space-y-3 text-slate-300 text-sm max-h-40 overflow-y-auto">
                <p>• Trading involves substantial risk of loss</p>
                <p>• Past performance does not guarantee future results</p>
                <p>• You may lose more than your initial investment</p>
                <p>• Market conditions can change rapidly</p>
                <p>• Algorithmic trading carries additional technical risks</p>
                <p>• No investment advice is provided by this platform</p>
              </div>
              <label className="flex items-center mt-4 cursor-pointer">
                <input
                  type="checkbox"
                  checked={riskDisclosureAccepted}
                  onChange={(e) => setRiskDisclosureAccepted(e.target.checked)}
                  className="sr-only"
                />
                <div className={`w-5 h-5 rounded border-2 mr-3 flex items-center justify-center ${
                  riskDisclosureAccepted ? 'bg-red-500 border-red-500' : 'border-slate-400'
                }`}>
                  {riskDisclosureAccepted && <CheckCircle className="h-3 w-3 text-white" />}
                </div>
                <span className="text-sm text-slate-300">I understand and accept the risks</span>
              </label>
            </div>
          </div>

          <div className="flex gap-4">
            <button
              onClick={() => setShowTerms(false)}
              className="flex-1 px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={handleTermsAcceptance}
              disabled={!termsAccepted || !riskDisclosureAccepted}
              className="flex-1 px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg transition-all"
            >
              Continue with Google
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <button
        onClick={handleGoogleSignIn}
        disabled={isLoading}
        className="w-full flex items-center justify-center px-6 py-3 bg-white hover:bg-gray-50 text-gray-900 rounded-lg border border-gray-300 transition-colors disabled:opacity-50"
      >
        {isLoading ? (
          <div className="w-5 h-5 border-2 border-gray-300 border-t-gray-900 rounded-full animate-spin mr-3" />
        ) : (
          <Chrome className="h-5 w-5 mr-3" />
        )}
        {isLoading ? 'Signing in...' : 'Continue with Google'}
      </button>
      
      <p className="text-xs text-slate-400 text-center">
        By signing in, you agree to our Terms of Service and Risk Disclosure
      </p>
    </div>
  );
}