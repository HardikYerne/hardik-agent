import json
import os
from pathlib import Path

SESSION_FILE = Path.home() / '.hardik-agent' / 'session.json'

def save_session(email):
    SESSION_FILE.parent.mkdir(exist_ok=True)
    with open(SESSION_FILE, 'w') as f:
        json.dump({'email': email, 'active': True}, f)

def is_session_active():
    try:
        if SESSION_FILE.exists():
            with open(SESSION_FILE) as f:
                session = json.load(f)
                return session.get('active', False)
    except:
        pass
    return False

def clear_session():
    try:
        if SESSION_FILE.exists():
            os.remove(SESSION_FILE)
    except:
        pass
