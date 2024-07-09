import subprocess
import time

def startPygameEnvironment():
    subprocess.Popen(["python", "main.py"])

def simulateKeyPress(key):
    # This function should simulate key press events for testing.
    # Note: Actual key press simulation may require external libraries like `pynput` or `pyautogui`.
    print(f"Simulating key press: {key}")

if __name__ == "__main__":
    startPygameEnvironment()
    time.sleep(5)  # Wait for the Pygame window to initialize

    # Simulate key presses to interact with the Pygame environment
    simulateKeyPress('w')  # Change shape
    time.sleep(1)
    simulateKeyPress('s')  # Change color
    time.sleep(1)
    simulateKeyPress('UP')  # Move shape up
    time.sleep(1)
    simulateKeyPress('RIGHT')  # Move shape right
    time.sleep(1)
    simulateKeyPress('RETURN')  # Place shape
    time.sleep(1)
    simulateKeyPress('e')  # Export grid state
    time.sleep(1)
    simulateKeyPress
