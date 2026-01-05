"""
Google Sheets integration for price tracking
"""
from typing import List, Dict, Optional
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import discovery
from config import config
from logger import app_logger
import os
from pathlib import Path

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class GoogleSheetsManager:
    """Manage Google Sheets for price tracking"""
    
    def __init__(self, spreadsheet_id: str = None, credentials_file: str = None):
        """
        Initialize Google Sheets manager
        
        Args:
            spreadsheet_id: Google Sheets ID
            credentials_file: Path to credentials JSON file
        """
        self.spreadsheet_id = spreadsheet_id or config.GOOGLE_SHEETS_ID
        self.credentials_file = credentials_file or config.GOOGLE_CREDENTIALS_FILE
        self.service = None
        
        if not self.spreadsheet_id:
            raise ValueError("GOOGLE_SHEETS_ID not configured")
        
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            if not os.path.exists(self.credentials_file):
                raise FileNotFoundError(
                    f"Credentials file not found: {self.credentials_file}\n"
                    f"Please set up Google API credentials (see README.md)"
                )
            
            # Try service account authentication first
            try:
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_file,
                    scopes=SCOPES
                )
                app_logger.info("Authenticated using service account credentials")
            except Exception:
                # Fall back to OAuth2 authentication
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file,
                    scopes=SCOPES
                )
                credentials = flow.run_local_server(port=0)
                app_logger.info("Authenticated using OAuth2")
            
            self.service = discovery.build('sheets', 'v4', credentials=credentials)
            app_logger.info("Google Sheets API authenticated successfully")
            
        except Exception as e:
            app_logger.error(f"Authentication error: {e}")
            raise
    
    def _get_sheet_names(self) -> List[str]:
        """Get all sheet names in the spreadsheet"""
        try:
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            return [sheet['properties']['title'] for sheet in spreadsheet['sheets']]
        except Exception as e:
            app_logger.error(f"Error getting sheet names: {e}")
            return []
    
    def _create_sheet(self, sheet_name: str) -> bool:
        """
        Create a new sheet
        
        Args:
            sheet_name: Name of the sheet to create
            
        Returns:
            True if created successfully
        """
        try:
            request_body = {
                'requests': [
                    {
                        'addSheet': {
                            'properties': {
                                'title': sheet_name
                            }
                        }
                    }
                ]
            }
            
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=request_body
            ).execute()
            
            app_logger.info(f"Sheet created: {sheet_name}")
            return True
        except Exception as e:
            app_logger.error(f"Error creating sheet: {e}")
            return False
    
    def initialize_sheet(self, sheet_name: str = "Price Tracker") -> bool:
        """
        Initialize a sheet with headers
        
        Args:
            sheet_name: Name of the sheet
            
        Returns:
            True if successful
        """
        try:
            sheet_names = self._get_sheet_names()
            
            # Create sheet if it doesn't exist
            if sheet_name not in sheet_names:
                self._create_sheet(sheet_name)
            
            # Write headers
            headers = [
                ['Product Name', 'Product ID', 'Price', 'Discount (%)', 
                 'Shop Name', 'Rating', 'URL', 'Timestamp']
            ]
            
            range_name = f"'{sheet_name}'!A1:H1"
            
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body={'values': headers}
            ).execute()
            
            app_logger.info(f"Sheet initialized: {sheet_name}")
            return True
        except Exception as e:
            app_logger.error(f"Error initializing sheet: {e}")
            return False
    
    def append_price_data(self, product_data: Dict, sheet_name: str = "Price Tracker") -> bool:
        """
        Append price data to sheet
        
        Args:
            product_data: Product information dictionary
            sheet_name: Sheet name
            
        Returns:
            True if successful
        """
        try:
            values = [[
                product_data.get('name', ''),
                product_data.get('product_id', ''),
                product_data.get('price', ''),
                product_data.get('discount', ''),
                product_data.get('shop_name', ''),
                product_data.get('rating', ''),
                product_data.get('url', ''),
                product_data.get('timestamp', '')
            ]]
            
            range_name = f"'{sheet_name}'!A:H"
            
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body={'values': values}
            ).execute()
            
            app_logger.info(f"Data appended: {product_data.get('name')}")
            return True
        except Exception as e:
            app_logger.error(f"Error appending data: {e}")
            return False
    
    def append_multiple(self, products_data: List[Dict], 
                       sheet_name: str = "Price Tracker") -> int:
        """
        Append multiple product records
        
        Args:
            products_data: List of product dictionaries
            sheet_name: Sheet name
            
        Returns:
            Number of records appended
        """
        count = 0
        for product in products_data:
            if self.append_price_data(product, sheet_name):
                count += 1
        return count
    
    def get_latest_prices(self, sheet_name: str = "Price Tracker") -> List[Dict]:
        """
        Get latest price data from sheet
        
        Args:
            sheet_name: Sheet name
            
        Returns:
            List of price records
        """
        try:
            range_name = f"'{sheet_name}'!A:H"
            
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            rows = result.get('values', [])
            
            if not rows:
                return []
            
            # Skip header row
            headers = rows[0]
            products = []
            
            for row in rows[1:]:
                if len(row) >= len(headers):
                    product = {
                        headers[i]: row[i] for i in range(len(headers))
                    }
                    products.append(product)
            
            return products
        except Exception as e:
            app_logger.error(f"Error getting data: {e}")
            return []
    
    def create_summary_sheet(self, sheet_name: str = "Summary") -> bool:
        """
        Create a summary sheet with price changes
        
        Args:
            sheet_name: Summary sheet name
            
        Returns:
            True if successful
        """
        try:
            sheet_names = self._get_sheet_names()
            
            if sheet_name not in sheet_names:
                self._create_sheet(sheet_name)
            
            headers = [
                ['Product Name', 'Latest Price', 'Previous Price', 'Change', 'Change %']
            ]
            
            range_name = f"'{sheet_name}'!A1:E1"
            
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body={'values': headers}
            ).execute()
            
            app_logger.info(f"Summary sheet created: {sheet_name}")
            return True
        except Exception as e:
            app_logger.error(f"Error creating summary sheet: {e}")
            return False
