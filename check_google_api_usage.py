"""
Check Google Custom Search API Usage and Quota
"""

import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def check_api_usage():
    """Check Google Custom Search API usage"""
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in .env file")
        return
    
    print("🔍 Checking Google Custom Search API Usage...")
    print("=" * 50)
    
    # Method 1: Check via Google Cloud Console API
    try:
        # This requires the Cloud Monitoring API to be enabled
        url = f"https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': 'test',  # Dummy search engine ID for testing
            'q': 'test'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            print("✅ API key is working")
        elif response.status_code == 403:
            print("❌ API key error or quota exceeded")
            data = response.json()
            if 'error' in data:
                print(f"Error: {data['error'].get('message', 'Unknown error')}")
        else:
            print(f"⚠️  API response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
    
    print("\n📊 How to Check Usage:")
    print("=" * 50)
    
    print("1. GOOGLE CLOUD CONSOLE:")
    print("   - Go to: https://console.cloud.google.com/")
    print("   - Select your project")
    print("   - Go to 'APIs & Services' > 'Dashboard'")
    print("   - Find 'Custom Search API'")
    print("   - Click on it to see usage metrics")
    
    print("\n2. GOOGLE CLOUD CONSOLE - QUOTAS:")
    print("   - Go to: https://console.cloud.google.com/")
    print("   - Select your project")
    print("   - Go to 'APIs & Services' > 'Quotas'")
    print("   - Search for 'Custom Search API'")
    print("   - Look for 'Queries per day'")
    
    print("\n3. GOOGLE CLOUD CONSOLE - BILLING:")
    print("   - Go to: https://console.cloud.google.com/")
    print("   - Select your project")
    print("   - Go to 'Billing'")
    print("   - Check 'Reports' for API usage")
    
    print("\n4. PROGRAMMATIC CHECK:")
    print("   - Enable Cloud Monitoring API")
    print("   - Use Google Cloud Monitoring API")
    print("   - More complex but automated")
    
    print("\n📈 USAGE ESTIMATE:")
    print("=" * 50)
    
    # Calculate estimated usage based on your scraper
    keywords = [
        'ai summer camp',
        'artificial intelligence summer program', 
        'ai summer camp high school',
        'machine learning summer camp',
        'ai summer program students'
    ]
    
    searches_per_run = len(keywords) * 3  # 3 search engines
    print(f"Keywords per run: {len(keywords)}")
    print(f"Search engines: 3 (Google API, Bing, DuckDuckGo)")
    print(f"Total searches per run: {searches_per_run}")
    print(f"Daily limit: 100 (Google API only)")
    print(f"Runs per day before hitting limit: {100 // len(keywords)}")
    
    print("\n💡 TIPS:")
    print("=" * 50)
    print("• Google API: 100 free searches per day")
    print("• Bing/DuckDuckGo: No limits")
    print("• You can run the scraper ~20 times per day")
    print("• Monitor usage in Google Cloud Console")
    print("• Set up billing alerts if needed")

def test_api_quota():
    """Test API with a simple search to check quota"""
    api_key = os.getenv('GOOGLE_API_KEY')
    search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
    
    if not api_key or not search_engine_id:
        print("❌ API credentials not configured")
        return
    
    print("\n🧪 Testing API Quota...")
    
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': search_engine_id,
            'q': 'test',
            'num': 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            print("✅ API is working - quota available")
            data = response.json()
            if 'items' in data:
                print(f"✅ Found {len(data['items'])} test results")
        elif response.status_code == 403:
            print("❌ Quota exceeded or API error")
            data = response.json()
            if 'error' in data:
                error_msg = data['error'].get('message', 'Unknown error')
                print(f"Error: {error_msg}")
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")

if __name__ == "__main__":
    check_api_usage()
    test_api_quota()
