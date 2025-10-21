# Figma Design System - CSS & JSON Reference

## 🎨 Color Palette (Ready to Use in Figma)

### Primary Colors

```
Navy Primary
HEX: #0C1B2A
RGB: 12, 27, 42
HSL: 205, 54%, 11%

Teal Accent
HEX: #00C7B7
RGB: 0, 199, 183
HSL: 172, 100%, 39%

Off-white Background
HEX: #F8FAFC
RGB: 248, 250, 252
HSL: 210, 40%, 98%

Silver Gray
HEX: #D1D5DB
RGB: 209, 213, 219
HSL: 210, 14%, 84%

Emerald Success
HEX: #10B981
RGB: 16, 185, 129
HSL: 160, 84%, 39%

Gold Accent
HEX: #FACC15
RGB: 250, 204, 21
HSL: 45, 96%, 53%
```

### Text Colors

```
Dark Text (Light BG)
HEX: #1F2937
RGB: 31, 41, 55
HSL: 217, 33%, 17%

Light Text (Dark BG)
HEX: #F3F4F6
RGB: 243, 244, 246
HSL: 210, 14%, 96%
```

### Color Variants in JSON Format

```json
{
  "colors": {
    "navy": {
      "50": "#F7F9FB",
      "100": "#EEF2F8",
      "200": "#DDE5F1",
      "300": "#C2D1E5",
      "400": "#A3B8D9",
      "500": "#7A92BB",
      "600": "#4D5F7D",
      "700": "#2C3E5A",
      "800": "#1A2842",
      "900": "#0C1B2A"
    },
    "teal": {
      "50": "#F0FFFE",
      "100": "#CCFAF6",
      "200": "#99F5F0",
      "300": "#66E4E1",
      "400": "#33CFCA",
      "500": "#00C7B7",
      "600": "#009B8A",
      "700": "#007166",
      "800": "#004E44",
      "900": "#002C26"
    },
    "emerald": {
      "50": "#F0FDF5",
      "100": "#DCFCE8",
      "200": "#B8F8D4",
      "300": "#88F0BB",
      "400": "#4EE09E",
      "500": "#10B981",
      "600": "#059669",
      "700": "#047857",
      "800": "#065F46",
      "900": "#064E3B"
    },
    "gold": {
      "50": "#FEFCE9",
      "100": "#FEF8C3",
      "200": "#FEF08A",
      "300": "#FDE047",
      "400": "#FACC15",
      "500": "#EAB308",
      "600": "#CA8A04",
      "700": "#A16207",
      "800": "#854D0E",
      "900": "#713F12"
    }
  }
}
```

---

## 🔤 Typography Specifications

### Font Import URLs

For Figma, use these font families:
- **Headings:** Satoshi, Poppins
- **Body:** Inter, DM Sans

### Type Scale (All sizes with line heights)

```
Heading 1 (H1)
Desktop: 56px
Mobile: 32px
Weight: 700 (Bold)
Line Height: 1.2 (67px / 38px)
Letter Spacing: -2% (-1.12px / -0.64px)

Heading 2 (H2)
Desktop: 40px
Mobile: 28px
Weight: 700 (Bold)
Line Height: 1.3 (52px / 36px)
Letter Spacing: -1% (-0.4px / -0.28px)

Heading 3 (H3)
Desktop: 24px
Mobile: 20px
Weight: 700 (Bold)
Line Height: 1.3 (31px / 26px)
Letter Spacing: 0

Heading 4 (H4)
Desktop: 18px
Mobile: 16px
Weight: 600 (Semibold)
Line Height: 1.4 (25px / 22px)
Letter Spacing: 0

Body Large
Size: 16px
Weight: 400 (Regular)
Line Height: 1.5 (24px)
Letter Spacing: 0

Body Regular
Size: 14px
Weight: 400 (Regular)
Line Height: 1.5 (21px)
Letter Spacing: 0

Caption/Label
Size: 12px
Weight: 600 (Semibold)
Line Height: 1.5 (18px)
Letter Spacing: 0
Text Transform: Uppercase (optional)
```

### CSS Font Stack

```css
/* Headings */
font-family: 'Satoshi', 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Body Text */
font-family: 'Inter', 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

---

## 🎨 Gradients

### Gradient Definitions for Figma

**Hero Gradient (Background)**
```
Type: Linear
Angle: 135° (top-left to bottom-right)
Start Color: #0C1B2A (Navy)
End Color: #1A3A52 (Navy Light)
```

**Accent Gradient (CTAs)**
```
Type: Linear
Angle: 90° (left to right)
Start Color: #00C7B7 (Teal)
End Color: #10B981 (Emerald)
```

**Gold Gradient (Premium)**
```
Type: Linear
Angle: 90° (left to right)
Start Color: #FACC15 (Gold)
End Color: #F59E0B (Gold Dark)
```

**Glass Effect Background**
```
Type: Solid + Backdrop Blur
Background Color: rgba(248, 250, 252, 0.7)
Backdrop Filter: blur(10px)
Border: 1px solid rgba(255, 255, 255, 0.2)
```

---

## 🔳 Border Radius System

```
Extra Small: 4px
Small: 8px
Medium: 12px
Large: 16px
Extra Large: 24px
Full (Circle): 9999px / 50%
```

---

## 💧 Shadows & Depth

### Shadow System

```
Subtle Shadow (Cards, hover state for buttons)
X Offset: 0px
Y Offset: 1px
Blur: 3px
Spread: 0px
Color: rgba(12, 27, 42, 0.08)
CSS: 0 1px 3px rgba(12, 27, 42, 0.08)

Medium Shadow (Card hover, active state)
X Offset: 0px
Y Offset: 4px
Blur: 12px
Spread: 0px
Color: rgba(12, 27, 42, 0.12)
CSS: 0 4px 12px rgba(12, 27, 42, 0.12)

Glow Effect (CTA buttons, accent)
X Offset: 0px
Y Offset: 0px
Blur: 20px
Spread: 0px
Color: rgba(0, 199, 183, 0.3)
CSS: 0 0 20px rgba(0, 199, 183, 0.3)
```

---

## 📐 Spacing Scale (8px Base)

```
2xs:   2px
xs:    4px
sm:    8px
md:    16px
lg:    24px
xl:    32px
2xl:   48px
3xl:   64px
4xl:   96px
5xl:   128px
```

### Common Spacing Patterns

```
Card Padding: 32px (xl)
Section Padding (Vertical): 80px (3xl + xl)
Section Padding (Horizontal): 40px (xl + md)
Gap between cards: 32px (xl) desktop, 24px (lg) mobile
Button Padding (Vertical): 12px (md + sm)
Button Padding (Horizontal): 24px (lg)
```

---

## 📱 Responsive Grid System

### Desktop (1440px)

```
Columns: 12
Column Width: 88px
Gutter: 32px
Margin: 40px each side
Working Width: 1360px
Total Width: 1440px

Layout Calculation:
(12 × 88px) + (11 × 32px) + (2 × 40px) = 1440px
```

### Tablet (768px)

```
Columns: 8
Column Width: 72px
Gutter: 24px
Margin: 24px each side
Working Width: 720px
Total Width: 768px

Layout Calculation:
(8 × 72px) + (7 × 24px) + (2 × 24px) = 768px
```

### Mobile (375px)

```
Columns: 4
Column Width: 70px
Gutter: 16px
Margin: 16px each side
Working Width: 343px
Total Width: 375px

Layout Calculation:
(4 × 70px) + (3 × 16px) + (2 × 16px) = 375px
```

---

## 🎬 Animation Specifications

### Timing & Easing

```
Ease Out (Entrance):
cubic-bezier(0.16, 1, 0.3, 1)

Ease In Out (Transition):
cubic-bezier(0.4, 0, 0.2, 1)

Ease Out (Exit):
cubic-bezier(0.7, 0, 0.84, 0)

Spring Animation:
tension: 170
friction: 26
mass: 1
```

### Micro-interaction Timing

```
Button Hover: 0.3s ease-out
Card Lift: 0.3s ease-out
Fade In: 0.6s ease-out
Slide Up: 0.6s ease-out
Scale In: 0.5s ease-out
Stagger Delay: 100ms between elements
```

### Transformation Values

```
Button Press: scale(0.98)
Card Hover: translateY(-4px)
Hover Lift: scale(1.02)
Default: scale(1), translateY(0)
```

---

## 🔘 Button System

### Button Sizes

```
Small (sm)
Height: 36px
Padding: 8px 16px
Font Size: 14px
Font Weight: 600

Medium (md)
Height: 44px
Padding: 12px 20px
Font Size: 14px
Font Weight: 600

Large (lg)
Height: 48px
Padding: 12px 24px
Font Size: 16px
Font Weight: 600
```

### Button States

```
Default State
Background: Gradient (Teal → Emerald)
Text Color: White
Shadow: Subtle

Hover State
Background: Darker gradient
Text Color: White
Shadow: Medium
Transform: scale(1.02)
Glow: Teal glow (20px blur)

Active/Pressed State
Transform: scale(0.98)
Shadow: Subtle
Duration: 0.1s

Disabled State
Opacity: 0.5
Cursor: not-allowed
No hover effects
```

---

## 🎯 Component Specifications

### Hero Section Card (Stats)

```
Background: rgba(248, 250, 252, 0.7)
Backdrop Filter: blur(10px)
Border: 1px solid rgba(255, 255, 255, 0.2)
Padding: 24px (lg)
Border Radius: 12px (lg)
Value Font Size: 32px (h3)
Value Font Weight: 700
Value Color: #00C7B7 (Teal)
Label Font Size: 14px (body)
Label Color: #94A3B8 (Slate-400)
```

### Feature Card

```
Background: White (#FFFFFF)
Border: 1px solid #D1D5DB (Silver)
Border Radius: 12px (lg)
Padding: 32px (xl)
Box Shadow: 0 1px 3px rgba(12, 27, 42, 0.08)

Hover State:
Border Color: #00C7B7 (Teal)
Box Shadow: 0 4px 12px rgba(12, 27, 42, 0.12)
Transform: translateY(-4px)

Icon:
Size: 48px
Font Size: 48px (emoji)

Title:
Font Size: 24px (h3)
Font Weight: 700
Color: #1F2937 (Dark Text)
Margin Bottom: 16px (md)

Description:
Font Size: 14px (body)
Color: #6B7280 (Gray-500)
Margin Bottom: 24px (lg)
Line Height: 1.5

Metric:
Font Size: 32px (h3)
Font Weight: 700
Color: #00C7B7 (Teal)

Metric Label:
Font Size: 12px (label)
Color: #9CA3AF (Gray-400)
```

### Pricing Card

```
Background: White
Border: 1px solid #E5E7EB (Gray-200)
Border Radius: 12px (lg)
Padding: 32px (xl)
Box Shadow: 0 1px 3px rgba(12, 27, 42, 0.08)

Recommended Badge:
Position: absolute top (-12px) center
Background: #00C7B7 (Teal)
Color: White
Padding: 6px 16px (sm + md)
Border Radius: 20px (full)
Font Size: 12px (label)
Font Weight: 600

Recommended Card Variant:
Background: linear-gradient(135deg, rgba(0, 199, 183, 0.1), rgba(16, 185, 129, 0.1))
Border Color: rgba(0, 199, 183, 0.5)
Transform: scale(1.05) on desktop
Box Shadow: 0 4px 12px rgba(12, 27, 42, 0.12)

Price:
Font Size: 40px
Font Weight: 700
Color: #00C7B7 (Teal)
Margin Bottom: 8px (sm)

Price Period:
Font Size: 14px
Color: #6B7280 (Gray-500)
Margin Bottom: 32px (xl)

CTA Button:
Width: 100%
Height: 44px (md)
Margin Bottom: 32px (xl)

Features List:
Item Padding: 16px (md) per item
Item Border Bottom: 1px solid #E5E7EB

Feature Checkmark:
Size: 20px
Background: #DCFCE8 (Emerald light)
Color: #059669 (Emerald)
Border Radius: 50%
```

---

## 📐 Artboard Sizes for Figma

### Hero Section

```
Desktop (1440px wide)
Width: 1440px
Height: 600px
Padding: 120px vertical, 40px horizontal

Mobile (375px wide)
Width: 375px
Height: 500px
Padding: 80px vertical, 16px horizontal
```

### Feature Grid (2x2)

```
Desktop (1440px wide)
Each card: 320px × 280px
Gap: 32px
Total height: 600px

Mobile (375px wide)
Each card: full width (343px)
Gap: 24px
Total height: stacked vertically
```

### Pricing Section (3 columns)

```
Desktop (1440px wide)
Each card: 320px × 600px (recommended 5% larger)
Gap: 32px
Total height: 650px

Mobile (375px wide)
Each card: full width (343px)
Gap: 24px
Total height: stacked vertically
```

---

## ✅ Figma Setup Checklist

- [ ] Create new Figma file: "Algo Trading Platform - Website Design"
- [ ] Set up pages: Cover, Design System, Desktop Artboards, Mobile Artboards, Components
- [ ] Add all colors to Figma color library
- [ ] Add typography styles (H1-H4, Body, Label)
- [ ] Create grid system with 12-column layout
- [ ] Set up component library with variants
- [ ] Apply shadows and effects to components
- [ ] Add animation/transition annotations
- [ ] Create mobile (375px) and desktop (1440px) artboards
- [ ] Design each section with responsive variations
- [ ] Export design tokens as JSON
- [ ] Share design with dev team via Figma link

---

## 🚀 Next Steps for Development

1. **Export Assets:**
   - Export all icons as SVG (24px, 32px, 48px)
   - Export dashboard mockup at 2x resolution
   - Export logos with transparent background

2. **Create Design Specs:**
   - Generate Figma inspection specs for developers
   - Use Figma Dev Mode for seamless handoff
   - Document all interactions and animations

3. **Implement in React:**
   - Follow component structure from FIGMA_TO_REACT_GUIDE.md
   - Install Framer Motion for animations
   - Use Tailwind CSS with design tokens
   - Test responsive behavior across all breakpoints

4. **Quality Assurance:**
   - Perform cross-browser testing
   - Test on actual mobile devices
   - Verify animations on slower devices
   - Check accessibility (WCAG 2.1 AA)

