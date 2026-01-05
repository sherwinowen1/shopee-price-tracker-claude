#!/usr/bin/env python3
"""
Helper script to set up Google Sheets API credentials
This will guide you through the OAuth2 authentication process
"""

import os
import json
import webbrowser
from pathlib import Path

def create_oauth_credentials():
    """
    Guide user through creating OAuth2 credentials
    """
    print("\n" + "="*70)
    print("GOOGLE SHEETS API CREDENTIALS SETUP")
    print("="*70)
    
    print("""
This script will help you set up Google API credentials for OAuth2.

STEP 1: Create Google Cloud Project
─────────────────────────────────────
1. Go to: https://console.cloud.google.com
2. Click "Select a Project" > "New Project"
3. Name it: "Shopee Price Tracker"
4. Click "Create"
5. Wait for project creation to complete

STEP 2: Enable Google Sheets API
─────────────────────────────────────
1. In Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Google Sheets API"
3. Click it, then click "Enable"
4. Wait for it to enable

STEP 3: Create OAuth2 Credentials
─────────────────────────────────────
1. Go to "APIs & Services" > "Credentials"
2. Click "+ Create Credentials"
3. Choose "OAuth client ID"
4. If prompted, click "Configure OAuth consent screen" first
   - Choose "External"
   - Fill in app name: "Shopee Price Tracker"
   - Add your email
   - Save and continue
5. Back to Credentials, click "+ Create Credentials" > "OAuth client ID"
6. Choose "Desktop application"
7. Click "Create"

STEP 4: Download Credentials
─────────────────────────────────────
1. Click the download icon (↓) next to your OAuth2 credentials
2. A JSON file will download
3. Rename it to: credentials.json
4. Move it to this project folder

STEP 5: Verify
─────────────────────────────────────
The credentials.json file should be in the same folder as this script.
    """)
    
    print("\nDo you want to open Google Cloud Console now? (yes/no): ", end="")
    response = input().strip().lower()
    
    if response == 'yes':
        webbrowser.open('https://console.cloud.google.com')
        print("Opened in browser!")
    
    print("""
After downloading credentials.json:
1. Save it in this project folder
2. Run: python track.py --url "YOUR_PRODUCT_URL"
    """)

def create_service_account_credentials():
    """
    Guide user through creating Service Account credentials
    """
    print("\n" + "="*70)
    print("GOOGLE SHEETS SERVICE ACCOUNT SETUP")
    print("="*70)
    
    print("""
Use this method for 24/7 automation without user interaction.

STEP 1: Create Service Account
─────────────────────────────────────
1. Go to: https://console.cloud.google.com
2. Go to "APIs & Services" > "Credentials"
3. Click "+ Create Credentials" > "Service Account"
4. Name: "shopee-price-tracker"
5. Click "Create and Continue"
6. Grant "Editor" role
7. Click "Continue" and "Done"

STEP 2: Create JSON Key
─────────────────────────────────────
1. Click the service account you just created
2. Go to "Keys" tab
3. Click "Add Key" > "Create new key"
4. Choose "JSON"
5. Click "Create"
6. A JSON file will download

STEP 3: Save Credentials
─────────────────────────────────────
1. Rename downloaded file to: credentials.json
2. Move it to this project folder

STEP 4: Share Google Sheet
─────────────────────────────────────
1. Open your Google Sheet
2. Click "Share" button
3. In the downloaded JSON file, find "client_email"
4. Share the sheet with that email address
5. Give it "Editor" access

STEP 5: Use It
─────────────────────────────────────
1. Put credentials.json in this folder
2. Run: python track.py --url "YOUR_PRODUCT_URL"
    """)
    
    print("\nDo you want to open Google Cloud Console? (yes/no): ", end="")
    response = input().strip().lower()
    
    if response == 'yes':
        webbrowser.open('https://console.cloud.google.com')
        print("Opened in browser!")

def verify_credentials():
    """
    Check if credentials.json exists
    """
    if os.path.exists('credentials.json'):
        print("\n✓ credentials.json found!")
        
        try:
            with open('credentials.json', 'r') as f:
                creds = json.load(f)
                if 'client_id' in creds:
                    print("  Type: OAuth2 (Desktop Application)")
                elif 'client_email' in creds:
                    print("  Type: Service Account")
                    print(f"  Email: {creds['client_email']}")
                return True
        except json.JSONDecodeError:
            print("✗ credentials.json exists but is not valid JSON")
            return False
    else:
        print("\n✗ credentials.json not found")
        print("  It should be in the project folder")
        return False

def main():
    """Main function"""
    print("\n" + "="*70)
    print("Google Sheets Credentials Setup Helper")
    print("="*70)
    
    # Check if credentials already exist
    if verify_credentials():
        print("\nYou're ready to use the tracker!")
        print("Run: python track.py --url \"YOUR_PRODUCT_URL\"")
        return
    
    print("\nChoose an authentication method:")
    print("1. OAuth2 (Easier for personal use)")
    print("2. Service Account (Better for 24/7 automation)")
    print("3. Cancel")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        create_oauth_credentials()
    elif choice == '2':
        create_service_account_credentials()
    elif choice == '3':
        print("Cancelled.")
        return
    else:
        print("Invalid choice")
        return
    
    print("\n" + "="*70)
    print("After saving credentials.json in this folder, run:")
    print("  python track.py --url \"YOUR_PRODUCT_URL\"")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
