import sqlite3
import os
import datetime
from pathlib import Path

class DatabaseHandler:
    """
    Handles all database operations for the Jain Temple app.
    """
    def __init__(self):
        # Determine the database file path
        if os.path.exists('/storage/emulated/0/'):
            # Android path
            db_dir = '/storage/emulated/0/JainTempleApp'
            os.makedirs(db_dir, exist_ok=True)
            self.db_path = os.path.join(db_dir, 'jaintemple.db')
        else:
            # Default path for other platforms
            db_dir = os.path.join(os.path.expanduser('~'), 'JainTempleApp')
            os.makedirs(db_dir, exist_ok=True)
            self.db_path = os.path.join(db_dir, 'jaintemple.db')
        
        self.conn = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """Establish a database connection."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
    
    def setup_database(self):
        """Set up the database schema if it doesn't exist."""
        try:
            # Create admins table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Create devotees table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS devotees (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Create visits table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                devotee_id TEXT NOT NULL,
                visit_date DATE NOT NULL,
                selected_item TEXT NOT NULL,
                FOREIGN KEY (devotee_id) REFERENCES devotees (id)
            )
            ''')
            
            # Create settings table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            ''')
            
            # Create items table for the 18 items
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
            ''')
            
            # Insert default admin if none exists
            self.cursor.execute("SELECT COUNT(*) FROM admins")
            count = self.cursor.fetchone()[0]
            if count == 0:
                self.cursor.execute(
                    "INSERT INTO admins (username, password) VALUES (?, ?)",
                    ("admin", "admin123")  # Default credentials
                )
            
            # Insert app activation status if it doesn't exist
            self.cursor.execute("SELECT COUNT(*) FROM settings WHERE key = 'app_activated'")
            count = self.cursor.fetchone()[0]
            if count == 0:
                self.cursor.execute(
                    "INSERT INTO settings (key, value) VALUES (?, ?)",
                    ("app_activated", "0")  # 0 means not activated
                )
            
            # Insert default items if none exist
            self.cursor.execute("SELECT COUNT(*) FROM items")
            count = self.cursor.fetchone()[0]
            if count == 0:
                items = [
                    "Swamivatsalya", "Sadavrata", "Jñāna Dāna", "Auṣadha Dāna", 
                    "Abhaya Dāna", "Vaiyāvṛttya", "Jinālaya Jīrṇoddhāra", "Pratimā",
                    "Pūjā", "Upavāsa", "Santhārā", "Saṃyama", "Tapasya", 
                    "Tyāga", "Brahmacārya", "Kṣamā", "Ahiṃsā", "Satya"
                ]
                for item in items:
                    self.cursor.execute(
                        "INSERT INTO items (name, description) VALUES (?, ?)",
                        (item, f"Description for {item}")
                    )
            
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database setup error: {e}")
    
    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
    
    def is_app_activated(self):
        """Check if the app is activated."""
        try:
            self.cursor.execute("SELECT value FROM settings WHERE key = 'app_activated'")
            result = self.cursor.fetchone()
            return result[0] == "1" if result else False
        except sqlite3.Error as e:
            print(f"Error checking app activation: {e}")
            return False
    
    def activate_app(self):
        """Activate the app."""
        try:
            self.cursor.execute("UPDATE settings SET value = '1' WHERE key = 'app_activated'")
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error activating app: {e}")
            return False
    
    def verify_admin(self, username, password):
        """Verify admin credentials."""
        try:
            self.cursor.execute(
                "SELECT id FROM admins WHERE username = ? AND password = ?",
                (username, password)
            )
            result = self.cursor.fetchone()
            return result is not None
        except sqlite3.Error as e:
            print(f"Admin verification error: {e}")
            return False
    
    def add_devotee(self, devotee_id, name, phone="", email="", address=""):
        """Add a new devotee to the database."""
        try:
            self.cursor.execute(
                "INSERT INTO devotees (id, name, phone, email, address) VALUES (?, ?, ?, ?, ?)",
                (devotee_id, name, phone, email, address)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding devotee: {e}")
            return False
    
    def get_devotee(self, devotee_id):
        """Get devotee details by ID."""
        try:
            self.cursor.execute(
                "SELECT * FROM devotees WHERE id = ?",
                (devotee_id,)
            )
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting devotee: {e}")
            return None
    
    def get_all_devotees(self):
        """Get all devotees."""
        try:
            self.cursor.execute("SELECT * FROM devotees ORDER BY name")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting all devotees: {e}")
            return []
    
    def update_devotee(self, devotee_id, name, phone, email, address):
        """Update devotee information."""
        try:
            self.cursor.execute(
                "UPDATE devotees SET name = ?, phone = ?, email = ?, address = ? WHERE id = ?",
                (name, phone, email, address, devotee_id)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating devotee: {e}")
            return False
    
    def delete_devotee(self, devotee_id):
        """Delete a devotee."""
        try:
            self.cursor.execute("DELETE FROM devotees WHERE id = ?", (devotee_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting devotee: {e}")
            return False
    
    def record_visit(self, devotee_id, selected_item):
        """Record a devotee's visit with the selected item."""
        try:
            today = datetime.date.today().isoformat()
            self.cursor.execute(
                "INSERT INTO visits (devotee_id, visit_date, selected_item) VALUES (?, ?, ?)",
                (devotee_id, today, selected_item)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error recording visit: {e}")
            return False
    
    def get_all_items(self):
        """Get all items for random selection."""
        try:
            self.cursor.execute("SELECT name FROM items")
            items = self.cursor.fetchall()
            return [item[0] for item in items]
        except sqlite3.Error as e:
            print(f"Error getting items: {e}")
            return []
    
    def get_daily_visits(self, date):
        """Get all visits for a specific date."""
        try:
            self.cursor.execute(
                """
                SELECT v.id, v.devotee_id, d.name, v.selected_item 
                FROM visits v
                JOIN devotees d ON v.devotee_id = d.id
                WHERE v.visit_date = ?
                ORDER BY v.id DESC
                """,
                (date,)
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting daily visits: {e}")
            return []
    
    def get_monthly_visits(self, year, month):
        """Get all visits for a specific month."""
        try:
            # Convert month to 1-12 format if needed
            month_num = month if isinstance(month, int) else {
                'January': 1, 'February': 2, 'March': 3, 'April': 4,
                'May': 5, 'June': 6, 'July': 7, 'August': 8,
                'September': 9, 'October': 10, 'November': 11, 'December': 12
            }.get(month, 1)
            
            # Create date range for the month
            if month_num < 10:
                month_str = f"0{month_num}"
            else:
                month_str = str(month_num)
            
            date_pattern = f"{year}-{month_str}-%"
            
            self.cursor.execute(
                """
                SELECT v.visit_date, COUNT(*) as visit_count
                FROM visits v
                WHERE v.visit_date LIKE ?
                GROUP BY v.visit_date
                ORDER BY v.visit_date
                """,
                (date_pattern,)
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting monthly visits: {e}")
            return []
    
    def get_yearly_visits(self, year):
        """Get visit statistics for a specific year."""
        try:
            date_pattern = f"{year}-%"
            
            self.cursor.execute(
                """
                SELECT strftime('%m', v.visit_date) as month, COUNT(*) as visit_count
                FROM visits v
                WHERE v.visit_date LIKE ?
                GROUP BY month
                ORDER BY month
                """,
                (date_pattern,)
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting yearly visits: {e}")
            return []
    
    def get_devotee_visits(self, devotee_id):
        """Get all visits for a specific devotee."""
        try:
            self.cursor.execute(
                """
                SELECT v.visit_date, v.selected_item
                FROM visits v
                WHERE v.devotee_id = ?
                ORDER BY v.visit_date DESC
                """,
                (devotee_id,)
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting devotee visits: {e}")
            return []
    
    def get_attendance_calendar(self, devotee_id, year, month):
        """Get attendance data for calendar view."""
        try:
            # Convert month to 1-12 format if needed
            month_num = month if isinstance(month, int) else {
                'January': 1, 'February': 2, 'March': 3, 'April': 4,
                'May': 5, 'June': 6, 'July': 7, 'August': 8,
                'September': 9, 'October': 10, 'November': 11, 'December': 12
            }.get(month, 1)
            
            # Create date range for the month
            if month_num < 10:
                month_str = f"0{month_num}"
            else:
                month_str = str(month_num)
            
            date_pattern = f"{year}-{month_str}-%"
            
            self.cursor.execute(
                """
                SELECT v.visit_date
                FROM visits v
                WHERE v.devotee_id = ? AND v.visit_date LIKE ?
                ORDER BY v.visit_date
                """,
                (devotee_id, date_pattern)
            )
            
            # Convert to list of attendance dates
            results = self.cursor.fetchall()
            return [row[0] for row in results]
        except sqlite3.Error as e:
            print(f"Error getting attendance calendar: {e}")
            return []
