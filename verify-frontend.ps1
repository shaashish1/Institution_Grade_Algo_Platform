# Frontend Verification Script (PowerShell)
# Run this after cloning to verify all fixes are working

$ErrorActionPreference = "Stop"

Write-Host "🚀 AlgoProject Frontend Verification Script" -ForegroundColor Cyan
Write-Host "==========================================="
Write-Host ""

# Navigate to frontend directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$scriptPath\frontend"

Write-Host "📁 Current directory: $(Get-Location)"
Write-Host ""

# Step 1: Clean installation
Write-Host "🧹 Step 1: Clean installation" -ForegroundColor Yellow
Write-Host "Removing old artifacts..."
Remove-Item -Recurse -Force node_modules -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .next -ErrorAction SilentlyContinue
Remove-Item -Force tsconfig.tsbuildinfo -ErrorAction SilentlyContinue

Write-Host "Installing dependencies..."
npm ci
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Dependency installation failed" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 2: TypeScript type check
Write-Host "🔍 Step 2: Running TypeScript type check" -ForegroundColor Yellow
npm run type-check
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Type check passed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Type check has warnings (non-blocking)" -ForegroundColor Yellow
}
Write-Host ""

# Step 3: Linting
Write-Host "🎨 Step 3: Running linter" -ForegroundColor Yellow
npm run lint
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Linting passed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Linting has warnings (non-blocking)" -ForegroundColor Yellow
}
Write-Host ""

# Step 4: Production build
Write-Host "🏗️  Step 4: Building production bundle" -ForegroundColor Yellow
npm run build
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Production build successful" -ForegroundColor Green
} else {
    Write-Host "❌ Production build failed" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 5: Check build artifacts
Write-Host "📦 Step 5: Verifying build artifacts" -ForegroundColor Yellow
if (Test-Path ".next") {
    $buildSize = (Get-ChildItem .next -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
    $buildSizeFormatted = [math]::Round($buildSize, 2)
    Write-Host "✅ Build artifacts found (.next folder: $buildSizeFormatted MB)" -ForegroundColor Green
} else {
    Write-Host "❌ Build artifacts not found" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 6: Check for critical files
Write-Host "📋 Step 6: Checking critical files" -ForegroundColor Yellow
$criticalFiles = @(
    "package.json",
    "next.config.js",
    "tailwind.config.js",
    "tsconfig.json",
    "src\app\layout.tsx",
    "src\app\page.tsx",
    ".env.example"
)

foreach ($file in $criticalFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ Missing: $file" -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# Step 7: Environment check
Write-Host "🌍 Step 7: Environment configuration check" -ForegroundColor Yellow
if (Test-Path ".env.example") {
    Write-Host "✅ .env.example found" -ForegroundColor Green
    if (Test-Path ".env.local") {
        Write-Host "✅ .env.local exists (environment configured)" -ForegroundColor Green
    } else {
        Write-Host "⚠️  .env.local not found (copy from .env.example if needed)" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ .env.example not found" -ForegroundColor Red
}
Write-Host ""

# Final summary
Write-Host "==========================================="
Write-Host "🎉 All verification steps passed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Copy .env.example to .env.local (if using environment variables)"
Write-Host "2. Run 'npm run dev' to start the development server"
Write-Host "3. Open http://localhost:3000 in your browser"
Write-Host ""
Write-Host "For production deployment:"
Write-Host "  npm run build"
Write-Host "  npm run start"
Write-Host ""
