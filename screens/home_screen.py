from kivy.uix.screenmanager import Screen
from kivy.app import App

class HomeScreen(Screen):
    """
    Home screen with navigation to devotee page and admin login.
    """
    
    def go_to_devotee_page(self):
        """Navigate to the devotee page."""
        app = App.get_running_app()
        app.root.current = 'devotee'
    
    def go_to_admin_login(self):
        """Navigate to the admin login page."""
        app = App.get_running_app()
        app.root.current = 'admin_login'
