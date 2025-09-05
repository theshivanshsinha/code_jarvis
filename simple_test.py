import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend import create_app

def test_app():
    print("Creating Flask app...")
    app = create_app()
    
    print("\nRegistered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule} {list(rule.methods)}")
    
    print("\nTesting app context...")
    with app.test_client() as client:
        print("\nTesting root route (/):")
        response = client.get('/')
        print(f"Status: {response.status_code}")
        print(f"Response: {response.data.decode()[:200]}")
        
        print("\nTesting health check (/api/health):")
        response = client.get('/api/health')
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json}")

if __name__ == "__main__":
    test_app()
