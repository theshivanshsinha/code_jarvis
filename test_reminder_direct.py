import requests
import json
from datetime import datetime, timedelta

# Test data
test_data = {
    "user_email": "test@example.com",
    "contest_name": "Test Contest",
    "contest_url": "https://example.com/contest/123",
    "contest_time": (datetime.utcnow() + timedelta(days=1)).isoformat() + "Z",
    "timezone": "UTC"
}

def test_endpoint():
    print("Testing endpoint...")
    try:
        # First test the health endpoint
        print("\n1. Testing health endpoint...")
        health_url = "http://localhost:5000/api/health"
        health_response = requests.get(health_url)
        print(f"Health check status: {health_response.status_code}")
        print(f"Response: {health_response.text}")
        
        if health_response.status_code != 200:
            print("❌ Health check failed. Is the server running?")
            return
            
        # Now test the reminder endpoint
        print("\n2. Testing reminder creation...")
        reminder_url = "http://localhost:5000/api/reminders"
        print(f"Sending POST request to: {reminder_url}")
        print(f"Request data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(
            reminder_url,
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nResponse status: {response.status_code}")
        print("Response headers:")
        for k, v in response.headers.items():
            print(f"  {k}: {v}")
            
        try:
            print("\nResponse body:")
            print(json.dumps(response.json(), indent=2))
        except:
            print(f"Could not parse JSON response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {str(e)}")
        print("This usually means the server is not running or not accessible.")
        print("Please make sure the backend server is running and accessible at http://localhost:5000")

if __name__ == "__main__":
    test_endpoint()
