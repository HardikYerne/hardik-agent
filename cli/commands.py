import typer
from rich.console import Console
from rich.panel import Panel
from config.settings import ASSISTANT_NAME, VERSION

app = typer.Typer()
console = Console()

@app.command()
def setup():
    console.print(Panel(f"[bold green]Welcome to {ASSISTANT_NAME} Agent[/bold green]\nRunning first-time setup...", title="Setup"))

@app.command()
def start():
    console.print(Panel(f"[bold blue]{ASSISTANT_NAME} Agent v{VERSION} is starting...[/bold blue]\nSay the wake word to begin.", title="Starting"))

@app.command()
def status():
    console.print(Panel("[bold yellow]Agent Status[/bold yellow]\n[green]Runtime: Active[/green]\n[green]Voice: Ready[/green]\n[green]Tools: Loaded[/green]", title="Status"))