"""
Test script for translation functionality
"""

from translator import TranslationService
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_translation():
    """Test the translation service"""
    translator = TranslationService()
    
    # Test data
    test_data = [
        {
            'keyword': 'ai summer camp',
            'title': 'AI Summer Camp for High School Students',
            'url': 'https://example.com/ai-camp',
            'description': 'Join our artificial intelligence summer program for high school students',
            'source': 'Google'
        },
        {
            'keyword': 'machine learning program',
            'title': 'Machine Learning Summer Institute',
            'url': 'https://example.com/ml-institute',
            'description': 'Learn machine learning and deep learning techniques',
            'source': 'Bing'
        }
    ]
    
    print("Testing translation service...")
    print("=" * 50)
    
    # Test individual text translation
    test_text = "AI Summer Camp for High School Students"
    translated_text = translator.translate_text(test_text)
    print(f"Original: {test_text}")
    print(f"Translated: {translated_text}")
    print()
    
    # Test data translation
    print("Translating test data...")
    translated_data = translator.translate_data(test_data)
    
    for i, (original, translated) in enumerate(zip(test_data, translated_data)):
        print(f"Item {i+1}:")
        print(f"  Keyword: {original['keyword']} -> {translated['keyword']}")
        print(f"  Title: {original['title']} -> {translated['title']}")
        print(f"  Description: {original['description']} -> {translated['description']}")
        print()
    
    # Test headers
    print("Spanish headers:")
    spanish_headers = translator.get_spanish_headers()
    print(spanish_headers)
    
    print("\nTranslation test completed!")

if __name__ == "__main__":
    test_translation()
