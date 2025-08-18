# Dual-Tab Implementation for AI Summer Camp Web Scraper

## Overview

The web scraper has been enhanced to create two tabs in Google Sheets:
1. **English Tab**: Original data in English
2. **Spanish Tab**: Translated data with Spanish headers and translated content

## Changes Made

### 1. New Files Created

#### `translator.py`
- Translation service using Google Translate API
- Translates keywords, titles, and descriptions from English to Spanish
- Includes retry logic for failed translations
- Provides Spanish column headers

#### `test_translation.py`
- Test script to verify translation functionality
- Tests individual text translation and bulk data translation

#### `test_dual_tabs.py`
- Test script to verify dual-tab functionality
- Tests authentication, sheet creation, and data upload

### 2. Modified Files

#### `requirements.txt`
- Added `googletrans==4.0.0rc1` for translation functionality

#### `config.py`
- Added `SPANISH_SHEET_NAME` constant for Spanish tab name

#### `sheets_manager.py`
- **Major refactoring** to support dual tabs
- Added `TranslationService` integration
- Modified `upload_data()` to create both English and Spanish tabs
- Updated `get_existing_urls()` to check both tabs for duplicates
- Updated `clear_sheet()` to clear both tabs
- Added `get_or_create_worksheet()` method for individual worksheet management

#### `README.md`
- Updated to document dual-tab functionality
- Added translation features section
- Updated project structure

## Translation Details

### Translated Fields
- **Keyword**: Translated to Spanish
- **Title**: Translated to Spanish  
- **Description**: Translated to Spanish

### Untranslated Fields
- **URL**: Remains unchanged
- **Date_Found**: Remains unchanged
- **Source**: Remains unchanged

### Spanish Headers
- Keyword → Palabra Clave
- Title → Título
- URL → URL
- Description → Descripción
- Date_Found → Fecha_Encontrado
- Source → Fuente

## Tab Names
- **English Tab**: "AI Summer Camps"
- **Spanish Tab**: "AI Summer Camps - Español"

## Testing

### Test Translation Only
```bash
python3 test_translation.py
```

### Test Full Dual-Tab Functionality
```bash
python3 test_dual_tabs.py
```

## Usage

The scraper now automatically:
1. Scrapes data in English
2. Creates/updates the English tab with original data
3. Translates relevant fields to Spanish
4. Creates/updates the Spanish tab with translated data
5. Prevents duplicates across both tabs

## Error Handling

- Translation failures fall back to original text
- Retry logic for translation API calls
- Graceful handling of worksheet creation failures
- Comprehensive logging for debugging

## Performance Considerations

- Translation adds processing time
- Rate limiting implemented for translation API
- Batch processing for efficiency
- Caching of translated content (if needed in future)

## Future Enhancements

- Support for additional languages
- Translation quality improvements
- Caching of translations
- Custom translation dictionaries for domain-specific terms
