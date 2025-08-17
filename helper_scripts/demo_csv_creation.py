#!/usr/bin/env python3
"""
Simple Delta Exchange CSV demo - creates sample files to show locations
"""

import os
import csv
from datetime import datetime

def create_demo_csv_files():
    """Create demo CSV files to show exactly where they are saved."""
    
    input_path = r"d:\AlgoProject\crypto\input"
    
    # Demo data for different pair types
    demo_pairs = {
        "delta_spot_usdt.csv": [
            ["symbol", "base", "quote", "type", "active"],
            ["BTC/USDT", "BTC", "USDT", "spot", "true"],
            ["ETH/USDT", "ETH", "USDT", "spot", "true"],
            ["SOL/USDT", "SOL", "USDT", "spot", "true"]
        ],
        "delta_perpetual_usdt.csv": [
            ["symbol", "base", "quote", "type", "active"],
            ["BTC-PERP", "BTC", "USDT", "perpetual", "true"],
            ["ETH-PERP", "ETH", "USDT", "perpetual", "true"]
        ],
        "delta_pairs_summary.csv": [
            ["category", "count", "file_location"],
            ["spot_usdt", "3", "delta_spot_usdt.csv"],
            ["perpetual_usdt", "2", "delta_perpetual_usdt.csv"],
            ["total_active", "5", "multiple_files"]
        ]
    }
    
    print("🎯 Creating Demo Delta Exchange CSV Files")
    print("=" * 50)
    
    created_files = []
    
    for filename, data in demo_pairs.items():
        file_path = os.path.join(input_path, filename)
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(data)
            
            print(f"✅ Created: {filename}")
            print(f"   📍 Full path: {file_path}")
            print(f"   📊 Rows: {len(data)-1} pairs")
            created_files.append(file_path)
            
        except Exception as e:
            print(f"❌ Error creating {filename}: {e}")
    
    print()
    print("📁 File Verification:")
    
    for file_path in created_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {os.path.basename(file_path)} - {size} bytes")
        else:
            print(f"❌ {os.path.basename(file_path)} - NOT FOUND")
    
    print()
    print("🎯 Summary:")
    print(f"📥 CSV Files Location: {input_path}")
    print(f"📊 Files Created: {len(created_files)}")
    print("🚀 Ready for Delta Exchange integration!")
    
    return created_files

if __name__ == "__main__":
    create_demo_csv_files()
