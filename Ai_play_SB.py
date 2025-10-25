import pyautogui
import cv2
import numpy as np
import keyboard
import time
import random

# important RGB:
# cpu (127,127,127)
# p1 (242,89,90)

def take_screenshot(x1,y1,x2,y2):
    # Take a screenshot of the entire screen
    screenshot = pyautogui.screenshot(region=(x1,y1,x2-x1,y2-y1))
    screenshot = np.array(screenshot)
    return screenshot

def process_screenshot(screenshot):
    # Your image processing logic here (e.g., object detection, segmentation)
    # For simplicity, let's assume we don't have complex processing and just return the original screenshot.
    return screenshot

def check_pixel_rgba(image,a,b,c):
    image_np = np.array(image)

    # Extract the RGB values of the pixels in the array
    rgb_values = image_np[:, :, :3]

    # Find the indices of pixels with the RGB value of (231, 90, 16)
    matching_indices = np.where((rgb_values[:, :, 0] == a) &
                                (rgb_values[:, :, 1] == b) &
                                (rgb_values[:, :, 2] == c))
    
    return len(matching_indices[0])

def attack_enemy():
    # Press and hold the control key to attack
    keyboard.press('x')
    time.sleep(0.5)
    # Release the control key
    keyboard.release('x')

def stop_script():
    # Check if backspace key is pressed
    if keyboard.is_pressed('backspace'):
        return True
    else:
        return False
    
def hold_key(key):
    keyboard.press(key)
    time.sleep(0.05)
    keyboard.release(key)

def double_jump(pos):
    for x in range(1,2):
        keyboard.press(pos)
        keyboard.press("up")
        time.sleep(1)
        keyboard.release(pos)
        time.sleep(1)
        keyboard.release("up")

def jump(pos):
    keyboard.press("up")
    keyboard.press(pos)
    time.sleep(0.05)
    keyboard.press("up")
    keyboard.release(pos)
    time.sleep(0.20)
    keyboard.release("x")

def find_largest_x_red(image):
    # xThreshold the image to isolate red pixels
    lower_red = np.array([0, 0, 100])
    upper_red = np.array([100, 100, 255])
    red_mask = cv2.inRange(image, lower_red, upper_red)

    # Find contours of red pixels
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest x-coordinate of red pixels
    largest_x_red = 0
    for contour in contours:
        for point in contour:
            x, _, = point[0]
            if x > largest_x_red:
                largest_x_red = x

    return largest_x_red

def find_smallest_x_blue(image):
    # Threshold the image to isolate blue pixels
    lower_blue = np.array([100, 0, 0])
    upper_blue = np.array([255, 100, 100])
    blue_mask = cv2.inRange(image, lower_blue, upper_blue)

    # Find contours of blue pixels
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the smallest x-coordinate of blue pixels
    smallest_x_blue = float('inf')
    for contour in contours:
        for point in contour:
            x, _, = point[0]
            if x < smallest_x_blue:
                smallest_x_blue = x

    return smallest_x_blue

def main():
    while True:
        # Take a screenshot
        screenshot = take_screenshot(0,0,1054,864)

      # Check for the presence of spcific RGB values in the processed screenshot
        #if find_zombe_pixel(screenshot):
        #    attack_zombie()
        """
        if check_pixel_rgba(screenshot_main,57,189,49) > 0:
            long_jump_right()
        elif find_smallest_x_blue(screenshot_main) - find_largest_x_red(screenshot_main) < 200:
            long_jump_right()
        if check_pixel_rgba(screenshot_main,231,90,16) > 0:
            jump_right()
        elif check_pixel_rgba(screenshot_main,123,148,255) > 0:
            jump_right()
        else:
            hold_key("right")
        """
        double_jump("right")
        jump("left")

        # Check if backspace is pressed to stop the script
        if stop_script():
            print("Stopping script...")
            break

        # Sleep for a short duration before taking the next action
        #time.sleep(0.5)

if __name__ == "__main__":
    main()