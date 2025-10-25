import pyautogui
import cv2
import numpy as np
import keyboard
import time
import random

def take_screenshot():
    # Take a screenshot of the entire screen
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    return cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

def process_screenshot(screenshot):
    # Your image processing logic here (e.g., object detection, segmentation)
    # For simplicity, let's assume we don't have complex processing and just return the original screenshot.
    return screenshot

def find_zombie_pixel(image):
    # Check for the presence of specific RGB values (e.g., (70,37,19)) in the image
    zombie_pixel = np.all(np.isclose(image, [70,37,19], atol=10), axis=-1)
    return np.any(zombie_pixel)

def attack_zombie():
    # Press and hold the control key to attack
    keyboard.press('ctrl')

    # Move the mouse to a zombie (you need to implement this)
    pyautogui.moveTo(10, 20)

    # Perform a mouse click to attack the zombie
    pyautogui.click()

    # Release the control key
    keyboard.release('ctrl')

def stop_script():
    # Check if backspace key is pressed
    if keyboard.is_pressed('backspace'):
        return True
    else:
        return False
    
def hold_key(key):
    # Hold a specific key for a given duration
    start_time = time.time()
    while time.time() - start_time < 0.2:
        keyboard.press(key)
        keyboard.release(key)

def main():
    while True:
        # Take a screenshot
        screenshot = take_screenshot()

        # Process the screenshot
        processed_screenshot = process_screenshot(screenshot)

        # Check for the presence of specific RGB values in the processed screenshot
        """if find_zombie_pixel(screenshot):
            attack_zombie()"""

        # Move in a random direction (for demonstration purposes)
        #directions = ["up", "down", "left", "right"]
        #hold_key(random.choice(directions))
        """
        if pyautogui.position()[0] > 400:
            pyautogui.moveTo(400,pyautogui.position()[1])
        elif pyautogui.position()[0] < 100:
            pyautogui.moveTo(100,pyautogui.position()[1])
        """
        pyautogui.click()
        if random.randint(1,10) < 5:
            x = random.randint(600,1260)
            pyautogui.moveTo(x, 870)
            pyautogui.click()
            pyautogui.moveTo(random.randint(600,1260), 950)
            pyautogui.click()
            pyautogui.moveTo(random.randint(400,800), random.randint(120,800))
            pyautogui.click()
        else:
            pyautogui.moveTo(random.randint(400,800), random.randint(120,800))
            pyautogui.click()
    
        if random.randint(1,100) > 95:
            keyboard.press('tab')
            keyboard.release('tab')
            break

        # Check if backspace is pressed to stop the script
        if stop_script():
            print("Stopping script...")
            break

        # Sleep for a short duration before taking the next action
        #time.sleep(0.5)

if __name__ == "__main__":
    pyautogui.moveTo(random.randint(400,800), random.randint(120,800))
    main()