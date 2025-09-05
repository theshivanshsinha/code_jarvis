import os
import sys
import json
from datetime import datetime, timedelta

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.services.simple_email_service import email_service
from backend.services.reminder_service import reminder_service

def test_email_service():
    print("Testing email service...")
    
    # Test sending a reminder email
    success = email_service.send_reminder_created_email(
        user_email="test@example.com",
        contest_name="Test Contest",
        contest_date=(datetime.utcnow() + timedelta(days=1)).strftime("%B %d, %Y at %I:%M %p"),
        contest_url="https://example.com/contest/123"
    )
    
    if success:
        print("✅ Email sent successfully!")
    else:
        print("❌ Failed to send email")

def test_reminder_service():
    print("\nTesting reminder service...")
    
    # Create a test reminder
    reminder = reminder_service.create_reminder(
        user_email="test@example.com",
        contest_name="Test Contest",
        contest_url="https://example.com/contest/123",
        contest_time=datetime.utcnow() + timedelta(days=1)
    )
    
    if reminder:
        print(f"✅ Created reminder: {reminder['id']}")
        
        # Check if we can get the reminder
        reminders = reminder_service.get_user_reminders("test@example.com")
        if any(r['id'] == reminder['id'] for r in reminders):
            print("✅ Successfully retrieved reminder")
        else:
            print("❌ Could not find created reminder")
        
        # Test sending reminders
        print("\nSending test reminders...")
        reminder_service.check_and_send_reminders()
        print("✅ Checked and sent reminders")
        
        # Remove the test reminder
        if reminder_service.remove_reminder(reminder['id']):
            print("✅ Successfully removed reminder")
        else:
            print("❌ Failed to remove reminder")
    else:
        print("❌ Failed to create reminder")

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    test_email_service()
    test_reminder_service()
