from voice.speech_to_text import transcribe
from voice.text_to_speech import speak
from rich.console import Console

console = Console()

def ask_confirmation(message):
    speak(message + ' Say yes to confirm or no to cancel.')
    console.print(f'[yellow]Confirmation: {message}[/yellow]')
    response = transcribe()
    console.print(f'[dim]User said: {response}[/dim]')
    if any(word in response.lower() for word in ['yes', 'confirm', 'sure', 'ok', 'okay', 'do it']):
        speak('Confirmed. Executing.')
        return True
    else:
        speak('Cancelled.')
        return False
