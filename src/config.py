"""
Configuration management for Shopee Price Tracker
"""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class Config:
    """Base configuration"""
    
    # Project root
    PROJECT_ROOT = Path(__file__).parent.parent
    
    # Google Sheets
    GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID", "")
    GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
    
    # Shopee Configuration
    SHOPEE_PRODUCT_URLS = os.getenv(
        "SHOPEE_PRODUCT_URLS", 
        ""
    ).split(",") if os.getenv("SHOPEE_PRODUCT_URLS") else []
    
    # Scheduling
    CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 3600))  # 1 hour
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_PATH = PROJECT_ROOT / "logs"
    
    # Request settings
    REQUEST_TIMEOUT = 10
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    # Ensure directories exist
    LOG_PATH.mkdir(exist_ok=True)

config = Config()
