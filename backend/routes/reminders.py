from flask import Blueprint, jsonify, request
from datetime import datetime
from ..services.reminder_manager import reminder_manager
from ..services.simple_email import simple_email_service


reminders_bp = Blueprint("reminders", __name__)

@reminders_bp.route("/api/reminders", methods=["POST"])
def create_reminder():
    """Create a new contest reminder"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract required fields
        user_email = data.get('user_email')
        contest_name = data.get('contest_name')
        contest_url = data.get('contest_url')
        contest_time_str = data.get('contest_time')
        platform = data.get('platform', 'Unknown')
        
        # Validate required fields
        if not all([user_email, contest_name, contest_url, contest_time_str]):
            return jsonify({
                "error": "Missing required fields: user_email, contest_name, contest_url, contest_time"
            }), 400
        
        # Parse contest time
        try:
            contest_time = datetime.fromisoformat(contest_time_str.replace('Z', ''))
        except ValueError:
            return jsonify({"error": "Invalid contest_time format. Use ISO format."}), 400
        
        # Check if reminder already exists
        if reminder_manager.is_reminder_active(user_email, contest_name, contest_url):
            return jsonify({
                "error": "Reminder already exists for this contest",
                "reminder_id": reminder_manager.find_reminder_id(user_email, contest_name, contest_url)
            }), 409
        
        # Create reminder
        reminder_id = reminder_manager.add_reminder(
            user_email=user_email,
            contest_name=contest_name,
            contest_url=contest_url,
            contest_time=contest_time,
            platform=platform
        )
        
        return jsonify({
            "success": True,
            "message": "Reminder created successfully!",
            "reminder_id": reminder_id,
            "contest_name": contest_name,
            "contest_time": contest_time.isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({"error": f"Failed to create reminder: {str(e)}"}), 500

@reminders_bp.route("/api/reminders", methods=["DELETE"])
def remove_reminder():
    """Remove a contest reminder"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        user_email = data.get('user_email')
        reminder_id = data.get('reminder_id')
        contest_name = data.get('contest_name')
        contest_url = data.get('contest_url')
        
        if not user_email:
            return jsonify({"error": "user_email is required"}), 400
        
        # Try to find and remove by reminder_id first
        if reminder_id:
            success = reminder_manager.remove_reminder(reminder_id, user_email)
        # Otherwise try to find by contest details
        elif contest_name and contest_url:
            reminder_id = reminder_manager.find_reminder_id(user_email, contest_name, contest_url)
            if reminder_id:
                success = reminder_manager.remove_reminder(reminder_id, user_email)
            else:
                success = False
        else:
            return jsonify({"error": "Either reminder_id or (contest_name + contest_url) required"}), 400
        
        if success:
            return jsonify({
                "success": True,
                "message": "Reminder removed successfully"
            }), 200
        else:
            return jsonify({"error": "Reminder not found or already removed"}), 404
            
    except Exception as e:
        return jsonify({"error": f"Failed to remove reminder: {str(e)}"}), 500

@reminders_bp.route("/api/reminders/<user_email>", methods=["GET"])
def get_user_reminders(user_email):
    """Get all active reminders for a user"""
    try:
        reminders = reminder_manager.get_user_reminders(user_email)
        
        return jsonify({
            "success": True,
            "reminders": reminders,
            "count": len(reminders)
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get reminders: {str(e)}"}), 500

@reminders_bp.route("/api/reminders/calendar", methods=["GET"])
def get_calendar_reminders():
    """Get all active reminders for calendar display"""
    try:
        reminders = reminder_manager.get_all_active_reminders()
        
        # Format reminders for calendar display
        calendar_events = []
        for reminder in reminders:
            try:
                contest_time = datetime.fromisoformat(reminder['contest_time'])
                calendar_events.append({
                    'id': reminder['id'],
                    'title': reminder['contest_name'],
                    'start': reminder['contest_time'],
                    'url': reminder['contest_url'],
                    'platform': reminder.get('platform', 'Unknown'),
                    'user_email': reminder['user_email']
                })
            except:
                continue
        
        return jsonify({
            "success": True,
            "events": calendar_events,
            "count": len(calendar_events)
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get calendar reminders: {str(e)}"}), 500

@reminders_bp.route("/api/reminders/check", methods=["POST"])
def check_reminder_status():
    """Check if a reminder exists for a specific contest"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        user_email = data.get('user_email')
        contest_name = data.get('contest_name')
        contest_url = data.get('contest_url')
        
        if not all([user_email, contest_name, contest_url]):
            return jsonify({"error": "user_email, contest_name, and contest_url are required"}), 400
        
        is_active = reminder_manager.is_reminder_active(user_email, contest_name, contest_url)
        reminder_id = reminder_manager.find_reminder_id(user_email, contest_name, contest_url) if is_active else None
        
        return jsonify({
            "has_reminder": is_active,
            "reminder_id": reminder_id
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to check reminder status: {str(e)}"}), 500

@reminders_bp.route("/api/reminders/debug-email", methods=["POST"])
def debug_email_config():
    """Debug email configuration"""
    try:
        import os
        from ..services.simple_email import simple_email_service
        
        # Check environment variables
        email_password = os.getenv("EMAIL_PASSWORD")
        smtp_password = os.getenv("SMTP_PASSWORD")
        sender_email = simple_email_service.sender_email
        
        debug_info = {
            "sender_email": sender_email,
            "has_email_password": bool(email_password),
            "has_smtp_password": bool(smtp_password),
            "email_password_length": len(email_password) if email_password else 0,
            "smtp_password_length": len(smtp_password) if smtp_password else 0,
            "using_password": simple_email_service.sender_password is not None,
            "password_source": "EMAIL_PASSWORD" if email_password else "SMTP_PASSWORD" if smtp_password else "None"
        }
        
        # Test connection
        connection_test = simple_email_service.test_connection()
        
        return jsonify({
            "success": True,
            "debug_info": debug_info,
            "connection_test": connection_test
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to debug email config: {str(e)}"}), 500

@reminders_bp.route("/api/reminders/test-email", methods=["POST"])
def test_email_service():
    """Test the email service"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        test_email = data.get('email')
        if not test_email:
            return jsonify({"error": "email is required"}), 400
        
        # Test connection first
        if not simple_email_service.test_connection():
            return jsonify({
                "success": False,
                "error": "Email service connection failed. Check EMAIL_PASSWORD environment variable."
            }), 500
        
        # Send test email
        test_time = datetime.utcnow()
        success = simple_email_service.send_reminder_email(
            recipient_email=test_email,
            contest_name="Test Contest - Email Service Check",
            contest_url="https://codeforces.com",
            contest_time=test_time,
            reminder_type="confirmation"
        )
        
        if success:
            return jsonify({
                "success": True,
                "message": "Test email sent successfully!"
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Failed to send test email"
            }), 500
            
    except Exception as e:
        return jsonify({"error": f"Failed to test email service: {str(e)}"}), 500