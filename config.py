"""
Configuration settings for the AI Summer Camp Web Scraper
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Sheets Configuration
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID', '')
CREDENTIALS_FILE = 'credentials.json'

# Search Configuration
DEFAULT_KEYWORDS = [
    'ai summer camp 2024',
    'artificial intelligence summer program high school',
    'ai summer camp application deadline',
    'machine learning summer camp students',
    'ai summer program registration',
    'artificial intelligence summer institute',
    'ai summer academy high school',
    'machine learning summer program apply'
]

# Get keywords from environment or use defaults
SEARCH_KEYWORDS = os.getenv('SEARCH_KEYWORDS', '').split(',') if os.getenv('SEARCH_KEYWORDS') else DEFAULT_KEYWORDS

# Search Engines Configuration
SEARCH_ENGINES = {
    'google': {
        'base_url': 'https://www.google.com/search',
        'params': {
            'q': '',
            'num': 10,  # Number of results
            'start': 0
        },
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    },
    'bing': {
        'base_url': 'https://www.bing.com/search',
        'params': {
            'q': '',
            'count': 10,
            'first': 0
        },
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }
}

# Scraping Configuration
MAX_RESULTS_PER_KEYWORD = 20
DELAY_BETWEEN_REQUESTS = 2  # seconds
MAX_RETRIES = 3

# Google Sheets Configuration
SHEET_NAME = 'AI Summer Camps'
SPANISH_SHEET_NAME = 'AI Summer Camps - Español'
COLUMNS = ['Keyword', 'Title', 'URL', 'Description', 'Date_Found', 'Source']

# Scheduling Configuration
SCHEDULE_INTERVAL_HOURS = 24  # Run every 24 hours
SCHEDULE_TIME = '09:00'  # Run at 9 AM

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FILE = 'scraper.log' 