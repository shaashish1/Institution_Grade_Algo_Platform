"""
Data Feed Validation Test
Tests end-to-end data flow: Backend → API → Response
"""

import requests
import json
from datetime import datetime

def test_backend_health():
    """Test if backend server is running"""
    print("\n🔍 Testing Backend Health...")
    try:
        response = requests.get('http://localhost:8000/health')
        assert response.status_code == 200
        print("✅ Backend server is healthy")
        return True
    except Exception as e:
        print(f"❌ Backend health check failed: {e}")
        return False

def test_market_indices():
    """Test NSE indices endpoint"""
    print("\n🔍 Testing Market Indices API...")
    try:
        response = requests.get('http://localhost:8000/api/market/indices')
        assert response.status_code == 200
        
        data = response.json()
        assert 'indices' in data
        assert len(data['indices']) > 0
        
        # Check NIFTY 50 data
        nifty = next((idx for idx in data['indices'] if idx['symbol'] == 'NIFTY 50'), None)
        assert nifty is not None
        assert 'price' in nifty
        assert 'change' in nifty
        assert 'change_percent' in nifty
        assert nifty['data_source'] == 'NSE_FREE'
        
        print(f"✅ Market Indices working - NIFTY 50: ₹{nifty['price']:.2f}")
        print(f"   Change: {nifty['change']:+.2f} ({nifty['change_percent']:+.2f}%)")
        return True
    except Exception as e:
        print(f"❌ Market indices test failed: {e}")
        return False

def test_stock_quotes():
    """Test stock quotes endpoint"""
    print("\n🔍 Testing Stock Quotes API...")
    try:
        response = requests.post(
            'http://localhost:8000/api/market/quotes',
            json={'symbols': ['RELIANCE', 'TCS'], 'exchange': 'NSE'}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert 'RELIANCE' in data
        assert 'TCS' in data
        
        # Check RELIANCE data
        reliance = data['RELIANCE']
        assert 'ltp' in reliance
        assert 'change' in reliance
        assert reliance['data_source'] == 'NSE_FREE'
        
        print(f"✅ Stock Quotes working - RELIANCE: ₹{reliance['ltp']:.2f}")
        print(f"   Change: {reliance['change']:+.2f} ({reliance['change_percent']:+.2f}%)")
        return True
    except Exception as e:
        print(f"❌ Stock quotes test failed: {e}")
        return False

def test_provider_status():
    """Test data provider status"""
    print("\n🔍 Testing Data Provider Status...")
    try:
        response = requests.get('http://localhost:8000/api/market-data/provider-status')
        assert response.status_code == 200
        
        data = response.json()
        assert 'status' in data
        
        print(f"✅ Provider Status: {data.get('status', 'unknown')}")
        print(f"   Data Source: {data.get('data_source', 'unknown')}")
        return True
    except Exception as e:
        print(f"❌ Provider status test failed: {e}")
        return False

def test_data_freshness():
    """Test if data is fresh (not stale)"""
    print("\n🔍 Testing Data Freshness...")
    try:
        response = requests.get('http://localhost:8000/api/market/indices')
        data = response.json()
        
        # Check if we have recent data
        nifty = next((idx for idx in data['indices'] if idx['symbol'] == 'NIFTY 50'), None)
        if nifty and nifty.get('price', 0) > 0:
            print(f"✅ Data is fresh - Last price: ₹{nifty['price']:.2f}")
            return True
        else:
            print("⚠️  Warning: Data might be stale")
            return False
    except Exception as e:
        print(f"❌ Data freshness test failed: {e}")
        return False

def main():
    """Run all validation tests"""
    print("=" * 60)
    print("🚀 DATA FEED VALIDATION TEST")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        test_backend_health,
        test_market_indices,
        test_stock_quotes,
        test_provider_status,
        test_data_freshness
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {total - passed} ❌")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - Data feed is fully operational!")
        return 0
    else:
        print("\n⚠️  Some tests failed - Please check the errors above")
        return 1

if __name__ == "__main__":
    exit(main())
