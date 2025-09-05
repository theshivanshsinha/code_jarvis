import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Optional

class SimpleEmailService:
    def __init__(self):
        # Gmail SMTP configuration
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.sender_email = 'kumarshivanshsinha@gmail.com'
        self.sender_password = 'Ssinha1518'
        self.sender_name = 'CodeJarvis'
    
    def send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """Send an email using Gmail SMTP"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = to_email
            
            # Create HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Connect to SMTP server and send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✅ Email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_reminder_created_email(self, user_email: str, contest_name: str, contest_date: str, contest_url: str) -> bool:
        """Send confirmation email when reminder is created"""
        subject = f"✅ Reminder Set: {contest_name}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Reminder Set - {contest_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; }}
                .header {{ background: #4a6fa5; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .button {{ 
                    display: inline-block; 
                    background: #4a6fa5; 
                    color: white; 
                    padding: 10px 20px; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    margin: 20px 0; 
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⏰ Contest Reminder Set!</h1>
                </div>
                <div class="content">
                    <p>Hello,</p>
                    <p>We've successfully set up a reminder for:</p>
                    <h2>{contest_name}</h2>
                    <p><strong>Date & Time:</strong> {contest_date}</p>
                    <p>You'll receive email reminders before the contest starts.</p>
                    <p>
                        <a href="{contest_url}" class="button">View Contest Details</a>
                    </p>
                    <p>Happy coding! 🚀</p>
                    <p>— The CodeJarvis Team</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_content)
    
    def send_contest_reminder(self, user_email: str, contest_name: str, contest_date: str, contest_url: str, time_until: str) -> bool:
        """Send contest reminder email"""
        subject = f"⏰ Reminder: {contest_name} starts {time_until}!"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Contest Reminder - {contest_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; }}
                .header {{ background: #ff6b6b; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .button {{ 
                    display: inline-block; 
                    background: #ff6b6b; 
                    color: white; 
                    padding: 10px 20px; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    margin: 20px 0; 
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⏰ Contest Starting Soon!</h1>
                </div>
                <div class="content">
                    <p>Hello,</p>
                    <p>This is a friendly reminder that the contest you're interested in is starting {time_lower}!</p>
                    <h2>{contest_name}</h2>
                    <p><strong>Starts at:</strong> {contest_date}</p>
                    <p>Get ready to compete and have fun! 🚀</p>
                    <p>
                        <a href="{contest_url}" class="button">Join Contest Now</a>
                    </p>
                    <p>Good luck! 🍀</p>
                    <p>— The CodeJarvis Team</p>
                </div>
            </div>
        </body>
        </html>
        """.format(
            contest_name=contest_name,
            contest_date=contest_date,
            contest_url=contest_url,
            time_lower=time_until.lower()
        )
        
        return self.send_email(user_email, subject, html_content)

# Global instance
email_service = SimpleEmailService()
