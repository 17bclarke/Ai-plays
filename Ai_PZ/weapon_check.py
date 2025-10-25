import pyautogui
import easyocr
import cv2
import numpy as np
import re

# List of Project Zomboid weapons ordered from strongest to weakest
weapons = [
    # Strongest melee weapons
    "Katana", "Machete", "Axe", "Spiked Baseball Bat", "Sledgehammer", "Baseball Bat", "Crowbar",
    "Hunting Knife", "Hand Axe", "Pickaxe", "Shovel", "Lead Pipe", "Metal Bar", "Metal Pipe",
    
    # Weaker melee weapons
    "Hammer", "Screwdriver", "Plank", "Rolling Pin", "Golf Club", "Nightstick", "Meat Cleaver",
    "Kitchen Knife", "Butter Knife", "Hand Scythe", "Garden Fork", "Hand Fork", "Trowel", "Broom", 
    "Rake", "Hoe", "Garden Hoe", "Wrench", "Pipe Wrench", "Frying Pan", "Saucepan",

    # Tools (least powerful weapons)
    "Stone Axe", "Wooden Spear", "Propane Torch", "Blowtorch", "Welding Mask", "Welding Rod"
]

# Variable to keep track of the index of the strongest weapon found so far
strongest_weapon_index = -1

# Step 1: Capture a screenshot using pyautogui
screenshot = pyautogui.screenshot()

# Step 2: Convert the screenshot to a numpy array for processing
screenshot_np = np.array(screenshot)

# Step 3: Convert RGB to BGR for OpenCV (EasyOCR accepts BGR format)
screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

# Step 4: Initialize EasyOCR Reader
reader = easyocr.Reader(['en'], gpu=False)  # Use the appropriate language code

# Step 5: Use EasyOCR to read text from the screenshot once
results = reader.readtext(screenshot_np)

# Step 6: Search for the strongest weapon and right-click on it
weapon_found = False  # Flag to indicate if we've found a weapon
for (bbox, text, prob) in results:
    # Check each word in the weapons list
    for i, weapon in enumerate(weapons):
        # Use regex to match the weapon name with any surrounding symbols
        if re.search(rf'\b{weapon}\b', text, re.IGNORECASE):  # Match weapon name case-insensitively
            # Check if this weapon is stronger (higher in the list) than the last detected one
            if i < strongest_weapon_index:  # This weapon is stronger, so we right-click
                # Extract the bounding box coordinates (bbox)
                (top_left, top_right, bottom_right, bottom_left) = bbox
                # Calculate the center of the detected text box
                center_x = int((top_left[0] + bottom_right[0]) / 2)
                center_y = int((top_left[1] + bottom_right[1]) / 2)
                
                # Move the mouse to the center of the detected text and right-click
                pyautogui.moveTo(center_x, center_y)
                pyautogui.rightClick()

                # Update the strongest weapon index to the current one
                strongest_weapon_index = i
                weapon_found = True
                print(f"Right-clicked on stronger weapon: {weapon} with confidence: {prob}")
                break  # Stop checking other weapons since we found the strongest one
    if weapon_found:
        break  # Stop searching other texts if the strongest weapon has been found

# Step 7: If the strongest weapon was found, look for "Equip in both hands" or "Equip primary"
if weapon_found:
    for (bbox, text, prob) in results:
        # First look for "Equip in both hands"
        if re.search(r'Equip in both hands', text, re.IGNORECASE):
            # Extract the bounding box coordinates (bbox) for "Equip in both hands"
            (top_left, top_right, bottom_right, bottom_left) = bbox
            center_x = int((top_left[0] + bottom_right[0]) / 2)
            center_y = int((top_left[1] + bottom_right[1]) / 2)
            
            # Move the mouse to the center of the detected text and left-click
            pyautogui.moveTo(center_x, center_y)
            pyautogui.click()

            print(f"Left-clicked on 'Equip in both hands' with confidence: {prob}")
            break  # Stop after finding and clicking "Equip in both hands"

        # If "Equip in both hands" is not found, look for "Equip primary"
        elif re.search(r'Equip primary', text, re.IGNORECASE):
            # Extract the bounding box coordinates (bbox) for "Equip primary"
            (top_left, top_right, bottom_right, bottom_left) = bbox
            center_x = int((top_left[0] + bottom_right[0]) / 2)
            center_y = int((top_left[1] + bottom_right[1]) / 2)
            
            # Move the mouse to the center of the detected text and left-click
            pyautogui.moveTo(center_x, center_y)
            pyautogui.click()

            print(f"Left-clicked on 'Equip primary' with confidence: {prob}")
            break  # Stop after finding and clicking "Equip primary"
