#!/usr/bin/env python3
"""
Ultra Simple Test - No External Dependencies
Tests basic functionality without pandas/ccxt
"""

import os
import sys
import time
from datetime import datetime

print("🧪 ULTRA SIMPLE TEST")
print("="*40)
print(f"Timestamp: {datetime.now()}")
print(f"Python: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print("="*40)

# Test 1: Basic imports
print("\n🔧 Test 1: Basic Python imports")
try:
    import json
    import csv
    import time
    print("✅ Standard library imports work")
except Exception as e:
    print(f"❌ Standard library import failed: {e}")
    sys.exit(1)

# Test 2: File system
print("\n🔧 Test 2: File system access")
try:
    # Check if we can read/write files
    test_file = "test_write.txt"
    with open(test_file, 'w') as f:
        f.write("test")
    
    with open(test_file, 'r') as f:
        content = f.read()
    
    os.remove(test_file)
    print("✅ File system access works")
except Exception as e:
    print(f"❌ File system access failed: {e}")

# Test 3: Try numpy (often causes issues)
print("\n🔧 Test 3: Testing numpy import")
try:
    print("   Importing numpy...", end="")
    import numpy as np
    print(" ✅ Success")
    
    print("   Testing numpy array...", end="")
    arr = np.array([1, 2, 3])
    print(f" ✅ Success: {arr}")
except Exception as e:
    print(f" ❌ Numpy failed: {e}")

# Test 4: Try pandas (this is where it hangs)
print("\n🔧 Test 4: Testing pandas import")
try:
    print("   Importing pandas (this might hang)...", end="")
    sys.stdout.flush()  # Force output
    
    import pandas as pd
    print(" ✅ Success")
    
    print("   Testing pandas DataFrame...", end="")
    df = pd.DataFrame({'a': [1, 2, 3]})
    print(f" ✅ Success: {len(df)} rows")
except Exception as e:
    print(f" ❌ Pandas failed: {e}")

# Test 5: Network without external libraries
print("\n🔧 Test 5: Testing basic network")
try:
    import urllib.request
    import socket
    
    print("   Testing socket connection...", end="")
    socket.create_connection(("8.8.8.8", 53), timeout=3)
    print(" ✅ Success")
    
except Exception as e:
    print(f" ❌ Network failed: {e}")

print("\n✅ Ultra simple test completed")
print("If this works, issue is with pandas/ccxt installation")
