import os
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class ImprovedGoogleCalendarService:
    """Improved Google Calendar integration with better OAuth handling"""
    
    def __init__(self):
        self.scopes = [
            'https://www.googleapis.com/auth/calendar.events',
            'https://www.googleapis.com/auth/calendar.readonly'
        ]
        self.credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
        self.tokens_dir = os.getenv('CALENDAR_TOKENS_DIR', 'calendar_tokens')
        
        # Ensure tokens directory exists
        os.makedirs(self.tokens_dir, exist_ok=True)
        
        # OAuth configuration
        self.redirect_uri = os.getenv('OAUTH_REDIRECT_URI', 'http://localhost:8080/auth/google/callback')
        
    def get_oauth_url(self, user_id: str, state: str = None) -> Optional[Tuple[str, str]]:
        """Get OAuth authorization URL and state for user authentication"""
        try:
            if not os.path.exists(self.credentials_file):
                print(f"❌ Google credentials file not found: {self.credentials_file}")
                return None, None
                
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_file, 
                self.scopes
            )
            flow.redirect_uri = self.redirect_uri
            
            # Generate authorization URL
            authorization_url, oauth_state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent',  # Force consent screen to ensure refresh token
                state=state or user_id
            )
            
            # Store flow for later use
            flow_file = os.path.join(self.tokens_dir, f"flow_{user_id}.json")
            with open(flow_file, 'w') as f:
                json.dump({
                    'client_config': flow.client_config,
                    'redirect_uri': flow.redirect_uri,
                    'scopes': flow.scopes,
                    'state': oauth_state
                }, f)
            
            return authorization_url, oauth_state
            
        except Exception as e:
            print(f"❌ Failed to generate OAuth URL: {str(e)}")
            return None, None
    
    def handle_oauth_callback(self, user_id: str, authorization_code: str, state: str) -> bool:
        """Handle OAuth callback and store credentials"""
        try:
            flow_file = os.path.join(self.tokens_dir, f"flow_{user_id}.json")
            
            if not os.path.exists(flow_file):
                print("❌ OAuth flow data not found")
                return False
            
            # Recreate flow from stored data
            with open(flow_file, 'r') as f:
                flow_data = json.load(f)
            
            flow = InstalledAppFlow.from_client_config(
                flow_data['client_config'],
                flow_data['scopes']
            )
            flow.redirect_uri = flow_data['redirect_uri']
            
            # Exchange authorization code for tokens
            flow.fetch_token(code=authorization_code)
            
            # Store credentials
            token_file = os.path.join(self.tokens_dir, f"user_{user_id}_token.json")
            with open(token_file, 'w') as f:
                f.write(flow.credentials.to_json())
            
            # Clean up flow file
            os.remove(flow_file)
            
            print(f"✅ Calendar integration completed for user {user_id}")
            return True
            
        except Exception as e:
            print(f"❌ OAuth callback failed: {str(e)}")
            return False
    
    def get_service(self, user_id: str):
        """Get authenticated Google Calendar service for user"""
        token_file = os.path.join(self.tokens_dir, f"user_{user_id}_token.json")
        
        if not os.path.exists(token_file):
            return None
        
        try:
            creds = Credentials.from_authorized_user_file(token_file, self.scopes)
            
            # Refresh credentials if expired
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                # Save refreshed credentials
                with open(token_file, 'w') as f:
                    f.write(creds.to_json())
            
            if not creds or not creds.valid:
                return None
                
            return build('calendar', 'v3', credentials=creds)
            
        except Exception as e:
            print(f"❌ Failed to authenticate calendar service: {str(e)}")
            return None
    
    def create_contest_event(self, user_id: str, contest_data: Dict) -> Optional[str]:
        """Create contest event in Google Calendar"""
        service = self.get_service(user_id)
        if not service:
            print("❌ Calendar service not available. User needs to authorize access.")
            return None
        
        try:
            # Parse contest time
            start_time = datetime.fromisoformat(contest_data['start_time'].replace('Z', '+00:00'))
            duration = contest_data.get('duration_minutes', 180)
            end_time = start_time + timedelta(minutes=duration)
            
            # Create event
            event = {
                'summary': f"🏆 {contest_data['name']} - {contest_data['platform']}",
                'description': self._create_event_description(contest_data),
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': contest_data.get('timezone', 'UTC'),
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': contest_data.get('timezone', 'UTC'),
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 60},       # 1 hour before  
                        {'method': 'popup', 'minutes': 15},       # 15 minutes before
                    ],
                },
                'colorId': '11',  # Red color for contests
                'location': contest_data.get('url', ''),
                'source': {
                    'title': 'CodeJarvis',
                    'url': contest_data.get('url', '')
                }
            }
            
            # Insert event
            created_event = service.events().insert(calendarId='primary', body=event).execute()
            event_id = created_event.get('id')
            
            print(f"✅ Calendar event created successfully: {event_id}")
            return event_id
            
        except HttpError as e:
            print(f"❌ Google Calendar API error: {e.resp.status} - {e.content}")
            return None
        except Exception as e:
            print(f"❌ Failed to create calendar event: {str(e)}")
            return None
    
    def delete_contest_event(self, user_id: str, event_id: str) -> bool:
        """Delete contest event from Google Calendar"""
        service = self.get_service(user_id)
        if not service:
            return False
            
        try:
            service.events().delete(calendarId='primary', eventId=event_id).execute()
            print(f"✅ Calendar event deleted: {event_id}")
            return True
        except Exception as e:
            print(f"❌ Failed to delete calendar event: {str(e)}")
            return False
    
    def check_user_authorization(self, user_id: str) -> Dict:
        """Check if user has authorized calendar access"""
        token_file = os.path.join(self.tokens_dir, f"user_{user_id}_token.json")
        
        if not os.path.exists(token_file):
            return {
                'authorized': False,
                'message': 'Calendar access not authorized',
                'needs_auth': True
            }
        
        try:
            creds = Credentials.from_authorized_user_file(token_file, self.scopes)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    # Try to refresh
                    creds.refresh(Request())
                    with open(token_file, 'w') as f:
                        f.write(creds.to_json())
                    return {
                        'authorized': True,
                        'message': 'Calendar access authorized and refreshed',
                        'needs_auth': False
                    }
                else:
                    return {
                        'authorized': False,
                        'message': 'Calendar authorization expired',
                        'needs_auth': True
                    }
            
            return {
                'authorized': True,
                'message': 'Calendar access authorized',
                'needs_auth': False
            }
            
        except Exception as e:
            return {
                'authorized': False,
                'message': f'Calendar authorization error: {str(e)}',
                'needs_auth': True
            }
    
    def _create_event_description(self, contest_data: Dict) -> str:
        """Create a detailed event description"""
        description = f"""🏆 {contest_data['name']}

Platform: {contest_data['platform']}
Duration: {contest_data.get('duration_minutes', 180)} minutes
Registration: {contest_data.get('url', 'N/A')}

📚 Contest Tips:
• Register early if registration is required
• Test your coding environment beforehand  
• Have snacks and water ready
• Stay calm and read problems carefully
• Manage your time effectively

Good luck! 🚀

Created by CodeJarvis - Your AI coding companion
"""
        return description


class CalendarFallbackService:
    """Fallback service for users without Google Calendar API access"""
    
    @staticmethod
    def generate_ics_content(contest_data: Dict) -> str:
        """Generate ICS file content for manual calendar import"""
        start_time = datetime.fromisoformat(contest_data['start_time'].replace('Z', '+00:00'))
        duration = contest_data.get('duration_minutes', 180)
        end_time = start_time + timedelta(minutes=duration)
        
        # Format times for ICS (UTC)
        start_str = start_time.strftime('%Y%m%dT%H%M%SZ')
        end_str = end_time.strftime('%Y%m%dT%H%M%SZ')
        created_str = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        
        # Create unique UID
        uid = f"{contest_data['name'].replace(' ', '_')}_{start_str}@codejarvis.com"
        
        ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//CodeJarvis//Contest Reminder//EN
METHOD:PUBLISH
CALSCALE:GREGORIAN
BEGIN:VEVENT
UID:{uid}
DTSTART:{start_str}
DTEND:{end_str}
DTSTAMP:{created_str}
CREATED:{created_str}
LAST-MODIFIED:{created_str}
SUMMARY:🏆 {contest_data['name']} - {contest_data['platform']}
DESCRIPTION:Contest Details:\\n\\nPlatform: {contest_data['platform']}\\nDuration: {duration} minutes\\nURL: {contest_data.get('url', 'N/A')}\\n\\nGood luck! 🚀\\n\\nCreated by CodeJarvis
LOCATION:{contest_data.get('url', '')}
URL:{contest_data.get('url', '')}
STATUS:CONFIRMED
TRANSP:OPAQUE
SEQUENCE:0
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
    
    @staticmethod
    def save_ics_file(contest_data: Dict, filepath: str) -> bool:
        """Save ICS file for download"""
        try:
            ics_content = CalendarFallbackService.generate_ics_content(contest_data)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(ics_content)
            return True
        except Exception as e:
            print(f"❌ Failed to create ICS file: {str(e)}")
            return False


# Global service instances
google_calendar_service = ImprovedGoogleCalendarService()
calendar_fallback_service = CalendarFallbackService()
