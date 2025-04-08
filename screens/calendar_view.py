from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
import calendar
import datetime

class CalendarViewScreen(Screen):
    """
    Screen for viewing devotee attendance in a calendar format.
    """
    
    def on_enter(self):
        """Called when the screen is entered."""
        app = App.get_running_app()
        
        # Populate devotee spinner
        devotees = app.db.get_all_devotees()
        if devotees:
            devotee_values = [f"{d[0]} - {d[1]}" for d in devotees]
            self.ids.devotee_spinner.values = devotee_values
            self.ids.devotee_spinner.text = devotee_values[0]
        else:
            self.ids.devotee_spinner.values = ['No devotees found']
            self.ids.devotee_spinner.text = 'No devotees found'
        
        # Set default month and year
        now = datetime.datetime.now()
        self.ids.month_spinner.text = calendar.month_name[now.month]
        self.ids.year_spinner.text = str(now.year)
        
        # Update calendar
        self.update_calendar()
    
    def select_devotee(self, devotee_text):
        """Called when a devotee is selected from the spinner."""
        if devotee_text != 'No devotees found':
            self.update_calendar()
    
    def update_calendar(self):
        """Update the calendar grid with attendance data."""
        # Clear the calendar grid
        self.ids.calendar_grid.clear_widgets()
        
        # Get current selections
        devotee_text = self.ids.devotee_spinner.text
        month_text = self.ids.month_spinner.text
        year_text = self.ids.year_spinner.text
        
        if devotee_text == 'No devotees found':
            return
        
        # Extract devotee ID
        devotee_id = devotee_text.split(' - ')[0]
        
        # Convert month name to number
        month_names = {name: num for num, name in enumerate(calendar.month_name) if num}
        month_num = month_names.get(month_text, 1)  # Default to January if not found
        
        # Convert year to int
        year_num = int(year_text)
        
        # Get calendar for month
        cal = calendar.monthcalendar(year_num, month_num)
        
        # Get attendance data
        app = App.get_running_app()
        attendance_dates = app.db.get_attendance_calendar(devotee_id, year_text, month_text)
        
        # Convert to datetime objects for easy comparison
        attendance_set = set()
        for date_str in attendance_dates:
            attendance_set.add(date_str)
        
        # Populate calendar grid
        for week in cal:
            for day in week:
                if day == 0:
                    # Empty day (padding at start/end of month)
                    self.ids.calendar_grid.add_widget(Label(text=''))
                else:
                    # Format date to match database format (YYYY-MM-DD)
                    if month_num < 10:
                        month_str = f"0{month_num}"
                    else:
                        month_str = str(month_num)
                    
                    if day < 10:
                        day_str = f"0{day}"
                    else:
                        day_str = str(day)
                    
                    date_str = f"{year_num}-{month_str}-{day_str}"
                    
                    # Check if devotee was present on this day
                    is_present = date_str in attendance_set
                    
                    # Create day button with appropriate color
                    day_btn = Button(text=str(day))
                    
                    if is_present:
                        # Green for present
                        day_btn.background_color = [0.2, 0.8, 0.2, 1]
                    else:
                        # Red for absent or default
                        day_btn.background_color = [0.8, 0.2, 0.2, 1]
                    
                    self.ids.calendar_grid.add_widget(day_btn)
    
    def go_back(self):
        """Navigate back to admin dashboard."""
        app = App.get_running_app()
        app.root.current = 'admin_dashboard'
