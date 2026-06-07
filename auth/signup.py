import json
import os
import getpass
from pathlib import Path
from rich.console import Console
from auth.password_manager import hash_password, validate_password

console = Console()

PROFILE_DIR = Path.home() / ".hardik-agent"
CREDENTIALS_FILE = PROFILE_DIR / "credentials.json"

def is_registered():
    return CREDENTIALS_FILE.exists()

def signup():
    console.print("\n[bold green]Create your Hardik Agent account[/bold green]\n")

    email = input("Enter your email: ").strip()
    if not email or "@" not in email:
        console.print("[red]Invalid email address.[/red]")
        return False

    while True:
        password = getpass.getpass("Create password: ")
        valid, message = validate_password(password)
        if not valid:
            console.print(f"[red]{message}[/red]")
            continue
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            console.print("[red]Passwords do not match. Try again.[/red]")
            continue
        break

    PROFILE_DIR.mkdir(exist_ok=True)
    credentials = {
        "email": email,
        "password": hash_password(password)
    }
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(credentials, f)

    console.print("\n[bold green]Account created successfully![/bold green]")
    return True