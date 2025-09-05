#!/usr/bin/env python3
"""
CodeJarvis Backend Development Server
Run this script to start the development server.
"""

import sys
import os

# Add the current directory to Python path so we can import backend
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend import create_app

def main():
    """Main entry point for the development server."""
    print("Starting CodeJarvis development server...")
    print(" * Environment: Development")
    print(" * Running on http://127.0.0.1:5000/")
    print(" * Debug mode: on")
    print(" * Press Ctrl+C to quit")
    print()
    
    app = create_app()
    
    try:
        app.run(host="0.0.0.0", port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n * Server stopped by user")
    except Exception as e:
        print(f"\n * Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
