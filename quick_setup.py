"""
Quick Setup Script for Google API Configuration
"""

import os
import json
import webbrowser
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🚀 AI SUMMER CAMP WEB SCRAPER - QUICK SETUP")
    print("=" * 60)
    print()

def check_prerequisites():
    """Check if prerequisites are met"""
    print("📋 Checking Prerequisites...")
    
    # Check if virtual environment is activated
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is activated")
    else:
        print("⚠️  Virtual environment may not be activated")
        print("   Make sure you've activated your virtual environment")
    
    # Check if requirements are installed
    try:
        import requests
        import gspread
        import beautifulsoup4
        print("✅ Required packages are installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print()
    return True

def open_google_cloud_console():
    """Open Google Cloud Console in browser"""
    print("🌐 Opening Google Cloud Console...")
    webbrowser.open("https://console.cloud.google.com/")
    print("   Please complete Steps 1-4 in the browser")
    print("   Then return here and press Enter to continue...")
    input()

def create_env_file():
    """Create .env file with user input"""
    print("\n📝 Creating .env file...")
    
    sheet_id = input("Enter your Google Sheet ID: ").strip()
    
    if not sheet_id:
        print("❌ Sheet ID is required!")
        return False
    
    # Default keywords
    default_keywords = "ai summer camp,artificial intelligence summer program,ai summer camp high school,machine learning summer camp,ai summer program students"
    keywords = input(f"Enter search keywords (comma-separated) [default: {default_keywords}]: ").strip()
    
    if not keywords:
        keywords = default_keywords
    
    # Create .env file
    env_content = f"""# Google Sheets Configuration
GOOGLE_SHEET_ID={sheet_id}

# Search Keywords (comma-separated)
SEARCH_KEYWORDS={keywords}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")
    return True

def verify_credentials():
    """Verify credentials.json exists and is valid"""
    print("\n🔐 Verifying credentials...")
    
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        print("   Please download it from Google Cloud Console and place it in this folder")
        return False
    
    try:
        with open('credentials.json', 'r') as f:
            creds = json.load(f)
        
        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        for field in required_fields:
            if field not in creds:
                print(f"❌ Missing field in credentials.json: {field}")
                return False
        
        print("✅ credentials.json is valid")
        print(f"   Service account: {creds['client_email']}")
        return True
        
    except json.JSONDecodeError:
        print("❌ credentials.json is not valid JSON")
        return False
    except Exception as e:
        print(f"❌ Error reading credentials.json: {e}")
        return False

def test_connection():
    """Test Google Sheets connection"""
    print("\n🧪 Testing Google Sheets connection...")
    
    try:
        from sheets_manager import GoogleSheetsManager
        
        sheets_manager = GoogleSheetsManager()
        if sheets_manager.authenticate():
            print("✅ Google Sheets authentication successful!")
            
            if sheets_manager.get_or_create_sheet():
                print("✅ Google Sheets access successful!")
                return True
            else:
                print("❌ Could not access Google Sheet")
                print("   Make sure you've shared the sheet with the service account")
                return False
        else:
            print("❌ Google Sheets authentication failed")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def run_test_scrape():
    """Run a quick test scrape"""
    print("\n🔍 Running test scrape...")
    
    try:
        from scraper import WebScraper
        
        scraper = WebScraper()
        results_count = scraper.run_scraper()
        
        if results_count > 0:
            print(f"✅ Test scrape successful! Found {results_count} results")
            return True
        else:
            print("⚠️  Test scrape completed but no new results found")
            print("   This might be normal if you've already scraped recently")
            return True
            
    except Exception as e:
        print(f"❌ Test scrape failed: {e}")
        return False

def main():
    """Main setup function"""
    print_banner()
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please fix the issues above and try again.")
        return
    
    print("🎯 Let's set up your Google API access!")
    print()
    
    # Step 1: Open Google Cloud Console
    print("STEP 1: Google Cloud Console Setup")
    print("-" * 40)
    open_google_cloud_console()
    
    # Step 2: Verify credentials
    print("\nSTEP 2: Verify Credentials")
    print("-" * 40)
    if not verify_credentials():
        print("\n❌ Please download credentials.json and try again.")
        return
    
    # Step 3: Create .env file
    print("\nSTEP 3: Configure Environment")
    print("-" * 40)
    if not create_env_file():
        print("\n❌ Failed to create .env file.")
        return
    
    # Step 4: Test connection
    print("\nSTEP 4: Test Connection")
    print("-" * 40)
    if not test_connection():
        print("\n❌ Connection test failed. Please check your setup.")
        return
    
    # Step 5: Test scrape
    print("\nSTEP 5: Test Scrape")
    print("-" * 40)
    if not run_test_scrape():
        print("\n❌ Test scrape failed. Please check your setup.")
        return
    
    # Success!
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETE!")
    print("=" * 60)
    print()
    print("Your AI Summer Camp Web Scraper is ready to use!")
    print()
    print("Next steps:")
    print("1. Check your Google Sheet for results")
    print("2. Run 'python scraper.py' for manual scraping")
    print("3. Run 'python scheduler.py' for automated scraping")
    print()
    print("Happy scraping! 🚀")

if __name__ == "__main__":
    import sys
    main() 