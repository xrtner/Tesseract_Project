import subprocess

# Run the OCR script (test_tesseract.py)
subprocess.run(["python3", "test_tesseract.py"])

# Run the load stem script (load_stem.py)
subprocess.run(["python3", "osc_test2.py"])
