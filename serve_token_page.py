#!/usr/bin/env python3
"""
Simple HTTP server to serve the token capture page on port 3000
Run this to capture your OAuth tokens easily.
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 3001
DIRECTORY = Path(__file__).parent

class TokenPageHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def do_GET(self):
        # Serve the token capture page for any path
        if self.path == '/' or self.path.startswith('/auth/'):
            self.path = '/token_capture.html'
        return super().do_GET()
    
    def log_message(self, format, *args):
        # Custom logging
        print(f"[{self.date_time_string()}] {format % args}")

def main():
    print("🎯 CodeJarvis Token Capture Server")
    print("=" * 40)
    print(f"📡 Starting server on http://localhost:{PORT}")
    print(f"📁 Serving files from: {DIRECTORY}")
    print()
    
    try:
        with socketserver.TCPServer(("", PORT), TokenPageHandler) as httpd:
            print(f"✅ Server running at http://localhost:{PORT}")
            print(f"🌐 Token capture page: http://localhost:{PORT}/token_capture.html")
            print()
            print("📋 Instructions:")
            print("1. Keep this server running")
            print("2. Open http://localhost:3000 in your browser")
            print("3. Click 'Login with Google' to start OAuth flow")
            print("4. Your token will be captured automatically!")
            print()
            print("⌨️  Press Ctrl+C to stop the server")
            print()
            
            # Auto-open browser
            try:
                webbrowser.open(f"http://localhost:{PORT}")
                print("🔄 Opened browser automatically")
            except:
                print("⚠️  Could not open browser automatically")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use!")
            print("💡 Try stopping any other servers running on port 3000")
            print("   Or change the PORT variable in this script")
        else:
            print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
