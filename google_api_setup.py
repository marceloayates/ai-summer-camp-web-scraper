"""
Google Custom Search API Setup and Implementation
"""

import requests
import json
import logging
from datetime import datetime

class GoogleCustomSearch:
    def __init__(self, api_key=None, search_engine_id=None):
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        self.logger = logging.getLogger(__name__)
        
    def search(self, keyword, max_results=10):
        """Search using Google Custom Search API"""
        if not self.api_key or not self.search_engine_id:
            self.logger.error("API key or Search Engine ID not configured")
            return []
        
        results = []
        try:
            # Google API allows max 10 results per request
            num_requests = (max_results + 9) // 10  # Ceiling division
            
            for i in range(num_requests):
                start_index = i * 10 + 1  # Google uses 1-based indexing
                
                params = {
                    'key': self.api_key,
                    'cx': self.search_engine_id,
                    'q': keyword,
                    'num': min(10, max_results - i * 10),
                    'start': start_index
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
                
                # Add delay between requests to be respectful
                if i < num_requests - 1:
                    import time
                    time.sleep(1)
            
            self.logger.info(f"Found {len(results)} results from Google API for '{keyword}'")
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Google API request failed: {str(e)}")
        except json.JSONDecodeError as e:
            self.logger.error(f"Google API response parsing failed: {str(e)}")
        except Exception as e:
            self.logger.error(f"Google API search failed: {str(e)}")
        
        return results

def setup_google_api():
    """Interactive setup for Google Custom Search API"""
    print("=" * 60)
    print("GOOGLE CUSTOM SEARCH API SETUP")
    print("=" * 60)
    print()
    
    print("STEP 1: Create Google Cloud Project")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create a new project or select existing one")
    print("3. Note down your Project ID")
    print()
    
    print("STEP 2: Enable Custom Search API")
    print("1. In your project, go to 'APIs & Services' > 'Library'")
    print("2. Search for 'Custom Search API'")
    print("3. Click on it and press 'Enable'")
    print()
    
    print("STEP 3: Create API Credentials")
    print("1. Go to 'APIs & Services' > 'Credentials'")
    print("2. Click 'Create Credentials' > 'API Key'")
    print("3. Copy the API key (you'll need it)")
    print("4. Click 'Restrict Key' and select 'Custom Search API'")
    print()
    
    print("STEP 4: Create Custom Search Engine")
    print("1. Go to https://cse.google.com/cse/")
    print("2. Click 'Add' to create a new search engine")
    print("3. Enter any site (e.g., 'example.com')")
    print("4. Name it 'AI Summer Camp Scraper'")
    print("5. Click 'Create'")
    print("6. Go to 'Setup' tab and copy the 'Search engine ID'")
    print()
    
    print("STEP 5: Configure Environment")
    print("Add these to your .env file:")
    print("GOOGLE_API_KEY=your_api_key_here")
    print("GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here")
    print()
    
    # Get user input
    api_key = input("Enter your Google API Key: ").strip()
    search_engine_id = input("Enter your Search Engine ID: ").strip()
    
    if api_key and search_engine_id:
        # Test the API
        print("\nTesting Google Custom Search API...")
        searcher = GoogleCustomSearch(api_key, search_engine_id)
        test_results = searcher.search("ai summer camp", 5)
        
        if test_results:
            print(f"✅ API test successful! Found {len(test_results)} results")
            
            # Update .env file
            try:
                with open('.env', 'r') as f:
                    env_content = f.read()
                
                # Add or update the Google API variables
                if 'GOOGLE_API_KEY=' in env_content:
                    env_content = env_content.replace('GOOGLE_API_KEY=.*', f'GOOGLE_API_KEY={api_key}')
                else:
                    env_content += f'\nGOOGLE_API_KEY={api_key}'
                
                if 'GOOGLE_SEARCH_ENGINE_ID=' in env_content:
                    env_content = env_content.replace('GOOGLE_SEARCH_ENGINE_ID=.*', f'GOOGLE_SEARCH_ENGINE_ID={search_engine_id}')
                else:
                    env_content += f'\nGOOGLE_SEARCH_ENGINE_ID={search_engine_id}'
                
                with open('.env', 'w') as f:
                    f.write(env_content)
                
                print("✅ .env file updated successfully!")
                
            except Exception as e:
                print(f"❌ Error updating .env file: {e}")
                print("Please manually add the API credentials to your .env file")
        else:
            print("❌ API test failed. Please check your credentials.")
    else:
        print("❌ API key or Search Engine ID not provided.")

if __name__ == "__main__":
    setup_google_api()
