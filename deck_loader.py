import os
import time
import json
import fcntl
from pythonosc.udp_client import SimpleUDPClient
import sys

sys.stderr = open('error.log', 'a')  # Errors will go to error.log instead of screen

# Configure OSC client
ip = "127.0.0.1"  # Localhost for Bitwig
port = 8000       # Bitwig's OSC receive port

client = SimpleUDPClient(ip, port)

# Directory containing stems
stem_directory = "/Users/dominik/Library/Mobile Documents/com~apple~CloudDocs/0_artner/0_FH Stp/00_Masterarbeit/Tesserax/T5_Stems"

# Path to the TID file
tid_file_path = "/Users/dominik/Library/Mobile Documents/com~apple~CloudDocs/0_artner/0_FH Stp/00_Masterarbeit/Tesserax/T6_Screenshots/extracted_tid.txt"

def read_tid_with_lock():
    """Read TID from file with proper locking and validation"""
    if not os.path.exists(tid_file_path):
        print(f"TID file not found at: {tid_file_path}")
        return None, None

    with open(tid_file_path, 'r') as f:
        # Get a shared lock
        fcntl.flock(f.fileno(), fcntl.LOCK_SH)
        try:
            data = json.load(f)
            # Check if the file is fresh (less than 5 seconds old)
            if time.time() - data['timestamp'] > 5:
                print("TID file is too old, may be stale")
                return None, None
            return data['tid'], data['status']
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error reading TID file: {e}")
            return None, None
        finally:
            # Release the lock
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

# Read the TID with proper locking
current_tid, status = read_tid_with_lock()
if not current_tid or status != 'complete':
    print("No valid TID found. Exiting process.")
    exit(1)

print(f"Processing TID: {current_tid}")

# Define track mappings
track_mapping = {
    "01": 1,  # Deck 01
    "02": 2,  # Deck 02
    "03": 3,  # Deck 03
    "04": 4,  # Deck 04
    "05": 5,
}

# Scan directory for stem files
stem_files = [f for f in os.listdir(stem_directory) if f.endswith((".wav", ".mp3"))]

# Filter stems by the correct TID
filtered_stems = [f for f in stem_files if f[3:6] == current_tid]  # Match digits 3, 4, 5
print("\nFound stems for TID {current_tid}:")
for stem in filtered_stems:
    print(f"  - {stem}")

# Check if no stems match the TID
if not filtered_stems:
    print(f"No stems found for TID {current_tid}. Exiting process.")
    exit(1)

# Parse and load stems
loaded_decks = set()  # Keep track of already loaded decks
for stem_file in filtered_stems:
    try:
        # Extract the stem identifier (digits 7 and 8 in the filename)
        stem_id = stem_file[7:9]  # Adjust indices if necessary

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
            print(f"Loaded: {stem_file}")
            print(f"For Deck {track_number} -> Clip {clip_number}")
            loaded_decks.add(stem_id)  # Mark this deck as loaded

            client.send_message(f"/track/{track_number}/clip/{clip_number}/mode", "raw")

        else:
            print(f"Skipping {stem_file}: Already loaded or invalid stem ID {stem_id}")
    except Exception as e:
        print(f"Error processing {stem_file}: {e}")

# Optional: Stop playback for all tracks
time.sleep(0.5)  # Delay before stopping to allow all clips to launch
client.send_message("/stop", 1)  # Stop playback

# Print final status for Deck 1
print("\nACTIVE:")
print("\nDeck 1:")
print(f"TID{current_tid}")
# Get track title from first stem file (removing TID and stem number prefix and file extension)
track_title = filtered_stems[0][10:-4]  # -4 to remove .wav or .mp3
print(track_title)
print()  # Add blank line at the end