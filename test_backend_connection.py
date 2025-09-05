import requests
import sys

def test_connection():
    print("Testing backend connection...")
    
    # Test basic connectivity
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        print(f"✅ Health check status: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to backend: {str(e)}")
        print("Please make sure the backend server is running.")
        print("You can start it with: python -m backend")
        return False

if __name__ == "__main__":
    test_connection()
