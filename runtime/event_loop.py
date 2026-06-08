from voice.speech_to_text import transcribe
from voice.text_to_speech import speak
from agent.brain import process_command
from rich.console import Console

console = Console()

def run():
    speak('Hardik Agent is ready.')
    console.print('[bold green]Hardik Agent is running...[/bold green]')
    console.print('[dim]Speak any command. Say stop agent to quit.[/dim]')

    while True:
        try:
            console.print('\n[bold blue]Listening...[/bold blue]')
            text = transcribe()

            if not text or len(text.strip()) < 2:
                console.print('[dim]Nothing heard. Listening again...[/dim]')
                continue

            console.print(f'[yellow]You said: {text}[/yellow]')

            if 'stop agent' in text.lower():
                speak('Goodbye.')
                break

            result = process_command(text)
            speak(result)

        except KeyboardInterrupt:
            speak('Goodbye.')
            break
        except Exception as e:
            console.print(f'[red]Error: {e}[/red]')
            continue
