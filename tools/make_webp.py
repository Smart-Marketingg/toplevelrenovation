#!/usr/bin/env python3
"""Make a .webp next to every .jpg under images/ (skips ones already up to date).
build.py points pages at the .webp when it exists; the .jpg stays for og:image,
schema and as the source. Needs Pillow:  pip install Pillow

    python3 tools/make_webp.py
"""
import os
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'images')
n = jpg = webp = 0
for d, _, files in os.walk(ROOT):
    for f in files:
        if not f.lower().endswith('.jpg'):
            continue
        src = os.path.join(d, f); dst = src[:-4] + '.webp'
        if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
            Image.open(src).convert('RGB').save(dst, 'WEBP', quality=72, method=6)
            n += 1
        jpg += os.path.getsize(src); webp += os.path.getsize(dst)
print(f'{n} converted; jpg {jpg / 1e6:.1f} MB -> webp {webp / 1e6:.1f} MB')
