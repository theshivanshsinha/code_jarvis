import os
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from .simple_email_service import email_service
from .improved_calendar_service import google_calendar_service, calendar_fallback_service

class ReminderService:
    def __init__(self):
        # In-memory storage for reminders (replace with database in production)
        self.reminders_file = os.path.join('data', 'reminders.json')
        self.reminders = self._load_reminders()
        
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
    
    def _load_reminders(self) -> Dict[str, dict]:
        """Load reminders from JSON file"""
        if not os.path.exists(self.reminders_file):
            return {}
        
        try:
            with open(self.reminders_file, 'r') as f:
                reminders_data = json.load(f)
                
                # Convert string dates back to datetime objects
                for reminder_id, reminder in reminders_data.items():
                    if 'contest_time' in reminder:
                        reminder['contest_time'] = datetime.fromisoformat(reminder['contest_time'])
                    if 'created_at' in reminder:
                        reminder['created_at'] = datetime.fromisoformat(reminder['created_at'])
                    if 'last_reminder_sent' in reminder:
                        reminder['last_reminder_sent'] = datetime.fromisoformat(reminder['last_reminder_sent'])
                
                return reminders_data
        except Exception as e:
            print(f"Error loading reminders: {e}")
            return {}
    
    def _save_reminders(self):
        """Save reminders to JSON file"""
        try:
            # Convert datetime objects to ISO format for JSON serialization
            serializable_reminders = {}
            for reminder_id, reminder in self.reminders.items():
                serializable_reminders[reminder_id] = {
                    'user_email': reminder['user_email'],
                    'contest_name': reminder['contest_name'],
                    'contest_url': reminder['contest_url'],
                    'contest_time': reminder['contest_time'].isoformat(),
                    'created_at': reminder['created_at'].isoformat(),
                    'last_reminder_sent': reminder.get('last_reminder_sent', ''),
                    'google_calendar_event_id': reminder.get('google_calendar_event_id', ''),
                    'is_active': reminder.get('is_active', True)
                }
            
            with open(self.reminders_file, 'w') as f:
                json.dump(serializable_reminders, f, indent=2)
        except Exception as e:
            print(f"Error saving reminders: {e}")
    
    def create_reminder(
        self, 
        user_email: str, 
        contest_name: str, 
        contest_url: str, 
        contest_time: datetime,
        user_id: Optional[str] = None
    ) -> Optional[dict]:
        """Create a new contest reminder"""
        try:
            reminder_id = str(uuid.uuid4())
            now = datetime.utcnow()
            
            # Create Google Calendar event if user is authenticated
            google_calendar_event_id = None
            if user_id:
                calendar_data = {
                    'name': contest_name,
                    'start_time': contest_time.isoformat(),
                    'url': contest_url,
                    'platform': 'CodeForces' if 'codeforces' in contest_url.lower() else 'Other'
                }
                google_calendar_event_id = google_calendar_service.create_contest_event(user_id, calendar_data)
            
            reminder = {
                'id': reminder_id,
                'user_email': user_email,
                'contest_name': contest_name,
                'contest_url': contest_url,
                'contest_time': contest_time,
                'created_at': now,
                'last_reminder_sent': None,
                'google_calendar_event_id': google_calendar_event_id,
                'is_active': True
            }
            
            self.reminders[reminder_id] = reminder
            self._save_reminders()
            
            # Send confirmation email
            email_service.send_reminder_created_email(
                user_email=user_email,
                contest_name=contest_name,
                contest_date=contest_time.strftime("%B %d, %Y at %I:%M %p %Z"),
                contest_url=contest_url
            )
            
            return reminder
            
        except Exception as e:
            print(f"Error creating reminder: {e}")
            return None
    
    def remove_reminder(self, reminder_id: str, user_id: Optional[str] = None) -> bool:
        """Remove a contest reminder"""
        try:
            if reminder_id not in self.reminders:
                return False
            
            reminder = self.reminders[reminder_id]
            
            # Remove from Google Calendar if exists
            if user_id and reminder.get('google_calendar_event_id'):
                google_calendar_service.delete_contest_event(
                    user_id=user_id,
                    event_id=reminder['google_calendar_event_id']
                )
            
            # Mark as inactive instead of deleting to preserve history
            self.reminders[reminder_id]['is_active'] = False
            self._save_reminders()
            
            return True
            
        except Exception as e:
            print(f"Error removing reminder: {e}")
            return False
    
    def get_user_reminders(self, user_email: str) -> List[dict]:
        """Get all active reminders for a user"""
        return [
            reminder for reminder in self.reminders.values() 
            if reminder['user_email'] == user_email and reminder.get('is_active', True)
        ]
    
    def check_and_send_reminders(self):
        """Check for reminders that need to be sent and send them"""
        now = datetime.utcnow()
        
        for reminder_id, reminder in self.reminders.items():
            if not reminder.get('is_active', True):
                continue
                
            time_until_contest = reminder['contest_time'] - now
            
            # Skip if contest has already started
            if time_until_contest.total_seconds() <= 0:
                continue
            
            # Check if we need to send a reminder
            should_send = False
            time_until_str = ""
            
            # 24 hours before
            if time_until_contest <= timedelta(hours=24) and \
               (not reminder.get('last_reminder_sent') or 
                (now - reminder['last_reminder_sent']).total_seconds() > 3600):  # At least 1 hour since last reminder
                should_send = True
                time_until_str = "in 24 hours"
            
            # 1 hour before
            elif time_until_contest <= timedelta(hours=1) and \
                 (not reminder.get('last_reminder_sent') or 
                  (now - reminder['last_reminder_sent']).total_seconds() > 300):  # At least 5 minutes since last reminder
                should_send = True
                time_until_str = "in 1 hour"
            
            # 10 minutes before
            elif time_until_contest <= timedelta(minutes=10) and \
                 (not reminder.get('last_reminder_sent') or 
                  (now - reminder['last_reminder_sent']).total_seconds() > 60):  # At least 1 minute since last reminder
                should_send = True
                time_until_str = "in 10 minutes"
            
            if should_send and time_until_str:
                try:
                    # Send reminder email
                    email_service.send_contest_reminder(
                        user_email=reminder['user_email'],
                        contest_name=reminder['contest_name'],
                        contest_date=reminder['contest_time'].strftime("%B %d, %Y at %I:%M %p %Z"),
                        contest_url=reminder['contest_url'],
                        time_until=time_until_str
                    )
                    
                    # Update last reminder sent time
                    self.reminders[reminder_id]['last_reminder_sent'] = now
                    self._save_reminders()
                    
                except Exception as e:
                    print(f"Error sending reminder {reminder_id}: {e}")

# Global instance
reminder_service = ReminderService()
