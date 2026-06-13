import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.energy_threshold = 200
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 1.0
recognizer.operation_timeout = None

COMMON_CORRECTIONS = {
    'open crow': 'open chrome',
    'open crome': 'open chrome',
    'open cream': 'open chrome',
    'open chrome': 'open chrome',
    'open crumb': 'open chrome',
    'open you tube': 'open youtube',
    'open you too': 'open youtube',
    'what stop': 'whatsapp',
    'what step': 'whatsapp',
    'instagram': 'instagram',
    'in instagram': 'open instagram',
    'vs code': 'open vscode',
    'the score': 'vscode',
    'open the score': 'open vscode',
    'file manager': 'open file manager',
    'take a screenshot': 'take screenshot',
    'screenshot': 'take screenshot',
    'shut down': 'shutdown',
    'volume up': 'increase volume',
    'volume down': 'decrease volume',
    'what time': 'what time is it',
    'battery': 'check battery',
    'check battery': 'check battery',
}

def correct_text(text):
    text_lower = text.lower().strip()
    for wrong, correct in COMMON_CORRECTIONS.items():
        if wrong in text_lower:
            text_lower = text_lower.replace(wrong, correct)
    return text_lower

def transcribe():
    with sr.Microphone() as source:
        print('Listening...')
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print('Processing...')

            # try Indian English first
            try:
                text = recognizer.recognize_google(audio, language='en-IN')
                text = correct_text(text)
                print(f'You said: {text}')
                return text
            except:
                pass

            # fallback to regular English
            try:
                text = recognizer.recognize_google(audio, language='en-US')
                text = correct_text(text)
                print(f'You said: {text}')
                return text
            except:
                pass

            return ''

        except sr.WaitTimeoutError:
            return ''
        except sr.UnknownValueError:
            print('Could not understand')
            return ''
        except Exception as e:
            print(f'Error: {e}')
            return ''
