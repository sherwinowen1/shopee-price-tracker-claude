#!/usr/bin/env python3
"""
Track products from a URL list file
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scraper import ShopeeScraper
from google_sheets import GoogleSheetsManager
from logger import app_logger

def track_from_file(filename: str, limit: int = None):
    """
    Track products from a file containing URLs (one per line)
    
    Args:
        filename: File containing product URLs
        limit: Max products to track
    """
    # Read URLs from file
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        app_logger.error(f"File not found: {filename}")
        return
    
    if not urls:
        app_logger.error("No URLs found in file")
        return
    
    # Limit if specified
    if limit:
        urls = urls[:limit]
    
    app_logger.info(f"Found {len(urls)} product URLs in {filename}")
    
    # Initialize scraper and sheets
    scraper = ShopeeScraper()
    sheets = GoogleSheetsManager()
    sheets.initialize_sheet()
    
    tracked = 0
    failed = 0
    
    # Track each product
    for i, url in enumerate(urls, 1):
        url = url.strip()
        if not url or url.startswith('#'):
            continue
        
        try:
            app_logger.info(f"[{i}/{len(urls)}] Tracking: {url}")
            
            product_data = scraper.scrape_product(url)
            if product_data:
                if sheets.append_price_data(product_data):
                    tracked += 1
                    name = product_data.get('name', 'Unknown')
                    price = product_data.get('price', 'N/A')
                    print(f"  ✓ {name} - ₱{price}")
                else:
                    failed += 1
                    print(f"  ✗ Failed to save to Google Sheets")
            else:
                failed += 1
                print(f"  ✗ Failed to scrape product")
                
        except Exception as e:
            failed += 1
            app_logger.error(f"Error: {e}")
    
    # Summary
    print("\n" + "="*70)
    print(f"Tracking Complete")
    print(f"✓ Successfully tracked: {tracked}")
    print(f"✗ Failed: {failed}")
    print(f"Total: {tracked + failed}")
    print("="*70)
    
    if tracked > 0:
        print(f"\nData saved to Google Sheets!")

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "product_urls.txt"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    if not os.path.exists(filename):
        print(f"Usage: python track_from_file.py <filename> [limit]")
        print(f"\nExample:")
        print(f"  python track_from_file.py product_urls.txt")
        print(f"  python track_from_file.py product_urls.txt 10")
        print(f"\nFile format: One URL per line")
        print(f"  https://shopee.ph/Product-Name-i.123456.789")
        sys.exit(1)
    
    track_from_file(filename, limit)
