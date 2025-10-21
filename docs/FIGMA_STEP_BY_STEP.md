# Complete Figma Design Walkthrough - Step by Step

## 🎯 How to Create This Design in Figma (Complete Tutorial)

This guide walks you through creating the professional Algo Trading website design in Figma from scratch.

---

## 📋 Step 1: Setup & Project Structure (15 minutes)

### 1.1 Create a New Figma File

1. Go to [figma.com](https://figma.com) and log in
2. Click "New file"
3. Name it: **"Algo Trading Platform - Website Design"**
4. Choose the Figma standard (not FigJam)

### 1.2 Set Up Pages

In the Pages panel (left sidebar), create these pages:

```
📄 Cover & Overview
📄 Design System
📄 Desktop - Full Page
📄 Mobile - Full Page
📄 Components Library
📄 Animations & Specs
📄 Dev Handoff
```

### 1.3 Configure File Settings

1. **View Settings** (top right)
   - Enable "Show pixel grid"
   - Enable "Show distance"
   - Set zoom to "Fit all"

2. **Preferences** → Rulers & Guides
   - Enable "Show rulers"
   - Set guide color to light gray

### 1.4 Create Master Frames

On **Desktop - Full Page**, create these frames:

```
Frame: "Desktop 1440" (1440 × 3200)
  ├─ Hero Section (1440 × 600)
  ├─ Trust Section (1440 × 500)
  ├─ Features Section (1440 × 700)
  ├─ Demo Section (1440 × 600)
  ├─ Testimonials Section (1440 × 500)
  ├─ Pricing Section (1440 × 800)
  └─ Footer (1440 × 400)

Frame: "Mobile 375" (375 × 4500)
  ├─ Hero Mobile (375 × 500)
  ├─ Trust Mobile (375 × 600)
  ├─ Features Mobile (375 × 900)
  ├─ Demo Mobile (375 × 400)
  ├─ Testimonials Mobile (375 × 500)
  ├─ Pricing Mobile (375 × 1200)
  └─ Footer Mobile (375 × 400)
```

---

## 🎨 Step 2: Design System Setup (20 minutes)

### 2.1 Import Colors

On the **Design System** page:

1. **Create a color palette frame** (800 × 1000)
2. **Add rectangles for each color:**

```
Rectangle 1: Navy Primary (#0C1B2A)
Rectangle 2: Teal Accent (#00C7B7)
Rectangle 3: Emerald (#10B981)
Rectangle 4: Gold (#FACC15)
Rectangle 5: Off-white (#F8FAFC)
Rectangle 6: Silver Gray (#D1D5DB)
```

3. **Save these as Figma Colors:**
   - Select each rectangle
   - Right-click → "Create component"
   - In the Design tab → Save all colors to the library

### 2.2 Add Gradients

Create 3 rectangles for gradients:

**Hero Gradient** (1440 × 300)
```
Fill: Linear gradient
Start color: #0C1B2A (Navy)
End color: #1A3A52 (Navy Light)
Angle: 135°
```

**Accent Gradient** (1440 × 300)
```
Fill: Linear gradient
Start color: #00C7B7 (Teal)
End color: #10B981 (Emerald)
Angle: 90°
```

**Save these as styles** for reuse

### 2.3 Create Typography Styles

1. **Add text frame** for each style
2. Go to **Assets** → **Typography** (right panel)

**Add Styles:**

```
Heading 1
Font: Satoshi Bold, 56px
Line Height: 1.2
Letter Spacing: -2%

Heading 2
Font: Satoshi Bold, 40px
Line Height: 1.3
Letter Spacing: -1%

Heading 3
Font: Satoshi Bold, 24px
Line Height: 1.3

Body Large
Font: Inter Regular, 16px
Line Height: 1.5

Body Regular
Font: Inter Regular, 14px
Line Height: 1.5

Caption
Font: Inter Semibold, 12px
Text Transform: Uppercase
```

### 2.4 Add Shadow Styles

In the **Design** panel on the right:

```
Shadow 1 - Subtle
X: 0, Y: 1, Blur: 3, Spread: 0
Color: rgba(12, 27, 42, 0.08)

Shadow 2 - Medium
X: 0, Y: 4, Blur: 12, Spread: 0
Color: rgba(12, 27, 42, 0.12)

Glow - Teal
X: 0, Y: 0, Blur: 20, Spread: 0
Color: rgba(0, 199, 183, 0.3)
```

---

## 🧩 Step 3: Create Reusable Components (45 minutes)

### 3.1 Button Component

On the **Components Library** page:

1. **Create a rectangle** (200 × 48)
2. Add:
   - Background color: Teal gradient
   - Border radius: 8px
   - Text: "Start Free Trial" (white, Poppins Bold)
   - Padding: 12px horizontal, 8px vertical

3. **Convert to component:**
   - Right-click → "Create component"
   - Name: `Button/Primary/Default`

4. **Create variants:**
   - Duplicate 2 times
   - Rename: `Button/Primary/Hover` and `Button/Primary/Active`
   - Adjust background color and shadow

5. **Create Secondary button variant:**
   - Outline style with Teal border
   - Transparent background
   - Name: `Button/Secondary/Default`

### 3.2 Feature Card Component

1. **Create a rectangle** (320 × 280)
   - Background: White
   - Border: 1px #D1D5DB
   - Corner radius: 12px
   - Padding: 32px

2. **Add child elements:**
   - Icon text: 48px emoji
   - Title: "Live Algo Dashboard" (Heading 3)
   - Description: "Monitor real-time..." (Body Regular)
   - Metric: "$2.4M" (Heading 3, Teal)
   - Link: "Learn more →" (14px, Teal)

3. **Convert to component:**
   - Name: `Card/Feature/Default`

4. **Create variants:**
   - Hover: Add Shadow 2, lift it up 4px
   - Active: Darker border

### 3.3 Pricing Card Component

1. **Create a rectangle** (320 × 600)
   - Background: White
   - Border: 1px #D1D5DB
   - Corner radius: 12px
   - Padding: 32px

2. **Add child elements:**
   - Plan name: "Pro" (Heading 3)
   - Price: "$199" (40px bold, Teal)
   - Price period: "/month" (Body Regular)
   - Feature list: 12 items
   - CTA button: Full width

3. **Convert to component:**
   - Name: `Card/Pricing/Default`

4. **Create variants:**
   - Recommended: Gradient background, scale 1.05

### 3.4 Testimonial Card Component

1. **Create a rectangle** (320 × 200)
   - Background: White
   - Border: 1px #D1D5DB
   - Corner radius: 12px

2. **Add elements:**
   - Quote: Body Regular, italic
   - Avatar: 48px circle with placeholder
   - Name: 14px bold
   - Role: 12px gray
   - Star rating: 5 stars (⭐)

3. **Convert to component:**
   - Name: `Card/Testimonial/Default`

### 3.5 Icon Badge Component

1. **Create a circle** (48 × 48)
   - Background: Teal with opacity 0.1
   - Add text/icon inside: 32px

2. **Convert to component:**
   - Name: `Badge/Icon/Default`

3. **Create color variants:**
   - Teal, Emerald, Gold, Navy

---

## 🏗️ Step 4: Design Hero Section (20 minutes)

### 4.1 Setup Hero Frame

On **Desktop - Full Page**, select the "Hero Section (1440 × 600)" frame:

1. Add background gradient:
   - Linear gradient: #0C1B2A → #1A3A52 at 135°

2. **Add elements:**

**Headline (Centered)**
```
Text: "Smarter Trading, Powered by Algorithms You Control."
Style: Heading 1
Color: White
Position: Center top, Y: 80px
Width: 1000px max
```

**Subheadline**
```
Text: "Automate your stock and crypto trades with institutional-grade AI tools built for retail investors."
Style: Body Large
Color: Slate-300 (#cbd5e1)
Position: Center, Y: 180px
Width: 800px max
```

**CTA Button Group**
```
Button 1: "Start Free Trial →"
- Component: Button/Primary/Default
- Position: Center, Y: 280px
- Margin right: 16px

Button 2: "Book Demo"
- Component: Button/Secondary/Default
- Position: Right of Button 1
```

**Key Stats Grid (2×2)**
```
Create frame: Stats (1000 × 200)
Add 4 cards:
- Each 200 × 100
- Gap: 32px between
- Background: rgba(248, 250, 252, 0.7) with blur
- Text: Large number (Teal) + label

Cards:
1. "$5.2B" + "Total Volume"
2. "50K+" + "Active Traders"
3. "99.99%" + "Uptime"
4. "24/7" + "Support"
```

**Positioning:**
```
Y: 380px
Center aligned
```

### 4.2 Add Visual Effects

1. **Background effect:**
   - Add an ellipse: 400 × 400, #00C7B7, opacity 0.1
   - Blur: 120px
   - Position: top-left corner

2. **Data particles (optional):**
   - Add small circles/dots with animation
   - Opacity 0.3, scattered around

---

## 📋 Step 5: Design Trust Section (15 minutes)

### 5.1 Section Setup

Create frame: "Trust Section (1440 × 500)"
- Background: #F8FAFC

### 5.2 Add Content

1. **Headline:**
```
Text: "Why Choose AlgoProject?"
Style: Heading 2
Color: Navy (#0C1B2A)
Position: Center, Y: 60px
```

2. **3-Column Layout:**

**Column 1 (330 × 250):**
```
Icon: ⚙️ (48px)
Title: "Proven Algorithms"
Description: "Backtested and optimized for real market conditions."
```

**Column 2 (330 × 250):**
```
Icon: 🔒 (48px)
Title: "Enterprise Security"
Description: "Bank-level encryption for peace of mind."
```

**Column 3 (330 × 250):**
```
Icon: 🤝 (48px)
Title: "Trusted by Traders"
Description: "Thousands of active users worldwide."
```

Layout:
```
Gap between columns: 32px
Vertical position: Y: 150px
Each column has:
- Icon at top (48px)
- Title below (Heading 4, Navy)
- Description (Body, Gray)
```

3. **Logo Strip (Exchange partners):**
```
Position: Y: 400px
Center aligned
Logos: Binance, Zerodha, Coinbase, etc.
Size: 40px height each
Gap: 32px between
Opacity: 0.6
```

---

## 💡 Step 6: Design Features Section (25 minutes)

### 6.1 Section Setup

Create frame: "Features Section (1440 × 700)"
- Background: #F8FAFC

### 6.2 Add Content

1. **Headline:**
```
Text: "Powerful Tools for Modern Traders"
Style: Heading 2
Position: Center, Y: 60px
```

2. **2×2 Grid (1200 × 600):**

**Feature 1 - Live Algo Dashboard**
```
Component: Card/Feature
Icon: 📊
Title: "Live Algo Dashboard"
Description: "Monitor real-time performance, profit & loss, and execution stats."
Metric: "$2.4M"
Metric Label: "in trades executed"
Position: Top-left
```

**Feature 2 - Strategy Builder**
```
Component: Card/Feature
Icon: ⚙️
Title: "No-Code Strategy Builder"
Description: "Create sophisticated trading strategies without writing code."
Metric: "1000+"
Metric Label: "strategies deployed"
Position: Top-right
```

**Feature 3 - Real-time Insights**
```
Component: Card/Feature
Icon: 📈
Title: "Real-time Market Insights"
Description: "AI-powered market analysis with actionable alerts."
Metric: "24/7"
Metric Label: "market monitoring"
Position: Bottom-left
```

**Feature 4 - Automated Execution**
```
Component: Card/Feature
Icon: ⚡
Title: "24/7 Automated Execution"
Description: "Your algorithms trade while you sleep, worldwide markets covered."
Metric: "<1ms"
Metric Label: "execution latency"
Position: Bottom-right
```

Layout:
```
Grid spacing: 32px
Center the entire 2×2 grid
Position: Y: 150px
```

---

## 🎬 Step 7: Design Demo Section (15 minutes)

### 7.1 Section Setup

Create frame: "Demo Section (1440 × 600)"
- Background: Gradient #0C1B2A → #142038

### 7.2 Add Content

1. **Headline:**
```
Text: "See It In Action"
Style: Heading 2
Color: White
Position: Center top, Y: 60px
```

2. **Dashboard Mockup:**
```
Create rectangle: 800 × 400
Background: #1F2937 (dark gray)
Border: 1px #374151 (outline)
Corner radius: 12px
Position: Center, Y: 150px

Inside mockup, add grid pattern:
- Columns, data cells
- Use placeholder lines with different gray shades
```

3. **Overlay Text:**
```
Position: Bottom-left of dashboard
Background: rgba(12, 27, 42, 0.8)
Padding: 24px
Corner radius: 8px
Text: "Build, backtest, and deploy your strategy in minutes."
Style: Body Large, White
```

4. **CTA Button:**
```
Component: Button/Primary
Text: "Explore Platform"
Position: Bottom-center, Y: 520px
```

---

## 💬 Step 8: Design Testimonials Section (20 minutes)

### 8.1 Section Setup

Create frame: "Testimonials Section (1440 × 500)"
- Background: #F8FAFC

### 8.2 Add Content

1. **Headline:**
```
Text: "Trusted by Traders Worldwide"
Style: Heading 2
Position: Center top, Y: 60px
```

2. **Testimonial Slider:**

Create 3 testimonial cards (320 × 200 each):

**Card 1:**
```
Quote: "AlgoTrading has transformed my portfolio. The backtesting tools are incredibly accurate and the automation has saved me hours."
Avatar: Placeholder circle 48px
Name: "Arjun Sharma"
Role: "Independent Trader, Mumbai"
Rating: ⭐⭐⭐⭐⭐
```

**Card 2:**
```
Quote: "Finally, institutional-grade tools available to retail investors. The performance metrics alone make it worth it."
Avatar: Placeholder circle 48px
Name: "Priya Singh"
Role: "Portfolio Manager, Delhi"
Rating: ⭐⭐⭐⭐⭐
```

**Card 3:**
```
Quote: "Secure, reliable, and intuitive. I trust this platform with my investments without hesitation."
Avatar: Placeholder circle 48px
Name: "Vikram Kumar"
Role: "Crypto Enthusiast, Bangalore"
Rating: ⭐⭐⭐⭐⭐
```

3. **Carousel Controls:**
```
Position arrows at left/right
Position dots at bottom
Dots: 3 circles, gap 8px
Selected dot color: Teal
Unselected dot color: Gray
```

Layout:
```
Cards center aligned: Y: 150px
Gap between visible cards: 32px
Arrows: outside the cards
Dots: Y: 420px, centered
```

---

## 💰 Step 9: Design Pricing Section (30 minutes)

### 9.1 Section Setup

Create frame: "Pricing Section (1440 × 800)"
- Background: #F8FAFC

### 9.2 Add Content

1. **Headline:**
```
Text: "Simple, Transparent Pricing"
Style: Heading 2
Position: Center top, Y: 60px
```

2. **3-Column Pricing Grid:**

**Card 1: Starter** (320 × 650)
```
Component: Card/Pricing/Default variant
Plan name: "Starter"
Price: "$49"
Period: "/month"
Features: [List of 12 features]
Button: "Get Started"
Position: Left column
```

**Card 2: Pro (Recommended)** (320 × 650)
```
Component: Card/Pricing/Recommended variant
Badge: "Most Popular" (top center)
Plan name: "Pro"
Price: "$199"
Period: "/month"
Features: [List of 12 features]
Button: "Start Free Trial"
Background: Teal gradient with opacity
Scale: 1.05 (appears slightly larger)
Position: Center column (scaled up)
Z-index: Higher
```

**Card 3: Institutional** (320 × 650)
```
Component: Card/Pricing/Default variant
Plan name: "Institutional"
Price: "Contact Sales"
Period: ""
Features: [List of 12 features]
Button: "Book Demo"
Position: Right column
```

Layout:
```
Cards position: Y: 150px
Gap: 32px between cards
Center: Recommenced card is 5% larger
All cards flex: center alignment
```

3. **Feature Comparison (Optional):**
```
Add small text below pricing cards:
"See detailed comparison" (link in Teal)
```

---

## 🔗 Step 10: Design Footer (15 minutes)

### 10.1 Section Setup

Create frame: "Footer (1440 × 400)"
- Background: #0C1B2A (Navy)

### 10.2 Add Content

1. **4-Column Layout:**

**Column 1 - Company** (280 × 300):
```
Logo: 40px height (placeholder)
Description: "Smart trading for everyone." (12px, gray)
Social icons: LinkedIn, X, GitHub (24px)
Gap: 16px between icons
Spacing: Each icon as separate element
```

**Column 2 - Legal** (280 × 300):
```
Heading: "Legal" (Heading 4, white)
Links:
- Terms of Service
- Privacy Policy
- Cookie Policy
- Compliance
- SEBI Registration

Text: 12px, gray
Color on hover: Teal
```

**Column 3 - Resources** (280 × 300):
```
Heading: "Resources" (Heading 4, white)
Links:
- Documentation
- API Reference
- Community Forum
- Blog
- Help Center

Text: 12px, gray
```

**Column 4 - Contact** (280 × 300):
```
Heading: "Contact" (Heading 4, white)
Info:
- Email: hello@algotrading.com
- Phone: +91 80000 00000
- Address: India
- Newsletter signup input

Text: 12px, gray
Input field: white bg, gray border
```

2. **Bottom Bar:**
```
Position: Y: 320px
Border-top: 1px solid rgba(0, 199, 183, 0.2)
Padding-top: 24px

Left: Copyright text (12px, gray)
Center: Compliance badge
Right: Security icons

Copyright: "© 2025 AlgoTrading. All rights reserved."
Compliance: "Registered & compliant with SEBI standards."
```

Layout:
```
4 columns: 280px each
Gap: 48px
Horizontal padding: 40px
Vertical padding: 60px top/bottom
```

---

## 📱 Step 11: Create Mobile Versions (60 minutes)

### 11.1 Mobile Frame Setup

On **Mobile - Full Page**, create a master frame:
- Frame size: 375 × 4500
- Background: #F8FAFC

### 11.2 Adapt Each Section for Mobile

**Mobile Hero (375 × 500):**
```
Headline: Same, but 32px (from 56px)
Subheadline: 18px (from 20px)
Buttons: Stack vertically, full width
Gap: 12px between stacked buttons
Stats grid: 2×2 instead of 4×1
Padding: 16px (from 40px)
Y spacing: 40px vertical (from 80px)
```

**Mobile Trust (375 × 600):**
```
Cards: Stack vertically
Icon size: 40px (from 48px)
Width: Full width with 16px margin
Gap: 24px (from 32px)
Logo strip: Horizontal scroll or 2×3 grid
Logo size: 32px height
```

**Mobile Features (375 × 900):**
```
Cards: Stack vertically
Card width: Full width (343px) with 16px margin
Gap: 20px
Grid: 1×4 instead of 2×2
Font sizes: Slightly reduced
```

**Mobile Testimonials (375 × 500):**
```
Cards: Single column
Width: Full width
Height: Auto content
Scroll horizontally with pagination
```

**Mobile Pricing (375 × 1200):**
```
Cards: Stack vertically
Width: Full width (343px)
Recommended card: No scale, same size
Gap: 20px
```

**Mobile Footer (375 × 400):**
```
Columns: Stack vertically
Width: Full width
Text: Center aligned
Links: Full width tap targets (44px min height)
Gap: 32px between columns
```

---

## 🎬 Step 12: Add Animations & Interactions (45 minutes)

### 12.1 Add Animation Annotations

For each section, add a text layer with animation specs:

**Hero Section Animation:**
```
Headline: Fade in + Slide up
Duration: 0.8s
Delay: 0s
Easing: ease-out

Subheadline: Fade in + Slide up
Duration: 0.8s
Delay: 0.1s

Buttons: Fade in
Duration: 0.6s
Delay: 0.2s

Stats grid: Fade in + Stagger
Duration: 0.5s
Delay: 0.3s (staggered 100ms per item)
```

**Feature Cards Hover:**
```
On Hover:
- Lift: translateY(-4px)
- Shadow: Increase to medium shadow
- Duration: 0.3s
- Easing: ease-out
- Border color: Change to Teal
```

**Button Interactions:**
```
Button Hover:
- Background: Shift darker
- Shadow: Increase
- Duration: 0.3s

Button Click:
- Scale: 0.98
- Duration: 0.1s (press effect)
```

### 12.2 Add Component Prototypes

1. Select a button component
2. Go to **Prototype** tab (right panel)
3. Add interaction:
   ```
   Trigger: On click
   Action: Navigate to URL
   Destination: (your app URL)
   Animation: Slide right or Fade
   ```

---

## ✅ Step 13: Final Touches & Export (30 minutes)

### 13.1 Visual Polish

1. **Check all colors:**
   - Use color library consistently
   - Verify contrast ratios (WCAG AA minimum)

2. **Typography verification:**
   - All text uses defined styles
   - Line heights are consistent
   - Font weights are correct

3. **Spacing audit:**
   - Use the 8px grid consistently
   - Verify all padding/margins use scale
   - Check alignment with guides

4. **Shadow & effects:**
   - Apply shadows to cards
   - Add subtle blur effects
   - Verify glow effects on CTAs

### 13.2 Export Assets

1. **Export individual components:**
   - Select each component
   - Right-click → Export
   - Format: SVG (for icons), PNG (for mockups)
   - Scale: 2x for retina quality

2. **Export color tokens:**
   - Save as JSON or CSS
   - Include RGB, Hex, HSL values

3. **Export typography:**
   - Document all font families, sizes, weights
   - Export as design tokens

### 13.3 Create Handoff Documentation

1. Add a **"Dev Handoff"** page with:
   - Component list
   - Animation specs
   - Breakpoint documentation
   - Interaction guide

2. Use Figma's **Dev Mode** for better developer experience:
   - Turn on in top-right menu
   - Generates code snippets
   - Provides measurement tools

### 13.4 Share with Team

1. **Set permissions:**
   - Share link or invite team members
   - Set to "View only" for stakeholders
   - "Edit" access for designers

2. **Create a Figma component library:**
   - Publish components
   - Version control for updates

3. **Document design decisions:**
   - Create a design spec PDF
   - Include rationale for choices
   - Link to this guide

---

## 🚀 Next Steps After Design

1. **Review with team:**
   - Gather feedback on design
   - Iterate on color/typography if needed
   - Validate responsive behavior

2. **Prepare for development:**
   - Create component specs
   - Export all assets
   - Generate CSS design tokens

3. **Hand off to developers:**
   - Share Figma file link
   - Provide design tokens
   - Document interactions
   - Use Figma Dev Mode

4. **Implement in React:**
   - Follow FIGMA_TO_REACT_GUIDE.md
   - Use design tokens in code
   - Install Framer Motion for animations
   - Test all breakpoints

---

## 📊 Design Checklist

- [ ] File structure created (pages, frames, artboards)
- [ ] Design system set up (colors, typography, shadows)
- [ ] Components created and saved to library
- [ ] Hero section designed (desktop + mobile)
- [ ] Trust section designed (desktop + mobile)
- [ ] Features section designed (desktop + mobile)
- [ ] Demo section designed (desktop + mobile)
- [ ] Testimonials section designed (desktop + mobile)
- [ ] Pricing section designed (desktop + mobile)
- [ ] Footer designed (desktop + mobile)
- [ ] Animations and interactions documented
- [ ] All components have hover states
- [ ] Mobile responsive versions complete
- [ ] Assets exported and organized
- [ ] Design tokens created and exported
- [ ] Documentation written
- [ ] Design shared with development team
- [ ] Feedback incorporated
- [ ] Ready for implementation

---

## 💡 Pro Tips for Figma Design

1. **Use components for everything:**
   - Buttons, cards, headers, footers
   - Makes updates quick and consistent

2. **Name layers consistently:**
   - Use clear naming convention
   - Helps developers find elements

3. **Use guides & grids:**
   - Snap to grid for perfect alignment
   - Use guides for consistent spacing

4. **Color & typography styles:**
   - Central library makes updates easy
   - Automatic consistency

5. **Create variants:**
   - Hover, active, disabled states
   - Light/dark theme variants

6. **Document everything:**
   - Leave comments on complex interactions
   - Explain design decisions

7. **Test on actual devices:**
   - Use Figma Mirror for mobile preview
   - Verify responsive behavior

8. **Keep file organized:**
   - Archive completed pages
   - Use folders for component library
   - Regular cleanup

---

## 🎓 Resources

- **Figma Learning:** https://help.figma.com/
- **Design System Guide:** https://www.designsystems.com/
- **Accessibility:** https://www.w3.org/WAI/WCAG21/quickref/
- **Animation Easing:** https://easings.net/
- **Color Contrast:** https://webaim.org/resources/contrastchecker/

