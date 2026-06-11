import typer
import subprocess
import platform
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from config.settings import ASSISTANT_NAME, VERSION
from auth.signup import signup, is_registered
from auth.login import login
from auth.session import save_session, is_session_active, clear_session

app = typer.Typer()
console = Console()

def detect_os():
    system = platform.system()
    if system == 'Windows': return 'windows'
    elif system == 'Linux': return 'linux'
    elif system == 'Darwin': return 'macos'
    return 'unknown'

def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except: return False

def check_ollama():
    try:
        subprocess.run(['ollama', '--version'], capture_output=True, check=True)
        return True
    except: return False

def check_model_exists():
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        return 'llama3' in result.stdout
    except: return False

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
        console.print('[green]FFmpeg ready.[/green]')
    console.print('\n[bold]Checking Ollama...[/bold]')
    if check_ollama():
        console.print('[green]Ollama ready.[/green]')
    console.print('\n[bold]Checking AI model...[/bold]')
    if check_model_exists():
        console.print('[green]AI model ready.[/green]')
    console.print('\n[bold]Setting up account...[/bold]')
    if is_registered():
        console.print('[yellow]Account already exists.[/yellow]')
    else:
        signup()

    add_startup = input('\nStart Hardik Agent automatically on Windows boot? (y/n): ')
    if add_startup.lower() == 'y':
        from runtime.startup import add_to_startup
        result = add_to_startup()
        console.print(f'[green]{result}[/green]')

    console.print(Panel(
        '[bold green]Setup complete![/bold green]\n\nRun: py -3.12 main.py start',
        title='Ready'
    ))

@app.command()
def start():
    if not is_registered():
        console.print('[red]No account found. Run: py -3.12 main.py setup[/red]')
        return
    if is_session_active():
        console.print('[green]Auto login successful.[/green]')
    else:
        logged_in = login()
        if not logged_in:
            return
        save_session('active')
    console.print(Panel(
        f'[bold blue]{ASSISTANT_NAME} Agent v{VERSION} starting...[/bold blue]\nListening for your commands.',
        title='Starting'
    ))
    from runtime.event_loop import run
    run()

@app.command()
def stop():
    clear_session()
    console.print('[yellow]Hardik Agent stopped.[/yellow]')

@app.command()
def status():
    os_type = detect_os()
    from runtime.startup import is_in_startup
    console.print(Panel(
        f'[bold]System Status[/bold]\n\n'
        f'OS: {os_type.upper()}\n'
        f'FFmpeg: {"OK" if check_ffmpeg() else "MISSING"}\n'
        f'Ollama: {"OK" if check_ollama() else "MISSING"}\n'
        f'AI Model: {"OK" if check_model_exists() else "MISSING"}\n'
        f'Account: {"OK" if is_registered() else "MISSING"}\n'
        f'Session: {"ACTIVE" if is_session_active() else "NOT ACTIVE"}\n'
        f'Auto Startup: {"YES" if is_in_startup() else "NO"}',
        title='Hardik Agent Status'
    ))

@app.command()
def add_startup():
    from runtime.startup import add_to_startup
    result = add_to_startup()
    console.print(f'[green]{result}[/green]')

@app.command()
def remove_startup():
    from runtime.startup import remove_from_startup
    result = remove_from_startup()
    console.print(f'[green]{result}[/green]')
