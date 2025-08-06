from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import datetime
from database import AnalyticsDB
from scheduler import AnalyticsScheduler
from config import Config

app = Flask(__name__, static_folder='../')
CORS(app)

# Initialize components
db = AnalyticsDB()
scheduler = AnalyticsScheduler()

@app.route('/')
def index():
    """Serve the main index.html file"""
    return send_from_directory('../', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('../', filename)

@app.route('/api/track', methods=['POST'])
def track_page_view():
    """Track a page view"""
    try:
        data = request.get_json()
        page_name = data.get('page', 'unknown')
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')
        
        # Record the page view
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
    # Start the scheduler
    scheduler.start_scheduler()
    
    # Send setup confirmation if not already sent
    scheduler.send_setup_confirmation()
    
    print(f"🌐 Starting analytics server for {Config.WEBSITE_NAME}")
    print(f"📊 Analytics tracking: {'Enabled' if Config.TRACK_PAGE_VIEWS else 'Disabled'}")
    print(f"📧 Monthly reports: {'Enabled' if Config.MONTHLY_REPORT_ENABLED else 'Disabled'}")
    print(f"📧 Reports will be sent to: {Config.RECIPIENT_EMAIL}")
    
    app.run(host='0.0.0.0', port=5000, debug=False) 