import subprocess
import json
import os

# Path to the TID file
tid_file_path = "/Users/dominik/Library/Mobile Documents/com~apple~CloudDocs/0_artner/0_FH Stp/00_Masterarbeit/Tesserax/T6_Screenshots/extracted_tid.txt"

def get_current_tid():
    try:
        if os.path.exists(tid_file_path):
            with open(tid_file_path, 'r') as f:
                data = json.load(f)
                return data.get('tid')
    except:
        pass
    return None

# Store the current TID before running OCR
old_tid = get_current_tid()

# Run the OCR script (test_tesseract.py)
subprocess.run(["python3", "test_tesseract.py"])

# Get the new TID
new_tid = get_current_tid()

# Log whether it's the same or new TID
if new_tid == old_tid:
    print(f"Same TID detected ({new_tid}), reloading stems...")
else:
    print(f"New TID detected: {new_tid}, loading stems...")

# Always run the process
subprocess.run(["python3", "deck_loader.py"])
