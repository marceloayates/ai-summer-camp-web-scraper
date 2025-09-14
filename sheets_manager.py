"""
Google Sheets Manager for uploading scraped data
"""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import logging
from config import GOOGLE_SHEET_ID, CREDENTIALS_FILE, SHEET_NAME, SPANISH_SHEET_NAME, COLUMNS
from translator import TranslationService

class GoogleSheetsManager:
    def __init__(self):
        self.sheet_id = GOOGLE_SHEET_ID
        self.credentials_file = CREDENTIALS_FILE
        self.sheet_name = SHEET_NAME
        self.columns = COLUMNS
        self.client = None
        self.sheet = None
        self.translator = TranslationService()
        
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
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error getting/creating sheet: {str(e)}")
            return False
    
    def get_or_create_worksheet(self, worksheet_name, headers):
        """Get existing worksheet or create new one"""
        try:
            # Get or create worksheet
            try:
                worksheet = self.sheet.worksheet(worksheet_name)
                self.logger.info(f"Opened existing worksheet: {worksheet_name}")
            except:
                worksheet = self.sheet.add_worksheet(
                    title=worksheet_name, 
                    rows=1000, 
                    cols=len(headers)
                )
                self.logger.info(f"Created new worksheet: {worksheet_name}")
            
            # Set up headers if worksheet is empty
            if not worksheet.get_all_values():
                worksheet.append_row(headers)
                self.logger.info(f"Added headers to worksheet: {worksheet_name}")
            
            return worksheet
            
        except Exception as e:
            self.logger.error(f"Error getting/creating worksheet {worksheet_name}: {str(e)}")
            return None
    
    def upload_data(self, data):
        """Upload scraped data to Google Sheets in both English and Spanish"""
        try:
            if not self.get_or_create_sheet():
                return False
            
            # Get or create English worksheet
            english_worksheet = self.get_or_create_worksheet(self.sheet_name, self.columns)
            if not english_worksheet:
                return False
            
            # Get or create Spanish worksheet
            spanish_headers = self.translator.get_spanish_headers()
            spanish_worksheet = self.get_or_create_worksheet(SPANISH_SHEET_NAME, spanish_headers)
            if not spanish_worksheet:
                return False
            
            # Prepare English data
            english_rows = []
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            for item in data:
                row = [
                    item.get('title', ''),
                    item.get('url', ''),
                    item.get('category', ''),
                    item.get('description', ''),
                    item.get('source', '')
                ]
                english_rows.append(row)
            
            # Upload English data
            if english_rows:
                english_worksheet.append_rows(english_rows)
                self.logger.info(f"Successfully uploaded {len(english_rows)} rows to English worksheet")
            
            # Translate data for Spanish worksheet
            self.logger.info("Translating data to Spanish...")
            translated_data = self.translator.translate_data(data)
            
            # Prepare Spanish data
            spanish_rows = []
            for item in translated_data:
                row = [
                    item.get('title', ''),
                    item.get('url', ''),
                    item.get('category', ''),
                    item.get('description', ''),
                    item.get('source', '')
                ]
                spanish_rows.append(row)
            
            # Upload Spanish data
            if spanish_rows:
                spanish_worksheet.append_rows(spanish_rows)
                self.logger.info(f"Successfully uploaded {len(spanish_rows)} rows to Spanish worksheet")
            
            return True
                
        except Exception as e:
            self.logger.error(f"Error uploading data: {str(e)}")
            return False
    
    def get_existing_urls(self):
        """Get existing URLs to avoid duplicates from both worksheets"""
        try:
            if not self.get_or_create_sheet():
                return set()
            
            urls = set()
            
            # Get URLs from English worksheet
            try:
                english_worksheet = self.get_or_create_worksheet(self.sheet_name, self.columns)
                if english_worksheet:
                    all_values = english_worksheet.get_all_values()
                    if len(all_values) > 1:  # More than just headers
                        urls.update([row[2] for row in all_values[1:] if len(row) > 2 and row[2]])
            except Exception as e:
                self.logger.warning(f"Error getting URLs from English worksheet: {str(e)}")
            
            # Get URLs from Spanish worksheet
            try:
                spanish_headers = self.translator.get_spanish_headers()
                spanish_worksheet = self.get_or_create_worksheet(SPANISH_SHEET_NAME, spanish_headers)
                if spanish_worksheet:
                    all_values = spanish_worksheet.get_all_values()
                    if len(all_values) > 1:  # More than just headers
                        urls.update([row[2] for row in all_values[1:] if len(row) > 2 and row[2]])
            except Exception as e:
                self.logger.warning(f"Error getting URLs from Spanish worksheet: {str(e)}")
            
            return urls
            
        except Exception as e:
            self.logger.error(f"Error getting existing URLs: {str(e)}")
            return set()
    
    def clear_sheet(self):
        """Clear all data from both worksheets (keep headers)"""
        try:
            if not self.get_or_create_sheet():
                return False
            
            success = True
            
            # Clear English worksheet
            try:
                english_worksheet = self.get_or_create_worksheet(self.sheet_name, self.columns)
                if english_worksheet:
                    all_values = english_worksheet.get_all_values()
                    if len(all_values) > 1:
                        english_worksheet.delete_rows(2, len(all_values))
                        self.logger.info("Cleared all data from English worksheet")
            except Exception as e:
                self.logger.error(f"Error clearing English worksheet: {str(e)}")
                success = False
            
            # Clear Spanish worksheet
            try:
                spanish_headers = self.translator.get_spanish_headers()
                spanish_worksheet = self.get_or_create_worksheet(SPANISH_SHEET_NAME, spanish_headers)
                if spanish_worksheet:
                    all_values = spanish_worksheet.get_all_values()
                    if len(all_values) > 1:
                        spanish_worksheet.delete_rows(2, len(all_values))
                        self.logger.info("Cleared all data from Spanish worksheet")
            except Exception as e:
                self.logger.error(f"Error clearing Spanish worksheet: {str(e)}")
                success = False
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error clearing sheets: {str(e)}")
            return False 