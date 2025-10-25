import pyautogui
import cv2
import numpy as np
import keyboard
import time
import random

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
    


import pyautogui
from PIL import Image

def take_screenshot():
    # Take a screenshot of the entire screen
    screenshot = pyautogui.screenshot()
    return screenshot

def find_furthest_closest_grey_pixel(image):
    width, height = image.size
    max_distance = 0
    min_distance = float('inf')
    furthest_pixel = closest_pixel = None

    # Iterate through each pixel in the image
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            # Check if the pixel is grey
            if isinstance(pixel, tuple) and len(pixel) == 3:
                if pixel[0] == pixel[1] == pixel[2]:
                    # Calculate distance from the center of the image
                    distance = ((width/2 - x)**2 + (height/2 - y)**2) ** 0.5
                    # Update furthest and closest pixels
                    if distance > max_distance:
                        max_distance = distance
                        furthest_pixel = (x, y)
                    if distance < min_distance:
                        min_distance = distance
                        closest_pixel = (x, y)
    return furthest_pixel, closest_pixel

def move_mouse_to_pixel(pixel):
    # Move the mouse to the given pixel coordinates
    pyautogui.moveTo(pixel[0], pixel[1])

def straighten_line(furthest_pixel, closest_pixel):
    # Move the mouse to the furthest pixel
    move_mouse_to_pixel(furthest_pixel)

    # Get the x-coordinate difference between furthest and closest pixels
    x_difference = furthest_pixel[0] - closest_pixel[0]

    # Press the arrow keys until the line is straight
    if x_difference > 0:
        keyboard.press('left')
        while x_difference > 0:
            # Press left arrow key
            pass
        keyboard.release('left')
    elif x_difference < 0:
        # Press right arrow key
        keyboard.press('right')
        while x_difference > 0:
            # Press left arrow key
            pass
        keyboard.release('right')

def main():
    while True:
        # Take a screenshot
        screenshot = take_screenshot()

        # Convert the screenshot to grayscale
        screenshot_gray = screenshot.convert('L')

        # Find furthest and closest grey pixels
        furthest_pixel, closest_pixel = find_furthest_closest_grey_pixel(screenshot_gray)

        if furthest_pixel and closest_pixel:
            print("Furthest Pixel:", furthest_pixel)
            print("Closest Pixel:", closest_pixel)

            # Straighten the line
            straighten_line(furthest_pixel, closest_pixel)

        if stop_script():
            print("Stopping script...")
            keyboard.release('x')

            break

if __name__ == "__main__":
    keyboard.press("x")
    main()
