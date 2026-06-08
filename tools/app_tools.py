import subprocess
import os
import sys
from rich.console import Console

console = Console()

def open_chrome():
    try:
        if sys.platform == 'win32':
            subprocess.Popen(['start', 'chrome'], shell=True)
        elif sys.platform == 'linux':
            subprocess.Popen(['google-chrome'])
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', '-a', 'Google Chrome'])
        console.print('[green]Chrome opened successfully.[/green]')
        return 'Chrome opened successfully'
    except Exception as e:
        return f'Could not open Chrome: {e}'

def open_vscode():
    try:
        subprocess.Popen(['code', '.'], shell=True)
        console.print('[green]VS Code opened successfully.[/green]')
        return 'VS Code opened successfully'
    except Exception as e:
        return f'Could not open VS Code: {e}'

def open_notepad():
    try:
        if sys.platform == 'win32':
            subprocess.Popen(['notepad.exe'])
        elif sys.platform == 'linux':
            subprocess.Popen(['gedit'])
        console.print('[green]Notepad opened successfully.[/green]')
        return 'Notepad opened successfully'
    except Exception as e:
        return f'Could not open Notepad: {e}'

def open_file_manager():
    try:
        if sys.platform == 'win32':
            subprocess.Popen(['explorer.exe'])
        elif sys.platform == 'linux':
            subprocess.Popen(['nautilus'])
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', '-a', 'Finder'])
        console.print('[green]File manager opened successfully.[/green]')
        return 'File manager opened successfully'
    except Exception as e:
        return f'Could not open file manager: {e}'

def open_task_manager():
    try:
        if sys.platform == 'win32':
            subprocess.Popen(['taskmgr.exe'])
        console.print('[green]Task manager opened successfully.[/green]')
        return 'Task manager opened successfully'
    except Exception as e:
        return f'Could not open task manager: {e}'

def open_calculator():
    try:
        if sys.platform == 'win32':
            subprocess.Popen(['calc.exe'])
        elif sys.platform == 'linux':
            subprocess.Popen(['gnome-calculator'])
        console.print('[green]Calculator opened successfully.[/green]')
        return 'Calculator opened successfully'
    except Exception as e:
        return f'Could not open calculator: {e}'

def open_settings():
    try:
        if sys.platform == 'win32':
            subprocess.Popen(['ms-settings:'], shell=True)
        console.print('[green]Settings opened successfully.[/green]')
        return 'Settings opened successfully'
    except Exception as e:
        return f'Could not open settings: {e}'

def open_browser():
    return open_chrome()

def create_folder(folder_name='New Folder'):
    try:
        path = os.path.join(os.path.expanduser('~'), 'Desktop', folder_name)
        os.makedirs(path, exist_ok=True)
        console.print(f'[green]Folder created on Desktop.[/green]')
        return f'Folder {folder_name} created on Desktop'
    except Exception as e:
        return f'Could not create folder: {e}'

def shutdown_pc():
    try:
        if sys.platform == 'win32':
            subprocess.run(['shutdown', '/s', '/t', '10'])
        elif sys.platform == 'linux':
            subprocess.run(['shutdown', '-h', '+1'])
        return 'Shutting down in 10 seconds'
    except Exception as e:
        return f'Could not shutdown: {e}'

def take_screenshot():
    try:
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        path = os.path.join(os.path.expanduser('~'), 'Desktop', f'screenshot_{timestamp}.png')
        import pyautogui
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        return f'Screenshot saved to Desktop'
    except Exception as e:
        return f'Could not take screenshot: {e}'

def open_youtube():
    try:
        if sys.platform == 'win32':
            subprocess.Popen(['start', 'https://youtube.com'], shell=True)
        return 'Opening YouTube'
    except Exception as e:
        return f'Could not open YouTube: {e}'

def open_gmail():
    try:
        if sys.platform == 'win32':
            subprocess.Popen(['start', 'https://gmail.com'], shell=True)
        return 'Opening Gmail'
    except Exception as e:
        return f'Could not open Gmail: {e}'
