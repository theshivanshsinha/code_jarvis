import socket
import sys

def check_port(host, port):
    """Check if a port is open on the given host."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

def find_backend_ports():
    """Check common ports where the backend might be running."""
    host = '127.0.0.1'
    common_ports = [5000, 8000, 8080, 3000, 5001, 8001, 8081, 3001, 3002, 5002]
    
    print(f"Checking for running servers on {host}...\n")
    
    found = False
    for port in common_ports:
        if check_port(host, port):
            print(f"✅ Found server running on port {port}")
            found = True
    
    if not found:
        print("❌ No running servers found on common ports.")
        print("\nPlease make sure the backend server is running by executing:")
        print("  python -m backend")
    else:
        print("\nIf you see the backend port above, try accessing it directly in your browser or API client.")
        print("For example: http://localhost:5000/")

if __name__ == "__main__":
    find_backend_ports()
