import ollama
import json
import subprocess
import os
from tools.tool_registry import execute_tool

SYSTEM_PROMPT = '''
You are Hardik Agent, a powerful AI desktop assistant.
You control the user Windows computer.

You can do ANYTHING the user asks. Think intelligently.

For opening any app respond with:
{"action": "open_app", "app": "app name"}

For opening any website respond with:
{"action": "open_url", "url": "website.com"}

For searching Google respond with:
{"action": "search_google", "query": "search words"}

For searching YouTube respond with:
{"action": "search_youtube", "query": "search words"}

For system tools respond with:
{"action": "system", "tool": "tool_name"}

System tools available:
get_battery, get_cpu, get_ram, get_disk,
get_time, get_ip, take_screenshot,
increase_volume, decrease_volume, mute_volume,
minimize_window, maximize_window, close_window,
show_desktop, lock_screen, shutdown_pc,
open_file_manager, open_task_manager,
open_calculator, open_settings, create_folder

For conversation respond with:
{"action": "talk", "response": "your reply"}

Examples:
User: "open whatsapp"
You: {"action": "open_app", "app": "whatsapp"}

User: "open spotify"
You: {"action": "open_app", "app": "spotify"}

User: "open telegram"
You: {"action": "open_app", "app": "telegram"}

User: "open vs code"
You: {"action": "open_app", "app": "code"}

User: "open chrome"
You: {"action": "open_app", "app": "chrome"}

User: "open notepad"
You: {"action": "open_app", "app": "notepad"}

User: "open netflix"
You: {"action": "open_url", "url": "netflix.com"}

User: "open chatgpt"
You: {"action": "open_url", "url": "chatgpt.com"}

User: "open instagram"
You: {"action": "open_url", "url": "instagram.com"}

User: "search lofi music on youtube"
You: {"action": "search_youtube", "query": "lofi music"}

User: "search python tutorial on google"
You: {"action": "search_google", "query": "python tutorial"}

User: "what time is it"
You: {"action": "system", "tool": "get_time"}

User: "check battery"
You: {"action": "system", "tool": "get_battery"}

User: "take screenshot"
You: {"action": "system", "tool": "take_screenshot"}

User: "hello"
You: {"action": "talk", "response": "Hello! How can I help you?"}

IMPORTANT: Always respond with valid JSON only. Nothing else.
'''

def extract_json(text):
    try:
        text = text.strip()
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            json_str = text[start:end+1]
            json_str = json_str.replace('}}', '}').replace('{{', '{')
            return json.loads(json_str)
    except Exception as e:
        print(f'JSON parse error: {e}')
    return {'action': 'talk', 'response': 'I could not process that command.'}

def open_any_app(app_name):
    try:
        app_name = app_name.lower().strip()
        result = subprocess.Popen(
            ['start', app_name],
            shell=True
        )
        return f'Opening {app_name}'
    except Exception as e:
        return f'Could not open {app_name}: {e}'

def open_any_url(url):
    try:
        if not url.startswith('http'):
            url = 'https://' + url
        subprocess.Popen(['start', url], shell=True)
        return f'Opening {url}'
    except Exception as e:
        return f'Could not open {url}: {e}'

def search_google(query):
    url = f'https://www.google.com/search?q={query.replace(" ", "+")}'
    subprocess.Popen(['start', url], shell=True)
    return f'Searching Google for: {query}'

def search_youtube(query):
    url = f'https://www.youtube.com/results?search_query={query.replace(" ", "+")}'
    subprocess.Popen(['start', url], shell=True)
    return f'Searching YouTube for: {query}'

def think(user_input):
    try:
        response = ollama.chat(
            model='llama3.2:1b',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': user_input}
            ]
        )
        raw = response['message']['content'].strip()
        print(f'AI decision: {raw}')
        result = extract_json(raw)
        return result
    except Exception as e:
        print(f'Brain error: {e}')
        return {'action': 'talk', 'response': 'I could not process that command.'}

def process_command(user_input):
    print(f'Processing: {user_input}')

    if len(user_input.strip()) < 3:
        return 'Please say your command clearly.'

    decision = think(user_input)
    action = decision.get('action', 'talk')

    if action == 'open_app':
        app = decision.get('app', '')
        if app:
            return open_any_app(app)
        return 'Which app do you want to open?'

    elif action == 'open_url':
        url = decision.get('url', '')
        if url:
            return open_any_url(url)
        return 'Which website do you want to open?'

    elif action == 'search_google':
        query = decision.get('query', '')
        if query:
            return search_google(query)
        return 'What do you want to search?'

    elif action == 'search_youtube':
        query = decision.get('query', '')
        if query:
            return search_youtube(query)
        return 'What do you want to search on YouTube?'

    elif action == 'system':
        tool = decision.get('tool', '')
        if tool:
            return execute_tool(tool)
        return 'What system task do you want?'

    elif action == 'talk':
        return decision.get('response', 'How can I help you?')

    else:
        return execute_tool(action)
