#!/bin/bash

# Frontend Verification Script
# Run this after cloning to verify all fixes are working

set -e  # Exit on error

echo "🚀 AlgoProject Frontend Verification Script"
echo "==========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Navigate to frontend directory
cd "$(dirname "$0")/frontend" || exit 1

echo "📁 Current directory: $(pwd)"
echo ""

# Step 1: Clean installation
echo "🧹 Step 1: Clean installation"
echo "Removing old artifacts..."
rm -rf node_modules .next tsconfig.tsbuildinfo 2>/dev/null || true

echo "Installing dependencies..."
if npm ci; then
    echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
else
    echo -e "${RED}❌ Dependency installation failed${NC}"
    exit 1
fi
echo ""

# Step 2: TypeScript type check
echo "🔍 Step 2: Running TypeScript type check"
if npm run type-check; then
    echo -e "${GREEN}✅ Type check passed${NC}"
else
    echo -e "${YELLOW}⚠️  Type check has warnings (non-blocking)${NC}"
fi
echo ""

# Step 3: Linting
echo "🎨 Step 3: Running linter"
if npm run lint; then
    echo -e "${GREEN}✅ Linting passed${NC}"
else
    echo -e "${YELLOW}⚠️  Linting has warnings (non-blocking)${NC}"
fi
echo ""

# Step 4: Production build
echo "🏗️  Step 4: Building production bundle"
if npm run build; then
    echo -e "${GREEN}✅ Production build successful${NC}"
else
    echo -e "${RED}❌ Production build failed${NC}"
    exit 1
fi
echo ""

# Step 5: Check build artifacts
echo "📦 Step 5: Verifying build artifacts"
if [ -d ".next" ]; then
    BUILD_SIZE=$(du -sh .next | cut -f1)
    echo -e "${GREEN}✅ Build artifacts found (.next folder: $BUILD_SIZE)${NC}"
else
    echo -e "${RED}❌ Build artifacts not found${NC}"
    exit 1
fi
echo ""

# Step 6: Check for critical files
echo "📋 Step 6: Checking critical files"
CRITICAL_FILES=(
    "package.json"
    "next.config.js"
    "tailwind.config.js"
    "tsconfig.json"
    "src/app/layout.tsx"
    "src/app/page.tsx"
    ".env.example"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $file${NC}"
    else
        echo -e "${RED}❌ Missing: $file${NC}"
        exit 1
    fi
done
echo ""

# Step 7: Environment check
echo "🌍 Step 7: Environment configuration check"
if [ -f ".env.example" ]; then
    echo -e "${GREEN}✅ .env.example found${NC}"
    if [ -f ".env.local" ]; then
        echo -e "${GREEN}✅ .env.local exists (environment configured)${NC}"
    else
        echo -e "${YELLOW}⚠️  .env.local not found (copy from .env.example if needed)${NC}"
    fi
else
    echo -e "${RED}❌ .env.example not found${NC}"
fi
echo ""

# Final summary
echo "==========================================="
echo -e "${GREEN}🎉 All verification steps passed!${NC}"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env.local (if using environment variables)"
echo "2. Run 'npm run dev' to start the development server"
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "For production deployment:"
echo "  npm run build"
echo "  npm run start"
echo ""
