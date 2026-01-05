#!/usr/bin/env python3
"""Test Shopee API approach"""

import requests
import re

# Extract product ID from URL
url = "https://shopee.ph/Outdoor-Portable-Camping-Tent-2Person-Waterproof-Hiking-Shelter-i.25316261.2935397050"

# Extract IDs
match = re.search(r'\.i\.(\d+)\.(\d+)', url)
if match:
    shop_id = match.group(1)
    product_id = match.group(2)
    print(f"Shop ID: {shop_id}")
    print(f"Product ID: {product_id}")
    
    # Try Shopee's API endpoint
    api_url = f"https://shopee.ph/api/v2/item/get?itemid={product_id}&shopid={shop_id}"
    print(f"\nTrying API: {api_url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    response = requests.get(api_url, headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nAPI Response keys: {list(data.keys())}")
        
        # Try to get product data
        if 'data' in data:
            product = data['data']
            print(f"\nProduct keys: {list(product.keys())[:10]}")
            print(f"Product ID: {product.get('itemid')}")
            print(f"Name: {product.get('name')}")
            print(f"Price: {product.get('price')}")
            print(f"Price Before Discount: {product.get('price_before_discount')}")
    else:
        print(f"Error: {response.text[:500]}")
