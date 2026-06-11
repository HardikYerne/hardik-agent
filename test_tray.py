from PIL import Image, ImageDraw
import pystray

def create_icon():
    img = Image.new('RGB', (64, 64), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, 60, 60], fill='#0066cc')
    return img

def on_exit(icon, item):
    icon.stop()

menu = pystray.Menu(
    pystray.MenuItem('Hardik Agent Running', None, enabled=False),
    pystray.MenuItem('Exit', on_exit)
)

icon = pystray.Icon('hardik_agent', create_icon(), 'Hardik Agent', menu)
print('Tray icon starting...')
icon.run()
