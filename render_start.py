#!/usr/bin/env python3
"""
Render-optimized startup script for CodeJarvis Backend
"""
import os
import sys
import time
from pathlib import Path

# Ensure proper Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Get and validate PORT
PORT = int(os.environ.get("PORT", 5000))
print(f"🚀 Starting CodeJarvis on PORT: {PORT}")
print(f"🌍 Host: 0.0.0.0")
print(f"📁 Working Dir: {os.getcwd()}")
print(f"🐍 Python Path: {sys.path[:3]}")

try:
    # Import Flask app
    print("📦 Importing backend...")
    from backend import create_app
    
    print("⚙️ Creating Flask app...")
    app = create_app()
    
    # Configure for production
    app.config.update({
        'DEBUG': False,
        'ENV': 'production',
        'TESTING': False
    })
    
    print("✅ Flask app created successfully")
    print(f"🔧 App config - DEBUG: {app.config.get('DEBUG')}")
    
    # Test that the app responds
    with app.test_client() as client:
        response = client.get('/api/health')
        print(f"🏥 Health check: {response.status_code}")
    
    print(f"🎯 Starting server on 0.0.0.0:{PORT}")
    
    # Start the application with proper settings
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False,
        threaded=True,
        use_reloader=False
    )
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("🔍 Available modules:")
    for path in sys.path[:3]:
        try:
            items = os.listdir(path) if os.path.exists(path) else []
            print(f"  {path}: {items[:5]}")
        except:
            pass
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Startup Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)