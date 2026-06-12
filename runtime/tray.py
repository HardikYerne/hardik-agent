import pystray
from PIL import Image, ImageDraw
import threading
import sys
import os

def create_icon_image():
    img = Image.new('RGB', (64, 64), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, 60, 60], fill='#0066cc')
    draw.text((22, 18), 'H', fill='white')
    return img

def run_tray(stop_event):
    try:
        def on_start(icon, item):
            pass

        def on_stop(icon, item):
            stop_event.set()
            icon.stop()

        def on_exit(icon, item):
            stop_event.set()
            icon.stop()
            sys.exit(0)

        menu = pystray.Menu(
            pystray.MenuItem('Hexa Agent - Running', None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Stop Listening', on_stop),
            pystray.MenuItem('Exit', on_exit)
        )

        icon = pystray.Icon(
            'Hexa_agent',
            create_icon_image(),
            'Hexa Agent',
            menu
        )

        icon.run()

    except Exception as e:
        print(f'Tray error: {e}')

