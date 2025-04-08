from kivy.uix.screenmanager import Screen
from kivy.app import App

class AddDevoteeScreen(Screen):
    """
    Screen for adding new devotees to the system.
    """
    
    def save_devotee(self):
        """Save the new devotee to the database."""
        app = App.get_running_app()
        
        # Get input values
        devotee_id = self.ids.devotee_id_input.text.strip()
        name = self.ids.name_input.text.strip()
        phone = self.ids.phone_input.text.strip()
        email = self.ids.email_input.text.strip()
        address = self.ids.address_input.text.strip()
        
        # Validate required fields
        if not devotee_id:
            self.ids.error_label.text = 'Devotee ID is required'
            return
            
        if not name:
            self.ids.error_label.text = 'Name is required'
            return
        
        # Check if ID already exists
        existing_devotee = app.db.get_devotee(devotee_id)
        if existing_devotee:
            self.ids.error_label.text = f'Devotee ID {devotee_id} already exists'
            return
        
        # Save devotee
        success = app.db.add_devotee(devotee_id, name, phone, email, address)
        
        if success:
            # Clear form
            self.ids.devotee_id_input.text = ''
            self.ids.name_input.text = ''
            self.ids.phone_input.text = ''
            self.ids.email_input.text = ''
            self.ids.address_input.text = ''
            
            # Show success message
            self.ids.error_label.text = 'Devotee added successfully'
            self.ids.error_label.color = [0.2, 0.8, 0.2, 1]  # Green
        else:
            self.ids.error_label.text = 'Failed to add devotee'
            self.ids.error_label.color = [1, 0, 0, 1]  # Red
    
    def go_back(self):
        """Navigate back to admin dashboard."""
        app = App.get_running_app()
        app.root.current = 'admin_dashboard'
