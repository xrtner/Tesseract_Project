import os
import subprocess

def take_screenshot():
    # Define the exact file path for the screenshot
    screenshot_path = "/Users/dominik/Library/Mobile Documents/com~apple~CloudDocs/0_artner/0_FH Stp/00_Masterarbeit/Tesserax/T6_Screenshots/screenshot.png"
    print(f"Attempting to save screenshot to: {screenshot_path}")

    # Verify if the directory exists
    directory = os.path.dirname(screenshot_path)
    if not os.path.exists(directory):
        print(f"Directory does not exist: {directory}")
        return

    try:
        # Run the screencapture command
        print("Running 'screencapture' command...")
        subprocess.run(
            ["screencapture", "-x", screenshot_path],
            check=True,
            capture_output=True,
            text=True
        )
        print("Screenshot successfully saved!")

        # Call the automation process
        run_automation(screenshot_path)

    except subprocess.CalledProcessError as e:
        print("Error taking the screenshot or running automation.")
        print("Command output:", e.stdout)
        print("Command error:", e.stderr)
    except PermissionError:
        print("Permission error: Cannot write to the specified directory.")


def run_automation(screenshot_path):
    print("Running automation process...")
    try:
        # Call your automation script
        subprocess.run(["python3", "run_automation.py", screenshot_path], check=True)
        print("Automation process completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running automation: {e}")
        print(f"Command output: {e.stdout}")
        print(f"Command error: {e.stderr}")


if __name__ == "__main__":
    take_screenshot()
