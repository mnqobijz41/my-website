import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'analytics.db')

    # Email Configuration
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'mnqobijz41@gmail.com')
    SENDER_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', 'mnqobijz41@gmail.com')

    # Website Info
    WEBSITE_NAME = 'MNQOBI LISBON JEZA Portfolio'
    WEBSITE_URL = os.getenv('WEBSITE_URL', 'https://mnqobijz41.github.io/my-website')

    # Analytics Settings
    TRACK_PAGE_VIEWS = True
    MONTHLY_REPORT_ENABLED = True