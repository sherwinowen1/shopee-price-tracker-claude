#!/usr/bin/env python3
"""
Test Shopee API with proper authentication
"""

import requests
import re
import json

url = "https://shopee.ph/adidas-Lifestyle-Adilette-Clog-2.0-Unisex-Black-JQ8058-i.319506484.27785404088"

# Extract IDs
match = re.search(r'-i\.(\d+)\.(\d+)', url)
if match:
    shop_id, item_id = match.group(1), match.group(2)
    print(f"Shop ID: {shop_id}, Item ID: {item_id}")
    
    # API endpoint
    api_url = f"https://shopee.ph/api/v4/product/get"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': url,
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    params = {
        'shopid': shop_id,
        'itemid': item_id,
    }
    
    print(f"\nTrying API endpoint: {api_url}")
    try:
        response = requests.get(api_url, headers=headers, params=params, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
            
            if 'data' in data:
                product = data['data']
                print(f"\nProduct found!")
                print(f"Name: {product.get('name', 'N/A')}")
                print(f"Price: {product.get('price', 'N/A')}")
                print(f"Status: Success")
            elif 'error' in data:
                print(f"API Error: {data['error']}")
        else:
            print(f"Response text: {response.text[:300]}")
            
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Could not extract IDs")
