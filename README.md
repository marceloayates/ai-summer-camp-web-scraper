# AI Summer Camp Web Scraper

A Python web scraper that searches for AI summer camp applications and uploads results to Google Sheets in both English and Spanish.

## Features

- Searches multiple search engines for AI summer camp opportunities
- Extracts URLs and headers from search results
- Uploads data to Google Sheets automatically in two tabs:
  - **English Tab**: Original data in English
  - **Spanish Tab**: Translated data with Spanish headers and translated content
- Translates keywords, titles, and descriptions to Spanish
- Supports multiple search keywords
- Can run periodically or manually
- Handles up to 100 rows of data efficiently
- Automatic duplicate detection across both tabs

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Google Sheets API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API
4. Create credentials (Service Account)
5. Download the JSON credentials file
6. Rename it to `credentials.json` and place in the project root
7. Share your Google Sheet with the service account email

### 3. Environment Configuration
Create a `.env` file with:
```
GOOGLE_SHEET_ID=your_sheet_id_here
SEARCH_KEYWORDS=ai summer camp,artificial intelligence summer program
```

### 4. Create Google Sheet
Create a new Google Sheet and note the Sheet ID from the URL.

## Usage

### Manual Run
```bash
python scraper.py
```

### Scheduled Run
```bash
python scheduler.py
```

## Configuration

- Edit `config.py` to modify search engines, keywords, and settings
- Update `.env` file for Google Sheets configuration
- Modify `scraper.py` to add more data extraction fields

## Project Structure

- `scraper.py` - Main scraper logic
- `sheets_manager.py` - Google Sheets integration with dual-tab support
- `translator.py` - Translation service for English to Spanish conversion
- `scheduler.py` - Automated scheduling
- `config.py` - Configuration settings
- `credentials.json` - Google API credentials (not in repo)
- `.env` - Environment variables (not in repo)

## Translation Features

The scraper now creates two tabs in your Google Sheet:

### English Tab ("AI Summer Camps")
- Original data in English
- Headers: Keyword, Title, URL, Description, Date_Found, Source

### Spanish Tab ("AI Summer Camps - Español")
- Translated data in Spanish
- Headers: Palabra Clave, Título, URL, Descripción, Fecha_Encontrado, Fuente
- Translated fields: Keyword, Title, Description
- Untranslated fields: URL, Date_Found, Source

## Testing Translation

To test the translation functionality:
```bash
python test_translation.py
``` 