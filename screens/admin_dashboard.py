from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class AdminDashboardScreen(Screen):
    """
    Admin dashboard screen with various administrative functions.
    """
    
    def open_reports(self):
        """Navigate to reports screen."""
        app = App.get_running_app()
        app.root.current = 'reports'
    
    def open_calendar(self):
        """Navigate to calendar view screen."""
        app = App.get_running_app()
        app.root.current = 'calendar_view'
    
    def add_devotee(self):
        """Navigate to add devotee screen."""
        app = App.get_running_app()
        app.root.current = 'add_devotee'
    
    def view_devotees(self):
        """Display a list of all devotees."""
        app = App.get_running_app()
        devotees = app.db.get_all_devotees()
        
        # Create popup to show devotee list
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Add title
        content.add_widget(Label(
            text='Devotee List',
            font_size='20sp',
            size_hint_y=None,
            height='40dp'
        ))
        
        # Create scrollable list
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.gridlayout import GridLayout
        
        scroll = ScrollView(size_hint=(1, 0.8))
        grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        # Add devotees to the list
        if devotees:
            for devotee in devotees:
                # Create a row for each devotee
                row = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height='50dp'
                )
                
                # Add devotee info
                info_text = f"ID: {devotee[0]} - {devotee[1]}"
                if devotee[2]:  # If phone exists
                    info_text += f" - {devotee[2]}"
                
                row.add_widget(Label(text=info_text, size_hint_x=0.7))
                
                # Add edit button
                edit_btn = Button(
                    text='Edit',
                    size_hint_x=0.15
                )
                devotee_id = devotee[0]
                edit_btn.bind(on_release=lambda btn, id=devotee_id: self.edit_devotee(id))
                row.add_widget(edit_btn)
                
                # Add delete button
                delete_btn = Button(
                    text='Delete',
                    size_hint_x=0.15,
                    background_color=[0.8, 0.2, 0.2, 1]
                )
                delete_btn.bind(on_release=lambda btn, id=devotee_id: self.confirm_delete_devotee(id))
                row.add_widget(delete_btn)
                
                grid.add_widget(row)
        else:
            grid.add_widget(Label(
                text='No devotees found',
                size_hint_y=None,
                height='50dp'
            ))
        
        scroll.add_widget(grid)
        content.add_widget(scroll)
        
        # Add close button
        close_btn = Button(
            text='Close',
            size_hint_y=None,
            height='50dp'
        )
        
        content.add_widget(close_btn)
        
        # Create and show popup
        popup = Popup(
            title='Devotee Management',
            content=content,
            size_hint=(0.9, 0.9),
            auto_dismiss=False
        )
        
        close_btn.bind(on_release=popup.dismiss)
        popup.open()
    
    def edit_devotee(self, devotee_id):
        """Open a popup to edit devotee details."""
        app = App.get_running_app()
        devotee = app.db.get_devotee(devotee_id)
        
        if not devotee:
            return
        
        # Create popup content
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Add title
        content.add_widget(Label(
            text=f'Edit Devotee: {devotee[1]}',
            font_size='18sp',
            size_hint_y=None,
            height='40dp'
        ))
        
        # Create form fields
        from kivy.uix.textinput import TextInput
        
        # ID (read-only)
        content.add_widget(Label(text=f'Devotee ID: {devotee[0]}', halign='left', size_hint_y=None, height='30dp'))
        
        # Name
        content.add_widget(Label(text='Name:', halign='left', size_hint_y=None, height='30dp'))
        name_input = TextInput(
            text=devotee[1],
            multiline=False,
            size_hint_y=None,
            height='40dp'
        )
        content.add_widget(name_input)
        
        # Phone
        content.add_widget(Label(text='Phone:', halign='left', size_hint_y=None, height='30dp'))
        phone_input = TextInput(
            text=devotee[2] if devotee[2] else '',
            multiline=False,
            size_hint_y=None,
            height='40dp'
        )
        content.add_widget(phone_input)
        
        # Email
        content.add_widget(Label(text='Email:', halign='left', size_hint_y=None, height='30dp'))
        email_input = TextInput(
            text=devotee[3] if devotee[3] else '',
            multiline=False,
            size_hint_y=None,
            height='40dp'
        )
        content.add_widget(email_input)
        
        # Address
        content.add_widget(Label(text='Address:', halign='left', size_hint_y=None, height='30dp'))
        address_input = TextInput(
            text=devotee[4] if devotee[4] else '',
            multiline=True,
            size_hint_y=None,
            height='80dp'
        )
        content.add_widget(address_input)
        
        # Error label
        error_label = Label(
            text='',
            color=[1, 0, 0, 1],
            size_hint_y=None,
            height='30dp'
        )
        content.add_widget(error_label)
        
        # Add buttons
        buttons = BoxLayout(size_hint_y=None, height='50dp', spacing=10)
        
        cancel_btn = Button(text='Cancel')
        save_btn = Button(text='Save', background_color=[0.2, 0.7, 0.3, 1])
        
        buttons.add_widget(cancel_btn)
        buttons.add_widget(save_btn)
        content.add_widget(buttons)
        
        # Create popup
        popup = Popup(
            title='Edit Devotee',
            content=content,
            size_hint=(0.9, 0.9),
            auto_dismiss=False
        )
        
        # Bind buttons
        cancel_btn.bind(on_release=popup.dismiss)
        
        def save_devotee(btn):
            """Save updated devotee information."""
            # Validate
            if not name_input.text.strip():
                error_label.text = 'Name is required'
                return
            
            # Update devotee
            success = app.db.update_devotee(
                devotee_id,
                name_input.text.strip(),
                phone_input.text.strip(),
                email_input.text.strip(),
                address_input.text.strip()
            )
            
            if success:
                popup.dismiss()
                # Refresh the devotee list
                self.view_devotees()
            else:
                error_label.text = 'Failed to update devotee'
        
        save_btn.bind(on_release=save_devotee)
        
        # Show popup
        popup.open()
    
    def confirm_delete_devotee(self, devotee_id):
        """Show confirmation dialog before deleting a devotee."""
        app = App.get_running_app()
        devotee = app.db.get_devotee(devotee_id)
        
        if not devotee:
            return
        
        # Create confirmation dialog
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Add warning message
        content.add_widget(Label(
            text=f'Are you sure you want to delete devotee:\n{devotee[1]} (ID: {devotee[0]})?',
            halign='center'
        ))
        
        # Add note about data loss
        content.add_widget(Label(
            text='This will delete all visit history for this devotee.\nThis action cannot be undone.',
            color=[1, 0, 0, 1],
            halign='center',
            font_size='14sp'
        ))
        
        # Add buttons
        buttons = BoxLayout(size_hint_y=None, height='50dp', spacing=10)
        
        cancel_btn = Button(text='Cancel')
        delete_btn = Button(
            text='Delete',
            background_color=[0.8, 0.2, 0.2, 1]
        )
        
        buttons.add_widget(cancel_btn)
        buttons.add_widget(delete_btn)
        content.add_widget(buttons)
        
        # Create popup
        popup = Popup(
            title='Confirm Deletion',
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        
        # Bind buttons
        cancel_btn.bind(on_release=popup.dismiss)
        
        def perform_delete(btn):
            """Delete the devotee."""
            success = app.db.delete_devotee(devotee_id)
            popup.dismiss()
            
            # Refresh the devotee list
            if success:
                self.view_devotees()
        
        delete_btn.bind(on_release=perform_delete)
        
        # Show popup
        popup.open()
    
    def backup_data(self):
        """Create a backup of the database."""
        # This would typically export the database to an external file
        # For simplicity, we'll just show a success message
        
        content = BoxLayout(orientation='vertical', padding=10)
        
        message = Label(
            text='Data backup functionality will be implemented\nbased on client requirements.',
            halign='center'
        )
        content.add_widget(message)
        
        close_btn = Button(
            text='Close',
            size_hint_y=None,
            height='50dp'
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title='Backup Data',
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        
        close_btn.bind(on_release=popup.dismiss)
        popup.open()
    
    def open_settings(self):
        """Open application settings."""
        # This would be implemented based on client requirements
        content = BoxLayout(orientation='vertical', padding=10)
        
        message = Label(
            text='Settings functionality will be implemented\nbased on client requirements.',
            halign='center'
        )
        content.add_widget(message)
        
        close_btn = Button(
            text='Close',
            size_hint_y=None,
            height='50dp'
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title='Settings',
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        
        close_btn.bind(on_release=popup.dismiss)
        popup.open()
    
    def logout(self):
        """Log out and go back to home screen."""
        app = App.get_running_app()
        app.root.current = 'home'
    
    def go_back(self):
        """Go back to devotee screen."""
        app = App.get_running_app()
        app.root.current = 'devotee'
