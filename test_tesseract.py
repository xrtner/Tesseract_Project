from pytesseract import pytesseract
from PIL import Image
import re

# Set the Tesseract executable path (for macOS)
pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# Path to the latest screenshot
image_path = "/Users/dominik/Library/Mobile Documents/com~apple~CloudDocs/0_artner/0_FH Stp/00_Masterarbeit/Tesserax/T6_Screenshots/TID_001_Test_02.png"
print(f"Image path: {image_path}")  # Debugging print

image = Image.open(image_path)

# Run Tesseract OCR to extract text
extracted_text = pytesseract.image_to_string(image)

# Find the Track ID (TID)
tid_match = re.search(r"TID:\s*(\d{3})", extracted_text)  # This will search for TID followed by 3 digits
if tid_match:
    track_id = tid_match.group(1)  # Extract the track ID
    print(f"TID: {track_id}")  # Only print the TID
    with open("extracted_tid.txt", "w") as f:
        f.write(track_id)
else:
    print("No TID found")  # Print "No TID found" if not found


