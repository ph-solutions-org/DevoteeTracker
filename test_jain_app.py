import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

# Set window size for desktop
Window.size = (400, 700)
Window.clearcolor = (0.95, 0.95, 0.95, 1)  # Light gray background

# Define screens
class HomeScreen(Screen):
    def go_to_second(self):
        self.manager.current = 'second'

class SecondScreen(Screen):
    def go_back(self):
        self.manager.current = 'home'

# Load KV string directly
kv_string = '''
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        
        Label:
            text: 'Jain Temple Test App'
            font_size: '24sp'
            size_hint_y: 0.3
            
        Label:
            text: 'Home Screen'
            font_size: '20sp'
            size_hint_y: 0.3
            
        Button:
            text: 'Go to Second Screen'
            font_size: '18sp'
            size_hint_y: 0.2
            on_release: root.go_to_second()
            background_color: 0.2, 0.6, 1, 1

<SecondScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        
        Label:
            text: 'Second Screen'
            font_size: '24sp'
            size_hint_y: 0.5
            
        Button:
            text: 'Go Back'
            font_size: '18sp'
            size_hint_y: 0.2
            on_release: root.go_back()
            background_color: 0.8, 0.2, 0.2, 1
'''

class TestJainApp(App):
    def build(self):
        # Load the KV string
        Builder.load_string(kv_string)
        
        # Create screen manager and add screens
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(SecondScreen(name='second'))
        
        return sm

if __name__ == '__main__':
    TestJainApp().run()