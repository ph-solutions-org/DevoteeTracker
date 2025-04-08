import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window

# Set window size for desktop testing
Window.size = (400, 700)
Window.clearcolor = (0.95, 0.95, 0.95, 1)  # Light gray background

# Define our screens
class HomeScreen(Screen):
    def go_to_second(self):
        self.manager.current = 'second'

class SecondScreen(Screen):
    def go_back(self):
        self.manager.current = 'home'

# Embed KV directly to avoid loading issues
KV = '''
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        
        Label:
            text: 'Jain Temple App'
            font_size: '24sp'
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

class EmbeddedKvApp(App):
    def build(self):
        # Load the embedded KV
        Builder.load_string(KV)
        
        # Create screen manager and add screens
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(SecondScreen(name='second'))
        
        return sm

if __name__ == '__main__':
    EmbeddedKvApp().run()