import whisper
import sounddevice as sd
import scipy.io.wavfile as wav
import os
import tempfile

model = whisper.load_model('base')

def record_audio(duration=7, sample_rate=16000):
    print('Listening...')
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='int16'
    )
    sd.wait()
    return audio, sample_rate

def transcribe():
    audio, sample_rate = record_audio()
    temp_path = os.path.join(tempfile.gettempdir(), 'hardik_audio.wav')
    wav.write(temp_path, sample_rate, audio)
    result = model.transcribe(
        temp_path,
        language='en',
        fp16=False,
        temperature=0,
        condition_on_previous_text=False,
        initial_prompt='Open apps, search internet, control computer'
    )
    text = result['text'].strip().lower()
    print(f'You said: {text}')
    return text
