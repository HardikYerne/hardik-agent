import pyautogui
import os
import datetime

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

def take_screenshot():
    try:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        path = os.path.join(os.path.expanduser('~'), 'Desktop', f'screenshot_{timestamp}.png')
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        return f'Screenshot saved to Desktop'
    except Exception as e:
        return f'Screenshot failed: {e}'

def increase_volume():
    for _ in range(5):
        pyautogui.press('volumeup')
    return 'Volume increased'

def decrease_volume():
    for _ in range(5):
        pyautogui.press('volumedown')
    return 'Volume decreased'

def mute_volume():
    pyautogui.press('volumemute')
    return 'Volume muted'

def minimize_window():
    pyautogui.hotkey('win', 'down')
    return 'Window minimized'

def maximize_window():
    pyautogui.hotkey('win', 'up')
    return 'Window maximized'

def close_window():
    pyautogui.hotkey('alt', 'f4')
    return 'Window closed'

def show_desktop():
    pyautogui.hotkey('win', 'd')
    return 'Desktop shown'

def lock_screen():
    pyautogui.hotkey('win', 'l')
    return 'Screen locked'
