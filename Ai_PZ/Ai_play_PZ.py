import pyautogui
import keyboard
import time
import cv2
import numpy as np
import easyocr
import math

# Configuration Settings
WEIGHT_THRESHOLD = 15  # Adjust as needed
ZOMBIE_DETECTION_REGION = (500, 300, 400, 400)  # Example values
PLAYER_DETECTION_REGION = (600, 500, 200, 200)  # Example values
STORAGE_DETECTION_REGION = (100, 100, 300, 300)  # Example values
INVENTORY_REGION = (200, 200, 400, 400)  # Example values
HEALTH_BAR_REGION = (50, 50, 200, 50)  # Example values
WEAPON_KEYWORDS = [
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
DROP_ITEMS = ["rock", "branch", "ripped sheets"]

reader = easyocr.Reader(['en'])

def take_screenshot(region=None):
    screenshot = pyautogui.screenshot(region=region)
    return np.array(screenshot)

# Optimize storage detection using template matching
def detect_storage():
    screenshot = take_screenshot(STORAGE_DETECTION_REGION)
    template = cv2.imread("storage_template.png", 0)
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    res = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)
    return max_val > 0.8  # Adjust confidence threshold if needed

# Enhanced zombie detection using contour analysis
def detect_zombies():
    screenshot = take_screenshot(ZOMBIE_DETECTION_REGION)
    gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return len(contours) > 5  # Adjust threshold

# Combat movement (strafe, dodge, step back)
def combat_movement():
    keyboard.press('shift')
    keyboard.press('left')
    time.sleep(0.3)
    keyboard.release('left')
    keyboard.press('right')
    time.sleep(0.3)
    keyboard.release('right')
    keyboard.release('shift')

def attack_zombies():
    keyboard.press('control')
    while detect_zombies():
        pyautogui.click()
        combat_movement()  # Move while attacking
    keyboard.release('control')

# Inventory optimization (prioritize weapons, drop heavy items)
def optimize_inventory():
    pyautogui.press('i')
    time.sleep(0.5)
    for _ in range(5):
        pyautogui.scroll(-500)
        time.sleep(0.5)
        screenshot = take_screenshot(region=INVENTORY_REGION)
        inventory_text = reader.readtext(screenshot, detail=0)
        for item in inventory_text:
            if any(weapon in item.lower() for weapon in WEAPON_KEYWORDS):
                return True  # Found a weapon
    return False

def drop_heavy_items():
    pyautogui.press('i')
    time.sleep(0.5)
    for _ in range(3):
        pyautogui.scroll(-500)
        screenshot = take_screenshot(region=INVENTORY_REGION)
        inventory_text = reader.readtext(screenshot, detail=0)
        for item in inventory_text:
            if any(word in item.lower() for word in DROP_ITEMS):
                pyautogui.rightClick()
                time.sleep(0.5)
                pyautogui.press('d')  # Drop item shortcut
    pyautogui.press('i')

# Auto-bandage if injured
def check_health():
    screenshot = take_screenshot(region=HEALTH_BAR_REGION)
    health_text = reader.readtext(screenshot, detail=0)
    if "injured" in health_text or "bleeding" in health_text:
        pyautogui.press('h')  # Bandage shortcut

def game_automation_logic():
    if not optimize_inventory():
        if detect_storage():
            print("Looting for weapons")
        else:
            print("No weapons, fleeing!")
            keyboard.press('shift')
            keyboard.press('left')
            time.sleep(1.5)
            keyboard.release('left')
            keyboard.release('shift')
            return
    check_health()
    if detect_zombies():
        attack_zombies()

def main():
    while True:
        game_automation_logic()

if __name__ == "__main__":
    main()
