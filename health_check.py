#!/usr/bin/env python3
"""System health check for Shopee Price Tracker"""

print('=== SHOPEE PRICE TRACKER - SYSTEM CHECK ===\n')

import sys
sys.path.insert(0, 'src')

checks_passed = 0
total_checks = 6

# Check 1: Config
print('1. Configuration...')
try:
    from config import config
    print(f'   ✓ Config loaded')
    print(f'   ✓ Sheet ID: {config.GOOGLE_SHEETS_ID[:20]}...')
    checks_passed += 1
except Exception as e:
    print(f'   ✗ Config error: {e}')

# Check 2: Logger
print('\n2. Logging System...')
try:
    from logger import app_logger
    print(f'   ✓ Logger configured')
    checks_passed += 1
except Exception as e:
    print(f'   ✗ Logger error: {e}')

# Check 3: Scraper
print('\n3. Web Scraper...')
try:
    from scraper import ShopeeScraper
    scraper = ShopeeScraper()
    pid = scraper.extract_product_id('https://shopee.ph/test-i.123.456')
    print(f'   ✓ Scraper initialized')
    print(f'   ✓ ID extraction works: {pid}')
    checks_passed += 1
except Exception as e:
    print(f'   ✗ Scraper error: {e}')

# Check 4: Google Sheets
print('\n4. Google Sheets Integration...')
try:
    from google_sheets import GoogleSheetsManager
    manager = GoogleSheetsManager(config.GOOGLE_SHEETS_ID)
    print(f'   ✓ Google Sheets authenticated')
    checks_passed += 1
except Exception as e:
    print(f'   ✗ Google Sheets error: {e}')

# Check 5: Tracker
print('\n5. Price Tracker Engine...')
try:
    from tracker import PriceTracker
    tracker = PriceTracker(config.GOOGLE_SHEETS_ID)
    print(f'   ✓ Tracker initialized')
    checks_passed += 1
except Exception as e:
    print(f'   ✗ Tracker error: {e}')

# Check 6: Requirements
print('\n6. Python Dependencies...')
try:
    import subprocess
    result = subprocess.run([sys.executable, '-m', 'pip', 'list'], capture_output=True, text=True)
    required = ['requests', 'beautifulsoup4', 'google-api-python-client', 'python-dotenv', 'schedule']
    missing = []
    for pkg in required:
        if pkg.lower() in result.stdout.lower():
            print(f'   ✓ {pkg}')
        else:
            print(f'   ✗ {pkg} - missing')
            missing.append(pkg)
    if not missing:
        checks_passed += 1
except Exception as e:
    print(f'   ✗ Dependency check error: {e}')

print(f'\n=== STATUS: {checks_passed}/{total_checks} CHECKS PASSED ===')

if checks_passed == total_checks:
    print('\n✓ ALL SYSTEMS OPERATIONAL!\n')
    print('Next steps:')
    print('  1. python track.py --url "https://shopee.ph/your-product"')
    print('  2. python verify_sheets.py')
    print('  3. Check your Google Sheet for tracked data')
else:
    print(f'\n✗ {total_checks - checks_passed} system(s) need attention.')
    print('Check the errors above and troubleshoot accordingly.')
