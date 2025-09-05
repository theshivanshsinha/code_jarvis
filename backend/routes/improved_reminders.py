"""
Example: Using the new improved email and calendar services
This shows how to replace your current complex SMTP setup with much simpler solutions!
"""

from flask import Blueprint, request, jsonify, send_file
from datetime import datetime, timedelta
import os

# Import the NEW improved services
from backend.services.sendgrid_email_service import sendgrid_email_service
from backend.services.improved_calendar_service import google_calendar_service, calendar_fallback_service

# Create blueprint
improved_reminders = Blueprint('improved_reminders', __name__)

@improved_reminders.route('/reminders/create', methods=['POST'])
def create_reminder():
    """Create contest reminder with improved email & calendar integration"""
    try:
        data = request.get_json()
        
        # Extract data
        user_id = data.get('user_id')
        user_email = data.get('user_email')
        user_name = data.get('user_name')
        contest_data = data.get('contest')
        
        # Validate required fields
        if not all([user_id, user_email, contest_data]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        response = {'success': True, 'services_used': []}
        
        # 1. Send confirmation email using SendGrid (much easier than SMTP!)
        email_sent = sendgrid_email_service.send_reminder_confirmation(
            user_email=user_email,
            user_name=user_name,
            contest_name=contest_data['name'],
            contest_date=datetime.fromisoformat(contest_data['start_time'].replace('Z', '')),
            contest_url=contest_data.get('url', '')
        )
        
        if email_sent:
            response['services_used'].append('email_confirmation')
            response['email_status'] = 'sent'
        else:
            response['email_status'] = 'failed'
            response['email_fallback'] = 'Consider using EmailJS for frontend-only emails'
        
        # 2. Try to create Google Calendar event
        calendar_event_id = None
        calendar_status = google_calendar_service.check_user_authorization(user_id)
        
        if calendar_status['authorized']:
            # User has authorized calendar access
            calendar_event_id = google_calendar_service.create_contest_event(
                user_id=user_id,
                contest_data={
                    'name': contest_data['name'],
                    'platform': contest_data.get('platform', 'Contest'),
                    'start_time': contest_data['start_time'],
                    'duration_minutes': contest_data.get('duration_minutes', 180),
                    'url': contest_data.get('url', '')
                }
            )
            
            if calendar_event_id:
                response['services_used'].append('google_calendar')
                response['calendar_event_id'] = calendar_event_id
                response['calendar_status'] = 'event_created'
            else:
                response['calendar_status'] = 'failed'
        else:
            # User hasn't authorized calendar - offer alternatives
            response['calendar_status'] = 'not_authorized'
            response['calendar_oauth_needed'] = True
            
            # Generate OAuth URL for calendar authorization
            auth_url, state = google_calendar_service.get_oauth_url(user_id)
            if auth_url:
                response['calendar_oauth_url'] = auth_url
                response['calendar_oauth_state'] = state
        
        # 3. Generate .ics file as fallback (always available!)
        ics_filename = f"contest_{contest_data['name'].replace(' ', '_')}_{user_id}.ics"
        ics_filepath = os.path.join('temp_ics', ics_filename)
        
        os.makedirs('temp_ics', exist_ok=True)
        
        ics_created = calendar_fallback_service.save_ics_file(
            contest_data={
                'name': contest_data['name'],
                'platform': contest_data.get('platform', 'Contest'),
                'start_time': contest_data['start_time'],
                'duration_minutes': contest_data.get('duration_minutes', 180),
                'url': contest_data.get('url', '')
            },
            filepath=ics_filepath
        )
        
        if ics_created:
            response['services_used'].append('ics_file')
            response['ics_download_url'] = f'/reminders/download-ics/{ics_filename}'
            response['ics_message'] = 'Download .ics file to import into any calendar app'
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': f'Failed to create reminder: {str(e)}'}), 500

@improved_reminders.route('/reminders/download-ics/<filename>')
def download_ics(filename):
    """Download .ics file for manual calendar import"""
    try:
        filepath = os.path.join('temp_ics', filename)
        
        if os.path.exists(filepath):
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename,
                mimetype='text/calendar'
            )
        else:
            return jsonify({'error': 'File not found'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@improved_reminders.route('/reminders/send-reminder', methods=['POST'])
def send_contest_reminder():
    """Send contest reminder email (for scheduled reminders)"""
    try:
        data = request.get_json()
        
        # Send reminder using SendGrid (much more reliable than SMTP!)
        success = sendgrid_email_service.send_contest_reminder(
            user_email=data['user_email'],
            user_name=data['user_name'],
            contest_name=data['contest_name'],
            contest_date=datetime.fromisoformat(data['contest_date']),
            contest_url=data['contest_url'],
            time_until=data['time_until']
        )
        
        if success:
            return jsonify({'success': True, 'message': 'Reminder sent successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to send reminder'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Failed to send reminder: {str(e)}'}), 500

@improved_reminders.route('/calendar/oauth-url/<user_id>')
def get_calendar_oauth_url(user_id):
    """Get Google Calendar OAuth URL for user"""
    try:
        auth_url, state = google_calendar_service.get_oauth_url(user_id)
        
        if auth_url:
            return jsonify({
                'success': True,
                'oauth_url': auth_url,
                'state': state,
                'message': 'Visit the URL to authorize calendar access'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Calendar OAuth not configured. Check credentials.json'
            }), 500
            
    except Exception as e:
        return jsonify({'error': f'OAuth URL generation failed: {str(e)}'}), 500

@improved_reminders.route('/calendar/oauth-callback')
def calendar_oauth_callback():
    """Handle Google Calendar OAuth callback"""
    try:
        code = request.args.get('code')
        state = request.args.get('state')
        
        if not code or not state:
            return jsonify({'error': 'Missing OAuth parameters'}), 400
        
        # Extract user_id from state (you might encode more info in state)
        user_id = state
        
        success = google_calendar_service.handle_oauth_callback(user_id, code, state)
        
        if success:
            return """
            <html>
                <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                    <h2>✅ Calendar Integration Successful!</h2>
                    <p>CodeJarvis can now create events in your Google Calendar.</p>
                    <p>You can close this window and return to the app.</p>
                    <button onclick="window.close()">Close Window</button>
                </body>
            </html>
            """
        else:
            return """
            <html>
                <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                    <h2>❌ Calendar Integration Failed</h2>
                    <p>Please try again or contact support.</p>
                    <button onclick="window.close()">Close Window</button>
                </body>
            </html>
            """, 500
            
    except Exception as e:
        return f"<html><body><h2>Error: {str(e)}</h2></body></html>", 500

@improved_reminders.route('/calendar/status/<user_id>')
def check_calendar_status(user_id):
    """Check if user has authorized calendar access"""
    try:
        status = google_calendar_service.check_user_authorization(user_id)
        return jsonify(status)
        
    except Exception as e:
        return jsonify({'error': f'Status check failed: {str(e)}'}), 500

@improved_reminders.route('/test-services')
def test_services():
    """Test endpoint to verify services are working"""
    try:
        results = {}
        
        # Test SendGrid
        if sendgrid_email_service.api_key:
            connection_test = sendgrid_email_service.test_connection()
            results['sendgrid'] = {
                'configured': True,
                'connection': connection_test
            }
        else:
            results['sendgrid'] = {
                'configured': False,
                'message': 'Set SENDGRID_API_KEY in .env'
            }
        
        # Test Calendar OAuth setup
        auth_url, _ = google_calendar_service.get_oauth_url("test_user")
        results['calendar'] = {
            'oauth_configured': bool(auth_url),
            'message': 'OAuth URL generation successful' if auth_url else 'Need credentials.json'
        }
        
        # Test .ics generation
        test_contest = {
            'name': 'Test Contest',
            'platform': 'Test Platform',
            'start_time': '2025-05-15T14:30:00Z',
            'duration_minutes': 90,
            'url': 'https://example.com/contest'
        }
        
        ics_content = calendar_fallback_service.generate_ics_content(test_contest)
        results['ics_fallback'] = {
            'working': bool(ics_content and 'BEGIN:VCALENDAR' in ics_content),
            'message': '.ics file generation successful' if ics_content else 'Failed to generate .ics'
        }
        
        return jsonify({
            'success': True,
            'message': 'Service test completed',
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': f'Service test failed: {str(e)}'}), 500

# Usage example in your main app.py:
"""
from backend.routes.improved_reminders import improved_reminders

app.register_blueprint(improved_reminders, url_prefix='/api')
"""
