#!/usr/bin/env python3
"""
Test enhanced email templates with contest details, countdown, and registration reminders
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our email service
from backend.services.simple_email import simple_email_service

def test_enhanced_emails():
    print("🧪 Testing Enhanced Email Templates")
    print("=" * 60)
    
    # Test email configuration
    print("1️⃣ Testing email service...")
    if not simple_email_service.test_connection():
        print("❌ Email service not working - check configuration")
        return False
    print("✅ Email service ready")
    
    # Test different contest scenarios
    test_scenarios = [
        {
            "name": "Immediate Contest (2 hours)",
            "contest_name": "Codeforces Educational Round #123 (Div. 2)",
            "contest_url": "https://codeforces.com/contest/1789",
            "contest_time": datetime.utcnow() + timedelta(hours=2),
            "type": "confirmation"
        },
        {
            "name": "Tomorrow's Contest (24 hours)", 
            "contest_name": "LeetCode Weekly Contest #345",
            "contest_url": "https://leetcode.com/contest/weekly-contest-345/",
            "contest_time": datetime.utcnow() + timedelta(hours=25),
            "type": "reminder"
        },
        {
            "name": "Final Warning (30 minutes)",
            "contest_name": "AtCoder Beginner Contest #298",
            "contest_url": "https://atcoder.jp/contests/abc298",
            "contest_time": datetime.utcnow() + timedelta(minutes=30),
            "type": "final_reminder"
        }
    ]
    
    test_email = "kumarshivanshsinha@gmail.com"
    
    for i, scenario in enumerate(test_scenarios, 2):
        print(f"\\n{i}️⃣ Testing: {scenario['name']}")
        print(f"   Contest: {scenario['contest_name']}")
        print(f"   Time: {scenario['contest_time'].strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"   Email Type: {scenario['type']}")
        
        # Send test email
        result = simple_email_service.send_reminder_email(
            recipient_email=test_email,
            contest_name=scenario['contest_name'],
            contest_url=scenario['contest_url'],
            contest_time=scenario['contest_time'],
            reminder_type=scenario['type']
        )
        
        if result:
            print(f"   ✅ {scenario['type'].title()} email sent successfully!")
        else:
            print(f"   ❌ Failed to send {scenario['type']} email")
    
    print("\\n" + "=" * 60)
    print("📬 Email Test Summary:")
    print(f"📧 Check your inbox: {test_email}")
    print("🎯 You should receive 3 different types of emails:")
    print("   1. ✅ Confirmation Email - with registration reminder")
    print("   2. ⏰ 24-hour Reminder - with contest prep tips")
    print("   3. 🚨 Final Warning - with urgent countdown")
    print()
    print("🎨 New Features in Emails:")
    print("   • Detailed contest date and time")
    print("   • Smart countdown timer")
    print("   • Direct contest links")
    print("   • Registration reminders")
    print("   • Contest preparation tips")
    print("   • Urgency indicators for final reminders")
    print("   • Enhanced visual design")

def preview_countdown_formats():
    print("\\n🕐 Testing Countdown Formats:")
    print("-" * 40)
    
    # Test different time scenarios
    test_times = [
        timedelta(weeks=2, days=3, hours=5),
        timedelta(days=7, hours=2),
        timedelta(days=1, hours=3, minutes=45),
        timedelta(hours=5, minutes=30),
        timedelta(hours=1, minutes=15),
        timedelta(minutes=45),
        timedelta(minutes=5, seconds=30),
        timedelta(seconds=45)
    ]
    
    now = datetime.utcnow()
    
    for time_delta in test_times:
        contest_time = now + time_delta
        countdown = simple_email_service._time_until(contest_time)
        print(f"   {str(time_delta):20} → {countdown}")

if __name__ == "__main__":
    try:
        print("🚀 Starting enhanced email template tests...")
        print("📝 This will send actual emails to test the new features")
        print()
        
        # Preview countdown formats first
        preview_countdown_formats()
        
        # Ask for confirmation
        print("\\n" + "=" * 60)
        response = input("Send test emails? (y/n): ").lower().strip()
        
        if response == 'y' or response == 'yes':
            test_enhanced_emails()
        else:
            print("Test cancelled. You can still see the countdown formats above!")
            
    except Exception as e:
        print(f"❌ Error during tests: {e}")
        import traceback
        traceback.print_exc()