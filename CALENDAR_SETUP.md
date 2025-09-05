# 📅 Google Calendar Integration Setup

## Overview
CodeJarvis can automatically create calendar events for contest reminders, daily coding sessions, and other important events. Follow these steps to set up Google Calendar integration.

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Name your project (e.g., "CodeJarvis Calendar Integration")

## Step 2: Enable Calendar API

1. In the Google Cloud Console, go to **APIs & Services > Library**
2. Search for "Google Calendar API" 
3. Click on it and press **ENABLE**

## Step 3: Create Credentials

### Option A: OAuth 2.0 Client ID (Recommended)
1. Go to **APIs & Services > Credentials**
2. Click **CREATE CREDENTIALS > OAuth client ID**
3. Choose **Desktop application**
4. Name it "CodeJarvis Desktop"
5. Download the JSON file
6. Rename it to `credentials.json` and place it in your project root directory

### Option B: Service Account (Simpler but less secure)
1. Go to **APIs & Services > Credentials** 
2. Click **CREATE CREDENTIALS > Service account**
3. Name it "codejarvis-calendar-service"
4. Download the JSON key
5. Rename it to `service-account.json`

## Step 4: Configure Environment

Add these variables to your `.env` file:

```env
# Google Calendar Configuration
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_TOKEN_FILE=token.json
```

## Step 5: Test Integration

Run the backend server and test calendar integration:

```bash
# Test calendar authorization
curl http://localhost:5000/api/reminders/calendar/authorize

# Create a test reminder with calendar integration
curl -X POST http://localhost:5000/api/reminders \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Contest",
    "start": "2024-12-25T15:00:00Z",
    "url": "https://example.com",
    "platform": "test"
  }'
```

## Calendar Features

### ✅ What Works
- **Contest Events**: Automatically create calendar events for contests
- **Custom Reminders**: Set multiple reminder times (1 day, 1 hour, 15 min before)
- **Event Details**: Include contest URLs, platform info, and descriptions
- **Color Coding**: Different colors for different types of events

### 🔄 What's Planned
- **Daily Coding Sessions**: Recurring events for daily practice
- **Weekly Reviews**: Scheduled coding progress reviews
- **Achievement Celebrations**: Calendar events for major milestones

## Troubleshooting

### Common Issues

1. **"Credentials not found" Error**
   - Make sure `credentials.json` is in the project root
   - Check file permissions
   - Verify the file is valid JSON

2. **"OAuth Error" or "Invalid Grant"**
   - Delete `token.json` and re-authorize
   - Check system clock is accurate
   - Ensure redirect URI matches exactly

3. **"Calendar API not enabled"**
   - Go back to Google Cloud Console
   - Enable the Google Calendar API
   - Wait a few minutes for changes to propagate

4. **Permission Denied**
   - Make sure your Google account has calendar access
   - Check OAuth consent screen configuration
   - Verify required scopes are requested

### Support

If you encounter issues:
1. Check the backend logs for detailed error messages
2. Test with the `/api/email/config` endpoint first
3. Use demo mode to test functionality without full setup
4. Create an issue on the GitHub repository

## Security Notes

- **Never commit `credentials.json` or `token.json` to version control**
- Add these files to your `.gitignore`
- Use environment variables for sensitive configuration
- Consider using service accounts for production deployments

## Advanced Configuration

For production or advanced setups:

```env
# Advanced Calendar Settings
CALENDAR_DEFAULT_REMINDER_MINUTES=60,15
CALENDAR_DEFAULT_COLOR_ID=11
CALENDAR_TIME_ZONE=America/New_York
CALENDAR_MAXIMUM_EVENTS=100
```

This will give you full Google Calendar integration with your CodeJarvis app! 🚀
