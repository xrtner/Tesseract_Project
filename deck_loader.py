import os
import time
from pythonosc.udp_client import SimpleUDPClient

# Configure OSC client
ip = "127.0.0.1"  # Localhost for Bitwig
port = 8000       # Bitwig's OSC receive port

client = SimpleUDPClient(ip, port)

# Directory containing stems
stem_directory = "/Users/dominik/Library/Mobile Documents/com~apple~CloudDocs/0_artner/0_FH Stp/00_Masterarbeit/Tesserax/T5_Stems"

# TID to match (set dynamically or manually)
current_tid = "001"  # Example TID

# Define track mappings
track_mapping = {
    "01": 1,  # Deck 01
    "02": 2,  # Deck 02
    "03": 3,  # Deck 03
    "04": 4,  # Deck 04
}

# Scan directory for stem files
stem_files = [f for f in os.listdir(stem_directory) if f.endswith((".wav", ".mp3"))]
print(f"Found stem files: {stem_files}")

# Filter stems by the correct TID
filtered_stems = [f for f in stem_files if f[3:6] == current_tid]  # Match digits 3, 4, 5
print(f"Filtered stems for TID {current_tid}: {filtered_stems}")

# Check if no stems match the TID
if not filtered_stems:
    print(f"No stems found for TID {current_tid}. Exiting process.")
    exit()

# Parse and load stems
loaded_decks = set()  # Keep track of already loaded decks
for stem_file in filtered_stems:
    try:
        # Extract the stem identifier (digits 7 and 8 in the filename)
        stem_id = stem_file[7:9]  # Adjust indices if necessary
        print(f"Processing stem file: {stem_file} with stem ID: {stem_id}")

        if stem_id in track_mapping and stem_id not in loaded_decks:
            track_number = track_mapping[stem_id]
            file_path = os.path.join(stem_directory, stem_file)
            clip_number = 1  # Assuming all use the first clip slot

            # Step 1: Insert file into the clip launcher
            client.send_message(f"/track/{track_number}/clip/{clip_number}/insertFile", file_path)
            time.sleep(0.5)  # Small delay to ensure the file is processed

            # Step 2: Launch the clip to make it audible
            client.send_message(f"/track/{track_number}/clip/{clip_number}/launch", 1)
            time.sleep(0.5)

            # Step 3: Set clip start to 1.2.2.00
            clip_start_position = 2.25  # 1.2.2.00 in bars.beats.sixteenths as a float
            client.send_message(f"/track/{track_number}/clip/{clip_number}/start", clip_start_position)
            print(f"Loaded {stem_file} into Deck {track_number}, Clip {clip_number}.")
            loaded_decks.add(stem_id)  # Mark this deck as loaded
        else:
            print(f"Skipping {stem_file}: No matching track or already loaded for stem ID {stem_id}.")
    except Exception as e:
        print(f"Error processing {stem_file}: {e}")

# Optional: Stop playback for all tracks
time.sleep(0.5)  # Delay before stopping to allow all clips to launch
client.send_message("/stop", 1)  # Stop playback
