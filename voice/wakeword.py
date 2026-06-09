import struct
import pyaudio
import pvporcupine
from rich.console import Console

console = Console()

def listen_for_wakeword():
    porcupine = None
    pa = None
    audio_stream = None

    try:
        # use built-in wake word "hey siri" style
        # for free we use "computer" or "jarvis" keyword
        porcupine = pvporcupine.create(
            keywords=['computer'],
        )

        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        console.print('[dim]Waiting for wake word "Computer"...[/dim]')

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                console.print('[green]Wake word detected![/green]')
                return True

    except Exception as e:
        console.print(f'[red]Wake word error: {e}[/red]')
        return False

    finally:
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()
        if porcupine is not None:
            porcupine.delete()
