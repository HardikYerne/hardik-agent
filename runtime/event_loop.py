from voice.speech_to_text import transcribe
from voice.text_to_speech import speak
from agent.langgraph_brain import process_command
from memory.memory_manager import save_command, get_recent_commands
from rich.console import Console

console = Console()

def listen_for_wakeword_simple():
    from voice.speech_to_text import transcribe
    text = transcribe()
    wake_words = ['h', 'computer', 'hey hardik', 'ok hardik', 'agent']
    if any(word in text.lower() for word in wake_words):
        return True
    return False

def run(auto=False):
    speak('Hardik Agent is ready. Say Hardik to activate me.')
    console.print('[bold green]Hardik Agent is running...[/bold green]')
    console.print('[dim]Say "Hardik" to activate. Say "stop agent" to quit.[/dim]')

    while True:
        try:
            console.print('\n[bold cyan]Waiting for wake word...[/bold cyan]')

            # listen for wake word
            wake_text = transcribe()

            if not wake_text:
                continue

            # check stop
            if 'stop agent' in wake_text.lower():
                speak('Goodbye. Hardik Agent is shutting down.')
                break

            # check wake word
            wake_words = ['hardik', 'computer', 'hey hardik', 'ok hardik', 'agent', 'hello']
            if any(word in wake_text.lower() for word in wake_words):
                speak('Yes, I am listening.')
                console.print('[bold green]Activated! Listening for command...[/bold green]')

                # listen for actual command
                command = transcribe()

                if not command or len(command.strip()) < 3:
                    speak('I did not hear a command. Please try again.')
                    continue

                console.print(f'[yellow]Command: {command}[/yellow]')

                # check memory commands
                if 'last command' in command.lower() or 'what did i say' in command.lower():
                    recent = get_recent_commands(3)
                    if recent:
                        memory_text = 'Your recent commands were: '
                        for cmd, meta in recent:
                            memory_text += f'{cmd}, '
                        speak(memory_text)
                        continue

                # process command
                result = process_command(command)

                # save to memory
                save_command(command, result)

                # speak result
                speak(result)

            else:
                console.print(f'[dim]Heard: {wake_text} - waiting for wake word...[/dim]')

        except KeyboardInterrupt:
            speak('Goodbye.')
            break
        except Exception as e:
            console.print(f'[red]Error: {e}[/red]')
            continue
