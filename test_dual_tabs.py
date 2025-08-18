"""
Test script for dual-tab functionality
"""

from sheets_manager import GoogleSheetsManager
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_dual_tabs():
    """Test the dual-tab functionality"""
    sheets_manager = GoogleSheetsManager()
    
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
    
    print("Testing dual-tab functionality...")
    print("=" * 50)
    
    # Test authentication
    print("Testing authentication...")
    if not sheets_manager.authenticate():
        print("❌ Authentication failed")
        return
    
    print("✅ Authentication successful")
    
    # Test sheet creation
    print("\nTesting sheet creation...")
    if not sheets_manager.get_or_create_sheet():
        print("❌ Sheet creation failed")
        return
    
    print("✅ Sheet creation successful")
    
    # Test data upload
    print("\nTesting data upload to dual tabs...")
    success = sheets_manager.upload_data(test_data)
    
    if success:
        print("✅ Data upload successful")
        print("📊 Check your Google Sheet for two tabs:")
        print("   - 'AI Summer Camps' (English)")
        print("   - 'AI Summer Camps - Español' (Spanish)")
    else:
        print("❌ Data upload failed")
    
    print("\nDual-tab test completed!")

if __name__ == "__main__":
    test_dual_tabs()
