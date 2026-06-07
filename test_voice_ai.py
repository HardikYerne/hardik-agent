from voice.speech_to_text import transcribe
from voice.text_to_speech import speak
from agent.brain import process_command

def voice_ai_loop():
    speak('I am listening. Say a command.')
    text = transcribe()
    print(f'You said: {text}')
    result = process_command(text)
    speak(result)

if __name__ == '__main__':
    voice_ai_loop()
