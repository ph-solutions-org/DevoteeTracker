import random
from kivy.app import App

class ItemSelector:
    """
    Manages item selection functionality.
    """
    
    def __init__(self):
        """Initialize the item selector."""
        # Default items in case database is unavailable
        self.default_items = [
            "Swamivatsalya", "Sadavrata", "Jñāna Dāna", "Auṣadha Dāna", 
            "Abhaya Dāna", "Vaiyāvṛttya", "Jinālaya Jīrṇoddhāra", "Pratimā",
            "Pūjā", "Upavāsa", "Santhārā", "Saṃyama", "Tapasya", 
            "Tyāga", "Brahmacārya", "Kṣamā", "Ahiṃsā", "Satya"
        ]
    
    def select_random_item(self):
        """
        Select a random item from the 18 available items.
        
        Returns:
            String representing the selected item
        """
        app = App.get_running_app()
        
        try:
            # Get items from database
            items = app.db.get_all_items()
            
            # If items list is empty, use default items
            if not items:
                items = self.default_items
            
            # Select random item
            return random.choice(items)
        except Exception as e:
            print(f"Error selecting random item: {e}")
            # Fallback to default items if database fails
            return random.choice(self.default_items)
