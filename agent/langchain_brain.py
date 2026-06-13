import ollama
import subprocess
import os
import psutil
import datetime
import socket
import pyautogui
import pyperclip
import json
import time

llm_model = 'llama3.2:1b'

def open_application(app_name):
    try:
        subprocess.Popen(['start', app_name], shell=True)
        return f'Opening {app_name}'
    except Exception as e:
        return f'Could not open {app_name}: {e}'

def open_website(url):
    try:
        if not url.startswith("http"):
            url = "https://" + url
        import subprocess
        subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", url])
        return f"Opening {url} in Chrome"
    except:
        pass
    try:
        if not url.startswith('http'):
            url = 'https://' + url
        subprocess.Popen(['start', url], shell=True)
        return f'Opening {url}'
    except Exception as e:
        return f'Could not open: {e}'

def search_google(query):
    url = f'https://www.google.com/search?q={query.replace(" ", "+")}'
    subprocess.Popen(['start', url], shell=True)
    return f'Searching Google for: {query}'

def search_youtube(query):
    url = f'https://www.youtube.com/results?search_query={query.replace(" ", "+")}'
    subprocess.Popen(['start', url], shell=True)
    return f'Searching YouTube for: {query}'

def send_whatsapp_message(contact, message):
    try:
        subprocess.Popen(['start', 'https://web.whatsapp.com'], shell=True)
        print('Opening WhatsApp Web...')
        time.sleep(8)
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        pyperclip.copy(contact)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(1)
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')
        return f'Message sent to {contact} on WhatsApp'
    except Exception as e:
        return f'Could not send message: {e}'

def get_battery():
    try:
        battery = psutil.sensors_battery()
        if battery:
            status = 'charging' if battery.power_plugged else 'not charging'
            return f'Battery is at {battery.percent}% and {status}'
        return 'Battery information not available'
    except Exception as e:
        return f'Error: {e}'

def get_cpu():
    try:
        cpu = psutil.cpu_percent(interval=1)
        return f'CPU usage is {cpu}%'
    except Exception as e:
        return f'Error: {e}'

def get_ram():
    try:
        ram = psutil.virtual_memory()
        used = round(ram.used/(1024**3), 2)
        total = round(ram.total/(1024**3), 2)
        return f'RAM usage is {used}GB of {total}GB at {ram.percent}%'
    except Exception as e:
        return f'Error: {e}'

def get_disk():
    try:
        disk = psutil.disk_usage('C:/')
        used = round(disk.used/(1024**3), 2)
        total = round(disk.total/(1024**3), 2)
        return f'Disk usage is {used}GB of {total}GB at {disk.percent}%'
    except Exception as e:
        return f'Error: {e}'

def get_time():
    now = datetime.datetime.now()
    return f'Current time is {now.strftime("%I:%M %p")} on {now.strftime("%A %B %d %Y")}'

def get_ip():
    try:
        ip = socket.gethostbyname(socket.gethostname())
        return f'Your IP address is {ip}'
    except Exception as e:
        return f'Error: {e}'

def control_system(action):
    try:
        if action == 'screenshot':
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            path = os.path.join(os.path.expanduser('~'), 'Desktop', f'screenshot_{timestamp}.png')
            pyautogui.screenshot().save(path)
            return 'Screenshot saved to Desktop'
        elif action == 'volume_up':
            for _ in range(5): pyautogui.press('volumeup')
            return 'Volume increased'
        elif action == 'volume_down':
            for _ in range(5): pyautogui.press('volumedown')
            return 'Volume decreased'
        elif action == 'mute':
            pyautogui.press('volumemute')
            return 'Volume muted'
        elif action == 'minimize':
            pyautogui.hotkey('win', 'down')
            return 'Window minimized'
        elif action == 'maximize':
            pyautogui.hotkey('win', 'up')
            return 'Window maximized'
        elif action == 'close_window':
            pyautogui.hotkey('alt', 'f4')
            return 'Window closed'
        elif action == 'show_desktop':
            pyautogui.hotkey('win', 'd')
            return 'Desktop shown'
        elif action == 'lock_screen':
            from security.safe_execution import safe_execute
            return safe_execute('lock_screen', 'lock screen', lambda: _lock_screen())
        elif action == 'shutdown':
            from security.safe_execution import safe_execute
            return safe_execute('shutdown', 'shutdown computer', lambda: _shutdown())
        return f'Unknown action: {action}'
    except Exception as e:
        return f'Error: {e}'

def _lock_screen():
    pyautogui.hotkey('win', 'l')
    return 'Screen locked'

def _shutdown():
    subprocess.run(['shutdown', '/s', '/t', '10'])
    return 'Shutting down in 10 seconds'

def create_folder(folder_name):
    try:
        path = os.path.join(os.path.expanduser('~'), 'Desktop', folder_name)
        os.makedirs(path, exist_ok=True)
        return f'Folder {folder_name} created on Desktop'
    except Exception as e:
        return f'Error: {e}'

SYSTEM_PROMPT = '''You are Hexa, an AI desktop assistant on Windows.
Respond with ONE line of JSON only. No extra text.

Rules:
- Only one JSON object
- No text before or after
- No double braces

Actions:
open any app -> {"action": "open_app", "value": "appname"}
open any website -> {"action": "open_web", "value": "site.com"}
search google -> {"action": "search_google", "value": "query"}
search youtube -> {"action": "search_youtube", "value": "query"}
whatsapp message -> {"action": "whatsapp", "contact": "name", "message": "text"}
battery -> {"action": "battery"}
cpu -> {"action": "cpu"}
ram -> {"action": "ram"}
disk -> {"action": "disk"}
time -> {"action": "time"}
ip -> {"action": "ip"}
screenshot -> {"action": "screenshot"}
volume up -> {"action": "volume_up"}
volume down -> {"action": "volume_down"}
mute -> {"action": "mute"}
minimize -> {"action": "minimize"}
maximize -> {"action": "maximize"}
close window -> {"action": "close_window"}
show desktop -> {"action": "show_desktop"}
lock screen -> {"action": "lock_screen"}
shutdown -> {"action": "shutdown"}
create folder -> {"action": "create_folder", "value": "name"}
conversation -> {"action": "talk", "value": "reply"}

APPS - use open_app:
chrome, firefox, edge, opera, brave -> browser
spotify, vlc, winamp, musicbee -> music
whatsapp, telegram, discord, slack, skype, zoom, teams -> communication
vscode, pycharm, intellij, notepad, notepad++, sublime -> coding
word, excel, powerpoint, onenote, outlook -> microsoft office
photoshop, illustrator, gimp, paint -> design
steam, epic, roblox, minecraft -> games
obs, streamlabs -> streaming
git, github desktop -> version control
postman -> api testing
android studio -> mobile dev
virtualbox, vmware -> virtual machine
7zip, winrar -> archive
vlc -> media player
task manager, taskmgr -> system
calculator, calc -> calculator
camera -> camera
settings -> settings
file explorer, explorer -> files
control panel -> control
cmd, command prompt -> terminal
powershell -> shell
paint -> drawing
snipping tool -> screenshot

WEBSITES - use open_web:
youtube.com -> youtube, yt
google.com -> google
gmail.com -> gmail
drive.google.com -> google drive
docs.google.com -> google docs
sheets.google.com -> google sheets
meet.google.com -> google meet
facebook.com -> facebook, fb
instagram.com -> instagram
twitter.com -> twitter, x
linkedin.com -> linkedin
whatsapp.com/web -> whatsapp web
web.whatsapp.com -> whatsapp web
telegram.org -> telegram web
discord.com -> discord web
netflix.com -> netflix
hotstar.com -> hotstar, disney hotstar
primevideo.com -> amazon prime, prime video
spotify.com -> spotify web
github.com -> github
stackoverflow.com -> stackoverflow
chatgpt.com -> chatgpt
claude.ai -> claude
gemini.google.com -> gemini
amazon.in -> amazon india
amazon.com -> amazon
flipkart.com -> flipkart
myntra.com -> myntra
swiggy.com -> swiggy
zomato.com -> zomato
paytm.com -> paytm
phonepe.com -> phonepe
gpay -> pay.google.com
sbi.co.in -> sbi
hdfcbank.com -> hdfc
icicibank.com -> icici
maps.google.com -> google maps
translate.google.com -> google translate
news.google.com -> google news
weather.com -> weather
reddit.com -> reddit
quora.com -> quora
medium.com -> medium
wikipedia.org -> wikipedia
canva.com -> canva
figma.com -> figma
notion.so -> notion
trello.com -> trello
zoom.us -> zoom web
udemy.com -> udemy
coursera.org -> coursera
leetcode.com -> leetcode
hackerrank.com -> hackerrank

Examples:
open spotify -> {"action": "open_app", "value": "spotify"}
open netflix -> {"action": "open_web", "value": "netflix.com"}
open whatsapp -> {"action": "open_app", "value": "whatsapp"}
open whatsapp web -> {"action": "open_web", "value": "web.whatsapp.com"}
open instagram -> {"action": "open_web", "value": "instagram.com"}
open gmail -> {"action": "open_web", "value": "gmail.com"}
open google drive -> {"action": "open_web", "value": "drive.google.com"}
open chatgpt -> {"action": "open_web", "value": "chatgpt.com"}
open youtube -> {"action": "open_web", "value": "youtube.com"}
open discord -> {"action": "open_app", "value": "discord"}
open telegram -> {"action": "open_app", "value": "telegram"}
open zoom -> {"action": "open_app", "value": "zoom"}
open vs code -> {"action": "open_app", "value": "code"}
open notepad -> {"action": "open_app", "value": "notepad"}
open calculator -> {"action": "open_app", "value": "calc"}
open file manager -> {"action": "open_app", "value": "explorer"}
open task manager -> {"action": "open_app", "value": "taskmgr"}
open settings -> {"action": "open_app", "value": "ms-settings:"}
open swiggy -> {"action": "open_web", "value": "swiggy.com"}
open zomato -> {"action": "open_web", "value": "zomato.com"}
open flipkart -> {"action": "open_web", "value": "flipkart.com"}
open amazon -> {"action": "open_web", "value": "amazon.in"}
open hotstar -> {"action": "open_web", "value": "hotstar.com"}
open prime video -> {"action": "open_web", "value": "primevideo.com"}
open google maps -> {"action": "open_web", "value": "maps.google.com"}
open translate -> {"action": "open_web", "value": "translate.google.com"}
search lofi on youtube -> {"action": "search_youtube", "value": "lofi"}
search python on google -> {"action": "search_google", "value": "python"}
what time is it -> {"action": "time"}
check battery -> {"action": "battery"}
check ram -> {"action": "ram"}
take screenshot -> {"action": "screenshot"}
increase volume -> {"action": "volume_up"}
shutdown -> {"action": "shutdown"}
hello -> {"action": "talk", "value": "Hello! How can I help you?"}'''

def extract_json(text):
    try:
        text = text.strip()
        while text.endswith('}}'):
            text = text[:-1]
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            json_str = text[start:end+1]
            return json.loads(json_str)
    except Exception as e:
        print(f'JSON error: {e}')
    return {'action': 'talk', 'value': 'I could not process that command.'}

def process_command(user_input: str) -> str:
    try:
        print(f'Processing: {user_input}')
        response = ollama.chat(
            model=llm_model,
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': user_input}
            ]
        )
        raw = response['message']['content'].strip()
        print(f'AI decision: {raw}')
        decision = extract_json(raw)
        action = decision.get('action', 'talk')

        if action == 'open_app':
            return open_application(decision.get('value', ''))
        elif action == 'open_web':
            return open_website(decision.get('value', ''))
        elif action == 'search_google':
            return search_google(decision.get('value', ''))
        elif action == 'search_youtube':
            return search_youtube(decision.get('value', ''))
        elif action == 'whatsapp':
            contact = decision.get('contact', '')
            message = decision.get('message', '')
            if contact and message:
                return send_whatsapp_message(contact, message)
            return 'Please say contact name and message.'
        elif action == 'battery':
            return get_battery()
        elif action == 'cpu':
            return get_cpu()
        elif action == 'ram':
            return get_ram()
        elif action == 'disk':
            return get_disk()
        elif action == 'time':
            return get_time()
        elif action == 'ip':
            return get_ip()
        elif action == 'screenshot':
            return control_system('screenshot')
        elif action == 'volume_up':
            return control_system('volume_up')
        elif action == 'volume_down':
            return control_system('volume_down')
        elif action == 'mute':
            return control_system('mute')
        elif action == 'minimize':
            return control_system('minimize')
        elif action == 'maximize':
            return control_system('maximize')
        elif action == 'close_window':
            return control_system('close_window')
        elif action == 'show_desktop':
            return control_system('show_desktop')
        elif action == 'lock_screen':
            return control_system('lock_screen')
        elif action == 'shutdown':
            return control_system('shutdown')
        elif action == 'create_folder':
            return create_folder(decision.get('value', 'New Folder'))
        elif action == 'talk':
            return decision.get('value', 'How can I help you?')
        else:
            return 'How can I help you?'

    except Exception as e:
        print(f'Error: {e}')
        return 'I could not process that command.'



