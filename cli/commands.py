import typer
import subprocess
import platform
from rich.console import Console
from rich.panel import Panel
from config.settings import ASSISTANT_NAME, VERSION
from auth.signup import signup, is_registered
from auth.login import login

app = typer.Typer()
console = Console()

def detect_os():
    system = platform.system()
    if system == 'Windows':
        return 'windows'
    elif system == 'Linux':
        return 'linux'
    elif system == 'Darwin':
        return 'macos'
    return 'unknown'

def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except:
        return False

def check_ollama():
    try:
        subprocess.run(['ollama', '--version'], capture_output=True, check=True)
        return True
    except:
        return False

def check_model_exists():
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        return 'llama3' in result.stdout
    except:
        return False

@app.command()
def setup():
    console.print(Panel(
        f'[bold green]Welcome to {ASSISTANT_NAME} Agent v{VERSION}[/bold green]\nSetting up your AI desktop assistant...',
        title='Hardik Agent Setup'
    ))
    os_type = detect_os()
    console.print(f'\n[blue]System detected: {os_type.upper()}[/blue]')
    console.print('\n[bold]Checking FFmpeg...[/bold]')
    if check_ffmpeg():
        console.print('[green]FFmpeg already installed.[/green]')
    console.print('\n[bold]Checking Ollama...[/bold]')
    if check_ollama():
        console.print('[green]Ollama already installed.[/green]')
    console.print('\n[bold]Checking AI model...[/bold]')
    if check_model_exists():
        console.print('[green]AI model already downloaded.[/green]')
    console.print('\n[bold]Setting up your account...[/bold]')
    if is_registered():
        console.print('[yellow]Account already exists.[/yellow]')
    else:
        signup()
    console.print(Panel(
        '[bold green]Setup complete![/bold green]\n\nRun this command to start:\n[bold blue]py -3.12 main.py start[/bold blue]',
        title='Ready'
    ))

@app.command()
def start():
    if not is_registered():
        console.print('[red]No account found. Run: py -3.12 main.py setup[/red]')
        return
    if login():
        console.print(Panel(
            f'[bold blue]{ASSISTANT_NAME} Agent v{VERSION} starting...[/bold blue]\nSay Hardik to activate.',
            title='Starting'
        ))
        from runtime.event_loop import run
        run()

@app.command()
def status():
    os_type = detect_os()
    ffmpeg_ok = 'OK' if check_ffmpeg() else 'MISSING'
    ollama_ok = 'OK' if check_ollama() else 'MISSING'
    model_ok = 'OK' if check_model_exists() else 'MISSING'
    registered = 'OK' if is_registered() else 'MISSING'
    console.print(Panel(
        f'[bold]System Status[/bold]\n\nOS: {os_type.upper()}\nFFmpeg: {ffmpeg_ok}\nOllama: {ollama_ok}\nAI Model: {model_ok}\nAccount: {registered}',
        title='Hardik Agent Status'
    ))
