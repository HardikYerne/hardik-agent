import os
import sys
import subprocess
from pathlib import Path

def add_to_startup():
    try:
        project_path = Path(__file__).parent.parent
        python_path = sys.executable

        bat_content = f'@echo off\ncd /d "{project_path}"\nstart /min "" "{python_path}" main.py start\n'

        startup_folder = Path(os.environ['APPDATA']) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Startup'
        shortcut_path = startup_folder / 'HardikAgent.bat'

        with open(shortcut_path, 'w') as f:
            f.write(bat_content)

        return f'Hardik Agent will now start automatically on Windows boot'
    except Exception as e:
        return f'Could not add to startup: {e}'

def remove_from_startup():
    try:
        startup_folder = Path(os.environ['APPDATA']) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Startup'
        shortcut_path = startup_folder / 'HardikAgent.bat'
        if shortcut_path.exists():
            os.remove(shortcut_path)
            return 'Hardik Agent removed from startup'
        return 'Hardik Agent was not in startup'
    except Exception as e:
        return f'Could not remove from startup: {e}'

def is_in_startup():
    try:
        startup_folder = Path(os.environ['APPDATA']) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Startup'
        shortcut_path = startup_folder / 'HardikAgent.bat'
        return shortcut_path.exists()
    except:
        return False
