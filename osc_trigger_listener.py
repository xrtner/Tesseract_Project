
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import subprocess

# Define the function to run automation when the OSC trigger is received
def trigger_action(unused_addr, args):
    print("Trigger received!")
    try:
        print("Starting automation script...")
        subprocess.run(["python3", "screenshot_and_load.py"], check=True)
        print("Automation process completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Subprocess error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def trigger_action(unused_addr, args):
    print(f"Received OSC trigger with args: {args}")
    print("Trigger received! Running automation...")
    try:
        subprocess.run(["python3", "screenshot_and_load.py"], check=True)
        print("Automation process completed successfully.")
    except Exception as e:
        print(f"Error running automation: {e}")


# Set up the dispatcher to handle incoming OSC messages
dispatcher = Dispatcher()
dispatcher.map("/trigger", trigger_action)  # Map the "/trigger" address to the function
print("Dispatcher set up and ready to map OSC messages.")

# Define OSC server settings
ip = "127.0.0.1"
port = 9100  # This should match the port in your TouchDesigner OSC Out
print(f"Setting up OSC server on {ip}:{port}...")

# Set up the OSC server
try:
    server = BlockingOSCUDPServer((ip, port), dispatcher)
    print(f"OSC server successfully started on {ip}:{port}. Listening for OSC messages...")
except Exception as e:
    print(f"Failed to start OSC server: {e}")
    exit(1)

# Start the server
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("Server manually stopped.")
except Exception as e:
    print(f"Unexpected error while running the server: {e}")
