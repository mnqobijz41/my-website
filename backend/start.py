#!/usr/bin/env python3
"""
Analytics Backend Startup Script
Run this to start the analytics server for MNQOBI LISBON JEZA's website
"""

import sys
import os
import traceback

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, scheduler
    from config import Config
    
    print("🚀 Starting MNQOBI LISBON JEZA Website Analytics Backend")
    print("=" * 60)
    
    # Check if email password is configured
    if not Config.SENDER_PASSWORD:
        print("⚠️  WARNING: Email password not configured!")
        print("   Please set EMAIL_PASSWORD in .env file for email functionality")
        print("   Analytics tracking will still work without email reports")
        print()
    
    # Start the scheduler
    scheduler.start_scheduler()
    
    # Send setup confirmation
    print("📧 Sending setup confirmation email...")
    scheduler.send_setup_confirmation()
    
    print()
    print("✅ Analytics backend is ready!")
    print(f"🌐 Website: {Config.WEBSITE_NAME}")
    print(f"📧 Reports to: {Config.RECIPIENT_EMAIL}")
    print(f"📊 Tracking: {'Enabled' if Config.TRACK_PAGE_VIEWS else 'Disabled'}")
    print(f"📅 Monthly reports: {'Enabled' if Config.MONTHLY_REPORT_ENABLED else 'Disabled'}")
    print()
    print("🔗 Access your website at: http://localhost:5000")
    print("📊 Health check: http://localhost:5000/health")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)
    
except KeyboardInterrupt:
    print("\n🛑 Server stopped by user")
    scheduler.stop_scheduler()
    
except Exception as e:
    print(f"❌ Error starting analytics backend: {e}")
    print("Stack trace:")
    traceback.print_exc()
    sys.exit(1) 