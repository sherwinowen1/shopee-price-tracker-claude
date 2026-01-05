#!/usr/bin/env python3
"""
Test the Shopee Price Tracker setup
Run this to verify everything is working
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from config import config
        from logger import app_logger
        from scraper import ShopeeScraper
        from tracker import PriceTracker
        print("✓ All modules imported successfully\n")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}\n")
        return False

def test_config():
    """Test configuration"""
    print("Testing configuration...")
    try:
        from config import config
        print(f"  LOG_LEVEL: {config.LOG_LEVEL}")
        print(f"  CHECK_INTERVAL: {config.CHECK_INTERVAL}s")
        print(f"  LOG_PATH exists: {config.LOG_PATH.exists()}")
        print("✓ Configuration loaded\n")
        return True
    except Exception as e:
        print(f"✗ Config error: {e}\n")
        return False

def test_scraper():
    """Test scraper initialization"""
    print("Testing scraper...")
    try:
        from scraper import ShopeeScraper
        scraper = ShopeeScraper()
        
        # Test product ID extraction
        url = "https://shopee.sg/product-name-i.12345.67890"
        product_id = scraper.extract_product_id(url)
        
        if product_id == "67890":
            print(f"✓ Product ID extraction works: {product_id}\n")
            return True
        else:
            print(f"✗ Product ID extraction failed\n")
            return False
    except Exception as e:
        print(f"✗ Scraper error: {e}\n")
        return False

def test_google_sheets_config():
    """Test Google Sheets configuration"""
    print("Testing Google Sheets configuration...")
    try:
        from config import config
        
        if not config.GOOGLE_SHEETS_ID:
            print("⚠ GOOGLE_SHEETS_ID not set in .env")
            print("  (This is OK for now, set it when ready)\n")
            return True
        else:
            print(f"✓ Google Sheets ID configured\n")
            return True
    except Exception as e:
        print(f"✗ Config error: {e}\n")
        return False

def test_directories():
    """Test directory structure"""
    print("Testing directory structure...")
    dirs = {
        'src': 'Source code',
        'tests': 'Tests',
        'data': 'Data storage',
        '.github': 'GitHub configs'
    }
    
    all_exist = True
    for dir_name, description in dirs.items():
        exists = os.path.isdir(dir_name)
        status = "✓" if exists else "✗"
        print(f"  {status} {dir_name}/ - {description}")
        all_exist = all_exist and exists
    
    print()
    return all_exist

def test_files():
    """Test required files"""
    print("Testing required files...")
    files = {
        'requirements.txt': 'Dependencies',
        'setup.py': 'Setup script',
        'track.py': 'Main script',
        '.env.example': 'Config template',
        'README.md': 'Documentation',
        'src/config.py': 'Configuration',
        'src/scraper.py': 'Web scraper',
        'src/google_sheets.py': 'Google Sheets API',
        'src/tracker.py': 'Tracking engine',
    }
    
    all_exist = True
    for file_path, description in files.items():
        exists = os.path.isfile(file_path)
        status = "✓" if exists else "✗"
        print(f"  {status} {file_path}")
        all_exist = all_exist and exists
    
    print()
    return all_exist

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Shopee Price Tracker - Setup Verification")
    print("=" * 60 + "\n")
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Scraper", test_scraper),
        ("Google Sheets Config", test_google_sheets_config),
        ("Directories", test_directories),
        ("Files", test_files),
    ]
    
    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))
    
    # Summary
    print("=" * 60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    if passed == total:
        print(f"✓ All tests passed! ({passed}/{total})")
        print("\nYou're ready to use Shopee Price Tracker!")
        print("\nNext steps:")
        print("1. Edit .env with your Google Sheets ID and product URLs")
        print("2. Place credentials.json in the project folder")
        print("3. Run: python track.py")
    else:
        print(f"⚠ Some tests failed ({passed}/{total})")
        print("\nPlease fix the issues above and try again.")
    
    print("=" * 60 + "\n")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
