import sqlite3
import datetime
from config import Config

class AnalyticsDB:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create page_views table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS page_views (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_name TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create monthly_stats table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER NOT NULL,
                month INTEGER NOT NULL,
                total_views INTEGER DEFAULT 0,
                unique_visitors INTEGER DEFAULT 0,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(year, month)
            )
        ''')
        
        # Create analytics_setup table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics_setup (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setup_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                setup_complete BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def record_page_view(self, page_name, ip_address=None, user_agent=None):
        """Record a page view"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO page_views (page_name, ip_address, user_agent)
            VALUES (?, ?, ?)
        ''', (page_name, ip_address, user_agent))
        
        conn.commit()
        conn.close()
    
    def get_monthly_stats(self, year, month):
        """Get statistics for a specific month"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT total_views, unique_visitors
            FROM monthly_stats
            WHERE year = ? AND month = ?
        ''', (year, month))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {'total_views': result[0], 'unique_visitors': result[1]}
        return {'total_views': 0, 'unique_visitors': 0}
    
    def calculate_monthly_stats(self, year, month):
        """Calculate and store monthly statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get total views for the month
        cursor.execute('''
            SELECT COUNT(*) as total_views,
                   COUNT(DISTINCT ip_address) as unique_visitors
            FROM page_views
            WHERE strftime('%Y', timestamp) = ? AND strftime('%m', timestamp) = ?
        ''', (str(year), f'{month:02d}'))
        
        result = cursor.fetchone()
        total_views = result[0] if result else 0
        unique_visitors = result[1] if result else 0
        
        # Insert or update monthly stats
        cursor.execute('''
            INSERT OR REPLACE INTO monthly_stats (year, month, total_views, unique_visitors, last_updated)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (year, month, total_views, unique_visitors))
        
        conn.commit()
        conn.close()
        
        return {'total_views': total_views, 'unique_visitors': unique_visitors}
    
    def mark_setup_complete(self):
        """Mark analytics setup as complete"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO analytics_setup (id, setup_complete)
            VALUES (1, TRUE)
        ''')
        
        conn.commit()
        conn.close()
    
    def is_setup_complete(self):
        """Check if analytics setup is complete"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT setup_complete FROM analytics_setup WHERE id = 1')
        result = cursor.fetchone()
        
        conn.close()
        
        return result and result[0] 