#!/usr/bin/env python3
"""
Test script to verify reminder creation and email sending
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our services
from backend.services.reminder_manager import reminder_manager
from backend.services.simple_email import simple_email_service

def test_reminder_system():
    print("🧪 Testing CodeJarvis Reminder System")
    print("=" * 50)
    
    # Test email service first
    print("1️⃣ Testing email service...")
    email_ok = simple_email_service.test_connection()
    print(f"   Email service: {'✅ Ready' if email_ok else '❌ Not working'}")
    
    if not email_ok:
        print("❌ Cannot test reminders without working email service")
        return False
    
    # Test reminder creation
    print("\n2️⃣ Testing reminder creation...")
    test_email = "kumarshivanshsinha@gmail.com"
    contest_name = "Test Contest - Reminder System"
    contest_url = "https://codeforces.com/contest/test"
    contest_time = datetime.utcnow() + timedelta(hours=2)
    
    print(f"   User Email: {test_email}")
    print(f"   Contest: {contest_name}")
    print(f"   Time: {contest_time}")
    
    # Create reminder
    try:
        reminder_id = reminder_manager.add_reminder(
            user_email=test_email,
            contest_name=contest_name,
            contest_url=contest_url,
            contest_time=contest_time,
            platform="codeforces"
        )
        
        print(f"   ✅ Reminder created with ID: {reminder_id}")
        
        # Check if reminder was saved
        reminders = reminder_manager.get_user_reminders(test_email)
        found_reminder = any(r['id'] == reminder_id for r in reminders)
        print(f"   ✅ Reminder saved: {'Yes' if found_reminder else 'No'}")
        
        # Clean up - remove the test reminder
        cleanup_success = reminder_manager.remove_reminder(reminder_id, test_email)
        print(f"   🧹 Cleanup: {'✅ Success' if cleanup_success else '❌ Failed'}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error creating reminder: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_confirmation_email():
    print("\n3️⃣ Testing confirmation email specifically...")
    
    test_email = "kumarshivanshsinha@gmail.com"
    contest_time = datetime.utcnow() + timedelta(hours=3)
    
    result = simple_email_service.send_reminder_email(
        recipient_email=test_email,
        contest_name="Manual Test - Confirmation Email",
        contest_url="https://leetcode.com/contest/test",
        contest_time=contest_time,
        reminder_type="confirmation"
    )
    
    print(f"   Confirmation email: {'✅ Sent' if result else '❌ Failed'}")
    return result

if __name__ == "__main__":
    try:
        print("🚀 Starting reminder system tests...\n")
        
        # Test individual components
        test_reminder_system()
        test_confirmation_email()
        
        print("\n" + "=" * 50)
        print("📝 Summary:")
        print("• If email service shows ✅ Ready, then SMTP is configured correctly")
        print("• If reminder creation shows ✅ Success, then the reminder system works")
        print("• Check your email inbox for test emails")
        print("• If you're not receiving emails, check spam/junk folder")
        
    except Exception as e:
        print(f"❌ Error during tests: {e}")
        import traceback
        traceback.print_exc()