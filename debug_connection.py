#!/usr/bin/env python3
"""
Debug script to test API connectivity and CORS issues
"""

import requests
import json
import time

def test_backend_connection():
    """Test if backend is running and accessible"""
    print("🔍 Testing Backend Connection")
    print("=" * 40)
    
    # Test basic connection
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        print(f"✅ Health Check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Backend server is not running on port 5000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test CORS headers
    try:
        response = requests.options("http://localhost:5000/api/stats", 
                                  headers={
                                      "Origin": "http://localhost:3000",
                                      "Access-Control-Request-Method": "GET"
                                  })
        print(f"✅ CORS Preflight: {response.status_code}")
        print(f"   CORS Headers: {dict(response.headers)}")
    except Exception as e:
        print(f"⚠️ CORS Test Error: {e}")
    
    return True

def test_stats_endpoints():
    """Test stats endpoints"""
    print("\n📊 Testing Stats Endpoints")
    print("=" * 40)
    
    endpoints = [
        ("/api/stats", "Basic stats"),
        ("/api/stats/demo", "Demo stats with real data"),
        ("/api/stats/daily", "Daily activity"),
        ("/api/stats/problems?limit=5", "Problem history")
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"http://localhost:5000{endpoint}", timeout=10)
            print(f"✅ {description}: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if endpoint == "/api/stats/demo":
                    # Show demo stats summary
                    overview = data.get('overview', {})
                    total_problems = overview.get('problemsSolved', {}).get('total', 0)
                    max_rating = overview.get('maxRating', {}).get('value', 0)
                    print(f"   📈 Total Problems: {total_problems}")
                    print(f"   🏆 Max Rating: {max_rating}")
                elif endpoint == "/api/stats/daily":
                    total_activity = data.get('totalActivity', 0)
                    active_days = data.get('activeDays', 0)
                    print(f"   📅 Total Activity: {total_activity}")
                    print(f"   📊 Active Days: {active_days}")
                elif "problems" in endpoint:
                    total = data.get('total', 0)
                    showing = data.get('showing', 0)
                    print(f"   🧩 Problems: {showing}/{total}")
            else:
                print(f"   ❌ Error: {response.text}")
                
        except Exception as e:
            print(f"❌ {description}: Error - {e}")

def simulate_frontend_request():
    """Simulate the exact request the frontend would make"""
    print("\n🌐 Simulating Frontend Request")
    print("=" * 40)
    
    try:
        # Simulate the exact headers a React app would send
        headers = {
            "Origin": "http://localhost:3000",
            "Referer": "http://localhost:3000/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        response = requests.get("http://localhost:5000/api/stats", 
                              headers=headers, 
                              timeout=10)
        
        print(f"✅ Frontend Simulation: {response.status_code}")
        print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not set')}")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'Not set')}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   📊 Data keys: {list(data.keys())}")
        else:
            print(f"   ❌ Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Frontend simulation failed: {e}")

def check_ports():
    """Check what's running on common ports"""
    print("\n🔍 Checking Ports")
    print("=" * 40)
    
    ports_to_check = [5000, 3000, 8000, 8080]
    
    for port in ports_to_check:
        try:
            response = requests.get(f"http://localhost:{port}", timeout=2)
            print(f"✅ Port {port}: {response.status_code} - Something is running")
        except requests.exceptions.ConnectionError:
            print(f"❌ Port {port}: Nothing running")
        except Exception as e:
            print(f"⚠️ Port {port}: {e}")

def main():
    """Run all tests"""
    print("🐛 CodeJarvis Connection Debugger")
    print("=" * 50)
    print("This script will help diagnose connection issues between frontend and backend")
    print()
    
    # Check ports first
    check_ports()
    
    # Test backend
    if test_backend_connection():
        test_stats_endpoints()
        simulate_frontend_request()
        
        print("\n🎯 Troubleshooting Tips:")
        print("=" * 40)
        print("1. Make sure both servers are running:")
        print("   - Backend: python run.py")
        print("   - Frontend: cd frontend/codej && npm start")
        print()
        print("2. Check browser console for detailed errors")
        print()
        print("3. Try accessing backend directly:")
        print("   - http://localhost:5000/api/health")
        print("   - http://localhost:5000/api/stats/demo")
        print()
        print("4. If CORS errors persist, clear browser cache")
    else:
        print("\n❌ Backend server is not running!")
        print("Please start the backend server first:")
        print("   python run.py")

if __name__ == "__main__":
    main()
