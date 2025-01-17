from pythonosc.udp_client import SimpleUDPClient

# Configure OSC client
ip = "127.0.0.1"  # Localhost for Bitwig
port = 8000       # Bitwig's OSC receive port

client = SimpleUDPClient(ip, port)

# Define file path and target
file_path = "/Users/dominik/Library/Mobile Documents/com~apple~CloudDocs/0_artner/0_FH Stp/00_Masterarbeit/Tesserax/T5_Stems/TID001_01_Synth_Bob Semp - Retroflect (Original Mix) - 142bpm - Cmaj.wav"
track_number = 1  # For Deck 01 - Stem 01
clip_number = 1   # Assuming first clip slot

# Send OSC command to load the file into the specified track and clip
client.send_message(f"/track/{track_number}/clip/{clip_number}/insertFile", file_path)
