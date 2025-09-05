from jinja2 import Template
from datetime import datetime
from typing import Dict

class EmailTemplates:
    """Clean, modern email templates for CodeJarvis"""
    
    def __init__(self):
        self.base_styles = """
        <style>
            * { box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; 
                line-height: 1.6; 
                color: #333; 
                margin: 0; 
                padding: 0; 
                background-color: #f8fafc; 
            }
            .container { 
                max-width: 600px; 
                margin: 20px auto; 
                background: white; 
                border-radius: 12px; 
                overflow: hidden; 
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); 
            }
            .header { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 32px 24px; 
                text-align: center; 
            }
            .header h1 { margin: 0 0 8px 0; font-size: 24px; font-weight: 600; }
            .header p { margin: 0; opacity: 0.9; font-size: 16px; }
            .content { padding: 32px 24px; }
            .contest-card { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 24px; 
                border-radius: 8px; 
                margin: 24px 0; 
            }
            .stats-grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
                gap: 16px; 
                margin: 24px 0; 
            }
            .stat-card { 
                background: #f8fafc; 
                border: 1px solid #e2e8f0; 
                padding: 20px; 
                border-radius: 8px; 
                text-align: center; 
            }
            .stat-card h3 { margin: 0 0 8px 0; font-size: 32px; color: #667eea; }
            .stat-card p { margin: 0; color: #64748b; font-size: 14px; }
            .button { 
                display: inline-block; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                text-decoration: none; 
                padding: 14px 28px; 
                border-radius: 8px; 
                font-weight: 600; 
                margin: 16px 0; 
            }
            .footer { 
                background: #1a202c; 
                color: #a0aec0; 
                text-align: center; 
                padding: 24px; 
                font-size: 14px; 
            }
            .footer p { margin: 8px 0; }
            .urgent { 
                background: linear-gradient(90deg, #ff6b6b, #feca57); 
                color: white; 
                padding: 16px; 
                text-align: center; 
                font-weight: 600; 
                margin: -32px -24px 24px -24px; 
                border-radius: 0; 
            }
        </style>
        """
    
    def render_contest_reminder(self, context: Dict) -> str:
        """Render contest reminder email"""
        template = Template(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Contest Reminder - CodeJarvis</title>
            {self.base_styles}
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚡ CodeJarvis</h1>
                    <p>Contest Starting Soon!</p>
                </div>
                <div class="content">
                    <div class="urgent">
                        🚨 {{{{ time_until }}}} remaining!
                    </div>
                    
                    <p>Hi {{{{ user_name }}}},</p>
                    
                    <p>Your contest is starting soon! Time to show off your coding skills! 🚀</p>
                    
                    <div class="contest-card">
                        <h3>🏆 {{{{ contest_name }}}}</h3>
                        <p><strong>Starts:</strong> {{{{ contest_date }}}}</p>
                        <p><strong>Time Remaining:</strong> {{{{ time_until }}}}</p>
                    </div>
                    
                    <h4>🎯 Quick Checklist:</h4>
                    <ul>
                        <li>✅ Registered for the contest</li>
                        <li>💻 IDE/editor ready</li>
                        <li>🌐 Internet connection stable</li>
                        <li>☕ Snacks and water nearby</li>
                    </ul>
                    
                    <div style="text-align: center; margin: 32px 0;">
                        <a href="{{{{ contest_url }}}}" class="button">🚀 Join Contest</a>
                    </div>
                    
                    <p><strong>Good luck! You've got this! 💪</strong></p>
                </div>
                <div class="footer">
                    <p>© {{{{ current_year|default('2025') }}}} CodeJarvis - Your AI coding companion</p>
                    <p>Helping developers never miss a contest 🎯</p>
                </div>
            </div>
        </body>
        </html>
        """)
        
        return template.render(context)
    
    def render_reminder_confirmation(self, context: Dict) -> str:
        """Render reminder confirmation email"""
        template = Template(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reminder Set - CodeJarvis</title>
            {self.base_styles}
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚡ CodeJarvis</h1>
                    <p>Reminder Successfully Created!</p>
                </div>
                <div class="content">
                    <p>Hi {{{{ user_name }}}},</p>
                    
                    <p>Perfect! We've set up your contest reminder. You'll never miss an important contest again! 🎯</p>
                    
                    <div class="contest-card">
                        <h3>📅 {{{{ contest_name }}}}</h3>
                        <p><strong>Date:</strong> {{{{ contest_date }}}}</p>
                        <p>We'll send you reminders leading up to this contest!</p>
                    </div>
                    
                    <h4>📬 What to expect:</h4>
                    <ul>
                        <li>📧 Email reminder 1 day before</li>
                        <li>⏰ Final reminder 1 hour before</li>
                        <li>📱 Calendar event (if connected)</li>
                    </ul>
                    
                    <div style="text-align: center; margin: 32px 0;">
                        <a href="{{{{ contest_url }}}}" class="button">View Contest Details</a>
                    </div>
                    
                    <p>Happy coding! 🚀</p>
                </div>
                <div class="footer">
                    <p>© {{{{ current_year|default('2025') }}}} CodeJarvis - Your AI coding companion</p>
                    <p>You're receiving this because you set up a contest reminder</p>
                </div>
            </div>
        </body>
        </html>
        """)
        
        return template.render(context)
    
    def render_daily_motivation(self, context: Dict) -> str:
        """Render daily motivation email"""
        template = Template(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Daily Coding Time - CodeJarvis</title>
            {self.base_styles}
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚡ CodeJarvis</h1>
                    <p>Time to Code! 🚀</p>
                </div>
                <div class="content">
                    <p>Hi {{{{ user_name }}}},</p>
                    
                    <p>Ready for another productive day? Let's keep that coding momentum going! 💪</p>
                    
                    <div class="stats-grid">
                        <div class="stat-card">
                            <h3>{{{{ total_solved }}}}</h3>
                            <p>Problems Solved</p>
                        </div>
                        <div class="stat-card">
                            <h3>{{{{ current_streak }}}}</h3>
                            <p>Day Streak 🔥</p>
                        </div>
                    </div>
                    
                    <div style="background: #f0f9ff; border-left: 4px solid #3b82f6; padding: 20px; margin: 24px 0; border-radius: 4px;">
                        <h4 style="margin: 0 0 12px 0;">💡 Today's Coding Tip</h4>
                        <p style="margin: 0;">"The best way to learn programming is by writing programs." - Start with one problem today!</p>
                    </div>
                    
                    <h4>🎯 Suggested actions:</h4>
                    <ul>
                        <li>Solve 1-2 problems on {{{{ favorite_platform }}}}</li>
                        <li>Review a solution from yesterday</li>
                        <li>Learn one new algorithm concept</li>
                        <li>Practice for 30 minutes</li>
                    </ul>
                    
                    <div style="text-align: center; margin: 32px 0;">
                        <a href="#" class="button">🚀 Start Coding</a>
                    </div>
                    
                    <p>Every problem solved is progress! Keep it up! 🌟</p>
                </div>
                <div class="footer">
                    <p>© {{{{ current_year|default('2025') }}}} CodeJarvis - Your daily coding companion</p>
                </div>
            </div>
        </body>
        </html>
        """)
        
        return template.render(context)
    
    def render_weekly_summary(self, context: Dict) -> str:
        """Render weekly summary email"""
        template = Template(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Weekly Summary - CodeJarvis</title>
            {self.base_styles}
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚡ CodeJarvis</h1>
                    <p>Your Weekly Coding Summary 📊</p>
                </div>
                <div class="content">
                    <p>Hi {{{{ user_name }}}},</p>
                    
                    <p>Here's your awesome coding week recap! 🎉</p>
                    
                    <div class="stats-grid">
                        <div class="stat-card">
                            <h3>{{{{ problems_solved }}}}</h3>
                            <p>Problems Solved</p>
                        </div>
                        <div class="stat-card">
                            <h3>{{{{ contests_participated }}}}</h3>
                            <p>Contests Joined</p>
                        </div>
                    </div>
                    
                    {{% if achievements %}}
                    <h4>🏆 This Week's Achievements:</h4>
                    {{% for achievement in achievements %}}
                    <div style="background: #f0fdf4; border: 1px solid #22c55e; padding: 16px; margin: 12px 0; border-radius: 8px;">
                        <strong>🎯 {{{{ achievement.title }}}}</strong>
                        <p style="margin: 4px 0 0 0; color: #059669;">{{{{ achievement.description }}}}</p>
                    </div>
                    {{% endfor %}}
                    {{% endif %}}
                    
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 24px; border-radius: 8px; margin: 24px 0; text-align: center;">
                        <h3 style="margin: 0 0 12px 0;">🚀 Keep the momentum!</h3>
                        <p style="margin: 0;">You're doing amazing! Every solved problem makes you a better developer.</p>
                    </div>
                    
                    <p><strong>Ready for another productive week? Let's code! 💻</strong></p>
                </div>
                <div class="footer">
                    <p>© {{{{ current_year|default('2025') }}}} CodeJarvis - Tracking your coding journey</p>
                </div>
            </div>
        </body>
        </html>
        """)
        
        return template.render(context)
