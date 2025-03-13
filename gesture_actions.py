import pyautogui
import screen_brightness_control as sbc

def adjust_brightness(direction):
    """Adjust screen brightness based on direction."""
    current_brightness = sbc.get_brightness()[0]
    if direction == "up":
        sbc.set_brightness(min(100, current_brightness + 10))
    elif direction == "down":
        sbc.set_brightness(max(0, current_brightness - 10))

def zoom(action):
    """Zoom in or out."""
    if action == "in":
        pyautogui.hotkey('ctrl', '+')  # Ctrl + '+' to zoom in
    elif action == "out":
        pyautogui.hotkey('ctrl', '-')  # Ctrl + '-' to zoom out

def trackpad_move(direction):
    """Simulate trackpad movement."""
    if direction == "left":
        pyautogui.move(-50, 0)
    elif direction == "right":
        pyautogui.move(50, 0)
    elif direction == "up":
        pyautogui.move(0, -50)
    elif direction == "down":
        pyautogui.move(0, 50)

def application_shortcut(action):
    """Switch applications."""
    if action == "next":
        pyautogui.hotkey('alt', 'tab')  # Switch to the next window
    elif action == "previous":
        pyautogui.hotkey('alt', 'shift', 'tab')  # Switch to the previous window
