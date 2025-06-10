from pytesseract import pytesseract
from PIL import Image
import re
import os
import fcntl
import json
import time
import sys
import logging

# Configure logging
logging.basicConfig(
    filename='tesseract.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Redirect stderr to log file
sys.stderr = open('error.log', 'a')

# Set the Tesseract executable path (for macOS)
pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# Path to the latest screenshot
image_path = "/Users/dominik/Library/Mobile Documents/com~apple~CloudDocs/0_artner/0_FH Stp/00_Masterarbeit/Tesserax/T6_Screenshots/screenshot.png"
print(f"Image path: {image_path}")  # Debugging print

# Path to the TID file
tid_file_path = "/Users/dominik/Library/Mobile Documents/com~apple~CloudDocs/0_artner/0_FH Stp/00_Masterarbeit/Tesserax/T6_Screenshots/extracted_tid.txt"

def write_tid_with_lock(tid):
    """Write TID to file with proper locking and timestamp"""
    data = {
        'tid': tid,
        'timestamp': time.time(),
        'status': 'complete'
    }
    
    try:
        with open(tid_file_path, 'w') as f:
            # Get an exclusive lock
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                json.dump(data, f)
                logging.info(f"Successfully wrote TID: {tid}")
            finally:
                # Release the lock
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    except Exception as e:
        logging.error(f"Error writing TID: {e}")
        raise

def detect_tid(max_retries=3, delay=0.5):
    """Try to detect TID with retries"""
    for attempt in range(max_retries):
        try:
            # Open the image and crop the ROI
            image = Image.open(image_path)
            width, height = image.size
            top_left_roi = (0, 0, width // 2, height // 2)
            cropped_image = image.crop(top_left_roi)

            # Run Tesseract OCR on the cropped image
            extracted_text = pytesseract.image_to_string(cropped_image)
            logging.info(f"Extracted text: {extracted_text}")

            # Find all Track IDs (TID) in the text
            tid_matches = re.finditer(r"TID:\s*(\d{3})", extracted_text)
            tid_list = [match.group(1) for match in tid_matches]

            if tid_list:
                # Take the most recent TID (last one found in the text)
                track_id = tid_list[-1]
                logging.info(f"Found TIDs: {tid_list}, using most recent: {track_id}")
                return track_id
            
            logging.warning(f"No TID found on attempt {attempt + 1}")
            if attempt < max_retries - 1:
                time.sleep(delay)
                
        except Exception as e:
            logging.error(f"Error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
    
    return None

# Main execution
try:
    track_id = detect_tid()
    if track_id:
        write_tid_with_lock(track_id)
        print(f"Successfully processed TID: {track_id}")
        sys.exit(0)
    else:
        logging.error("Failed to detect TID after all retries")
        sys.exit(1)
except Exception as e:
    logging.error(f"Fatal error: {e}")
    sys.exit(1)
