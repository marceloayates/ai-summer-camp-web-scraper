"""
Helper script to guide users through Google API setup
"""

import os
import json

def print_setup_instructions():
    """Print step-by-step Google API setup instructions"""
    print("=" * 60)
    print("GOOGLE SHEETS API SETUP INSTRUCTIONS")
    print("=" * 60)
    print()
    
    print("STEP 1: Create a Google Cloud Project")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Click 'Select a project' or create a new one")
    print("3. Note down your Project ID")
    print()
    
    print("STEP 2: Enable Google Sheets API")
    print("1. In your project, go to 'APIs & Services' > 'Library'")
    print("2. Search for 'Google Sheets API'")
    print("3. Click on it and press 'Enable'")
    print()
    
    print("STEP 3: Create Service Account Credentials")
    print("1. Go to 'APIs & Services' > 'Credentials'")
    print("2. Click 'Create Credentials' > 'Service Account'")
    print("3. Fill in the details:")
    print("   - Service account name: 'ai-summer-camp-scraper'")
    print("   - Service account ID: auto-generated")
    print("   - Description: 'Service account for AI summer camp web scraper'")
    print("4. Click 'Create and Continue'")
    print("5. Skip role assignment (click 'Continue')")
    print("6. Click 'Done'")
    print()
    
    print("STEP 4: Generate JSON Key")
    print("1. Click on your new service account")
    print("2. Go to 'Keys' tab")
    print("3. Click 'Add Key' > 'Create new key'")
    print("4. Choose 'JSON' format")
    print("5. Click 'Create'")
    print("6. Download the JSON file")
    print("7. Rename it to 'credentials.json' and place it in this project folder")
    print()
    
    print("STEP 5: Create Google Sheet")
    print("1. Go to https://sheets.google.com/")
    print("2. Create a new spreadsheet")
    print("3. Note the Sheet ID from the URL:")
    print("   https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE/edit")
    print("4. Share the sheet with your service account email")
    print("   (found in credentials.json under 'client_email')")
    print()
    
    print("STEP 6: Configure Environment")
    print("1. Copy 'env_example.txt' to '.env'")
    print("2. Update the GOOGLE_SHEET_ID with your actual sheet ID")
    print("3. Optionally update SEARCH_KEYWORDS")
    print()

def create_env_file():
    """Create .env file with user input"""
    print("Let's create your .env file:")
    print()
    
    sheet_id = input("Enter your Google Sheet ID: ").strip()
    
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
    
    print()
    print("✅ .env file created successfully!")
    print()

def check_setup():
    """Check if setup is complete"""
    print("Checking setup...")
    print()
    
    # Check for credentials.json
    if os.path.exists('credentials.json'):
        print("✅ credentials.json found")
        try:
            with open('credentials.json', 'r') as f:
                creds = json.load(f)
            print(f"✅ Service account email: {creds.get('client_email', 'Not found')}")
        except:
            print("❌ credentials.json is not valid JSON")
    else:
        print("❌ credentials.json not found")
    
    # Check for .env file
    if os.path.exists('.env'):
        print("✅ .env file found")
        try:
            with open('.env', 'r') as f:
                env_content = f.read()
            if 'GOOGLE_SHEET_ID=' in env_content:
                print("✅ GOOGLE_SHEET_ID configured")
            else:
                print("❌ GOOGLE_SHEET_ID not found in .env")
        except:
            print("❌ Error reading .env file")
    else:
        print("❌ .env file not found")
    
    print()

def main():
    """Main function"""
    print("AI Summer Camp Web Scraper - Google API Setup")
    print("=" * 50)
    print()
    
    while True:
        print("Choose an option:")
        print("1. Show setup instructions")
        print("2. Create .env file")
        print("3. Check current setup")
        print("4. Exit")
        print()
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            print_setup_instructions()
        elif choice == '2':
            create_env_file()
        elif choice == '3':
            check_setup()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")
        
        print()

if __name__ == "__main__":
    main() 