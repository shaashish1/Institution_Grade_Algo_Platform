#!/usr/bin/env python3
"""
Test script for Fyers User Service API endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_fyers_endpoints():
    """Test all Fyers user service endpoints"""
    
    print("🧪 Testing Fyers User Service API Endpoints")
    print("=" * 50)
    
    # Test data
    test_user_id = "test_user_123"
    test_credentials = {
        "user_id": test_user_id,
        "client_id": "XA12345-100",
        "secret_key": "TEST_SECRET_KEY",
        "redirect_uri": "https://www.google.com",
        "user_name": "XA00330",
        "totp_key": "DV42ZDKZPMX6U7TH7272FVMYY4OQTINQ",
        "pin": "1234",
        "is_active": True
    }
    
    try:
        # Test 1: Add credentials
        print("\n1️⃣ Testing POST /fyers/credentials")
        response = requests.post(f"{BASE_URL}/fyers/credentials", json=test_credentials)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Success: {response.json()}")
        else:
            print(f"❌ Error: {response.text}")
            
        # Test 2: Get credentials
        print(f"\n2️⃣ Testing GET /fyers/credentials/{test_user_id}")
        response = requests.get(f"{BASE_URL}/fyers/credentials/{test_user_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Success: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Error: {response.text}")
            
        # Test 3: Get status
        print(f"\n3️⃣ Testing GET /fyers/status/{test_user_id}")
        response = requests.get(f"{BASE_URL}/fyers/status/{test_user_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Success: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Error: {response.text}")
            
        # Test 4: Test connection
        print(f"\n4️⃣ Testing POST /fyers/test-connection/{test_user_id}")
        response = requests.post(f"{BASE_URL}/fyers/test-connection/{test_user_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Success: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Error: {response.text}")
            
        # Test 5: List users
        print(f"\n5️⃣ Testing GET /fyers/users")
        response = requests.get(f"{BASE_URL}/fyers/users")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Success: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Error: {response.text}")
            
        # Test 6: Delete credentials (cleanup)
        print(f"\n6️⃣ Testing DELETE /fyers/credentials/{test_user_id}")
        response = requests.delete(f"{BASE_URL}/fyers/credentials/{test_user_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Success: {response.json()}")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the FastAPI server is running on localhost:8000")
        print("   Run: python api/main.py")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        
    print("\n" + "=" * 50)
    print("🏁 Fyers API endpoint testing completed!")

if __name__ == "__main__":
    test_fyers_endpoints()