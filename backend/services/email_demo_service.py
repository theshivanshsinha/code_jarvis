import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from .email_service import email_service

class EmailDemoService:
    """Demo service for testing email functionality without requiring full SMTP setup"""
    
    def __init__(self):
        self.demo_mode = True
        self.sent_emails = []  # Store sent emails for demo purposes
    
    def test_email_configuration(self) -> Dict:
        """Test email configuration and return status"""
        try:
            smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', '587'))
            smtp_username = os.getenv('SMTP_USERNAME', '')
            smtp_password = os.getenv('SMTP_PASSWORD', '')
            
            if not smtp_username:
                return {
                    "status": "error",
                    "message": "SMTP_USERNAME not configured",
                    "config": {
                        "server": smtp_server,
                        "port": smtp_port,
                        "username": "Not configured"
                    }
                }
            
            if smtp_password == 'your-gmail-app-password-here' or not smtp_password:
                return {
                    "status": "warning", 
                    "message": "Gmail App Password not set up. Emails will be simulated.",
                    "instructions": [
                        "1. Go to Google Account Settings",
                        "2. Enable 2-Factor Authentication",
                        "3. Generate App Password for 'Mail'", 
                        "4. Update SMTP_PASSWORD in .env file",
                        "5. Restart the application"
                    ],
                    "config": {
                        "server": smtp_server,
                        "port": smtp_port,
                        "username": smtp_username,
                        "password_configured": False
                    }
                }
            
            # Test SMTP connection
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
            
            return {
                "status": "success",
                "message": "Email configuration is working!",
                "config": {
                    "server": smtp_server,
                    "port": smtp_port,
                    "username": smtp_username,
                    "password_configured": True
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Email configuration test failed: {str(e)}",
                "config": {
                    "server": smtp_server,
                    "port": smtp_port,
                    "username": smtp_username
                }
            }
    
    def send_test_email(self, to_email: str = None) -> Dict:
        """Send a test email to verify functionality"""
        target_email = to_email or os.getenv('SMTP_USERNAME', 'kumarshivanshsinha@gmail.com')
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>CodeJarvis Test Email</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 8px; }
                .content { padding: 20px; background: #f9f9f9; border-radius: 8px; margin-top: 20px; }
                .success { color: #28a745; font-weight: bold; }
                .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚡ CodeJarvis Email Test</h1>
                    <p>Your email configuration is working!</p>
                </div>
                <div class="content">
                    <h2 class="success">✅ Success!</h2>
                    <p>Congratulations! Your CodeJarvis email system is properly configured and ready to send:</p>
                    <ul>
                        <li>🏆 Contest reminders (1 day and 1 hour before)</li>
                        <li>🚀 Daily coding practice reminders</li>
                        <li>📊 Weekly coding progress summaries</li>
                        <li>🎯 Achievement notifications</li>
                    </ul>
                    
                    <h3>Next Steps:</h3>
                    <ol>
                        <li>Set up contest reminders in the app</li>
                        <li>Configure your daily coding schedule</li>
                        <li>Connect your coding platforms (LeetCode, Codeforces, etc.)</li>
                        <li>Enjoy automated reminders to boost your coding journey!</li>
                    </ol>
                    
                    <p><strong>Test sent at:</strong> {timestamp}</p>
                </div>
                <div class="footer">
                    <p>© 2024 CodeJarvis - Your AI Coding Companion</p>
                </div>
            </div>
        </body>
        </html>
        """.format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        config_test = self.test_email_configuration()
        
        if config_test["status"] == "success":
            success = email_service.send_email(
                to_email=target_email,
                subject="🚀 CodeJarvis Email Test - Configuration Working!",
                html_content=html_content
            )
            
            if success:
                return {
                    "status": "success", 
                    "message": f"Test email sent successfully to {target_email}",
                    "email_sent": True
                }
            else:
                return {
                    "status": "error",
                    "message": "Failed to send test email",
                    "email_sent": False
                }
        else:
            # Demo mode - simulate email sending
            demo_email = {
                "to": target_email,
                "subject": "🚀 CodeJarvis Email Test - Configuration Working!",
                "content": html_content,
                "sent_at": datetime.now().isoformat(),
                "type": "test_email"
            }
            self.sent_emails.append(demo_email)
            
            return {
                "status": "demo",
                "message": f"Email simulated (Demo Mode) - would be sent to {target_email}",
                "email_sent": False,
                "demo_email": demo_email,
                "configuration": config_test
            }
    
    def send_demo_contest_reminder(self, user_email: str = None, user_name: str = "Coder") -> Dict:
        """Send a demo contest reminder email"""
        target_email = user_email or os.getenv('SMTP_USERNAME', 'kumarshivanshsinha@gmail.com')
        contest_date = datetime.now() + timedelta(hours=1)  # Contest in 1 hour
        
        success = email_service.send_contest_reminder_email(
            user_email=target_email,
            user_name=user_name,
            contest_name="Codeforces Round #900 (Div. 2)",
            contest_date=contest_date,
            contest_url="https://codeforces.com/contest/1900",
            time_until="1 hour"
        )
        
        if success or not os.getenv('SMTP_PASSWORD') or os.getenv('SMTP_PASSWORD') == 'your-gmail-app-password-here':
            demo_email = {
                "to": target_email,
                "subject": f"⏰ Contest Reminder: Codeforces Round #900 (Div. 2) starts 1 hour!",
                "type": "contest_reminder",
                "contest": "Codeforces Round #900 (Div. 2)",
                "time_until": "1 hour",
                "sent_at": datetime.now().isoformat()
            }
            self.sent_emails.append(demo_email)
            
            return {
                "status": "demo" if not success else "success",
                "message": f"Contest reminder {'sent' if success else 'simulated'} to {target_email}",
                "email_sent": success,
                "demo_email": demo_email
            }
        
        return {
            "status": "error",
            "message": "Failed to send contest reminder",
            "email_sent": False
        }
    
    def send_demo_daily_reminder(self, user_email: str = None, user_name: str = "Coder") -> Dict:
        """Send a demo daily coding reminder"""
        target_email = user_email or os.getenv('SMTP_USERNAME', 'kumarshivanshsinha@gmail.com')
        
        stats = {
            "total_solved": 150,
            "current_streak": 5,
            "platforms": ["leetcode", "codeforces", "atcoder"]
        }
        
        success = email_service.send_daily_coding_reminder(
            user_email=target_email,
            user_name=user_name,
            stats=stats
        )
        
        demo_email = {
            "to": target_email,
            "subject": f"🚀 Daily Coding Challenge - Keep Going, {user_name}!",
            "type": "daily_reminder",
            "stats": stats,
            "sent_at": datetime.now().isoformat()
        }
        self.sent_emails.append(demo_email)
        
        return {
            "status": "demo" if not success else "success",
            "message": f"Daily reminder {'sent' if success else 'simulated'} to {target_email}",
            "email_sent": success,
            "demo_email": demo_email
        }
    
    def get_sent_emails(self) -> List[Dict]:
        """Get list of all sent/simulated emails"""
        return self.sent_emails
    
    def clear_sent_emails(self):
        """Clear the sent emails log"""
        self.sent_emails.clear()

# Global demo service instance
email_demo_service = EmailDemoService()
