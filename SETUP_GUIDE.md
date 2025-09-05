# CodeJarvis - Simple Reminder System Setup

This guide will help you set up the simplified CodeJarvis reminder system with email notifications.

## Features

✅ **Clean Project Structure** - Removed all unnecessary files and complex calendar integrations
✅ **Simple Email Reminders** - Uses Gmail SMTP for reliable email delivery
✅ **Local Calendar** - Contest reminders appear on the home page calendar
✅ **Remind/Unremind Toggle** - Easy one-click reminder management
✅ **Automatic Email Scheduling** - 24-hour and 1-hour reminder emails

## Quick Setup

### 1. Environment Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` and add:

```env
# Flask Secret (generate a random string)
FLASK_SECRET=your-secret-key-here

# Email Configuration
EMAIL_PASSWORD=your-gmail-app-password
```

### 2. Gmail App Password Setup

1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Navigate to **Security** → **2-Step Verification**
3. Click **App passwords**
4. Generate a new app password for \"Mail\"
5. Copy the 16-character password to `EMAIL_PASSWORD` in `.env`

### 3. Install Dependencies

```bash
# Backend dependencies
cd backend
pip install -r requirements.txt

# Frontend dependencies
cd ../frontend/codej
npm install
```

### 4. Run the Application

**Option 1: Start both servers separately**

```bash
# Terminal 1 - Backend
python run.py

# Terminal 2 - Frontend
cd frontend/codej
npm start
```

**Option 2: Use the included start script**

```bash
python run.py  # This starts the backend on http://localhost:5000
```

Then in another terminal:
```bash
cd frontend/codej
npm start  # This starts the frontend on http://localhost:3000
```

### 5. Test the System

1. Open http://localhost:3000
2. Sign in with Google
3. Find a contest and click \"Remind me\"
4. Check your email for the confirmation
5. The reminder will appear in your home page calendar
6. Click \"Unremind\" to remove the reminder

## How It Works

### Email Reminders
- **Confirmation Email**: Sent immediately when you set a reminder
- **24-Hour Reminder**: Sent 1 day before the contest
- **1-Hour Reminder**: Sent 1 hour before the contest starts

### Calendar Integration
- Reminders appear on the home page calendar
- No external calendar dependencies
- Clean, simple interface

### Data Storage
- Reminders stored in `data/reminders.json`
- No database required for basic functionality
- Automatic cleanup of old reminders

## API Endpoints

### Create Reminder
```http
POST /api/reminders
Content-Type: application/json

{
  \"user_email\": \"user@example.com\",
  \"contest_name\": \"Codeforces Round 123\",
  \"contest_url\": \"https://codeforces.com/contest/123\",
  \"contest_time\": \"2025-12-31T18:00:00Z\",
  \"platform\": \"Codeforces\"
}
```

### Remove Reminder
```http
DELETE /api/reminders
Content-Type: application/json

{
  \"user_email\": \"user@example.com\",
  \"contest_name\": \"Codeforces Round 123\",
  \"contest_url\": \"https://codeforces.com/contest/123\"
}
```

### Get User Reminders
```http
GET /api/reminders/{user_email}
```

### Get Calendar Events
```http
GET /api/reminders/calendar
```

### Test Email Service
```http
POST /api/reminders/test-email
Content-Type: application/json

{
  \"email\": \"test@example.com\"
}
```

## Troubleshooting

### Email Not Sending
1. Check `EMAIL_PASSWORD` in `.env`
2. Ensure 2-Step Verification is enabled on Google account
3. Generate a new App Password
4. Test with `/api/reminders/test-email` endpoint

### Frontend Issues
1. Ensure both backend (port 5000) and frontend (port 3000) are running
2. Check browser console for errors
3. Verify user is signed in

### Calendar Not Showing
1. Check if user email is properly set
2. Verify reminders exist by checking `/api/reminders/{email}`
3. Refresh the calendar component

## File Structure

```
CodeJarvis/
├── backend/
│   ├── routes/
│   │   ├── reminders.py          # Main reminder API
│   │   └── ...
│   ├── services/
│   │   ├── simple_email.py       # Email service
│   │   ├── reminder_manager.py   # Reminder management
│   │   └── ...
│   └── app.py
├── frontend/codej/
│   ├── src/
│   │   ├── components/
│   │   │   └── SimpleCalendar.jsx # Calendar component
│   │   ├── pages/
│   │   │   └── Home.jsx          # Updated home page
│   │   └── ...
│   └── package.json
├── data/
│   └── reminders.json            # Local reminder storage
├── .env                          # Environment variables
└── README.md
```

## Security Notes

- App passwords are more secure than regular passwords
- Email service only sends from the configured sender address
- No external calendar APIs or tokens required
- Local data storage with automatic cleanup

## Support

If you encounter issues:
1. Check the console logs for error messages
2. Verify all environment variables are set correctly
3. Test the email service using the test endpoint
4. Ensure all dependencies are installed

---

**Enjoy your simplified CodeJarvis experience!** 🚀