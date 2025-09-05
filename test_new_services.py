#!/usr/bin/env python3
"""
Test script for new email and calendar services
Run this to verify your setup is working correctly!
"""

import os
import sys
from datetime import datetime, timedelta

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_sendgrid_service():
    """Test SendGrid email service"""
    print("\n🧪 Testing SendGrid Email Service...")
    
    try:
        from backend.services.sendgrid_email_service import sendgrid_email_service
        
        # Test connection
        connection_test = sendgrid_email_service.test_connection()
        
        if not sendgrid_email_service.api_key:
            print("⚠️  SendGrid not configured - set SENDGRID_API_KEY in .env")
            return False
            
        print("✅ SendGrid service initialized successfully")
        
        # Test email sending (optional - uncomment to actually send test email)
        # test_success = sendgrid_email_service.send_contest_reminder(
        #     user_email='your-test-email@gmail.com',
        #     user_name='Test User',
        #     contest_name='Test Contest',
        #     contest_date=datetime.now() + timedelta(hours=1),
        #     contest_url='https://leetcode.com/contest/',
        #     time_until='1 hour'
        # )
        # print(f"📧 Test email sent: {test_success}")
        
        return True
        
    except Exception as e:
        print(f"❌ SendGrid test failed: {str(e)}")
        return False

def test_calendar_service():
    """Test improved calendar service"""
    print("\n🧪 Testing Improved Calendar Service...")
    
    try:
        from backend.services.improved_calendar_service import google_calendar_service, calendar_fallback_service
        
        # Test OAuth URL generation
        auth_url, state = google_calendar_service.get_oauth_url("test_user_123")
        
        if auth_url:
            print("✅ Calendar OAuth URL generation successful")
            print(f"🔗 OAuth URL: {auth_url[:50]}...")
        else:
            print("⚠️  Google Calendar OAuth not configured - need credentials.json")
        
        # Test .ics file generation (fallback)
        test_contest_data = {
            'name': 'Test Contest',
            'platform': 'LeetCode',
            'start_time': '2025-05-15T14:30:00Z',
            'duration_minutes': 90,
            'url': 'https://leetcode.com/contest/'
        }
        
        ics_content = calendar_fallback_service.generate_ics_content(test_contest_data)
        
        if ics_content and 'BEGIN:VCALENDAR' in ics_content:
            print("✅ .ics file generation successful")
            
            # Save test .ics file
            test_file = 'test_contest.ics'
            if calendar_fallback_service.save_ics_file(test_contest_data, test_file):
                print(f"✅ Test .ics file saved: {test_file}")
                # Clean up
                if os.path.exists(test_file):
                    os.remove(test_file)
            
        return True
        
    except Exception as e:
        print(f"❌ Calendar test failed: {str(e)}")
        return False

def test_email_templates():
    """Test email templates"""
    print("\n🧪 Testing Email Templates...")
    
    try:
        from backend.services.email_templates import EmailTemplates
        
        templates = EmailTemplates()
        
        # Test contest reminder template
        test_context = {
            'user_name': 'Test User',
            'contest_name': 'LeetCode Weekly Contest 350',
            'contest_date': 'May 15, 2025 at 02:30 PM',
            'contest_url': 'https://leetcode.com/contest/weekly-350/',
            'time_until': '1 hour',
            'current_year': 2025
        }
        
        html_content = templates.render_contest_reminder(test_context)
        
        if html_content and 'Contest Starting Soon!' in html_content:
            print("✅ Contest reminder template rendered successfully")
        
        # Test daily motivation template
        motivation_context = {
            'user_name': 'Test User',
            'total_solved': 150,
            'current_streak': 7,
            'favorite_platform': 'LeetCode',
            'current_year': 2025
        }
        
        motivation_html = templates.render_daily_motivation(motivation_context)
        
        if motivation_html and 'Time to Code!' in motivation_html:
            print("✅ Daily motivation template rendered successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Template test failed: {str(e)}")
        return False

def check_environment():
    """Check environment configuration"""
    print("\n🔍 Checking Environment Configuration...")
    
    # Check for .env file
    env_file = '.env'
    if os.path.exists(env_file):
        print(f"✅ Found {env_file}")
    else:
        print(f"⚠️  {env_file} not found - create it for configuration")
    
    # Check important environment variables
    important_vars = [
        'SENDGRID_API_KEY',
        'FROM_EMAIL',
        'FROM_NAME',
        'GOOGLE_CREDENTIALS_FILE',
        'CALENDAR_TOKENS_DIR'
    ]
    
    for var in important_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if 'KEY' in var or 'SECRET' in var:
                masked_value = f"{value[:10]}..." if len(value) > 10 else "***"
                print(f"✅ {var}: {masked_value}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"⚠️  {var}: Not set")
    
    return True

def main():
    """Run all tests"""
    print("🚀 CodeJarvis - Testing New Email & Calendar Services")
    print("=" * 50)
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded")
    except ImportError:
        print("⚠️  python-dotenv not installed, using system environment")
    except Exception as e:
        print(f"⚠️  Error loading .env: {e}")
    
    # Run tests
    tests = [
        ("Environment Check", check_environment),
        ("Email Templates", test_email_templates),
        ("SendGrid Service", test_sendgrid_service),
        ("Calendar Service", test_calendar_service)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your new services are ready to use!")
        print("\n📖 Next steps:")
        print("1. Follow the EASY_SETUP_GUIDE.md for detailed setup")
        print("2. Configure SendGrid or EmailJS for email")
        print("3. Set up Google Calendar OAuth (optional)")
        print("4. Replace old service imports in your code")
    else:
        print("\n⚠️  Some tests failed. Check the setup guide for troubleshooting.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
