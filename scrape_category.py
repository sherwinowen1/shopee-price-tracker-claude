#!/usr/bin/env python3
"""
Scrape all products from a Shopee category page
"""
import sys
import os
import requests

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scraper import ShopeeScraper
from google_sheets import GoogleSheetsManager
from logger import app_logger

def scrape_category(category_url: str, limit: int = None):
    """
    Scrape all products from a category page and track them
    
    Args:
        category_url: Shopee category URL
        limit: Max products to scrape (None = all)
    """
    scraper = ShopeeScraper()
    
    # Try Method 1: Extract from category URL and use Shopee API
    # https://shopee.ph/Crocs-Classic-Sandal-V2 -> search for "Crocs Classic Sandal V2"
    from urllib.parse import urlparse, unquote
    parsed = urlparse(category_url)
    path = parsed.path.strip('/').replace('-', ' ')
    
    app_logger.info(f"Searching for products matching: '{path}'")
    
    try:
        # Use Shopee search API (if available)
        search_url = f"https://shopee.ph/api/v2/search_items"
        params = {
            'by': 'relevancy',
            'keyword': path,
            'limit': limit or 20,
            'offset': 0,
        }
        
        response = requests.get(search_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            
            if items:
                app_logger.info(f"Found {len(items)} products via API")
                
                # Construct product URLs from API response
                product_links = []
                for item in items:
                    shop_id = item.get('shop_id')
                    item_id = item.get('item_id')
                    name = item.get('name', '').replace(' ', '-')
                    
                    if shop_id and item_id:
                        url = f"https://shopee.ph/{name}-i.{shop_id}.{item_id}"
                        product_links.append(url)
                
                if product_links:
                    app_logger.info(f"Will track {len(product_links)} products")
                    track_products(product_links, limit)
                    return
    except Exception as e:
        app_logger.debug(f"API search failed: {e}")
    
    # Fallback: Try scraping HTML for product links
    app_logger.info("Attempting HTML scraping...")
    product_links = scraper.scrape_category_products(category_url)
    
    if not product_links:
        app_logger.warning("⚠️  No products found. Try one of these:")
        app_logger.warning("1. Provide a direct product URL (with -i.xxx.xxx)")
        app_logger.warning("2. Try a different category URL")
        app_logger.warning("3. Use manual URL list in a file")
        return
    
    track_products(product_links, limit)

def track_products(product_links: list, limit: int = None):
    """Track a list of product URLs"""
    scraper = ShopeeScraper()
    
    # Limit if specified
    if limit:
        product_links = product_links[:limit]
    
    # Track all products
    sheets = GoogleSheetsManager()
    sheets.initialize_sheet()
    
    tracked = 0
    failed = 0
    
    for i, url in enumerate(product_links, 1):
        try:
            app_logger.info(f"Tracking {i}/{len(product_links)}: {url}")
            
            product_data = scraper.scrape_product(url)
            if product_data:
                if sheets.append_price_data(product_data):
                    tracked += 1
                    app_logger.info(f"✓ Tracked: {product_data.get('name')}")
                else:
                    failed += 1
                    app_logger.error(f"✗ Failed to save: {url}")
            else:
                failed += 1
                app_logger.error(f"✗ Failed to scrape: {url}")
                
        except Exception as e:
            failed += 1
            app_logger.error(f"Error processing {url}: {e}")
    
    # Summary
    print("\n" + "="*60)
    print(f"Scraping Complete")
    print(f"✓ Successfully tracked: {tracked}")
    print(f"✗ Failed: {failed}")
    print(f"Total: {tracked + failed}")
    print("="*60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scrape_category.py <category_url> [limit]")
        print("\nExample:")
        print("  python scrape_category.py 'https://shopee.ph/Crocs-Classic-Sandal-V2'")
        print("  python scrape_category.py 'https://shopee.ph/Crocs-Classic-Sandal-V2' 10")
        sys.exit(1)
    
    category_url = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    scrape_category(category_url, limit)
