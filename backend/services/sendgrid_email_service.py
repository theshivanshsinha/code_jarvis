import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from datetime import datetime
from typing import Dict, List, Optional
from .email_templates import EmailTemplates

class SendGridEmailService:
    def __init__(self):
        """Initialize SendGrid email service - much simpler than SMTP!"""
        # Get SendGrid API key from environment
        self.api_key = os.getenv('SENDGRID_API_KEY')
        self.from_email = os.getenv('FROM_EMAIL', 'noreply@codejarvis.com')
        self.from_name = os.getenv('FROM_NAME', 'CodeJarvis')
        
        if not self.api_key:
            print("⚠️  SENDGRID_API_KEY not found in environment variables")
            print("   Set up your SendGrid account and add the API key to your .env file")
        
        self.sg = sendgrid.SendGridAPIClient(api_key=self.api_key) if self.api_key else None
        self.templates = EmailTemplates()
    
    def send_email(self, to_email: str, subject: str, html_content: str, 
                  text_content: str = None) -> bool:
        """Send an email using SendGrid API - much more reliable than SMTP!"""
        if not self.sg:
            print("❌ SendGrid not configured. Please add SENDGRID_API_KEY to your .env file")
            return False
        
        try:
            # Create the email
            from_email = Email(self.from_email, self.from_name)
            to_email = To(to_email)
            
            # SendGrid automatically handles both HTML and text versions
            content = Content("text/html", html_content)
            
            mail = Mail(from_email, to_email, subject, content)
            
            # Add plain text version if provided
            if text_content:
                mail.add_content(Content("text/plain", text_content))
            
            # Send the email
            response = self.sg.send(mail)
            
            # SendGrid returns 202 for successful queuing
            if response.status_code == 202:
                print(f"✅ Email sent successfully to {to_email}")
                return True
            else:
                print(f"❌ SendGrid returned status code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to send email via SendGrid: {str(e)}")
            return False
    
    def send_contest_reminder(self, user_email: str, user_name: str, 
                            contest_name: str, contest_date: datetime, 
                            contest_url: str, time_until: str) -> bool:
        """Send contest reminder email"""
        html_content = self.templates.render_contest_reminder({
            'user_name': user_name,
            'contest_name': contest_name,
            'contest_date': contest_date.strftime('%B %d, %Y at %I:%M %p'),
            'contest_url': contest_url,
            'time_until': time_until
        })
        
        subject = f"⏰ Contest Alert: {contest_name} starts {time_until}!"
        return self.send_email(user_email, subject, html_content)
    
    def send_reminder_confirmation(self, user_email: str, user_name: str, 
                                 contest_name: str, contest_date: datetime, 
                                 contest_url: str) -> bool:
        """Send confirmation when reminder is created"""
        html_content = self.templates.render_reminder_confirmation({
            'user_name': user_name,
            'contest_name': contest_name,
            'contest_date': contest_date.strftime('%B %d, %Y at %I:%M %p'),
            'contest_url': contest_url
        })
        
        subject = f"✅ Reminder Set: {contest_name}"
        return self.send_email(user_email, subject, html_content)
    
    def send_daily_motivation(self, user_email: str, user_name: str, 
                            stats: Dict) -> bool:
        """Send daily coding motivation"""
        html_content = self.templates.render_daily_motivation({
            'user_name': user_name,
            'total_solved': stats.get('total_solved', 0),
            'current_streak': stats.get('current_streak', 0),
            'favorite_platform': stats.get('favorite_platform', 'LeetCode')
        })
        
        subject = f"🚀 Daily Coding Challenge - {user_name}!"
        return self.send_email(user_email, subject, html_content)
    
    def send_weekly_summary(self, user_email: str, user_name: str, 
                          summary: Dict) -> bool:
        """Send weekly coding summary"""
        html_content = self.templates.render_weekly_summary({
            'user_name': user_name,
            'problems_solved': summary.get('problems_solved', 0),
            'contests_participated': summary.get('contests_participated', 0),
            'achievements': summary.get('achievements', [])
        })
        
        subject = f"📊 Your Weekly Coding Summary - {user_name}"
        return self.send_email(user_email, subject, html_content)
    
    def test_connection(self) -> bool:
        """Test SendGrid connection"""
        if not self.sg:
            return False
        
        try:
            # SendGrid API health check
            response = self.sg.user.get()
            return response.status_code == 200
        except Exception as e:
            print(f"SendGrid connection test failed: {str(e)}")
            return False

# Global instance
sendgrid_email_service = SendGridEmailService()
