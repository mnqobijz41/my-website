import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

class EmailService:
    def __init__(self):
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.sender_email = Config.SENDER_EMAIL
        self.sender_password = Config.SENDER_PASSWORD
        self.recipient_email = Config.RECIPIENT_EMAIL
    
    def send_email(self, subject, body, html_body=None):
        """Send an email"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = subject
            
            # Add plain text and HTML versions
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_setup_confirmation(self):
        """Send confirmation email when analytics is first set up"""
        subject = f"✅ Analytics Setup Complete - {Config.WEBSITE_NAME}"
        
        body = f"""
Analytics Setup Confirmation

Dear MNQOBI LISBON JEZA,

Your website analytics system has been successfully set up and is now active!

Website: {Config.WEBSITE_NAME}
URL: {Config.WEBSITE_URL}

What's been configured:
✅ Page view tracking
✅ Monthly statistics calculation
✅ Monthly email reports (only sent when there are viewers)
✅ Database for storing analytics data

You will receive monthly reports at: {self.recipient_email}

The system will automatically:
- Track all page views on your website
- Calculate monthly statistics
- Send you a report only if there were viewers that month
- Store data securely in a local database

If you have any questions or need to modify settings, please check the backend configuration files.

Best regards,
Your Analytics System
        """
        
        html_body = f"""
        <html>
        <body>
            <h2>✅ Analytics Setup Complete</h2>
            <p><strong>Dear MNQOBI LISBON JEZA,</strong></p>
            
            <p>Your website analytics system has been successfully set up and is now active!</p>
            
            <h3>Website Details:</h3>
            <ul>
                <li><strong>Website:</strong> {Config.WEBSITE_NAME}</li>
                <li><strong>URL:</strong> {Config.WEBSITE_URL}</li>
            </ul>
            
            <h3>What's been configured:</h3>
            <ul>
                <li>✅ Page view tracking</li>
                <li>✅ Monthly statistics calculation</li>
                <li>✅ Monthly email reports (only sent when there are viewers)</li>
                <li>✅ Database for storing analytics data</li>
            </ul>
            
            <p><strong>You will receive monthly reports at:</strong> {self.recipient_email}</p>
            
            <h3>The system will automatically:</h3>
            <ul>
                <li>Track all page views on your website</li>
                <li>Calculate monthly statistics</li>
                <li>Send you a report only if there were viewers that month</li>
                <li>Store data securely in a local database</li>
            </ul>
            
            <p>If you have any questions or need to modify settings, please check the backend configuration files.</p>
            
            <p><strong>Best regards,<br>Your Analytics System</strong></p>
        </body>
        </html>
        """
        
        return self.send_email(subject, body, html_body)
    
    def send_monthly_report(self, year, month, stats):
        """Send monthly analytics report"""
        month_name = datetime.date(year, month, 1).strftime('%B %Y')
        
        subject = f"📊 Monthly Analytics Report - {month_name} - {Config.WEBSITE_NAME}"
        
        body = f"""
Monthly Analytics Report

Dear MNQOBI LISBON JEZA,

Here's your monthly analytics report for {month_name}:

Website: {Config.WEBSITE_NAME}
URL: {Config.WEBSITE_URL}

📈 Statistics for {month_name}:
• Total Page Views: {stats['total_views']:,}
• Unique Visitors: {stats['unique_visitors']:,}

This report was generated automatically by your analytics system.

Best regards,
Your Analytics System
        """
        
        html_body = f"""
        <html>
        <body>
            <h2>📊 Monthly Analytics Report</h2>
            <p><strong>Dear MNQOBI LISBON JEZA,</strong></p>
            
            <p>Here's your monthly analytics report for <strong>{month_name}</strong>:</p>
            
            <h3>Website Details:</h3>
            <ul>
                <li><strong>Website:</strong> {Config.WEBSITE_NAME}</li>
                <li><strong>URL:</strong> {Config.WEBSITE_URL}</li>
            </ul>
            
            <h3>📈 Statistics for {month_name}:</h3>
            <ul>
                <li><strong>Total Page Views:</strong> {stats['total_views']:,}</li>
                <li><strong>Unique Visitors:</strong> {stats['unique_visitors']:,}</li>
            </ul>
            
            <p><em>This report was generated automatically by your analytics system.</em></p>
            
            <p><strong>Best regards,<br>Your Analytics System</strong></p>
        </body>
        </html>
        """
        
        return self.send_email(subject, body, html_body) 