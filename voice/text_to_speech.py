import pyttsx3

def speak(text: str):
    print(f"Agent: {text}")
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('rate', 175)
        engine.setProperty('volume', 0.9)
        if voices:
            engine.setProperty('voice', voices[0].id)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"TTS error: {e}")
        print(f"(speaking): {text}")