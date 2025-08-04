# Complete Google API Setup Guide

## Prerequisites
- ✅ Virtual environment created and activated
- ✅ Dependencies installed (`pip install -r requirements.txt`)

## Step 1: Create a Google Cloud Project

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create or Select a Project**
   - If you don't have a project, click "Select a project" → "New Project"
   - Give it a name like "AI Summer Camp Scraper"
   - Click "Create"
   - **Note down your Project ID** (you'll need this later)

## Step 2: Enable Google Sheets API

1. **Navigate to APIs & Services**
   - In the left sidebar, click "APIs & Services" → "Library"

2. **Find Google Sheets API**
   - Search for "Google Sheets API" in the search bar
   - Click on "Google Sheets API" from the results

3. **Enable the API**
   - Click the blue "Enable" button
   - Wait for the API to be enabled

## Step 3: Create Service Account Credentials

1. **Go to Credentials**
   - In the left sidebar, click "APIs & Services" → "Credentials"

2. **Create Service Account**
   - Click "Create Credentials" → "Service Account"
   - Fill in the details:
     - **Service account name**: `ai-summer-camp-scraper`
     - **Service account ID**: Leave as auto-generated
     - **Description**: `Service account for AI summer camp web scraper`
   - Click "Create and Continue"

3. **Skip Role Assignment**
   - Click "Continue" (we don't need to assign roles for this project)

4. **Complete Setup**
   - Click "Done"

## Step 4: Generate JSON Key File

1. **Access Your Service Account**
   - In the Credentials page, click on your new service account name

2. **Create Key**
   - Go to the "Keys" tab
   - Click "Add Key" → "Create new key"

3. **Choose JSON Format**
   - Select "JSON" as the key type
   - Click "Create"

4. **Download and Save**
   - The JSON file will automatically download
   - **Rename it to `credentials.json`**
   - **Move it to your project folder** (same folder as `scraper.py`)

## Step 5: Create Google Sheet

1. **Create New Spreadsheet**
   - Go to: https://sheets.google.com/
   - Click the "+" to create a new spreadsheet
   - Give it a name like "AI Summer Camp Results"

2. **Get Sheet ID**
   - Look at the URL in your browser
   - It will look like: `https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit`
   - **Copy the long string between `/d/` and `/edit`**
   - This is your Sheet ID

3. **Share with Service Account**
   - Click the "Share" button (top right)
   - **Find your service account email** in the `credentials.json` file
   - Look for the `"client_email"` field
   - Add that email address with "Editor" permissions
   - Click "Send" (you can uncheck "Notify people")

## Step 6: Configure Environment Variables

1. **Create .env File**
   - In your project folder, create a new file called `.env`
   - Add the following content:

```env
# Google Sheets Configuration
GOOGLE_SHEET_ID=your_actual_sheet_id_here

# Search Keywords (comma-separated)
SEARCH_KEYWORDS=ai summer camp,artificial intelligence summer program,ai summer camp high school,machine learning summer camp,ai summer program students
```

2. **Replace the Sheet ID**
   - Replace `your_actual_sheet_id_here` with the Sheet ID you copied in Step 5

## Step 7: Test Your Setup

1. **Run the Setup Checker**
   ```bash
   python setup_google_api.py
   ```
   - Choose option 3 to check your setup

2. **Test the Scraper**
   ```bash
   python scraper.py
   ```

## Troubleshooting Common Issues

### Issue: "Service account not found"
- Make sure you've shared the Google Sheet with the service account email
- Check that the email in `credentials.json` matches what you shared

### Issue: "Invalid credentials"
- Ensure `credentials.json` is in the same folder as your Python files
- Check that the file hasn't been corrupted during download

### Issue: "Sheet not found"
- Verify your Sheet ID is correct
- Make sure the sheet is shared with the service account

### Issue: "API not enabled"
- Go back to Google Cloud Console and ensure Google Sheets API is enabled
- Wait a few minutes for changes to propagate

## File Structure After Setup

Your project folder should look like this:
```
ai-summer-camp-web-scraper/
├── credentials.json          # Your Google API credentials
├── .env                      # Your environment variables
├── scraper.py               # Main scraper
├── sheets_manager.py        # Google Sheets integration
├── config.py                # Configuration
├── scheduler.py             # Scheduler
├── requirements.txt         # Dependencies
└── ... (other files)
```

## Security Notes

- **Never commit `credentials.json` or `.env` to version control**
- **Keep your service account credentials secure**
- **The `.gitignore` file is already configured to exclude these files**

## Next Steps

Once setup is complete:
1. Run `python scraper.py` to test
2. Run `python scheduler.py` to set up automated scraping
3. Check your Google Sheet for results!

Need help? Run `python setup_google_api.py` for interactive assistance. 