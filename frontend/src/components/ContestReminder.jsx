import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const ContestReminder = ({ contest, userId, userEmail }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [hasReminder, setHasReminder] = useState(false);
  const [reminderId, setReminderId] = useState(null);

  // Check if user already has a reminder for this contest
  useEffect(() => {
    const checkReminder = async () => {
      if (!userEmail) return;
      
      try {
        const response = await axios.get('http://localhost:5000/api/reminders', {
          params: { user_email: userEmail },
          withCredentials: true
        });
        
        if (response.data && response.data.reminders) {
          const reminder = response.data.reminders.find(
            r => r.contest_url === contest.url && r.is_active
          );
          
          if (reminder) {
            setHasReminder(true);
            setReminderId(reminder.id);
          }
        }
      } catch (error) {
        console.error('Error checking reminder:', error.response?.data || error.message);
      }
    };

    checkReminder();
  }, [contest.url, userEmail]);

  const handleReminderToggle = async () => {
    if (isLoading || !userEmail) return;
    
    setIsLoading(true);
    
    try {
      if (hasReminder && reminderId) {
        // Remove reminder
        await axios.delete(`http://localhost:5000/api/reminders/${reminderId}`, {
          headers: userId ? { 'X-User-ID': userId } : {},
          withCredentials: true
        });
        setHasReminder(false);
        setReminderId(null);
        toast.success('Reminder removed successfully');
      } else {
        // Add reminder
        const response = await axios.post('http://localhost:5000/api/reminders', {
          user_email: userEmail,
          contest_name: contest.name,
          contest_url: contest.url,
          contest_time: contest.start_time,
          timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
        }, {
          headers: userId ? { 'X-User-ID': userId } : {},
          withCredentials: true
        });
        
        if (response.data && response.data.reminder_id) {
          setHasReminder(true);
          setReminderId(response.data.reminder_id);
          toast.success('Reminder set successfully!');
        } else {
          throw new Error('Invalid response from server');
        }
      }
    } catch (error) {
      console.error('Error toggling reminder:', error.response?.data || error.message);
      toast.error(
        error.response?.data?.error || 
        'Failed to update reminder. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      onClick={handleReminderToggle}
      disabled={isLoading}
      className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
        hasReminder 
          ? 'bg-red-500 hover:bg-red-600 text-white'
          : 'bg-blue-500 hover:bg-blue-600 text-white'
      }`}
    >
      {isLoading ? (
        'Loading...'
      ) : hasReminder ? (
        <>
          <i className="fas fa-bell-slash mr-2"></i>
          Remove Reminder
        </>
      ) : (
        <>
          <i className="fas fa-bell mr-2"></i>
          Set Reminder
        </>
      )}
    </button>
  );
};

export default ContestReminder;
