import speech_recognition as sr
import time

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.dynamic_energy_adjustment_damping = 0.15
recognizer.dynamic_energy_ratio = 1.5
recognizer.pause_threshold = 0.8
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.5

NOISE_WORDS = [
    'thank you', 'thanks for watching', 'subscribe',
    'like and subscribe', 'please subscribe', 'bell icon',
    'notification', 'comment below', 'see you next',
    'bye', 'goodbye', 'you', 'the', 'a', 'um', 'uh',
    'hmm', 'okay', 'ok', 'alright', 'so', 'well',
]

CORRECTIONS = {
    'open crow': 'open chrome',
    'open crome': 'open chrome',
    'open cream': 'open chrome',
    'open crumb': 'open chrome',
    'open you tube': 'open youtube',
    'open you too': 'open youtube',
    'what step': 'whatsapp',
    'what stop': 'whatsapp',
    'what sup': 'whatsapp',
    'in instagram': 'open instagram',
    'the score': 'vs code',
    'vs cold': 'vs code',
    'vs coat': 'vs code',
    'file manage': 'file manager',
    'shut down': 'shutdown',
    'screen shot': 'screenshot',
    'volume app': 'volume up',
    'what time': 'what time is it',
    'check better': 'check battery',
    'check better': 'check battery',
    'open settings': 'open settings',
    'open setting': 'open settings',
    'take screenshot': 'take screenshot',
    'take a screenshot': 'take screenshot',
}

def is_noise(text):
    text = text.strip().lower()
    if len(text) < 3:
        return True
    if text in NOISE_WORDS:
        return True
    if len(text.split()) == 1 and text not in ['battery', 'cpu', 'ram', 'disk', 'time', 'ip', 'mute']:
        return True
    return False

def correct(text):
    text = text.lower().strip()
    for wrong, right in CORRECTIONS.items():
        if wrong in text:
            text = text.replace(wrong, right)
    return text

def transcribe():
    with sr.Microphone() as source:
        print('Calibrating microphone...')
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print('Listening...')

        try:
            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=12
            )
        except sr.WaitTimeoutError:
            print('No speech detected')
            return ''

        print('Processing...')

        # try Indian English first
        try:
            text = recognizer.recognize_google(
                audio,
                language='en-IN',
                show_all=False
            )
            text = correct(text.lower().strip())
            if is_noise(text):
                print(f'Noise filtered: {text}')
                return ''
            print(f'You said: {text}')
            return text
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            pass

        # fallback to US English
        try:
            text = recognizer.recognize_google(
                audio,
                language='en-US',
                show_all=False
            )
            text = correct(text.lower().strip())
            if is_noise(text):
                print(f'Noise filtered: {text}')
                return ''
            print(f'You said: {text}')
            return text
        except sr.UnknownValueError:
            print('Could not understand speech')
            return ''
        except sr.RequestError as e:
            print(f'Google STT error: {e}')
            # fallback to offline recognition
            try:
                text = recognizer.recognize_sphinx(audio)
                text = correct(text.lower().strip())
                print(f'You said (offline): {text}')
                return text
            except:
                return ''
        except Exception as e:
            print(f'Error: {e}')
            return ''