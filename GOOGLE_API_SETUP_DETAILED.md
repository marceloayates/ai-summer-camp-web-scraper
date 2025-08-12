# Google Custom Search API Setup Guide

## Step 1: Create Google Cloud Project

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create New Project**
   - Click "Select a project" → "New Project"
   - Name: `AI Summer Camp Scraper`
   - Click "Create"

## Step 2: Enable Custom Search API

1. **Navigate to APIs**
   - In the left sidebar, click "APIs & Services" → "Library"

2. **Find Custom Search API**
   - Search for "Custom Search API"
   - Click on "Custom Search API"
   - Click "Enable"

## Step 3: Create API Key

1. **Go to Credentials**
   - Click "APIs & Services" → "Credentials"

2. **Create API Key**
   - Click "Create Credentials" → "API Key"
   - Copy the API key (you'll need this)

3. **Restrict the API Key**
   - Click "Restrict Key"
   - Under "API restrictions", select "Restrict key"
   - Choose "Custom Search API" from the dropdown
   - Click "Save"

## Step 4: Create Custom Search Engine

1. **Go to Custom Search**
   - Visit: https://cse.google.com/cse/
   - Sign in with your Google account

2. **Create New Search Engine**
   - Click "Add" button
   - Fill in the details:
     - **Sites to search**: `example.com` (or any site)
     - **Name**: `AI Summer Camp Scraper`
     - **Language**: English
   - Click "Create"

3. **Get Search Engine ID**
   - Click on your new search engine
   - Go to "Setup" tab
   - Copy the "Search engine ID" (looks like: `012345678901234567890:abcdefghijk`)

## Step 5: Configure Your Project

1. **Update .env file**
   - Open your `.env` file
   - Add these lines:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   GOOGLE_SEARCH_ENGINE_ID=your_actual_search_engine_id_here
   ```

2. **Test the Setup**
   ```bash
   source venv/bin/activate
   python google_api.py
   ```

## Step 6: Run Your Scraper

Once configured, your scraper will now use:
- ✅ **Google Custom Search API** (reliable, no bot detection)
- ✅ **Bing** (web scraping)
- ✅ **DuckDuckGo** (web scraping)

```bash
source venv/bin/activate
python scraper.py
```

## Benefits of Google Custom Search API

- ✅ **100 free searches per day**
- ✅ **No bot detection**
- ✅ **Reliable results**
- ✅ **Official Google API**
- ✅ **High-quality data**

## Troubleshooting

### "API key not valid"
- Check that you copied the API key correctly
- Make sure you enabled the Custom Search API
- Verify the API key is restricted to Custom Search API

### "Search engine not found"
- Check that you copied the Search Engine ID correctly
- Make sure the search engine is active

### "Quota exceeded"
- You've used all 100 free searches for the day
- Wait until tomorrow or upgrade to paid plan

## Cost Information

- **Free tier**: 100 searches per day
- **Paid tier**: $5 per 1,000 searches
- **Your usage**: Likely under 50 searches per day

## Next Steps

1. Follow the setup steps above
2. Test with `python google_api.py`
3. Run your scraper: `python scraper.py`
4. Check your Google Sheet for results!

The Google API will give you much better and more reliable results than web scraping.
