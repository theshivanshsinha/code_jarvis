#!/usr/bin/env python3
"""
Test script to verify email functionality
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

def test_email_service():
    print("🧪 Testing CodeJarvis Email Service")
    print("=" * 50)
    
    # Check environment variables
    email_password = os.getenv("EMAIL_PASSWORD")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    print(f"📧 Sender Email: {simple_email_service.sender_email}")
    print(f"🔑 EMAIL_PASSWORD set: {'Yes' if email_password else 'No'}")
    print(f"🔑 SMTP_PASSWORD set: {'Yes' if smtp_password else 'No'}")
    print(f"🔑 Using password: {'Yes' if simple_email_service.sender_password else 'No'}")
    print()
    
    # Test connection
    print("🔌 Testing SMTP connection...")
    connection_ok = simple_email_service.test_connection()
    print(f"Connection result: {'✅ Success' if connection_ok else '❌ Failed'}")
    print()
    
    if not connection_ok:
        print("❌ Cannot proceed with email test - connection failed")
        return False
    
    # Test sending confirmation email
    print("📧 Testing confirmation email...")
    test_email = "kumarshivanshsinha@gmail.com"  # Send to same email for testing
    contest_time = datetime.utcnow() + timedelta(hours=2)
    
    result = simple_email_service.send_reminder_email(
        recipient_email=test_email,
        contest_name="Test Contest - CodeJarvis Email Service",
        contest_url="https://codeforces.com/contests",
        contest_time=contest_time,
        reminder_type="confirmation"
    )
    
    print(f"Email send result: {'✅ Success' if result else '❌ Failed'}")
    
    if result:
        print()
        print("✅ Email service is working correctly!")
        print(f"📬 Check {test_email} for the test email")
    else:
        print()
        print("❌ Email service has issues")
    
    return result

if __name__ == "__main__":
    try:
        test_email_service()
    except Exception as e:
        print(f"❌ Error during email test: {e}")
        import traceback
        traceback.print_exc()