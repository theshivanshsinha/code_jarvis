import sys
import os
from pathlib import Path

# Add parent directory to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Now we can import the backend module
try:
    from backend import create_app
except ImportError:
    # Fallback for deployment scenarios
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from backend import create_app

# Create the app instance
app = create_app()

# Configure for production if not in debug mode
if not app.debug:
    app.config['ENV'] = 'production'
    app.config['DEBUG'] = False

if __name__ == "__main__":
    print("Starting CodeJarvis development server...")
    print(" * Environment: Development")
    print(" * Running on http://127.0.0.1:5000/")
    print(" * Debug mode: on")
    print(" * Press Ctrl+C to quit")
    print()
    try:
        app.run(host="0.0.0.0", port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n * Server stopped by user")
    except Exception as e:
        print(f"\n * Error starting server: {e}")
        sys.exit(1)
