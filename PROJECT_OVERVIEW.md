# Shopee Price Tracker - Project Overview

## 📱 What is This?

A Python application that:
- **Tracks** Shopee product prices
- **Scrapes** product data from Shopee
- **Saves** price history to Google Sheets
- **Schedules** automatic price checks
- **Monitors** price changes over time

## 🚀 Getting Started (30 seconds)

```bash
# 1. Run setup
python setup.py

# 2. Configure .env with your Google Sheets ID and product URLs

# 3. Place credentials.json in the folder

# 4. Track prices
python track.py
```

## 📊 How It Works

```
User configures products
         ↓
Script scrapes Shopee
         ↓
Extracts price data
         ↓
Saves to Google Sheets
         ↓
Creates price history
```

## 🎯 Main Features

### 1. **Web Scraping**
- Extracts product information from Shopee
- Gets: price, discount, shop name, rating
- Handles Shopee's page structure

### 2. **Google Sheets Integration**
- Saves data directly to your Google Sheet
- Creates price history automatically
- Beautiful organized data

### 3. **Scheduling**
- Run once or continuously
- Configurable intervals (default: 1 hour)
- Background tracking

### 4. **Easy Configuration**
- Simple .env file setup
- No code changes needed
- Support for multiple products

## 📁 Project Structure

```
shopee-price-tracker-claude/
│
├── src/                          # Source code
│   ├── __init__.py              # Package init
│   ├── config.py                # Configuration loading
│   ├── logger.py                # Logging setup
│   ├── scraper.py               # Shopee web scraper
│   ├── google_sheets.py         # Google Sheets API client
│   └── tracker.py               # Main tracking engine
│
├── tests/                        # Unit tests
│   └── test_tracker.py
│
├── track.py                      # Main entry point
├── setup.py                      # Setup script
├── examples.py                   # Usage examples
├── verify.py                     # Verification script
│
├── requirements.txt              # Python dependencies
├── .env.example                 # Configuration template
├── .gitignore                   # Git ignore rules
│
├── README.md                    # Full documentation
├── QUICKSTART.md                # Quick start guide
├── PROJECT_OVERVIEW.md          # This file
│
└── .github/
    └── copilot-instructions.md  # AI assistant instructions
```

## 🔧 How Each Module Works

### `config.py`
- Loads environment variables from .env
- Provides configuration to all modules
- Ensures directories exist

### `logger.py`
- Sets up logging to console and file
- Creates logs/ folder automatically
- Tracks all operations

### `scraper.py` ⭐
- Makes HTTP requests to Shopee
- Parses HTML with BeautifulSoup
- Extracts price and product details
- Handles different page formats

### `google_sheets.py` ⭐
- Authenticates with Google API
- Reads/writes to your Google Sheet
- Manages sheet headers and data
- Handles authentication errors

### `tracker.py` ⭐
- Main orchestration logic
- Calls scraper to get data
- Saves to Google Sheets
- Schedules automatic updates

### `track.py`
- Command-line entry point
- Handles user arguments
- Calls tracker for operations

## 💾 Data Saved to Google Sheets

```
| Product Name | Product ID | Price | Discount | Shop Name | Rating | URL | Timestamp |
|---|---|---|---|---|---|---|---|
| Product 1 | 12345 | 299.99 | 15 | MyShop | 4.5 | https://... | 2024-01-02 10:30:00 |
| Product 2 | 67890 | 599.99 | 20 | OtherShop | 4.8 | https://... | 2024-01-02 10:35:00 |
```

## 🔑 Configuration Options

### `.env` File

```env
# Google Sheets ID (from URL)
GOOGLE_SHEETS_ID=1BxiMVs0XRA5nFMKUVfIEdidaQxfuJXvPYU76xm1V-EE

# Google API credentials file
GOOGLE_CREDENTIALS_FILE=credentials.json

# Shopee product URLs (comma-separated)
SHOPEE_PRODUCT_URLS=https://shopee.com/product-1,https://shopee.com/product-2

# Tracking interval in seconds (default: 3600 = 1 hour)
CHECK_INTERVAL=3600

# Logging level
LOG_LEVEL=INFO
```

## 📚 Usage Examples

### Basic Usage

```bash
# Track all products from .env once
python track.py

# Track a single product
python track.py --url "https://shopee.com/my-product"

# Show help
python track.py --help
```

### Scheduler Usage

```bash
# Start continuous background tracking
python track.py --schedule

# Track with custom interval (30 minutes)
python track.py --schedule --interval 1800

# Use different Google Sheets
python track.py --schedule --sheets-id YOUR_SHEETS_ID
```

### Testing

```bash
# Verify setup
python verify.py

# Run tests
python tests/test_tracker.py

# See examples
python examples.py
```

## 🔐 Authentication Setup

### Option 1: OAuth 2.0 (Personal Use)
1. Go to Google Cloud Console
2. Create Desktop OAuth2 credentials
3. Download JSON → `credentials.json`
4. Run application (browser opens for auth)

### Option 2: Service Account (Automation)
1. Create Service Account in Google Cloud
2. Download JSON key → `credentials.json`
3. Share Google Sheet with service email
4. Run application

## 📊 Workflow Examples

### Example 1: One-Time Price Check
```bash
python track.py --url "https://shopee.com/laptop-i.123456.789"
```
→ Scrapes price once → Saves to Sheet → Done

### Example 2: Daily Monitoring
```bash
# Set in .env: CHECK_INTERVAL=86400 (24 hours)
python track.py --schedule
```
→ Tracks daily → Saves to Sheet → Email notifications possible

### Example 3: Batch Tracking
```bash
# Set in .env: SHOPEE_PRODUCT_URLS=url1,url2,url3,...
python track.py
```
→ Tracks multiple → Saves all → Creates history

## 🛠️ Troubleshooting Guide

| Problem | Solution |
|---------|----------|
| "Credentials not found" | Download credentials.json from Google Cloud Console |
| "Sheets ID not configured" | Add GOOGLE_SHEETS_ID to .env |
| Products won't scrape | Check if URLs are valid, check logs/ folder |
| "No products configured" | Add SHOPEE_PRODUCT_URLS to .env |
| Authentication fails | Ensure credentials.json is valid JSON |
| Permission denied | Share Google Sheet with service account email |

## 🚀 Advanced Usage

### Custom Python Script
```python
from src.tracker import PriceTracker

tracker = PriceTracker("YOUR_SHEETS_ID")
product = tracker.track_product("https://shopee.com/product")
print(f"Price: {product['price']}")
```

### Multiple Sheets
```python
tracker1 = PriceTracker("SHEETS_ID_1")
tracker2 = PriceTracker("SHEETS_ID_2")

tracker1.track_product("url1")
tracker2.track_product("url2")
```

### Get Price History
```python
tracker = PriceTracker("YOUR_SHEETS_ID")
history = tracker.get_price_history()
for record in history:
    print(f"{record['Product Name']}: {record['Price']}")
```

## 📈 Future Enhancements

- [ ] Email notifications on price drops
- [ ] Price comparison dashboard
- [ ] Multiple marketplace support (Lazada, etc)
- [ ] Telegram/Discord bot integration
- [ ] Web interface
- [ ] REST API
- [ ] Price trend analysis

## 📝 Key Files to Know

| File | Purpose |
|------|---------|
| `track.py` | Main script - start here |
| `setup.py` | Installation and setup |
| `verify.py` | Test your setup |
| `src/scraper.py` | Where scraping happens |
| `src/google_sheets.py` | Google Sheets integration |
| `.env` | Your configuration |
| `logs/` | Application logs |

## ⚡ Performance Tips

1. **Increase interval** if Shopee blocks requests
2. **Use service account** for 24/7 automation
3. **Batch multiple products** in one run
4. **Check logs** for any warnings

## 📞 Support Resources

- **README.md** - Full documentation
- **QUICKSTART.md** - 5-minute setup guide
- **examples.py** - Code examples
- **verify.py** - Test your setup
- **logs/** folder - Error details

## 🎓 Learning Resources

- [Google Sheets API docs](https://developers.google.com/sheets/api)
- [BeautifulSoup docs](https://www.crummy.com/software/BeautifulSoup/)
- [Python requests](https://requests.readthedocs.io/)
- [Google Cloud Console](https://console.cloud.google.com)

## 📄 License

This project is provided for educational and personal use.

---

## Summary

This is a **complete, production-ready Python application** for tracking Shopee prices. It includes:

✅ Web scraping with error handling  
✅ Google Sheets integration  
✅ Scheduled background tasks  
✅ Comprehensive logging  
✅ Configuration management  
✅ Unit tests  
✅ Full documentation  
✅ Setup automation  
✅ Example code  

**Start with:** `python setup.py`  
**Then run:** `python track.py`

Happy tracking! 📊
