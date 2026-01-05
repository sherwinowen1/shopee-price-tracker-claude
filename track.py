#!/usr/bin/env python3
"""
Shopee Price Tracker - Main Script
Track Shopee product prices and save to Google Sheets
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tracker import PriceTracker
from logger import app_logger
from config import config
import argparse

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Shopee Price Tracker - Track product prices and save to Google Sheets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python track.py                    # Track all products once
  python track.py --url URL          # Track a specific product
  python track.py --schedule         # Run scheduler for continuous tracking
  python track.py --scheduler        # Same as --schedule
        """
    )
    
    parser.add_argument(
        '--url',
        type=str,
        help='Shopee product URL to track'
    )
    
    parser.add_argument(
        '--schedule',
        '--scheduler',
        dest='schedule',
        action='store_true',
        help='Run scheduler for continuous tracking'
    )
    
    parser.add_argument(
        '--sheets-id',
        type=str,
        help='Google Sheets ID (overrides .env)'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        help='Tracking interval in seconds (default: from .env or 3600)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Shopee Price Tracker v1.0.0'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize tracker
        tracker = PriceTracker(args.sheets_id)
        
        if args.url:
            # Track specific URL
            app_logger.info(f"Tracking single product: {args.url}")
            product = tracker.track_product(args.url)
            if product:
                print(f"\n✓ Successfully tracked: {product.get('name')}")
                print(f"  Price: ₱{product.get('price', 'N/A')}")
                print(f"  URL: {product.get('url')}")
            else:
                print("✗ Failed to track product")
                sys.exit(1)
        
        elif args.schedule:
            # Run scheduler
            print("Starting Shopee Price Tracker Scheduler...")
            print(f"Tracking {len(config.SHOPEE_PRODUCT_URLS)} products every {config.CHECK_INTERVAL} seconds")
            print("Press Ctrl+C to stop\n")
            
            tracker.schedule_tracking(args.interval)
            tracker.run_scheduler()
        
        else:
            # Track all products once
            if not config.SHOPEE_PRODUCT_URLS:
                print("No products configured. Set SHOPEE_PRODUCT_URLS in .env")
                print("Example: SHOPEE_PRODUCT_URLS=https://shopee.com/product-1,https://shopee.com/product-2")
                sys.exit(1)
            
            print(f"Tracking {len(config.SHOPEE_PRODUCT_URLS)} products...")
            results = tracker.track_all_products()
            
            print(f"\n✓ Successfully tracked {len(results)} product(s)")
            for product in results:
                print(f"  • {product.get('name')} - ₱{product.get('price', 'N/A')}")
            
            if len(results) < len(config.SHOPEE_PRODUCT_URLS):
                failed = len(config.SHOPEE_PRODUCT_URLS) - len(results)
                print(f"\n⚠ {failed} product(s) failed to track")
    
    except KeyboardInterrupt:
        print("\n\nTracker stopped by user")
        sys.exit(0)
    except Exception as e:
        app_logger.error(f"Fatal error: {e}")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
