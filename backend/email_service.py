import datetime
import urllib.request
import urllib.error
import json
import os
from config import Config

class EmailService:
    def __init__(self):
        self.sender_email = Config.SENDER_EMAIL
        self.recipient_email = Config.RECIPIENT_EMAIL
        self.api_key = os.getenv('SENDGRID_API_KEY', '')

    def send_email(self, subject, body, html_body=None):
        """Send an email via SendGrid HTTP API"""
        try:
            if not self.api_key:
                print("❌ SENDGRID_API_KEY is not set!")
                return False

            payload = {
                "personalizations": [
                    {
                        "to": [{"email": self.recipient_email}],
                        "subject": subject
                    }
                ],
                "from": {"email": self.sender_email, "name": "Portfolio Analytics"},
                "content": [
                    {"type": "text/plain", "value": body}
                ]
            }

            if html_body:
                payload["content"].append({"type": "text/html", "value": html_body})

            data = json.dumps(payload).encode("utf-8")

            req = urllib.request.Request(
                "https://api.sendgrid.com/v3/mail/send",
                data=data,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                method="POST"
            )

            with urllib.request.urlopen(req) as response:
                print(f"✅ Email sent! Status: {response.status}")
                return True

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            print(f"❌ SendGrid HTTP error {e.code}: {error_body}")
            return False
        except Exception as e:
            print(f"❌ Error sending email: {e}")
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
- Page view tracking
- Monthly statistics calculation
- Monthly email reports (sent every month, even with zero views)
- Database for storing analytics data

You will receive monthly reports at: {self.recipient_email}

Best regards,
Your Analytics System
        """

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="color: #2c3e50;">✅ Analytics Setup Complete</h2>
            <p><strong>Dear MNQOBI LISBON JEZA,</strong></p>
            <p>Your website analytics system has been successfully set up!</p>
            <h3>Website Details:</h3>
            <ul>
                <li><strong>Website:</strong> {Config.WEBSITE_NAME}</li>
                <li><strong>URL:</strong> <a href="{Config.WEBSITE_URL}">{Config.WEBSITE_URL}</a></li>
            </ul>
            <h3>What's been configured:</h3>
            <ul>
                <li>✅ Page view tracking</li>
                <li>✅ Monthly statistics calculation</li>
                <li>✅ Monthly email reports (sent every month, even with zero views)</li>
                <li>✅ Database for storing analytics data</li>
            </ul>
            <p><strong>You will receive monthly reports at:</strong> {self.recipient_email}</p>
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

Statistics for {month_name}:
- Total Page Views: {stats['total_views']:,}
- Unique Visitors: {stats['unique_visitors']:,}

{"No visitors this month, but the system is running and tracking." if stats['total_views'] == 0 else "Great job! Keep sharing your portfolio."}

Best regards,
Your Analytics System
        """

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="color: #2c3e50;">📊 Monthly Analytics Report</h2>
            <p><strong>Dear MNQOBI LISBON JEZA,</strong></p>
            <p>Here's your monthly analytics report for <strong>{month_name}</strong>:</p>
            <h3>Website Details:</h3>
            <ul>
                <li><strong>Website:</strong> {Config.WEBSITE_NAME}</li>
                <li><strong>URL:</strong> <a href="{Config.WEBSITE_URL}">{Config.WEBSITE_URL}</a></li>
            </ul>
            <h3>📈 Statistics for {month_name}:</h3>
            <table style="border-collapse: collapse; width: 300px;">
                <tr style="background: #f4f4f4;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Total Page Views</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{stats['total_views']:,}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Unique Visitors</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{stats['unique_visitors']:,}</td>
                </tr>
            </table>
            <p style="margin-top: 20px; color: #666;">
                {"No visitors this month, but the system is running and tracking." if stats['total_views'] == 0 else "Great job! Keep sharing your portfolio."}
            </p>
            <p><strong>Best regards,<br>Your Analytics System</strong></p>
        </body>
        </html>
        """

        return self.send_email(subject, body, html_body)