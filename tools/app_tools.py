import subprocess
import os
import sys
from rich.console import Console

console = Console()

def open_chrome():
    try:
        if sys.platform == "win32":
            subprocess.Popen(["start", "chrome"], shell=True)
        elif sys.platform == "linux":
            subprocess.Popen(["google-chrome"])
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-a", "Google Chrome"])
        console.print("[green]Chrome opened successfully.[/green]")
        return "Chrome opened successfully"
    except Exception as e:
        return f"Could not open Chrome: {e}"

def open_vscode():
    try:
        subprocess.Popen(["code", "."], shell=True)
        console.print("[green]VS Code opened successfully.[/green]")
        return "VS Code opened successfully"
    except Exception as e:
        return f"Could not open VS Code: {e}"

def open_notepad():
    try:
        if sys.platform == "win32":
            subprocess.Popen(["notepad.exe"])
        elif sys.platform == "linux":
            subprocess.Popen(["gedit"])
        console.print("[green]Notepad opened successfully.[/green]")
        return "Notepad opened successfully"
    except Exception as e:
        return f"Could not open Notepad: {e}"

def create_folder(folder_name="New Folder"):
    try:
        path = os.path.join(os.path.expanduser("~"), "Desktop", folder_name)
        os.makedirs(path, exist_ok=True)
        console.print(f"[green]Folder '{folder_name}' created on Desktop.[/green]")
        return f"Folder {folder_name} created"
    except Exception as e:
        return f"Could not create folder: {e}"

def shutdown_pc():
    try:
        if sys.platform == "win32":
            subprocess.run(["shutdown", "/s", "/t", "10"])
        elif sys.platform == "linux":
            subprocess.run(["shutdown", "-h", "+1"])
        return "Shutting down in 10 seconds"
    except Exception as e:
        return f"Could not shutdown: {e}"