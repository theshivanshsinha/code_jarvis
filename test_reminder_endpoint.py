import requests
import json
from datetime import datetime, timezone, timedelta

# Test data
test_data = {
    "user_email": "test@example.com",
    "contest_name": "Test Contest",
    "contest_url": "https://example.com/contest/123",
    "contest_time": (datetime.utcnow() + timedelta(days=1)).isoformat() + "Z",
    "timezone": "UTC"
}

def test_create_reminder():
    print("Testing reminder creation...")
    print(f"Sending data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            "http://localhost:5000/api/reminders",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 201:
            print("✅ Test passed: Reminder created successfully")
            return response.json().get('id')
        else:
            print("❌ Test failed: Failed to create reminder")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_list_reminders():
    print("\nTesting listing reminders...")
    try:
        response = requests.get(
            "http://localhost:5000/api/reminders",
            params={"user_email": test_data["user_email"]}
        )
        
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print("✅ Test passed: Successfully retrieved reminders")
            return response.json()
        else:
            print("❌ Test failed: Failed to retrieve reminders")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_remove_reminder(reminder_id):
    if not reminder_id:
        print("No reminder ID provided for removal test")
        return
        
    print(f"\nTesting removal of reminder {reminder_id}...")
    try:
        response = requests.delete(
            f"http://localhost:5000/api/reminders/{reminder_id}",
            params={"user_email": test_data["user_email"]}
        )
        
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2) if response.content else "No content")
        
        if response.status_code == 200:
            print("✅ Test passed: Reminder removed successfully")
        else:
            print("❌ Test failed: Failed to remove reminder")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("=== Testing Reminder API Endpoints ===\n")
    
    # Test creating a reminder
    reminder_id = test_create_reminder()
    
    # Test listing reminders
    if reminder_id:
        test_list_reminders()
        
        # Uncomment to test removal
        # test_remove_reminder(reminder_id)
