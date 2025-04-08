import os
import sys
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.properties import ColorProperty, NumericProperty

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
    Window.clearcolor = (0.97, 0.97, 0.97, 1)  # Light gray background

# Modern UI styling embedded in the code
KV = '''
#:kivy 2.0.0
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import Window kivy.core.window.Window
#:import dp kivy.metrics.dp
#:import sp kivy.metrics.sp

# Define modern colors
#:set primary_color get_color_from_hex('#3F51B5')  # Indigo
#:set primary_light get_color_from_hex('#757de8')
#:set primary_dark get_color_from_hex('#002984')
#:set accent_color get_color_from_hex('#FF9800')  # Orange
#:set text_color get_color_from_hex('#212121')
#:set text_secondary get_color_from_hex('#757575')
#:set divider_color get_color_from_hex('#BDBDBD')
#:set bg_color get_color_from_hex('#FAFAFA')
#:set card_color get_color_from_hex('#FFFFFF')
#:set error_color get_color_from_hex('#F44336')
#:set success_color get_color_from_hex('#4CAF50')

# Style definitions
<Button>:
    background_normal: ''
    background_color: primary_color
    color: 1, 1, 1, 1
    size_hint_y: None
    height: dp(50)
    border_radius: [5, 5, 5, 5]
    font_size: sp(16)
    canvas.before:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [5, 5, 5, 5]
    
<Label>:
    color: text_color
    font_size: sp(16)
    
<TextInput>:
    background_normal: ''
    background_active: ''
    background_color: 0, 0, 0, 0
    foreground_color: text_color
    cursor_color: primary_color
    multiline: False
    size_hint_y: None
    height: dp(48)
    font_size: sp(16)
    padding: dp(15), dp(10)
    canvas.before:
        Color:
            rgba: divider_color
        Line:
            points: self.x, self.y, self.x + self.width, self.y
            width: 1
    canvas.after:
        Color:
            rgba: primary_color if self.focus else (0, 0, 0, 0)
        Line:
            points: self.x, self.y, self.x + self.width, self.y
            width: 2
            
<Card@BoxLayout>:
    orientation: 'vertical'
    padding: dp(15)
    spacing: dp(10)
    size_hint_y: None
    height: self.minimum_height
    canvas.before:
        Color:
            rgba: card_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(5), dp(5), dp(5), dp(5)]
        # Shadow (basic simulation)
        Color:
            rgba: 0, 0, 0, 0.05
        RoundedRectangle:
            pos: self.x + dp(2), self.y - dp(2)
            size: self.width, self.height
            radius: [dp(5), dp(5), dp(5), dp(5)]
            
<IconButton@Button>:
    icon: ''
    background_color: 0, 0, 0, 0
    color: primary_color
    font_name: 'Icons'  # We'll handle this in code for proper icons
    size_hint: None, None
    size: dp(48), dp(48)
    border_radius: [dp(24), dp(24), dp(24), dp(24)]
    
<NumPadButton@Button>:
    font_size: sp(24)
    border_radius: [dp(8), dp(8), dp(8), dp(8)]
    background_color: primary_light
    size_hint_y: None
    height: dp(60)
    
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: bg_color
            Rectangle:
                pos: self.pos
                size: self.size
        
        Label:
            text: 'Jain Temple'
            font_size: sp(28)
            size_hint_y: 0.1
            color: primary_color
            bold: True
            
        Label:
            text: 'Devotee Management System'
            font_size: sp(18)
            size_hint_y: 0.05
            color: text_secondary
            
        Image:
            source: 'generated-icon.png'  # Using the project icon instead of remote SVG
            size_hint_y: 0.3
            
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(20)
            size_hint_y: 0.55
            
            Button:
                text: 'Devotee Page'
                font_size: sp(18)
                on_release: root.go_to_devotee_page()
                background_color: primary_color
                
            Button:
                text: 'Admin Dashboard'
                font_size: sp(18)
                on_release: root.go_to_admin_login()
                background_color: accent_color

<AdminLoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: bg_color
            Rectangle:
                pos: self.pos
                size: self.size
        
        BoxLayout:
            size_hint_y: 0.1
            
            Label:
                text: 'Admin Login'
                font_size: sp(24)
                halign: 'left'
                color: primary_color
                bold: True
                size_hint_x: 0.7
                text_size: self.size
                valign: 'middle'
                    
            Button:
                text: 'Back'
                size_hint: 0.3, 1
                background_color: text_secondary
                on_release: root.go_back()
        
        Card:
            size_hint_y: 0.8
            
            Label:
                text: 'Username'
                halign: 'left'
                size_hint_y: None
                height: dp(30)
                text_size: self.size
                valign: 'bottom'
                    
            TextInput:
                id: username_input
                hint_text: 'Enter Username'
                    
            Label:
                text: 'Password'
                halign: 'left'
                size_hint_y: None
                height: dp(30)
                text_size: self.size
                valign: 'bottom'
                    
            TextInput:
                id: password_input
                password: True
                hint_text: 'Enter Password'
                    
            Label:
                id: error_label
                text: ''
                color: error_color
                size_hint_y: None
                height: dp(30)
                    
            Button:
                text: 'LOGIN'
                on_release: root.login()
                background_color: primary_color
                size_hint_y: None
                height: dp(50)

<DevoteeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(15)
        spacing: dp(15)
        canvas.before:
            Color:
                rgba: bg_color
            Rectangle:
                pos: self.pos
                size: self.size
        
        # App Bar
        BoxLayout:
            size_hint_y: 0.08
            canvas.before:
                Color:
                    rgba: primary_color
                Rectangle:
                    pos: self.pos
                    size: self.size
            
            Button:
                text: '≡'
                font_size: sp(24)
                size_hint_x: 0.15
                background_color: 0, 0, 0, 0
                on_release: root.show_menu()
                
            Label:
                text: 'Devotee Page'
                font_size: sp(20)
                color: 1, 1, 1, 1
                
            Button:
                text: 'Home'
                size_hint_x: 0.25
                background_color: primary_dark
                on_release: root.go_home()
        
        # Printer Status
        BoxLayout:
            size_hint_y: 0.05
            
            Label:
                id: printer_status
                text: 'Printer: Not Connected'
                color: error_color
                font_size: sp(14)
        
        # Devotee ID Input
        Card:
            size_hint_y: 0.15
            
            Label:
                text: 'Enter Devotee ID:'
                halign: 'left'
                size_hint_y: None
                height: dp(30)
                text_size: self.size
                valign: 'bottom'
                
            TextInput:
                id: devotee_id_input
                readonly: True
                font_size: sp(22)
                halign: 'center'
                size_hint_y: None
                height: dp(60)
        
        # Numeric Keypad
        Card:
            size_hint_y: 0.5
            
            GridLayout:
                cols: 3
                spacing: dp(8)
                padding: dp(5)
                size_hint_y: None
                height: self.minimum_height
                
                NumPadButton:
                    text: '1'
                    on_release: root.add_number('1')
                    
                NumPadButton:
                    text: '2'
                    on_release: root.add_number('2')
                    
                NumPadButton:
                    text: '3'
                    on_release: root.add_number('3')
                    
                NumPadButton:
                    text: '4'
                    on_release: root.add_number('4')
                    
                NumPadButton:
                    text: '5'
                    on_release: root.add_number('5')
                    
                NumPadButton:
                    text: '6'
                    on_release: root.add_number('6')
                    
                NumPadButton:
                    text: '7'
                    on_release: root.add_number('7')
                    
                NumPadButton:
                    text: '8'
                    on_release: root.add_number('8')
                    
                NumPadButton:
                    text: '9'
                    on_release: root.add_number('9')
                    
                Button:
                    text: 'Clear'
                    font_size: sp(16)
                    on_release: root.clear_input()
                    background_color: error_color
                    size_hint_y: None
                    height: dp(60)
                    
                NumPadButton:
                    text: '0'
                    on_release: root.add_number('0')
                    
                Button:
                    text: 'Del'
                    font_size: sp(16)
                    on_release: root.delete_last()
                    background_color: error_color
                    size_hint_y: None
                    height: dp(60)
        
        # Submit and Result
        Card:
            size_hint_y: 0.22
            
            Button:
                text: 'SUBMIT & PRINT'
                font_size: sp(20)
                background_color: success_color
                on_release: root.submit_and_print()
                size_hint_y: None
                height: dp(60)
                
            Label:
                id: selected_item_label
                text: ''
                font_size: sp(20)
                color: primary_color
                size_hint_y: None
                height: dp(50)
                halign: 'center'
                
            Label:
                id: error_label
                text: ''
                color: error_color
                font_size: sp(14)
                size_hint_y: None
                height: dp(30)
                halign: 'center'

<BluetoothPopup>:
    title: 'Connect to Printer'
    size_hint: 0.8, 0.8
    auto_dismiss: False
    
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        
        Label:
            text: 'Available Devices:'
            size_hint_y: 0.1
            
        ScrollView:
            size_hint_y: 0.7
            
            BoxLayout:
                id: devices_list
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(5)
        
        Button:
            text: 'Scan for Devices'
            size_hint_y: 0.1
            on_release: root.scan_devices()
            
        Button:
            text: 'Close'
            size_hint_y: 0.1
            on_release: root.dismiss()
'''

# Only load the embedded KV and not the separate KV file to avoid overlapping elements
Builder.load_string(KV)
print("Full KV file loaded successfully")

class ModernJainTempleApp(App):
    """
    Main application class for the modern Jain Temple app.
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
        # For testing purposes, we'll start at the home screen
        self.root.current = 'home'
        
        print("Using mock Bluetooth implementation for desktop testing")
    
    def on_stop(self):
        """Called when the application stops."""
        # Close database connection
        self.db.close_connection()
        
        # Disconnect bluetooth if connected
        if hasattr(self, 'bluetooth') and self.bluetooth.is_connected():
            self.bluetooth.disconnect()

if __name__ == '__main__':
    ModernJainTempleApp().run()