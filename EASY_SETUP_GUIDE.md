# 🚀 Easy Setup Guide - Email & Calendar Integration

This guide will help you set up **much easier** email and calendar solutions for your CodeJarvis project!

## 🎯 Quick Overview

I've created **3 different email solutions** for you to choose from, ordered from easiest to more complex:

1. **EmailJS** (Frontend only - Super Easy!) ⭐ **RECOMMENDED FOR BEGINNERS**
2. **SendGrid** (Backend API - Easy & Reliable) ⭐ **RECOMMENDED FOR PRODUCTION**
3. **SMTP** (Traditional - Your current complex setup) ❌ **NOT RECOMMENDED**

## 📧 Email Solutions

### Option 1: EmailJS (Easiest!) 

**Perfect for**: Beginners, development, simple deployments
**Time to setup**: ~5 minutes
**Complexity**: ⭐ Very Easy

#### Setup Steps:

1. **Create EmailJS Account** (Free!)
   - Go to [https://www.emailjs.com/](https://www.emailjs.com/)
   - Sign up with your email
   - Create a new service (choose Gmail, Outlook, etc.)

2. **Get Your Keys**
   - Copy your **Service ID**, **Template IDs**, and **Public Key**

3. **Add to Frontend .env** (`frontend/.env`):
   ```env
   REACT_APP_EMAILJS_SERVICE_ID=service_xxxxxxxxx
   REACT_APP_EMAILJS_PUBLIC_KEY=your_public_key_here
   REACT_APP_EMAILJS_CONTEST_TEMPLATE=contest_reminder
   REACT_APP_EMAILJS_DAILY_TEMPLATE=daily_motivation
   REACT_APP_EMAILJS_CONFIRMATION_TEMPLATE=reminder_confirmation
   ```

4. **Install EmailJS Package**:
   ```bash
   cd frontend
   npm install @emailjs/browser
   ```

5. **Use in Your Components**:
   ```javascript
   import { emailJSService } from './services/emailjs-service';
   
   // Send contest reminder
   await emailJSService.sendContestReminder({
     userEmail: 'user@example.com',
     userName: 'John Doe',
     contestName: 'LeetCode Weekly Contest 350',
     contestDate: '2025-05-15 14:30:00',
     contestUrl: 'https://leetcode.com/contest/weekly-350/',
     timeUntil: '1 hour'
   });
   ```

**Pros**: 
- ✅ No backend required
- ✅ Works from browser
- ✅ Free tier available
- ✅ Very simple setup

**Cons**: 
- ⚠️ Limited customization
- ⚠️ Emails sent from browser

---

### Option 2: SendGrid (Best for Production!)

**Perfect for**: Production apps, reliable delivery, professional emails
**Time to setup**: ~10 minutes  
**Complexity**: ⭐⭐ Easy

#### Setup Steps:

1. **Create SendGrid Account**
   - Go to [https://sendgrid.com/](https://sendgrid.com/)
   - Sign up (free tier: 100 emails/day)
   - Verify your account

2. **Get API Key**
   - Go to Settings → API Keys
   - Create a new API key with "Mail Send" permissions
   - Copy the key (starts with `SG.`)

3. **Add to Backend .env**:
   ```env
   SENDGRID_API_KEY=SG.your_api_key_here
   FROM_EMAIL=noreply@yourdomain.com
   FROM_NAME=CodeJarvis
   ```

4. **Update requirements.txt** (already done):
   ```
   sendgrid==6.11.0
   ```

5. **Use in Your Backend**:
   ```python
   from backend.services.sendgrid_email_service import sendgrid_email_service
   
   # Send contest reminder
   success = sendgrid_email_service.send_contest_reminder(
       user_email='user@example.com',
       user_name='John Doe', 
       contest_name='LeetCode Weekly Contest 350',
       contest_date=datetime.now(),
       contest_url='https://leetcode.com/contest/',
       time_until='1 hour'
   )
   ```

**Pros**:
- ✅ Excellent deliverability
- ✅ Professional sender reputation
- ✅ Detailed analytics
- ✅ Much simpler than SMTP

**Cons**:
- ⚠️ Requires API key
- ⚠️ Cost after free tier

---

### Option 3: Traditional SMTP (Not Recommended)

**Perfect for**: When you have no other choice
**Time to setup**: ~30+ minutes  
**Complexity**: ⭐⭐⭐⭐ Complex

This is your current setup. It's complex and often fails due to:
- Gmail security restrictions
- App passwords required
- Firewall/network issues
- Authentication problems

**If you must use SMTP**, check your current `email_service.py` file.

## 📅 Calendar Integration

I've also improved your calendar integration with better OAuth handling!

### Google Calendar Setup

1. **Enable Google Calendar API**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project (if you don't have one)
   - Enable "Google Calendar API"

2. **Create OAuth Credentials**
   - Go to Credentials → Create Credentials → OAuth 2.0 Client
   - Application type: Web application
   - Add authorized redirect URIs: `http://localhost:8080/auth/google/callback`
   - Download `credentials.json`

3. **Add to Backend .env**:
   ```env
   GOOGLE_CREDENTIALS_FILE=credentials.json
   CALENDAR_TOKENS_DIR=calendar_tokens
   OAUTH_REDIRECT_URI=http://localhost:8080/auth/google/callback
   ```

4. **Use the Improved Service**:
   ```python
   from backend.services.improved_calendar_service import google_calendar_service
   
   # Get OAuth URL for user
   auth_url, state = google_calendar_service.get_oauth_url(user_id="123")
   
   # Create calendar event
   event_id = google_calendar_service.create_contest_event(
       user_id="123",
       contest_data={
           'name': 'LeetCode Contest',
           'platform': 'LeetCode', 
           'start_time': '2025-05-15T14:30:00Z',
           'duration_minutes': 90,
           'url': 'https://leetcode.com/contest/'
       }
   )
   ```

### Fallback: .ics File Generation

For users who don't want Google Calendar integration:

```python
from backend.services.improved_calendar_service import calendar_fallback_service

# Generate .ics file content
ics_content = calendar_fallback_service.generate_ics_content(contest_data)

# Save to file for download
calendar_fallback_service.save_ics_file(contest_data, 'contest.ics')
```

## 🔧 Migration from Your Current System

### Quick Migration Steps:

1. **Choose your email solution** (I recommend EmailJS for simplicity or SendGrid for production)

2. **Update your imports** in existing files:
   ```python
   # Replace this:
   from backend.services.email_service import email_service
   
   # With this (for SendGrid):
   from backend.services.sendgrid_email_service import sendgrid_email_service
   ```

3. **Update method calls**:
   ```python
   # Old way:
   email_service.send_contest_reminder_email(...)
   
   # New way (SendGrid):
   sendgrid_email_service.send_contest_reminder(...)
   ```

4. **Replace calendar service**:
   ```python
   # Replace this:
   from backend.services.calendar_service import google_calendar_service
   
   # With this:
   from backend.services.improved_calendar_service import google_calendar_service
   ```

## 🎯 Recommended Setup for Different Use Cases

### For Quick Testing/Development:
- **Email**: EmailJS (frontend only)
- **Calendar**: .ics file generation (no OAuth needed)
- **Time to setup**: 10 minutes

### For Production/Professional:
- **Email**: SendGrid (backend API)  
- **Calendar**: Google Calendar with OAuth
- **Time to setup**: 30 minutes

### For Maximum Reliability:
- **Email**: SendGrid + EmailJS as fallback
- **Calendar**: Google Calendar + .ics fallback
- **Time to setup**: 45 minutes

## 🚨 Troubleshooting

### EmailJS Not Working?
1. Check your public key in EmailJS dashboard
2. Verify template IDs match your EmailJS templates
3. Check browser console for errors
4. Make sure you're not hitting rate limits

### SendGrid Not Working?
1. Verify API key is correct (starts with `SG.`)
2. Check SendGrid dashboard for rejected emails
3. Verify sender email is authenticated
4. Check spam folder

### Calendar OAuth Issues?
1. Make sure `credentials.json` is in the right location
2. Verify redirect URI matches exactly
3. Check that Calendar API is enabled
4. Clear browser cookies and try again

## 📞 Need Help?

If you encounter issues:
1. Check the error messages in console/logs
2. Verify all environment variables are set correctly  
3. Test with simple examples first
4. Use the fallback options (EmailJS, .ics files)

The new solutions are **much simpler** than your current SMTP setup and should work much more reliably! 🚀
