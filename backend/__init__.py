import os
import sys
import logging
import threading
import time
from datetime import datetime
from flask import Flask, jsonify, request, g
from flask_cors import CORS
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def create_app() -> Flask:
    """Create and configure an instance of the Flask application."""
    load_dotenv()
    app = Flask(__name__)
    
    # Set log level based on environment
    if app.debug:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)
    
    # Needed for OAuth state/session
    from .config import settings
    app.secret_key = settings.flask_secret
    
    # Request logging middleware
    @app.before_request
    def log_request():
        g.start_time = time.time()
        g.request_id = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{os.urandom(4).hex()}"
        
        # Skip logging for health checks and static files
        if request.path == '/api/health' or request.path.startswith('/static/'):
            return
            
        logger.info(f"Request: {request.method} {request.path} (ID: {g.request_id})")
        if request.method in ['POST', 'PUT', 'PATCH'] and request.is_json:
            logger.debug(f"Request body: {request.get_json()}")
    
    @app.after_request
    def log_response(response):
        # Skip logging for health checks and static files
        if request.path == '/api/health' or request.path.startswith('/static/'):
            return response
            
        duration = (time.time() - g.start_time) * 1000  # Convert to milliseconds
        logger.info(
            f"Response: {request.method} {request.path} "
            f"=> {response.status_code} ({duration:.2f}ms) (ID: {g.request_id})"
        )
        return response
        
    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

    # CORS for frontend dev - allow all origins for development
    CORS(app, 
         resources={
             r"/api/*": {
                 "origins": ["http://localhost:3000", "http://127.0.0.1:3000", "*"],
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                 "allow_headers": ["Content-Type", "Authorization", "X-User-ID"]
             }
         },
         supports_credentials=True)

    @app.get("/api/health")
    def health_check():
        return jsonify({"status": "ok", "message": "CodeJarvis API is running!"})
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500
    
    @app.before_request
    def log_request_info():
        print(f"Request: {request.method} {request.url}")
    
    # Add a simple test route
    @app.get("/")
    def index():
        return "<h1>CodeJarvis Backend is running!</h1>"

    # Import and register blueprints
    try:
        from .routes.auth import auth_bp, oauth
        from .routes.contests import contests_bp
        from .routes.reminders import reminders_bp
        from .routes.accounts import accounts_bp
        from .routes.stats import stats_bp
        from .routes.qotd import qotd_bp
        
        app.register_blueprint(auth_bp, url_prefix="/api/auth")
        app.register_blueprint(contests_bp, url_prefix="/api/contests")
        app.register_blueprint(reminders_bp)  # Reminder routes are already prefixed with /api/reminders
        app.register_blueprint(accounts_bp, url_prefix="/api/accounts")
        app.register_blueprint(stats_bp, url_prefix="/api/stats")
        app.register_blueprint(qotd_bp, url_prefix="/api/qotd")
        
        # Initialize OAuth client with app context
        oauth.init_app(app)
        
        # Initialize Google OAuth client within app context
        with app.app_context():
            from .routes.auth import init_google_oauth
            google_client = init_google_oauth()
            if google_client:
                app.logger.info("Google OAuth initialized successfully")
            else:
                app.logger.warning("Google OAuth initialization failed - check credentials")
                
    except ImportError as e:
        print(f"Warning: Could not import all modules - some features may be disabled: {e}")
    
    # Start background task for reminder cleanup and restart
    def reminder_maintenance_task():
        from .services.reminder_manager import reminder_manager
        import time
        
        print("Starting reminder maintenance task...")
        # Restart pending reminders on server start
        reminder_manager.restart_pending_reminders()
        
        while True:
            try:
                # Clean up old reminders every hour
                reminder_manager.cleanup_old_reminders()
            except Exception as e:
                print(f"Error in reminder maintenance task: {e}")
            time.sleep(3600)  # Run cleanup every hour
    
    # Only start the background task if we're the main process (not a forked process)
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        reminder_thread = threading.Thread(target=reminder_maintenance_task, daemon=True)
        reminder_thread.start()
        print("Started background reminder maintenance task")

    return app

# This makes the create_app function available when importing from the package
__all__ = ['create_app']


