import os
import sys
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock
from kivy.resources import resource_add_path

# Add the current directory to resource path
resource_add_path(os.path.dirname(os.path.abspath(__file__)))

# Import screens
from screens.home_screen import HomeScreen
from screens.devotee_screen import DevoteeScreen
from screens.admin_login import AdminLoginScreen
from screens.admin_dashboard import AdminDashboardScreen
from screens.add_devotee import AddDevoteeScreen
from screens.reports import ReportsScreen
from screens.calendar_view import CalendarViewScreen

# Import utilities
from utils.bluetooth_manager import BluetoothManager
from utils.authentication import Authentication
from database.db_handler import DatabaseHandler

# Set window size for desktop testing
if platform not in ('android', 'ios'):
    Window.size = (400, 700)
    Window.clearcolor = (0.95, 0.95, 0.95, 1)  # Light gray background
    
# Load the KV file explicitly
try:
    # First try absolute path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    kv_path = os.path.join(current_dir, 'jainapp.kv')
    Builder.load_file(kv_path)
    print(f"KV file loaded successfully from: {kv_path}")
except Exception as e:
    try:
        # Try direct file loading
        Builder.load_file('jainapp.kv')
        print("KV file loaded successfully from current directory")
    except Exception as e2:
        print(f"Failed to load KV file: {e2}")
        print("Current directory:", os.getcwd())
        print("Files in directory:", os.listdir())

class JainTempleApp(App):
    """
    Main application class for the Jain Temple app.
    """
    def build(self):
        # Initialize database
        self.db = DatabaseHandler()
        self.db.setup_database()
        
        # Initialize authentication system
        self.auth = Authentication(self.db)
        
        # Initialize bluetooth manager
        self.bluetooth = BluetoothManager()
        
        # Create screen manager
        self.sm = ScreenManager(transition=SlideTransition())
        
        # Add screens
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(AdminLoginScreen(name='admin_login'))
        self.sm.add_widget(DevoteeScreen(name='devotee'))
        self.sm.add_widget(AdminDashboardScreen(name='admin_dashboard'))
        self.sm.add_widget(AddDevoteeScreen(name='add_devotee'))
        self.sm.add_widget(ReportsScreen(name='reports'))
        self.sm.add_widget(CalendarViewScreen(name='calendar_view'))
        
        return self.sm
    
    def on_start(self):
        """Called when the application starts."""
        # Check if app is already activated
        if self.db.is_app_activated():
            self.root.current = 'home'
        else:
            self.root.current = 'admin_login'
    
    def on_stop(self):
        """Called when the application stops."""
        # Close database connection
        self.db.close_connection()
        
        # Disconnect bluetooth if connected
        if hasattr(self, 'bluetooth') and self.bluetooth.is_connected():
            self.bluetooth.disconnect()

if __name__ == '__main__':
    JainTempleApp().run()
