from flask import Blueprint, jsonify, request
from ..services.email_demo_service import email_demo_service
from ..services.email_service import email_service
import os

email_test_bp = Blueprint("email_test", __name__)

@email_test_bp.get("/config")
def get_email_config():
    """Get current email configuration status"""
    return jsonify(email_demo_service.test_email_configuration())

@email_test_bp.post("/test")
def send_test_email():
    """Send a test email to verify configuration"""
    body = request.get_json(force=True, silent=True) or {}
    email = body.get('email') or os.getenv('SMTP_USERNAME', 'kumarshivanshsinha@gmail.com')
    
    result = email_demo_service.send_test_email(email)
    return jsonify(result)

@email_test_bp.post("/demo/contest")
def send_demo_contest_reminder():
    """Send a demo contest reminder email"""
    body = request.get_json(force=True, silent=True) or {}
    email = body.get('email') or os.getenv('SMTP_USERNAME', 'kumarshivanshsinha@gmail.com')
    name = body.get('name', 'Coder')
    
    result = email_demo_service.send_demo_contest_reminder(email, name)
    return jsonify(result)

@email_test_bp.post("/demo/daily")
def send_demo_daily_reminder():
    """Send a demo daily coding reminder email"""
    body = request.get_json(force=True, silent=True) or {}
    email = body.get('email') or os.getenv('SMTP_USERNAME', 'kumarshivanshsinha@gmail.com')
    name = body.get('name', 'Coder')
    
    result = email_demo_service.send_demo_daily_reminder(email, name)
    return jsonify(result)

@email_test_bp.get("/sent")
def get_sent_emails():
    """Get list of sent/simulated emails"""
    return jsonify({
        "emails": email_demo_service.get_sent_emails(),
        "total": len(email_demo_service.get_sent_emails())
    })

@email_test_bp.delete("/sent")
def clear_sent_emails():
    """Clear the sent emails log"""
    email_demo_service.clear_sent_emails()
    return jsonify({"message": "Sent emails log cleared"})

@email_test_bp.get("/instructions")
def get_setup_instructions():
    """Get detailed setup instructions for email configuration"""
    return jsonify({
        "title": "📧 Email Configuration Setup Guide",
        "description": "Follow these steps to set up email reminders with your Gmail account",
        "steps": [
            {
                "step": 1,
                "title": "Enable 2-Factor Authentication",
                "description": "Go to your Google Account settings and enable 2FA if not already enabled",
                "url": "https://myaccount.google.com/security"
            },
            {
                "step": 2,
                "title": "Generate App Password",
                "description": "Create an app-specific password for CodeJarvis",
                "details": [
                    "Go to Google Account > Security > App passwords",
                    "Select 'Mail' as the app type",
                    "Copy the generated 16-character password"
                ],
                "url": "https://myaccount.google.com/apppasswords"
            },
            {
                "step": 3,
                "title": "Update .env File",
                "description": "Replace 'your-gmail-app-password-here' with your app password",
                "file": ".env",
                "setting": "SMTP_PASSWORD=your-generated-app-password"
            },
            {
                "step": 4,
                "title": "Restart Application",
                "description": "Restart the CodeJarvis backend to load the new configuration"
            },
            {
                "step": 5,
                "title": "Test Email",
                "description": "Use the /api/email/test endpoint to verify everything works"
            }
        ],
        "troubleshooting": [
            {
                "issue": "Authentication Error",
                "solution": "Make sure you're using an App Password, not your regular Gmail password"
            },
            {
                "issue": "Connection Timeout",
                "solution": "Check your internet connection and firewall settings"
            },
            {
                "issue": "Emails Not Received",
                "solution": "Check spam folder and ensure the recipient email is correct"
            }
        ],
        "current_config": {
            "smtp_server": os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            "smtp_port": os.getenv('SMTP_PORT', '587'),
            "sender_email": os.getenv('SENDER_EMAIL', 'kumarshivanshsinha@gmail.com'),
            "password_configured": os.getenv('SMTP_PASSWORD', 'your-gmail-app-password-here') != 'your-gmail-app-password-here'
        }
    })

@email_test_bp.get("/preview/<email_type>")
def preview_email(email_type):
    """Preview email templates without sending"""
    if email_type == "contest":
        return jsonify({
            "type": "contest_reminder",
            "subject": "⏰ Contest Reminder: Codeforces Round #900 (Div. 2) starts 1 hour!",
            "preview": "Contest reminder email with countdown, preparation tips, and direct contest link",
            "features": [
                "Urgent countdown banner",
                "Contest details (name, time, platform)",
                "Last-minute preparation tips",
                "Direct link to contest",
                "Motivational content"
            ]
        })
    elif email_type == "daily":
        return jsonify({
            "type": "daily_reminder",
            "subject": "🚀 Daily Coding Challenge - Keep Going, Coder!",
            "preview": "Daily coding motivation with stats and personalized challenges",
            "features": [
                "Personal coding statistics",
                "Current streak information",
                "Motivational quotes",
                "Daily action suggestions",
                "Progress tracking"
            ]
        })
    elif email_type == "weekly":
        return jsonify({
            "type": "weekly_summary",
            "subject": "📊 Your Weekly Coding Summary",
            "preview": "Comprehensive weekly progress report with achievements",
            "features": [
                "Problems solved this week",
                "Contest participation",
                "New achievements unlocked",
                "Performance insights",
                "Next week's goals"
            ]
        })
    else:
        return jsonify({"error": "Unknown email type"}), 400
