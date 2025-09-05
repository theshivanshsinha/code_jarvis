import os
import json
from datetime import datetime, timedelta
from typing import Dict, Optional
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class GoogleCalendarService:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/calendar']
        self.credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
        self.token_file = os.getenv('GOOGLE_TOKEN_FILE', 'token.json')
        self.service = None
    
    def authenticate(self, user_id: str) -> bool:
        """Authenticate with Google Calendar API for a specific user"""
        try:
            creds = None
            token_file = f"tokens/user_{user_id}_token.json"
            
            # Load existing token
            if os.path.exists(token_file):
                creds = Credentials.from_authorized_user_file(token_file, self.scopes)
            
            # If there are no (valid) credentials available, let the user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    # This would need to be handled through OAuth flow in production
                    # For now, return False to indicate authentication needed
                    return False
                
                # Save the credentials for the next run
                os.makedirs(os.path.dirname(token_file), exist_ok=True)
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
            
            self.service = build('calendar', 'v3', credentials=creds)
            return True
        except Exception as e:
            print(f"Authentication failed: {str(e)}")
            return False
    
    def create_contest_event(self, user_id: str, contest_data: Dict) -> Optional[str]:
        """Create a contest event in Google Calendar"""
        if not self.authenticate(user_id):
            return None
        
        try:
            # Parse contest start time
            start_time = datetime.fromisoformat(contest_data['start'].replace('Z', '+00:00'))
            end_time = start_time + timedelta(minutes=contest_data.get('duration_minutes', 180))
            
            # Create event
            event = {
                'summary': f"{contest_data['platform']}: {contest_data['name']}",
                'description': f"""
🏆 Contest Details:
Platform: {contest_data['platform']}
Duration: {contest_data.get('duration_minutes', 180)} minutes
Registration: {contest_data.get('url', 'N/A')}

📅 Created by CodeJarvis - Your AI coding companion
""".strip(),
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 60},       # 1 hour before
                        {'method': 'popup', 'minutes': 15},       # 15 minutes before
                    ],
                },
                'attendees': [
                    {'email': contest_data.get('user_email', '')},
                ],
                'colorId': '11',  # Red color for contests
                'location': contest_data.get('url', ''),
                'source': {
                    'title': 'CodeJarvis',
                    'url': 'https://your-app-domain.com'
                }
            }
            
            # Insert event
            event_result = self.service.events().insert(calendarId='primary', body=event).execute()
            return event_result.get('id')
        
        except Exception as e:
            print(f"Failed to create calendar event: {str(e)}")
            return None
    
    def update_contest_event(self, user_id: str, event_id: str, contest_data: Dict) -> bool:
        """Update an existing contest event"""
        if not self.authenticate(user_id):
            return False
        
        try:
            # Get existing event
            event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
            
            # Update event details
            start_time = datetime.fromisoformat(contest_data['start'].replace('Z', '+00:00'))
            end_time = start_time + timedelta(minutes=contest_data.get('duration_minutes', 180))
            
            event['summary'] = f"{contest_data['platform']}: {contest_data['name']}"
            event['start']['dateTime'] = start_time.isoformat()
            event['end']['dateTime'] = end_time.isoformat()
            event['location'] = contest_data.get('url', '')
            
            # Update event
            self.service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
            return True
        
        except Exception as e:
            print(f"Failed to update calendar event: {str(e)}")
            return False
    
    def delete_contest_event(self, user_id: str, event_id: str) -> bool:
        """Delete a contest event from Google Calendar"""
        if not self.authenticate(user_id):
            return False
        
        try:
            self.service.events().delete(calendarId='primary', eventId=event_id).execute()
            return True
        except Exception as e:
            print(f"Failed to delete calendar event: {str(e)}")
            return False
    
    def get_oauth_authorization_url(self) -> Optional[str]:
        """Get OAuth authorization URL for user to grant calendar access"""
        try:
            if not os.path.exists(self.credentials_file):
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_file, self.scopes
            )
            flow.redirect_uri = 'http://localhost:8080/callback'  # Configure as needed
            
            authorization_url, _ = flow.authorization_url(prompt='consent')
            return authorization_url
        except Exception as e:
            print(f"Failed to get OAuth URL: {str(e)}")
            return None
    
    def exchange_code_for_token(self, code: str, user_id: str) -> bool:
        """Exchange OAuth code for access token"""
        try:
            if not os.path.exists(self.credentials_file):
                return False
            
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_file, self.scopes
            )
            flow.redirect_uri = 'http://localhost:8080/callback'
            
            flow.fetch_token(code=code)
            creds = flow.credentials
            
            # Save credentials
            token_file = f"tokens/user_{user_id}_token.json"
            os.makedirs(os.path.dirname(token_file), exist_ok=True)
            
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
            
            return True
        except Exception as e:
            print(f"Failed to exchange code for token: {str(e)}")
            return False
    
    def create_recurring_reminder(self, user_id: str, reminder_data: Dict) -> Optional[str]:
        """Create a recurring reminder event (e.g., daily coding reminder)"""
        if not self.authenticate(user_id):
            return None
        
        try:
            # Create recurring event for daily coding reminders
            event = {
                'summary': '🚀 Daily Coding Time - CodeJarvis',
                'description': """
Time for your daily coding practice!

📚 Suggestions:
- Solve at least one problem
- Review previous solutions
- Learn a new concept
- Practice on your favorite platform

Keep up the great work! 💪

Created by CodeJarvis
""".strip(),
                'start': {
                    'dateTime': reminder_data['start_time'],
                    'timeZone': reminder_data.get('timezone', 'UTC'),
                },
                'end': {
                    'dateTime': reminder_data['end_time'],
                    'timeZone': reminder_data.get('timezone', 'UTC'),
                },
                'recurrence': [
                    f"RRULE:FREQ=DAILY;BYDAY={reminder_data.get('days', 'MO,TU,WE,TH,FR,SA,SU')}"
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 0},
                    ],
                },
                'colorId': '10',  # Green color for reminders
            }
            
            event_result = self.service.events().insert(calendarId='primary', body=event).execute()
            return event_result.get('id')
        
        except Exception as e:
            print(f"Failed to create recurring reminder: {str(e)}")
            return None

# Alternative service for users without Google Calendar API access
class SimpleCalendarService:
    """Fallback service that creates .ics files for manual import"""
    
    def create_ics_event(self, contest_data: Dict) -> str:
        """Create an ICS file content for contest reminder"""
        start_time = datetime.fromisoformat(contest_data['start'].replace('Z', '+00:00'))
        end_time = start_time + timedelta(minutes=contest_data.get('duration_minutes', 180))
        
        # Format times for ICS
        start_str = start_time.strftime('%Y%m%dT%H%M%SZ')
        end_str = end_time.strftime('%Y%m%dT%H%M%SZ')
        
        ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//CodeJarvis//Contest Reminder//EN
METHOD:REQUEST
BEGIN:VEVENT
UID:{contest_data['name'].replace(' ', '_')}_{start_str}@codejarvis
DTSTART:{start_str}
DTEND:{end_str}
SUMMARY:{contest_data['platform']}: {contest_data['name']}
DESCRIPTION:Contest Details:\\nPlatform: {contest_data['platform']}\\nDuration: {contest_data.get('duration_minutes', 180)} minutes\\nURL: {contest_data.get('url', 'N/A')}\\n\\nCreated by CodeJarvis
LOCATION:{contest_data.get('url', '')}
STATUS:CONFIRMED
BEGIN:VALARM
TRIGGER:-P1D
ACTION:DISPLAY
DESCRIPTION:Contest tomorrow: {contest_data['name']}
END:VALARM
BEGIN:VALARM
TRIGGER:-PT1H
ACTION:DISPLAY
DESCRIPTION:Contest starts in 1 hour: {contest_data['name']}
END:VALARM
END:VEVENT
END:VCALENDAR"""
        
        return ics_content
    
    def save_ics_file(self, contest_data: Dict, filename: str) -> bool:
        """Save ICS content to file"""
        try:
            ics_content = self.create_ics_event(contest_data)
            with open(filename, 'w') as f:
                f.write(ics_content)
            return True
        except Exception as e:
            print(f"Failed to save ICS file: {str(e)}")
            return False

# Global service instances
google_calendar_service = GoogleCalendarService()
simple_calendar_service = SimpleCalendarService()
