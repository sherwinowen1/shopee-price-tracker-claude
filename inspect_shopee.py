#!/usr/bin/env python3
"""Helper script to inspect Shopee page structure"""

import requests
from bs4 import BeautifulSoup
import re
import json

url = 'https://shopee.ph/Outdoor-Portable-Camping-Tent-2Person-Waterproof-Hiking-Shelter-i.25316261.2935397050'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

print("Fetching page...")
r = requests.get(url, headers=headers, timeout=10)

print(f"Status code: {r.status_code}")
print(f"Page size: {len(r.text)} characters")

# Save for inspection
with open('shopee_page.html', 'w', encoding='utf-8') as f:
    f.write(r.text)
print("Saved to shopee_page.html")

# Look for JSON-LD
json_ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', r.text, re.DOTALL)
print(f"\nJSON-LD scripts found: {len(json_ld)}")
for i, ld in enumerate(json_ld[:2]):
    print(f"  [{i}] {ld[:200]}...")

# Look for script tags with data
scripts = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
print(f"\nTotal script tags: {len(scripts)}")

# Look for data attributes
soup = BeautifulSoup(r.text, 'html.parser')
print(f"\nElements with data-* attributes:")
for elem in soup.find_all(attrs={'data-testid': True})[:5]:
    print(f"  {elem.name}: data-testid='{elem.get('data-testid')}' -> {elem.get_text(strip=True)[:100]}")

# Check for OG meta tags
og_tags = soup.find_all('meta', property=re.compile(r'^og:'))
print(f"\nOG Meta tags found: {len(og_tags)}")
for tag in og_tags:
    print(f"  {tag.get('property')}: {tag.get('content', '')[:100]}")

# Look for common price/title patterns
print("\nSearching for price patterns in first 10000 chars:")
patterns = [
    r'[\d,]+(?:\.\d{2})?',  # Numbers
    r'(?:₱|PHP|P)\s*[\d,]+',  # PHP currency
]

for pattern in patterns:
    matches = re.findall(pattern, r.text[:10000])
    if matches:
        print(f"  Pattern '{pattern}': {matches[:5]}")

print("\nFirst 2000 characters of HTML body:")
body = soup.find('body')
if body:
    print(body.prettify()[:2000])
