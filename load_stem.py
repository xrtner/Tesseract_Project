import os

# Path to the folder containing your stems
stems_folder = "/path/to/stems/folder"  # Replace with your stems folder path

# Read the extracted TID from the file
with open("extracted_tid.txt", "r") as f:
    track_id = f.read().strip()

# Search for the stem file
file_to_load = None
for file in os.listdir(stems_folder):
    if file.startswith(f"TID{track_id}") and file.endswith(".wav"):
        file_to_load = os.path.join(stems_folder, file)
        break

if file_to_load:
    print(f"Found file: {file_to_load}")
    # Here you would add the code to load the file into Ableton/Bitwig (this part will depend on the DAW integration)
else:
    print(f"No stem file found for TID {track_id}")