#!/usr/bin/env python3
"""
Frontend URL Testing Script
===========================

Systematically tests all frontend URLs to identify and fix internal server errors.
"""

import requests
import time
from urllib.parse import urljoin

# Base URL for the frontend
BASE_URL = "http://localhost:3002"

# Complete list of all URLs to test
URLS_TO_TEST = [
    # Main Pages
    "/",
    "/about",
    "/dashboard",
    "/portfolio",
    "/analytics",
    
    # Trading Pages
    "/crypto",
    "/crypto/backtest",
    "/stocks",
    "/stocks/backtest",
    "/stocks/backtest/multi-strategy",
    "/stocks/backtest/universal",
    "/stocks/derivatives",
    "/stocks/option-chain",
    "/stocks/option-chain/complete",
    
    # Charts and Analysis
    "/charts",
    "/exchanges",
    "/reports",
    
    # AI Features
    "/ai/analysis",
    "/ai/sentiment",
    "/ai/risk",
    "/ai/strategies",
    
    # Tools
    "/tools/alerts",
    "/tools/calculator",
    "/tools/risk",
    "/tools/screener",
    
    # Settings
    "/settings",
    "/settings/exchanges",
    
    # Legal Pages
    "/privacy",
    "/terms",
    "/risk-disclosure",
    
    # Internal Network (if exists)
    "/intranet",
    "/intranet/dashboard",
    "/intranet/network",
    "/intranet/security",
]

def test_url(url):
    """Test a single URL and return status"""
    full_url = urljoin(BASE_URL, url)
    try:
        response = requests.get(full_url, timeout=10)
        return {
            'url': url,
            'full_url': full_url,
            'status_code': response.status_code,
            'status': 'PASS' if response.status_code == 200 else 'FAIL',
            'error': None
        }
    except requests.exceptions.RequestException as e:
        return {
            'url': url,
            'full_url': full_url,
            'status_code': None,
            'status': 'ERROR',
            'error': str(e)
        }

def main():
    """Test all URLs systematically"""
    print("🔍 Frontend URL Testing - Systematic Analysis")
    print("=" * 60)
    print(f"📡 Base URL: {BASE_URL}")
    print(f"📊 Total URLs to test: {len(URLS_TO_TEST)}")
    print("=" * 60)
    
    results = []
    passed = 0
    failed = 0
    errors = 0
    
    for i, url in enumerate(URLS_TO_TEST, 1):
        print(f"\n[{i:2d}/{len(URLS_TO_TEST)}] Testing: {url}")
        result = test_url(url)
        results.append(result)
        
        if result['status'] == 'PASS':
            print(f"    ✅ {result['status_code']} - OK")
            passed += 1
        elif result['status'] == 'FAIL':
            print(f"    ❌ {result['status_code']} - FAILED")
            failed += 1
        else:
            print(f"    🔥 ERROR - {result['error']}")
            errors += 1
        
        # Small delay to avoid overwhelming the server
        time.sleep(0.5)
    
    # Summary Report
    print("\n" + "=" * 60)
    print("📊 TESTING SUMMARY")
    print("=" * 60)
    print(f"✅ Passed:  {passed:2d} URLs")
    print(f"❌ Failed:  {failed:2d} URLs")
    print(f"🔥 Errors:  {errors:2d} URLs")
    print(f"📈 Success Rate: {(passed/(passed+failed+errors)*100):.1f}%")
    
    # Detailed Failed URLs
    if failed > 0 or errors > 0:
        print("\n" + "=" * 60)
        print("🚨 PROBLEMATIC URLS")
        print("=" * 60)
        
        for result in results:
            if result['status'] != 'PASS':
                print(f"❌ {result['url']}")
                print(f"   Status: {result['status_code']} ({result['status']})")
                if result['error']:
                    print(f"   Error: {result['error']}")
                print()
    
    # Working URLs
    print("\n" + "=" * 60)
    print("✅ WORKING URLS")
    print("=" * 60)
    
    for result in results:
        if result['status'] == 'PASS':
            print(f"✅ {result['url']}")
    
    return results

if __name__ == "__main__":
    results = main()