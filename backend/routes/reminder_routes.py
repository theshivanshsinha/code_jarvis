import logging
from flask import Blueprint, request, jsonify, g
from datetime import datetime
from typing import Optional, Dict, Any
import pytz

from ..services.reminder_service import reminder_service

logger = logging.getLogger(__name__)

reminder_bp = Blueprint('reminder', __name__)

@reminder_bp.route('/api/reminders', methods=['POST'])
def create_reminder():
    """
    Create a new contest reminder
    Expected JSON payload:
    {
        "user_email": "user@example.com",
        "contest_name": "Weekly Contest 123",
        "contest_url": "https://example.com/contest/123",
        "contest_time": "2025-12-31T23:59:59Z",
        "timezone": "UTC"
    }
    """
    logger.info(f"[Request ID: {g.get('request_id', 'N/A')}] Creating new reminder")
    data = request.get_json()
    
    if not data:
        logger.error("No JSON data received in request")
        return jsonify({'error': 'No JSON data received'}), 400
        
    logger.debug(f"Received data: {data}")
    
    # Validate required fields
    required_fields = ['user_email', 'contest_name', 'contest_url', 'contest_time']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        error_msg = f"Missing required fields: {', '.join(missing_fields)}"
        logger.error(f"[Request ID: {g.get('request_id', 'N/A')}] {error_msg}")
        return jsonify({'error': error_msg}), 400
    
    try:
        # Parse contest time
        timezone = pytz.timezone(data.get('timezone', 'UTC'))
        contest_time = datetime.fromisoformat(data['contest_time'].replace('Z', '+00:00'))
        contest_time = contest_time.astimezone(timezone)
        
        # Get user ID from auth token if available
        user_id = request.headers.get('X-User-ID')
        
        # Create reminder
        reminder = reminder_service.create_reminder(
            user_email=data['user_email'],
            contest_name=data['contest_name'],
            contest_url=data['contest_url'],
            contest_time=contest_time,
            user_id=user_id
        )
        
        if not reminder:
            return jsonify({
                'error': 'Failed to create reminder'
            }), 500
        
        return jsonify({
            'message': 'Reminder created successfully',
            'reminder_id': reminder['id']
        }), 201
        
    except ValueError as e:
        return jsonify({
            'error': f'Invalid date format: {str(e)}. Use ISO 8601 format (e.g., 2025-12-31T23:59:59Z)'
        }), 400
    except Exception as e:
        return jsonify({
            'error': f'Failed to create reminder: {str(e)}'
        }), 500

@reminder_bp.route('/api/reminders/<reminder_id>', methods=['DELETE'])
def remove_reminder(reminder_id: str):
    """Remove a contest reminder"""
    try:
        # Get user ID from auth token if available
        user_id = request.headers.get('X-User-ID')
        
        success = reminder_service.remove_reminder(reminder_id, user_id)
        
        if not success:
            return jsonify({
                'error': 'Reminder not found or already removed'
            }), 404
            
        return jsonify({
            'message': 'Reminder removed successfully',
            'reminder_id': reminder_id
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to remove reminder: {str(e)}'
        }), 500

@reminder_bp.route('/api/reminders', methods=['GET'])
def get_user_reminders():
    """Get all active reminders for the current user"""
    try:
        user_email = request.args.get('user_email')
        
        if not user_email:
            return jsonify({
                'error': 'Missing user_email parameter'
            }), 400
        
        reminders = reminder_service.get_user_reminders(user_email)
        
        # Convert datetime objects to ISO format for JSON serialization
        serialized_reminders = []
        for reminder in reminders:
            serialized = {
                'id': reminder['id'],
                'contest_name': reminder['contest_name'],
                'contest_url': reminder['contest_url'],
                'contest_time': reminder['contest_time'].isoformat(),
                'created_at': reminder['created_at'].isoformat(),
                'is_active': reminder.get('is_active', True)
            }
            if 'last_reminder_sent' in reminder and reminder['last_reminder_sent']:
                serialized['last_reminder_sent'] = reminder['last_reminder_sent'].isoformat()
            serialized_reminders.append(serialized)
        
        return jsonify({
            'reminders': serialized_reminders
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch reminders: {str(e)}'
        }), 500

@reminder_bp.route('/api/reminders/check', methods=['POST'])
def check_reminders():
    """Check and send pending reminders (for scheduled tasks)"""
    try:
        reminder_service.check_and_send_reminders()
        return jsonify({
            'message': 'Reminder check completed'
        }), 200
    except Exception as e:
        return jsonify({
            'error': f'Failed to check reminders: {str(e)}'
        }), 500
