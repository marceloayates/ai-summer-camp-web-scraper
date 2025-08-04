"""
Google Sheets Manager for uploading scraped data
"""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import logging
from config import GOOGLE_SHEET_ID, CREDENTIALS_FILE, SHEET_NAME, COLUMNS

class GoogleSheetsManager:
    def __init__(self):
        self.sheet_id = GOOGLE_SHEET_ID
        self.credentials_file = CREDENTIALS_FILE
        self.sheet_name = SHEET_NAME
        self.columns = COLUMNS
        self.client = None
        self.sheet = None
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            # Define the scope
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Load credentials
            credentials = Credentials.from_service_account_file(
                self.credentials_file, 
                scopes=scope
            )
            
            # Create client
            self.client = gspread.authorize(credentials)
            self.logger.info("Successfully authenticated with Google Sheets API")
            return True
            
        except Exception as e:
            self.logger.error(f"Authentication failed: {str(e)}")
            return False
    
    def get_or_create_sheet(self):
        """Get existing sheet or create new one"""
        try:
            if not self.client:
                if not self.authenticate():
                    return False
            
            # Try to open existing sheet
            try:
                self.sheet = self.client.open_by_key(self.sheet_id)
                self.logger.info(f"Opened existing sheet: {self.sheet.title}")
            except:
                # Create new sheet if it doesn't exist
                self.sheet = self.client.create(self.sheet_name)
                self.logger.info(f"Created new sheet: {self.sheet.title}")
            
            # Get or create worksheet
            try:
                self.worksheet = self.sheet.worksheet(self.sheet_name)
            except:
                self.worksheet = self.sheet.add_worksheet(
                    title=self.sheet_name, 
                    rows=1000, 
                    cols=len(self.columns)
                )
            
            # Set up headers if sheet is empty
            if not self.worksheet.get_all_values():
                self.worksheet.append_row(self.columns)
                self.logger.info("Added headers to worksheet")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error getting/creating sheet: {str(e)}")
            return False
    
    def upload_data(self, data):
        """Upload scraped data to Google Sheets"""
        try:
            if not self.get_or_create_sheet():
                return False
            
            # Convert data to list of lists
            rows_to_upload = []
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            for item in data:
                row = [
                    item.get('keyword', ''),
                    item.get('title', ''),
                    item.get('url', ''),
                    item.get('description', ''),
                    current_date,
                    item.get('source', '')
                ]
                rows_to_upload.append(row)
            
            # Upload data
            if rows_to_upload:
                self.worksheet.append_rows(rows_to_upload)
                self.logger.info(f"Successfully uploaded {len(rows_to_upload)} rows to Google Sheets")
                return True
            else:
                self.logger.warning("No data to upload")
                return False
                
        except Exception as e:
            self.logger.error(f"Error uploading data: {str(e)}")
            return False
    
    def get_existing_urls(self):
        """Get existing URLs to avoid duplicates"""
        try:
            if not self.get_or_create_sheet():
                return set()
            
            # Get all values from the URL column (index 2)
            all_values = self.worksheet.get_all_values()
            if len(all_values) <= 1:  # Only headers or empty
                return set()
            
            # Extract URLs from column 2 (index 2)
            urls = [row[2] for row in all_values[1:] if len(row) > 2 and row[2]]
            return set(urls)
            
        except Exception as e:
            self.logger.error(f"Error getting existing URLs: {str(e)}")
            return set()
    
    def clear_sheet(self):
        """Clear all data from the sheet (keep headers)"""
        try:
            if not self.get_or_create_sheet():
                return False
            
            # Clear all data except headers
            all_values = self.worksheet.get_all_values()
            if len(all_values) > 1:
                self.worksheet.delete_rows(2, len(all_values))
                self.logger.info("Cleared all data from sheet")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error clearing sheet: {str(e)}")
            return False 