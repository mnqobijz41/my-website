# Analytics Backend for MNQOBI LISBON JEZA Website

This Python backend provides analytics tracking and monthly email reports for the personal portfolio website.

## Features

- 📊 **Page View Tracking**: Records all page views with IP addresses and user agents
- 📅 **Monthly Reports**: Automatically generates and emails monthly statistics
- 📧 **Smart Email**: Only sends reports when there are actual viewers
- 🔒 **Secure**: Uses SQLite database for local data storage
- ⚡ **Lightweight**: Minimal resource usage with Flask

## Setup Instructions

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Email (Optional but Recommended)

Create a `.env` file in the backend directory:

```bash
# backend/.env
EMAIL_PASSWORD=your_gmail_app_password
```

**Note**: Use a Gmail App Password, not your regular password. To get one:
1. Go to Google Account Settings
2. Security → 2-Step Verification → App passwords
3. Generate a new app password for "Mail"

### 3. Start the Analytics Server

```bash
python start.py
```

The server will start on `http://localhost:5000` and serve your website with analytics tracking.

## How It Works

### Page View Tracking
- Every page load sends a tracking request to `/api/track`
- Data is stored in SQLite database (`analytics.db`)
- Tracks page name, IP address, user agent, and timestamp

### Monthly Reports
- Runs on the 1st of each month at 9:00 AM
- Calculates total views and unique visitors for the previous month
- Only sends email if there were actual viewers
- Email sent to: `mnqobijz41@gmail.com`

### Setup Confirmation
- Sends a confirmation email when first started
- Confirms all systems are working properly

## API Endpoints

- `GET /` - Serves the main website
- `POST /api/track` - Track a page view
- `GET /api/stats/<year>/<month>` - Get monthly statistics
- `POST /api/setup/confirm` - Send setup confirmation
- `GET /health` - Health check endpoint

## File Structure

```
backend/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── database.py         # SQLite database operations
├── email_service.py    # Email functionality
├── scheduler.py        # Monthly report scheduler
├── start.py           # Startup script
├── requirements.txt   # Python dependencies
├── README.md         # This file
└── .env              # Email configuration (create this)
```

## Configuration

Edit `config.py` to modify:
- Email settings
- Website information
- Analytics preferences

## Troubleshooting

### Email Not Working
1. Check `.env` file has correct `EMAIL_PASSWORD`
2. Ensure 2FA is enabled on Gmail
3. Use App Password, not regular password

### Server Won't Start
1. Check Python version (3.7+ required)
2. Install all dependencies: `pip install -r requirements.txt`
3. Check port 5000 is not in use

### No Analytics Data
1. Ensure website is accessed through `http://localhost:5000`
2. Check browser console for JavaScript errors
3. Verify `/api/track` endpoint is responding

## Security Notes

- Database is stored locally (`analytics.db`)
- No sensitive data is transmitted externally
- Email uses secure SMTP with TLS
- IP addresses are stored for unique visitor counting

## Deployment

For production deployment:
1. Update `WEBSITE_URL` in `config.py`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Set up proper SSL certificates
4. Configure firewall rules
5. Set up automatic startup scripts

## Support

For issues or questions, check:
1. This README
2. Python error logs
3. Database file (`analytics.db`)
4. Email configuration

---

**Created for MNQOBI LISBON JEZA's Portfolio Website** 