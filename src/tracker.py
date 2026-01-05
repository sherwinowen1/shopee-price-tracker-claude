"""
Main price tracking logic
"""
import schedule
import time
from typing import List, Dict, Optional
from scraper import ShopeeScraper
from google_sheets import GoogleSheetsManager
from logger import app_logger
from config import config
from datetime import datetime

class PriceTracker:
    """Main price tracking engine"""
    
    def __init__(self, spreadsheet_id: str = None):
        """
        Initialize tracker
        
        Args:
            spreadsheet_id: Google Sheets ID
        """
        self.scraper = ShopeeScraper()
        self.sheets = GoogleSheetsManager(spreadsheet_id)
        self.products_urls = config.SHOPEE_PRODUCT_URLS
        
        # Initialize Google Sheet
        self.sheets.initialize_sheet()
    
    def track_product(self, url: str) -> Optional[Dict]:
        """
        Track a single product
        
        Args:
            url: Product URL
            
        Returns:
            Product data dictionary
        """
        try:
            # Scrape product
            product_data = self.scraper.scrape_product(url)
            
            if not product_data:
                app_logger.error(f"Failed to scrape: {url}")
                return None
            
            # Save to Google Sheets
            if self.sheets.append_price_data(product_data):
                app_logger.info(f"Saved to Google Sheets: {product_data.get('name')}")
                return product_data
            else:
                app_logger.error(f"Failed to save to Google Sheets: {product_data.get('name')}")
                return None
            
        except Exception as e:
            app_logger.error(f"Error tracking product: {e}")
            return None
    
    def track_all_products(self) -> List[Dict]:
        """
        Track all configured products
        
        Returns:
            List of successfully tracked products
        """
        if not self.products_urls:
            app_logger.warning("No product URLs configured")
            return []
        
        app_logger.info(f"Starting to track {len(self.products_urls)} products...")
        results = []
        
        for url in self.products_urls:
            url = url.strip()
            if url:
                product = self.track_product(url)
                if product:
                    results.append(product)
        
        app_logger.info(f"Tracking completed. {len(results)}/{len(self.products_urls)} successful")
        return results
    
    def schedule_tracking(self, interval_seconds: int = None):
        """
        Schedule automatic tracking
        
        Args:
            interval_seconds: Interval between tracking (default from config)
        """
        interval = interval_seconds or config.CHECK_INTERVAL
        
        # Schedule tracking
        schedule.every(interval).seconds.do(self.track_all_products)
        
        hours = interval // 3600
        minutes = (interval % 3600) // 60
        
        if hours > 0:
            app_logger.info(f"Tracking scheduled every {hours}h {minutes}m")
        else:
            app_logger.info(f"Tracking scheduled every {minutes}m")
    
    def run_scheduler(self):
        """Run the scheduler in the background"""
        app_logger.info("Starting scheduler...")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            app_logger.info("Scheduler stopped by user")
        except Exception as e:
            app_logger.error(f"Scheduler error: {e}")
    
    def get_price_history(self, sheet_name: str = "Price Tracker") -> List[Dict]:
        """
        Get price history from Google Sheets
        
        Args:
            sheet_name: Sheet name
            
        Returns:
            List of price records
        """
        return self.sheets.get_latest_prices(sheet_name)
