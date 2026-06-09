from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import datetime
from database import AnalyticsDB
from scheduler import AnalyticsScheduler
from config import Config

app = Flask(__name__)
CORS(app)

# Initialize components
db = AnalyticsDB()
scheduler = AnalyticsScheduler()

@app.route('/api/track', methods=['POST'])
def track_page_view():
    """Track a page view"""
    try:
        data = request.get_json()
        page_name = data.get('page', 'unknown')
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')

        db.record_page_view(page_name, ip_address, user_agent)

        return jsonify({'status': 'success', 'message': 'Page view tracked'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/stats/<int:year>/<int:month>')
def get_monthly_stats(year, month):
    """Get monthly statistics"""
    try:
        stats = db.get_monthly_stats(year, month)
        return jsonify({
            'status': 'success',
            'year': year,
            'month': month,
            'stats': stats
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/test-email', methods=['POST'])
def test_email():
    """Manually trigger a test monthly report email"""
    try:
        import threading
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        stats = db.calculate_monthly_stats(year, month)
        
        def send_in_background():
            try:
                print(f"📧 Attempting to send email to {Config.RECIPIENT_EMAIL}")
                print(f"📧 Using sender: {Config.SENDER_EMAIL}")
                print(f"📧 Password set: {'Yes' if Config.SENDER_PASSWORD else 'NO - EMPTY!'}")
                success = scheduler.email_service.send_monthly_report(year, month, stats)
                if success:
                    print("✅ Email sent successfully!")
                else:
                    print("❌ Email send returned False")
            except Exception as e:
                print(f"❌ Background email error: {e}")
        
        thread = threading.Thread(target=send_in_background, daemon=True)
        thread.start()
        
        return jsonify({'status': 'success', 'message': f'Email sending in background for {year}-{month:02d}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/setup/confirm', methods=['POST'])
def confirm_setup():
    """Send setup confirmation email"""
    try:
        success = scheduler.send_setup_confirmation()
        if success:
            return jsonify({'status': 'success', 'message': 'Setup confirmation sent'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to send confirmation'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'analytics_enabled': Config.TRACK_PAGE_VIEWS
    })

if __name__ == '__main__':
    scheduler.start_scheduler()
    scheduler.send_setup_confirmation()

    print(f"🌐 Starting analytics server for {Config.WEBSITE_NAME}")
    print(f"📊 Analytics tracking: {'Enabled' if Config.TRACK_PAGE_VIEWS else 'Disabled'}")
    print(f"📧 Monthly reports: {'Enabled' if Config.MONTHLY_REPORT_ENABLED else 'Disabled'}")
    print(f"📧 Reports will be sent to: {Config.RECIPIENT_EMAIL}")

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)