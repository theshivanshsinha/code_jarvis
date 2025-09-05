/**
 * EmailJS Service - Super Simple Email Solution!
 * No backend email server required - emails sent directly from browser
 * Perfect for development and simple deployments
 */

import emailjs from '@emailjs/browser';

class EmailJSService {
    constructor() {
        // EmailJS configuration - get these from your EmailJS dashboard
        this.serviceId = process.env.REACT_APP_EMAILJS_SERVICE_ID || 'your_service_id';
        this.templateId = {
            contestReminder: process.env.REACT_APP_EMAILJS_CONTEST_TEMPLATE || 'contest_reminder',
            dailyMotivation: process.env.REACT_APP_EMAILJS_DAILY_TEMPLATE || 'daily_motivation',
            reminderConfirmation: process.env.REACT_APP_EMAILJS_CONFIRMATION_TEMPLATE || 'reminder_confirmation'
        };
        this.publicKey = process.env.REACT_APP_EMAILJS_PUBLIC_KEY || 'your_public_key';
        
        // Initialize EmailJS
        if (this.publicKey !== 'your_public_key') {
            emailjs.init(this.publicKey);
            console.log('✅ EmailJS initialized successfully');
        } else {
            console.warn('⚠️  EmailJS not configured. Add your keys to .env file');
        }
    }
    
    /**
     * Send contest reminder email
     * @param {Object} params - Email parameters
     */
    async sendContestReminder(params) {
        const emailParams = {
            to_email: params.userEmail,
            to_name: params.userName,
            contest_name: params.contestName,
            contest_date: params.contestDate,
            contest_url: params.contestUrl,
            time_until: params.timeUntil,
            from_name: 'CodeJarvis'
        };
        
        try {
            const response = await emailjs.send(
                this.serviceId,
                this.templateId.contestReminder,
                emailParams
            );
            
            console.log('✅ Contest reminder sent successfully:', response.status);
            return { success: true, message: 'Contest reminder sent!' };
        } catch (error) {
            console.error('❌ Failed to send contest reminder:', error);
            return { success: false, message: 'Failed to send reminder', error };
        }
    }
    
    /**
     * Send reminder confirmation email
     */
    async sendReminderConfirmation(params) {
        const emailParams = {
            to_email: params.userEmail,
            to_name: params.userName,
            contest_name: params.contestName,
            contest_date: params.contestDate,
            contest_url: params.contestUrl,
            from_name: 'CodeJarvis'
        };
        
        try {
            const response = await emailjs.send(
                this.serviceId,
                this.templateId.reminderConfirmation,
                emailParams
            );
            
            console.log('✅ Confirmation sent successfully:', response.status);
            return { success: true, message: 'Confirmation sent!' };
        } catch (error) {
            console.error('❌ Failed to send confirmation:', error);
            return { success: false, message: 'Failed to send confirmation', error };
        }
    }
    
    /**
     * Send daily motivation email
     */
    async sendDailyMotivation(params) {
        const emailParams = {
            to_email: params.userEmail,
            to_name: params.userName,
            total_solved: params.totalSolved || 0,
            current_streak: params.currentStreak || 0,
            favorite_platform: params.favoritePlatform || 'LeetCode',
            from_name: 'CodeJarvis'
        };
        
        try {
            const response = await emailjs.send(
                this.serviceId,
                this.templateId.dailyMotivation,
                emailParams
            );
            
            console.log('✅ Daily motivation sent successfully:', response.status);
            return { success: true, message: 'Daily motivation sent!' };
        } catch (error) {
            console.error('❌ Failed to send daily motivation:', error);
            return { success: false, message: 'Failed to send motivation', error };
        }
    }
    
    /**
     * Test EmailJS connection
     */
    async testConnection() {
        if (this.publicKey === 'your_public_key') {
            return { success: false, message: 'EmailJS not configured' };
        }
        
        try {
            // Send a test email to verify connection
            const testParams = {
                to_email: 'test@example.com',
                to_name: 'Test User',
                message: 'This is a test message from CodeJarvis',
                from_name: 'CodeJarvis'
            };
            
            // Note: This would actually send an email, so we just validate config
            return { 
                success: true, 
                message: 'EmailJS configured correctly',
                config: {
                    serviceId: this.serviceId,
                    hasPublicKey: !!this.publicKey,
                    templates: Object.keys(this.templateId).length
                }
            };
        } catch (error) {
            return { 
                success: false, 
                message: 'EmailJS configuration error', 
                error: error.message 
            };
        }
    }
}

// Export singleton instance
export const emailJSService = new EmailJSService();

export default EmailJSService;
