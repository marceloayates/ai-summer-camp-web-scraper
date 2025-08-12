"""
Alternative Google Search Methods to Work Around Bot Detection
"""

import requests
import time
import random
from bs4 import BeautifulSoup
import logging

class GoogleSearchAlternatives:
    def __init__(self):
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        
    def method1_rotating_agents(self, keyword, max_results=10):
        """Method 1: Rotating User Agents"""
        user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
        # Add random delay
        time.sleep(random.uniform(2, 5))
        
        search_url = f"https://www.google.com/search?q={keyword.replace(' ', '+')}&num={max_results}"
        response = self.session.get(search_url, headers=headers, timeout=20)
        
        return self._parse_google_results(response, keyword)
    
    def method2_google_apis(self, keyword, max_results=10):
        """Method 2: Use Google Custom Search API (requires API key)"""
        # This requires setting up Google Custom Search API
        # You need an API key and Custom Search Engine ID
        api_key = "YOUR_API_KEY"  # Get from Google Cloud Console
        search_engine_id = "YOUR_SEARCH_ENGINE_ID"  # Get from Custom Search
        
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': search_engine_id,
            'q': keyword,
            'num': max_results
        }
        
        response = self.session.get(url, params=params)
        return self._parse_api_results(response, keyword)
    
    def method3_serpapi(self, keyword, max_results=10):
        """Method 3: Use SerpAPI (paid service but reliable)"""
        # This is a paid service but very reliable
        api_key = "YOUR_SERPAPI_KEY"
        url = "https://serpapi.com/search"
        params = {
            'api_key': api_key,
            'engine': 'google',
            'q': keyword,
            'num': max_results
        }
        
        response = self.session.get(url, params=params)
        return self._parse_serpapi_results(response, keyword)
    
    def method4_proxy_rotation(self, keyword, max_results=10):
        """Method 4: Use proxy rotation (requires proxy list)"""
        # This requires a list of working proxies
        proxies = [
            # Add your proxy list here
            # {'http': 'http://proxy1:port', 'https': 'https://proxy1:port'},
            # {'http': 'http://proxy2:port', 'https': 'https://proxy2:port'},
        ]
        
        if proxies:
            proxy = random.choice(proxies)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            search_url = f"https://www.google.com/search?q={keyword.replace(' ', '+')}&num={max_results}"
            response = self.session.get(search_url, headers=headers, proxies=proxy, timeout=20)
            
            return self._parse_google_results(response, keyword)
        
        return []
    
    def method5_alternative_search_engines(self, keyword, max_results=10):
        """Method 5: Use alternative search engines that are more bot-friendly"""
        results = []
        
        # Try Startpage (Google results without tracking)
        try:
            startpage_url = f"https://www.startpage.com/sp/search?query={keyword.replace(' ', '+')}"
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
            response = self.session.get(startpage_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Parse Startpage results
                # (Implementation depends on Startpage's HTML structure)
                pass
        except Exception as e:
            self.logger.error(f"Startpage search failed: {e}")
        
        return results
    
    def _parse_google_results(self, response, keyword):
        """Parse Google search results"""
        results = []
        try:
            if response.status_code != 200:
                return results
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try multiple selectors
            selectors = ['div.g', 'div[data-hveid]', 'div.rc', 'div.yuRUbf']
            search_results = []
            
            for selector in selectors:
                if '.' in selector:
                    class_name = selector.split('.')[1]
                    search_results = soup.find_all('div', class_=class_name)
                else:
                    search_results = soup.select(selector)
                
                if search_results:
                    break
            
            for result in search_results:
                try:
                    links = result.find_all('a', href=True)
                    for link in links:
                        href = link.get('href', '')
                        if href.startswith('http') and 'google.com' not in href:
                            title = link.get_text().strip()
                            if title:
                                results.append({
                                    'keyword': keyword,
                                    'title': title,
                                    'url': href,
                                    'description': '',
                                    'source': 'Google'
                                })
                                break
                except:
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error parsing Google results: {e}")
        
        return results
    
    def _parse_api_results(self, response, keyword):
        """Parse Google Custom Search API results"""
        results = []
        try:
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
        except Exception as e:
            self.logger.error(f"Error parsing API results: {e}")
        
        return results
    
    def _parse_serpapi_results(self, response, keyword):
        """Parse SerpAPI results"""
        results = []
        try:
            data = response.json()
            if 'organic_results' in data:
                for item in data['organic_results']:
                    results.append({
                        'keyword': keyword,
                        'title': item.get('title', ''),
                        'url': item.get('link', ''),
                        'description': item.get('snippet', ''),
                        'source': 'SerpAPI'
                    })
        except Exception as e:
            self.logger.error(f"Error parsing SerpAPI results: {e}")
        
        return results

# Usage examples:
if __name__ == "__main__":
    searcher = GoogleSearchAlternatives()
    
    # Try different methods
    keyword = "ai summer camp"
    
    print("Method 1: Rotating User Agents")
    results1 = searcher.method1_rotating_agents(keyword)
    print(f"Found {len(results1)} results")
    
    print("\nMethod 5: Alternative Search Engines")
    results5 = searcher.method5_alternative_search_engines(keyword)
    print(f"Found {len(results5)} results")
