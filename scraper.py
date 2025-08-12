"""
Main web scraper for AI Summer Camp applications
"""

import requests
from bs4 import BeautifulSoup
import time
import logging
from datetime import datetime
from urllib.parse import urljoin, urlparse
import re

from config import (
    SEARCH_ENGINES, 
    SEARCH_KEYWORDS, 
    MAX_RESULTS_PER_KEYWORD, 
    DELAY_BETWEEN_REQUESTS,
    MAX_RETRIES
)
from sheets_manager import GoogleSheetsManager
from google_api import GoogleCustomSearch

class WebScraper:
    def __init__(self):
        self.sheets_manager = GoogleSheetsManager()
        self.session = requests.Session()
        self.google_api = GoogleCustomSearch()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Setup session headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_google(self, keyword, max_results=10):
        """Search Google using Custom Search API"""
        try:
            results = self.google_api.search(keyword, max_results)
            self.logger.info(f"Google API search completed for '{keyword}'")
            return results
        except Exception as e:
            self.logger.error(f"Google API search failed for '{keyword}': {str(e)}")
            return []
    
    def search_bing(self, keyword, max_results=10):
        """Search Bing and extract results"""
        results = []
        try:
            search_url = f"https://www.bing.com/search?q={keyword.replace(' ', '+')}&count={max_results}"
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find search results
            search_results = soup.find_all('li', class_='b_algo')
            
            for result in search_results[:max_results]:
                try:
                    # Extract title and URL
                    title_element = result.find('h2')
                    if not title_element:
                        continue
                    
                    link_element = title_element.find('a')
                    if not link_element:
                        continue
                    
                    title = title_element.get_text().strip()
                    url = link_element.get('href', '')
                    
                    # Extract description
                    desc_element = result.find('p')
                    description = desc_element.get_text().strip() if desc_element else ""
                    
                    # Filter out dictionary/Wikipedia results
                    if self._is_relevant_result(title, description, url):
                        results.append({
                            'keyword': keyword,
                            'title': title,
                            'url': url,
                            'description': description,
                            'source': 'Bing'
                        })
                        
                except Exception as e:
                    self.logger.debug(f"Error extracting Bing result: {str(e)}")
                    continue
            
            self.logger.info(f"Found {len(results)} relevant results from Bing for '{keyword}'")
            
        except Exception as e:
            self.logger.error(f"Error searching Bing: {str(e)}")
        
        return results
    
    def search_duckduckgo(self, keyword, max_results=10):
        """Search DuckDuckGo and extract results"""
        results = []
        try:
            search_url = f"https://duckduckgo.com/html/?q={keyword.replace(' ', '+')}"
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find search results
            search_results = soup.find_all('div', class_='result')
            
            for result in search_results[:max_results]:
                try:
                    # Extract title and URL
                    title_element = result.find('a', class_='result__a')
                    if not title_element:
                        continue
                    
                    title = title_element.get_text().strip()
                    url = title_element.get('href', '')
                    
                    # Extract description
                    desc_element = result.find('a', class_='result__snippet')
                    description = desc_element.get_text().strip() if desc_element else ""
                    
                    # Filter out dictionary/Wikipedia results
                    if self._is_relevant_result(title, description, url):
                        results.append({
                            'keyword': keyword,
                            'title': title,
                            'url': url,
                            'description': description,
                            'source': 'DuckDuckGo'
                        })
                        
                except Exception as e:
                    self.logger.debug(f"Error extracting DuckDuckGo result: {str(e)}")
                    continue
            
            self.logger.info(f"Found {len(results)} results from DuckDuckGo for '{keyword}'")
            
        except Exception as e:
            self.logger.error(f"Error searching DuckDuckGo: {str(e)}")
        
        return results
    
    def scrape_all_engines(self, keyword, max_results_per_engine=10):
        """Scrape results from all search engines"""
        all_results = []
        
        # Search Google (with fallback)
        try:
            google_results = self.search_google(keyword, max_results_per_engine)
            all_results.extend(google_results)
            self.logger.info(f"Google search completed for '{keyword}'")
        except Exception as e:
            self.logger.warning(f"Google search failed for '{keyword}': {str(e)}")
        
        time.sleep(DELAY_BETWEEN_REQUESTS)
        
        # Search Bing
        try:
            bing_results = self.search_bing(keyword, max_results_per_engine)
            all_results.extend(bing_results)
            self.logger.info(f"Bing search completed for '{keyword}'")
        except Exception as e:
            self.logger.warning(f"Bing search failed for '{keyword}': {str(e)}")
        
        time.sleep(DELAY_BETWEEN_REQUESTS)
        
        # Search DuckDuckGo
        try:
            duckduckgo_results = self.search_duckduckgo(keyword, max_results_per_engine)
            all_results.extend(duckduckgo_results)
            self.logger.info(f"DuckDuckGo search completed for '{keyword}'")
        except Exception as e:
            self.logger.warning(f"DuckDuckGo search failed for '{keyword}': {str(e)}")
        
        return all_results
    
    def _is_relevant_result(self, title, description, url):
        """Check if a search result is relevant to AI summer camps"""
        # Basic URL and title validation
        if not title or not url or not url.startswith('http'):
            return False
        
        # Convert to lowercase for easier matching
        title_lower = title.lower()
        desc_lower = description.lower()
        url_lower = url.lower()
        
        # Keywords that indicate this is NOT a summer camp program
        irrelevant_keywords = [
            'wikipedia.org',
            'dictionary.com',
            'merriam-webster',
            'urbandictionary',
            'definition',
            'meaning of',
            'what is',
            'encyclopedia',
            'wiki',
            'dictionary',
            'thesaurus',
            'synonym',
            'antonym'
        ]
        
        # Check if result contains irrelevant keywords
        for keyword in irrelevant_keywords:
            if (keyword in title_lower or 
                keyword in desc_lower or 
                keyword in url_lower):
                return False
        
        # Keywords that indicate this IS a summer camp program
        relevant_keywords = [
            'summer camp',
            'summer program',
            'summer institute',
            'summer academy',
            'summer school',
            'camp registration',
            'apply now',
            'application',
            'enrollment',
            'register',
            'program dates',
            'tuition',
            'cost',
            'fee',
            'deadline',
            'admission',
            'accepting applications'
        ]
        
        # Check if result contains relevant keywords
        for keyword in relevant_keywords:
            if (keyword in title_lower or 
                keyword in desc_lower):
                return True
        
        # If no relevant keywords found, still include if it has AI-related terms
        ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'deep learning', 'neural network']
        for keyword in ai_keywords:
            if (keyword in title_lower or 
                keyword in desc_lower):
                return True
        
        return False

    def remove_duplicates(self, results, existing_urls):
        """Remove duplicate results based on URL"""
        unique_results = []
        seen_urls = set()
        
        for result in results:
            url = result.get('url', '')
            if url and url not in seen_urls and url not in existing_urls:
                unique_results.append(result)
                seen_urls.add(url)
        
        return unique_results
    
    def run_scraper(self):
        """Main scraping function"""
        try:
            self.logger.info("Starting web scraper...")
            
            # Get existing URLs to avoid duplicates
            existing_urls = self.sheets_manager.get_existing_urls()
            self.logger.info(f"Found {len(existing_urls)} existing URLs")
            
            all_results = []
            
            # Search for each keyword
            for keyword in SEARCH_KEYWORDS:
                self.logger.info(f"Searching for: {keyword}")
                
                results = self.scrape_all_engines(keyword, MAX_RESULTS_PER_KEYWORD // 3)  # Back to 3 engines
                all_results.extend(results)
                
                time.sleep(DELAY_BETWEEN_REQUESTS)
            
            # Remove duplicates
            unique_results = self.remove_duplicates(all_results, existing_urls)
            self.logger.info(f"Found {len(unique_results)} unique new results")
            
            # Upload to Google Sheets
            if unique_results:
                success = self.sheets_manager.upload_data(unique_results)
                if success:
                    self.logger.info("Successfully uploaded data to Google Sheets")
                else:
                    self.logger.error("Failed to upload data to Google Sheets")
            else:
                self.logger.info("No new results to upload")
            
            return len(unique_results)
            
        except Exception as e:
            self.logger.error(f"Error in main scraper: {str(e)}")
            return 0
        
        finally:
            # Clean up
            pass # No Selenium cleanup needed

def main():
    """Main function to run the scraper"""
    scraper = WebScraper()
    results_count = scraper.run_scraper()
    print(f"Scraping completed. Found {results_count} new results.")

if __name__ == "__main__":
    main() 