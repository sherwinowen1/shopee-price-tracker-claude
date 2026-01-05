# Shopee Price Tracker

A Python script to track Shopee product prices and automatically save the data to Google Sheets.

## Features

- 🔍 **Web Scraping**: Extract product prices from Shopee
- 📊 **Google Sheets Integration**: Automatically save prices to Google Sheets
- ⏰ **Scheduled Updates**: Track prices at regular intervals
- 📈 **Price History**: Keep complete price history in Google Sheets
- 🔧 **Easy Configuration**: Simple .env file setup
- 🚀 **Flexible**: Track one product or multiple products

## Quick Start

### 1. Installation

Clone/download the project and install dependencies:

```bash
cd shopee-price-tracker-claude
python setup.py
```

### 2. Google Sheets Setup

1. Create a Google Sheet: https://sheets.google.com
2. Copy your Spreadsheet ID from the URL
3. Get Google Sheets API credentials from Google Cloud Console
4. Save credentials as `credentials.json` in the project directory

### 3. Configuration

Edit `.env` file:

```env
GOOGLE_SHEETS_ID=your_google_sheet_id_here
SHOPEE_PRODUCT_URLS=https://shopee.com/product-1,https://shopee.com/product-2
CHECK_INTERVAL=3600
```

### 4. Run Tracker

**Track all products once:**
```bash
python track.py
```

**Track a specific product:**
```bash
python track.py --url "https://shopee.com/your-product"
```

**Run continuous tracking (scheduler):**
```bash
python track.py --schedule
```

## Configuration Guide

### .env File

```env
# Google Sheets Spreadsheet ID
GOOGLE_SHEETS_ID=1BxiMVs0XRA5nFMKUVfIEdidaQxfuJXvPYU76xm1V-EE

# Google API Credentials File
GOOGLE_CREDENTIALS_FILE=credentials.json

# Shopee Product URLs (comma-separated)
SHOPEE_PRODUCT_URLS=https://shopee.sg/product-1-i.123456.789,https://shopee.sg/product-2-i.123456.790

# Check interval in seconds (default: 3600 = 1 hour)
CHECK_INTERVAL=3600

# Logging level
LOG_LEVEL=INFO
```

## Usage Examples

### Single Product Tracking

Track one product immediately:

```bash
python track.py --url "https://shopee.com/My-Product-i.12345.67890"
```

### Batch Tracking

Track multiple products from .env:

```bash
python track.py
```

### Scheduled Tracking

Run continuous background tracking:

```bash
python track.py --schedule
```

Tracks all products every hour (or your configured interval).

### Custom Interval

Track with custom interval (in seconds):

```bash
python track.py --schedule --interval 1800  # Every 30 minutes
```

## Google Sheets Setup Guide

### Getting Credentials

#### Option 1: OAuth 2.0 (Recommended for personal use)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable "Google Sheets API"
4. Go to "Credentials" → "Create Credentials" → "OAuth client ID"
5. Choose "Desktop application"
6. Download as JSON
7. Save as `credentials.json`

#### Option 2: Service Account (For automation)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a Service Account
3. Create and download JSON key
4. Save as `credentials.json`
5. Share your Google Sheet with the service account email

### Getting Your Spreadsheet ID

1. Open your Google Sheet
2. The ID is in the URL: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`
3. Copy the long ID string
4. Add to `.env`: `GOOGLE_SHEETS_ID=your_id_here`

## Project Structure

```
shopee-price-tracker-claude/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration management
│   ├── logger.py            # Logging setup
│   ├── scraper.py           # Shopee scraper
│   ├── google_sheets.py     # Google Sheets integration
│   └── tracker.py           # Main tracking engine
├── track.py                 # Main script
├── setup.py                 # Setup script
├── requirements.txt         # Dependencies
├── .env.example            # Configuration template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## How It Works

1. **Scraping**: The `scraper.py` module fetches product data from Shopee
2. **Data Collection**: Extracts price, discount, shop name, rating, etc.
3. **Google Sheets**: Appends data to your Google Sheet with timestamp
4. **Scheduling**: Optionally runs on a schedule for continuous tracking

### Data Saved to Google Sheets

Each product tracking creates a row with:
- **Product Name**: Name of the product
- **Product ID**: Unique Shopee product ID
- **Price**: Current price
- **Discount (%)**: Discount percentage
- **Shop Name**: Seller name
- **Rating**: Product rating
- **URL**: Product URL
- **Timestamp**: When the data was collected

## Troubleshooting

### "Credentials not found" Error

- Download `credentials.json` from Google Cloud Console
- Save it in the project root directory
- Make sure filename is exactly `credentials.json`

### "Google Sheets ID not configured" Error

- Add your Spreadsheet ID to `.env`:
  ```env
  GOOGLE_SHEETS_ID=your_id_here
  ```
- Get ID from Google Sheets URL

### Products Not Scraping

- Check if URLs are correct Shopee product links
- Shopee website structure may have changed
- Check logs in `logs/` directory
- Ensure internet connection is working

### "No products configured" Error

- Add product URLs to `.env`:
  ```env
  SHOPEE_PRODUCT_URLS=https://shopee.com/product-1,https://shopee.com/product-2
  ```
- Or use `--url` flag: `python track.py --url "https://shopee.com/product"`

### Rate Limiting Issues

- Shopee may block requests if too frequent
- Increase `CHECK_INTERVAL` in `.env`
- Default is 3600 seconds (1 hour)

## Requirements

- Python 3.7+
- Google account for Google Sheets
- Google Cloud project with Sheets API enabled
- Internet connection

## Dependencies

All dependencies are in `requirements.txt`:
- `requests`: HTTP requests
- `beautifulsoup4`: HTML parsing
- `google-auth-oauthlib`: Google authentication
- `google-api-python-client`: Google Sheets API
- `python-dotenv`: Environment configuration
- `schedule`: Task scheduling

## Advanced Usage

### Tracking Multiple Sheets

Create separate trackers for different products:

```python
from src.tracker import PriceTracker

# Track to different sheets
tracker1 = PriceTracker("SHEETS_ID_1")
tracker1.track_product("https://shopee.com/product-1")

tracker2 = PriceTracker("SHEETS_ID_2")
tracker2.track_product("https://shopee.com/product-2")
```

### Custom Script Integration

```python
from src.scraper import ShopeeScraper
from src.google_sheets import GoogleSheetsManager

scraper = ShopeeScraper()
sheets = GoogleSheetsManager("YOUR_SHEETS_ID")

# Scrape product
product = scraper.scrape_product("https://shopee.com/product")

# Save to Google Sheets
sheets.append_price_data(product)
```

## Limitations

- Shopee changes page structure frequently - may need updates
- Web scraping depends on page structure
- Rate limiting from Shopee after many requests
- Google Sheets API has quotas

## Future Enhancements

- [ ] Support for multiple Shopee regions
- [ ] Email notifications on price drops
- [ ] Telegram bot integration
- [ ] Web dashboard
- [ ] REST API
- [ ] Database backend option
- [ ] Price comparison across sellers

## Support & Issues

For issues or questions:
1. Check `logs/` directory for error details
2. Verify credentials.json is valid
3. Ensure .env configuration is correct
4. Check if product URLs are valid

## License

This project is provided as-is for educational and personal use.

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

---

**Happy tracking!** 📊

For API documentation, see:
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Shopee Documentation](https://shopee.com)
