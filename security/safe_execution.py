from security.permissions import is_dangerous, is_blocked, get_confirmation_message
from security.confirmations import ask_confirmation
from pathlib import Path
from datetime import datetime
import json

LOG_FILE = Path.home() / '.hardik-agent' / 'security.log'

def log_action(action, command, result, confirmed=True):
    try:
        LOG_FILE.parent.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = {'timestamp': timestamp, 'action': action, 'command': command, 'result': result, 'confirmed': confirmed}
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception as e:
        print(f'Log error: {e}')

def safe_execute(action, command, execute_func):
    try:
        if is_blocked(action):
            log_action(action, command, 'BLOCKED', False)
            return f'Sorry, {action} is not allowed for safety reasons.'
        if is_dangerous(action):
            message = get_confirmation_message(action)
            confirmed = ask_confirmation(message)
            if not confirmed:
                log_action(action, command, 'CANCELLED', False)
                return 'Action cancelled.'
        result = execute_func()
        log_action(action, command, result, True)
        return result
    except Exception as e:
        log_action(action, command, f'ERROR: {e}', False)
        return f'Error: {e}'
