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
    MAX_RETRIES,
    CATEGORIES,
    CATEGORY_KEYWORDS
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
            api_results = self.google_api.search(keyword, max_results)
            # Add categorization to Google API results
            categorized_results = []
            for result in api_results:
                category = self.categorize_result(result.get('title', ''), result.get('description', ''), result.get('url', ''))
                result['category'] = category
                categorized_results.append(result)
            
            self.logger.info(f"Google API search completed for '{keyword}'")
            return categorized_results
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
            self.logger.debug(f"Bing found {len(search_results)} raw results for '{keyword}'")
            
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
                    
                    self.logger.debug(f"Bing result: {title[:50]}... - {url}")
                    
                    # Filter out dictionary/Wikipedia results
                    if self._is_relevant_result(title, description, url):
                        category = self.categorize_result(title, description, url)
                        results.append({
                            'keyword': keyword,
                            'title': title,
                            'url': url,
                            'description': description,
                            'source': 'Bing',
                            'category': category
                        })
                        self.logger.debug(f"Bing result added: {title[:50]}...")
                    else:
                        self.logger.debug(f"Bing result filtered out: {title[:50]}...")
                        
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
                        category = self.categorize_result(title, description, url)
                        results.append({
                            'keyword': keyword,
                            'title': title,
                            'url': url,
                            'description': description,
                            'source': 'DuckDuckGo',
                            'category': category
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
        
        # Be more lenient - if it's from a search about AI summer camps, include it unless it's clearly irrelevant
        # This will catch more results that might be relevant but don't have exact keyword matches
        return True

    def categorize_result(self, title, description, url):
        """Categorize a search result based on title, description, and URL"""
        # Combine all text for analysis
        text_to_analyze = f"{title} {description} {url}".lower()
        
        # Score each category based on keyword matches
        category_scores = {}
        
        for category_key, keywords in CATEGORY_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in text_to_analyze:
                    # Weight title matches more heavily
                    if keyword.lower() in title.lower():
                        score += 5  # Increased weight for title matches
                    elif keyword.lower() in description.lower():
                        score += 3  # Increased weight for description matches
                    elif keyword.lower() in url.lower():
                        score += 1
            
            category_scores[category_key] = score
        
        # Find the category with the highest score
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            # Use the best category if it has any score, otherwise try fallback logic
            if category_scores[best_category] > 0:
                return CATEGORIES[best_category]
        
        # If no category has any score, use fallback logic
        # Try to infer from URL domain or other clues
        url_lower = url.lower()
        if any(word in url_lower for word in ['state', 'community', 'public']):
            return CATEGORIES['STATE_LOCAL_OPPORTUNITY']
        elif any(word in url_lower for word in ['online', 'course', 'platform']):
            return CATEGORIES['SELF_GUIDED_COURSES']
        elif any(word in url_lower for word in ['scholarship', 'grant', 'fund']):
            return CATEGORIES['TECHNOLOGY_SCHOLARSHIP']
        elif any(word in text_to_analyze for word in ['university', 'college', 'institute']):
            return CATEGORIES['SECONDARY_SCHOOL_FELLOWSHIP']
        else:
            # If we can't determine anything, use "Other"
            return CATEGORIES['OTHER']

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