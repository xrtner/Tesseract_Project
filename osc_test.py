from pythonosc.udp_client import SimpleUDPClient

# Configure OSC client
ip = "127.0.0.1"  # Localhost for Bitwig
port = 8000       # Default DrivenByMoss OSC port
client = SimpleUDPClient(ip, port)

# Test: Start playback in Bitwig
client.send_message("/play", 1)  # 1 to start playback, 0 to stop

# Test: Stop playback in Bitwig
client.send_message("/play", 0)  # Stops playback