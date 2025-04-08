from kivy.app import App
import datetime

class LabelPrinter:
    """
    Manages label printing functionality for the barcode printer.
    """
    
    def __init__(self):
        """Initialize the label printer."""
        # Default label width (in mm) for typical barcode printers
        self.label_width = 50
        self.label_height = 30
    
    def generate_label_data(self, print_data):
        """
        Generate PRN command data for printing a label.
        
        Args:
            print_data: Dictionary containing:
                - devotee_id: The devotee's ID
                - devotee_name: The devotee's name
                - selected_item: The randomly selected item
                - date: The current date
                
        Returns:
            Binary data to send to printer
        """
        # ZPL (Zebra Programming Language) based template
        # This is a common printer language - adjust as needed for actual printer
        
        devotee_id = print_data.get('devotee_id', '')
        devotee_name = print_data.get('devotee_name', '')
        selected_item = print_data.get('selected_item', '')
        date = print_data.get('date', datetime.date.today().strftime("%d/%m/%Y"))
        
        # Calculate positions based on label dimensions
        # Width and height in dots (assuming 203 DPI printer)
        width_dots = int(self.label_width * 8)  # 8 dots per mm at 203 DPI
        height_dots = int(self.label_height * 8)
        
        # Set up ZPL code for a label
        zpl_code = f"""
^XA
^CI28
^CF0,30
^FO20,20^FDDevotee ID: {devotee_id}^FS
^CF0,25
^FO20,60^FDName: {devotee_name}^FS
^CF0,25
^FO20,100^FDItem: {selected_item}^FS
^CF0,20
^FO20,140^FDDate: {date}^FS
^BY2,2,50
^FO20,170^BC^FD{devotee_id}^FS
^XZ
"""
        
        return zpl_code.encode('utf-8')
    
    def print_label(self, print_data):
        """
        Print a label using the connected Bluetooth printer.
        
        Args:
            print_data: Dictionary with label data
            
        Returns:
            Boolean indicating success
        """
        app = App.get_running_app()
        
        # Check if printer is connected
        if not app.bluetooth.is_connected():
            return False
        
        try:
            # Generate label data
            label_data = self.generate_label_data(print_data)
            
            # Send to printer
            return app.bluetooth.send_data(label_data)
        except Exception as e:
            print(f"Error printing label: {e}")
            return False
    
    def set_label_dimensions(self, width, height):
        """Set label dimensions in millimeters."""
        self.label_width = width
        self.label_height = height
