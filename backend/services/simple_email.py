"""
Simple Email Service for Contest Reminders
Uses SMTP to send reminder emails from kumarshivanshsinha@gmail.com
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional

class SimpleEmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "kumarshivanshsinha@gmail.com"
        self.sender_password = os.getenv("EMAIL_PASSWORD") or os.getenv("SMTP_PASSWORD")  # App password for Gmail
        
    def send_reminder_email(self, recipient_email: str, contest_name: str, contest_url: str, contest_time: datetime, reminder_type: str = "reminder") -> bool:
        """
        Send a contest reminder email
        
        Args:
            recipient_email: Email address to send to
            contest_name: Name of the contest
            contest_url: URL of the contest
            contest_time: Start time of the contest
            reminder_type: Type of reminder ('confirmation', 'reminder', 'final_reminder')
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            if not self.sender_password:
                print("⚠️ EMAIL_PASSWORD or SMTP_PASSWORD not configured in environment variables")
                print(f"🔍 Available env vars: EMAIL_PASSWORD={os.getenv('EMAIL_PASSWORD')}, SMTP_PASSWORD={os.getenv('SMTP_PASSWORD')}")
                print(f"🔍 Current working directory: {os.getcwd()}")
                print(f"🔍 Environment file exists: {os.path.exists('.env')}")
                return False
                
            print(f"📧 Attempting to send {reminder_type} email to {recipient_email} for contest: {contest_name}")
                
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            
            if reminder_type == "confirmation":
                msg['Subject'] = f"✅ Reminder Set: {contest_name}"
                html_content = self._create_confirmation_email(contest_name, contest_url, contest_time)
            elif reminder_type == "final_reminder":
                msg['Subject'] = f"🚨 STARTING SOON: {contest_name}"
                html_content = self._create_final_reminder_email(contest_name, contest_url, contest_time)
            else:
                msg['Subject'] = f"⏰ Reminder: {contest_name}"
                html_content = self._create_reminder_email(contest_name, contest_url, contest_time)
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            print(f"📡 Connecting to SMTP server {self.smtp_server}:{self.smtp_port}")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                print(f"🔐 Logging in with email: {self.sender_email}")
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
                
            print(f"✅ {reminder_type.title()} email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send {reminder_type} email to {recipient_email}: {str(e)}")
            print(f"   Error details: {type(e).__name__}")
            return False
    
    def _create_confirmation_email(self, contest_name: str, contest_url: str, contest_time: datetime) -> str:
        """Create HTML content for confirmation email"""
        time_until = self._time_until(contest_time)
        formatted_time = contest_time.strftime('%A, %B %d, %Y at %I:%M %p UTC')
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Reminder Confirmation</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 30px;">
                <h1 style="margin: 0; font-size: 28px;">📅 Reminder Set!</h1>
                <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.9;">We'll remind you about this contest</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; border-left: 4px solid #667eea; margin-bottom: 25px;">
                <h2 style="color: #667eea; margin-top: 0;">{contest_name}</h2>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border: 1px solid #e9ecef;">
                    <h3 style="color: #495057; margin-top: 0; margin-bottom: 15px; font-size: 16px;">📋 Contest Details</h3>
                    <div style="margin-bottom: 12px;">
                        <strong style="color: #495057;">📅 Date & Time:</strong>
                        <div style="color: #6c757d; margin-top: 4px; font-size: 14px;">{formatted_time}</div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <strong style="color: #495057;">⏱️ Time Until Contest:</strong>
                        <div style="color: #28a745; font-weight: bold; margin-top: 4px; font-size: 16px;">{time_until}</div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <strong style="color: #495057;">🔗 Contest Link:</strong>
                        <div style="margin-top: 4px;">
                            <a href="{contest_url}" style="color: #007bff; text-decoration: none; word-break: break-all;">{contest_url}</a>
                        </div>
                    </div>
                </div>
                
                <div style="text-align: center; margin: 25px 0;">
                    <a href="{contest_url}" style="background: #667eea; color: white; text-decoration: none; padding: 12px 30px; border-radius: 25px; font-weight: bold; display: inline-block; margin-right: 10px;">
                        🚀 Go to Contest
                    </a>
                    <a href="{contest_url}" style="background: #28a745; color: white; text-decoration: none; padding: 12px 30px; border-radius: 25px; font-weight: bold; display: inline-block;">
                        ✅ Register Now
                    </a>
                </div>
                
                <div style="background: #fff3cd; padding: 15px; border-radius: 8px; border: 1px solid #ffeaa7; margin: 20px 0;">
                    <h4 style="color: #856404; margin: 0 0 10px 0; font-size: 14px;">📝 Important Reminder:</h4>
                    <p style="color: #856404; margin: 0; font-size: 13px;">Make sure to <strong>register for the contest</strong> if you haven't already! Most platforms require registration before the contest starts.</p>
                </div>
            </div>
            
            <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
                <h3 style="color: #28a745; margin-top: 0;">📧 What happens next?</h3>
                <ul style="margin: 0; padding-left: 20px; color: #155724;">
                    <li style="margin: 10px 0;">You'll receive a reminder <strong>24 hours before</strong> the contest</li>
                    <li style="margin: 10px 0;">You'll receive a final reminder <strong>1 hour before</strong> the contest</li>
                    <li style="margin: 10px 0;">The reminder will appear on your CodeJarvis calendar</li>
                    <li style="margin: 10px 0;">Don't forget to register if you haven't already!</li>
                </ul>
            </div>
            
            <div style="background: #d1ecf1; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
                <h3 style="color: #0c5460; margin-top: 0;">💡 Contest Preparation Tips</h3>
                <ul style="margin: 0; padding-left: 20px; color: #0c5460;">
                    <li style="margin: 8px 0;">Review the contest format and rules</li>
                    <li style="margin: 8px 0;">Prepare your coding environment and templates</li>
                    <li style="margin: 8px 0;">Make sure you have a stable internet connection</li>
                    <li style="margin: 8px 0;">Get some practice problems done beforehand</li>
                    <li style="margin: 8px 0;"><strong>Register early</strong> to avoid last-minute issues</li>
                </ul>
            </div>
            
            <div style="text-align: center; color: #666; font-size: 14px; margin-top: 30px;">
                <p>Happy coding! 🎯</p>
                <p style="margin: 5px 0;">— The CodeJarvis Team</p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="font-size: 12px;">This email was sent from CodeJarvis contest reminder system.</p>
            </div>
        </body>
        </html>
        """
    
    def _create_reminder_email(self, contest_name: str, contest_url: str, contest_time: datetime) -> str:
        """Create HTML content for regular reminder email"""
        time_until = self._time_until(contest_time)
        formatted_time = contest_time.strftime('%A, %B %d, %Y at %I:%M %p UTC')
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Contest Reminder</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 30px;">
                <h1 style="margin: 0; font-size: 28px;">⏰ Contest Reminder</h1>
                <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.9;">Don't miss this contest!</p>
            </div>
            
            <div style="background: #fff3cd; padding: 25px; border-radius: 10px; border-left: 4px solid #f093fb; margin-bottom: 25px;">
                <h2 style="color: #f5576c; margin-top: 0;">{contest_name}</h2>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border: 1px solid #ffeaa7;">
                    <h3 style="color: #856404; margin-top: 0; margin-bottom: 15px; font-size: 16px;">📋 Contest Information</h3>
                    <div style="margin-bottom: 12px;">
                        <strong style="color: #856404;">📅 Date & Time:</strong>
                        <div style="color: #6c757d; margin-top: 4px; font-size: 14px;">{formatted_time}</div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <strong style="color: #856404;">⏱️ Time Remaining:</strong>
                        <div style="color: #d63384; font-weight: bold; margin-top: 4px; font-size: 18px;">🔥 {time_until}</div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <strong style="color: #856404;">🔗 Contest Link:</strong>
                        <div style="margin-top: 4px;">
                            <a href="{contest_url}" style="color: #f5576c; text-decoration: none; word-break: break-all; font-weight: bold;">{contest_url}</a>
                        </div>
                    </div>
                </div>
                
                <div style="text-align: center; margin: 25px 0;">
                    <a href="{contest_url}" style="background: #f5576c; color: white; text-decoration: none; padding: 15px 35px; border-radius: 25px; font-weight: bold; display: inline-block; font-size: 16px; box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3); margin-right: 10px;">
                        🏃‍♂️ Join Contest Now
                    </a>
                </div>
                
                <div style="background: #ffe6e6; padding: 15px; border-radius: 8px; border: 1px solid #ffcccb; margin: 20px 0;">
                    <h4 style="color: #dc3545; margin: 0 0 10px 0; font-size: 14px;">⚠️ Last Chance Reminder:</h4>
                    <p style="color: #dc3545; margin: 0; font-size: 13px;">If you haven't registered yet, <strong>register now</strong>! Many contests close registration before they start. Don't miss out on this opportunity!</p>
                </div>
            </div>
            
            <div style="background: #d1ecf1; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
                <h3 style="color: #0c5460; margin-top: 0;">💡 Last-Minute Contest Tips</h3>
                <ul style="margin: 0; padding-left: 20px; color: #0c5460;">
                    <li style="margin: 10px 0;">Double-check the contest format and rules</li>
                    <li style="margin: 10px 0;">Prepare your coding environment and templates</li>
                    <li style="margin: 10px 0;">Make sure you have a stable internet connection</li>
                    <li style="margin: 10px 0;">Review common algorithms and data structures</li>
                    <li style="margin: 10px 0;"><strong>Complete your registration</strong> if not done already!</li>
                    <li style="margin: 10px 0;">Get some rest before the contest - fresh mind = better performance!</li>
                </ul>
            </div>
            
            <div style="text-align: center; color: #666; font-size: 14px; margin-top: 30px;">
                <p>Best of luck! 🍀</p>
                <p style="margin: 5px 0;">— The CodeJarvis Team</p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="font-size: 12px;">This email was sent from CodeJarvis contest reminder system.</p>
            </div>
        </body>
        </html>
        """
    
    def _create_final_reminder_email(self, contest_name: str, contest_url: str, contest_time: datetime) -> str:
        """Create HTML content for final reminder email (1 hour before)"""
        time_until = self._time_until(contest_time)
        formatted_time = contest_time.strftime('%A, %B %d, %Y at %I:%M %p UTC')
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Final Contest Reminder</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 30px; box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);">
                <h1 style="margin: 0; font-size: 32px; animation: pulse 2s infinite;">🚨 STARTING SOON!</h1>
                <p style="margin: 10px 0 0 0; font-size: 20px; opacity: 0.9;">Final call for the contest!</p>
            </div>
            
            <div style="background: #ffe6e6; padding: 25px; border-radius: 10px; border-left: 4px solid #ff6b6b; margin-bottom: 25px; border: 2px solid #ffcccc;">
                <h2 style="color: #ee5a24; margin-top: 0; font-size: 22px;">{contest_name}</h2>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border: 2px solid #ff6b6b; box-shadow: 0 4px 15px rgba(255, 107, 107, 0.2);">
                    <h3 style="color: #dc3545; margin-top: 0; margin-bottom: 15px; font-size: 18px;">🚨 URGENT - Contest Details</h3>
                    <div style="margin-bottom: 15px;">
                        <strong style="color: #dc3545;">📅 Starting:</strong>
                        <div style="color: #6c757d; margin-top: 4px; font-size: 15px;">{formatted_time}</div>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <strong style="color: #dc3545;">🔥 Time Remaining:</strong>
                        <div style="color: #dc3545; font-weight: bold; margin-top: 4px; font-size: 24px; background: #fff5f5; padding: 10px; border-radius: 8px; text-align: center; border: 2px dashed #dc3545;">
                            ⏰ {time_until}
                        </div>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <strong style="color: #dc3545;">🔗 Contest Link:</strong>
                        <div style="margin-top: 4px;">
                            <a href="{contest_url}" style="color: #dc3545; text-decoration: none; word-break: break-all; font-weight: bold; background: #fff5f5; padding: 8px; border-radius: 4px; display: inline-block;">{contest_url}</a>
                        </div>
                    </div>
                </div>
                
                <div style="text-align: center; margin: 25px 0;">
                    <a href="{contest_url}" style="background: #dc3545; color: white; text-decoration: none; padding: 20px 50px; border-radius: 30px; font-weight: bold; display: inline-block; font-size: 20px; box-shadow: 0 6px 20px rgba(220, 53, 69, 0.4); margin-bottom: 15px; animation: bounce 1s infinite;">
                        🎯 JOIN NOW!
                    </a>
                    <div style="margin-top: 15px;">
                        <a href="{contest_url}" style="background: #fd7e14; color: white; text-decoration: none; padding: 12px 25px; border-radius: 20px; font-weight: bold; display: inline-block; font-size: 14px;">
                            ⚡ Quick Registration Check
                        </a>
                    </div>
                </div>
                
                <div style="background: #fff2cc; padding: 20px; border-radius: 8px; border: 2px solid #ffc107; margin: 20px 0;">
                    <h4 style="color: #856404; margin: 0 0 15px 0; font-size: 16px;">🚨 CRITICAL: Registration Status</h4>
                    <div style="color: #856404; font-size: 14px; line-height: 1.6;">
                        <p style="margin: 0 0 10px 0;"><strong>If you haven't registered yet:</strong></p>
                        <ul style="margin: 0; padding-left: 20px;">
                            <li>Click the registration link immediately</li>
                            <li>Many contests close registration just before start</li>
                            <li>Don't wait until the last minute!</li>
                        </ul>
                        <p style="margin: 15px 0 0 0; font-weight: bold;">Time is running out - register NOW!</p>
                    </div>
                </div>
            </div>
            
            <div style="background: #fff2cc; padding: 20px; border-radius: 10px; margin-bottom: 25px; border: 1px solid #ffc107;">
                <h3 style="color: #d39e00; margin-top: 0;">⚡ Last Minute Checklist</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div style="background: white; padding: 15px; border-radius: 8px; text-align: center; border: 2px solid #28a745;">
                        <div style="font-size: 24px; margin-bottom: 5px;">✅</div>
                        <p style="margin: 0; font-weight: bold; color: #28a745; font-size: 12px;">Contest Registration</p>
                    </div>
                    <div style="background: white; padding: 15px; border-radius: 8px; text-align: center; border: 2px solid #28a745;">
                        <div style="font-size: 24px; margin-bottom: 5px;">💻</div>
                        <p style="margin: 0; font-weight: bold; color: #28a745; font-size: 12px;">Code Editor Ready</p>
                    </div>
                    <div style="background: white; padding: 15px; border-radius: 8px; text-align: center; border: 2px solid #28a745;">
                        <div style="font-size: 24px; margin-bottom: 5px;">📋</div>
                        <p style="margin: 0; font-weight: bold; color: #28a745; font-size: 12px;">Templates Prepared</p>
                    </div>
                    <div style="background: white; padding: 15px; border-radius: 8px; text-align: center; border: 2px solid #28a745;">
                        <div style="font-size: 24px; margin-bottom: 5px;">🌐</div>
                        <p style="margin: 0; font-weight: bold; color: #28a745; font-size: 12px;">Internet Connection</p>
                    </div>
                </div>
            </div>
            
            <div style="text-align: center; color: #666; font-size: 14px; margin-top: 30px;">
                <p style="font-size: 20px; color: #ee5a24; font-weight: bold;">Go crush it! 💪</p>
                <p style="margin: 5px 0;">— The CodeJarvis Team</p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="font-size: 12px;">This email was sent from CodeJarvis contest reminder system.</p>
            </div>
        </body>
        </html>
        """
    
    def _time_until(self, contest_time: datetime) -> str:
        """Calculate and format time until contest with detailed countdown"""
        try:
            now = datetime.utcnow()
            if contest_time <= now:
                return "Contest has started! 🚀"
            
            time_diff = contest_time - now
            total_seconds = int(time_diff.total_seconds())
            
            days = time_diff.days
            hours, remainder = divmod(time_diff.seconds, 3600)
            minutes = remainder // 60
            seconds = remainder % 60
            
            # Format based on time remaining
            if days > 7:
                return f"{days} days, {hours} hours ({days // 7} week{'s' if days // 7 > 1 else ''})"
            elif days > 0:
                if hours > 0:
                    return f"{days} day{'s' if days > 1 else ''}, {hours} hour{'s' if hours > 1 else ''}, {minutes} minute{'s' if minutes > 1 else ''}"
                else:
                    return f"{days} day{'s' if days > 1 else ''}, {minutes} minute{'s' if minutes > 1 else ''}"
            elif hours > 0:
                if hours > 1:
                    return f"{hours} hour{'s' if hours > 1 else ''}, {minutes} minute{'s' if minutes > 1 else ''}"
                else:
                    return f"{hours} hour, {minutes} minute{'s' if minutes > 1 else ''}"
            elif minutes > 0:
                if minutes > 10:
                    return f"{minutes} minutes"
                else:
                    return f"{minutes} minute{'s' if minutes > 1 else ''}, {seconds} second{'s' if seconds > 1 else ''}"
            else:
                return f"{seconds} second{'s' if seconds > 1 else ''} (Almost starting!)"
                
        except Exception as e:
            print(f"Error calculating time until contest: {e}")
            return "Soon"
    
    def test_connection(self) -> bool:
        """Test email service connection"""
        try:
            if not self.sender_password:
                print("⚠️ EMAIL_PASSWORD or SMTP_PASSWORD not configured")
                print(f"🔍 Available env vars: EMAIL_PASSWORD={os.getenv('EMAIL_PASSWORD')}, SMTP_PASSWORD={os.getenv('SMTP_PASSWORD')}")
                return False
                
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                print("✅ Email service connection successful")
                return True
                
        except Exception as e:
            print(f"❌ Email service connection failed: {str(e)}")
            return False

# Global instance
simple_email_service = SimpleEmailService()