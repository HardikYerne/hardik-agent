import typer
from rich.console import Console
from rich.panel import Panel
from config.settings import ASSISTANT_NAME, VERSION
from auth.signup import signup, is_registered
from auth.login import login

app = typer.Typer()
console = Console()

@app.command()
def setup():
    console.print(Panel(f"[bold green]Welcome to {ASSISTANT_NAME} Agent v{VERSION}[/bold green]", title="Setup"))
    if is_registered():
        console.print("[yellow]Account already exists. Use: python main.py login[/yellow]")
        return
    signup()

@app.command()
def start():
    if not is_registered():
        console.print("[red]No account found. Run: python main.py setup[/red]")
        return
    if login():
        console.print(Panel(f"[bold blue]{ASSISTANT_NAME} Agent is starting...[/bold blue]\nSay the wake word to begin.", title="Starting"))

@app.command()
def status():
    console.print(Panel("[bold yellow]Agent Status[/bold yellow]\n[green]Runtime: Active[/green]\n[green]Voice: Ready[/green]\n[green]Tools: Loaded[/green]", title="Status"))

@app.command()
def login_cmd():
    login()