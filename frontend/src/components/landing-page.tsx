'use client';

import React, { useState, useEffect } from 'react';
import { Header } from './layout/new-header';
import { HeroSection } from './sections/hero-section';
import { FeaturesSection } from './sections/features-section';
import { TradingPreview } from './sections/trading-preview';
import { PricingSection } from './sections/pricing-section';
import { Footer } from './layout/footer';
import { SEBIWarning } from './compliance/sebi-warning';

export function LandingPage() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900">
      <SEBIWarning />
      <Header />
      <main>
        <HeroSection />
        <FeaturesSection />
        <TradingPreview />
        <PricingSection />
      </main>
      <Footer />
    </div>
  );
}