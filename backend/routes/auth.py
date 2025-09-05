from flask import Blueprint, jsonify, request, redirect, session, current_app
from flask import Blueprint, jsonify, request, redirect, session, current_app
from authlib.integrations.flask_client import OAuth
from ..config import settings
from ..db import get_db
import jwt
import secrets
import logging
from datetime import datetime, timedelta, timezone


auth_bp = Blueprint("auth", __name__)
oauth = OAuth()

# Initialize Google OAuth configuration
def init_google_oauth():
    """Initialize Google OAuth client with proper error handling"""
    try:
        return oauth.register(
            name="google",
            client_id=settings.google_client_id,
            client_secret=settings.google_client_secret,
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email profile"},
        )
    except Exception as e:
        current_app.logger.error(f"Failed to initialize Google OAuth: {str(e)}")
        return None

# Initialize google client (will be set when app context is available)
google = None


@auth_bp.get("/google/url")
def google_oauth_url():
    """Generate Google OAuth authorization URL with proper state handling"""
    global google
    try:
        # Initialize Google OAuth if not already done
        if google is None:
            google = init_google_oauth()
            if google is None:
                return jsonify({"error": "Google OAuth not configured properly"}), 500
        
        # Validate required settings
        if not settings.google_client_id or not settings.google_client_secret:
            return jsonify({"error": "Google OAuth credentials not configured"}), 500
        
        # Generate a secure random state
        state = secrets.token_urlsafe(32)
        session['oauth_state'] = state
        
        # Build the authorization URL with state parameter
        redirect_uri = settings.google_redirect_uri
        return google.authorize_redirect(redirect_uri, state=state)
    except Exception as e:
        current_app.logger.error(f"Failed to generate OAuth URL: {str(e)}")
        return jsonify({"error": f"Failed to generate OAuth URL: {str(e)}"}), 500


@auth_bp.get("/me")
def me():
    """Get current authenticated user information from JWT token"""
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"user": None})
        
        token = auth_header.replace("Bearer ", "")
        if not token:
            return jsonify({"user": None})
        
        # Decode and validate JWT token
        payload = jwt.decode(token, settings.flask_secret, algorithms=["HS256"])
        
        # Verify required fields
        if not payload.get("sub") or not payload.get("email"):
            current_app.logger.warning("Invalid token payload: missing required fields")
            return jsonify({"user": None})
        
        return jsonify({
            "user": {
                "sub": payload.get("sub"),
                "email": payload.get("email"),
                "name": payload.get("name", ""),
                "picture": payload.get("picture", "")
            }
        })
    except jwt.ExpiredSignatureError:
        current_app.logger.info("Expired JWT token")
        return jsonify({"user": None})
    except jwt.InvalidTokenError as e:
        current_app.logger.warning(f"Invalid JWT token: {str(e)}")
        return jsonify({"user": None})
    except Exception as e:
        current_app.logger.error(f"Error validating token: {str(e)}")
        return jsonify({"user": None})

@auth_bp.get("/google/callback")
def google_callback():
    """Handle Google OAuth callback with proper state validation and user storage"""
    global google
    try:
        # Initialize Google OAuth if not already done
        if google is None:
            google = init_google_oauth()
            if google is None:
                current_app.logger.error("Google OAuth not configured properly")
                return redirect(f"{settings.client_origin}/auth/error?error=oauth_not_configured")
        
        # Check for OAuth error in callback
        error = request.args.get('error')
        if error:
            current_app.logger.warning(f"OAuth error: {error}")
            error_description = request.args.get('error_description', '')
            return redirect(f"{settings.client_origin}/auth/error?error={error}&description={error_description}")
        
        # Validate state parameter to prevent CSRF attacks
        received_state = request.args.get('state')
        stored_state = session.get('oauth_state')
        
        if not received_state or not stored_state or received_state != stored_state:
            current_app.logger.warning(f"State mismatch: received={received_state}, stored={stored_state}")
            return redirect(f"{settings.client_origin}/auth/error?error=state_mismatch")
        
        # Clear the state from session
        session.pop('oauth_state', None)
        
        # Exchange authorization code for token
        token = google.authorize_access_token()
        if not token:
            current_app.logger.error("Failed to exchange authorization code for token")
            return redirect(f"{settings.client_origin}/auth/error?error=token_exchange_failed")
        
        # Get user info from the token
        userinfo = token.get("userinfo") or {}
        if not userinfo.get('sub') or not userinfo.get('email'):
            current_app.logger.error(f"Invalid user info: {userinfo}")
            return redirect(f"{settings.client_origin}/auth/error?error=invalid_user_info")
        
        # Store/update user in database
        try:
            db = get_db()
            user_data = {
                'sub': userinfo.get('sub'),
                'email': userinfo.get('email'),
                'name': userinfo.get('name', ''),
                'picture': userinfo.get('picture', ''),
                'last_login': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            # Update or insert user
            db.users.update_one(
                {'sub': user_data['sub']},
                {'$set': user_data, '$setOnInsert': {'created_at': datetime.utcnow()}},
                upsert=True
            )
            current_app.logger.info(f"User {user_data['email']} logged in successfully")
        except Exception as e:
            current_app.logger.warning(f"Failed to store user in database: {str(e)}")
            # Continue anyway - we can still create the JWT
        
        # Create session JWT token
        exp = datetime.now(timezone.utc) + timedelta(days=7)
        session_jwt = jwt.encode({
            "sub": userinfo.get("sub"), 
            "email": userinfo.get("email"), 
            "name": userinfo.get("name", ''),
            "picture": userinfo.get("picture", ''),
            "exp": exp
        }, settings.flask_secret, algorithm="HS256")
        
        # Redirect back to client with token as URL fragment (SPA-friendly)
        redirect_url = f"{settings.client_origin}/auth/callback#token={session_jwt}"
        return redirect(redirect_url)
        
    except Exception as e:
        current_app.logger.error(f"OAuth callback error: {str(e)}")
        return redirect(f"{settings.client_origin}/auth/error?error=oauth_callback_failed&message={str(e)}")


@auth_bp.get("/test-login")
def test_login():
    """Simple test route to check authentication flow status"""
    return jsonify({
        "message": "Test login endpoint",
        "session_has_oauth_state": 'oauth_state' in session,
        "client_origin": settings.client_origin,
        "google_redirect_uri": settings.google_redirect_uri,
        "google_configured": bool(settings.google_client_id and settings.google_client_secret),
        "instructions": {
            "step1": "Visit /api/auth/google/url to start OAuth flow",
            "step2": "Complete Google login",
            "step3": "You'll be redirected back with a JWT token",
            "step4": "Use the token in Authorization: Bearer <token> headers"
        }
    })

@auth_bp.post("/logout")
def logout():
    """Logout endpoint that clears session data"""
    try:
        # Clear OAuth state from session
        session.pop('oauth_state', None)
        
        # Note: JWT tokens are stateless, so we can't invalidate them server-side
        # The client should discard the token
        return jsonify({"message": "Logged out successfully"})
    except Exception as e:
        current_app.logger.error(f"Error during logout: {str(e)}")
        return jsonify({"error": "Logout failed"}), 500

@auth_bp.get("/config")
def auth_config():
    """Get authentication configuration (for frontend)"""
    return jsonify({
        "google_configured": bool(settings.google_client_id and settings.google_client_secret),
        "client_origin": settings.client_origin
    })


