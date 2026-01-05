# Shopee Price Tracker - Quick Start Guide

## Installation (5 minutes)

### Step 1: Download Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project
3. Enable "Google Sheets API"
4. Create OAuth 2.0 credentials (Desktop app)
5. Download as JSON and save as `credentials.json` in project folder

### Step 2: Run Setup
```bash
python setup.py
```

This will:
- Install dependencies
- Create .env file
- Prompt for Google Sheets ID
- Create necessary directories

### Step 3: Configure Products
Edit `.env` and add your product URLs:
```env
GOOGLE_SHEETS_ID=your_google_sheet_id
SHOPEE_PRODUCT_URLS=https://shopee.com/product-1,https://shopee.com/product-2
CHECK_INTERVAL=3600
```

## Usage

### Track All Products Once
```bash
python track.py
```

### Track a Single Product
```bash
python track.py --url "https://shopee.com/your-product"
```

### Run Continuous Tracking (Scheduler)
```bash
python track.py --schedule
```

This will track your products every hour (or your configured interval).

### Custom Interval
```bash
python track.py --schedule --interval 1800  # Every 30 minutes
```

## What Gets Saved to Google Sheets

Each price check creates a row with:
- Product Name
- Product ID  
- Current Price
- Discount %
- Shop Name
- Rating
- Product URL
- Timestamp

Perfect for tracking price changes over time!

## Troubleshooting

### "Credentials not found"
- Download `credentials.json` from Google Cloud Console
- Place in project root directory

### "Google Sheets ID not configured"
- Get your Spreadsheet ID from Google Sheets URL
- Add to .env: `GOOGLE_SHEETS_ID=your_id`

### Products not scraping
- Check URLs are valid Shopee product links
- Verify internet connection
- Check `logs/shopee_tracker.log` for errors

## Getting Your Google Sheets ID

1. Open your Google Sheet
2. Look at the URL: `https://docs.google.com/spreadsheets/d/{ID}/edit`
3. Copy the {ID} part
4. Add to .env: `GOOGLE_SHEETS_ID={ID}`

## Examples

See `examples.py` for code examples:
```bash
python examples.py
```

## Need Help?

- Check README.md for detailed documentation
- Look in `logs/` folder for error details
- Verify .env configuration
- Ensure credentials.json is valid

## Next Steps

1. ✅ Run setup.py
2. ✅ Configure .env with Sheets ID and product URLs  
3. ✅ Place credentials.json in project folder
4. ✅ Run: `python track.py`
5. ✅ Check your Google Sheet!

Happy tracking! 📊
