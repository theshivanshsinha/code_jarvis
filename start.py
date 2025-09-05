#!/usr/bin/env python3
"""
Production startup script for CodeJarvis backend.
This is the entry point for deployment on platforms like Render.
"""
import os
import sys
from pathlib import Path

# Ensure we're working from the correct directory
project_root = Path(__file__).parent
os.chdir(project_root)

# Add the project root to Python path
sys.path.insert(0, str(project_root))

try:
    # Import the Flask app
    from backend import create_app
    
    # Create the app instance
    app = create_app()
    
    # Configure for production
    app.config['DEBUG'] = False
    app.config['ENV'] = 'production'
    
    # Log startup information
    print("🚀 CodeJarvis Backend Starting...")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🐍 Python version: {sys.version}")
    print(f"🌐 Environment: {app.config.get('ENV', 'unknown')}")
    print("✅ Backend initialized successfully!")
    
except Exception as e:
    print(f"❌ Failed to initialize backend: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Export the app for gunicorn
application = app

if __name__ == "__main__":
    # For production deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)