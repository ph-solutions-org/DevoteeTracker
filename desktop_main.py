import os
import sys
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock

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

# Load KV directly as a string instead of from a file
# This is more reliable for desktop testing
KV = '''
#:kivy 2.0.0

<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        
        Label:
            text: 'Jain Temple\\nDevotee Management System'
            font_size: '24sp'
            halign: 'center'
            size_hint_y: 0.3
            
        BoxLayout:
            orientation: 'vertical'
            spacing: 20
            size_hint_y: 0.7
            
            Button:
                text: 'Devotee Page'
                font_size: '20sp'
                on_release: root.go_to_devotee_page()
                background_color: 0.2, 0.6, 1, 1
                
            Button:
                text: 'Admin Dashboard'
                font_size: '20sp'
                on_release: root.go_to_admin_login()
                background_color: 0.8, 0.2, 0.2, 1
'''

# Load the KV string
Builder.load_string(KV)

# Then try to load the full KV file, but don't fail if it doesn't work
try:
    kv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jainapp.kv')
    if os.path.exists(kv_path):
        Builder.load_file(kv_path)
        print(f"Full KV file loaded successfully")
    else:
        print("Using embedded KV definitions only")
except Exception as e:
    print(f"Using embedded KV definitions only, error loading full KV: {e}")

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