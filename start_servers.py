#!/usr/bin/env python3
"""
Script to start both backend and frontend servers for CodeJarvis
"""

import subprocess
import sys
import os
import time
import signal

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting Backend Server...")
    backend_process = subprocess.Popen(
        [sys.executable, "run.py"],
        cwd=os.getcwd(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return backend_process

def start_frontend():
    """Start the React frontend server"""
    print("🌐 Starting Frontend Server...")
    frontend_dir = os.path.join(os.getcwd(), "frontend", "codej")
    
    if not os.path.exists(frontend_dir):
        print("❌ Frontend directory not found!")
        return None
    
    try:
        # Try to start with npm
        frontend_process = subprocess.Popen(
            ["npm", "start"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        return frontend_process
    except FileNotFoundError:
        print("❌ npm not found! Please install Node.js and npm")
        return None

def check_server_health():
    """Check if the backend server is responding"""
    import requests
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Health Check: {data.get('message', 'OK')}")
            return True
    except:
        pass
    return False

def main():
    """Main function to start servers"""
    print("🎯 CodeJarvis Server Startup")
    print("=" * 40)
    
    backend_process = None
    frontend_process = None
    
    try:
        # Start backend
        backend_process = start_backend()
        
        # Wait a moment for backend to start
        print("⏳ Waiting for backend to start...")
        time.sleep(3)
        
        # Check backend health
        if check_server_health():
            print("✅ Backend server is running on http://localhost:5000")
        else:
            print("⚠️ Backend health check failed, but continuing...")
        
        # Start frontend
        frontend_process = start_frontend()
        
        if frontend_process:
            print("✅ Frontend server starting on http://localhost:3000")
            print("\n🎉 Both servers are starting!")
            print("\n📋 Available URLs:")
            print("  🔧 Backend API: http://localhost:5000")
            print("  🌐 Frontend App: http://localhost:3000")
            print("  📊 API Health: http://localhost:5000/api/health")
            print("  🧪 Demo Stats: http://localhost:5000/api/stats/demo")
            print("\n⌨️ Press Ctrl+C to stop both servers")
            
            # Wait for user interrupt
            while True:
                time.sleep(1)
        else:
            print("❌ Failed to start frontend server")
    
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping servers...")
        
        if backend_process:
            backend_process.terminate()
            print("✅ Backend server stopped")
            
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend server stopped")
            
        print("👋 Goodbye!")
        
    except Exception as e:
        print(f"❌ Error starting servers: {e}")
        
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        
        sys.exit(1)

if __name__ == "__main__":
    main()
