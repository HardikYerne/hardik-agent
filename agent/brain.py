import ollama
import json
from tools.tool_registry import execute_tool

SYSTEM_PROMPT = '''
You are Hardik Agent, an AI desktop assistant.
You control the user computer using available tools.

Available tools:
- open_chrome: opens Google Chrome browser
- open_vscode: opens Visual Studio Code
- open_notepad: opens Notepad
- create_folder: creates a new folder on Desktop
- shutdown_pc: shuts down the computer

When user gives a command, respond with ONLY this JSON format:
{"tool": "tool_name"}

If no tool matches respond with:
{"tool": "none", "response": "your message"}

IMPORTANT: Always respond with valid JSON only. Nothing else.
'''

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
        result = json.loads(raw)
        return result
    except Exception as e:
        print(f'Brain error: {e}')
        return {'tool': 'none', 'response': 'I could not process that command.'}

def process_command(user_input):
    print(f'Processing: {user_input}')
    decision = think(user_input)
    tool_name = decision.get('tool', 'none')
    if tool_name == 'none':
        return decision.get('response', 'I did not understand that command.')
    result = execute_tool(tool_name)
    return result
