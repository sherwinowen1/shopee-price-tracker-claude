"""
Unit tests for Shopee Price Tracker
"""
import unittest
import sys
import os
import tempfile
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from scraper import ShopeeScraper
from config import config

class TestShopeeScraper(unittest.TestCase):
    """Test Shopee scraper"""
    
    def setUp(self):
        """Initialize scraper"""
        self.scraper = ShopeeScraper()
    
    def test_product_id_extraction_format1(self):
        """Test extracting product ID from standard Shopee URL"""
        url = "https://shopee.sg/product-name-i.12345.67890"
        product_id = self.scraper.extract_product_id(url)
        self.assertEqual(product_id, "67890")
    
    def test_product_id_extraction_format2(self):
        """Test extracting product ID from alternative format"""
        url = "https://shopee.com/i.67890"
        product_id = self.scraper.extract_product_id(url)
        self.assertIsNotNone(product_id)
    
    def test_invalid_url(self):
        """Test with invalid URL"""
        url = "https://example.com/invalid"
        product_id = self.scraper.extract_product_id(url)
        self.assertIsNone(product_id)
    
    def test_scraper_initialization(self):
        """Test scraper initializes correctly"""
        self.assertIsNotNone(self.scraper.timeout)
        self.assertIsNotNone(self.scraper.headers)
        self.assertIn('User-Agent', self.scraper.headers)

class TestConfig(unittest.TestCase):
    """Test configuration"""
    
    def test_config_has_required_attributes(self):
        """Test config has required attributes"""
        self.assertTrue(hasattr(config, 'GOOGLE_SHEETS_ID'))
        self.assertTrue(hasattr(config, 'SHOPEE_PRODUCT_URLS'))
        self.assertTrue(hasattr(config, 'CHECK_INTERVAL'))
        self.assertTrue(hasattr(config, 'LOG_LEVEL'))
    
    def test_log_path_exists(self):
        """Test log directory is created"""
        self.assertTrue(config.LOG_PATH.exists())
    
    def test_check_interval_positive(self):
        """Test check interval is positive"""
        self.assertGreater(config.CHECK_INTERVAL, 0)

class TestProductData(unittest.TestCase):
    """Test product data structure"""
    
    def test_product_data_structure(self):
        """Test product data has required fields"""
        sample_product = {
            'name': 'Test Product',
            'product_id': '12345',
            'price': 99.99,
            'discount': 10,
            'shop_name': 'Test Shop',
            'rating': 4.5,
            'url': 'https://shopee.com/test',
            'timestamp': datetime.now().isoformat()
        }
        
        required_fields = ['name', 'price', 'url', 'timestamp']
        for field in required_fields:
            self.assertIn(field, sample_product)

def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)

if __name__ == '__main__':
    run_tests()
