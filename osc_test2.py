from pythonosc.udp_client import SimpleUDPClient

# Configure OSC client
ip = "127.0.0.1"  # Localhost for Bitwig
port = 8000       # Bitwig's OSC receive port

client = SimpleUDPClient(ip, port)

# Define file path and target
file_path = "/path/to/your/file.wav"
track_number = 1  # Track index (1-based)
clip_number = 1   # Clip slot (1-based)

# Step 1: Insert file into the clip launcher
client.send_message(f"/track/{track_number}/clip/{clip_number}/insertFile", file_path)

# Step 2: Record clip into the Arrangement
# Command to launch the clip (if needed)
client.send_message(f"/clip/launch", 1)

# Optional: Send command to toggle Arrangement playback/recording (if script logic allows this in Bitwig)
#client.send_message("/transport/record", 1)
