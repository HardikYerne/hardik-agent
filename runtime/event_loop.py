import threading
from voice.speech_to_text import transcribe
from voice.text_to_speech import speak
from agent.langgraph_brain import process_command
from memory.memory_manager import save_command, get_recent_commands
from rich.console import Console

console = Console()

def confirm_command(text):
    speak(f'You said {text}. Say yes to confirm or repeat your command.')
    response = transcribe()
    if not response:
        return False
    if any(word in response.lower() for word in ['yes', 'correct', 'right', 'confirm', 'ok', 'okay', 'yeah', 'yep']):
        return True
    return False

def run(auto=False):
    speak('Hexa is ready.')
    console.print('[bold green]Hexa is running...[/bold green]')
    console.print('[dim]Speak any command. Say stop agent to quit.[/dim]')

    stop_event = threading.Event()
    try:
        from runtime.tray import run_tray
        tray_thread = threading.Thread(target=run_tray, args=(stop_event,), daemon=True)
        tray_thread.start()
    except Exception as e:
        console.print(f'[dim]Tray not available: {e}[/dim]')

    while True:
        try:
            if stop_event.is_set():
                speak('Goodbye.')
                break

            console.print('\n[bold blue]Listening...[/bold blue]')
            text = transcribe()

            if not text or len(text.strip()) < 3:
                continue

            console.print(f'[yellow]You said: {text}[/yellow]')

            if 'stop agent' in text.lower():
                speak('Goodbye. Hexa is shutting down.')
                break

            if 'last command' in text.lower() or 'what did i say' in text.lower():
                recent = get_recent_commands(3)
                if recent:
                    memory_text = 'Your recent commands were: '
                    for cmd, meta in recent:
                        memory_text += f'{cmd}, '
                    speak(memory_text)
                    continue

            # confirm before executing
            confirmed = confirm_command(text)
            if not confirmed:
                speak('Please repeat your command.')
                continue

            result = process_command(text)
            save_command(text, result)
            speak(result)

        except KeyboardInterrupt:
            speak('Goodbye.')
            break
        except Exception as e:
            console.print(f'[red]Error: {e}[/red]')
            continue
