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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from config import (
    SEARCH_ENGINES, 
    SEARCH_KEYWORDS, 
    MAX_RESULTS_PER_KEYWORD, 
    DELAY_BETWEEN_REQUESTS,
    MAX_RETRIES
)
from sheets_manager import GoogleSheetsManager

class WebScraper:
    def __init__(self):
        self.sheets_manager = GoogleSheetsManager()
        self.session = requests.Session()
        self.driver = None
        
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
    
    def setup_selenium(self):
        """Setup Selenium WebDriver for dynamic content"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            self.driver = webdriver.Chrome(
                ChromeDriverManager().install(),
                options=chrome_options
            )
            self.logger.info("Selenium WebDriver setup complete")
            return True
        except Exception as e:
            self.logger.error(f"Failed to setup Selenium: {str(e)}")
            return False
    
    def search_google(self, keyword, max_results=10):
        """Search Google and extract results"""
        results = []
        try:
            # Use Selenium for Google as it has anti-bot protection
            if not self.driver:
                if not self.setup_selenium():
                    return results
            
            search_url = f"https://www.google.com/search?q={keyword.replace(' ', '+')}&num={max_results}"
            self.driver.get(search_url)
            
            # Wait for results to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.g"))
            )
            
            # Extract results
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "div.g")
            
            for result in search_results[:max_results]:
                try:
                    # Extract title and URL
                    title_element = result.find_element(By.CSS_SELECTOR, "h3")
                    link_element = result.find_element(By.CSS_SELECTOR, "a")
                    
                    title = title_element.text.strip()
                    url = link_element.get_attribute("href")
                    
                    # Extract description
                    try:
                        desc_element = result.find_element(By.CSS_SELECTOR, "div.VwiC3b")
                        description = desc_element.text.strip()
                    except:
                        description = ""
                    
                    if title and url and url.startswith('http'):
                        results.append({
                            'keyword': keyword,
                            'title': title,
                            'url': url,
                            'description': description,
                            'source': 'Google'
                        })
                        
                except Exception as e:
                    self.logger.debug(f"Error extracting result: {str(e)}")
                    continue
            
            self.logger.info(f"Found {len(results)} results from Google for '{keyword}'")
            
        except Exception as e:
            self.logger.error(f"Error searching Google: {str(e)}")
        
        return results
    
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
                    
                    if title and url and url.startswith('http'):
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
            
            self.logger.info(f"Found {len(results)} results from Bing for '{keyword}'")
            
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
                    
                    if title and url and url.startswith('http'):
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
        
        # Search Google
        google_results = self.search_google(keyword, max_results_per_engine)
        all_results.extend(google_results)
        
        time.sleep(DELAY_BETWEEN_REQUESTS)
        
        # Search Bing
        bing_results = self.search_bing(keyword, max_results_per_engine)
        all_results.extend(bing_results)
        
        time.sleep(DELAY_BETWEEN_REQUESTS)
        
        # Search DuckDuckGo
        duckduckgo_results = self.search_duckduckgo(keyword, max_results_per_engine)
        all_results.extend(duckduckgo_results)
        
        return all_results
    
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
                
                results = self.scrape_all_engines(keyword, MAX_RESULTS_PER_KEYWORD // 3)
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
            if self.driver:
                self.driver.quit()
                self.logger.info("Selenium WebDriver closed")

def main():
    """Main function to run the scraper"""
    scraper = WebScraper()
    results_count = scraper.run_scraper()
    print(f"Scraping completed. Found {results_count} new results.")

if __name__ == "__main__":
    main() 