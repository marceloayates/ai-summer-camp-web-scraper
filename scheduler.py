"""
Scheduler for running the web scraper periodically
"""

import schedule
import time
import logging
from datetime import datetime
from config import SCHEDULE_TIME, SCHEDULE_INTERVAL_HOURS
from scraper import WebScraper

def setup_logging():
    """Setup logging for the scheduler"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('scheduler.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def run_scraper_job():
    """Job function to run the scraper"""
    logger = logging.getLogger(__name__)
    logger.info("Starting scheduled scraper job...")
    
    try:
        scraper = WebScraper()
        results_count = scraper.run_scraper()
        logger.info(f"Scheduled scraping completed. Found {results_count} new results.")
        
    except Exception as e:
        logger.error(f"Error in scheduled scraper job: {str(e)}")

def run_manual_scraper():
    """Run scraper manually"""
    logger = logging.getLogger(__name__)
    logger.info("Starting manual scraper run...")
    
    try:
        scraper = WebScraper()
        results_count = scraper.run_scraper()
        print(f"Manual scraping completed. Found {results_count} new results.")
        logger.info(f"Manual scraping completed. Found {results_count} new results.")
        
    except Exception as e:
        error_msg = f"Error in manual scraper run: {str(e)}"
        print(error_msg)
        logger.error(error_msg)

def start_scheduler():
    """Start the scheduler"""
    logger = setup_logging()
    
    # Schedule daily run at specified time
    schedule.every().day.at(SCHEDULE_TIME).do(run_scraper_job)
    
    # Also schedule every N hours as backup
    schedule.every(SCHEDULE_INTERVAL_HOURS).hours.do(run_scraper_job)
    
    logger.info(f"Scheduler started. Will run daily at {SCHEDULE_TIME} and every {SCHEDULE_INTERVAL_HOURS} hours.")
    logger.info("Press Ctrl+C to stop the scheduler.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user.")
        print("Scheduler stopped.")

def main():
    """Main function"""
    print("AI Summer Camp Web Scraper Scheduler")
    print("=" * 40)
    print("1. Start scheduler (runs automatically)")
    print("2. Run scraper once manually")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            print("Starting scheduler...")
            start_scheduler()
        elif choice == '2':
            print("Running scraper manually...")
            run_manual_scraper()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main() 