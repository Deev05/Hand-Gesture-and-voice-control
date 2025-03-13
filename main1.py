import cv2
import pyautogui
import time
from hand_tracking import HandTracker
from voice_assistant import VoiceAssistant
import webbrowser
# Initialize the hand tracker and voice assistant
tracker = HandTracker()
assistant = VoiceAssistant()

# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False

# Screen dimensions
screen_width, screen_height = pyautogui.size()

# Initialize states
click_threshold = 0.05
double_click_time = 0.3
last_click_time = 0
last_double_click_time = 0
scroll_threshold = 0.15
scroll_speed = 100
voice_mode = False  # Start in gesture control mode

cap = cv2.VideoCapture(0)
def open_browser():
    """Function to open the default web browser."""
    webbrowser.open("https://www.google.com")
    print("Browser opened!")

def handle_voice_command(command):
    """Handles voice commands to switch modes or trigger actions."""
    global voice_mode
    command = command.lower()  # Normalize command for better matching
    if "cursor" in command or "gesture" in command:
        assistant.speak("Switching to cursor control mode.")
        print("[INFO] Gesture control mode activated.")
        voice_mode = False
    elif "voice" in command:
        assistant.speak("Switching to voice control mode.")
        print("[INFO] Voice control mode activated.")
        voice_mode = True
    elif "browser" in command:
        assistant.speak("Opening the web browser.")
        pyautogui.hotkey("ctrl", "t")
        open_browser()
    elif "close program" in command:
        assistant.speak("Closing the program. Goodbye!")
        print("[INFO] Program exited via voice command.")
        exit()


while True:
    success, img = cap.read()
    if not success:
        break

    if voice_mode:
        assistant.speak("Voice control mode active. Say a command.")
        command = assistant.listen()
        assistant.perform_task(command)
    else:
        # Display gesture mode status
        cv2.putText(img, "GESTURE MODE ACTIVE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Gesture control mode
        img, results = tracker.find_hands(img)
        landmarks = tracker.get_landmarks(results)

        if landmarks:
            # Get positions of index (8) and middle (12) fingers
            index_finger = landmarks[8]
            middle_finger = landmarks[12]

            # Map coordinates to screen size
            cursor_x = int(index_finger[0] * screen_width)
            cursor_y = int(index_finger[1] * screen_height)*1.5

            # Flip cursor horizontally for mirrored effect
            cursor_x = (screen_width - cursor_x)*1.5

            # Calculate distances
            finger_distance = tracker.calculate_distance(index_finger, middle_finger)

            # Detect click on finger tap
            if finger_distance < click_threshold:
                current_time = time.time()
                if current_time - last_click_time > 0.3:
                    pyautogui.click()
                    last_click_time = current_time

                # Double-click
                if current_time - last_double_click_time < double_click_time:
                    pyautogui.doubleClick()
                    last_double_click_time = current_time

            # Scrolling based on hand movement
            hand_movement = index_finger[1] - middle_finger[1]
            if hand_movement > scroll_threshold:
                pyautogui.scroll(-scroll_speed)
            elif hand_movement < -scroll_threshold:
                pyautogui.scroll(scroll_speed)

            # Move the cursor naturally (mirrored movement)
            pyautogui.moveTo(cursor_x, cursor_y)

    # Show webcam feed
    cv2.imshow("Gesture-Based Cursor Control", img)

    # Key press to switch modes
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Exit on 'q'
        break
    elif key == ord('v'):  # Activate voice mode on 'v'
        if not voice_mode:
            voice_mode = True
            assistant.speak("Voice mode activated.")
            print("[INFO] Voice mode activated.")
    elif key == ord('g'):  # Activate gesture mode on 'g'
        if voice_mode:
            voice_mode = False
            assistant.speak("Gesture mode activated.")
            print("[INFO] Gesture mode activated.")

cap.release()
cv2.destroyAllWindows()