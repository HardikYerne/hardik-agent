import json
from pathlib import Path
from rich.console import Console
from auth.password_manager import verify_password

console = Console()

CREDENTIALS_FILE = Path.home() / ".hardik-agent" / "credentials.json"

def login() -> bool:
    console.print("\n[bold blue]Login to Hardik Agent[/bold blue]\n")

    import getpass
    email = input("Email: ").strip()
    password = getpass.getpass("Password: ")

    with open(CREDENTIALS_FILE) as f:
        credentials = json.load(f)

    if email != credentials["email"]:
        console.print("[red]Email not found.[/red]")
        return False

    if not verify_password(password, credentials["password"]):
        console.print("[red]Incorrect password.[/red]")
        return False

    console.print(f"\n[bold green]Welcome back! Hardik Agent is ready.[/bold green]")
    return True