import subprocess
import time
import pyautogui
import pyperclip

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

def send_whatsapp(contact, message):
    try:
        print(f'Sending WhatsApp to {contact}: {message}')
        subprocess.Popen(['start', 'https://web.whatsapp.com'], shell=True)
        print('Opening WhatsApp Web - please wait...')
        time.sleep(8)
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1.5)
        pyperclip.copy(contact)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2.5)
        pyautogui.press('enter')
        time.sleep(1.5)
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')
        return f'Message sent to {contact} on WhatsApp'
    except Exception as e:
        return f'WhatsApp error: {e}'

def send_instagram(contact, message):
    try:
        print(f'Sending Instagram DM to {contact}: {message}')
        subprocess.Popen(['start', 'https://www.instagram.com/direct/new/'], shell=True)
        time.sleep(6)
        pyperclip.copy(contact)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('tab')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(1.5)
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')
        return f'Message sent to {contact} on Instagram'
    except Exception as e:
        return f'Instagram error: {e}'

def send_telegram(contact, message):
    try:
        print(f'Sending Telegram to {contact}: {message}')
        subprocess.Popen(['start', 'https://web.telegram.org'], shell=True)
        time.sleep(6)
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        pyperclip.copy(contact)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(1.5)
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')
        return f'Message sent to {contact} on Telegram'
    except Exception as e:
        return f'Telegram error: {e}'

def send_message(platform, contact, message):
    platform = platform.lower().strip()
    if platform == 'whatsapp':
        return send_whatsapp(contact, message)
    elif platform == 'instagram':
        return send_instagram(contact, message)
    elif platform == 'telegram':
        return send_telegram(contact, message)
    else:
        return f'Platform {platform} not supported yet'