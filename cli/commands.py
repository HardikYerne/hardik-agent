import typer
import sys
import subprocess
import platform
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from config.settings import ASSISTANT_NAME, VERSION
from auth.signup import signup, is_registered
from auth.login import login

app = typer.Typer()
console = Console()

def detect_os():
    system = platform.system()
    if system == "Windows":
        return "windows"
    elif system == "Linux":
        return "linux"
    elif system == "Darwin":
        return "macos"
    return "unknown"

def check_ffmpeg():
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            check=True
        )
        return True
    except:
        return False

def install_ffmpeg(os_type):
    console.print("[yellow]Installing FFmpeg...[/yellow]")
    try:
        if os_type == "windows":
            subprocess.run(
                ["winget", "install", "ffmpeg", "--silent"],
                check=True
            )
        elif os_type == "linux":
            subprocess.run(
                ["sudo", "apt-get", "install", "-y", "ffmpeg"],
                check=True
            )
        elif os_type == "macos":
            subprocess.run(
                ["brew", "install", "ffmpeg"],
                check=True
            )
        console.print("[green]FFmpeg installed.[/green]")
        return True
    except Exception as e:
        console.print(f"[red]FFmpeg install failed: {e}[/red]")
        return False

def check_ollama():
    try:
        subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            check=True
        )
        return True
    except:
        return False

def install_ollama(os_type):
    console.print("[yellow]Installing Ollama...[/yellow]")
    try:
        if os_type == "windows":
            subprocess.run(
                ["winget", "install", "Ollama.Ollama", "--silent"],
                check=True
            )
        elif os_type == "linux":
            subprocess.run(
                "curl -fsSL https://ollama.com/install.sh | sh",
                shell=True,
                check=True
            )
        elif os_type == "macos":
            subprocess.run(
                ["brew", "install", "ollama"],
                check=True
            )
        console.print("[green]Ollama installed.[/green]")
        return True
    except Exception as e:
        console.print(f"[red]Ollama install failed: {e}[/red]")
        return False

def pull_llama_model():
    console.print("[yellow]Downloading Llama3 AI model (~4GB)...[/yellow]")
    console.print("[dim]This only happens once. Please wait...[/dim]")
    try:
        subprocess.run(
            ["ollama", "pull", "llama3"],
            check=True
        )
        console.print("[green]Llama3 model ready.[/green]")
        return True
    except Exception as e:
        console.print(f"[red]Model download failed: {e}[/red]")
        return False

def check_model_exists():
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True
        )
        return "llama3" in result.stdout
    except:
        return False

@app.command()
def setup():
    console.print(Panel(
        f"[bold green]Welcome to {ASSISTANT_NAME} Agent v{VERSION}[/bold green]\n"
        "Setting up your AI desktop assistant...",
        title="Hardik Agent Setup"
    ))

    # step 1 - detect OS
    os_type = detect_os()
    console.print(f"\n[blue]System detected: {os_type.upper()}[/blue]")

    # step 2 - check and install FFmpeg
    console.print("\n[bold]Checking FFmpeg...[/bold]")
    if check_ffmpeg():
        console.print("[green]FFmpeg already installed.[/green]")
    else:
        install_ffmpeg(os_type)

    # step 3 - check and install Ollama
    console.print("\n[bold]Checking Ollama...[/bold]")
    if check_ollama():
        console.print("[green]Ollama already installed.[/green]")
    else:
        install_ollama(os_type)

    # step 4 - download AI model
    console.print("\n[bold]Checking AI model...[/bold]")
    if check_model_exists():
        console.print("[green]Llama3 model already downloaded.[/green]")
    else:
        pull_llama_model()

    # step 5 - user registration
    console.print("\n[bold]Setting up your account...[/bold]")
    if is_registered():
        console.print("[yellow]Account already exists.[/yellow]")
    else:
        signup()

    # done
    console.print(Panel(
        "[bold green]Setup complete![/bold green]\n\n"
        "Run this command to start:\n"
        "[bold blue]hardik-agent start[/bold blue]",
        title="Ready"
    ))

@app.command()
def start():
    if not is_registered():
        console.print("[red]No account found. Run: hardik-agent setup[/red]")
        return
    if login():
        console.print(Panel(
            f"[bold blue]{ASSISTANT_NAME} Agent is starting...[/bold blue]\n"
            "Say the wake word to begin.",
            title="Starting"
        ))

@app.command()
def status():
    os_type = detect_os()
    ffmpeg_ok = "✅" if check_ffmpeg() else "❌"
    ollama_ok = "✅" if check_ollama() else "❌"
    model_ok = "✅" if check_model_exists() else "❌"
    registered = "✅" if is_registered() else "❌"

    console.print(Panel(
        f"[bold]System Status[/bold]\n\n"
        f"OS: {os_type.upper()}\n"
        f"FFmpeg: {ffmpeg_ok}\n"
        f"Ollama: {ollama_ok}\n"
        f"Llama3 Model: {model_ok}\n"
        f"Account: {registered}",
        title="Hardik Agent Status"
    ))