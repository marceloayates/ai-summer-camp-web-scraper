"""
Translation service for converting English content to Spanish
"""

import logging
from googletrans import Translator
import time

class TranslationService:
    def __init__(self):
        self.translator = Translator()
        self.logger = logging.getLogger(__name__)
        
        # Spanish column headers
        self.spanish_headers = {
            'Keyword': 'Palabra Clave',
            'Title': 'Título',
            'URL': 'URL',
            'Description': 'Descripción',
            'Date_Found': 'Fecha_Encontrado',
            'Source': 'Fuente'
        }
    
    def translate_text(self, text, max_retries=3):
        """Translate text from English to Spanish with retry logic"""
        if not text or not text.strip():
            return text
        
        for attempt in range(max_retries):
            try:
                # Add delay to avoid rate limiting
                if attempt > 0:
                    time.sleep(2)
                
                result = self.translator.translate(text, src='en', dest='es')
                return result.text
                
            except Exception as e:
                self.logger.warning(f"Translation attempt {attempt + 1} failed for text '{text[:50]}...': {str(e)}")
                if attempt == max_retries - 1:
                    self.logger.error(f"Failed to translate text after {max_retries} attempts: {text[:50]}...")
                    return text  # Return original text if translation fails
                continue
        
        return text
    
    def translate_data(self, data):
        """Translate relevant fields in the data"""
        translated_data = []
        
        for item in data:
            translated_item = item.copy()
            
            # Translate keyword
            if 'keyword' in translated_item:
                translated_item['keyword'] = self.translate_text(translated_item['keyword'])
            
            # Translate title
            if 'title' in translated_item:
                translated_item['title'] = self.translate_text(translated_item['title'])
            
            # Translate description
            if 'description' in translated_item:
                translated_item['description'] = self.translate_text(translated_item['description'])
            
            translated_data.append(translated_item)
        
        return translated_data
    
    def get_spanish_headers(self):
        """Get Spanish column headers"""
        return list(self.spanish_headers.values())
    
    def translate_headers(self, english_headers):
        """Translate English headers to Spanish"""
        return [self.spanish_headers.get(header, header) for header in english_headers]
