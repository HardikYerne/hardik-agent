import ollama
import json
import re
from tools.tool_registry import execute_tool

SYSTEM_PROMPT = '''
You are Hardik Agent, an AI desktop assistant.
You control the user computer using available tools.

Available tools:
- open_chrome: opens Google Chrome browser
- open_browser: opens browser
- open_vscode: opens Visual Studio Code
- open_notepad: opens Notepad text editor
- open_file_manager: opens File Explorer
- open_task_manager: opens Task Manager
- open_calculator: opens Calculator
- open_settings: opens Windows Settings
- create_folder: creates a new folder on Desktop
- shutdown_pc: shuts down the computer
- take_screenshot: takes a screenshot
- open_youtube: opens YouTube
- open_gmail: opens Gmail

When user gives a command, respond with ONLY this JSON format:
{"tool": "tool_name"}

If user is just talking or no tool matches respond with:
{"tool": "none", "response": "friendly reply to user"}

IMPORTANT: Always respond with valid JSON only. Nothing else.
'''

def extract_json(text):
    try:
        # find first { and last }
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            json_str = text[start:end+1]
            return json.loads(json_str)
    except:
        pass
    return {'tool': 'none', 'response': 'I could not process that command.'}

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
        return {'tool': 'none', 'response': 'I could not process that command.'}

def process_command(user_input):
    print(f'Processing: {user_input}')
    decision = think(user_input)
    tool_name = decision.get('tool', 'none')
    if tool_name == 'none':
        return decision.get('response', 'How can I help you?')
    result = execute_tool(tool_name)
    return result
