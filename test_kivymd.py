from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.utils import platform

# Set window size for desktop testing
if platform not in ('android', 'ios'):
    Window.size = (400, 700)

class TestScreen(MDScreen):
    def __init__(self, **kwargs):
        super(TestScreen, self).__init__(**kwargs)
        
        # Create a vertical layout
        from kivymd.uix.boxlayout import MDBoxLayout
        layout = MDBoxLayout(orientation='vertical', 
                           padding=20, 
                           spacing=20,
                           adaptive_height=True)
        
        # Add a title
        title = MDLabel(
            text="Jain Temple App",
            halign="center",
            font_style="H4",
            adaptive_height=True
        )
        layout.add_widget(title)
        
        # Add a subtitle
        subtitle = MDLabel(
            text="Modern Material Design UI",
            halign="center",
            font_style="Subtitle1",
            adaptive_height=True
        )
        layout.add_widget(subtitle)
        
        # Add a button
        button = MDRaisedButton(
            text="CLICK ME",
            pos_hint={"center_x": 0.5},
            size_hint=(0.8, None),
            height="48dp"
        )
        layout.add_widget(button)
        
        self.add_widget(layout)

class TestKivyMDApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Light"
        
        sm = ScreenManager()
        sm.add_widget(TestScreen(name='test'))
        return sm

if __name__ == '__main__':
    TestKivyMDApp().run()