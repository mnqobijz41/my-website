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
        """Generate and send monthly report - always sends, even if zero views"""
        try:
            now = datetime.datetime.now()
            if now.month == 1:
                year = now.year - 1
                month = 12
            else:
                year = now.year
                month = now.month - 1

            current_month_key = f"{year}-{month:02d}"
            if self.last_report_month == current_month_key:
                print(f"Report for {current_month_key} already sent this session, skipping.")
                return

            stats = self.db.calculate_monthly_stats(year, month)

            # Always send — even if zero views
            print(f"Sending monthly report for {year}-{month:02d}: {stats['total_views']} views, {stats['unique_visitors']} unique visitors")
            success = self.email_service.send_monthly_report(year, month, stats)
            if success:
                print(f"✅ Monthly report sent successfully for {year}-{month:02d}")
                self.last_report_month = current_month_key
            else:
                print(f"❌ Failed to send monthly report for {year}-{month:02d}")

        except Exception as e:
            print(f"Error generating monthly report: {e}")

    def check_monthly_report(self):
        """Check if it's time to send monthly report (runs daily)"""
        now = datetime.datetime.now()
        if now.day == 1 and now.hour == 9 and now.minute < 10:
            self.generate_monthly_report()

    def schedule_monthly_report(self):
        """Schedule daily check for monthly report generation"""
        schedule.every().day.at("09:00").do(self.check_monthly_report)
        print("📅 Monthly report check scheduled daily at 09:00")

    def start_scheduler(self):
        """Start the scheduler in a background thread"""
        if not self.running:
            self.running = True
            self.schedule_monthly_report()

            def run_scheduler():
                while self.running:
                    schedule.run_pending()
                    time.sleep(60)

            scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
            scheduler_thread.start()
            print("🚀 Analytics scheduler started")

    def stop_scheduler(self):
        """Stop the scheduler"""
        self.running = False
        schedule.clear()
        print("🛑 Analytics scheduler stopped")

    def send_setup_confirmation(self):
        """Send setup confirmation email (only once)"""
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