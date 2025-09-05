#!/usr/bin/env python3
"""
Ultra-simple production server for Render deployment
"""
import os
import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Get port
PORT = int(os.environ.get("PORT", 5000))

print(f"🚀 CodeJarvis starting on port {PORT}")
print(f"🔗 Binding to 0.0.0.0:{PORT}")

try:
    # Import app
    from backend import create_app
    app = create_app()
    
    print("✅ App imported successfully")
    
    # Use waitress for production
    from waitress import serve
    print("🍽️ Starting Waitress WSGI server...")
    
    serve(
        app,
        host="0.0.0.0",
        port=PORT,
        threads=4,
        connection_limit=1000,
        cleanup_interval=30,
        channel_timeout=120
    )
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    # Fallback to Flask dev server
    print("⚠️ Falling back to Flask dev server")
    app.run(host="0.0.0.0", port=PORT, debug=False)
    
except Exception as e:
    print(f"❌ Server error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)