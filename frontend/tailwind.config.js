/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        // Playful Fintech Brand Colors
        'mint-green': '#65B891',
        'off-white': '#FAFAF8', 
        'charcoal-black': '#2B2B2B',
        'coral-pink': '#FF7A6A',
        'yellow': '#FFD55A',
        'cyan': '#4ACFD9',
        // Trading specific colors
        bullish: {
          DEFAULT: "#22c55e",
          foreground: "#ffffff",
        },
        bearish: {
          DEFAULT: "#ef4444",
          foreground: "#ffffff",
        },
        neutral: {
          DEFAULT: "#64748b",
          foreground: "#ffffff",
        },
        // Cosmic theme colors
        cosmic: {
          primary: '#8b5cf6',
          secondary: '#a78bfa',
          accent: '#f59e0b',
          background: '#0c0a1a',
          surface: '#1a1530',
          text: '#e2e8f0',
          muted: '#9ca3af',
          purple: {
            100: '#f3e8ff',
            200: '#e9d5ff',
            300: '#d8b4fe',
            400: '#c084fc',
            500: '#a855f7',
            600: '#9333ea',
            700: '#7c3aed',
            800: '#6b21a8',
            900: '#581c87',
          },
          space: {
            100: '#1e1b4b',
            200: '#312e81',
            300: '#3730a3',
            400: '#4338ca',
            500: '#4f46e5',
          }
        }
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: 0 },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: 0 },
        },
        "slide-in": {
          "0%": { transform: "translateX(-100%)" },
          "100%": { transform: "translateX(0)" },
        },
        "fade-in": {
          "0%": { opacity: 0 },
          "100%": { opacity: 1 },
        },
        "pulse-green": {
          "0%, 100%": { backgroundColor: "#22c55e" },
          "50%": { backgroundColor: "#16a34a" },
        },
        "pulse-red": {
          "0%, 100%": { backgroundColor: "#ef4444" },
          "50%": { backgroundColor: "#dc2626" },
        },
        // Cosmic animations
        "cosmic-glow": {
          "0%": { boxShadow: "0 0 20px rgba(139, 92, 246, 0.3)" },
          "100%": { boxShadow: "0 0 40px rgba(139, 92, 246, 0.8)" },
        },
        "shooting-star": {
          "0%": { transform: "translateX(-100px) translateY(100px)", opacity: "0" },
          "50%": { opacity: "1" },
          "100%": { transform: "translateX(100px) translateY(-100px)", opacity: "0" },
        },
        // Playful Fintech Animations  
        "draw-line": {
          "0%": { strokeDasharray: "0 1000" },
          "100%": { strokeDasharray: "1000 0" }
        },
        "doodle-wiggle": {
          "0%, 100%": { transform: "rotate(-3deg)" },
          "50%": { transform: "rotate(3deg)" }
        },
        "doodle-bounce": {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" }
        },
        "float": {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-20px)" }
        },
        "spin-slow": {
          "from": { transform: "rotate(0deg)" },
          "to": { transform: "rotate(360deg)" }
        },
        "sparkle": {
          "0%, 100%": { opacity: "0", transform: "scale(0.5)" },
          "50%": { opacity: "1", transform: "scale(1)" }
        }
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out", 
        "slide-in": "slide-in 0.3s ease-out",
        "fade-in": "fade-in 0.3s ease-out",
        "pulse-green": "pulse-green 2s infinite",
        "pulse-red": "pulse-red 2s infinite",
        // Cosmic animations
        "cosmic-glow": "cosmic-glow 2s ease-in-out infinite alternate",
        "shooting-star": "shooting-star 3s linear infinite",
        "sparkle": "sparkle 2s ease-in-out infinite",
        "float": "float 3s ease-in-out infinite",
        "pulse-slow": "pulse 4s ease-in-out infinite",
        // Playful Fintech Animations
        "draw-line": "draw-line 2s ease-out forwards",
        "doodle-wiggle": "doodle-wiggle 1s ease-in-out infinite",
        "doodle-bounce": "doodle-bounce 2s ease-in-out infinite",
        "spin-slow": "spin-slow 8s linear infinite",
        "cosmic-glow": "cosmic-glow 3s ease-in-out infinite alternate",
        "shooting-star": "shooting-star 3s linear infinite",
        "sparkle": "sparkle 2s linear infinite",
        "float": "float 6s ease-in-out infinite",
      },
    },
  },
  plugins: [require("@tailwindcss/typography"), require("@tailwindcss/forms")],
}