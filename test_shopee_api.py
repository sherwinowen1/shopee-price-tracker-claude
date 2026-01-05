#!/usr/bin/env python3
"""
Test using Shopee's internal API directly
"""

import requests
import json
import re
from urllib.parse import urlencode

def extract_ids(url):
    """Extract shop and product IDs from URL"""
    match = re.search(r'\.i\.(\d+)\.(\d+)', url)
    if match:
        return match.group(1), match.group(2)
    return None, None

url = "https://shopee.ph/Outdoor-Portable-Camping-Tent-2Person-Waterproof-Hiking-Shelter-i.25316261.2935397050"
shop_id, item_id = extract_ids(url)

if shop_id and item_id:
    print(f"Shop ID: {shop_id}, Item ID: {item_id}")
    
    # Try different API endpoints
    endpoints = [
        # Standard item endpoint
        f"https://shopee.ph/api/v2/item/get?itemid={item_id}&shopid={shop_id}",
        
        # GraphQL endpoint
        "https://shopee.ph/api/v4/graphql",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Referer': url,
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    # Test endpoint 1
    print("\n1. Testing /api/v2/item/get...")
    try:
        response = requests.get(endpoints[0], headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Keys: {list(data.keys())}")
            if 'data' in data:
                product = data['data']
                print(f"   Name: {product.get('name', 'N/A')[:100]}")
                print(f"   Price: {product.get('price', 'N/A')}")
                print(f"   Success!")
                exit(0)
        else:
            print(f"   Response: {response.text[:300]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test endpoint 2 - GraphQL
    print("\n2. Testing GraphQL endpoint...")
    try:
        query = {
            "operationName": "ItemGetDetail",
            "variables": {
                "itemId": str(item_id),
                "shopId": str(shop_id)
            },
            "query": """query ItemGetDetail {
                item(id: $itemId) {
                    id
                    name
                    price
                }
            }"""
        }
        
        response = requests.post(endpoints[1], json=query, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:300]}")
    except Exception as e:
        print(f"   Error: {e}")
else:
    print(f"Could not extract IDs from URL: {url}")
