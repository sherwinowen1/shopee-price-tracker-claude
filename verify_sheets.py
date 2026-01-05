#!/usr/bin/env python3
"""Verify data in Google Sheets"""

import sys
sys.path.insert(0, 'src')

from google_sheets import GoogleSheetsManager
from config import config

print("Checking data in Google Sheets...")
print(f"Sheet ID: {config.GOOGLE_SHEETS_ID}")

try:
    manager = GoogleSheetsManager(config.GOOGLE_SHEETS_ID)
    prices = manager.get_latest_prices()
    
    if prices:
        print(f"\n✓ Successfully retrieved {len(prices)} records from Google Sheets!")
        print("\nLatest entries:")
        for i, p in enumerate(prices[-3:], 1):
            print(f"\n  Entry {i}:")
            print(f"    Product: {p.get('Product Name', 'N/A')[:50]}")
            print(f"    Price: ₱{p.get('Price', 'N/A')}")
            print(f"    Date: {p.get('Timestamp', 'N/A')[:10]}")
            print(f"    Rating: {p.get('Rating', 'N/A')} / 5")
    else:
        print("\nNo data in Google Sheets yet.")
        print("Run: python track.py --url <product-url>")
        
except Exception as e:
    print(f"\nError accessing Google Sheets: {e}")
    print("Make sure credentials.json is in the project root")

