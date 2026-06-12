from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_default_avatar(name='H', size=80):
    img = Image.new('RGB', (size, size), color='#0a0a1a')
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, size-4, size-4], fill='#0055cc')
    initial = name[0].upper() if name else 'H'
    bbox = draw.textbbox((0, 0), initial)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((size-w)//2, (size-h)//2 - 2), initial, fill='white')
    return img

def get_profile_photo():
    photo_path = Path.home() / '.hardik-agent' / 'profile.png'
    if photo_path.exists():
        return Image.open(photo_path)
    return create_default_avatar('H')

def save_profile_photo(source_path):
    dest = Path.home() / '.hardik-agent' / 'profile.png'
    dest.parent.mkdir(exist_ok=True)
    img = Image.open(source_path)
    img = img.resize((80, 80))
    img.save(dest)
    return str(dest)
