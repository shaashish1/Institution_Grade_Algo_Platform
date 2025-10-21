'use client';

import React, { useState, useEffect } from 'react';

// AlgoBot Component - A customizable mascot character
interface AlgoBotProps {
    expression?: 'happy' | 'thinking' | 'confused' | 'excited';
    size?: 'small' | 'medium' | 'large';
    accessories?: string[];
}

export function AlgoBot({ expression = 'happy', size = 'medium', accessories = [] }: AlgoBotProps) {
    const sizeClasses = {
        small: 'w-16 h-16',
        medium: 'w-24 h-24',
        large: 'w-32 h-32',
    };
    
    const expressionMap = {
        happy: '😊',
        thinking: '🤔',
        confused: '😕',
        excited: '😃',
    };
    
    const accessoryEmojis: Record<string, string> = {
        coffee: '☕',
        rocket: '🚀',
        hat: '🎩',
        glasses: '👓',
        book: '📚',
        laptop: '💻',
    };

    return (
        <div className={`${sizeClasses[size]} flex flex-col items-center justify-center`}>
            <div className="relative bg-gradient-to-br from-blue-400 to-cyan-300 rounded-full flex items-center justify-center shadow-lg">
                <div className="absolute inset-0 rounded-full border-4 border-charcoal-black"></div>
                <span className="text-3xl">{expressionMap[expression]}</span>
                <div className="absolute -top-4 -right-2 flex space-x-1">
                    {accessories.map((accessory, index) => (
                        <span key={index} className="text-lg">
                            {accessoryEmojis[accessory] || ''}
                        </span>
                    ))}
                </div>
            </div>
        </div>
    );
}

// Pricing Card Component
interface PlayfulPricingCardProps {
    plan: string;
    price: string;
    badge?: string;
    isPopular?: boolean;
    features: string[];
}

export function PlayfulPricingCard({ 
    plan, 
    price, 
    badge, 
    isPopular = false,
    features 
}: PlayfulPricingCardProps) {
    return (
        <div className={`
            bg-white/10 backdrop-blur-md rounded-3xl border-2 
            ${isPopular ? 'border-emerald-400 shadow-lg shadow-emerald-400/20' : 'border-white/20'} 
            p-8 relative overflow-hidden transition-all duration-300 hover:scale-105
        `}>
            <div className="absolute inset-0 opacity-5">
                <div className="absolute top-4 left-4 text-2xl">📈</div>
                <div className="absolute bottom-4 right-4 text-2xl">💰</div>
            </div>
            
            {badge && (
                <div className="absolute top-6 right-6">
                    <span className={`
                        inline-flex px-3 py-1 rounded-full text-xs font-semibold
                        ${isPopular ? 'bg-emerald-400 text-emerald-900' : 'bg-white/20 text-white'}
                    `}>
                        {badge}
                    </span>
                </div>
            )}

            <div className="relative z-10">
                <h3 className="text-2xl font-bold text-white mb-2" style={{ fontFamily: 'Comic Neue, cursive' }}>
                    {plan}
                </h3>
                
                <div className="flex items-end mb-6">
                    <span className="text-4xl font-bold text-white" style={{ fontFamily: 'Comic Neue, cursive' }}>
                        {price}
                    </span>
                    <span className="text-white/70 ml-1">/month</span>
                </div>
                
                <div className="h-px bg-white/20 w-full my-6"></div>
                
                <ul className="space-y-3 mb-8">
                    {features.map((feature, index) => (
                        <li key={index} className="flex items-start">
                            <span className="text-emerald-400 mr-2">✓</span>
                            <span className="text-white/80">{feature}</span>
                        </li>
                    ))}
                </ul>
                
                <button className={`
                    w-full py-3 rounded-xl font-bold transition-all duration-300
                    ${isPopular ? 
                        'bg-gradient-to-r from-emerald-400 to-cyan-400 text-white hover:shadow-lg hover:shadow-emerald-400/20' : 
                        'bg-white/10 text-white border border-white/20 hover:bg-white/20'}
                `} style={{ fontFamily: 'Comic Neue, cursive' }}>
                    Choose Plan
                </button>
            </div>
        </div>
    );
}

// Hero Section Component
export function DoodleHeroSection() {
    return (
        <section className="relative min-h-screen flex items-center overflow-hidden">
            <div className="absolute inset-0">
                <div className="absolute inset-0 bg-gradient-to-b from-blue-950 via-purple-900 to-charcoal-black"></div>
                <div className="absolute inset-0 opacity-10" style={{
                    backgroundImage: 'radial-gradient(circle at center, #fff 0.5px, transparent 0)',
                    backgroundSize: '24px 24px'
                }}></div>
            </div>

            {['📊', '📈', '🤖', '💰', '📱', '⚙️', '🔍', '🧠'].map((emoji, i) => (
                <div
                    key={i}
                    className="absolute text-3xl animate-float opacity-50"
                    style={{
                        left: `${10 + (i * 10)}%`,
                        top: `${Math.random() * 70}%`,
                        animationDelay: `${i * 0.5}s`,
                        animationDuration: `${4 + Math.random() * 3}s`
                    }}
                >
                    {emoji}
                </div>
            ))}

            <div className="container mx-auto px-6 relative z-10">
                <div className="flex flex-col md:flex-row items-center">
                    <div className="w-full md:w-1/2 text-center md:text-left">
                        <div className="inline-flex items-center gap-2 mb-6 bg-white/10 backdrop-blur-md px-4 py-2 rounded-full">
                            <span className="animate-pulse h-3 w-3 rounded-full bg-green-400"></span>
                            <span className="text-sm font-medium text-white/90">AI-Powered Trading Platform</span>
                        </div>
                        
                        <h1 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-white via-blue-100 to-purple-100 bg-clip-text text-transparent mb-6" style={{ fontFamily: 'Comic Neue, cursive' }}>
                            Trade Smarter <br />
                            <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
                                with AlgoBot
                            </span>
                        </h1>
                        
                        <p className="text-xl text-white/70 mb-8" style={{ fontFamily: 'Poppins, sans-serif' }}>
                            Revolutionize your trading experience with our AI-powered platform that combines algorithmic strategies with intuitive design.
                        </p>
                        
                        <div className="flex flex-col sm:flex-row gap-6 justify-center md:justify-start">
                            <button className="group relative bg-gradient-to-r from-emerald-500 to-cyan-500 text-white px-10 py-4 rounded-2xl text-lg font-bold overflow-hidden transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-emerald-500/25" style={{ fontFamily: 'Comic Neue, cursive' }}>
                                <span className="relative z-10 flex items-center gap-2">
                                    Get Started Free
                                    <span className="group-hover:translate-x-1 transition-transform">→</span>
                                </span>
                            </button>
                            
                            <button className="bg-white/10 backdrop-blur-md border-2 border-white/30 text-white px-10 py-4 rounded-2xl text-lg font-bold hover:bg-white/20 transition-all duration-300" style={{ fontFamily: 'Comic Neue, cursive' }}>
                                Watch Demo
                            </button>
                        </div>
                    </div>
                    
                    <div className="w-full md:w-1/2 mt-12 md:mt-0">
                        <div className="relative">
                            <div className="absolute -top-10 -left-10 w-20 h-20 text-4xl animate-spin-slow">✨</div>
                            <div className="absolute -bottom-5 -right-5 w-16 h-16 text-3xl animate-bounce">🚀</div>
                            
                            <div className="bg-gradient-to-br from-purple-600/30 to-blue-600/30 backdrop-blur-md border-2 border-white/20 rounded-3xl overflow-hidden shadow-2xl">
                                <div className="aspect-[4/3] relative">
                                    <div className="absolute inset-0 flex items-center justify-center">
                                        <div className="text-6xl">📊</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}

// Features Section Component
export function ModernFeaturesSection() {
    const features = [
        {
            title: "AI Trading Algorithms",
            description: "Our advanced algorithms analyze market patterns and execute trades with precision.",
            icon: "🤖"
        },
        {
            title: "Real-time Analytics",
            description: "Track your portfolio performance with beautiful, real-time visualizations.",
            icon: "📊"
        },
        {
            title: "Secure & Compliant",
            description: "Bank-grade encryption and regulatory compliance keep your investments safe.",
            icon: "🔒"
        },
        {
            title: "Multi-platform Support",
            description: "Trade on any device with our seamless cross-platform experience.",
            icon: "📱"
        },
        {
            title: "Learning Resources",
            description: "Improve your trading skills with our educational content and tutorials.",
            icon: "📚"
        },
        {
            title: "24/7 Support",
            description: "Our support team is always available to help you navigate your trading journey.",
            icon: "💬"
        }
    ];

    return (
        <section className="py-24 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-b from-charcoal-black via-indigo-950/50 to-charcoal-black"></div>
            
            <div className="relative max-w-7xl mx-auto px-6">
                <div className="text-center mb-20">
                    <div className="inline-flex items-center gap-2 mb-6 bg-white/10 backdrop-blur-md px-4 py-2 rounded-full border border-white/20">
                        <span className="text-sm font-medium text-white/90">✨ Features</span>
                    </div>
                    
                    <h2 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-white via-blue-100 to-purple-100 bg-clip-text text-transparent mb-6" style={{ fontFamily: 'Comic Neue, cursive' }}>
                        Trading
                        <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
                            {" "}Superpowers
                        </span>
                    </h2>
                    
                    <p className="text-xl text-white/70 max-w-3xl mx-auto" style={{ fontFamily: 'Poppins, sans-serif' }}>
                        Discover the tools and features that will transform your trading experience and help you achieve your financial goals.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {features.map((feature, index) => (
                        <div 
                            key={index}
                            className="bg-white/5 backdrop-blur-md border border-white/10 rounded-3xl p-8 transition-all duration-300 hover:bg-white/10 hover:scale-105 hover:shadow-xl"
                        >
                            <div className="mb-6 text-4xl">{feature.icon}</div>
                            <h3 className="text-2xl font-bold text-white mb-4" style={{ fontFamily: 'Comic Neue, cursive' }}>
                                {feature.title}
                            </h3>
                            <p className="text-white/70" style={{ fontFamily: 'Poppins, sans-serif' }}>
                                {feature.description}
                            </p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}

// Community Section Component
export function CommunitySection() {
    const testimonials = [
        {
            quote: "This platform completely changed how I approach trading. The AI suggestions are incredibly accurate!",
            author: "Sarah M.",
            role: "Day Trader",
            avatar: "👩‍💼"
        },
        {
            quote: "As someone new to trading, the educational resources and intuitive interface made it easy to get started.",
            author: "James L.",
            role: "Beginner Investor",
            avatar: "👨‍🦱"
        },
        {
            quote: "The real-time analytics have helped me optimize my portfolio and increase my returns by 27%.",
            author: "Michael R.",
            role: "Portfolio Manager",
            avatar: "👨‍💼"
        }
    ];

    return (
        <section className="py-24 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-b from-transparent via-purple-900/20 to-transparent"></div>
            
            <div className="relative max-w-7xl mx-auto px-6">
                <div className="text-center mb-20">
                    <div className="inline-flex items-center gap-2 mb-6 bg-white/10 backdrop-blur-md px-4 py-2 rounded-full border border-white/20">
                        <span className="text-sm font-medium text-white/90">👥 Community</span>
                    </div>
                    
                    <h2 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-white via-blue-100 to-purple-100 bg-clip-text text-transparent mb-6" style={{ fontFamily: 'Comic Neue, cursive' }}>
                        Join Our
                        <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
                            {" "}Trading Family
                        </span>
                    </h2>
                    
                    <p className="text-xl text-white/70 max-w-3xl mx-auto" style={{ fontFamily: 'Poppins, sans-serif' }}>
                        Connect with traders from around the world who are achieving their financial goals with our platform.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
                    {testimonials.map((testimonial, index) => (
                        <div
                            key={index}
                            className="bg-white/5 backdrop-blur-md border border-white/10 rounded-3xl p-8 transition-all duration-300 hover:bg-white/10 hover:scale-105"
                        >
                            <div className="text-4xl mb-6">{testimonial.avatar}</div>
                            <p className="italic text-white/80 mb-6" style={{ fontFamily: 'Poppins, sans-serif' }}>
                                "{testimonial.quote}"
                            </p>
                            <div>
                                <p className="font-bold text-white" style={{ fontFamily: 'Comic Neue, cursive' }}>{testimonial.author}</p>
                                <p className="text-white/60 text-sm">{testimonial.role}</p>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
                    {[
                        { value: "10k+", label: "Active Users" },
                        { value: "$2.5M+", label: "Trading Volume" },
                        { value: "97%", label: "Success Rate" },
                        { value: "24/7", label: "Community Support" }
                    ].map((stat, index) => (
                        <div key={index} className="text-center">
                            <p className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent mb-2" style={{ fontFamily: 'Comic Neue, cursive' }}>
                                {stat.value}
                            </p>
                            <p className="text-white/70">{stat.label}</p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}

interface DoodleShowcaseProps {
  isActive?: boolean;
}

export function DoodleShowcase({ isActive = true }: DoodleShowcaseProps) {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  if (!isActive) return null;

  return (
    <div className="min-h-screen w-full overflow-x-hidden">
      {/* Floating AlgoBot that follows scroll */}
      <div 
        className="fixed bottom-8 right-8 z-50 transition-transform duration-300 hover:scale-110"
        style={{ transform: `translateY(${scrollY * 0.1}px)` }}
      >
        <AlgoBot expression="happy" size="medium" accessories={['coffee']} />
      </div>

      {/* Main Showcase Content */}
      <div className="w-full">
        {/* Hero Section */}
        <DoodleHeroSection />

        {/* Features Section */}
        <ModernFeaturesSection />

        {/* Community Section */}
        <CommunitySection />

        {/* Pricing Section */}
        <section className="py-24 relative overflow-hidden">
          {/* Background Elements */}
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-emerald-900/10 to-transparent"></div>
          
          <div className="relative max-w-7xl mx-auto px-6">
            <div className="text-center mb-20">
              <div className="inline-flex items-center gap-2 mb-6 bg-white/10 backdrop-blur-md px-4 py-2 rounded-full border border-white/20">
                <span className="text-sm font-medium text-white/90">💰 Pricing Plans</span>
              </div>
              
              <h2 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-white via-blue-100 to-purple-100 bg-clip-text text-transparent mb-6" style={{ fontFamily: 'Comic Neue, cursive' }}>
                Choose Your
                <br />
                <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
                  Trading Plan
                </span>
              </h2>
              
              <p className="text-xl text-white/70 max-w-3xl mx-auto" style={{ fontFamily: 'Poppins, sans-serif' }}>
                Start your trading journey with our flexible plans designed for every skill level and budget.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
              <PlayfulPricingCard
                plan="Starter"
                price="$29"
                badge="Perfect for Beginners"
                features={[
                  "5 AI Trading Strategies",
                  "Basic Market Analytics",
                  "Mobile App Access",
                  "Email Support",
                  "Educational Resources"
                ]}
              />
              <PlayfulPricingCard
                plan="Professional"
                price="$79"
                badge="Most Popular"
                isPopular={true}
                features={[
                  "20+ AI Trading Strategies",
                  "Advanced Analytics & Charts",
                  "Real-time Market Data",
                  "Portfolio Risk Management",
                  "Priority Support",
                  "Custom Indicators"
                ]}
              />
              <PlayfulPricingCard
                plan="Enterprise"
                price="$199"
                badge="For Trading Firms"
                features={[
                  "Unlimited Strategies",
                  "Institutional APIs",
                  "Advanced Risk Controls",
                  "Multi-Account Management",
                  "Dedicated Account Manager",
                  "24/7 Phone Support"
                ]}
              />
            </div>
          </div>
        </section>

        {/* Final CTA Section */}
        <section className="py-24 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-indigo-900/20 via-purple-900/20 to-pink-900/20"></div>
          
          <div className="relative max-w-4xl mx-auto px-6 text-center">
            <h2 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-white via-blue-100 to-purple-100 bg-clip-text text-transparent mb-6" style={{ fontFamily: 'Comic Neue, cursive' }}>
              Ready to Start Trading?
            </h2>
            <p className="text-xl text-white/70 mb-12 max-w-2xl mx-auto" style={{ fontFamily: 'Poppins, sans-serif' }}>
              Join thousands of successful traders who've transformed their financial future with our AI-powered platform.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center mb-16">
              <button className="group relative bg-gradient-to-r from-emerald-500 to-cyan-500 text-white px-10 py-4 rounded-2xl text-lg font-bold overflow-hidden transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-emerald-500/25" style={{ fontFamily: 'Comic Neue, cursive' }}>
                <span className="relative z-10 flex items-center gap-2">
                  Start Free Trial
                  <span className="group-hover:translate-x-1 transition-transform">→</span>
                </span>
              </button>
              
              <button className="bg-white/10 backdrop-blur-md border-2 border-white/30 text-white px-10 py-4 rounded-2xl text-lg font-bold hover:bg-white/20 hover:border-white/50 transition-all duration-300 hover:scale-105" style={{ fontFamily: 'Comic Neue, cursive' }}>
                <span className="flex items-center gap-2">
                  <span className="text-xl">📞</span>
                  Schedule Demo
                </span>
              </button>
            </div>
            
            {/* Trust indicators */}
            <div className="flex justify-center items-center gap-8 text-white/40">
              <span className="text-sm">🔒 Bank-Grade Security</span>
              <span className="text-sm">📊 Real-time Data</span>
              <span className="text-sm">🎯 24/7 Support</span>
            </div>
          </div>
        </section>

        {/* Footer with Mascot */}
        <footer className="py-20 text-center">
          <div className="container mx-auto px-6">
            {/* Blackboard-like texture */}
            <div className="bg-charcoal-black rounded-3xl p-12 relative overflow-hidden">
              {/* Chalk texture background */}
              <div className="absolute inset-0 opacity-10">
                <div className="w-full h-full" style={{
                  backgroundImage: `radial-gradient(circle at 25% 25%, white 2px, transparent 0),
                                   radial-gradient(circle at 75% 75%, white 1px, transparent 0)`,
                  backgroundSize: '50px 50px'
                }}></div>
              </div>

              <div className="relative z-10">
                {/* AlgoBot waving goodbye */}
                <div className="mb-8">
                  <AlgoBot expression="happy" size="large" accessories={['rocket']} />
                </div>

                <p className="text-2xl md:text-3xl text-off-white mb-4" style={{ fontFamily: 'Comic Neue, cursive' }}>
                  "Thanks for visiting! Ready to trade smarter? 🚀"
                </p>

                <p className="text-lg text-off-white/80 mb-8" style={{ fontFamily: 'Poppins, sans-serif' }}>
                  Made with ❤️ + Algorithms by the AlgoProject Team
                </p>

                {/* Social Links with Doodles */}
                <div className="flex justify-center items-center gap-6">
                  <a href="#" className="text-2xl hover:scale-110 transition-transform">📧</a>
                  <a href="#" className="text-2xl hover:scale-110 transition-transform">🐦</a>
                  <a href="#" className="text-2xl hover:scale-110 transition-transform">💬</a>
                  <a href="#" className="text-2xl hover:scale-110 transition-transform">📺</a>
                </div>
              </div>

              {/* Floating doodle elements */}
              <div className="absolute top-4 left-4 text-2xl animate-float opacity-30">📈</div>
              <div className="absolute top-4 right-4 text-2xl animate-doodle-bounce opacity-30">💰</div>
              <div className="absolute bottom-4 left-4 text-2xl animate-pulse opacity-30">⚙️</div>
              <div className="absolute bottom-4 right-4 text-2xl animate-spin-slow opacity-30">🌟</div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}

// Export additional components that other files might be importing
export function DoodleThemeEnhancer() {
  return (
    <div className="fixed inset-0 pointer-events-none z-0">
      {/* Subtle paper texture overlay */}
      <div className="absolute inset-0 opacity-30" style={{
        backgroundImage: `
          linear-gradient(90deg, transparent 78px, rgba(43,43,43,0.04) 79px, rgba(43,43,43,0.04) 81px, transparent 82px),
          linear-gradient(rgba(43,43,43,0.02) 0.5px, transparent 0.5px)
        `,
        backgroundSize: '82px 20px'
      }}></div>
      
      {/* Floating creativity particles */}
      <div className="absolute inset-0">
        {Array.from({ length: 8 }).map((_, i) => (
          <div
            key={i}
            className="absolute animate-float opacity-20"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${3 + Math.random() * 2}s`
            }}
          >
            {['💡', '⚡', '🎨', '🚀', '💎', '🎯', '⭐', '🌟'][i]}
          </div>
        ))}
      </div>
    </div>
  );
}

export function CreativeDoodleButton({ 
  children, 
  onClick, 
  variant = 'primary',
  className = ''
}: {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'accent';
  className?: string;
}) {
  const variantClasses = {
    primary: 'bg-mint-green hover:bg-mint-green/90 text-white',
    secondary: 'bg-coral-pink hover:bg-coral-pink/90 text-white',
    accent: 'bg-yellow hover:bg-yellow/90 text-charcoal-black'
  };

  return (
    <button
      onClick={onClick}
      className={`
        ${variantClasses[variant]}
        px-6 py-3 border-4 border-charcoal-black rounded-2xl font-bold
        shadow-lg hover:shadow-xl transform hover:scale-105 hover:rotate-1
        transition-all duration-300 relative overflow-hidden
        ${className}
      `}
      style={{ fontFamily: 'Comic Neue, cursive' }}
    >
      <span className="relative z-10">{children}</span>
      
      {/* Hover effect */}
      <div className="absolute inset-0 bg-white/20 rounded-2xl opacity-0 hover:opacity-100 transition-opacity duration-300"></div>
    </button>
  );
}

export function DoodleCard({ 
  children, 
  className = '',
  hover = true 
}: {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
}) {
  return (
    <div className={`
      bg-off-white border-4 border-charcoal-black rounded-2xl p-6 shadow-lg
      ${hover ? 'hover:shadow-xl transform hover:scale-105 hover:rotate-1 transition-all duration-300' : ''}
      ${className}
    `}>
      {children}
    </div>
  );
}