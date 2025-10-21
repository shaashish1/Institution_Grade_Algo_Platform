# Figma to React Implementation Guide

## 🚀 Quick Start

This guide maps the Figma design to React/Next.js components. Use this after finalizing your Figma design.

---

## 📁 React Component Structure

```
frontend/src/components/
├── layout/
│   ├── navbar.tsx
│   ├── footer.tsx
│   └── header.tsx
├── sections/
│   ├── hero-section.tsx
│   ├── trust-section.tsx
│   ├── features-section.tsx
│   ├── demo-section.tsx
│   ├── testimonials-section.tsx
│   └── pricing-section.tsx
├── cards/
│   ├── feature-card.tsx
│   ├── pricing-card.tsx
│   ├── testimonial-card.tsx
│   └── trust-card.tsx
├── buttons/
│   ├── button-primary.tsx
│   ├── button-secondary.tsx
│   └── button-group.tsx
├── ui/
│   ├── badge.tsx
│   ├── icon-wrapper.tsx
│   ├── gradient-background.tsx
│   └── section-divider.tsx
└── animations/
    ├── fade-in.tsx
    ├── slide-up.tsx
    ├── scale-in.tsx
    └── scroll-trigger.tsx
```

---

## 🎨 Design Tokens in React

### Create `src/tokens/design-system.ts`

```typescript
// Colors
export const colors = {
  navy: {
    main: '#0C1B2A',
    hover: '#142038',
    active: '#1A2842',
  },
  teal: {
    main: '#00C7B7',
    hover: '#00A89F',
    active: '#008E82',
  },
  offWhite: '#F8FAFC',
  silver: '#D1D5DB',
  emerald: '#10B981',
  gold: '#FACC15',
  darkText: '#1F2937',
  lightText: '#F3F4F6',
};

// Typography
export const typography = {
  fontFamilies: {
    heading: "'Satoshi', 'Poppins', sans-serif",
    body: "'Inter', 'DM Sans', sans-serif",
  },
  sizes: {
    h1: { desktop: '56px', mobile: '32px' },
    h2: { desktop: '40px', mobile: '28px' },
    h3: { desktop: '24px', mobile: '20px' },
    h4: { desktop: '18px', mobile: '16px' },
    bodyLarge: '16px',
    body: '14px',
    label: '12px',
  },
  weights: {
    bold: 700,
    semibold: 600,
    regular: 400,
  },
  lineHeights: {
    heading: 1.2,
    subheading: 1.3,
    body: 1.5,
    tight: 1.2,
  },
};

// Spacing (8px base)
export const spacing = {
  xs: '4px',
  sm: '8px',
  md: '16px',
  lg: '24px',
  xl: '32px',
  '2xl': '48px',
  '3xl': '64px',
  '4xl': '96px',
};

// Shadows
export const shadows = {
  subtle: '0 1px 3px rgba(12, 27, 42, 0.08)',
  medium: '0 4px 12px rgba(12, 27, 42, 0.12)',
  glow: '0 0 20px rgba(0, 199, 183, 0.3)',
};

// Border Radius
export const borderRadius = {
  sm: '4px',
  md: '8px',
  lg: '12px',
  xl: '16px',
  full: '9999px',
};

// Breakpoints
export const breakpoints = {
  mobile: '375px',
  tablet: '768px',
  desktop: '1440px',
};

// Gradients
export const gradients = {
  hero: 'linear-gradient(135deg, #0C1B2A 0%, #1A3A52 100%)',
  accent: 'linear-gradient(90deg, #00C7B7 0%, #10B981 100%)',
  gold: 'linear-gradient(90deg, #FACC15 0%, #F59E0B 100%)',
};
```

---

## 🧩 Core Components

### 1. Hero Section Component

```typescript
// src/components/sections/hero-section.tsx

'use client';

import React from 'react';
import { motion } from 'framer-motion';
import ButtonPrimary from '../buttons/button-primary';
import ButtonSecondary from '../buttons/button-secondary';
import GradientBackground from '../ui/gradient-background';
import { colors, typography } from '@/tokens/design-system';

interface HeroSectionProps {
  headline?: string;
  subheadline?: string;
  primaryCTA?: string;
  secondaryCTA?: string;
  onPrimaryClick?: () => void;
  onSecondaryClick?: () => void;
  visualContent?: React.ReactNode;
}

export default function HeroSection({
  headline = 'Smarter Trading, Powered by Algorithms You Control',
  subheadline = 'Automate your stock and crypto trades with institutional-grade AI tools built for retail investors.',
  primaryCTA = 'Start Free Trial',
  secondaryCTA = 'Book Demo',
  onPrimaryClick,
  onSecondaryClick,
  visualContent,
}: HeroSectionProps) {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.8, ease: 'easeOut' },
    },
  };

  return (
    <section className="relative min-h-[600px] md:min-h-[700px] pt-20 md:pt-32 pb-20 md:pb-16 px-6 md:px-12 overflow-hidden">
      {/* Gradient Background */}
      <GradientBackground variant="hero" />

      {/* Animated Mesh Particles (Optional) */}
      <div className="absolute inset-0 pointer-events-none">
        {/* Add animated data particles or mesh background here */}
      </div>

      {/* Content */}
      <motion.div
        className="relative z-10 max-w-4xl mx-auto text-center"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Headline */}
        <motion.h1
          className="text-5xl md:text-7xl font-bold mb-6 text-white"
          style={{
            fontFamily: typography.fontFamilies.heading,
            lineHeight: typography.lineHeights.heading,
            letterSpacing: '-2%',
          }}
          variants={itemVariants}
        >
          {headline}
        </motion.h1>

        {/* Subheadline */}
        <motion.p
          className="text-xl md:text-2xl mb-12 text-slate-300 max-w-2xl mx-auto"
          style={{
            fontFamily: typography.fontFamilies.body,
            lineHeight: typography.lineHeights.body,
          }}
          variants={itemVariants}
        >
          {subheadline}
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          className="flex flex-col sm:flex-row gap-4 justify-center mb-16"
          variants={itemVariants}
        >
          <ButtonPrimary onClick={onPrimaryClick}>
            {primaryCTA} →
          </ButtonPrimary>
          <ButtonSecondary onClick={onSecondaryClick}>
            {secondaryCTA}
          </ButtonSecondary>
        </motion.div>

        {/* Key Stats */}
        <motion.div
          className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-3xl mx-auto"
          variants={itemVariants}
        >
          {[
            { value: '$5.2B', label: 'Total Volume' },
            { value: '50K+', label: 'Active Traders' },
            { value: '99.99%', label: 'Uptime' },
            { value: '24/7', label: 'Support' },
          ].map((stat, idx) => (
            <div
              key={idx}
              className="bg-white/10 backdrop-blur-md border border-white/20 rounded-lg p-4 md:p-6"
            >
              <div className="text-2xl md:text-3xl font-bold text-teal-400 mb-2">
                {stat.value}
              </div>
              <div className="text-slate-300 text-sm md:text-base">
                {stat.label}
              </div>
            </div>
          ))}
        </motion.div>
      </motion.div>

      {/* Visual Content */}
      {visualContent && (
        <motion.div
          className="relative z-10 mt-16 max-w-5xl mx-auto"
          variants={itemVariants}
          initial="hidden"
          animate="visible"
        >
          {visualContent}
        </motion.div>
      )}
    </section>
  );
}
```

### 2. Feature Card Component

```typescript
// src/components/cards/feature-card.tsx

'use client';

import React from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  metric?: string;
  metricLabel?: string;
  learnMoreLink?: string;
  variant?: 'default' | 'highlighted';
}

export default function FeatureCard({
  icon,
  title,
  description,
  metric,
  metricLabel,
  learnMoreLink = '#',
  variant = 'default',
}: FeatureCardProps) {
  return (
    <motion.div
      className={`
        rounded-lg border p-8 h-full flex flex-col
        transition-all duration-300 hover:-translate-y-1 hover:shadow-medium
        ${
          variant === 'highlighted'
            ? 'bg-gradient-to-br from-teal-500/10 to-emerald-500/10 border-teal-500/30'
            : 'bg-white border-slate-200 hover:border-teal-400'
        }
      `}
      whileHover={{
        y: -4,
        transition: { duration: 0.3 },
      }}
    >
      {/* Icon */}
      <div className="text-5xl mb-6">
        {icon}
      </div>

      {/* Title */}
      <h3 className="text-xl md:text-2xl font-bold text-slate-900 mb-3">
        {title}
      </h3>

      {/* Description */}
      <p className="text-slate-600 mb-6 flex-grow">
        {description}
      </p>

      {/* Metric */}
      {metric && (
        <div className="mb-6">
          <div className="text-3xl font-bold text-teal-600">
            {metric}
          </div>
          {metricLabel && (
            <div className="text-sm text-slate-500">
              {metricLabel}
            </div>
          )}
        </div>
      )}

      {/* Learn More Link */}
      <Link
        href={learnMoreLink}
        className="text-teal-600 hover:text-teal-700 font-semibold text-sm inline-flex items-center gap-2 transition-colors"
      >
        Learn more →
      </Link>
    </motion.div>
  );
}
```

### 3. Pricing Card Component

```typescript
// src/components/cards/pricing-card.tsx

'use client';

import React from 'react';
import { motion } from 'framer-motion';
import Badge from '../ui/badge';
import ButtonPrimary from '../buttons/button-primary';

interface Feature {
  text: string;
  included: boolean;
}

interface PricingCardProps {
  name: string;
  price: string | number;
  period?: string;
  tagline?: string;
  features: Feature[];
  buttonText?: string;
  buttonVariant?: 'primary' | 'secondary';
  isRecommended?: boolean;
  onClick?: () => void;
}

export default function PricingCard({
  name,
  price,
  period = '/month',
  tagline,
  features,
  buttonText = 'Get Started',
  buttonVariant = 'secondary',
  isRecommended = false,
  onClick,
}: PricingCardProps) {
  return (
    <motion.div
      className={`
        rounded-lg border p-8 flex flex-col relative
        transition-all duration-300
        ${
          isRecommended
            ? 'bg-gradient-to-br from-teal-500/10 to-emerald-500/10 border-teal-500/50 md:scale-105 shadow-medium'
            : 'bg-white border-slate-200 hover:border-slate-300'
        }
      `}
      whileHover={!isRecommended ? { y: -4 } : undefined}
    >
      {/* Recommended Badge */}
      {isRecommended && (
        <Badge variant="highlight" className="absolute -top-3 left-1/2 -translate-x-1/2">
          Most Popular
        </Badge>
      )}

      {/* Plan Name */}
      <h3 className="text-2xl font-bold text-slate-900 mb-3">
        {name}
      </h3>

      {/* Tagline */}
      {tagline && (
        <p className="text-slate-600 text-sm italic mb-6">
          {tagline}
        </p>
      )}

      {/* Price */}
      <div className="mb-8">
        <div className={`text-4xl font-bold ${
          isRecommended ? 'text-teal-600' : 'text-slate-900'
        }`}>
          {typeof price === 'number' ? `$${price}` : price}
        </div>
        <div className="text-slate-500 text-sm">
          {period}
        </div>
      </div>

      {/* CTA Button */}
      <ButtonPrimary
        variant={buttonVariant}
        onClick={onClick}
        className="mb-8"
        full
      >
        {buttonText}
      </ButtonPrimary>

      {/* Features List */}
      <div className="space-y-4 flex-grow">
        {features.map((feature, idx) => (
          <div key={idx} className="flex items-start gap-3">
            <div className={`
              flex-shrink-0 w-5 h-5 rounded-full flex items-center justify-center mt-0.5
              ${feature.included ? 'bg-emerald-100' : 'bg-slate-100'}
            `}>
              {feature.included ? (
                <svg className="w-3 h-3 text-emerald-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              ) : (
                <svg className="w-3 h-3 text-slate-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              )}
            </div>
            <span className={`text-sm ${feature.included ? 'text-slate-700' : 'text-slate-400'}`}>
              {feature.text}
            </span>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
```

### 4. Primary Button Component

```typescript
// src/components/buttons/button-primary.tsx

'use client';

import React from 'react';
import { motion } from 'framer-motion';

interface ButtonPrimaryProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'solid' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  full?: boolean;
  loading?: boolean;
  children: React.ReactNode;
}

export default function ButtonPrimary({
  variant = 'solid',
  size = 'lg',
  full = false,
  loading = false,
  children,
  className = '',
  ...props
}: ButtonPrimaryProps) {
  const sizeClasses = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-2.5 text-base',
    lg: 'px-8 py-3 text-base',
  };

  const baseClasses = `
    font-semibold rounded-lg transition-all duration-300
    hover:shadow-glow hover:scale-105 active:scale-98
    ${full ? 'w-full' : ''}
    ${sizeClasses[size]}
    ${loading ? 'opacity-75 cursor-not-allowed' : 'cursor-pointer'}
  `;

  const variantClasses = {
    solid: 'bg-gradient-to-r from-teal-500 to-emerald-500 text-white hover:from-teal-600 hover:to-emerald-600',
    outline: 'border-2 border-teal-500 text-teal-600 hover:bg-teal-50',
  };

  return (
    <motion.button
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
      whileTap={{ scale: 0.98 }}
      whileHover={{ scale: 1.02 }}
      disabled={loading}
      {...props}
    >
      {loading ? (
        <span className="flex items-center gap-2">
          <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" opacity="0.25" />
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z" fill="currentColor" />
          </svg>
          Loading...
        </span>
      ) : (
        children
      )}
    </motion.button>
  );
}
```

---

## 🎬 Animation Components

### Fade-In Animation

```typescript
// src/components/animations/fade-in.tsx

'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';

interface FadeInProps {
  children: React.ReactNode;
  delay?: number;
  duration?: number;
  threshold?: number;
}

export default function FadeIn({
  children,
  delay = 0,
  duration = 0.6,
  threshold = 0.1,
}: FadeInProps) {
  const { ref, inView } = useInView({
    threshold,
    triggerOnce: true,
  });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0 }}
      animate={inView ? { opacity: 1 } : { opacity: 0 }}
      transition={{ duration, delay, ease: 'easeOut' }}
    >
      {children}
    </motion.div>
  );
}
```

### Slide-Up Animation

```typescript
// src/components/animations/slide-up.tsx

'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';

interface SlideUpProps {
  children: React.ReactNode;
  delay?: number;
  duration?: number;
  threshold?: number;
}

export default function SlideUp({
  children,
  delay = 0,
  duration = 0.6,
  threshold = 0.1,
}: SlideUpProps) {
  const { ref, inView } = useInView({
    threshold,
    triggerOnce: true,
  });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 40 }}
      transition={{ duration, delay, ease: 'easeOut' }}
    >
      {children}
    </motion.div>
  );
}
```

---

## 📦 Dependencies Required

Add to `frontend/package.json`:

```json
{
  "dependencies": {
    "framer-motion": "^10.16.0",
    "react-intersection-observer": "^9.8.0",
    "react-responsive-carousel": "^3.15.0"
  }
}
```

Install with:
```bash
npm install framer-motion react-intersection-observer react-responsive-carousel
```

---

## 🔗 Usage Example

```typescript
// src/app/page.tsx

import HeroSection from '@/components/sections/hero-section';
import TrustSection from '@/components/sections/trust-section';
import FeaturesSection from '@/components/sections/features-section';
import DemoSection from '@/components/sections/demo-section';
import TestimonialsSection from '@/components/sections/testimonials-section';
import PricingSection from '@/components/sections/pricing-section';
import Footer from '@/components/layout/footer';

export default function Home() {
  return (
    <main>
      <HeroSection
        onPrimaryClick={() => console.log('Start Trial clicked')}
        onSecondaryClick={() => console.log('Book Demo clicked')}
      />
      <TrustSection />
      <FeaturesSection />
      <DemoSection />
      <TestimonialsSection />
      <PricingSection />
      <Footer />
    </main>
  );
}
```

---

## ✅ Implementation Checklist

- [ ] Import design tokens into all components
- [ ] Install Framer Motion and animation dependencies
- [ ] Create all section components from Figma designs
- [ ] Implement responsive breakpoints (mobile, tablet, desktop)
- [ ] Add scroll animations (Fade-In, Slide-Up, Scale-In)
- [ ] Add hover animations (cards, buttons, links)
- [ ] Test animation performance
- [ ] Implement accessibility (ARIA labels, keyboard navigation)
- [ ] Optimize images and assets
- [ ] Test responsive design on actual devices
- [ ] Deploy and monitor performance

---

## 📱 Responsive Testing

Test components on:
- Mobile: 375px (iPhone SE)
- Tablet: 768px (iPad)
- Desktop: 1440px (Full HD)

Use Chrome DevTools device emulation or actual devices.

