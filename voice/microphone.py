from voice.speech_to_text import transcribe
from voice.text_to_speech import speak

def listen_and_respond():
    speak("I am listening")
    text = transcribe()
    speak(f"You said: {text}")
    return text