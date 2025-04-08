from kivy.utils import platform
import threading
import time

class BluetoothManager:
    """
    Manages Bluetooth connections for printing.
    """
    
    def __init__(self):
        self.is_android = platform == 'android'
        self.is_ios = platform == 'ios'
        self.connected_device = None
        self.bluetooth_adapter = None
        self.socket = None
        
        # Initialize Bluetooth based on platform
        self._init_bluetooth()
    
    def _init_bluetooth(self):
        """Initialize Bluetooth adapter based on platform."""
        if self.is_android:
            # Import Android-specific modules
            try:
                from jnius import autoclass
                
                # Android Bluetooth classes
                self.BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
                self.BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
                self.BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
                self.UUID = autoclass('java.util.UUID')
                
                # Standard serial UUID
                self.uuid = self.UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
                
                # Get the Bluetooth adapter
                self.bluetooth_adapter = self.BluetoothAdapter.getDefaultAdapter()
                
                if not self.bluetooth_adapter:
                    print("Bluetooth is not available on this device")
                elif not self.bluetooth_adapter.isEnabled():
                    print("Bluetooth is not enabled")
                    # Note: We should request to enable Bluetooth here
                    # but for simplicity, we'll assume it's enabled
            except Exception as e:
                print(f"Error initializing Android Bluetooth: {e}")
        
        elif self.is_ios:
            # For iOS, we would use PyObjus or another iOS bridge
            # This is a placeholder for future implementation
            print("iOS Bluetooth implementation not yet available")
        
        else:
            # For desktop testing, use a mock implementation
            print("Using mock Bluetooth implementation for desktop testing")
    
    def scan_for_devices(self):
        """
        Scan for available Bluetooth devices.
        Returns a list of device dictionaries with 'name' and 'address'.
        """
        devices = []
        
        if self.is_android:
            try:
                # Get paired devices
                paired_devices = self.bluetooth_adapter.getBondedDevices().toArray()
                
                for device in paired_devices:
                    name = device.getName()
                    address = device.getAddress()
                    devices.append({
                        'name': name,
                        'address': address
                    })
                
                # Optionally start discovery for new devices
                # self.bluetooth_adapter.startDiscovery()
                # But need to handle the BroadcastReceiver for ACTION_FOUND
            except Exception as e:
                print(f"Error scanning for devices: {e}")
        
        elif self.is_ios:
            # iOS implementation placeholder
            pass
        
        else:
            # Mock implementation for testing
            devices = [
                {'name': 'Test Printer 1', 'address': '00:11:22:33:44:55'},
                {'name': 'Test Printer 2', 'address': 'AA:BB:CC:DD:EE:FF'},
                {'name': 'Test Device', 'address': '12:34:56:78:90:AB'}
            ]
            # Simulate scanning delay
            time.sleep(1)
        
        return devices
    
    def connect_to_device(self, address):
        """
        Connect to a Bluetooth device by address.
        Returns boolean indicating success.
        """
        # Disconnect any existing connection
        if self.is_connected():
            self.disconnect()
        
        if self.is_android:
            try:
                # Get device by address
                device = self.bluetooth_adapter.getRemoteDevice(address)
                
                # Create socket and connect
                self.socket = device.createRfcommSocketToServiceRecord(self.uuid)
                self.socket.connect()
                
                # Store connected device
                self.connected_device = {'address': address, 'name': device.getName()}
                
                return True
            except Exception as e:
                print(f"Error connecting to device: {e}")
                self.socket = None
                self.connected_device = None
                return False
        
        elif self.is_ios:
            # iOS implementation placeholder
            return False
        
        else:
            # Mock implementation for testing
            self.connected_device = {'address': address, 'name': 'Test Printer'}
            # Simulate connection delay
            time.sleep(1)
            return True
    
    def disconnect(self):
        """Disconnect from the current device."""
        if not self.is_connected():
            return True
        
        if self.is_android:
            try:
                if self.socket:
                    self.socket.close()
                    self.socket = None
                    self.connected_device = None
                return True
            except Exception as e:
                print(f"Error disconnecting: {e}")
                return False
        
        elif self.is_ios:
            # iOS implementation placeholder
            return False
        
        else:
            # Mock implementation for testing
            self.connected_device = None
            return True
    
    def is_connected(self):
        """Check if connected to a device."""
        return self.connected_device is not None
    
    def send_data(self, data):
        """
        Send binary data to the connected device.
        Returns boolean indicating success.
        """
        if not self.is_connected():
            return False
        
        if self.is_android:
            try:
                # Get output stream from socket
                output_stream = self.socket.getOutputStream()
                
                # Convert string data to bytes if needed
                if isinstance(data, str):
                    data = data.encode('utf-8')
                
                # Write data
                output_stream.write(data)
                output_stream.flush()
                return True
            except Exception as e:
                print(f"Error sending data: {e}")
                return False
        
        elif self.is_ios:
            # iOS implementation placeholder
            return False
        
        else:
            # Mock implementation for testing
            print(f"Simulated data sent: {data[:20]}...")
            return True
