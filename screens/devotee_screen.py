from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import random
import datetime
from utils.item_selector import ItemSelector
from utils.printer import LabelPrinter

class BluetoothPopup(Popup):
    """Popup for connecting to Bluetooth printers."""
    
    def __init__(self, **kwargs):
        super(BluetoothPopup, self).__init__(**kwargs)
        self.app = App.get_running_app()
    
    def on_open(self):
        """Called when the popup is opened."""
        self.scan_devices()
    
    def scan_devices(self):
        """Scan for Bluetooth devices."""
        # Clear existing devices
        self.ids.devices_list.clear_widgets()
        
        # Add a loading indicator
        self.ids.devices_list.add_widget(Label(
            text='Scanning for devices...',
            size_hint_y=None,
            height='40dp'
        ))
        
        # Start scanning in separate thread to avoid blocking UI
        Clock.schedule_once(self._perform_scan, 0.1)
    
    def _perform_scan(self, dt):
        """Perform the actual Bluetooth scan."""
        self.ids.devices_list.clear_widgets()
        
        # Get available devices from Bluetooth manager
        devices = self.app.bluetooth.scan_for_devices()
        
        if not devices:
            self.ids.devices_list.add_widget(Label(
                text='No devices found',
                size_hint_y=None,
                height='40dp'
            ))
            return
        
        # Add buttons for each device
        for device in devices:
            device_name = device['name'] if device.get('name') else device['address']
            btn = Button(
                text=device_name,
                size_hint_y=None,
                height='50dp'
            )
            btn.device_address = device['address']
            btn.bind(on_release=self.connect_to_device)
            self.ids.devices_list.add_widget(btn)
    
    def connect_to_device(self, btn):
        """Connect to the selected device."""
        # Try to connect
        success = self.app.bluetooth.connect_to_device(btn.device_address)
        
        if success:
            # Update status on devotee screen
            devotee_screen = self.app.root.get_screen('devotee')
            devotee_screen.update_printer_status(True)
            self.dismiss()
        else:
            # Show error
            error_label = Label(
                text='Failed to connect to device',
                color=[1, 0, 0, 1],
                size_hint_y=None,
                height='40dp'
            )
            self.ids.devices_list.add_widget(error_label)
            
            # Remove error after 3 seconds
            Clock.schedule_once(lambda dt: self.ids.devices_list.remove_widget(error_label), 3)

class DevoteeScreen(Screen):
    """
    Screen for devotees to enter their ID and get a random item.
    """
    
    def __init__(self, **kwargs):
        super(DevoteeScreen, self).__init__(**kwargs)
        self.item_selector = ItemSelector()
        self.printer = LabelPrinter()
    
    def on_enter(self):
        """Called when the screen is entered."""
        app = App.get_running_app()
        if app.bluetooth.is_connected():
            self.update_printer_status(True)
        else:
            self.update_printer_status(False)
    
    def add_number(self, number):
        """Add a number to the devotee ID input."""
        current_text = self.ids.devotee_id_input.text
        self.ids.devotee_id_input.text = current_text + number
        
        # Clear any error message
        self.ids.error_label.text = ''
    
    def clear_input(self):
        """Clear the devotee ID input field."""
        self.ids.devotee_id_input.text = ''
        
        # Clear displayed item too
        self.ids.selected_item_label.text = ''
    
    def delete_last(self):
        """Delete the last character from the devotee ID input."""
        current_text = self.ids.devotee_id_input.text
        if current_text:
            self.ids.devotee_id_input.text = current_text[:-1]
    
    def show_menu(self):
        """Show the menu popup for Bluetooth connection."""
        popup = BluetoothPopup()
        popup.open()
    
    def update_printer_status(self, connected):
        """Update the printer connection status display."""
        if connected:
            self.ids.printer_status.text = 'Printer: Connected'
            self.ids.printer_status.color = [0.2, 0.8, 0.2, 1]  # Green
        else:
            self.ids.printer_status.text = 'Printer: Not Connected'
            self.ids.printer_status.color = [1, 0, 0, 1]  # Red
    
    def submit_and_print(self):
        """Process the devotee ID, select a random item, and print a label."""
        app = App.get_running_app()
        devotee_id = self.ids.devotee_id_input.text.strip()
        
        # Validate input
        if not devotee_id:
            self.ids.error_label.text = 'Please enter a devotee ID'
            return
        
        # Check if devotee exists
        devotee = app.db.get_devotee(devotee_id)
        if not devotee:
            self.ids.error_label.text = 'Devotee ID not found'
            return
        
        # Check printer connection
        if not app.bluetooth.is_connected():
            self.ids.error_label.text = 'Printer not connected'
            return
        
        # Select random item
        selected_item = self.item_selector.select_random_item()
        
        # Show the selected item with animation
        self.ids.selected_item_label.text = f"Selected: {selected_item}"
        
        # Record the visit in database
        app.db.record_visit(devotee_id, selected_item)
        
        # Get current date
        current_date = datetime.date.today().strftime("%d/%m/%Y")
        
        # Print the label
        print_data = {
            'devotee_id': devotee_id,
            'devotee_name': devotee[1],  # Name is at index 1
            'selected_item': selected_item,
            'date': current_date
        }
        
        success = self.printer.print_label(print_data)
        
        if not success:
            self.ids.error_label.text = 'Failed to print label'
    
    def go_home(self):
        """Navigate back to the home screen."""
        app = App.get_running_app()
        app.root.current = 'home'
