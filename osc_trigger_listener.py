from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import subprocess
import sys

# Redirect stderr to log file
sys.stderr = open('error.log', 'a')

# Function to handle button press events
def button_pressed(unused_addr, *args):
    signal = args[0] if args else 0.0
    if signal == 1.0:  # Button pressed
        print("Button pressed! Triggering screenshot.py...")
        try:
            # Run the screenshot script
            subprocess.run(["python3", "/Users/dominik/Library/Mobile Documents/com~apple~CloudDocs/0_artner/0_FH Stp/00_Masterarbeit/Tesserax/T3_Code/Tesseract_Project/screenshot.py"], check=True)
            print("screenshot.py executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error while running screenshot.py: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    elif signal == 0.0:  # Button released
        print("Button released.")

# Set up the dispatcher to handle incoming OSC messages
dispatcher = Dispatcher()
dispatcher.map("/ch14n40", button_pressed)
dispatcher.map("/ch10ctrl1", button_pressed)  # Map the button signal address

print("Starting OSC server on 127.0.0.1:9200...")
# server = BlockingOSCUDPServer(("192.168.0.228", 9100), dispatcher)
server = BlockingOSCUDPServer(("0.0.0.0", 9200), dispatcher)
print("OSC server is running and waiting for messages...")

# Start the OSC server
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("OSC server stopped.")
