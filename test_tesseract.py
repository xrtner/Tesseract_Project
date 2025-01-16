from pytesseract import pytesseract
from PIL import Image

# Set the Tesseract executable path
pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# Path to the image
image_path = "/Users/dominik/Library/Mobile Documents/com~apple~CloudDocs/0_artner/0_FH Stp/00_Masterarbeit/Tesserax/T9_Misc/TID_001_Test_02.png"  # Replace with the path to your image
image = Image.open(image_path)

# Extract text
extracted_text = pytesseract.image_to_string(image)

# Check for TID
if "TID:" in extracted_text:
    # Extract the TID value
    start_index = extracted_text.find("TID:") + len("TID:")
    tid = extracted_text[start_index:].split()[0]  # Split to get only the ID
    print(f"TID: {tid}")
else:
    print("No TID found")
