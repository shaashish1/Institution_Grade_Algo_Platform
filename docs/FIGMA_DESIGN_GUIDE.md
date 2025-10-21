# Figma Design Guide - Algo Trading Platform

## 📐 Design System Overview

### File Structure
```
Figma File: "Algo Trading Platform - Website Design"
├── 📄 Cover Page (Project Overview)
├── 🎨 Design System
│   ├── Color Palette
│   ├── Typography
│   ├── Spacing & Grid
│   ├── Components
│   └── Icons & Illustrations
├── 📱 Mobile Artboard (375px)
│   ├── Hero Mobile
│   ├── Trust Mobile
│   ├── Features Mobile
│   ├── Demo Mobile
│   ├── Testimonials Mobile
│   ├── Pricing Mobile
│   └── Footer Mobile
├── 💻 Desktop Artboard (1440px)
│   ├── Hero Desktop
│   ├── Trust Desktop
│   ├── Features Desktop
│   ├── Demo Desktop
│   ├── Testimonials Desktop
│   ├── Pricing Desktop
│   └── Footer Desktop
└── 🔧 Component Library (Reusable)
    ├── Hero Section
    ├── Feature Card
    ├── Pricing Card
    ├── Testimonial Slider
    ├── Navbar
    ├── Footer
    ├── CTA Button
    ├── Badge
    └── Icon Set
```

---

## 🎨 Design System

### Color Palette

| Name | Color Code | Usage | RGB |
|------|-----------|-------|-----|
| Navy Primary | #0C1B2A | Trust, backgrounds, text | rgb(12, 27, 42) |
| Teal Accent | #00C7B7 | Highlights, interactive, hover | rgb(0, 199, 183) |
| Off-white BG | #F8FAFC | Main background, cards | rgb(248, 250, 252) |
| Silver Gray | #D1D5DB | Dividers, secondary text | rgb(209, 213, 219) |
| Emerald Success | #10B981 | Success states, CTAs | rgb(16, 185, 129) |
| Gold Accent | #FACC15 | Premium features, highlights | rgb(250, 204, 21) |
| Dark Text | #1F2937 | Body text on light bg | rgb(31, 41, 55) |
| Light Text | #F3F4F6 | Body text on dark bg | rgb(243, 244, 246) |

### Color Variants
```
Navy Shades:
  - #0C1B2A (Main)
  - #142038 (Hover)
  - #1A2842 (Active)

Teal Shades:
  - #00C7B7 (Main)
  - #00A89F (Hover)
  - #008E82 (Active)

Gradient Definitions:
  - Hero Gradient: #0C1B2A → #1A3A52 (top-left to bottom-right)
  - Accent Gradient: #00C7B7 → #10B981 (left to right)
  - Gold Gradient: #FACC15 → #F59E0B (left to right)
```

### Typography

#### Font Families
- **Headings (H1-H4):** Satoshi or Poppins
  - Weight: Bold (700)
  - Spacing: -2% letter-spacing for large sizes

- **Body & UI Text:** Inter or DM Sans
  - Weight: Regular (400), Semibold (600)
  - Line Height: 1.5x (body), 1.2x (headings)

#### Type Scale
```
H1 (Hero Headline): 56px / 64px (desktop/mobile)
  Line Height: 1.2
  Letter Spacing: -2%
  Weight: 700 (Bold)

H2 (Section Headline): 40px / 32px (desktop/mobile)
  Line Height: 1.3
  Letter Spacing: -1%
  Weight: 700 (Bold)

H3 (Card Title): 24px / 20px (desktop/mobile)
  Line Height: 1.3
  Weight: 700 (Bold)

H4 (Feature Title): 18px / 16px (desktop/mobile)
  Line Height: 1.4
  Weight: 600 (Semibold)

Body Large: 16px
  Line Height: 1.5
  Weight: 400

Body Regular: 14px
  Line Height: 1.5
  Weight: 400

Label/Caption: 12px
  Line Height: 1.5
  Weight: 600
  Text Transform: Uppercase (optional)
```

### Spacing System (8px base)

```
xs: 4px
sm: 8px
md: 16px
lg: 24px
xl: 32px
2xl: 48px
3xl: 64px
4xl: 96px
```

### Grid System

#### Desktop (1440px)
- Columns: 12
- Column Width: 88px
- Gutter: 32px
- Margin: 40px (left/right)
- Working Width: 1360px

#### Tablet (768px)
- Columns: 8
- Column Width: 72px
- Gutter: 24px
- Margin: 24px
- Working Width: 720px

#### Mobile (375px)
- Columns: 4
- Column Width: 70px
- Gutter: 16px
- Margin: 16px
- Working Width: 343px

### Shadows & Effects

```
Subtle Shadow (Cards):
  X: 0px, Y: 1px
  Blur: 3px
  Spread: 0px
  Color: rgba(12, 27, 42, 0.08)

Medium Shadow (Hover):
  X: 0px, Y: 4px
  Blur: 12px
  Spread: 0px
  Color: rgba(12, 27, 42, 0.12)

Glow Effect (CTA):
  Blur: 20px
  Color: rgba(0, 199, 183, 0.3)

Glass Effect (Glassmorphism):
  Background: rgba(248, 250, 252, 0.7)
  Backdrop Filter: blur(10px)
  Border: 1px solid rgba(255, 255, 255, 0.2)
```

### Border Radius

```
Sharp: 0px
sm: 4px
md: 8px
lg: 12px
xl: 16px
full: 9999px (circular)
```

---

## 🧩 Component Specifications

### 1. Hero Section

**Layout:** Full-width, 600px+ height

**Components:**
- Background: Gradient (#0C1B2A → #1A3A52) with animated mesh overlay
- Headline: H1, Navy, max-width 800px
- Subheadline: Body Large, Silver Gray, max-width 600px
- CTA Button Group:
  - Primary: "Start Free Trial" (Teal BG, white text)
  - Secondary: "Book Demo" (Outline, Teal border)
- Floating Visual: Dashboard mockup or animated data particles

**Desktop Spacing:**
- Top padding: 120px
- Bottom padding: 80px
- Button gap: 16px

**Mobile Spacing:**
- Top padding: 80px
- Bottom padding: 60px
- Button layout: Stack vertically
- Full width buttons with 16px margin

---

### 2. Trust Section (Why Choose Us)

**Layout:** 3-column grid (desktop), stacked (mobile)

**Column 1:**
- Icon: ⚙️ (48px)
- Title: "Proven Algorithms"
- Description: "Backtested and optimized for real market conditions."

**Column 2:**
- Icon: 🔒 (48px)
- Title: "Enterprise Security"
- Description: "Bank-level encryption for peace of mind."

**Column 3:**
- Icon: 🤝 (48px)
- Title: "Trusted by Traders"
- Description: "Thousands of active users worldwide."

**Below Grid:**
- Horizontal logo strip with 5-6 exchange logos
- Spacing: 32px between logos
- Logo size: 40px height, auto width

**Background:** Off-white (#F8FAFC)
**Padding:** 80px vertical, 40px horizontal
**Divider:** Light gray line above section

---

### 3. Features Section

**Layout:** 2x2 grid (desktop), stacked (mobile)

**Card 1: Live Algo Dashboard**
- Icon: 📊
- Title: "Live Algo Dashboard"
- Description: "Monitor real-time performance, profit & loss, and execution stats."
- Metric: "$2.4M" (large text, Teal)
- Metric Label: "in trades executed"
- CTA Link: "Learn more →"

**Card 2: Strategy Builder**
- Icon: ⚙️
- Title: "No-Code Strategy Builder"
- Description: "Create sophisticated trading strategies without writing code."
- Metric: "1000+"
- Metric Label: "strategies deployed"
- CTA Link: "Learn more →"

**Card 3: Real-time Insights**
- Icon: 📈
- Title: "Real-time Market Insights"
- Description: "AI-powered market analysis with actionable alerts."
- Metric: "24/7"
- Metric Label: "market monitoring"
- CTA Link: "Learn more →"

**Card 4: Automated Execution**
- Icon: ⚡
- Title: "24/7 Automated Execution"
- Description: "Your algorithms trade while you sleep, worldwide markets covered."
- Metric: "<1ms"
- Metric Label: "execution latency"
- CTA Link: "Learn more →"

**Card Styling:**
- Background: White with subtle shadow
- Border: 1px solid Silver Gray
- Padding: 32px
- Hover effect: Lift (translateY -4px) + shadow increase
- Icon color: Teal gradient

**Background:** Off-white (#F8FAFC)
**Section Padding:** 80px vertical, 40px horizontal

---

### 4. Product Demo Section

**Layout:** Single column, centered

**Components:**
- Headline: H2, Navy
- Dashboard Mockup: Large image/mockup (800px width, desktop)
- Overlay Text: "Build, backtest, and deploy your strategy in minutes."
- Position overlay: Bottom-left corner of dashboard
- Background behind text: Semi-transparent Navy
- CTA Button: "Explore Platform" (Emerald #10B981)

**Background:** Navy gradient (#0C1B2A → #142038)
**Image Height:** 450px (desktop)
**Padding:** 80px vertical

**Mobile:**
- Image Height: 300px
- Overlay: Full width, bottom positioned
- Padding: 60px vertical

---

### 5. Testimonials Section

**Layout:** Horizontal slider (carousel)

**Testimonial Card:**
- Quote text: Body Regular, Italic
- Author photo: 48px circle, placeholder
- Author name: H4, Navy
- Role/title: Label, Silver Gray
- Star rating: 5 stars (Teal)
- Background: White, shadow
- Padding: 32px
- Width: 320px (fixed for carousel)

**Sample Testimonials:**

1. "AlgoTrading has transformed my portfolio. The backtesting tools are incredibly accurate and the automation has saved me hours."
   - Name: Arjun Sharma
   - Role: Independent Trader, Mumbai

2. "Finally, institutional-grade tools available to retail investors. The performance metrics alone make it worth it."
   - Name: Priya Singh
   - Role: Portfolio Manager, Delhi

3. "Secure, reliable, and intuitive. I trust this platform with my investments without hesitation."
   - Name: Vikram Kumar
   - Role: Crypto Enthusiast, Bangalore

**Carousel Controls:**
- Next/Prev arrows on sides
- Dot indicators at bottom
- Auto-scroll: every 6 seconds (optional)

**Background:** Off-white (#F8FAFC)
**Section Padding:** 80px vertical

---

### 6. Pricing Section

**Layout:** 3-column grid (desktop), stacked (mobile)

**Pricing Card (Base Structure):**
- Header: Plan name (H3)
- Price: Large text, Teal for highlighted plan
- Price period: "/ month" (Body Small)
- Tagline: Italic text (optional)
- Feature list: Bulleted (10-12 items)
- CTA button: Full width, 48px height
- Recommended badge: "Most Popular" (Teal label, top-center)

**Plan 1: Starter**
- Price: $49/month
- Button: "Get Started" (White text, Navy background)
- Button style: Outline
- Features:
  - Up to 5 algorithms
  - Real-time alerts
  - Basic analytics
  - Email support
  - Community access
  - Backtesting (30 days)
  - 1 portfolio
  - Market data (20 min delay)
  - Strategy templates
  - Desktop app
  - Mobile app
  - Auto-rebalancing

**Plan 2: Pro** (Recommended/Highlighted)
- Price: $199/month
- Badge: "Most Popular"
- Background: Gradient (Teal → Emerald)
- Button: "Start Free Trial" (Teal/Emerald gradient)
- Button style: Solid
- Features: All from Starter +
  - Unlimited algorithms
  - Webhooks API
  - Advanced analytics
  - Priority support
  - Private Slack channel
  - Unlimited backtesting
  - 10 portfolios
  - Real-time market data
  - Custom indicators
  - VIP education
  - Advanced charts
  - Risk analytics

**Plan 3: Institutional**
- Price: "Contact Sales"
- Button: "Book Demo" (Outline, Navy)
- Button style: Outline
- Features: All from Pro +
  - Custom algorithms
  - Dedicated account manager
  - White-label options
  - Advanced security
  - Enterprise API
  - Co-marketing opportunities
  - Custom reporting
  - Multiple teams
  - Advanced compliance
  - Custom integrations
  - SLA guarantee
  - Training & onboarding

**Card Spacing:**
- Gap between cards: 32px
- Card width: equal (1/3 each)
- Card height: auto (content-driven)
- Padding inside: 32px

**Background:** Off-white (#F8FAFC)
**Section Padding:** 80px vertical

**Mobile:** 
- Full width cards
- Margin: 16px bottom

---

### 7. Footer

**Layout:** 4-column grid (desktop), stacked (mobile)

**Column 1: Company**
- Logo (40px height)
- Description: "Smart trading for everyone."
- Social icons: LinkedIn, X (Twitter), GitHub (24px, Teal on hover)

**Column 2: Legal**
- Heading: "Legal"
- Links:
  - Terms of Service
  - Privacy Policy
  - Cookie Policy
  - Compliance
  - SEBI Registration

**Column 3: Resources**
- Heading: "Resources"
- Links:
  - Documentation
  - API Reference
  - Community Forum
  - Blog
  - Help Center

**Column 4: Contact**
- Heading: "Contact"
- Links/Info:
  - Email: hello@algotrading.com
  - Phone: +91 80000 00000
  - Address: India
  - Newsletter signup

**Bottom Bar:**
- Copyright text: "© 2025 AlgoTrading. All rights reserved."
- Compliance note: "Registered & compliant with SEBI standards."
- Icons: Security badge, verified checkmark

**Background:** Navy (#0C1B2A)
**Text Color:** Light text (#F3F4F6)
**Link hover:** Teal (#00C7B7)
**Padding:** 60px vertical, 40px horizontal
**Border-top:** 1px solid Teal (with 0.2 opacity)

---

## 🎬 Animation & Motion Specifications

### Scroll Animations (On-Scroll Entry)

```
Fade In (Hero):
  Duration: 0.8s
  Easing: ease-out
  Opacity: 0 → 1
  Delay: Staggered (100ms between elements)

Slide Up (Sections):
  Duration: 0.6s
  Easing: ease-out
  Transform: translateY(40px) → translateY(0)
  Opacity: 0 → 1

Scale In (Cards):
  Duration: 0.5s
  Easing: ease-out
  Transform: scale(0.95) → scale(1)
  Opacity: 0 → 1
  Stagger: 100ms per card
```

### Hover States

```
Button Hover:
  Duration: 0.3s
  Effects:
    - Background color shift (Teal → Emerald)
    - Shadow elevation increase
    - Text slight upward movement (2px)
    - Glow effect appear

Card Hover:
  Duration: 0.3s
  Effects:
    - Lift: translateY(-4px)
    - Shadow increase: Medium shadow
    - Background subtle brightening
    - Icon color shift: Navy → Teal

Link Hover:
  Duration: 0.2s
  Effects:
    - Color: Navy → Teal
    - Underline appear (2px)
    - Text shift right (1px)
```

### Micro-interactions

```
CTA Button Click:
  Duration: 0.2s
  Effects:
    - Scale: 1 → 0.98 (press effect)
    - Back to 1 after release

Testimonial Carousel:
  Transition: 0.5s ease-in-out
  Auto-scroll: 6s interval
  Pause on hover

Data Particles (Hero background):
  - Floating animation: 20s infinite
  - Opacity pulse: 0.3 → 0.6 → 0.3
  - Movement: Subtle drift effect
```

---

## 📱 Responsive Design Breakpoints

### Desktop (1440px)
- 12-column grid
- 40px margins
- Full visibility of all elements
- Hover states active

### Tablet (768px)
- 8-column grid
- 24px margins
- 2-column layouts collapse to single column
- Touch-friendly button sizing (48px min)

### Mobile (375px)
- 4-column grid
- 16px margins
- Single column layouts
- Full-width CTAs
- Hamburger navigation
- Carousel on testimonials
- Stacked pricing cards

---

## 🔧 Component Library

### Create Figma Components

1. **HeroSection**
   - Variants: Desktop, Mobile
   - Main elements: Background, Headline, Subheadline, Buttons, Visual

2. **FeatureCard**
   - Variants: Default, Hover, Active
   - Size variants: Small, Large
   - Fields: Icon, Title, Description, Metric, Metric Label, CTA Link

3. **PricingCard**
   - Variants: Starter, Pro (Recommended), Institutional
   - Size variants: Desktop, Mobile
   - Fields: Title, Price, Badge, Features, CTA Button

4. **TestimonialCard**
   - Variants: Light, Dark
   - Elements: Quote, Avatar, Name, Role, Rating

5. **Navbar**
   - Variants: Default, Sticky, Mobile Menu
   - Elements: Logo, Nav links, CTA button

6. **Footer**
   - Variants: Full, Compact
   - Columns: Company, Legal, Resources, Contact

7. **ButtonPrimary**
   - Variants: Default, Hover, Active, Disabled
   - Sizes: Small (36px), Medium (44px), Large (48px)
   - States: Normal, Loading, Success

8. **ButtonSecondary** (Outlined)
   - Same variants and sizes as Primary

9. **Badge**
   - Variants: Success, Highlight, Teal, Gold
   - Sizes: Small (sm), Medium (md)

10. **IconCard**
    - 48px circular background
    - Icon center (32px)
    - Color variants: Teal, Emerald, Gold, Navy

---

## 📤 Export & Dev Handoff

### File Organization
- Organize layers hierarchically
- Name components clearly (BtnPrimary, FeatureCardLarge, etc.)
- Use component variants instead of duplicating
- Add annotations with documentation

### Export Specifications

**For Developers:**
1. Export all components as individual artboards
2. Color palette: Export as CSS variables or design tokens
3. Typography: Export type scale with font names
4. Icons: Export as SVG (24px, 32px, 48px sizes)
5. Spacing: Document 8px grid system

**Asset Sizes:**
- Hero mockup: 1200px x 600px (2x for retina)
- Feature icons: 48px, 64px
- Social icons: 24px, 32px
- Logo: 32px, 40px, 200px (light + dark variants)

### Design Specs & Annotations

Add Figma comments/annotations on:
- Color values & usage guidelines
- Typography hierarchy and weights
- Animation timing and easing
- Responsive behavior at breakpoints
- Component composition rules

---

## 🎯 Implementation Checklist

- [ ] Create Figma file with all pages and artboards
- [ ] Set up design system (colors, typography, grid, shadows)
- [ ] Design hero section with background variations
- [ ] Create trust/why-choose-us section with 3 columns
- [ ] Build feature cards component with 2x2 grid
- [ ] Design product demo section with mockup overlay
- [ ] Create testimonial carousel mockup
- [ ] Design 3-tier pricing cards with variants
- [ ] Create footer component
- [ ] Build reusable component library
- [ ] Add animation/transition annotations
- [ ] Create mobile responsive versions for all sections
- [ ] Document design system in Figma
- [ ] Export assets and create dev handoff documentation
- [ ] Share Figma file with development team

---

## 🔗 Resources & Tools

- **Figma Plugins:**
  - Iconify (for icons)
  - Remove.bg (for backgrounds)
  - Content Reel (for Lorem ipsum)
  - UI Faces (for avatars)

- **Design Inspiration:**
  - Dribbble fintech category
  - Awwwards best in category
  - Fintech startup websites

- **Implementation:**
  - Next.js 15.5.6
  - React 18.2.0
  - Tailwind CSS 3.3.0
  - Framer Motion (for animations)
  - React Carousel (for testimonials)

---

## 📞 Design Collaboration Notes

- Use Figma's collaboration features for real-time feedback
- Create a dedicated Figma team/workspace
- Use dev mode for smooth handoff to developers
- Keep design file updated as requirements evolve
- Use Figma specs export for accurate measurements

