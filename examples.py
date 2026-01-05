"""
Quick start example for Shopee Price Tracker
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scraper import ShopeeScraper
from google_sheets import GoogleSheetsManager
from logger import app_logger

def example_1_scrape_single_product():
    """Example 1: Scrape a single Shopee product"""
    print("Example 1: Scrape Single Product")
    print("-" * 50)
    
    scraper = ShopeeScraper()
    
    # Example product URL (replace with actual)
    url = "https://shopee.com/example-product"
    
    product = scraper.scrape_product(url)
    
    if product:
        print(f"Product: {product['name']}")
        print(f"Price: ₱{product['price']}")
        print(f"Shop: {product['shop_name']}")
        print(f"Discount: {product['discount']}%")
        print(f"URL: {product['url']}")
    else:
        print("Failed to scrape product")
    print()

def example_2_save_to_google_sheets():
    """Example 2: Save product data to Google Sheets"""
    print("Example 2: Save to Google Sheets")
    print("-" * 50)
    
    try:
        # Initialize Google Sheets
        sheets = GoogleSheetsManager("YOUR_GOOGLE_SHEETS_ID")
        
        # Sample product data
        product_data = {
            'name': 'Sample Product',
            'product_id': '12345',
            'price': 299.99,
            'discount': 15,
            'shop_name': 'Sample Shop',
            'rating': 4.5,
            'url': 'https://shopee.com/sample-product',
            'timestamp': '2024-01-02T10:30:00'
        }
        
        # Append to sheet
        success = sheets.append_price_data(product_data)
        
        if success:
            print("✓ Data saved to Google Sheets")
        else:
            print("✗ Failed to save data")
    
    except Exception as e:
        print(f"Error: {e}")
    print()

def example_3_track_multiple_products():
    """Example 3: Track multiple products"""
    print("Example 3: Track Multiple Products")
    print("-" * 50)
    
    from tracker import PriceTracker
    
    try:
        tracker = PriceTracker("YOUR_GOOGLE_SHEETS_ID")
        
        urls = [
            "https://shopee.com/product-1",
            "https://shopee.com/product-2",
            "https://shopee.com/product-3",
        ]
        
        print(f"Tracking {len(urls)} products...\n")
        
        for url in urls:
            product = tracker.track_product(url)
            if product:
                print(f"✓ {product['name']} - ₱{product['price']}")
            else:
                print(f"✗ Failed to track: {url}")
        
        print("\nTracking complete!")
    
    except Exception as e:
        print(f"Error: {e}")
    print()

def example_4_scheduled_tracking():
    """Example 4: Scheduled tracking"""
    print("Example 4: Scheduled Tracking")
    print("-" * 50)
    
    from tracker import PriceTracker
    import schedule
    
    try:
        tracker = PriceTracker("YOUR_GOOGLE_SHEETS_ID")
        
        # Schedule tracking every hour
        tracker.schedule_tracking(interval_seconds=3600)
        
        print("Tracking scheduled every 1 hour")
        print("Press Ctrl+C to stop\n")
        
        # Run scheduler (uncomment to use)
        # tracker.run_scheduler()
    
    except Exception as e:
        print(f"Error: {e}")
    print()

if __name__ == "__main__":
    print("\nShopee Price Tracker - Examples")
    print("=" * 50)
    print()
    
    print("These examples show how to use the tracker.\n")
    print("Before running, update with your actual:")
    print("- Google Sheets ID")
    print("- Product URLs")
    print("- Credentials.json file\n")
    print("=" * 50)
    print()
    
    # Uncomment to run examples:
    # example_1_scrape_single_product()
    # example_2_save_to_google_sheets()
    # example_3_track_multiple_products()
    # example_4_scheduled_tracking()
    
    print("See README.md for full documentation and setup instructions.")
