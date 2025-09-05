"""
SUPER SIMPLE EMAIL REMINDERS - NO AUTHENTICATION REQUIRED!
Just provide email and contest details - we'll handle the rest!
Works locally and in production without any JWT token nonsense.
"""

from flask import Blueprint, jsonify, request, send_file
from datetime import datetime, timedelta
import os
import uuid
import json
from typing import Dict, Optional

# Import the simplified email services
try:
    from backend.services.sendgrid_email_service import sendgrid_email_service
    from backend.services.improved_calendar_service import calendar_fallback_service
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False
    print("⚠️  SendGrid service not found")

# For EmailJS alternative (frontend-only solution)
try:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    SMTP_AVAILABLE = True
except ImportError:
    SMTP_AVAILABLE = False

simple_reminders_bp = Blueprint('simple_reminders', __name__)

# Simple in-memory storage for reminders (replace with database in production)
reminders_store = {}

def validate_email(email: str) -> bool:
    """Simple email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def send_simple_email_smtp(to_email: str, subject: str, html_content: str) -> bool:
    """Send email using simple SMTP (fallback method)"""
    try:
        # Get SMTP settings from environment
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_username = os.getenv('SMTP_USERNAME', '')
        smtp_password = os.getenv('SMTP_PASSWORD', '')
        
        if not smtp_username or not smtp_password:
            print("⚠️  SMTP credentials not configured")
            return False
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"CodeJarvis <{smtp_username}>"
        msg['To'] = to_email
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"❌ SMTP email failed: {str(e)}")
        return False

def create_simple_html_email(user_name: str, contest_name: str, contest_date: str, contest_url: str, email_type: str = 'confirmation') -> str:
    """Create a simple HTML email template"""
    
    if email_type == 'reminder':
        subject_emoji = "⏰"
        header_text = "Contest Starting Soon!"
        message = f"Your contest {contest_name} is starting soon!"
        urgency_class = "urgent"
    else:
        subject_emoji = "✅"
        header_text = "Reminder Set Successfully!"
        message = f"We've set up your reminder for {contest_name}."
        urgency_class = "success"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{header_text} - CodeJarvis</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 24px; }}
            .content {{ padding: 30px; }}
            .contest-box {{ background: #f8f9ff; border-left: 4px solid #667eea; padding: 20px; margin: 20px 0; border-radius: 5px; }}
            .success {{ background: #f0f9f4; border-left-color: #22c55e; }}
            .urgent {{ background: #fef2f2; border-left-color: #ef4444; }}
            .button {{ display: inline-block; background: #667eea; color: white; text-decoration: none; padding: 12px 24px; border-radius: 5px; margin: 20px 0; }}
            .footer {{ background: #f8f9fa; text-align: center; padding: 20px; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{subject_emoji} CodeJarvis</h1>
                <p>{header_text}</p>
            </div>
            <div class="content">
                <p>Hi {user_name},</p>
                <p>{message}</p>
                
                <div class="contest-box {urgency_class}">
                    <h3>🏆 {contest_name}</h3>
                    <p><strong>Date:</strong> {contest_date}</p>
                    <p>Don't miss this contest!</p>
                </div>
                
                <div style="text-align: center;">
                    <a href="{contest_url}" class="button">View Contest</a>
                </div>
                
                <p>Good luck! 🚀</p>
                <p>- CodeJarvis Team</p>
            </div>
            <div class="footer">
                <p>© 2025 CodeJarvis - Your AI coding companion</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

@simple_reminders_bp.route('/create', methods=['POST'])
def create_simple_reminder():
    """
    Create a contest reminder - NO AUTHENTICATION REQUIRED!
    Just send: email, name, contest details - we handle the rest!
    """
    try:
        data = request.get_json() or {}
        
        # Validate required fields
        required_fields = ['user_email', 'contest_name', 'contest_date']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'required': {
                    'user_email': 'Your email address',
                    'contest_name': 'Name of the contest',
                    'contest_date': 'Contest start date (ISO format)',
                    'user_name': 'Your name (optional)',
                    'contest_url': 'Contest URL (optional)',
                    'platform': 'Platform name (optional)'
                }
            }), 400
        
        # Validate email
        if not validate_email(data['user_email']):
            return jsonify({
                'success': False,
                'error': 'Invalid email address format'
            }), 400
        
        # Extract and normalize data
        reminder_data = {
            'id': str(uuid.uuid4()),
            'user_email': data['user_email'].strip().lower(),
            'user_name': data.get('user_name', 'Contest Participant').strip(),
            'contest_name': data['contest_name'].strip(),
            'contest_date': data['contest_date'],
            'contest_url': data.get('contest_url', '').strip(),
            'platform': data.get('platform', 'Contest Platform').strip(),
            'created_at': datetime.utcnow().isoformat(),
            'status': 'active'
        }
        
        # Store reminder (in production, use a proper database)
        reminders_store[reminder_data['id']] = reminder_data
        
        response = {
            'success': True,
            'reminder_id': reminder_data['id'],
            'message': 'Reminder created successfully!',
            'services_used': [],
            'next_steps': []
        }
        
        # Try to send confirmation email
        email_sent = False
        email_method = None
        
        # Method 1: Try SendGrid (best option)
        if SENDGRID_AVAILABLE and os.getenv('SENDGRID_API_KEY'):
            try:
                contest_datetime = datetime.fromisoformat(reminder_data['contest_date'].replace('Z', ''))
                email_sent = sendgrid_email_service.send_reminder_confirmation(
                    user_email=reminder_data['user_email'],
                    user_name=reminder_data['user_name'],
                    contest_name=reminder_data['contest_name'],
                    contest_date=contest_datetime,
                    contest_url=reminder_data['contest_url']
                )
                email_method = 'SendGrid'
                if email_sent:
                    response['services_used'].append('sendgrid_email')
            except Exception as e:
                print(f"SendGrid failed: {str(e)}")
        
        # Method 2: Try simple SMTP (fallback)
        if not email_sent and SMTP_AVAILABLE:
            try:
                html_content = create_simple_html_email(
                    reminder_data['user_name'],
                    reminder_data['contest_name'],
                    reminder_data['contest_date'],
                    reminder_data['contest_url'],
                    'confirmation'
                )
                email_sent = send_simple_email_smtp(
                    reminder_data['user_email'],
                    f"✅ Reminder Set: {reminder_data['contest_name']}",
                    html_content
                )
                email_method = 'SMTP'
                if email_sent:
                    response['services_used'].append('smtp_email')
            except Exception as e:
                print(f"SMTP failed: {str(e)}")
        
        # Update response based on email result
        if email_sent:
            response['email_status'] = 'sent'
            response['email_method'] = email_method
            response['next_steps'].append(f'✅ Confirmation email sent via {email_method}')
        else:
            response['email_status'] = 'failed'
            response['next_steps'].append('⚠️ Email sending failed - but reminder is still created')
            response['email_setup_help'] = {
                'sendgrid': 'Add SENDGRID_API_KEY to .env for reliable email delivery',
                'smtp': 'Add SMTP_USERNAME, SMTP_PASSWORD to .env for email sending'
            }
        
        # Generate calendar file (.ics) - always works!
        try:
            ics_content = calendar_fallback_service.generate_ics_content({
                'name': reminder_data['contest_name'],
                'platform': reminder_data['platform'],
                'start_time': reminder_data['contest_date'],
                'duration_minutes': 120,
                'url': reminder_data['contest_url']
            })
            
            if ics_content:
                # Save .ics file temporarily
                ics_filename = f"contest_{reminder_data['id']}.ics"
                ics_path = os.path.join('temp_ics', ics_filename)
                os.makedirs('temp_ics', exist_ok=True)
                
                with open(ics_path, 'w', encoding='utf-8') as f:
                    f.write(ics_content)
                
                response['services_used'].append('ics_calendar')
                response['ics_download_url'] = f'/api/simple-reminders/download-ics/{reminder_data["id"]}'
                response['next_steps'].append('📅 Calendar file (.ics) generated - download to import into any calendar app')
        
        except Exception as e:
            print(f"ICS generation failed: {str(e)}")
        
        # Schedule reminder emails (simplified)
        try:
            contest_datetime = datetime.fromisoformat(reminder_data['contest_date'].replace('Z', ''))
            now = datetime.utcnow()
            
            if contest_datetime > now:
                time_until = contest_datetime - now
                response['next_steps'].append(f'⏰ Contest starts in {time_until.days} days, {time_until.seconds // 3600} hours')
                
                # In a real app, you'd use a proper task queue like Celery
                # For now, we'll just store the reminder and send manually
                response['next_steps'].append('📧 Use the reminder endpoints to send manual reminders')
        
        except Exception as e:
            print(f"Reminder scheduling failed: {str(e)}")
        
        return jsonify(response), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to create reminder: {str(e)}'
        }), 500

@simple_reminders_bp.route('/send-reminder/<reminder_id>', methods=['POST'])
def send_contest_reminder(reminder_id):
    """Send a contest reminder email manually"""
    try:
        # Get reminder from store
        reminder = reminders_store.get(reminder_id)
        if not reminder:
            return jsonify({
                'success': False,
                'error': 'Reminder not found'
            }), 404
        
        # Calculate time until contest
        try:
            contest_datetime = datetime.fromisoformat(reminder['contest_date'].replace('Z', ''))
            now = datetime.utcnow()
            time_delta = contest_datetime - now
            
            if time_delta.total_seconds() <= 0:
                time_until = "now"
            elif time_delta.days > 0:
                time_until = f"{time_delta.days} days"
            else:
                hours = time_delta.seconds // 3600
                time_until = f"{hours} hours"
        except:
            time_until = "soon"
        
        # Send reminder email
        email_sent = False
        email_method = None
        
        # Try SendGrid first
        if SENDGRID_AVAILABLE and os.getenv('SENDGRID_API_KEY'):
            try:
                email_sent = sendgrid_email_service.send_contest_reminder(
                    user_email=reminder['user_email'],
                    user_name=reminder['user_name'],
                    contest_name=reminder['contest_name'],
                    contest_date=contest_datetime,
                    contest_url=reminder['contest_url'],
                    time_until=time_until
                )
                email_method = 'SendGrid'
            except Exception as e:
                print(f"SendGrid reminder failed: {str(e)}")
        
        # Try SMTP fallback
        if not email_sent and SMTP_AVAILABLE:
            try:
                html_content = create_simple_html_email(
                    reminder['user_name'],
                    reminder['contest_name'],
                    reminder['contest_date'],
                    reminder['contest_url'],
                    'reminder'
                )
                email_sent = send_simple_email_smtp(
                    reminder['user_email'],
                    f"⏰ Contest Reminder: {reminder['contest_name']} starts {time_until}!",
                    html_content
                )
                email_method = 'SMTP'
            except Exception as e:
                print(f"SMTP reminder failed: {str(e)}")
        
        return jsonify({
            'success': email_sent,
            'message': 'Reminder email sent!' if email_sent else 'Failed to send reminder email',
            'email_method': email_method,
            'time_until_contest': time_until,
            'contest_name': reminder['contest_name']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to send reminder: {str(e)}'
        }), 500

@simple_reminders_bp.route('/download-ics/<reminder_id>', methods=['GET'])
def download_reminder_ics(reminder_id):
    """Download calendar file for a specific reminder"""
    try:
        # Get reminder from store
        reminder = reminders_store.get(reminder_id)
        if not reminder:
            return jsonify({
                'success': False,
                'error': 'Reminder not found'
            }), 404
        
        # Check if ICS file exists
        ics_filename = f"contest_{reminder_id}.ics"
        ics_path = os.path.join('temp_ics', ics_filename)
        
        if os.path.exists(ics_path):
            return send_file(
                ics_path,
                as_attachment=True,
                download_name=f"{reminder['contest_name'].replace(' ', '_')}.ics",
                mimetype='text/calendar'
            )
        else:
            # Generate on-the-fly
            ics_content = calendar_fallback_service.generate_ics_content({
                'name': reminder['contest_name'],
                'platform': reminder['platform'],
                'start_time': reminder['contest_date'],
                'duration_minutes': 120,
                'url': reminder['contest_url']
            })
            
            from flask import Response
            return Response(
                ics_content,
                mimetype='text/calendar',
                headers={
                    'Content-Disposition': f'attachment; filename="{reminder["contest_name"].replace(" ", "_")}.ics"'
                }
            )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to download calendar file: {str(e)}'
        }), 500

@simple_reminders_bp.route('/list', methods=['GET'])
def list_simple_reminders():
    """List all reminders (no authentication required)"""
    try:
        # In production, you'd filter by user or use some other identifier
        reminders_list = []
        
        for reminder in reminders_store.values():
            try:
                contest_datetime = datetime.fromisoformat(reminder['contest_date'].replace('Z', ''))
                now = datetime.utcnow()
                is_upcoming = contest_datetime > now
                
                reminders_list.append({
                    'id': reminder['id'],
                    'contest_name': reminder['contest_name'],
                    'platform': reminder['platform'],
                    'contest_date': reminder['contest_date'],
                    'user_email': reminder['user_email'][:3] + '***' + reminder['user_email'][-10:],  # Partial hide
                    'created_at': reminder['created_at'],
                    'status': 'upcoming' if is_upcoming else 'past',
                    'ics_download_url': f'/api/simple-reminders/download-ics/{reminder["id"]}'
                })
            except:
                continue
        
        # Sort by creation date
        reminders_list.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify({
            'success': True,
            'reminders': reminders_list,
            'total': len(reminders_list)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to list reminders: {str(e)}'
        }), 500

@simple_reminders_bp.route('/test-email', methods=['POST'])
def test_email_sending():
    """Test email sending functionality"""
    try:
        data = request.get_json() or {}
        test_email = data.get('email', 'test@example.com')
        
        if not validate_email(test_email):
            return jsonify({
                'success': False,
                'error': 'Invalid email address'
            }), 400
        
        # Create test email content
        html_content = create_simple_html_email(
            "Test User",
            "Test Contest - EmailJS Setup",
            datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "https://example.com/contest",
            "confirmation"
        )
        
        email_sent = False
        email_method = None
        
        # Try SendGrid
        if SENDGRID_AVAILABLE and os.getenv('SENDGRID_API_KEY'):
            try:
                email_sent = sendgrid_email_service.send_email(
                    test_email,
                    "✅ Test Email from CodeJarvis",
                    html_content
                )
                email_method = 'SendGrid'
            except Exception as e:
                print(f"SendGrid test failed: {str(e)}")
        
        # Try SMTP
        if not email_sent and SMTP_AVAILABLE:
            try:
                email_sent = send_simple_email_smtp(
                    test_email,
                    "✅ Test Email from CodeJarvis",
                    html_content
                )
                email_method = 'SMTP'
            except Exception as e:
                print(f"SMTP test failed: {str(e)}")
        
        return jsonify({
            'success': email_sent,
            'message': f'Test email sent via {email_method}!' if email_sent else 'Email sending failed',
            'email_method': email_method,
            'recipient': test_email,
            'available_methods': {
                'sendgrid': SENDGRID_AVAILABLE and bool(os.getenv('SENDGRID_API_KEY')),
                'smtp': SMTP_AVAILABLE and bool(os.getenv('SMTP_USERNAME'))
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Test email failed: {str(e)}'
        }), 500

@simple_reminders_bp.route('/status', methods=['GET'])
def get_simple_status():
    """Get status of email services (no authentication required)"""
    try:
        status = {
            'timestamp': datetime.utcnow().isoformat(),
            'total_reminders': len(reminders_store),
            'email_services': {}
        }
        
        # Check SendGrid
        if SENDGRID_AVAILABLE:
            sendgrid_configured = bool(os.getenv('SENDGRID_API_KEY'))
            status['email_services']['sendgrid'] = {
                'available': True,
                'configured': sendgrid_configured,
                'status': 'Ready' if sendgrid_configured else 'Need API key in .env'
            }
        else:
            status['email_services']['sendgrid'] = {
                'available': False,
                'status': 'Package not installed'
            }
        
        # Check SMTP
        smtp_configured = bool(os.getenv('SMTP_USERNAME')) and bool(os.getenv('SMTP_PASSWORD'))
        status['email_services']['smtp'] = {
            'available': SMTP_AVAILABLE,
            'configured': smtp_configured,
            'status': 'Ready' if smtp_configured else 'Need SMTP credentials in .env'
        }
        
        # Calendar service
        status['calendar_service'] = {
            'ics_generation': True,
            'google_calendar': os.path.exists('credentials.json')
        }
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Status check failed: {str(e)}'
        }), 500
