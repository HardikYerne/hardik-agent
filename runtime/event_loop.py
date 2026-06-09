from voice.speech_to_text import transcribe
from voice.text_to_speech import speak
from agent.langgraph_brain import process_command
from memory.memory_manager import save_command, get_recent_commands, search_memory
from rich.console import Console

console = Console()

def run(auto=False):
    speak('Hardik Agent is ready. How can I help you?')
    console.print('[bold green]Hardik Agent is running with memory...[/bold green]')
    console.print('[dim]Speak any command. Say stop agent to quit.[/dim]')

    while True:
        try:
            console.print('\n[bold blue]Listening...[/bold blue]')
            text = transcribe()

            if not text or len(text.strip()) < 3:
                continue

            console.print(f'[yellow]You said: {text}[/yellow]')

            if 'stop agent' in text.lower():
                speak('Goodbye. Hardik Agent is shutting down.')
                break

            # check memory for context
            if 'last command' in text.lower() or 'what did i say' in text.lower():
                recent = get_recent_commands(3)
                if recent:
                    memory_text = 'Your recent commands were: '
                    for cmd, meta in recent:
                        memory_text += f'{cmd}, '
                    speak(memory_text)
                    continue

            # process command
            result = process_command(text)

            # save to memory
            save_command(text, result)

            speak(result)

        except KeyboardInterrupt:
            speak('Goodbye.')
            break
        except Exception as e:
            console.print(f'[red]Error: {e}[/red]')
            continue
