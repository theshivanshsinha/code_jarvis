#!/usr/bin/env python3
"""
Complete flow test - simulates frontend creating a reminder
"""

import sys
import os
import requests
import json
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_complete_reminder_flow():
    """Test the complete reminder creation flow like the frontend does"""
    
    print("🧪 Testing Complete Reminder Flow")
    print("=" * 50)
    
    # Test data - similar to what frontend sends
    base_url = "http://localhost:5000"
    test_data = {
        "user_email": "kumarshivanshsinha@gmail.com",
        "contest_name": "codeforces: Educational Round #123 (Div. 2)",
        "contest_url": "https://codeforces.com/contest/1789",
        "contest_time": (datetime.utcnow() + timedelta(hours=2)).isoformat(),
        "platform": "codeforces",
        "description": "Educational Round focusing on algorithms and data structures. Suitable for Div. 2 participants."
    }
    
    print(f"📧 User Email: {test_data['user_email']}")
    print(f"🏆 Contest: {test_data['contest_name']}")
    print(f"🔗 URL: {test_data['contest_url']}")
    print(f"⏰ Time: {test_data['contest_time']}")
    print()
    
    try:
        # 1. Test health endpoint first
        print("1️⃣ Testing API health...")
        try:
            health_response = requests.get(f"{base_url}/api/health", timeout=5)
            if health_response.status_code == 200:
                print("   ✅ API is running")
            else:
                print(f"   ⚠️ API health check returned {health_response.status_code}")
        except requests.exceptions.ConnectionError:
            print("   ❌ API is not running - please start the backend server")
            print("   💡 Run: python -m backend.app")
            return False
        except Exception as e:
            print(f"   ❌ Health check failed: {e}")
            return False
        
        # 2. Test email configuration
        print("\\n2️⃣ Testing email configuration...")
        try:
            debug_response = requests.post(f"{base_url}/api/reminders/debug-email")
            debug_data = debug_response.json()
            print(f"   Debug info: {json.dumps(debug_data, indent=2)}")
        except Exception as e:
            print(f"   ⚠️ Could not get debug info: {e}")
        
        # 3. Create reminder (main test)
        print("\\n3️⃣ Creating reminder...")
        create_response = requests.post(
            f"{base_url}/api/reminders",
            headers={"Content-Type": "application/json"},
            json=test_data,
            timeout=10
        )
        
        print(f"   Response status: {create_response.status_code}")
        response_data = create_response.json()
        print(f"   Response data: {json.dumps(response_data, indent=2)}")
        
        if create_response.status_code == 201 and response_data.get("success"):
            print("   ✅ Reminder created successfully!")
            reminder_id = response_data.get("reminder_id")
            
            # 4. Verify reminder exists
            print("\\n4️⃣ Verifying reminder exists...")
            check_response = requests.post(
                f"{base_url}/api/reminders/check",
                headers={"Content-Type": "application/json"},
                json={
                    "user_email": test_data["user_email"],
                    "contest_name": test_data["contest_name"],
                    "contest_url": test_data["contest_url"]
                }
            )
            
            if check_response.status_code == 200:
                check_data = check_response.json()
                print(f"   Reminder exists: {check_data.get('has_reminder', False)}")
                print(f"   Reminder ID: {check_data.get('reminder_id')}")
            
            # 5. Clean up - remove the test reminder
            print("\\n5️⃣ Cleaning up test reminder...")
            cleanup_response = requests.delete(
                f"{base_url}/api/reminders",
                headers={"Content-Type": "application/json"},
                json={
                    "user_email": test_data["user_email"],
                    "reminder_id": reminder_id
                }
            )
            
            if cleanup_response.status_code == 200:
                print("   🧹 Test reminder removed successfully")
            else:
                print(f"   ⚠️ Could not remove test reminder: {cleanup_response.status_code}")
            
            return True
            
        else:
            print(f"   ❌ Failed to create reminder: {response_data.get('error', 'Unknown error')}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API - is the backend running?")
        return False
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 Starting complete reminder flow test...")
    print("📝 This simulates what happens when you click 'Remind me' in the frontend")
    print()
    
    success = test_complete_reminder_flow()
    
    print("\\n" + "=" * 50)
    print("📋 Test Summary:")
    if success:
        print("✅ Reminder creation flow works!")
        print("📬 Check your email for the confirmation message")
        print("💡 If no email received, check:")
        print("   - Spam/junk folder")
        print("   - Gmail app password is correct")
        print("   - Email service debug info above")
    else:
        print("❌ Reminder creation flow has issues")
        print("💡 Check the error messages above")
    
    print("\\n🔧 To debug further:")
    print("   - Check backend console logs")
    print("   - Verify .env file has EMAIL_PASSWORD")
    print("   - Test with: python test_email.py")

if __name__ == "__main__":
    main()