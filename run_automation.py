import subprocess

# Run the OCR script (test_tesseract.py)
subprocess.run(["python3", "test_tesseract.py"])

# Run the load stem script (deck_loader.py)
subprocess.run(["python3", "deck_loader.py"])
