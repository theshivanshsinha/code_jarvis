from http.server import HTTPServer, BaseHTTPRequestHandler
import time

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>Test HTTP Server is Running!</h1>')

if __name__ == "__main__":
    PORT = 8000
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'Starting HTTP server on port {PORT}...')
    print('Press Ctrl+C to stop')
    httpd.serve_forever()
