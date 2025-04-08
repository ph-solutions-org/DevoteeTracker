from kivy.uix.screenmanager import Screen
from kivy.app import App

class AdminLoginScreen(Screen):
    """
    Admin login screen for authentication.
    """
    
    def login(self):
        """Authenticate admin login."""
        app = App.get_running_app()
        username = self.ids.username_input.text.strip()
        password = self.ids.password_input.text.strip()
        
        # Validate input
        if not username or not password:
            self.ids.error_label.text = 'Please enter both username and password'
            return
        
        # Verify credentials
        if app.auth.verify_credentials(username, password):
            # Check if app is already activated
            if app.db.is_app_activated():
                # Navigate to admin dashboard
                app.root.current = 'admin_dashboard'
            else:
                # Activate the app and navigate to home screen
                app.db.activate_app()
                app.root.current = 'home'
        else:
            self.ids.error_label.text = 'Invalid username or password'
    
    def go_back(self):
        """Navigate back to the home screen."""
        app = App.get_running_app()
        # Check if app is activated
        if app.db.is_app_activated():
            app.root.current = 'home'
