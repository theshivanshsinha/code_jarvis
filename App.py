#!/usr/bin/env python3
"""
Production entry point for CodeJarvis backend.
This file is specifically for deployment platforms that expect 'app.py' in the root.
"""
import sys
import os
from pathlib import Path

# Set up the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Ensure PORT is properly set
port = int(os.environ.get("PORT", 5000))
print(f"🔗 Port configured: {port}")
print(f"🌐 Environment: {os.environ.get('FLASK_ENV', 'production')}")

try:
    # Import and create the Flask application
    from backend import create_app
    
    # Create the app instance
    app = create_app()
    
    # Configure for production
    app.config['DEBUG'] = False
    app.config['ENV'] = 'production'
    
    print("✅ CodeJarvis Backend initialized for production")
    print(f"🚀 Ready to serve on port {port}")
    
except Exception as e:
    print(f"❌ Failed to initialize backend: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# For gunicorn: this exposes the 'app' variable that gunicorn expects
# Command: gunicorn app:app
if __name__ == "__main__":
    # For direct execution (fallback)
    print(f"🔧 Starting Flask development server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)