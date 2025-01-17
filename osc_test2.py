import time
from pythonosc.udp_client import SimpleUDPClient

# Configure OSC client
ip = "127.0.0.1"  # Localhost for Bitwig
port = 8000       # Bitwig's OSC receive port

client = SimpleUDPClient(ip, port)

# Define a list of file paths and their target track numbers
stems = [
    {
        "file_path": "/Users/dominik/Library/Mobile Documents/com~apple~CloudDocs/0_artner/0_FH Stp/00_Masterarbeit/Tesserax/T5_Stems/TID001_01_Synth_Bob Semp - Retroflect (Original Mix) - 142bpm - Cmaj.wav",
        "track_number": 1,  # Deck 01 - Stem 01
    },
    {
        "file_path": "/Users/dominik/Library/Mobile Documents/com~apple~CloudDocs/0_artner/0_FH Stp/00_Masterarbeit/Tesserax/T5_Stems/TID001_02_Kick - Bob Semp - Retroflect (Original Mix) - 142bpm - Cmaj.wav",
        "track_number": 2,  # Deck 01 - Stem 02
    },
    # Add more stems here for scalability
]

# Iterate over the stems to load and launch them
for stem in stems:
    file_path = stem["file_path"]
    track_number = stem["track_number"]
    clip_number = 1  # Assuming all use the first clip slot

    # Step 1: Insert file into the clip launcher
    client.send_message(f"/track/{track_number}/clip/{clip_number}/insertFile", file_path)
    time.sleep(0.5)  # Small delay to ensure the file is processed

    # Step 2: Launch the clip to make it audible
    client.send_message(f"/track/{track_number}/clip/{clip_number}/launch", 1)
    time.sleep(0.5)

    # Step 3: Set clip start to 1.2.2.00
    clip_start_position = 2.25  # 1.2.2.00 in bars.beats.sixteenths as a float (e.g., 1 bar = 1.0, 2.2.0 = 2.25)
    client.send_message(f"/track/{track_number}/clip/{clip_number}/start", clip_start_position)
    print(f"Clip start position for track {track_number}, clip {clip_number} set to {clip_start_position}.")


# Optional: Stop playback for all tracks
time.sleep(0.5)  # Delay before stopping to allow all clips to launch
client.send_message("/stop", 1)  # Stop playback

