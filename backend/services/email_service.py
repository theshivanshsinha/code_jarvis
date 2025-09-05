import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import threading
import time
from jinja2 import Template
from typing import Dict, List, Optional

class EmailService:
    def __init__(self):
        # Email configuration - should be set via environment variables
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.sender_email = os.getenv('SENDER_EMAIL', self.smtp_username)
        self.sender_name = os.getenv('SENDER_NAME', 'CodeJarvis')
        
        # Email templates
        self.templates = {
            'reminder_created': self._get_reminder_created_template(),
            'contest_reminder': self._get_contest_reminder_template(),
            'daily_reminder': self._get_daily_reminder_template(),
            'weekly_summary': self._get_weekly_summary_template()
        }
    
    def send_email(self, to_email: str, subject: str, html_content: str, text_content: str = None) -> bool:
        """Send an email using SMTP"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = to_email
            
            # Add text and HTML parts
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Connect to server and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_reminder_created_email(self, user_email: str, user_name: str, contest_name: str, contest_date: datetime, contest_url: str) -> bool:
        """Send initial confirmation email when reminder is created"""
        template = Template(self.templates['reminder_created'])
        
        context = {
            'user_name': user_name,
            'contest_name': contest_name,
            'contest_date': contest_date.strftime('%B %d, %Y at %I:%M %p'),
            'contest_url': contest_url,
            'current_year': datetime.now().year
        }
        
        html_content = template.render(context)
        subject = f"✅ Reminder Set: {contest_name}"
        
        return self.send_email(user_email, subject, html_content)
    
    def send_contest_reminder_email(self, user_email: str, user_name: str, contest_name: str, contest_date: datetime, contest_url: str, time_until: str) -> bool:
        """Send contest reminder email"""
        template = Template(self.templates['contest_reminder'])
        
        context = {
            'user_name': user_name,
            'contest_name': contest_name,
            'contest_date': contest_date.strftime('%B %d, %Y at %I:%M %p'),
            'contest_url': contest_url,
            'time_until': time_until,
            'current_year': datetime.now().year
        }
        
        html_content = template.render(context)
        subject = f"⏰ Contest Reminder: {contest_name} starts {time_until}!"
        
        return self.send_email(user_email, subject, html_content)
    
    def send_daily_coding_reminder(self, user_email: str, user_name: str, stats: Dict) -> bool:
        """Send daily coding motivation email"""
        template = Template(self.templates['daily_reminder'])
        
        context = {
            'user_name': user_name,
            'total_solved': stats.get('total_solved', 0),
            'current_streak': stats.get('current_streak', 0),
            'platforms': stats.get('platforms', []),
            'current_year': datetime.now().year
        }
        
        html_content = template.render(context)
        subject = f"🚀 Daily Coding Challenge - Keep Going, {user_name}!"
        
        return self.send_email(user_email, subject, html_content)
    
    def send_weekly_summary(self, user_email: str, user_name: str, summary: Dict) -> bool:
        """Send weekly coding summary email"""
        template = Template(self.templates['weekly_summary'])
        
        context = {
            'user_name': user_name,
            'problems_solved': summary.get('problems_solved', 0),
            'contests_participated': summary.get('contests_participated', 0),
            'new_achievements': summary.get('new_achievements', []),
            'top_platforms': summary.get('top_platforms', []),
            'current_year': datetime.now().year
        }
        
        html_content = template.render(context)
        subject = f"📊 Your Weekly Coding Summary - {user_name}"
        
        return self.send_email(user_email, subject, html_content)
    
    def _get_reminder_created_template(self) -> str:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reminder Created - CodeJarvis</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f7fafc; }
                .container { max-width: 600px; margin: 0 auto; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
                .content { padding: 30px; }
                .contest-card { background-color: #f7fafc; border-left: 4px solid #667eea; padding: 20px; margin: 20px 0; border-radius: 4px; }
                .button { display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; padding: 12px 30px; border-radius: 6px; font-weight: 600; margin: 20px 0; }
                .footer { background-color: #2d3748; color: #a0aec0; text-align: center; padding: 20px; font-size: 12px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚡ CodeJarvis</h1>
                    <h2>Reminder Created Successfully!</h2>
                </div>
                <div class="content">
                    <p>Hi {{ user_name }},</p>
                    
                    <p>Great news! We've successfully created a reminder for your upcoming contest.</p>
                    
                    <div class="contest-card">
                        <h3>📅 {{ contest_name }}</h3>
                        <p><strong>Date & Time:</strong> {{ contest_date }}</p>
                        <p>We'll send you reminder emails leading up to this contest to make sure you don't miss it!</p>
                    </div>
                    
                    <p>Here's what happens next:</p>
                    <ul>
                        <li>📧 You'll get reminders 1 day before the contest</li>
                        <li>⏰ Another reminder 1 hour before it starts</li>
                        <li>📱 The event has been added to your Google Calendar (if connected)</li>
                    </ul>
                    
                    <div style="text-align: center;">
                        <a href="{{ contest_url }}" class="button">View Contest Details</a>
                    </div>
                    
                    <p>Happy coding! 🚀</p>
                    <p>The CodeJarvis Team</p>
                </div>
                <div class="footer">
                    <p>© {{ current_year }} CodeJarvis. Empowering developers worldwide.</p>
                    <p>You're receiving this because you set up a contest reminder.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_contest_reminder_template(self) -> str:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Contest Reminder - CodeJarvis</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f7fafc; }
                .container { max-width: 600px; margin: 0 auto; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
                .header { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; text-align: center; }
                .content { padding: 30px; }
                .urgent-banner { background: linear-gradient(90deg, #ff6b6b, #feca57); color: white; padding: 15px; text-align: center; font-weight: 600; margin: -30px -30px 20px -30px; }
                .contest-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; margin: 20px 0; border-radius: 8px; }
                .button { display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; padding: 15px 40px; border-radius: 6px; font-weight: 600; margin: 20px 0; font-size: 16px; }
                .tips { background-color: #f7fafc; padding: 20px; border-radius: 6px; margin: 20px 0; }
                .footer { background-color: #2d3748; color: #a0aec0; text-align: center; padding: 20px; font-size: 12px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚡ CodeJarvis</h1>
                    <h2>Contest Starting Soon!</h2>
                </div>
                <div class="content">
                    <div class="urgent-banner">
                        🚨 {{ time_until }} remaining!
                    </div>
                    
                    <p>Hi {{ user_name }},</p>
                    
                    <p>This is your reminder that the contest you're interested in starts very soon!</p>
                    
                    <div class="contest-card">
                        <h3>🏆 {{ contest_name }}</h3>
                        <p><strong>Starts:</strong> {{ contest_date }}</p>
                        <p><strong>Time Remaining:</strong> {{ time_until }}</p>
                    </div>
                    
                    <div class="tips">
                        <h4>🎯 Last-Minute Preparation Tips:</h4>
                        <ul>
                            <li>✅ Make sure you're registered for the contest</li>
                            <li>🍕 Get some snacks and water ready</li>
                            <li>💻 Test your coding environment and internet</li>
                            <li>📚 Review common algorithms if needed</li>
                            <li>🧘 Take a deep breath and stay calm</li>
                        </ul>
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="{{ contest_url }}" class="button">🚀 Join Contest Now</a>
                    </div>
                    
                    <p>Good luck and may the code be with you! 🚀</p>
                    <p>The CodeJarvis Team</p>
                </div>
                <div class="footer">
                    <p>© {{ current_year }} CodeJarvis. Helping you never miss a contest.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_daily_reminder_template(self) -> str:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Daily Coding Reminder - CodeJarvis</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f7fafc; }
                .container { max-width: 600px; margin: 0 auto; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
                .header { background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); color: #2d3748; padding: 30px; text-align: center; }
                .content { padding: 30px; }
                .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 20px 0; }
                .stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 8px; }
                .motivation { background-color: #ebf8ff; border-left: 4px solid #3182ce; padding: 20px; margin: 20px 0; border-radius: 4px; }
                .footer { background-color: #2d3748; color: #a0aec0; text-align: center; padding: 20px; font-size: 12px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚡ CodeJarvis</h1>
                    <h2>Time to Code! 🚀</h2>
                </div>
                <div class="content">
                    <p>Hi {{ user_name }},</p>
                    
                    <p>Ready for another productive day of coding? Let's keep that momentum going!</p>
                    
                    <div class="stats-grid">
                        <div class="stat-card">
                            <h3>{{ total_solved }}</h3>
                            <p>Problems Solved</p>
                        </div>
                        <div class="stat-card">
                            <h3>{{ current_streak }}</h3>
                            <p>Day Streak</p>
                        </div>
                    </div>
                    
                    <div class="motivation">
                        <h4>💪 Today's Motivation</h4>
                        <p>"The only way to do great work is to love what you do." - Steve Jobs</p>
                        <p>Every problem you solve makes you a better programmer. Keep pushing forward!</p>
                    </div>
                    
                    <h4>🎯 Suggested Actions:</h4>
                    <ul>
                        <li>Solve at least 1 problem today to maintain your streak</li>
                        <li>Try a problem from a topic you're learning</li>
                        <li>Review a previous solution and optimize it</li>
                        <li>Participate in a daily challenge if available</li>
                    </ul>
                    
                    <p>Happy coding! 🚀</p>
                    <p>The CodeJarvis Team</p>
                </div>
                <div class="footer">
                    <p>© {{ current_year }} CodeJarvis. Your daily coding companion.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_weekly_summary_template(self) -> str:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Weekly Summary - CodeJarvis</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f7fafc; }
                .container { max-width: 600px; margin: 0 auto; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
                .header { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: #2d3748; padding: 30px; text-align: center; }
                .content { padding: 30px; }
                .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
                .summary-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 8px; }
                .achievement-card { background-color: #f0fff4; border: 1px solid #9ae6b4; padding: 15px; margin: 10px 0; border-radius: 6px; }
                .footer { background-color: #2d3748; color: #a0aec0; text-align: center; padding: 20px; font-size: 12px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚡ CodeJarvis</h1>
                    <h2>Your Weekly Coding Summary 📊</h2>
                </div>
                <div class="content">
                    <p>Hi {{ user_name }},</p>
                    
                    <p>Here's what you accomplished this week:</p>
                    
                    <div class="summary-grid">
                        <div class="summary-card">
                            <h3>{{ problems_solved }}</h3>
                            <p>Problems Solved</p>
                        </div>
                        <div class="summary-card">
                            <h3>{{ contests_participated }}</h3>
                            <p>Contests Joined</p>
                        </div>
                    </div>
                    
                    {% if new_achievements %}
                    <h4>🏆 New Achievements This Week:</h4>
                    {% for achievement in new_achievements %}
                    <div class="achievement-card">
                        <strong>{{ achievement.title }}</strong>
                        <p>{{ achievement.description }}</p>
                    </div>
                    {% endfor %}
                    {% endif %}
                    
                    <h4>📈 Keep up the great work!</h4>
                    <p>Every line of code you write is progress. Keep challenging yourself and growing!</p>
                    
                    <p>See you next week! 🚀</p>
                    <p>The CodeJarvis Team</p>
                </div>
                <div class="footer">
                    <p>© {{ current_year }} CodeJarvis. Tracking your coding journey.</p>
                </div>
            </div>
        </body>
        </html>
        """

# Global email service instance
email_service = EmailService()
