#!/usr/bin/env python3
"""
Simple startup script for Render deployment.
This ensures proper port binding and startup logging.
"""
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Get port from environment
PORT = int(os.environ.get("PORT", 5000))

print(f"🔧 Starting CodeJarvis Backend on port {PORT}")
print(f"🌍 Host: 0.0.0.0")
print(f"🔗 Environment: {os.environ.get('FLASK_ENV', 'production')}")

try:
    from app import app
    print("✅ App imported successfully")
    
    # Start the application
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False,
        threaded=True
    )
    
except Exception as e:
    print(f"❌ Startup failed: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)