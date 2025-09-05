#!/usr/bin/env python3
"""
Minimal Flask server for Render - GUARANTEED TO WORK
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PORT = int(os.environ.get("PORT", 5000))

print(f"Starting on port {PORT}")

# Direct import
from backend import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0", 
        port=PORT, 
        debug=False,
        use_reloader=False,
        threaded=True
    )