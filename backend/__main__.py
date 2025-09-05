"""
Main entry point for the backend application.
Run this with: python -m backend
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    try:
        from . import create_app
        
        app = create_app()
        
        print("\n" + "="*50)
        print("Starting CodeJarvis Backend Server")
        print("="*50)
        print(f" * Environment: {'Development' if app.debug else 'Production'}")
        print(f" * Debug mode: {'on' if app.debug else 'off'}")
        print(f" * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)")
        print("="*50 + "\n")
        
        app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
        
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
