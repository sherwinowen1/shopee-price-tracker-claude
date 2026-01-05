"""
Setup script for Shopee Price Tracker
Installs dependencies and configures Google Sheets authentication
"""

import subprocess
import sys
import os
import json
import webbrowser
from pathlib import Path

def install_dependencies():
    """Install required packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✓ Dependencies installed\n")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies\n")
        return False

def setup_env_file():
    """Create .env file"""
    if os.path.exists('.env'):
        print("✓ .env file already exists\n")
        return True
    
    try:
        with open('.env.example', 'r') as src:
            content = src.read()
        with open('.env', 'w') as dst:
            dst.write(content)
        print("✓ Created .env file from template")
        print("  Edit .env to add your Google Sheets ID and product URLs\n")
        return True
    except Exception as e:
        print(f"✗ Failed to create .env: {e}\n")
        return False

def setup_google_credentials():
    """Setup Google Sheets API credentials"""
    print("Google Sheets API Setup")
    print("=" * 60)
    
    if os.path.exists('credentials.json'):
        print("✓ credentials.json already exists\n")
        return True
    
    print("""
To use Google Sheets integration, you need to:

1. Go to Google Cloud Console: https://console.cloud.google.com
2. Create a new project or select existing one
3. Enable Google Sheets API
4. Create OAuth 2.0 Client ID (Desktop application)
5. Download credentials as JSON
6. Save as 'credentials.json' in this directory

Alternatively, for service account:
1. Create a Service Account in Google Cloud Console
2. Generate JSON key
3. Save as 'credentials.json'

Documentation: https://developers.google.com/sheets/api/quickstart/python
    """)
    
    print("Have you downloaded credentials.json? (yes/no): ", end='')
    response = input().strip().lower()
    
    if response == 'yes':
        print("✓ Credentials setup acknowledged")
        return True
    else:
        print("Please download credentials.json and try again")
        return False

def setup_google_sheets_id():
    """Get Google Sheets ID from user"""
    print("\nGoogle Sheets Setup")
    print("=" * 60)
    
    # Check if already in .env
    try:
        with open('.env', 'r') as f:
            content = f.read()
            if 'GOOGLE_SHEETS_ID=' in content and 'your_google_sheet_id_here' not in content:
                print("✓ Google Sheets ID already configured in .env\n")
                return True
    except:
        pass
    
    print("""
To use this tracker, you need a Google Sheet:

1. Go to https://sheets.google.com
2. Create a new spreadsheet
3. Copy the Spreadsheet ID from the URL
   (It's the long string between /d/ and /edit)
   Example: 1BxiMVs0XRA5nFMKUVfIEdidaQxfuJXvPYU76xm1V-EE
    """)
    
    sheet_id = input("Enter your Google Sheets ID: ").strip()
    
    if sheet_id:
        # Update .env file
        try:
            with open('.env', 'r') as f:
                lines = f.readlines()
            
            with open('.env', 'w') as f:
                for line in lines:
                    if line.startswith('GOOGLE_SHEETS_ID='):
                        f.write(f'GOOGLE_SHEETS_ID={sheet_id}\n')
                    else:
                        f.write(line)
            
            print(f"✓ Google Sheets ID saved to .env\n")
            return True
        except Exception as e:
            print(f"✗ Failed to update .env: {e}\n")
            return False
    else:
        print("⚠ Skipped Google Sheets ID setup\n")
        return False

def add_sample_products():
    """Add sample product URLs"""
    print("Product Configuration")
    print("=" * 60)
    print("""
You can add products to track in the .env file using SHOPEE_PRODUCT_URLS:

Example:
SHOPEE_PRODUCT_URLS=https://shopee.com/product1,https://shopee.com/product2

Or use the --url flag to track a single product:
python track.py --url https://shopee.com/your-product
    """)
    
    response = input("Add sample URLs to .env? (yes/no): ").strip().lower()
    
    if response == 'yes':
        try:
            with open('.env', 'r') as f:
                content = f.read()
            
            if 'SHOPEE_PRODUCT_URLS=' in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('SHOPEE_PRODUCT_URLS='):
                        lines[i] = 'SHOPEE_PRODUCT_URLS=https://shopee.com/product-example'
                        break
                
                with open('.env', 'w') as f:
                    f.write('\n'.join(lines))
            
            print("✓ Sample URL added to .env (update with your actual URLs)\n")
            return True
        except Exception as e:
            print(f"✗ Failed to update .env: {e}\n")
            return False
    else:
        print("⚠ Skipped sample URLs\n")
        return True

def create_directories():
    """Create necessary directories"""
    dirs = ['logs']
    for dir_name in dirs:
        try:
            os.makedirs(dir_name, exist_ok=True)
        except Exception as e:
            print(f"✗ Failed to create {dir_name}/: {e}")
            return False
    return True

def main():
    """Run setup"""
    print("\n" + "=" * 60)
    print("Shopee Price Tracker - Setup")
    print("=" * 60 + "\n")
    
    # Step 1: Directories
    print("Step 1: Creating directories...")
    if not create_directories():
        sys.exit(1)
    print()
    
    # Step 2: Dependencies
    print("Step 2: Installing dependencies...")
    if not install_dependencies():
        sys.exit(1)
    
    # Step 3: Environment
    print("Step 3: Setting up environment...")
    if not setup_env_file():
        sys.exit(1)
    
    # Step 4: Google Credentials
    print("Step 4: Google Sheets API credentials...")
    if not setup_google_credentials():
        print("⚠ Skipped Google credentials setup")
    print()
    
    # Step 5: Google Sheets ID
    print("Step 5: Google Sheets ID...")
    setup_google_sheets_id()
    
    # Step 6: Product URLs
    print("Step 6: Product configuration...")
    add_sample_products()
    
    # Summary
    print("=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("""
Next steps:
1. Edit .env file with your settings:
   - GOOGLE_SHEETS_ID: Your Google Sheet ID
   - SHOPEE_PRODUCT_URLS: Comma-separated product URLs
   
2. Place credentials.json in this directory
   (Download from Google Cloud Console)

3. Run the tracker:
   python track.py              # Track once
   python track.py --schedule   # Run scheduler
   python track.py --url URL    # Track specific URL

For more information, see README.md
    """)

if __name__ == "__main__":
    main()
