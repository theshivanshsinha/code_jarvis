"""
Simple Reminder System
Stores reminders locally and manages email scheduling
"""

import json
import os
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from uuid import uuid4

class SimpleReminderManager:
    def __init__(self):
        self.reminders_file = "data/reminders.json"
        self.ensure_data_dir()
        self.active_timers = {}  # Store active reminder timers
        
    def ensure_data_dir(self):
        """Ensure data directory exists"""
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.reminders_file):
            with open(self.reminders_file, 'w') as f:
                json.dump({}, f)
    
    def load_reminders(self) -> Dict:
        """Load reminders from JSON file"""
        try:
            with open(self.reminders_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_reminders(self, reminders: Dict):
        """Save reminders to JSON file"""
        try:
            with open(self.reminders_file, 'w') as f:
                json.dump(reminders, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving reminders: {e}")
    
    def add_reminder(self, user_email: str, contest_name: str, contest_url: str, contest_time: datetime, platform: str = "Unknown") -> str:
        """
        Add a new reminder
        
        Returns:
            str: Reminder ID
        """
        reminder_id = str(uuid4())
        
        reminder_data = {
            "id": reminder_id,
            "user_email": user_email,
            "contest_name": contest_name,
            "contest_url": contest_url,
            "contest_time": contest_time.isoformat(),
            "platform": platform,
            "created_at": datetime.utcnow().isoformat(),
            "is_active": True,
            "email_sent_24h": False,
            "email_sent_1h": False
        }
        
        # Load existing reminders
        reminders = self.load_reminders()
        
        # Add new reminder
        reminders[reminder_id] = reminder_data
        
        # Save updated reminders
        self.save_reminders(reminders)
        
        # Schedule email reminders
        self.schedule_reminder_emails(reminder_id, reminder_data)
        
        return reminder_id
    
    def remove_reminder(self, reminder_id: str, user_email: str = None) -> bool:
        """
        Remove a reminder
        
        Args:
            reminder_id: ID of the reminder to remove
            user_email: Email of the user (for verification)
        
        Returns:
            bool: True if removed successfully
        """
        reminders = self.load_reminders()
        
        if reminder_id not in reminders:
            return False
        
        # Verify user owns this reminder (if email provided)
        if user_email and reminders[reminder_id].get("user_email") != user_email:
            return False
        
        # Cancel any scheduled timers
        self.cancel_reminder_timers(reminder_id)
        
        # Remove reminder
        del reminders[reminder_id]
        self.save_reminders(reminders)
        
        return True
    
    def get_user_reminders(self, user_email: str) -> List[Dict]:
        """Get all active reminders for a user"""
        reminders = self.load_reminders()
        user_reminders = []
        
        for reminder_id, reminder_data in reminders.items():
            if reminder_data.get("user_email") == user_email and reminder_data.get("is_active", True):
                user_reminders.append(reminder_data)
        
        # Sort by contest time
        user_reminders.sort(key=lambda x: x.get("contest_time", ""))
        return user_reminders
    
    def get_all_active_reminders(self) -> List[Dict]:
        """Get all active reminders (for calendar display)"""
        reminders = self.load_reminders()
        active_reminders = []
        
        for reminder_id, reminder_data in reminders.items():
            if reminder_data.get("is_active", True):
                active_reminders.append(reminder_data)
        
        # Sort by contest time
        active_reminders.sort(key=lambda x: x.get("contest_time", ""))
        return active_reminders
    
    def is_reminder_active(self, user_email: str, contest_name: str, contest_url: str) -> bool:
        """Check if a reminder already exists for this contest and user"""
        reminders = self.load_reminders()
        
        for reminder_data in reminders.values():
            if (reminder_data.get("user_email") == user_email and 
                reminder_data.get("contest_name") == contest_name and
                reminder_data.get("contest_url") == contest_url and
                reminder_data.get("is_active", True)):
                return True
        
        return False
    
    def find_reminder_id(self, user_email: str, contest_name: str, contest_url: str) -> Optional[str]:
        """Find reminder ID for a specific contest and user"""
        reminders = self.load_reminders()
        
        for reminder_id, reminder_data in reminders.items():
            if (reminder_data.get("user_email") == user_email and 
                reminder_data.get("contest_name") == contest_name and
                reminder_data.get("contest_url") == contest_url and
                reminder_data.get("is_active", True)):
                return reminder_id
        
        return None
    
    def schedule_reminder_emails(self, reminder_id: str, reminder_data: Dict):
        """Schedule email reminders for a contest"""
        try:
            from .simple_email import simple_email_service
            
            contest_time = datetime.fromisoformat(reminder_data["contest_time"])
            now = datetime.utcnow()
            
            print(f"📧 Scheduling emails for reminder {reminder_id}:")
            print(f"   Contest: {reminder_data['contest_name']}")
            print(f"   User: {reminder_data['user_email']}")
            print(f"   Time: {contest_time}")
            
            # Calculate reminder times
            reminder_24h = contest_time - timedelta(hours=24)
            reminder_1h = contest_time - timedelta(hours=1)
            
            # Send immediate confirmation email
            print(f"📧 Sending immediate confirmation email...")
            confirmation_result = simple_email_service.send_reminder_email(
                recipient_email=reminder_data["user_email"],
                contest_name=reminder_data["contest_name"],
                contest_url=reminder_data["contest_url"],
                contest_time=contest_time,
                reminder_type="confirmation"
            )
            
            if confirmation_result:
                print(f"✅ Confirmation email sent successfully to {reminder_data['user_email']}")
            else:
                print(f"❌ Failed to send confirmation email to {reminder_data['user_email']}")
            
            # Schedule 24-hour reminder
            if reminder_24h > now:
                delay_24h = (reminder_24h - now).total_seconds()
                timer_24h = threading.Timer(delay_24h, self._send_24h_reminder, args=[reminder_id])
                timer_24h.daemon = True
                timer_24h.start()
                
                # Store timer reference
                if reminder_id not in self.active_timers:
                    self.active_timers[reminder_id] = {}
                self.active_timers[reminder_id]["24h"] = timer_24h
                
                print(f"📧 24-hour reminder scheduled for {reminder_data['contest_name']} at {reminder_24h}")
            else:
                print(f"⏭️ Skipping 24-hour reminder (contest is within 24 hours)")
            
            # Schedule 1-hour reminder
            if reminder_1h > now:
                delay_1h = (reminder_1h - now).total_seconds()
                timer_1h = threading.Timer(delay_1h, self._send_1h_reminder, args=[reminder_id])
                timer_1h.daemon = True
                timer_1h.start()
                
                # Store timer reference
                if reminder_id not in self.active_timers:
                    self.active_timers[reminder_id] = {}
                self.active_timers[reminder_id]["1h"] = timer_1h
                
                print(f"🚨 1-hour reminder scheduled for {reminder_data['contest_name']} at {reminder_1h}")
            else:
                print(f"⏭️ Skipping 1-hour reminder (contest is within 1 hour)")
        
        except Exception as e:
            print(f"❌ Error scheduling reminder emails: {e}")
            import traceback
            traceback.print_exc()
    
    def _send_24h_reminder(self, reminder_id: str):
        """Send 24-hour reminder email"""
        try:
            from .simple_email import simple_email_service
            
            reminders = self.load_reminders()
            if reminder_id not in reminders or not reminders[reminder_id].get("is_active", True):
                return
            
            reminder_data = reminders[reminder_id]
            
            # Skip if already sent
            if reminder_data.get("email_sent_24h", False):
                return
            
            contest_time = datetime.fromisoformat(reminder_data["contest_time"])
            
            success = simple_email_service.send_reminder_email(
                recipient_email=reminder_data["user_email"],
                contest_name=reminder_data["contest_name"],
                contest_url=reminder_data["contest_url"],
                contest_time=contest_time,
                reminder_type="reminder"
            )
            
            if success:
                # Mark as sent
                reminder_data["email_sent_24h"] = True
                reminders[reminder_id] = reminder_data
                self.save_reminders(reminders)
                print(f"📧 24-hour reminder sent for {reminder_data['contest_name']}")
        
        except Exception as e:
            print(f"Error sending 24-hour reminder: {e}")
    
    def _send_1h_reminder(self, reminder_id: str):
        """Send 1-hour reminder email"""
        try:
            from .simple_email import simple_email_service
            
            reminders = self.load_reminders()
            if reminder_id not in reminders or not reminders[reminder_id].get("is_active", True):
                return
            
            reminder_data = reminders[reminder_id]
            
            # Skip if already sent
            if reminder_data.get("email_sent_1h", False):
                return
            
            contest_time = datetime.fromisoformat(reminder_data["contest_time"])
            
            success = simple_email_service.send_reminder_email(
                recipient_email=reminder_data["user_email"],
                contest_name=reminder_data["contest_name"],
                contest_url=reminder_data["contest_url"],
                contest_time=contest_time,
                reminder_type="final_reminder"
            )
            
            if success:
                # Mark as sent
                reminder_data["email_sent_1h"] = True
                reminders[reminder_id] = reminder_data
                self.save_reminders(reminders)
                print(f"🚨 1-hour reminder sent for {reminder_data['contest_name']}")
        
        except Exception as e:
            print(f"Error sending 1-hour reminder: {e}")
    
    def cancel_reminder_timers(self, reminder_id: str):
        """Cancel scheduled timers for a reminder"""
        if reminder_id in self.active_timers:
            timers = self.active_timers[reminder_id]
            
            if "24h" in timers and timers["24h"].is_alive():
                timers["24h"].cancel()
                print(f"⏹️ Cancelled 24-hour reminder timer for {reminder_id}")
            
            if "1h" in timers and timers["1h"].is_alive():
                timers["1h"].cancel()
                print(f"⏹️ Cancelled 1-hour reminder timer for {reminder_id}")
            
            del self.active_timers[reminder_id]
    
    def cleanup_old_reminders(self):
        """Remove reminders for contests that have already passed"""
        reminders = self.load_reminders()
        now = datetime.utcnow()
        
        to_remove = []
        for reminder_id, reminder_data in reminders.items():
            try:
                contest_time = datetime.fromisoformat(reminder_data["contest_time"])
                # Remove reminders for contests that ended more than 1 day ago
                if contest_time < now - timedelta(days=1):
                    to_remove.append(reminder_id)
            except:
                # Remove invalid reminders
                to_remove.append(reminder_id)
        
        for reminder_id in to_remove:
            self.cancel_reminder_timers(reminder_id)
            del reminders[reminder_id]
        
        if to_remove:
            self.save_reminders(reminders)
            print(f"🧹 Cleaned up {len(to_remove)} old reminders")
    
    def restart_pending_reminders(self):
        """Restart reminder timers after server restart"""
        reminders = self.load_reminders()
        
        for reminder_id, reminder_data in reminders.items():
            if reminder_data.get("is_active", True):
                try:
                    contest_time = datetime.fromisoformat(reminder_data["contest_time"])
                    now = datetime.utcnow()
                    
                    # Only restart if contest hasn't passed
                    if contest_time > now:
                        self.schedule_reminder_emails(reminder_id, reminder_data)
                except Exception as e:
                    print(f"Error restarting reminder {reminder_id}: {e}")

# Global instance
reminder_manager = SimpleReminderManager()