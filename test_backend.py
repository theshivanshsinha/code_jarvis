import requests
import sys

def test_backend():
    try:
        # Test basic connectivity
        print("Testing backend connectivity...")
        response = requests.get("http://localhost:5000/", timeout=5)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        # Test API health endpoint
        print("\nTesting API health endpoint...")
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to the backend server.")
        print("Please make sure the backend server is running by executing:")
        print("  python -m backend")
        return False
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    print("=== Backend Connection Test ===\n")
    success = test_backend()
    
    if success:
        print("\n✅ Backend is running and responding correctly!")
    else:
        print("\n❌ Backend test failed.")
        sys.exit(1)
