# Figma Design - Quick Reference Card

## 🎨 Color Palette

```
Primary Colors:
Navy #0C1B2A    ⬛ Trust & Base
Teal #00C7B7    🟦 Accent & Interactive  
Off-white #F8FAFC ⬜ Background

Accents:
Emerald #10B981 🟩 Success & CTAs
Gold #FACC15    🟨 Premium Highlight
Silver #D1D5DB  ⬜ Dividers & Text

Text:
Dark #1F2937    Black on Light
Light #F3F4F6   White on Dark
```

---

## 🔤 Typography

| Style | Size | Weight | Font |
|-------|------|--------|------|
| H1 | 56px (32px mobile) | 700 | Satoshi/Poppins |
| H2 | 40px (28px mobile) | 700 | Satoshi/Poppins |
| H3 | 24px (20px mobile) | 700 | Satoshi/Poppins |
| H4 | 18px (16px mobile) | 600 | Satoshi/Poppins |
| Body Large | 16px | 400 | Inter/DM Sans |
| Body | 14px | 400 | Inter/DM Sans |
| Caption | 12px | 600 | Inter/DM Sans |

---

## 📏 Spacing (8px Grid)

```
xs: 4px   | sm: 8px   | md: 16px   | lg: 24px  | xl: 32px
2xl: 48px | 3xl: 64px | 4xl: 96px  | 5xl: 128px
```

**Common Patterns:**
- Card padding: 32px (xl)
- Section padding: 80px vertical, 40px horizontal
- Card gap: 32px
- Button padding: 12px v, 24px h

---

## 📐 Responsive Grid

| Device | Width | Columns | Gutter | Margin | Working |
|--------|-------|---------|--------|--------|---------|
| Mobile | 375px | 4 | 16px | 16px | 343px |
| Tablet | 768px | 8 | 24px | 24px | 720px |
| Desktop | 1440px | 12 | 32px | 40px | 1360px |

---

## 🎬 Animations

| Element | Animation | Duration | Timing |
|---------|-----------|----------|--------|
| Hero Headline | Fade + Slide Up | 0.8s | ease-out |
| Hero Buttons | Fade In | 0.6s | ease-out |
| Cards (Scroll) | Fade + Scale | 0.5s | ease-out |
| Card Hover | Lift 4px + Shadow | 0.3s | ease-out |
| Button Hover | Scale 1.02 + Glow | 0.3s | ease-out |
| Button Click | Scale 0.98 | 0.1s | linear |

**Stagger:** 100ms between children

---

## 🧩 Component Sizes

### Feature Card
- Desktop: 320 × 280
- Mobile: Full width (343px)
- Padding: 32px
- Gap: 32px between cards

### Pricing Card
- Desktop: 320 × 600
- Mobile: Full width (343px)
- Recommended: 1.05 scale
- Gap: 32px desktop, 20px mobile

### Testimonial Card
- Size: 320 × 200
- Mobile: Full width
- Avatar: 48px circle
- Gap: 32px

### Button
- Small: 36px height, 8px v-padding
- Medium: 44px height, 12px v-padding
- Large: 48px height, 12px v-padding
- Horizontal: 24px padding

---

## 🖼️ Frame Sizes (Desktop)

```
Hero: 1440 × 600
Trust: 1440 × 500
Features: 1440 × 700
Demo: 1440 × 600
Testimonials: 1440 × 500
Pricing: 1440 × 800
Footer: 1440 × 400
```

**Total page height:** ~4200px

---

## 📱 Frame Sizes (Mobile)

```
Hero: 375 × 500
Trust: 375 × 600
Features: 375 × 900
Demo: 375 × 400
Testimonials: 375 × 500
Pricing: 375 × 1200
Footer: 375 × 400
```

**Total page height:** ~4500px

---

## 💾 Gradients

**Hero Background**
```
Type: Linear
Angle: 135°
Start: #0C1B2A (Navy)
End: #1A3A52 (Navy Light)
```

**CTA Buttons**
```
Type: Linear
Angle: 90°
Start: #00C7B7 (Teal)
End: #10B981 (Emerald)
```

**Premium Highlight**
```
Type: Linear
Angle: 90°
Start: #FACC15 (Gold)
End: #F59E0B (Gold Dark)
```

---

## 🔳 Border Radius

```
Small: 4px
Medium: 8px
Large: 12px
XL: 16px
Full: 9999px (circles)
```

---

## 💧 Shadows

**Subtle** (Default)
```
Offset: 0, 1
Blur: 3px
Color: rgba(12, 27, 42, 0.08)
```

**Medium** (Hover)
```
Offset: 0, 4
Blur: 12px
Color: rgba(12, 27, 42, 0.12)
```

**Glow** (CTA)
```
Offset: 0, 0
Blur: 20px
Color: rgba(0, 199, 183, 0.3)
```

---

## 🧩 7 Core Sections

1. **Hero**
   - Headline, subheadline, 2 CTAs
   - 4 stat cards
   - Gradient background

2. **Trust**
   - 3 columns (icons, text)
   - Logo strip
   - Navy background

3. **Features**
   - 2×2 card grid
   - 4 feature cards
   - Icons + metrics

4. **Demo**
   - Dashboard mockup
   - Overlay text
   - CTA button

5. **Testimonials**
   - Carousel/slider
   - 3 cards
   - Navigation dots

6. **Pricing**
   - 3 pricing cards
   - Recommended badge
   - Feature lists

7. **Footer**
   - 4 columns
   - Social links
   - Compliance info

---

## 📋 Component Library (8 Core)

1. **Button/Primary** - CTA buttons (solid)
2. **Button/Secondary** - Outlined buttons
3. **Card/Feature** - Feature showcase
4. **Card/Pricing** - Pricing plans
5. **Card/Testimonial** - User reviews
6. **Badge/Icon** - Circular icons
7. **Navbar** - Header navigation
8. **Footer** - Site footer

Each component should have:
- ✅ Default state
- ✅ Hover state
- ✅ Active/Selected state
- ✅ Desktop variant
- ✅ Mobile variant

---

## 🎯 Design Specifications Checklist

- [ ] All colors match palette
- [ ] Typography matches scale
- [ ] Spacing uses 8px grid
- [ ] Border radius consistent
- [ ] Shadows applied correctly
- [ ] Components are reusable
- [ ] Mobile versions created
- [ ] Hover states defined
- [ ] Animations documented
- [ ] Accessibility verified

---

## 🚀 Quick Start Steps

1. Create Figma file
2. Set up color library
3. Create typography styles
4. Build component library
5. Design hero section
6. Design remaining sections
7. Create mobile versions
8. Add animations
9. Export assets
10. Create handoff doc

---

## 📞 Key Files

| File | Purpose | Use When |
|------|---------|----------|
| FIGMA_DESIGN_GUIDE.md | Complete specs | Designing in Figma |
| FIGMA_DESIGN_TOKENS.md | CSS/JSON ready | Need exact values |
| FIGMA_TO_REACT_GUIDE.md | React code | Implementing |
| FIGMA_STEP_BY_STEP.md | Tutorial | Learning Figma |

---

## 💡 Pro Tips

1. **Use components** for everything reusable
2. **Name layers clearly** (helps developers)
3. **Snap to grid** (perfect alignment)
4. **Create variants** (hover, active, disabled)
5. **Document interactions** (add comments)
6. **Export regularly** (assets needed for dev)
7. **Test on devices** (use Figma Mirror)
8. **Version control** (track changes)

---

## ⚡ Common Measurements

```
Hero height: 600px (desktop), 500px (mobile)
Card width: 320px (desktop), full width (mobile)
Button height: 48px (large), 44px (medium)
Icon size: 48px (large), 32px (medium), 24px (small)
Logo height: 40px (default), 200px (full)
Gap between sections: 80px vertical
Avatar size: 48px (circle)
Stat value font: 32px
Section padding: 80px v, 40px h (desktop)
```

---

## 🎨 Theme Variants (Optional)

Beyond the primary design, consider these variants:

**Dark Mode**
- Background: Navy shades
- Text: Light colors
- Accents: Keep Teal bright

**Light Mode**
- Background: Off-white
- Text: Dark colors
- Accents: Teal slightly darker

**Accessibility Mode**
- Higher contrast
- Larger text
- Simplified animations
- Clear focus indicators

---

## 📊 File Organization Example

```
Figma File: "Algo Trading Platform"
├── 📄 Cover
├── 📄 Design System
│  ├─ Colors
│  ├─ Typography
│  ├─ Shadows
│  └─ Grid
├── 📄 Desktop Full Page
│  ├─ Hero
│  ├─ Trust
│  ├─ Features
│  ├─ Demo
│  ├─ Testimonials
│  ├─ Pricing
│  └─ Footer
├── 📄 Mobile Full Page
│  ├─ Hero
│  ├─ Trust
│  ├─ Features
│  ├─ Demo
│  ├─ Testimonials
│  ├─ Pricing
│  └─ Footer
├── 📄 Components Library
│  ├─ Buttons
│  ├─ Cards
│  ├─ Badges
│  ├─ Icons
│  └─ Utility
└── 📄 Animations & Specs
```

---

## ✅ Quality Checklist

**Design Quality**
- [ ] Professional appearance
- [ ] Clear visual hierarchy
- [ ] Consistent branding
- [ ] Accessible colors (WCAG AA)
- [ ] Proper typography scale
- [ ] Appropriate whitespace

**Developer Readiness**
- [ ] All components documented
- [ ] Measurements precise
- [ ] Assets exported
- [ ] Color codes provided
- [ ] Animation specs clear
- [ ] Responsive versions ready

**User Experience**
- [ ] Clear CTAs
- [ ] Good visual flow
- [ ] Trusted messaging
- [ ] Fast perception
- [ ] Mobile-friendly
- [ ] Engaging interactions

---

**Print this card and keep it handy while designing! 📌**

