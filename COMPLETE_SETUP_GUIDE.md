# 🚀 CodeJarvis Complete Setup Guide

Welcome to CodeJarvis! This guide will help you get your competitive programming companion up and running with full functionality including email reminders and Google Calendar integration.

## 🎯 What's Included

Your CodeJarvis application now includes:

✅ **Backend API Server** (Python Flask) - Fully functional  
✅ **Frontend Web App** (React) - Fully functional  
✅ **Email Reminder System** - Set up with kumarshivanshsinha@gmail.com  
✅ **Google Calendar Integration** - Ready for setup  
✅ **Contest Tracking** - Codeforces, LeetCode, AtCoder support  
✅ **Statistics Dashboard** - Performance analytics  
✅ **Problem History** - Track your solutions  

## 🚀 Quick Start (Recommended)

### Method 1: One-Click Startup (Windows)
1. **Double-click** `start_codejarvis.bat` in your project folder
2. The script will automatically:
   - Check dependencies
   - Install missing packages
   - Start both servers
   - Open your browser

### Method 2: PowerShell Startup
```powershell
# Open PowerShell in project directory and run:
.\start_codejarvis.ps1
```

### Method 3: Manual Startup
```bash
# Terminal 1: Start Backend
call .venv\Scripts\activate
python run.py

# Terminal 2: Start Frontend
cd frontend\codej
npm start
```

## 📧 Email Setup (Gmail Integration)

Your email system is configured to use `kumarshivanshsinha@gmail.com`. To enable email reminders:

### Step 1: Enable Gmail App Passwords
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. **Enable 2-Factor Authentication** if not already enabled
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Select "Mail" and generate a 16-character password
5. Copy this password

### Step 2: Configure Email
1. Open `.env` file in your project root
2. Replace `your-gmail-app-password-here` with your app password:
   ```
   SMTP_PASSWORD=your-generated-16-char-password
   ```
3. Save and restart the application

### Step 3: Test Email Setup
Visit: `http://localhost:5000/api/email/config` to test your configuration

## 📅 Calendar Integration Setup

### Option A: Quick Setup (Recommended)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project: "CodeJarvis Calendar"
3. Enable the **Google Calendar API**
4. Create **OAuth 2.0 Client ID** credentials
5. Download the JSON file as `credentials.json` in your project root

### Option B: Detailed Setup
Follow the comprehensive guide in `CALENDAR_SETUP.md`

## 🌐 Application URLs

Once running, access these URLs:

- **Frontend**: http://localhost:3000 or http://localhost:3001
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health
- **Email Test**: http://localhost:5000/api/email/config
- **Stats Demo**: http://localhost:5000/api/stats

## ✨ Features Overview

### 🏆 Contest Management
- **Unified Feed**: See contests from multiple platforms
- **One-Click Reminders**: Set email and calendar reminders
- **Smart Filtering**: Filter by platform, date, difficulty

### 📊 Performance Analytics
- **Cross-Platform Stats**: Combined statistics from all platforms
- **Topic Analysis**: Strengths and weaknesses by algorithm topic
- **Progress Tracking**: Daily activity, streaks, and trends
- **Problem History**: Detailed view of all solved problems

### 📧 Smart Reminders
- **Contest Alerts**: 1 day and 1 hour before contests
- **Daily Practice**: Motivational coding reminders
- **Weekly Summaries**: Progress reports and achievements
- **Achievement Notifications**: Celebrate your milestones

### 📱 Calendar Integration
- **Auto-Scheduling**: Contest events added to Google Calendar
- **Multi-Device Sync**: Access from anywhere
- **Custom Reminders**: Set your preferred notification times
- **ICS Export**: Manual calendar import option

## 🔧 Configuration Files

### .env Configuration
```bash
# Email Settings (Required for reminders)
SMTP_USERNAME=kumarshivanshsinha@gmail.com
SMTP_PASSWORD=your-gmail-app-password-here

# Calendar Settings (Optional)
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_TOKEN_FILE=token.json

# Database (Optional - uses mock data if not available)
MONGODB_URI=mongodb://localhost:27017/contesthub
```

## 🧪 Testing Your Setup

### Backend API Tests
```bash
# Health check
curl http://localhost:5000/api/health

# Email configuration
curl http://localhost:5000/api/email/config

# Contest data
curl http://localhost:5000/api/contests

# Statistics (demo data)
curl http://localhost:5000/api/stats
```

### Frontend Tests
1. Open http://localhost:3000
2. Click "Get Started" to test Google OAuth
3. Check if contest data loads
4. Test creating reminders

### Email Tests
1. Visit: http://localhost:5000/api/email/instructions
2. Send test email: http://localhost:5000/api/email/test
3. Create contest reminder and check email

## 🐛 Troubleshooting

### Common Issues

**"Port already in use"**
- Solution: The startup script automatically handles this, or manually kill processes on ports 3000/5000

**"Backend not starting"**
- Check if virtual environment is activated
- Ensure all requirements are installed: `pip install -r backend/requirements.txt`
- Check for Python version compatibility (3.8+)

**"Frontend compilation errors"**
- Update Node.js to version 16+
- Clear cache: `npm cache clean --force`
- Reinstall: `rm -rf node_modules && npm install`

**"Email not working"**
- Verify Gmail App Password is correctly set in .env
- Check 2FA is enabled on your Google account
- Test configuration at http://localhost:5000/api/email/config

**"Google OAuth error"**
- Ensure Google Client ID/Secret are correctly configured
- Check OAuth redirect URI matches exactly
- Try clearing browser cookies/localStorage

### Log Files and Debugging

**Backend Logs**: Check console output for detailed error messages  
**Frontend Logs**: Open browser developer tools (F12) > Console  
**Email Logs**: Check backend console for SMTP connection details

## 🎮 Usage Examples

### Setting Contest Reminders
1. Go to frontend homepage
2. Click "View Upcoming Contests"  
3. Click "Remind Me" on any contest
4. Check email and calendar for confirmation

### Viewing Your Stats
1. Sign in with Google
2. Go to Dashboard
3. Connect your competitive programming accounts
4. View comprehensive analytics

### Daily Coding Reminders
1. Configure your email in settings
2. Set preferred reminder time
3. Receive daily motivation emails with your progress

## 🚀 Advanced Features

### Problem Analytics
- **Filter by Difficulty**: Easy, Medium, Hard
- **Platform Filtering**: LeetCode, Codeforces, AtCoder
- **Tag-based Search**: Find problems by algorithm topics
- **Success Rate Tracking**: Monitor your improvement

### Custom Integrations
- **API Endpoints**: Build your own integrations
- **Webhook Support**: Receive real-time updates
- **Export Data**: CSV/JSON exports available

## 🆘 Need Help?

If you encounter any issues:

1. **Check the logs** in your terminal/console
2. **Verify your .env configuration** 
3. **Test individual components** using the provided URLs
4. **Restart the application** - many issues resolve with a fresh start

## 🎉 You're All Set!

Your CodeJarvis application is now fully functional with:

- ✅ Complete web application (Frontend + Backend)
- ✅ Email reminder system with kumarshivanshsinha@gmail.com
- ✅ Google Calendar integration ready
- ✅ Contest tracking from major platforms
- ✅ Comprehensive statistics and analytics
- ✅ Easy startup scripts for daily use

**Happy coding, and may your contest ratings soar! 🚀📊**

---

*Created with ❤️ for competitive programming enthusiasts*
