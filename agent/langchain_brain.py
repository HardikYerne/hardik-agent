
def handle_eye_control(user_input):
    user_input = user_input.lower()
    if any(word in user_input for word in ['start', 'enable', 'open', 'turn on']):
        from automation.eye_control import start_eye_control
        return start_eye_control()
    elif any(word in user_input for word in ['stop', 'disable', 'close', 'turn off']):
        from automation.eye_control import stop_eye_control
        return stop_eye_control()
    return None
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
from agent.conversation import context

llm_model = 'llama3.2:1b'

def open_application(app_name):
    try:
        subprocess.Popen(['start', app_name], shell=True)
        context.set_app(app_name)
        return f'Opening {app_name}'
    except Exception as e:
        return f'Could not open {app_name}: {e}'

def open_website(url):
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

def send_platform_message(platform, contact, message):
    from automation.messaging import send_message
    context.set_platform(platform)
    context.set_contact(contact)
    return send_message(platform, contact, message)

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
        return f'CPU usage is {psutil.cpu_percent(interval=1)}%'
    except Exception as e:
        return f'Error: {e}'

def get_ram():
    try:
        ram = psutil.virtual_memory()
        return f'RAM usage is {round(ram.used/(1024**3),2)}GB of {round(ram.total/(1024**3),2)}GB at {ram.percent}%'
    except Exception as e:
        return f'Error: {e}'

def get_disk():
    try:
        disk = psutil.disk_usage('C:/')
        return f'Disk usage is {round(disk.used/(1024**3),2)}GB of {round(disk.total/(1024**3),2)}GB at {disk.percent}%'
    except Exception as e:
        return f'Error: {e}'

def get_time():
    now = datetime.datetime.now()
    return f'Current time is {now.strftime("%I:%M %p")} on {now.strftime("%A %B %d %Y")}'

def get_ip():
    try:
        return f'Your IP address is {socket.gethostbyname(socket.gethostname())}'
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
            return safe_execute('lock_screen', 'lock screen', lambda: _lock())
        elif action == 'shutdown':
            from security.safe_execution import safe_execute
            return safe_execute('shutdown', 'shutdown', lambda: _shutdown())
        return f'Unknown action: {action}'
    except Exception as e:
        return f'Error: {e}'

def _lock():
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

def build_system_prompt():
    ctx = context.get_context_summary()
    current = ''
    if context.current_platform:
        current += f'Current platform: {context.current_platform}\n'
    if context.current_contact:
        current += f'Current contact: {context.current_contact}\n'
    if context.current_app:
        current += f'Current app: {context.current_app}\n'

    return f'''You are Hexa, an AI desktop assistant on Windows.
Respond with ONE line of JSON only. No extra text. No double braces.

{ctx}
{current}

IMPORTANT CONTEXT RULES:
- If user says "open mummy" or "open john" after opening whatsapp - they want to open that contact chat
- If user says "send message hi" after opening a contact - send that message to current contact
- If user says a name after opening a messaging app - that is the contact name
- Remember the context from previous commands

Actions:
open any app -> {{"action": "open_app", "value": "appname"}}
open any website -> {{"action": "open_web", "value": "site.com"}}
search google -> {{"action": "search_google", "value": "query"}}
search youtube -> {{"action": "search_youtube", "value": "query"}}
send message -> {{"action": "message", "platform": "whatsapp", "contact": "name", "message": "text"}}
open contact chat -> {{"action": "open_contact", "platform": "whatsapp", "contact": "name"}}
send to current contact -> {{"action": "send_current", "message": "text"}}
battery -> {{"action": "battery"}}
cpu -> {{"action": "cpu"}}
ram -> {{"action": "ram"}}
disk -> {{"action": "disk"}}
time -> {{"action": "time"}}
ip -> {{"action": "ip"}}
screenshot -> {{"action": "screenshot"}}
volume up -> {{"action": "volume_up"}}
volume down -> {{"action": "volume_down"}}
mute -> {{"action": "mute"}}
minimize -> {{"action": "minimize"}}
maximize -> {{"action": "maximize"}}
close window -> {{"action": "close_window"}}
show desktop -> {{"action": "show_desktop"}}
lock screen -> {{"action": "lock_screen"}}
shutdown -> {{"action": "shutdown"}}
create folder -> {{"action": "create_folder", "value": "name"}}
conversation -> {{"action": "talk", "value": "reply"}}

Examples:
open whatsapp web -> {{"action": "open_web", "value": "web.whatsapp.com"}}
open mummy [after whatsapp opened] -> {{"action": "open_contact", "platform": "whatsapp", "contact": "mummy"}}
send message hi [after contact opened] -> {{"action": "send_current", "message": "hi"}}
open john on whatsapp -> {{"action": "open_contact", "platform": "whatsapp", "contact": "john"}}
send whatsapp to rahul hello -> {{"action": "message", "platform": "whatsapp", "contact": "rahul", "message": "hello"}}
send instagram message to priya how are you -> {{"action": "message", "platform": "instagram", "contact": "priya", "message": "how are you"}}
send telegram to dad coming home -> {{"action": "message", "platform": "telegram", "contact": "dad", "message": "coming home"}}
open netflix -> {{"action": "open_web", "value": "netflix.com"}}
open chrome -> {{"action": "open_app", "value": "chrome"}}
search lofi on youtube -> {{"action": "search_youtube", "value": "lofi"}}
what time is it -> {{"action": "time"}}
check battery -> {{"action": "battery"}}
take screenshot -> {{"action": "screenshot"}}
increase volume -> {{"action": "volume_up"}}
hello -> {{"action": "talk", "value": "Hello! How can I help you?"}}
'''

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

def open_contact_chat(platform, contact):
    try:
        import pyautogui
        import pyperclip
        import time

        context.set_platform(platform)
        context.set_contact(contact)

        print(f'Opening {contact} chat on {platform}')
        time.sleep(1)

        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        pyperclip.copy(contact)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(1)

        return f'Opened {contact} chat on {platform}. What message do you want to send?'
    except Exception as e:
        return f'Could not open contact: {e}'

def send_to_current_contact(message):
    try:
        import pyautogui
        import pyperclip
        import time

        if not context.current_contact:
            return 'No contact selected. Please say who to send to.'

        print(f'Sending to {context.current_contact}: {message}')
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')

        contact = context.current_contact
        return f'Message sent to {contact}'
    except Exception as e:
        return f'Could not send message: {e}'

def process_command(user_input: str) -> str:
    try:
        print(f'Processing: {user_input}')

        if 'eye' in user_input.lower():
            result = handle_eye_control(user_input)
            if result:
                return result

        if len(user_input.strip()) < 3:
            return 'Please say your command clearly.'

        system_prompt = build_system_prompt()
        response = ollama.chat(
            model=llm_model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_input}
            ]
        )
        raw = response['message']['content'].strip()
        print(f'AI decision: {raw}')
        decision = extract_json(raw)
        action = decision.get('action', 'talk')

        result = 'How can I help you?'

        if 'eye control' in user_input.lower() or 'eye tracking' in user_input.lower():
            if any(word in user_input.lower() for word in ['start', 'enable', 'open', 'turn on']):
                from automation.eye_control import start_eye_control
                return start_eye_control()
            elif any(word in user_input.lower() for word in ['stop', 'disable', 'close', 'turn off']):
                from automation.eye_control import stop_eye_control
                return stop_eye_control()

        if action == 'open_app':
            result = open_application(decision.get('value', ''))

        elif action == 'open_web':
            url = decision.get('value', '')
            result = open_website(url)
            if 'whatsapp' in url:
                context.set_platform('whatsapp')
            elif 'instagram' in url:
                context.set_platform('instagram')
            elif 'telegram' in url:
                context.set_platform('telegram')

        elif action == 'search_google':
            result = search_google(decision.get('value', ''))

        elif action == 'search_youtube':
            result = search_youtube(decision.get('value', ''))

        elif action == 'message':
            platform = decision.get('platform', context.current_platform or 'whatsapp')
            contact = decision.get('contact', '')
            message = decision.get('message', '')
            if contact and message:
                result = send_platform_message(platform, contact, message)
            else:
                result = 'Please say the contact name and message.'

        elif action == 'open_contact':
            platform = decision.get('platform', context.current_platform or 'whatsapp')
            contact = decision.get('contact', '')
            if contact:
                result = open_contact_chat(platform, contact)
            else:
                result = 'Please say the contact name.'

        elif action == 'send_current':
            message = decision.get('message', '')
            if message:
                result = send_to_current_contact(message)
            else:
                result = 'What message do you want to send?'

        elif action == 'battery':
            result = get_battery()
        elif action == 'cpu':
            result = get_cpu()
        elif action == 'ram':
            result = get_ram()
        elif action == 'disk':
            result = get_disk()
        elif action == 'time':
            result = get_time()
        elif action == 'ip':
            result = get_ip()
        elif action == 'screenshot':
            result = control_system('screenshot')
        elif action == 'volume_up':
            result = control_system('volume_up')
        elif action == 'volume_down':
            result = control_system('volume_down')
        elif action == 'mute':
            result = control_system('mute')
        elif action == 'minimize':
            result = control_system('minimize')
        elif action == 'maximize':
            result = control_system('maximize')
        elif action == 'close_window':
            result = control_system('close_window')
        elif action == 'show_desktop':
            result = control_system('show_desktop')
        elif action == 'lock_screen':
            result = control_system('lock_screen')
        elif action == 'shutdown':
            result = control_system('shutdown')
        elif action == 'create_folder':
            result = create_folder(decision.get('value', 'New Folder'))
        elif action == 'eye_control_start':
            from automation.eye_control import start_eye_control
            result = start_eye_control()

        elif action == 'eye_control_stop':
            from automation.eye_control import stop_eye_control
            result = stop_eye_control()

        elif action == 'talk':
            result = decision.get('value', 'How can I help you?')

        context.update(user_input, action, result)
        return result

    except Exception as e:
        print(f'Error: {e}')
        return 'I could not process that command.'