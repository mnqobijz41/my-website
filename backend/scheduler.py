import schedule
import time
import datetime
import threading
from database import AnalyticsDB
from email_service import EmailService
from config import Config

class AnalyticsScheduler:
    def __init__(self):
        self.db = AnalyticsDB()
        self.email_service = EmailService()
        self.running = False
        self.last_report_month = None
    
    def generate_monthly_report(self):
        """Generate and send monthly report"""
        try:
            # Get last month's data
            now = datetime.datetime.now()
            if now.month == 1:
                year = now.year - 1
                month = 12
            else:
                year = now.year
                month = now.month - 1
            
            # Check if we already sent a report for this month
            current_month_key = f"{year}-{month:02d}"
            if self.last_report_month == current_month_key:
                return
            
            # Calculate monthly stats
            stats = self.db.calculate_monthly_stats(year, month)
            
            # Only send email if there were viewers
            if stats['total_views'] > 0:
                print(f"Sending monthly report for {year}-{month:02d}: {stats['total_views']} views")
                success = self.email_service.send_monthly_report(year, month, stats)
                if success:
                    print(f"✅ Monthly report sent successfully for {year}-{month:02d}")
                    self.last_report_month = current_month_key
                else:
                    print(f"❌ Failed to send monthly report for {year}-{month:02d}")
            else:
                print(f"No views for {year}-{month:02d}, skipping email report")
                self.last_report_month = current_month_key
                
        except Exception as e:
            print(f"Error generating monthly report: {e}")
    
    def check_monthly_report(self):
        """Check if it's time to send monthly report (runs daily)"""
        now = datetime.datetime.now()
        # Only run on the 1st of each month at 9:00 AM
        if now.day == 1 and now.hour == 9 and now.minute < 10:
            self.generate_monthly_report()
    
    def schedule_monthly_report(self):
        """Schedule daily check for monthly report generation"""
        # Check daily at 9:00 AM
        schedule.every().day.at("09:00").do(self.check_monthly_report)
        print("📅 Monthly report check scheduled for daily at 9:00 AM")
    
    def start_scheduler(self):
        """Start the scheduler in a separate thread"""
        if not self.running:
            self.running = True
            self.schedule_monthly_report()
            
            def run_scheduler():
                while self.running:
                    schedule.run_pending()
                    time.sleep(60)  # Check every minute
            
            scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
            scheduler_thread.start()
            print("🚀 Analytics scheduler started")
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.running = False
        schedule.clear()
        print("🛑 Analytics scheduler stopped")
    
    def send_setup_confirmation(self):
        """Send setup confirmation email"""
        if not self.db.is_setup_complete():
            success = self.email_service.send_setup_confirmation()
            if success:
                self.db.mark_setup_complete()
                print("✅ Setup confirmation email sent")
                return True
            else:
                print("❌ Failed to send setup confirmation email")
                return False
        return True 