"""
Test reminders endpoint without authentication
Use this for testing the new email and calendar services!
"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import os

# Import the NEW improved services
try:
    from backend.services.sendgrid_email_service import sendgrid_email_service
    from backend.services.improved_calendar_service import google_calendar_service, calendar_fallback_service
    SENDGRID_AVAILABLE = True
except ImportError:
    print("⚠️  New services not found - falling back to old services")
    try:
        from backend.services.email_service import email_service
        from backend.services.calendar_service import google_calendar_service as old_calendar_service
        SENDGRID_AVAILABLE = False
    except ImportError:
        print("❌ No email services found")
        SENDGRID_AVAILABLE = False

test_reminders_bp = Blueprint('test_reminders', __name__)

@test_reminders_bp.route('/test', methods=['GET'])
def test_endpoint():
    """Simple test endpoint to verify API is working"""
    return jsonify({
        'status': 'success',
        'message': 'Test reminders endpoint is working!',
        'timestamp': datetime.utcnow().isoformat(),
        'services_available': {
            'sendgrid': SENDGRID_AVAILABLE and bool(os.getenv('SENDGRID_API_KEY')),
            'calendar': os.path.exists('credentials.json'),
            'ics_fallback': True
        }
    })

@test_reminders_bp.route('/create-test', methods=['POST'])
def create_test_reminder():
    """Create a test reminder WITHOUT authentication - for testing only!"""
    try:
        # Get request data
        data = request.get_json() or {}
        
        # Use test data if not provided
        test_data = {
            'user_email': data.get('user_email', 'test@example.com'),
            'user_name': data.get('user_name', 'Test User'),
            'contest_name': data.get('contest_name', 'LeetCode Weekly Contest 350'),
            'contest_date': data.get('contest_date', (datetime.utcnow() + timedelta(hours=2)).isoformat()),
            'contest_url': data.get('contest_url', 'https://leetcode.com/contest/weekly-350/'),
            'platform': data.get('platform', 'LeetCode')
        }
        
        response = {
            'success': True,
            'message': 'Test reminder created',
            'services_used': [],
            'data': test_data
        }
        
        # 1. Try SendGrid email (if available)
        email_sent = False
        if SENDGRID_AVAILABLE and os.getenv('SENDGRID_API_KEY'):
            try:
                email_sent = sendgrid_email_service.send_reminder_confirmation(
                    user_email=test_data['user_email'],
                    user_name=test_data['user_name'],
                    contest_name=test_data['contest_name'],
                    contest_date=datetime.fromisoformat(test_data['contest_date'].replace('Z', '')),
                    contest_url=test_data['contest_url']
                )
                if email_sent:
                    response['services_used'].append('sendgrid_email')
                    response['email_status'] = 'sent'
                else:
                    response['email_status'] = 'failed'
            except Exception as e:
                response['email_status'] = f'error: {str(e)}'
        else:
            response['email_status'] = 'not_configured'
            response['email_setup'] = 'Add SENDGRID_API_KEY to .env file'
        
        # 2. Try calendar integration
        calendar_event_id = None
        if os.path.exists('credentials.json'):
            try:
                # For testing, we'll just check if we can generate OAuth URL
                auth_url, state = google_calendar_service.get_oauth_url("test_user_123")
                if auth_url:
                    response['services_used'].append('calendar_oauth_ready')
                    response['calendar_status'] = 'oauth_available'
                    response['calendar_oauth_url'] = auth_url
                else:
                    response['calendar_status'] = 'oauth_failed'
            except Exception as e:
                response['calendar_status'] = f'error: {str(e)}'
        else:
            response['calendar_status'] = 'not_configured'
            response['calendar_setup'] = 'Add credentials.json file'
        
        # 3. Generate .ics file (always works!)
        try:
            ics_content = calendar_fallback_service.generate_ics_content({
                'name': test_data['contest_name'],
                'platform': test_data['platform'],
                'start_time': test_data['contest_date'],
                'duration_minutes': 90,
                'url': test_data['contest_url']
            })
            
            if ics_content and 'BEGIN:VCALENDAR' in ics_content:
                response['services_used'].append('ics_generation')
                response['ics_status'] = 'generated'
                response['ics_length'] = len(ics_content)
            else:
                response['ics_status'] = 'failed'
        except Exception as e:
            response['ics_status'] = f'error: {str(e)}'
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Test reminder failed: {str(e)}'
        }), 500

@test_reminders_bp.route('/send-test-email', methods=['POST'])
def send_test_email():
    """Send a test email using the new services"""
    try:
        data = request.get_json() or {}
        
        if not SENDGRID_AVAILABLE:
            return jsonify({
                'success': False,
                'error': 'SendGrid service not available',
                'setup': 'Install sendgrid package and add SENDGRID_API_KEY to .env'
            }), 400
        
        if not os.getenv('SENDGRID_API_KEY'):
            return jsonify({
                'success': False,
                'error': 'SendGrid not configured',
                'setup': 'Add SENDGRID_API_KEY to your .env file'
            }), 400
        
        # Send test email
        success = sendgrid_email_service.send_contest_reminder(
            user_email=data.get('user_email', 'test@example.com'),
            user_name=data.get('user_name', 'Test User'),
            contest_name=data.get('contest_name', 'Test Contest'),
            contest_date=datetime.utcnow() + timedelta(hours=1),
            contest_url=data.get('contest_url', 'https://example.com/contest'),
            time_until='1 hour'
        )
        
        return jsonify({
            'success': success,
            'message': 'Test email sent!' if success else 'Email sending failed',
            'service': 'sendgrid'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Test email failed: {str(e)}'
        }), 500

@test_reminders_bp.route('/download-test-ics', methods=['GET'])
def download_test_ics():
    """Download a test .ics calendar file"""
    try:
        # Generate test contest data
        test_contest = {
            'name': 'CodeJarvis Test Contest',
            'platform': 'LeetCode',
            'start_time': (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'duration_minutes': 90,
            'url': 'https://leetcode.com/contest/test/'
        }
        
        # Generate .ics content
        ics_content = calendar_fallback_service.generate_ics_content(test_contest)
        
        # Return as downloadable file
        from flask import Response
        return Response(
            ics_content,
            mimetype='text/calendar',
            headers={
                'Content-Disposition': 'attachment; filename="test_contest.ics"'
            }
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'ICS generation failed: {str(e)}'
        }), 500

@test_reminders_bp.route('/status', methods=['GET'])
def get_services_status():
    """Get status of all available services"""
    try:
        status = {
            'timestamp': datetime.utcnow().isoformat(),
            'services': {}
        }
        
        # Check SendGrid
        if SENDGRID_AVAILABLE:
            api_key = os.getenv('SENDGRID_API_KEY')
            if api_key:
                try:
                    connection_test = sendgrid_email_service.test_connection()
                    status['services']['sendgrid'] = {
                        'available': True,
                        'configured': True,
                        'connection': connection_test,
                        'api_key_present': bool(api_key)
                    }
                except Exception as e:
                    status['services']['sendgrid'] = {
                        'available': True,
                        'configured': True,
                        'connection': False,
                        'error': str(e)
                    }
            else:
                status['services']['sendgrid'] = {
                    'available': True,
                    'configured': False,
                    'message': 'Add SENDGRID_API_KEY to .env file'
                }
        else:
            status['services']['sendgrid'] = {
                'available': False,
                'message': 'SendGrid package not installed'
            }
        
        # Check Google Calendar
        if os.path.exists('credentials.json'):
            try:
                auth_url, _ = google_calendar_service.get_oauth_url("test_user")
                status['services']['google_calendar'] = {
                    'available': True,
                    'configured': True,
                    'oauth_working': bool(auth_url),
                    'credentials_file': True
                }
            except Exception as e:
                status['services']['google_calendar'] = {
                    'available': True,
                    'configured': False,
                    'error': str(e)
                }
        else:
            status['services']['google_calendar'] = {
                'available': True,
                'configured': False,
                'message': 'Add credentials.json file'
            }
        
        # Check .ics generation (always available)
        try:
            test_ics = calendar_fallback_service.generate_ics_content({
                'name': 'Test',
                'platform': 'Test',
                'start_time': '2025-05-15T14:30:00Z',
                'duration_minutes': 90,
                'url': 'https://example.com'
            })
            status['services']['ics_fallback'] = {
                'available': True,
                'working': bool(test_ics and 'BEGIN:VCALENDAR' in test_ics)
            }
        except Exception as e:
            status['services']['ics_fallback'] = {
                'available': False,
                'error': str(e)
            }
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Status check failed: {str(e)}'
        }), 500
