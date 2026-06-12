import whisper
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import os
import tempfile

model = whisper.load_model('base')

NOISE_THRESHOLD = 400

def record_audio(duration=6, sample_rate=16000):
    print('Listening...')
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='int16'
    )
    sd.wait()
    return audio, sample_rate

def is_real_speech(audio):
    volume = np.abs(audio).mean()
    print(f'Volume level: {volume:.1f}')
    return volume > NOISE_THRESHOLD

def transcribe():
    audio, sample_rate = record_audio()

    if not is_real_speech(audio):
        print('Too quiet - skipping')
        return ''

    temp_path = os.path.join(tempfile.gettempdir(), 'hexa_audio.wav')
    wav.write(temp_path, sample_rate, audio)

    result = model.transcribe(
        temp_path,
        language='en',
        fp16=False,
        temperature=0,
        condition_on_previous_text=False
    )

    text = result['text'].strip().lower()

    # clean up common whisper hallucinations
    hallucinations = [
        'thank you', 'thanks for watching', 'subscribe',
        'like and subscribe', 'see you next time',
        'you', 'bye', 'okay', 'um', 'uh'
    ]

    for h in hallucinations:
        if text == h or text == h + '.':
            print(f'Hallucination detected: {text}')
            return ''

    if len(text) < 3:
        return ''

    print(f'You said: {text}')
    return text
