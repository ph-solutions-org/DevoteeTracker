from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
import datetime

class ReportsScreen(Screen):
    """
    Screen for viewing various reports about temple visits.
    """
    
    def on_enter(self):
        """Called when the screen is entered."""
        # Initialize report type spinner values
        self.ids.report_type.text = 'Select Report Type'
        
        # Default to Daily report
        self.change_report_type('Daily')
    
    def change_report_type(self, report_type):
        """Change the type of report to display."""
        # Clear current report
        self.ids.report_data.clear_widgets()
        self.ids.report_title.text = f'{report_type} Report'
        
        # Update filter spinner based on report type
        if report_type == 'Daily':
            # Last 7 days
            today = datetime.date.today()
            dates = [(today - datetime.timedelta(days=i)).isoformat() 
                    for i in range(7)]
            self.ids.filter_spinner.values = dates
            self.ids.filter_spinner.text = dates[0]  # Today
            
        elif report_type == 'Monthly':
            # Last 12 months
            months = ['January', 'February', 'March', 'April', 'May', 'June',
                     'July', 'August', 'September', 'October', 'November', 'December']
            current_month = datetime.date.today().month - 1  # 0-indexed
            ordered_months = months[current_month:] + months[:current_month]
            self.ids.filter_spinner.values = ordered_months
            self.ids.filter_spinner.text = months[current_month]  # Current month
            
        elif report_type == 'Yearly':
            # Last 3 years
            current_year = datetime.date.today().year
            years = [str(current_year - i) for i in range(3)]
            self.ids.filter_spinner.values = years
            self.ids.filter_spinner.text = str(current_year)  # Current year
            
        elif report_type == 'Devotee-wise':
            # Get all devotees
            app = App.get_running_app()
            devotees = app.db.get_all_devotees()
            if devotees:
                devotee_values = [f"{d[0]} - {d[1]}" for d in devotees]
                self.ids.filter_spinner.values = devotee_values
                self.ids.filter_spinner.text = devotee_values[0]
            else:
                self.ids.filter_spinner.values = ['No devotees found']
                self.ids.filter_spinner.text = 'No devotees found'
        
        # Load report data
        self.apply_filter(self.ids.filter_spinner.text)
    
    def apply_filter(self, filter_value):
        """Apply the selected filter and display the report."""
        # Clear existing report data
        self.ids.report_data.clear_widgets()
        
        app = App.get_running_app()
        report_type = self.ids.report_type.text
        
        if report_type == 'Daily':
            # Get visits for selected date
            visits = app.db.get_daily_visits(filter_value)
            
            # Create header
            header = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height='40dp',
                spacing=5
            )
            header.add_widget(Label(text='Devotee ID', size_hint_x=0.25))
            header.add_widget(Label(text='Name', size_hint_x=0.4))
            header.add_widget(Label(text='Selected Item', size_hint_x=0.35))
            self.ids.report_data.add_widget(header)
            
            # Add separator
            self.ids.report_data.add_widget(BoxLayout(
                size_hint_y=None,
                height='1dp',
                background_color=[0.5, 0.5, 0.5, 1]
            ))
            
            # Add visits
            if visits:
                for visit in visits:
                    row = BoxLayout(
                        orientation='horizontal',
                        size_hint_y=None,
                        height='40dp',
                        spacing=5
                    )
                    row.add_widget(Label(text=str(visit[1]), size_hint_x=0.25))  # Devotee ID
                    row.add_widget(Label(text=str(visit[2]), size_hint_x=0.4))   # Name
                    row.add_widget(Label(text=str(visit[3]), size_hint_x=0.35))  # Selected Item
                    self.ids.report_data.add_widget(row)
            else:
                self.ids.report_data.add_widget(Label(
                    text='No visits found for this date',
                    size_hint_y=None,
                    height='40dp'
                ))
            
            # Update title with count
            visit_count = len(visits)
            self.ids.report_title.text = f'Daily Report: {filter_value} - {visit_count} visits'
            
        elif report_type == 'Monthly':
            # Get current year
            current_year = datetime.date.today().year
            
            # Get visits for selected month
            visits = app.db.get_monthly_visits(current_year, filter_value)
            
            # Create header
            header = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height='40dp',
                spacing=5
            )
            header.add_widget(Label(text='Date', size_hint_x=0.7))
            header.add_widget(Label(text='Visit Count', size_hint_x=0.3))
            self.ids.report_data.add_widget(header)
            
            # Add separator
            self.ids.report_data.add_widget(BoxLayout(
                size_hint_y=None,
                height='1dp',
                background_color=[0.5, 0.5, 0.5, 1]
            ))
            
            # Add visits
            total_visits = 0
            if visits:
                for visit in visits:
                    row = BoxLayout(
                        orientation='horizontal',
                        size_hint_y=None,
                        height='40dp',
                        spacing=5
                    )
                    row.add_widget(Label(text=str(visit[0]), size_hint_x=0.7))      # Date
                    row.add_widget(Label(text=str(visit[1]), size_hint_x=0.3))      # Visit count
                    self.ids.report_data.add_widget(row)
                    total_visits += visit[1]
            else:
                self.ids.report_data.add_widget(Label(
                    text='No visits found for this month',
                    size_hint_y=None,
                    height='40dp'
                ))
            
            # Update title with count
            self.ids.report_title.text = f'Monthly Report: {filter_value} {current_year} - {total_visits} visits'
            
        elif report_type == 'Yearly':
            # Get visits for selected year
            visits = app.db.get_yearly_visits(filter_value)
            
            # Create header
            header = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height='40dp',
                spacing=5
            )
            header.add_widget(Label(text='Month', size_hint_x=0.7))
            header.add_widget(Label(text='Visit Count', size_hint_x=0.3))
            self.ids.report_data.add_widget(header)
            
            # Add separator
            self.ids.report_data.add_widget(BoxLayout(
                size_hint_y=None,
                height='1dp',
                background_color=[0.5, 0.5, 0.5, 1]
            ))
            
            # Add visits
            months = ['January', 'February', 'March', 'April', 'May', 'June',
                     'July', 'August', 'September', 'October', 'November', 'December']
            
            total_visits = 0
            if visits:
                for visit in visits:
                    month_idx = int(visit[0]) - 1  # 0-indexed
                    month_name = months[month_idx]
                    
                    row = BoxLayout(
                        orientation='horizontal',
                        size_hint_y=None,
                        height='40dp',
                        spacing=5
                    )
                    row.add_widget(Label(text=month_name, size_hint_x=0.7))      # Month
                    row.add_widget(Label(text=str(visit[1]), size_hint_x=0.3))   # Visit count
                    self.ids.report_data.add_widget(row)
                    total_visits += visit[1]
            else:
                self.ids.report_data.add_widget(Label(
                    text='No visits found for this year',
                    size_hint_y=None,
                    height='40dp'
                ))
            
            # Update title with count
            self.ids.report_title.text = f'Yearly Report: {filter_value} - {total_visits} visits'
            
        elif report_type == 'Devotee-wise':
            if filter_value == 'No devotees found':
                return
                
            # Extract devotee ID from spinner value
            devotee_id = filter_value.split(' - ')[0]
            
            # Get visits for selected devotee
            visits = app.db.get_devotee_visits(devotee_id)
            
            # Create header
            header = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height='40dp',
                spacing=5
            )
            header.add_widget(Label(text='Date', size_hint_x=0.5))
            header.add_widget(Label(text='Selected Item', size_hint_x=0.5))
            self.ids.report_data.add_widget(header)
            
            # Add separator
            self.ids.report_data.add_widget(BoxLayout(
                size_hint_y=None,
                height='1dp',
                background_color=[0.5, 0.5, 0.5, 1]
            ))
            
            # Add visits
            if visits:
                for visit in visits:
                    row = BoxLayout(
                        orientation='horizontal',
                        size_hint_y=None,
                        height='40dp',
                        spacing=5
                    )
                    row.add_widget(Label(text=str(visit[0]), size_hint_x=0.5))      # Date
                    row.add_widget(Label(text=str(visit[1]), size_hint_x=0.5))      # Selected Item
                    self.ids.report_data.add_widget(row)
            else:
                self.ids.report_data.add_widget(Label(
                    text='No visits found for this devotee',
                    size_hint_y=None,
                    height='40dp'
                ))
            
            # Update title with count
            devotee_name = filter_value.split(' - ')[1] if ' - ' in filter_value else devotee_id
            self.ids.report_title.text = f'Devotee Report: {devotee_name} - {len(visits)} visits'
    
    def export_report(self):
        """Export the current report as a CSV file."""
        # This would typically save the report to an external file
        # For simplicity, we'll just show a success message
        from kivy.uix.popup import Popup
        
        content = BoxLayout(orientation='vertical', padding=10)
        
        message = Label(
            text='Report exported successfully!',
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
            title='Export Report',
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        
        close_btn.bind(on_release=popup.dismiss)
        popup.open()
    
    def go_back(self):
        """Navigate back to admin dashboard."""
        app = App.get_running_app()
        app.root.current = 'admin_dashboard'
