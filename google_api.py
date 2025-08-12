"""
Google Custom Search API Implementation
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleCustomSearch:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        
    def search(self, keyword, max_results=10):
        """Search using Google Custom Search API"""
        if not self.api_key or not self.search_engine_id:
            print("Google API not configured. Please set GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID in .env")
            return []
        
        results = []
        try:
            params = {
                'key': self.api_key,
                'cx': self.search_engine_id,
                'q': keyword,
                'num': min(10, max_results)
            }
            
            response = requests.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            if 'items' in data:
                for item in data['items']:
                    results.append({
                        'keyword': keyword,
                        'title': item.get('title', ''),
                        'url': item.get('link', ''),
                        'description': item.get('snippet', ''),
                        'source': 'Google API'
                    })
            
            print(f"Found {len(results)} results from Google API for '{keyword}'")
            
        except Exception as e:
            print(f"Google API search failed: {str(e)}")
        
        return results

def setup_instructions():
    """Print setup instructions"""
    print("GOOGLE CUSTOM SEARCH API SETUP:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create project and enable Custom Search API")
    print("3. Create API key in Credentials")
    print("4. Go to https://cse.google.com/cse/")
    print("5. Create custom search engine")
    print("6. Add to .env file:")
    print("   GOOGLE_API_KEY=your_key_here")
    print("   GOOGLE_SEARCH_ENGINE_ID=your_engine_id_here")

if __name__ == "__main__":
    setup_instructions()
