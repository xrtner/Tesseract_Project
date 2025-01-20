from pytesseract import pytesseract
from PIL import Image
import re
import os

# Set the Tesseract executable path (for macOS)
pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# Path to the latest screenshot
image_path = "/Users/dominik/Library/Mobile Documents/com~apple~CloudDocs/0_artner/0_FH Stp/00_Masterarbeit/Tesserax/T6_Screenshots/screenshot.png"
print(f"Image path: {image_path}")  # Debugging print

# Open the image and crop the ROI
image = Image.open(image_path)
width, height = image.size
top_left_roi = (0, 0, width // 2, height // 2)
cropped_image = image.crop(top_left_roi)

# Run Tesseract OCR on the cropped image
extracted_text = pytesseract.image_to_string(cropped_image)

# Find the Track ID (TID)
tid_match = re.search(r"TID:\s*(\d{3})", extracted_text)
if tid_match:
    track_id = tid_match.group(1)  # Extract the track ID
    print(f"TID: {track_id}")  # Print the TID for debugging
    # Save the TID to a file
    tid_file_path = "/Users/dominik/Library/Mobile Documents/com~apple~CloudDocs/0_artner/0_FH Stp/00_Masterarbeit/Tesserax/T6_Screenshots/extracted_tid.txt"
    with open(tid_file_path, "w") as f:
        f.write(track_id)
else:
    print("No TID found")
    exit(1)  # Exit with an error code if no TID is found
